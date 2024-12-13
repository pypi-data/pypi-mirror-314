from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class AssetPositionEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:assetposition-list", request=self.request)


class AssetPositionPortfolioEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-asset-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )


class AssetPositionEquityEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:equity-asset-list",
            args=[self.view.kwargs["equity_id"]],
            request=self.request,
        )


class AssetPositionInstrumentEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:instrument-asset-list",
            args=[self.view.kwargs["instrument_id"]],
            request=self.request,
        )


class AssetPositionIndexEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:index-asset-list",
            args=[self.view.kwargs["index_id"]],
            request=self.request,
        )


class AssetPositionProductGroupEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:productgroup-asset-list",
            args=[self.view.kwargs["product_group_id"]],
            request=self.request,
        )


class CashPositionPortfolioEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:productcashposition-list",
            args=[],
            request=self.request,
        )


class ContributorPortfolioChartEndpointConfig(AssetPositionEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-contributor-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )


class AssetPositionUnderlyingInstrumentChartEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:instrument-assetpositionchart-list",
            args=[self.view.kwargs["instrument_id"]],
            request=self.request,
        )


class DistributionChartEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-distributionchart-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )


class DistributionTableEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-distributiontable-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )

    def get_endpoint(self, **kwargs):
        return None


class CompositionModelPortfolioPandasEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbportfolio:portfolio-modelcompositionpandas-list",
            args=[self.view.kwargs["portfolio_id"]],
            request=self.request,
        )
