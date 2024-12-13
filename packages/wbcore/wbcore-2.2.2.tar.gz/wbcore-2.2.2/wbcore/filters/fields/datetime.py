from contextlib import suppress

import django_filters
from wbcore.filters.mixins import WBCoreFilterMixin
from wbcore.forms import DateRangeField, DateTimeRangeField
from wbcore.utils.date import financial_performance_shortcuts
from wbcore.utils.date_builder.components import Component


class TimeFilter(WBCoreFilterMixin, django_filters.TimeFilter):
    filter_type = "time"


class DateTimeFilter(WBCoreFilterMixin, django_filters.DateTimeFilter):
    filter_type = "datetime"


class DateFilter(WBCoreFilterMixin, django_filters.DateFilter):
    filter_type = "date"


class ShortcutAndPerformanceMixin(WBCoreFilterMixin):
    def __init__(self, shortcuts: list | None = None, performance_mode: bool = False, *args, **kwargs):
        self.shortcuts = shortcuts
        self.performance_mode = performance_mode
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        representation["performance_mode"] = self.performance_mode

        if self.shortcuts:
            representation["shortcuts"] = self.shortcuts

        return representation, lookup_expr


class DateRangeFilter(ShortcutAndPerformanceMixin, django_filters.Filter):
    field_class = DateRangeField
    filter_type = "daterange"
    default_format = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "overlap")
        super().__init__(*args, **kwargs)

    def _get_default(self, *args):
        default = super()._get_default(*args)
        if default is not None:
            lower = upper = None
            if isinstance(default, tuple):
                lower, upper = default

                # if the default is a tuple of components, we need to convert them to string
                if isinstance(lower, Component) and isinstance(upper, Component):
                    return f"{lower},{upper}"

            elif hasattr(default, "lower") and hasattr(default, "upper"):
                lower, upper = default.lower, default.upper
            default = f'{lower.strftime(self.default_format) if lower else ""},{upper.strftime(self.default_format) if upper else ""}'
        return default

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        representation["lookup_expr"] = {"exact": self.field_name}
        with suppress(KeyError):  # TODO frontend needs to support both exact and overlaps lookup
            default = representation["default"].pop(self.lookup_expr)
            representation["default"]["exact"] = default

        return representation, lookup_expr

    @classmethod
    def base_date_range_filter_method(cls, queryset, field_name, value):
        if value:
            filters = {}
            if value.lower:
                filters[f"{field_name}__gte"] = value.lower
            if value.upper:
                filters[f"{field_name}__lte"] = value.upper
            return queryset.filter(**filters)
        return queryset


class FinancialPerformanceDateRangeFilter(DateRangeFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(performance_mode=True, shortcuts=financial_performance_shortcuts, *args, **kwargs)


class DateTimeRangeFilter(DateRangeFilter):
    field_class = DateTimeRangeField
    default_format = "%Y-%m-%dT%H:%M:%S%z"
