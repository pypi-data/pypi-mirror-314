from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class PortfolioEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return super().get_endpoint()

    def get_delete_endpoint(self, **kwargs):
        if self.view.is_portfolio_manager:
            return self.get_endpoint(**kwargs)
        return None

    def get_create_endpoint(self, **kwargs):
        return None


class ModelPortfolioEndpointConfig(PortfolioEndpointConfig):
    def get_endpoint(self, **kwargs):
        return reverse("wbportfolio:modelportfolio-list", request=self.request)


class PortfolioPortfolioThroughModelEndpointConfig(EndpointViewConfig):
    PK_FIELD = "dependency_portfolio"

    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-dependencyportfolio-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )

    def get_instance_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-list",
            args=[],
            request=self.request,
        )

    def get_endpoint(self, **kwargs):
        if self.request.user.is_superuser:
            return self.get_list_endpoint(**kwargs)
        return None
