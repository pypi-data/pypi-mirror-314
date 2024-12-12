from django.utils.translation import gettext as _
from wbcore.menus import ItemPermission, MenuItem
from wbcore.permissions.shortcuts import is_internal_user


def default_calendar_get_params(request) -> dict:
    return {"entities": request.user.profile.id}


CALENDAR_MENUITEM = MenuItem(
    label=_("Calendar"),
    endpoint="wbcore:agenda:calendaritem-list",
    permission=ItemPermission(
        method=lambda request: is_internal_user(request.user), permissions=["agenda.view_calendaritem"]
    ),
    endpoint_get_parameters=default_calendar_get_params,
)
