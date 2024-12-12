from wbcore.menus import ItemPermission, MenuItem
from wbportfolio.permissions import is_portfolio_manager

PortfolioMenuItem = MenuItem(
    label="Portfolios",
    endpoint="wbportfolio:portfolio-list",
    permission=ItemPermission(method=is_portfolio_manager, permissions=["wbportfolio.view_portfolio"]),
)


ModelPortfolioMenuItem = MenuItem(
    label="Model Portfolios",
    endpoint="wbportfolio:modelportfolio-list",
    permission=ItemPermission(method=is_portfolio_manager, permissions=["wbportfolio.view_portfolio"]),
)
