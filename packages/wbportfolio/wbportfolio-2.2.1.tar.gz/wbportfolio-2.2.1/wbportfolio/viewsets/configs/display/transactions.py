from typing import Optional

from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    Display,
    create_simple_display,
)
from wbcore.metadata.configs.display.instance_display.utils import repeat_field
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class TransactionDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="transaction_type", label="Type"),
                dp.Field(key="transaction_underlying_type", label="Underlying Type"),
                dp.Field(key="transaction_date", label="Transaction Date"),
                dp.Field(key="portfolio", label="Portfolio"),
                dp.Field(key="underlying_instrument", label="Instrument"),
                dp.Field(key="currency_fx_rate", label="FX Rate"),
                dp.Field(key="currency", label="Currency"),
                dp.Field(key="total_value", label="Total Value"),
                dp.Field(key="total_value_fx_portfolio", label="Total Value (Portfolio)"),
                dp.Field(key="total_value_usd", label="Total Value ($)"),
            ]
        )

    def get_instance_display(self) -> Display:
        return create_simple_display(
            [
                ["transaction_type", "underlying_instrument", "external_id"],
                ["transaction_date", "book_date", "value_date"],
                ["currency", "total_value", "total_value_fx_portfolio"],
                [".", "total_value_gross", "total_value_gross_fx_portfolio"],
                [repeat_field(3, "comment")],
            ]
        )


class TransactionPortfolioDisplayConfig(TransactionDisplayConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="transaction_type", label="Type"),
                dp.Field(key="transaction_underlying_type", label="Underlying Type"),
                dp.Field(key="transaction_date", label="Transaction Date"),
                dp.Field(key="underlying_instrument", label="Instrument"),
                dp.Field(key="currency_fx_rate", label="FX Rate"),
                dp.Field(key="currency", label="Currency"),
                dp.Field(key="total_value", label="Total Value"),
                dp.Field(key="total_value_fx_portfolio", label="Total Value (Portfolio)"),
                dp.Field(key="total_value_usd", label="Total Value ($)"),
            ]
        )
