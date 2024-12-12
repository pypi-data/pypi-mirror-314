from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class PerformancePandasEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_instance_endpoint(self, **kwargs):
        return reverse("wbportfolio:product-list", request=self.request)

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:productperformance-list", request=self.request)


class PerformanceComparisonEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_instance_endpoint(self, **kwargs):
        return reverse("wbportfolio:product-list", request=self.request)

    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:productperformancecomparison-list", request=self.request)


class ProductPerformanceNetNewMoneyEndpointConfig(PerformancePandasEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbportfolio:productperformancennmlist-list", request=self.request)
