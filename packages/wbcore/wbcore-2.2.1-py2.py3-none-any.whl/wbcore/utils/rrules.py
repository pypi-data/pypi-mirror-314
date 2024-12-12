import calendar as calendar_reference
from datetime import date

from dateutil import rrule


def convert_rrulestr_to_dict(
    rrule_str: str, dtstart: date | None = None, count: int | None = None, until: date | None = None
) -> dict:
    kwargs = {
        values[0]: values[1]
        for elt in rrule_str.replace("RRULE:", "").split(";")
        if (values := elt.split("=")) and len(values) == 2
    }
    rule_dict = {}
    if freq := kwargs.get("FREQ"):
        rule_dict = {
            "freq": getattr(rrule, freq),
            "interval": int(kwargs.get("INTERVAL", "1")),
        }
        if dtstart:
            rule_dict["dtstart"] = dtstart
        if count:
            rule_dict["count"] = count
        if until:
            rule_dict["until"] = until
        if wkst := kwargs.get("WKST"):
            rule_dict["wkst"] = getattr(rrule, wkst)
        if byday := kwargs.get("BYDAY"):
            rule_dict["byweekday"] = [getattr(rrule, day.strip()) for day in byday.split(",")]
    return rule_dict


def convert_weekday_rrule_to_day_name(wkday: rrule.weekday) -> str:
    week_dict = {_day: _day.weekday for _day in rrule.weekdays}
    if idx := week_dict.get(wkday):
        return calendar_reference.day_name[idx]
