from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext as _
from wbcore.menus import ItemPermission, MenuItem
from wbcore.permissions.shortcuts import is_internal_user


def default_activity_create_get_params(request) -> dict:
    return {"participants": request.user.profile.id}


def default_activitychart_get_params(request) -> dict:
    current_last_week_date_start = timezone.now().date() - timedelta(days=7)
    current_next_week_date_end = timezone.now().date() + timedelta(days=7)

    return {"period": f"{current_last_week_date_start:%Y-%m-%d},{current_next_week_date_end:%Y-%m-%d}"}


ACTIVITYTYPE_MENUITEM = MenuItem(
    label=_("Activity Types"),
    endpoint="wbcrm:activitytype-list",
    permission=ItemPermission(
        method=lambda request: is_internal_user(request.user),
        permissions=["wbcrm.view_activitytype"],
    ),
    add=MenuItem(
        label=_("Create Activity Type"),
        endpoint="wbcrm:activitytype-list",
        permission=ItemPermission(
            method=lambda request: is_internal_user(request.user),
            permissions=["wbcrm.add_activitytype"],
        ),
    ),
)


ACTIVITY_MENUTITEM = MenuItem(
    label=_("Activities"),
    endpoint="wbcrm:activity-list",
    permission=ItemPermission(
        method=lambda request: is_internal_user(request.user), permissions=["wbcrm.view_activity"]
    ),
    # endpoint_get_parameters={"only_recent": True}, # TODO confirm that this can actually be commented out
    add=MenuItem(
        label=_("Create Activity"),
        endpoint="wbcrm:activity-list",
        permission=ItemPermission(
            method=lambda request: is_internal_user(request.user), permissions=["wbcrm.add_activity"]
        ),
        endpoint_get_parameters=default_activity_create_get_params,
    ),
)
ACTIVITYCHART_MENUITEM = MenuItem(
    label=_("Activity Chart"),
    endpoint="wbcrm:activitychart-list",
    permission=ItemPermission(
        method=lambda request: is_internal_user(request.user), permissions=["wbcrm.view_activity"]
    ),
    endpoint_get_parameters=default_activitychart_get_params,
)
