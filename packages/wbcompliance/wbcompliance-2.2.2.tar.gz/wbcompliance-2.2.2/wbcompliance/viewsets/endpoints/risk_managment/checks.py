from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class RiskCheckEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        if rule_id := self.view.kwargs.get("rule_id"):
            return reverse(
                "wbcompliance:riskrule-check-list",
                args=[rule_id],
                request=self.request,
            )
        return super().get_endpoint(**kwargs)
