from wbcore import serializers
from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)


class NotificationTypeRepresentationSerializer(serializers.RepresentationSerializer):
    class Meta:
        model = NotificationType
        fields = (
            "id",
            "code",
            "title",
            "help_text",
        )


class NotificationTypeSettingModelSerializer(serializers.ModelSerializer):
    _notification_type = NotificationTypeRepresentationSerializer(source="notification_type")
    help_text = serializers.CharField()

    class Meta:
        read_only_fields = ("user", "notification_type")
        model = NotificationTypeSetting
        fields = (
            "id",
            "notification_type",
            "_notification_type",
            "help_text",
            "user",
            "enable_web",
            "enable_mobile",
            "enable_email",
            "_additional_resources",
        )
