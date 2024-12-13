from wbcore.menus import ItemPermission, MenuItem
from wbportfolio.permissions import is_manager

TRANSACTION_MENUITEM = MenuItem(
    label="Transactions",
    endpoint="wbportfolio:transaction-list",
    permission=ItemPermission(method=is_manager, permissions=["wbportfolio.view_transaction"]),
)
