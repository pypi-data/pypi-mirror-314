from datetime import date
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.functional import cached_property

from .checks import RiskCheck, evaluate_as_task
from .rules import RiskRule, RuleCheckedObjectRelationship


class RiskCheckMixin(models.Model):
    """
    A utility mixin to inherit from when a model proposes a risk check workflow on one of its field
    """

    id: int

    def _get_checked_object_field_name(self) -> str:
        """
        Return the object representing the checked object
        Returns NotImplementedError by default
        """
        raise NotImplementedError()

    @cached_property
    def content_type(self) -> ContentType:
        return ContentType.objects.get_for_model(self)

    @cached_property
    def checked_object(self) -> Any:
        return getattr(self, self._get_checked_object_field_name())

    @property
    def checks(self) -> models.QuerySet[RiskCheck]:
        """
        Returned the check triggered by this object (self)
        Returns: A queryset of RiskCheck
        """
        return RiskCheck.objects.filter(trigger_content_type=self.content_type, trigger_id=self.id)

    @cached_property
    def has_assigned_active_rules(self) -> bool:
        """
        Return True if an enabled and active rule is available for the assigned checked object
        """
        relationships = RuleCheckedObjectRelationship.objects.get_for_object(
            self.checked_object, rule__is_enable=True, rule__only_passive_check_allowed=False
        )
        return RiskRule.objects.filter(id__in=relationships.distinct("rule").values("rule")).exists()

    @property
    def has_all_check_completed_and_succeed(self) -> bool:
        """
        Return True if checks are available and they all succeed
        """
        return (
            self.checks.exists()
            and not self.checks.exclude(
                status__in=[RiskCheck.CheckStatus.SUCCESS, RiskCheck.CheckStatus.WARNING]
            ).exists()
        )

    @property
    def has_all_check_completed(self) -> bool:
        """
        Return True if checks are available and they all succeed
        """
        return (
            self.checks.exists()
            and not self.checks.filter(
                status__in=[RiskCheck.CheckStatus.RUNNING, RiskCheck.CheckStatus.PENDING]
            ).exists()
        ) or not self.checks.exists()

    @property
    def has_no_rule_or_all_checked_succeed(self) -> bool:
        return (
            self.has_assigned_active_rules and self.has_all_check_completed_and_succeed
        ) or not self.has_assigned_active_rules

    def get_worst_check_status(self) -> RiskCheck.CheckStatus:
        status_ordered = [
            RiskCheck.CheckStatus.FAILED,
            RiskCheck.CheckStatus.WARNING,
            RiskCheck.CheckStatus.RUNNING,
            RiskCheck.CheckStatus.PENDING,
        ]
        for status in status_ordered:
            if self.checks.filter(status=status).exists():
                return status
        return RiskCheck.CheckStatus.SUCCESS

    def evaluate_active_rules(self, evaluation_date: date, *dto, asynchronously: bool = True):
        for rel in RuleCheckedObjectRelationship.objects.get_for_object(
            self.checked_object, rule__is_enable=True, rule__only_passive_check_allowed=False
        ):
            check = RiskCheck.objects.update_or_create(
                rule_checked_object_relationship=rel,
                evaluation_date=evaluation_date,
                trigger_content_type=self.content_type,
                trigger_id=self.id,
                defaults={"status": RiskCheck.CheckStatus.PENDING},
            )[0]
            if asynchronously:
                transaction.on_commit(
                    lambda: evaluate_as_task.delay(
                        check.id, *dto, override_incident=True, ignore_informational_threshold=True
                    )
                )
            else:
                check.evaluate(*dto, override_incident=True, ignore_informational_threshold=True)

    class Meta:
        abstract = True
