from wbcore.metadata.configs.display import Field, ListDisplay
from wbcore.metadata.configs.display.instance_display import Display
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class NotificationTypeSettingDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> ListDisplay:
        return ListDisplay(
            fields=[
                Field(key="notification_type", label="Notification"),
                Field(key="help_text", label="Help Text"),
                Field(key="enable_web", label="Web"),
                Field(key="enable_mobile", label="Mobile"),
                Field(key="enable_email", label="E-Mail"),
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["notification_type", "notification_type", "notification_type"],
                ["enable_web", "enable_mobile", "enable_email"],
            ]
        )
