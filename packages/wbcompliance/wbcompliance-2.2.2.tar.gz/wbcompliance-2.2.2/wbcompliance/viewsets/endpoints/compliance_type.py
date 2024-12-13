from wbcompliance.models import ComplianceType
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class ComplianceTypeEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        if ComplianceType.is_administrator(self.request.user):
            return super().get_endpoint()
        return None
