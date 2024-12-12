from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class AssetPositionPandasEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:assetpositiongroupby-list", request=self.request)


class AggregatedAssetPositionLiquidityEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:aggregatedassetpositionliquidity-list", request=self.request)
