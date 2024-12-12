from contextlib import suppress

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.utils import get_anonymous_user
from wbcore.models import WBModel


class NotificationType(WBModel):
    code = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, default="")
    help_text = models.CharField(max_length=512, default="")

    stale = models.BooleanField(default=False)
    contenttype = models.ForeignKey(
        to="contenttypes.ContentType", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    default_enable_web = models.BooleanField(default=False)
    default_enable_mobile = models.BooleanField(default=False)
    default_enable_email = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Notification Type"
        verbose_name_plural = "Notification Types"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:notifications:notification_type"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:notifications:notification_type_representation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"


class NotificationTypeSetting(WBModel):
    notification_type = models.ForeignKey(
        to="notifications.NotificationType", related_name="user_settings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=get_user_model(), related_name="wbnotification_user_settings", on_delete=models.CASCADE
    )

    enable_web = models.BooleanField(default=False)
    enable_mobile = models.BooleanField(default=False)
    enable_email = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user}: {self.notification_type} ({self.enable_web}/{self.enable_mobile}/{self.enable_email})"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:notifications:notification_type_setting"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:notifications:notification_type_setting_representation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{notification_type}}"


@receiver(post_save, sender="notifications.NotificationType")
def post_save_notification_type(instance, **kwargs):
    anonymous_user = get_anonymous_user()
    for user in get_user_model().objects.filter(~models.Q(pk=anonymous_user.pk)):
        NotificationTypeSetting.objects.get_or_create(
            notification_type=instance,
            user=user,
            defaults={
                "enable_web": instance.default_enable_web,
                "enable_mobile": instance.default_enable_mobile,
                "enable_email": instance.default_enable_email,
            },
        )


@receiver(post_save, sender=get_user_model())
def post_save_user(instance, **kwargs):
    with suppress(get_user_model().DoesNotExist):
        anonymous_user = get_anonymous_user()
        if instance.pk == anonymous_user.pk:
            return

    for notification_type in NotificationType.objects.all():
        NotificationTypeSetting.objects.get_or_create(
            notification_type=notification_type,
            user=instance,
            defaults={
                "enable_web": notification_type.default_enable_web,
                "enable_mobile": notification_type.default_enable_mobile,
                "enable_email": notification_type.default_enable_email,
            },
        )
