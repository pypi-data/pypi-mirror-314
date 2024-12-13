from anymail.signals import inbound
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.module_loading import autodiscover_modules


class ImportExportConfig(AppConfig):
    name = "wbcore.contrib.io"

    def ready(self):
        """
        registered source from settings
        """
        # Implicitly connect a signal handlers decorated with @receiver.
        from wbcore.contrib.io.management import load_sources_from_settings

        from .backends.mail import handle_inbound

        # Explicitly connect a signal handler.
        inbound.connect(handle_inbound)

        autodiscover_modules("import_export.backends")

        post_migrate.connect(
            load_sources_from_settings,
            dispatch_uid="wbcore.contrib.io.load_sources_from_settings",
        )
