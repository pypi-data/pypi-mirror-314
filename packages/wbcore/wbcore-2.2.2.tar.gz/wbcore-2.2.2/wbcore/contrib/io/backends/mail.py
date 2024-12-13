import re
from datetime import datetime
from io import BytesIO, StringIO
from typing import Generator, Optional

from anymail.inbound import AnymailInboundMessage
from django.conf import settings
from django.db.models import Model, Q
from dynamic_preferences.registries import global_preferences_registry
from slugify import slugify

from ..models import Source
from .abstract import AbstractDataBackend
from .utils import register


@register("Default Mail", save_data_in_import_source=True, passive_only=True)
class DataBackend(AbstractDataBackend):
    def get_files(
        self,
        execution_time: datetime,
        file_name_regex: Optional[str] = None,
        message: Optional[AnymailInboundMessage] = None,
        import_credential: Optional[Model] = None,
        import_email_as_file: Optional[bool] = False,
        **kwargs,
    ) -> Generator[tuple[str, BytesIO], None, None]:
        """

        Args:
            execution_time: The time at which this import was called
            file_name_regex: The regex applied on the imported file for validation. Defaults to False.
            message: The AnymailInboundMessage received from the anymail inbounc
            import_credential: Import credential attached to the calling source. Defaults to None.
            import_email_as_file: If false, import the attachment as import source file. Otherwise, import the whole email as file
            **kwargs:

        Returns:

        """
        if message:
            if import_email_as_file:
                filename = f"{slugify(message.subject)}_{datetime.timestamp(execution_time)}.eml"
                yield filename, StringIO(message.as_string())
            elif file_name_regex:
                attachments = message.attachments
                attachments.extend(message.inline_attachments.values())

                for attachment in attachments:
                    f = attachment.as_uploaded_file()
                    f_name = attachment.get_filename()
                    result = re.findall(file_name_regex, f_name)
                    if len(result) > 0:
                        yield f_name, f.file


def is_sender_allowed(from_email: str, whitelisted_emails: list[str], admin_mails: list[str]) -> bool:
    if from_email in admin_mails:
        return True
    for whitelisted_email in whitelisted_emails:
        if re.search(whitelisted_email, from_email):
            return True
    return False


def handle_inbound(sender, event, esp_name, **kwargs):
    spam_detected = False
    if (message := event.message) and (from_email := message.from_email.addr_spec) and (subject := message.subject):
        if spam_score := getattr(settings, "WBIMPORT_EXPORT_MAILBACKEND_SPAMSCORE", None):
            spam_detected = message.spam_detected or message.spam_score >= spam_score
        if not spam_detected:
            admin_emails = global_preferences_registry.manager()["io__administrator_mails"].split(";")
            conditions = Q(import_parameters__inbound_address__isnull=True)
            for t in message.to:
                conditions |= Q(import_parameters__inbound_address__contains=t.addr_spec)

            sources = Source.objects.filter(
                conditions & Q(data_backend__backend_class_path="wbcore.contrib.io.backends.mail") & Q(is_active=True)
            )
            if s := re.search(r"\[([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})\]", subject):
                sources = sources.filter(uuid=s.group(1))

            for source in sources:
                if is_sender_allowed(from_email, source.import_parameters.get("whitelisted_emails", []), admin_emails):
                    source.trigger_workflow(message=message)
