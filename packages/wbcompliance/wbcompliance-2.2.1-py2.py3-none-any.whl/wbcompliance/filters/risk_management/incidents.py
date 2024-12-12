from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from wbcompliance.models.risk_management import (
    CheckedObjectIncidentRelationship,
    RiskIncident,
    RiskIncidentType,
    RiskRule,
    RuleCheckedObjectRelationship,
)
from wbcompliance.models.risk_management.rules import RuleGroup
from wbcore import filters as wb_filters


def get_default_severity(*args, **kwargs):
    non_informational_qs = RiskIncidentType.objects.exclude(is_informational=True)
    if non_informational_qs.exists():
        return list(non_informational_qs.values_list("id", flat=True))
    return []


class RiskIncidentFilterSet(wb_filters.FilterSet):
    date_range = wb_filters.DateRangeFilter(label="Date Range")
    status = wb_filters.ChoiceFilter(
        default=RiskIncident.Status.OPEN, choices=RiskIncident.Status.choices, label=_("Label")
    )
    rule = wb_filters.ModelMultipleChoiceFilter(
        label=_("Rule"),
        queryset=RiskRule.objects.all(),
        endpoint=RiskRule.get_representation_endpoint(),
        value_key=RiskRule.get_representation_value_key(),
        label_key=RiskRule.get_representation_label_key(),
    )

    severity = wb_filters.ModelMultipleChoiceFilter(
        label=_("Severity"),
        queryset=RiskIncidentType.objects.all(),
        endpoint=RiskIncidentType.get_representation_endpoint(),
        value_key=RiskIncidentType.get_representation_value_key(),
        label_key=RiskIncidentType.get_representation_label_key(),
        default=get_default_severity,
    )
    checked_object_relationships = wb_filters.MultipleChoiceContentTypeFilter(
        label="Checked Objects",
        field_name="checked_object_relationships",
        object_id_label="checked_object_relationships__rule_check__rule_checked_object_relationship__checked_object_id",
        content_type_label="checked_object_relationships__rule_check__rule_checked_object_relationship__checked_object_content_type",
        distinct=True,
        hidden=True,
    )

    rule_checked_object_relationship = wb_filters.ModelChoiceFilter(
        label=_("Rule Relationship"),
        queryset=RuleCheckedObjectRelationship.objects.all(),
        endpoint=RuleCheckedObjectRelationship.get_representation_endpoint(),
        value_key=RuleCheckedObjectRelationship.get_representation_value_key(),
        label_key=RuleCheckedObjectRelationship.get_representation_label_key(),
        hidden=True,
        method="filter_rule_checked_object_relationship",
    )
    object_repr = wb_filters.CharFilter(label="Object Representation", lookup_expr="icontains")

    def filter_rule_checked_object_relationship(self, queryset, label, value):
        if value:
            return queryset.filter(checked_object_relationships__rule_check__rule_checked_object_relationship=value)
        return queryset

    rule_group = wb_filters.ModelChoiceFilter(
        label=_("Group"),
        queryset=RuleGroup.objects.all(),
        endpoint=RuleGroup.get_representation_endpoint(),
        value_key=RuleGroup.get_representation_value_key(),
        label_key=RuleGroup.get_representation_label_key(),
        method="filter_rule_group",
    )

    def filter_rule_group(self, queryset, label, value):
        if value:
            return queryset.filter(
                Q(rule__rule_backend__rule_group=value) | Q(rule__rule_backend__rule_group__isnull=True)
            )
        return queryset

    class Meta:
        model = RiskIncident
        fields = {
            "status": ["exact"],
            "resolved_by": ["exact"],
            "comment": ["icontains"],
            "severity": ["exact"],
        }


class CheckedObjectIncidentRelationshipFilterSet(wb_filters.FilterSet):
    checked_object = wb_filters.CharFilter(
        method="filter_checked_object", field_name="checked_object", lookup_expr="icontains"
    )

    def filter_checked_object(self, queryset, label, value):
        if value:
            return queryset.filter(rule_check__rule_checked_object_relationship__checked_object_repr__icontains=value)
        return queryset

    class Meta:
        model = CheckedObjectIncidentRelationship
        fields = {
            "severity": ["exact"],
            "report": ["icontains"],
            "comment": ["icontains"],
            "resolved_by": ["exact"],
            "incident": ["exact"],
            "rule_check": ["exact"],
            "status": ["exact"],
        }
