from contextlib import suppress

from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from wbcompliance.models.risk_management.checks import RiskCheck
from wbcore.contrib.icons import WBIcon
from wbcore.metadata.configs import buttons as bt
from wbcore.signals import add_additional_resource, add_instance_button


class RiskCheckViewSetMixin:
    @classmethod
    def _get_risk_checks_button_title(cls) -> str:
        return "Checks"

    @classmethod
    def _add_risk_check_button(cls, sender, many, *args, view=None, **kwargs):
        icon = WBIcon.CONFIRM.icon
        with suppress(AssertionError):
            if view and (obj := view.get_object()):
                icon = RiskCheck.CheckStatus[obj.get_worst_check_status()].icon
        return bt.WidgetButton(key="checks", label=cls._get_risk_checks_button_title(), icon=icon)

    @classmethod
    def _add_risk_check_add_additional_resource(
        cls, sender, serializer, instance, request, user, view=None, is_list=False, **kwargs
    ):
        if not is_list and instance.checks.exists() and (content_type := ContentType.objects.get_for_model(instance)):
            return {
                "checks": f'{reverse("wbcompliance:riskcheck-list", args=[], request=request)}?triggers=[[{content_type.id},{instance.id}]]'
            }
        return {}

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP 'OPTIONS' request.
        """
        add_instance_button.connect(
            self._add_risk_check_button,
            sender=self.__class__,
            dispatch_uid="wbcompliance_add_instance_button_riskcheck",
        )
        return super().options(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        add_additional_resource.connect(
            self._add_risk_check_add_additional_resource,
            sender=serializer_class,
            dispatch_uid="wbcompliance_add_additional_resource_riskcheck",
        )
        return serializer_class
