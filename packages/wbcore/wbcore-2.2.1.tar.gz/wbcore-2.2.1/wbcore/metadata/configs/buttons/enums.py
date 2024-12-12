from enum import Enum


class ButtonDefaultColor(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    INHERIT = "inherit"  # 'inherit' means that the button will take the color of a surrounding button group


class ButtonType(Enum):
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"


class HyperlinkTarget(Enum):
    BLANK = "_blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"
