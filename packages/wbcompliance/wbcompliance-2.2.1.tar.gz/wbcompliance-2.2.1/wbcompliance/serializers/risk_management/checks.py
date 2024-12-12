from rest_framework.reverse import reverse
from wbcompliance.models.risk_management import RiskCheck
from wbcore import serializers as wb_serializers
from wbcore.content_type.serializers import ContentTypeRepresentationSerializer
from wbcore.contrib.icons.serializers import IconSelectField

from .rules import RuleCheckedObjectRelationshipRepresentationSerializer


class RiskCheckRepresentationSerializer(wb_serializers.RepresentationSerializer):
    class Meta:
        model = RiskCheck
        fields = ("id", "computed_str")


class RiskCheckModelSerializer(wb_serializers.ModelSerializer):
    _rule_checked_object_relationship = RuleCheckedObjectRelationshipRepresentationSerializer(
        source="rule_checked_object_relationship"
    )
    _trigger_content_type = ContentTypeRepresentationSerializer(source="trigger_content_type")
    rule_repr = wb_serializers.CharField()

    status_icon = IconSelectField(read_only=True)

    @wb_serializers.register_resource()
    def additional_resources(self, instance, request, user):
        res = {}
        if instance.incidents.exists():
            res[
                "incidents"
            ] = f'{reverse("wbcompliance:checkedobjectincidentrelationship-list", args=[], request=request)}?rule_check={instance.id}'

        return res

    class Meta:
        model = RiskCheck
        fields = (
            "id",
            "rule_repr",
            "rule_checked_object_relationship",
            "_rule_checked_object_relationship",
            "creation_datetime",
            "evaluation_date",
            "computed_str",
            "_trigger_content_type",
            "trigger_content_type",
            "trigger_id",
            "status",
            "rule_repr",
            "status_icon",
            "_additional_resources",
        )
        read_only_fields = fields
