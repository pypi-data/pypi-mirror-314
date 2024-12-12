from typing import Optional

from django.utils.translation import gettext as _
from wbcompliance.models.risk_management.checks import RiskCheck
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class RiskCheckDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="rule_repr", label=_("Rule")),
                dp.Field(key="evaluation_date", label=_("Evaluation Date")),
                dp.Field(key="creation_datetime", label=_("Creation Time")),
                dp.Field(
                    key="status_icon",
                    label=_("Status"),
                    formatting_rules=[
                        dp.FormattingRule(
                            style={"color": RiskCheck.CheckStatus[value].color},
                            condition=("==", RiskCheck.CheckStatus[value].icon),
                        )
                        for value in RiskCheck.CheckStatus.values
                    ],
                ),
            ],
            legends=[
                dp.Legend(
                    items=[
                        dp.LegendItem(icon=RiskCheck.CheckStatus[value].icon, label=RiskCheck.CheckStatus[value].label)
                        for value in RiskCheck.CheckStatus.values
                    ]
                )
            ],
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [[repeat_field(3, "status")], ["rule_checked_object_relationship", "evaluation_date", "creation_datetime"]]
        )
