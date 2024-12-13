from contextlib import suppress

from django.utils.text import slugify
from rest_framework.request import Request
from rest_framework.views import View
from wbcore.metadata.configs.display.instance_display.display import Display
from wbcore.metadata.configs.display.list_display import ListDisplay
from wbcore.metadata.configs.display.windows import Window

from ..base import WBCoreViewConfig
from .models import AppliedPreset


class DisplayViewConfig(WBCoreViewConfig):
    metadata_key = "display"
    config_class_attribute = "display_config_class"

    def __init__(self, view: View, request: Request, instance: bool | None = None):
        self.tooltip = request.GET.get("tooltip", None) == "true"
        self.inline = request.GET.get("inline", None) == "true"
        super().__init__(view, request, instance)

    def get_window(self) -> Window | None:
        return None

    def get_instance_display(self) -> Display | None:
        return None

    def get_list_display(self) -> ListDisplay | None:
        return None

    def get_preview_display(self) -> Display | None:
        return None

    def get_metadata(self) -> dict:
        display = dict()
        instance_display = self.get_instance_display()
        if isinstance(instance_display, Display):
            display["instance"] = instance_display.serialize(view_config=self, view=self.view, request=self.request)
        elif instance_display:
            display["instance"] = list(instance_display)
        else:
            display["instance"] = Display(pages=[]).serialize()

        if not self.instance:
            list_display = self.get_list_display()
            if isinstance(list_display, Display):
                display["list"] = list_display.serialize()
            else:
                display["list"] = dict(list_display or {})

        if window := self.get_window():
            display["window"] = window.serialize()

        # We get the path from the header (if it exists, only for nested tables inside forms) and then join it
        # with the current display identifier. If there is an applied preset for this user - we return it.
        path = self.request.META.get("HTTP_WB_DISPLAY_IDENTIFIER", None)
        display_identifier = self.view.display_identifier_config_class(
            self.view, self.request, self.instance
        ).get_display_identifier()
        display_identifier_path = ".".join(filter(lambda element: element is not None, [path, display_identifier]))

        with suppress(AppliedPreset.DoesNotExist):
            display["preset"] = AppliedPreset.objects.get(
                user=self.request.user, display_identifier_path=display_identifier_path
            ).display

        return display


class DisplayIdentifierViewConfig(WBCoreViewConfig):
    metadata_key = "display_identifier"
    config_class_attribute = "display_identifier_config_class"

    def get_display_identifier(self) -> str:
        display = self.view.display_config_class
        slugified_display_module = slugify(display.__module__.replace(".", "-"))
        slugified_display_class = slugify(display.__name__)
        return f"{slugified_display_module}-{slugified_display_class}"

    def get_metadata(self):
        return self.get_display_identifier()
