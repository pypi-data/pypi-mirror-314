from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class RiskManagementIncidentTableEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbcompliance:riskmanagementincidenttable-list",
            args=[],
            request=self.request,
        )
