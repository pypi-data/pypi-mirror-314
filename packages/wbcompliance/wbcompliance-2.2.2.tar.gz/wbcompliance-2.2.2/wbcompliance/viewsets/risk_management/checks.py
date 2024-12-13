from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from wbcompliance.filters.risk_management.checks import RiskCheckFilterSet
from wbcompliance.models.risk_management import RiskCheck
from wbcompliance.serializers import (
    RiskCheckModelSerializer,
    RiskCheckRepresentationSerializer,
)
from wbcompliance.viewsets.buttons import RiskCheckButtonConfig
from wbcompliance.viewsets.display import RiskCheckDisplayConfig
from wbcompliance.viewsets.endpoints import RiskCheckEndpointConfig
from wbcore import viewsets

User = get_user_model()


class RiskCheckRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = RiskCheck.objects.all()
    serializer_class = RiskCheckRepresentationSerializer


class RiskCheckModelViewSet(viewsets.ModelViewSet):
    button_config_class = RiskCheckButtonConfig
    display_config_class = RiskCheckDisplayConfig
    endpoint_config_class = RiskCheckEndpointConfig
    queryset = RiskCheck.objects.all()
    serializer_class = RiskCheckModelSerializer

    filterset_class = RiskCheckFilterSet

    def get_queryset(self):
        return (
            RiskCheck.objects.annotate(
                rule_repr=F("rule_checked_object_relationship__rule__name"),
                status_icon=models.Case(
                    *[
                        models.When(status=value, then=models.Value(RiskCheck.CheckStatus[value].icon))
                        for value in RiskCheck.CheckStatus.values
                    ],
                    default=models.Value("none")
                ),
            )
            .select_related(
                "rule_checked_object_relationship",
                "trigger_content_type",
            )
            .prefetch_related("incidents")
        )
