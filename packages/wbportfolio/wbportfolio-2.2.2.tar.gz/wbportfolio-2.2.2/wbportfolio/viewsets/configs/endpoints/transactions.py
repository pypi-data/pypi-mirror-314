from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class TransactionEndpointConfig(EndpointViewConfig):
    def get_instance_endpoint(self, **kwargs):
        model = "{{transaction_url_type}}"
        return f"{self.request.scheme}://{self.request.get_host()}/api/portfolio/{model}/"


class TransactionPortfolioEndpointConfig(TransactionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-transaction-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )
