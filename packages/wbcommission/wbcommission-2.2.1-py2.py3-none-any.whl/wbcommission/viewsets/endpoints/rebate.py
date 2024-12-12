from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class RebatePandasViewEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbcommission:rebatetable-list", request=self.request)


class RebateProductMarginalityEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbcommission:rebatemarginalitytable-list", request=self.request)

    def get_instance_endpoint(self, **kwargs):
        return reverse("wbportfolio:product-list", request=self.request)
