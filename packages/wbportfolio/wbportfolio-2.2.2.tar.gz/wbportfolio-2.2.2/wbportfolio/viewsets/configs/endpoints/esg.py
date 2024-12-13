from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class ESGMetricAggregationPortfolioPandasEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-esgaggregation-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )
