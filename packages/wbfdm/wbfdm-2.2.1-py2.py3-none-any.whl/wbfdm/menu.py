from django.utils.translation import gettext as _
from wbcore.menus import ItemPermission, MenuItem
from wbcore.permissions.shortcuts import is_internal_user

INSTRUMENT_MENU_ITEM = MenuItem(
    label=_("Instruments"),
    endpoint="wbfdm:instrument-list",
    permission=ItemPermission(
        method=lambda request: is_internal_user(request.user), permissions=["wbfdm.view_instrument"]
    ),
)
