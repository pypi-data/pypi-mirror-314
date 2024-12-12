from django.utils.translation import gettext as _
from wbcompliance.permissions import is_admin_compliance
from wbcore.menus import ItemPermission, MenuItem

COMPLIANCETYPE_MENUITEM = MenuItem(
    label=_("Administrators"),
    endpoint="wbcompliance:compliancetype-list",
    permission=ItemPermission(
        method=is_admin_compliance,
        permissions=["wbcompliance.view_compliancetype", "wbcompliance.administrate_compliance"],
    ),
    add=MenuItem(
        label=_("Add Compliance Type"),
        endpoint="wbcompliance:compliancetype-list",
        permission=ItemPermission(method=is_admin_compliance, permissions=["wbcompliance.administrate_compliance"]),
    ),
)
