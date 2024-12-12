from collections import defaultdict
from dataclasses import dataclass
from typing import List

from wbcore.serializers.fields.types import DisplayMode


@dataclass
class _BaseField:
    key: str
    label: str
    type: str = None
    decorators: List = None
    help_text: str = None

    def to_dict(self):
        base = {"key": self.key, "label": self.label, "type": self.type}
        if self.decorators:
            base["decorators"] = self.decorators

        for _attr in ["help_text", "extra"]:
            attr = getattr(self, _attr, None)
            if attr:
                base[_attr] = attr
        return base


@dataclass
class PKField(_BaseField):
    type: str = "primary_key"


@dataclass
class CharField(_BaseField):
    type: str = "text"


@dataclass
class DateField(_BaseField):
    type: str = "date"


@dataclass
class DateRangeField(_BaseField):
    type: str = "daterange"


@dataclass
class BooleanField(_BaseField):
    type: str = "boolean"


@dataclass
class TextField(_BaseField):
    type: str = "texteditor"


@dataclass
class EmojiRatingField(_BaseField):
    type: str = "emojirating"


@dataclass
class FloatField(_BaseField):
    type: str = "number"
    precision: int = 2
    delimiter: str = ","
    decimal_mark: str = "."
    percent: bool = False
    display_mode: DisplayMode = None

    def to_dict(self):
        base = super().to_dict()
        base.update(
            {
                "precision": self.precision,
                "delimiter": self.delimiter,
                "decimal_mark": self.decimal_mark,
            }
        )
        if self.percent:
            base["type"] = "percent"
        if self.display_mode:
            base["display_mode"] = self.display_mode.value
        return base


@dataclass
class IntegerField(FloatField):
    type: str = "number"
    precision: int = 0


@dataclass
class YearField(IntegerField):
    precision: int = 0
    delimiter: str = ""
    decimal_mark: str = "."

    def __post_init__(self):
        self.precision = 0
        self.delimiter = ""
        self.decimal_mark = "."


@dataclass
class ListField(_BaseField):
    type: str = "list"


@dataclass
class JsonField(_BaseField):
    type: str = "json"


@dataclass
class SparklineField(ListField):
    type: str = "sparkline"

    def to_dict(self):
        rv = super().to_dict()
        rv["sparkline_type"] = "column"
        return rv


@dataclass(unsafe_hash=True)
class PandasFields:
    fields: List[_BaseField]

    def to_dict(self):
        fields = defaultdict(dict)

        for field in self.fields:
            fields[field.key] = field.to_dict()

        return fields
