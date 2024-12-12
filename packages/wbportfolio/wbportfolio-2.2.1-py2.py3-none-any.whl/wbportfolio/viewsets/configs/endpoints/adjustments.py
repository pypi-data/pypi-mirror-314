from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class AdjustmentEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        if instrument_id := self.view.kwargs.get("instrument_id", None):
            return reverse("wbportfolio:instrument-adjustment-list", args=[instrument_id], request=self.request)
        return reverse("wbportfolio:adjustment-list", args=[], request=self.request)

    def get_instance_endpoint(self, **kwargs):
        if self.view.kwargs.get("pk", None):
            return None
        return self.get_endpoint(**kwargs)

    def get_delete_endpoint(self, **kwargs):
        return None
