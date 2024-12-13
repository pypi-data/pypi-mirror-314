from contextlib import suppress

from django_filters.utils import get_model_field

from .lookups import get_lookup_icon, get_lookup_label


class WBCoreFilterMixin:
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        self.initial = kwargs.pop("initial", None)
        self.required = kwargs.pop("required", False)
        self.clearable = kwargs.pop("clearable", True)  # TODO: Take away
        self.hidden = kwargs.pop("hidden", False)
        self.column_field_name = kwargs.pop("column_field_name", None)
        self.help_text = kwargs.pop("help_text", None)
        self.allow_empty_default = kwargs.pop("allow_empty_default", False)
        self.label_format = kwargs.pop(
            "label_format",
            getattr(self, "default_label_format", "{{field_label}} {{operation_icon}}  {{value_label}}"),
        )
        self.lookup_icon = kwargs.pop("lookup_icon", None)
        self.lookup_label = kwargs.pop("lookup_label", None)
        self.depends_on = kwargs.pop("depends_on", [])
        super().__init__(*args, **kwargs)

    @property
    def key(self):
        return self.column_field_name if self.column_field_name else self.field_name

    def get_label(self):
        if self.label is None:  # if label is not provided we gracefully convert the field name into capitalized label
            return self.field_name.replace("_", " ").title()
        else:
            return self.label

    def _get_default(self, request, view):
        # We consider the case where default is a boolean with value False.
        if callable(self.default):
            default = self.default(self, request, view)
        elif (
            isinstance(self.default, str)
            and (callable_default := getattr(self, self.default, None))
            and (callable(callable_default))
        ):
            default = callable_default(self, request, view)
        else:
            default = self.default

        return default

    def _validate_default_with_request(self, default, request, name):
        if request_default := request.GET.get(name):
            return request_default
        return default

    def get_help_text(self) -> str:
        if self.help_text:
            return self.help_text
        with suppress(AttributeError):
            field = get_model_field(self.parent._meta.model, self.field_name)
            if field.help_text:
                return field.help_text
        if self.label:
            return "Filter by " + self.label

    def get_representation(self, request, name, view):
        if self.hidden:
            return {}

        representation = {
            "key": self.key,
            "label_format": self.label_format,
            "label": self.get_label(),
            "help_text": self.get_help_text(),
        }
        lookup_expr = {
            "label": get_lookup_label(self.lookup_expr) if self.lookup_label is None else self.lookup_label,
            "icon": get_lookup_icon(self.lookup_expr) if self.lookup_icon is None else self.lookup_icon,
            "key": name,
            "hidden": self.hidden,
            "input_properties": {
                "type": self.filter_type,
            },
        }
        default = self._get_default(request, view)
        if default is not None or self.allow_empty_default:
            lookup_expr["input_properties"]["default"] = default

        initial = None
        if callable(self.initial):
            initial = self.initial(self, request, view)
        elif (
            isinstance(self.initial, str)
            and (callable_initial := getattr(self, self.initial, None))
            and (callable(callable_initial))
        ):
            initial = callable_initial(self, request, view)
        else:
            initial = self.initial

        if _initial := self._validate_default_with_request(initial, request, name):
            initial = _initial

        if initial is not None:
            lookup_expr["input_properties"]["initial"] = initial

        if self.required:
            lookup_expr["input_properties"]["required"] = True
            # assert representation["default"] != {}, "If a filter is required, it needs at least one default value"
        representation["depends_on"] = self.depends_on
        return representation, lookup_expr
