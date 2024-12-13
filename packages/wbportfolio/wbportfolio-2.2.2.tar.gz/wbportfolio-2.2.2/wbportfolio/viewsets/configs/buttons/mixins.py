from contextlib import suppress

from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbfdm.models.instruments import Instrument

from .portfolios import get_portfolio_start_end_serializer_class


class InstrumentButtonMixin:
    @classmethod
    def add_instrument_request_button(self, request=None, view=None, pk=None, **kwargs):
        buttons = [
            bt.WidgetButton(key="assets", label="Implemented Portfolios (Assets)"),
            # bt.WidgetButton(
            #     key="adjustments",
            #     label="Adjustments",
            #     icon=WBIcon.DATA_LIST.icon,
            # ),
        ]
        with suppress(Instrument.DoesNotExist):
            instrument = Instrument.objects.get(id=pk)
            asset_instrument_btn_label = "Asset Portfolio"
            if portfolio := instrument.portfolio:
                buttons.extend(
                    [
                        bt.ActionButton(
                            method=RequestType.PATCH,
                            identifiers=("wbportfolio:portfolio",),
                            key="resynchronize",
                            label="Resynchronize/Rebalance",
                            description_fields="""
                            <p>Resynchronize portfolio from {{start}} to {{end}}</p>
                            """,
                            serializer=get_portfolio_start_end_serializer_class(portfolio),
                            action_label="resynchronize",
                            title="Resynchronize/Rebalance",
                            instance_display=create_simple_display([["start"], ["end"]]),
                        ),
                        bt.WidgetButton(key="portfolio_positions", label=asset_instrument_btn_label),
                        bt.DropDownButton(
                            label="Charts",
                            icon=WBIcon.UNFOLD.icon,
                            buttons=(
                                bt.WidgetButton(
                                    key="portfolio_positions_contributors", label="Contributors (Computed)"
                                ),
                                bt.WidgetButton(key="distribution_chart", label="Distribution Chart"),
                                bt.WidgetButton(key="distribution_table", label="Distribution Table"),
                                bt.WidgetButton(key="assetschart", label="Portfolio Allocation"),
                            ),
                        ),
                    ]
                )
        return bt.DropDownButton(
            label="Portfolio",
            icon=WBIcon.UNFOLD.icon,
            buttons=buttons,
        )

    @classmethod
    def add_transactions_request_button(self, request=None, view=None, pk=None, **kwargs):
        return bt.DropDownButton(
            label="Transactions",
            icon=WBIcon.UNFOLD.icon,
            buttons=(
                bt.WidgetButton(key="portfolio_transactions", label="Transactions"),
                bt.WidgetButton(key="portfolio_trades", label="Trades"),
                bt.WidgetButton(key="instrument_subscriptionsredemptions", label="Subscriptions/Redemptions"),
                bt.WidgetButton(key="instrument_trades", label="Trades (Implemented)"),
                bt.WidgetButton(key="portfolio_fees", label="Fees"),
                bt.WidgetButton(key="portfolio_aggregatedfees", label="Aggregated Fees"),
                bt.DropDownButton(
                    label="Charts",
                    icon=WBIcon.UNFOLD.icon,
                    buttons=(
                        bt.WidgetButton(key="tradechart", label="Nominal"),
                        bt.WidgetButton(key="aumchart", label="AUM"),
                        bt.WidgetButton(key="custodiandistribution", label="Custodian Distribution"),
                        bt.WidgetButton(key="customerdistribution", label="Customer Distribution"),
                    ),
                ),
            ),
        )
