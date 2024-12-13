from dataclasses import dataclass, field
from typing import Iterable, Literal, Optional

from wbcore.metadata.configs.display.formatting import Formatting, FormattingRule


@dataclass
class Tooltip:
    key: str | None = None
    endpoint: str | None = None
    width: str | None = None
    height: str | None = None

    def __post_init__(self):
        if not self.key and not self.endpoint:
            raise ValueError("Either key or endpoint needs to be specified.")

    def serialize(self):
        tooltip = {}
        if self.key:
            tooltip["key"] = self.key

        if self.endpoint:
            tooltip["endpoint"] = self.endpoint

        if self.width:
            tooltip["width"] = self.width

        if self.height:
            tooltip["height"] = self.height

        return tooltip


@dataclass(unsafe_hash=True)
class Field:
    key: str
    label: str
    formatting_rules: Iterable[FormattingRule] = field(default_factory=list)
    width: int | None = None

    tooltip: Tooltip | None = None

    hide: bool | None = None
    pinned: str | None = None

    children: list["Field"] | None = None
    marry_children: bool | None = True
    show: Literal["open"] | Literal["closed"] | None = None
    open_by_default: bool | None = None
    supress_movable: bool = False
    lock_position: bool = False
    resizable: bool = True

    def iterate_leaf_fields(self, aggregated_parent_label: str = ""):
        label = self.label
        if aggregated_parent_label:
            label = aggregated_parent_label + " " + label
        if self.children:
            for children in self.children:
                yield from children.iterate_leaf_fields(label)
        else:
            yield self.key, label

    def __iter__(self):
        yield "key", self.key
        yield "label", self.label
        yield "formatting_rules", [dict(rule) for rule in self.formatting_rules]

        if self.width:
            yield "width", self.width

        if self.hide:
            yield "hide", self.hide

        if self.pinned and self.pinned in ["left", "right"]:
            yield "pinned", self.pinned

        if self.children:
            yield "children", [dict(child) for child in self.children]
            yield "marry_children", self.marry_children is True  # Convert None into False

        if self.show:
            yield "show", self.show

        if self.open_by_default is not None:
            yield "open_by_default", self.open_by_default
        yield "supress_movable", self.supress_movable
        yield "lock_position", self.lock_position

        if self.tooltip:
            yield "tooltip", self.tooltip.serialize()


@dataclass(unsafe_hash=True)
class LegendItem:
    icon: str
    label: str
    value: Optional[str | bool] = None

    def __iter__(self):
        yield "icon", self.icon
        yield "label", self.label

        if self.value is not None:
            yield "value", self.value


@dataclass(unsafe_hash=True)
class Legend:
    items: list[LegendItem]
    label: str | None = None
    key: str | None = None

    def __post_init__(self):
        if self.key:
            assert all(
                [item.value is not None for item in self.items]
            ), "If key is set, all items need to specify a value."

    def __iter__(self):
        if self.label:
            yield "label", self.label

        if self.key:
            yield "key", self.key

        yield "items", [dict(item) for item in self.items]


@dataclass(unsafe_hash=True)
class TreeGroupLevelOption:
    list_endpoint: str
    reorder_endpoint: str | None = None
    reparent_endpoint: str | None = None
    lookup: str = "_group_key"
    filter_key: str = "group_keys"
    filter_whitelist: list[str] = field(default_factory=list)
    filter_blacklist: list[str] = field(default_factory=list)
    clear_filter: bool = (
        False
        # Set to True if preselected filters other than required ones need to be cleared out before fetching the tree group
    )
    filter_depth: int = 1
    parent_field: str = "parent"
    ordering_field: str = "order"

    def __iter__(self):
        endpoints = {"list": self.list_endpoint}
        if self.reorder_endpoint:
            endpoints["reorder"] = self.reorder_endpoint

        if self.reparent_endpoint:
            endpoints["reparent"] = self.reparent_endpoint

        yield "endpoints", endpoints
        yield "lookup", self.lookup
        yield "filter_key", self.filter_key
        yield "filter_whitelist", self.filter_whitelist
        yield "filter_blacklist", self.filter_blacklist
        yield "clear_filter", self.clear_filter
        yield "filter_depth", self.filter_depth
        yield "parent_field", self.parent_field
        yield "ordering_field", self.ordering_field


@dataclass(unsafe_hash=True)
class ListDisplay:
    fields: list[Field | None]
    legends: list[Legend] = field(default_factory=list)
    formatting: list[Formatting] = field(default_factory=list)
    editable: bool = True
    hide_control_bar: bool = False

    ordering_field: str = "order"

    tree: bool = False
    tree_group_pinned: str = "left"
    tree_group_field: str | None = None
    tree_group_label: str | None = None
    tree_group_open_level: int = 0
    tree_group_field_sortable: bool = False

    tree_group_level_options: list[TreeGroupLevelOption] = field(default_factory=list)

    @property
    def flatten_fields(self) -> tuple[str, str]:
        for f in self.fields:
            yield from f.iterate_leaf_fields()

    def __iter__(self):
        yield "editable", self.editable
        yield "fields", [dict(field) for field in self.fields if field]
        yield "legends", [dict(legend) for legend in self.legends if legend]
        yield "formatting", [dict(formatting) for formatting in self.formatting if formatting]
        yield "hide_control_bar", self.hide_control_bar
        yield "ordering_field", self.ordering_field
        if self.tree:
            yield "tree", self.tree
            tree_group = {
                "pinned": self.tree_group_pinned,
                "field": self.tree_group_field if self.tree_group_field else self.fields[0].key,
                "label": self.tree_group_label if self.tree_group_label else self.fields[0].key,
                "open_level": self.tree_group_open_level,
                "field_sortable": self.tree_group_field_sortable,
            }
            tree_group["level_options"] = [dict(level_option) for level_option in self.tree_group_level_options]
            yield "tree_group", tree_group


@dataclass(unsafe_hash=True)
class Calendar:
    title: str
    period: str
    all_day: bool
    color: str
    icon: str
    entities: list
    endpoint: str

    def __iter__(self):
        yield "calendar", {
            "title": self.title,
            "period": self.period,
            "all_day": self.all_day,
            "color": self.color,
            "icon": self.icon,
            "entities": self.entities,
            "endpoint": self.endpoint,
        }
