from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class FeeEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:fees-list", args=[], request=self.request)


class FeesPortfolioEndpointConfig(FeeEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-fees-list", args=[self.view.kwargs["portfolio_id"]], request=self.request
        )


class FeesAggregatedPortfolioPandasEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-feesaggregated-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )
