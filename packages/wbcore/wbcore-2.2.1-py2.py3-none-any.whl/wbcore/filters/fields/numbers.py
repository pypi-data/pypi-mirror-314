import django_filters
from wbcore.filters.mixins import WBCoreFilterMixin


class NumberFilter(WBCoreFilterMixin, django_filters.NumberFilter):
    filter_type = "number"

    def __init__(self, precision: int = 0, percent: bool = False, delimiter=",", decimal_mark=".", *args, **kwargs):
        self.precision = precision
        self.percent = percent
        self.delimiter = delimiter
        self.decimal_mark = decimal_mark
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        representation["precision"] = self.precision
        representation["delimiter"] = self.delimiter
        representation["decimal_mark"] = self.decimal_mark
        return representation, lookup_expr

    def filter(self, qs, value):
        if self.percent and value is not None:
            value /= 100
        return super().filter(qs, value)


class YearFilter(NumberFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delimiter = ""
        self.decimal_mark = "."


class RangeSelectFilter(NumberFilter):
    filter_type = "rangeselect"

    def __init__(self, precision=2, *args, **kwargs):
        self.precision = precision
        self.color = kwargs.pop("color", "rgb(133, 144, 162)")
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["color"] = self.color
        return representation, lookup_expr
