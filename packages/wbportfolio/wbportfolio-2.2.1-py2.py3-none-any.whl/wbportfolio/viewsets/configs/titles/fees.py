from wbcore.metadata.configs.titles import TitleViewConfig
from wbportfolio.models import Portfolio


class FeesTitleConfig(TitleViewConfig):
    def get_list_title(self):
        return "Fees"

    def get_instance_title(self):
        return "Fees: {{_product.name}} {{date}}"

    def get_create_title(self):
        return "New Fees"


class FeesPortfolioTitleConfig(FeesTitleConfig):
    def get_list_title(self):
        portfolio = Portfolio.objects.get(id=self.view.kwargs["portfolio_id"])
        return f"Fees: {portfolio.name}"


class FeesAggregatedPortfolioTitleConfig(TitleViewConfig):
    def get_list_title(self):
        portfolio = Portfolio.objects.get(id=self.view.kwargs["portfolio_id"])
        return f"Aggregated Fees for {portfolio.name}"
