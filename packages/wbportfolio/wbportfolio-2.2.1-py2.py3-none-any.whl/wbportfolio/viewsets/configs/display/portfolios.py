from typing import Optional

from django.utils.translation import gettext_lazy as _
from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
    create_simple_section,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class PortfolioDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="name", label="Name"),
                dp.Field(key="currency", label="Currency"),
                dp.Field(key="portfolio_synchronization", label="Synchronization Method"),
                dp.Field(key="last_synchronization", label="Last Synchronization"),
                dp.Field(key="depends_on", label="Depends on"),
            ]
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["name", "currency"],
                ["portfolio_synchronization", "portfolio_synchronization"],
                [repeat_field(2, "dependent_portfolios")],
                [repeat_field(2, "trade_proposals_section")],
                [repeat_field(2, "instruments_section")],
                [repeat_field(2, "dependencyportfolios_section")],
                [repeat_field(2, "preferredclassification_section")],
            ],
            [
                create_simple_section(
                    "trade_proposals_section",
                    _("Trade Proposals"),
                    [["trade_proposals"]],
                    "trade_proposals",
                    collapsed=True,
                ),
                create_simple_section(
                    "instruments_section", _("Linked Instruments"), [["instruments"]], "instruments", collapsed=True
                ),
                create_simple_section(
                    "dependencyportfolios_section",
                    _("Dependency Portfolios"),
                    [["dependencyportfolios"]],
                    "dependencyportfolios",
                    collapsed=True,
                ),
                create_simple_section(
                    "preferredclassification_section",
                    _("Preferred Classification"),
                    [["preferredclassification"]],
                    "preferredclassification",
                    collapsed=True,
                ),
            ],
        )


class ModelPortfolioDisplayConfig(PortfolioDisplayConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="name", label="Name"),
                dp.Field(key="currency", label="Currency"),
                dp.Field(key="portfolio_synchronization", label="Synchronization Method"),
                dp.Field(key="last_synchronization", label="Last Synchronization"),
                dp.Field(key="depends_on", label="Depends on"),
            ]
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["name", "currency"],
                [repeat_field(2, "portfolio_synchronization")],
                [repeat_field(2, "dependent_portfolios")],
                [repeat_field(2, "trade_proposals_section")],
                [repeat_field(2, "instruments_section")],
                [repeat_field(2, "dependencyportfolios_section")],
                [repeat_field(2, "preferredclassification_section")],
            ],
            [
                create_simple_section(
                    "trade_proposals_section",
                    _("Trade Proposals"),
                    [["trade_proposals"]],
                    "trade_proposals",
                    collapsed=True,
                ),
                create_simple_section(
                    "instruments_section", _("Linked Instruments"), [["instruments"]], "instruments", collapsed=True
                ),
                create_simple_section(
                    "dependencyportfolios_section",
                    _("Dependency Portfolios"),
                    [["dependencyportfolios"]],
                    "dependencyportfolios",
                    collapsed=True,
                ),
                create_simple_section(
                    "preferredclassification_section",
                    _("Preferred Classification"),
                    [["preferredclassification"]],
                    "preferredclassification",
                    collapsed=True,
                ),
            ],
        )


class PortfolioPortfolioThroughModelDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="dependency_portfolio", label="Dependency Portfolio"),
                dp.Field(key="type", label="Type"),
            ]
        )
