from contextlib import suppress
from types import DynamicClassAttribute
from typing import Self

from celery import shared_task
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _
from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.icons import WBIcon
from wbcore.models import WBModel
from wbcore.utils.models import ComplexToStringMixin

from .incidents import CheckedObjectIncidentRelationship


class RiskCheck(ComplexToStringMixin, WBModel):
    class CheckStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        FAILED = "FAILED", "Failed"
        SUCCESS = "SUCCESS", "Success"
        WARNING = "WARNING", "Warning"

        @DynamicClassAttribute
        def icon(self):
            return {
                "PENDING": WBIcon.PENDING.icon,
                "RUNNING": WBIcon.RUNNING.icon,
                "FAILED": WBIcon.REJECT.icon,
                "SUCCESS": WBIcon.CONFIRM.icon,
                "WARNING": WBIcon.WARNING.icon,
            }[self.value]

        @DynamicClassAttribute
        def color(self):
            return {
                "PENDING": WBColor.YELLOW_LIGHT.value,
                "RUNNING": WBColor.BLUE_LIGHT.value,
                "FAILED": WBColor.RED_LIGHT.value,
                "SUCCESS": WBColor.GREEN_LIGHT.value,
                "WARNING": WBColor.YELLOW_DARK.value,
            }[self.value]

    rule_checked_object_relationship = models.ForeignKey(
        "wbcompliance.RuleCheckedObjectRelationship",
        on_delete=models.CASCADE,
        verbose_name=_("Rule-Checked Object Relationship"),
        related_name="checks",
    )

    creation_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation Date"),
        help_text=_("Time at which the check was created/triggered"),
    )
    evaluation_date = models.DateField(
        verbose_name=_("Evaluation Date"), help_text=_("The date at which the rule was evaluated")
    )

    trigger_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="triggered_checks", blank=True, null=True
    )
    trigger_id = models.PositiveIntegerField(blank=True, null=True)
    trigger = GenericForeignKey("trigger_content_type", "trigger_id")

    status = models.CharField(
        max_length=32, default=CheckStatus.PENDING, choices=CheckStatus.choices, verbose_name=_("Status")
    )

    @property
    def is_active(self) -> bool:
        return self.trigger is not None

    @property
    def rule(self):
        return self.rule_checked_object_relationship.rule

    @property
    def checked_object(self) -> models.Model:
        """
        Return the object from which the rule needs to be check against
        """
        return self.rule_checked_object_relationship.checked_object

    @property
    def previous_check(self) -> Self | None:
        """
        Property holding the last valid check

        Returns:
            The last valid check
        """
        with suppress(RiskCheck.DoesNotExist):
            return (
                RiskCheck.objects.filter(
                    evaluation_date__lt=self.evaluation_date,
                    rule_checked_object_relationship=self.rule_checked_object_relationship,
                )
                .order_by("-evaluation_date", "-creation_datetime")
                .first()
            )

    def compute_str(self) -> str:
        return _("{} - {}").format(
            self.rule_checked_object_relationship.checked_object,
            self.evaluation_date,
        )

    def evaluate(
        self, *explicit_dto, override_incident: bool = False, ignore_informational_threshold: bool = False
    ) -> list[models.Model]:
        """
        Evaluate the check and returns tuple of incidents information
        Args:
            override_incident: True if the existing incident needs to be overriden

        Returns:

        """
        self.status = self.CheckStatus.RUNNING
        self.save()
        rule_backend = self.rule.rule_backend.backend(
            self.evaluation_date, self.checked_object, self.rule.parameters, self.rule.thresholds.all()
        )
        self.status = self.CheckStatus.SUCCESS
        incidents = []
        report_template = Template(self.rule.rule_backend.incident_report_template)
        for incident_result in rule_backend.check_rule(*explicit_dto):
            if (
                ignore_informational_threshold
                and incident_result.severity.is_ignorable
                and incident_result.severity.is_informational
            ):
                self.status = self.CheckStatus.WARNING
            else:
                self.status = self.CheckStatus.FAILED
                # If the check is passive, we aggregated incident per breached object and return it for further processing
            report = report_template.render(Context({"report_details": incident_result.report_details}))
            if not self.is_active:
                incident, created = self.rule.get_or_create_incident(
                    self.evaluation_date,
                    incident_result.severity,
                    incident_result.breached_object,
                    incident_result.breached_object_repr,
                )
                incident.update_or_create_relationship(
                    self,
                    report,
                    incident_result.report_details,
                    incident_result.breached_value,
                    incident_result.severity,
                    override_incident=override_incident or created,
                )
                incidents.append(incident)
            else:
                # If the check is active, the only thing that matter is whether the check led to incident or not
                CheckedObjectIncidentRelationship.objects.create(
                    rule_check=self,
                    report=report,
                    report_details=incident_result.report_details,
                    breached_value=incident_result.breached_value,
                    severity=incident_result.severity,
                )
        self.save()
        return incidents

    class Meta:
        verbose_name = "Risk Check"
        verbose_name_plural = "Risk Checks"

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbcompliance:riskcheck"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcompliance:riskcheckrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"


@shared_task
def evaluate_as_task(
    check_id: int, *dto, override_incident: bool = False, ignore_informational_threshold: bool = False
):
    check = RiskCheck.objects.get(id=check_id)
    check.evaluate(
        *dto, override_incident=override_incident, ignore_informational_threshold=ignore_informational_threshold
    )
