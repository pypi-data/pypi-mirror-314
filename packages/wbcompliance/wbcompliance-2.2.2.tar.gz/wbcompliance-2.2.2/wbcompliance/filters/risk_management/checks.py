from wbcompliance.models.risk_management import RiskCheck
from wbcore import filters as wb_filters


class RiskCheckFilterSet(wb_filters.FilterSet):
    triggers = wb_filters.MultipleChoiceContentTypeFilter(
        label="Triggerers",
        field_name="triggers",
        object_id_label="trigger_id",
        content_type_label="trigger_content_type",
        distinct=True,
    )

    class Meta:
        model = RiskCheck

        fields = {
            "rule_checked_object_relationship": ["exact"],
            "creation_datetime": ["gte", "exact", "lte"],
            "evaluation_date": ["exact"],
            "status": ["exact"],
        }
