import factory
from wbcompliance.models.risk_management.checks import RiskCheck


class RiskCheckFactory(factory.django.DjangoModelFactory):
    rule_checked_object_relationship = factory.SubFactory(
        "wbcompliance.factories.risk_management.rules.RuleCheckedObjectRelationshipFactory"
    )
    evaluation_date = factory.Faker("date_object")

    class Meta:
        model = RiskCheck
