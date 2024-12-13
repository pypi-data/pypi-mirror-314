from wbcore.metadata.configs.titles import TitleViewConfig
from wbportfolio.models.portfolio import Portfolio


class PortfolioTitleConfig(TitleViewConfig):
    def get_list_title(self):
        return "Portfolios"

    def get_instance_title(self):
        return "Portfolio {{name}}"

    def get_create_title(self):
        return "New Portfolio"


class ModelPortfolioTitleConfig(TitleViewConfig):
    def get_list_title(self):
        return "Model Portfolios"

    def get_instance_title(self):
        return "Model Portfolio: {{ name }}"

    def get_create_title(self):
        return "New Model Portfolio"


class DailyPortfolioCashFlowTitleConfig(TitleViewConfig):
    def get_list_title(self):
        if portfolio_id := self.view.kwargs.get("portfolio_id", None):
            portfolio = Portfolio.objects.get(id=portfolio_id)
            return f"{portfolio}: Daily Portfolio Cash Flow"
        return "Daily Portfolio Cash Flow"
