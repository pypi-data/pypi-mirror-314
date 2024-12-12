from wbcore.metadata.configs.titles import TitleViewConfig
from wbportfolio.models import Portfolio


class TransactionPortfolioTitleConfig(TitleViewConfig):
    def get_list_title(self):
        portfolio = Portfolio.objects.get(id=self.view.kwargs["portfolio_id"])
        return f"Transactions for Product {str(portfolio)}"
