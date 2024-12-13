import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

import numpy as np
import pandas as pd
from celery import shared_task
from celery.canvas import Signature
from django.db import models
from django.db.models import F
from django.utils import timezone
from wbfdm.enums import MarketData
from wbfdm.models.instruments import Instrument
from wbportfolio.models import Portfolio
from wbportfolio.models.transactions.trade_proposals import TradeProposal
from wbportfolio.pms.typing import Portfolio as PortfolioDTO
from wbportfolio.pms.typing import Position as PositionDTO

from .synchronization import SynchronizationTask


def convert_currency(x, val_date, other_currency):
    instrument = Instrument.objects.get(id=x)
    try:
        return instrument.currency.convert(val_date, other_currency)
    except Exception:
        return np.nan


class PortfolioSynchronization(SynchronizationTask):
    is_automatic_validation = models.BooleanField(
        default=True,
        verbose_name="Automatic validation",
        help_text="Set to True if you want to automatically implement proposed positions",
    )
    propagate_history = models.BooleanField(
        default=False,
        verbose_name="Propagate History",
        help_text="If true, when the depends on portfolio changes at a certain date, this method will trigger a synchronization for each date (at the scheduled frequency) from that date to the latest valid date",
    )

    def synchronize(
        self,
        portfolio: models.Model,
        sync_date: date,
        task_execution_datetime: Optional[datetime] = None,
        override_execution_datetime_validity: Optional[bool] = False,
        post_processing: bool = True,
        **kwargs: Any,
    ):
        """
        This function compute the new portfolio composition after synchronization (returns from `_import_method`) for a
        given date and either update or create the portfolio or create a trade proposal given the new portfolio constituent.

        :param portfolio: The portfolio to synchronize the positions from
        :param sync_date: The date at which we need to synchronize the given portfolio
        :param task_execution_datetime: An optional datetime specifying at which time this task was initially executed.
        :param override_execution_datetime_validity: If true, we don't valide `task_execution_datetime`
        :param kwargs: keyword arguments
        """

        initkwargs = {**kwargs, **self.cast_kwargs}
        if not task_execution_datetime:
            task_execution_datetime = timezone.now()
        if portfolio.is_active_at_date(sync_date):
            if self.is_valid_date(task_execution_datetime) or override_execution_datetime_validity:
                if import_res := list(zip(*self._import_method(portfolio, sync_date, **initkwargs))):
                    effective_positions = list(filter(lambda x: x, import_res[0]))
                    target_positions = list(filter(lambda x: x, import_res[1]))
                    if len(target_positions) > 0:
                        target_portfolio = PortfolioDTO(target_positions)

                        effective_portfolio = (
                            PortfolioDTO(effective_positions) if len(effective_positions) > 0 else None
                        )
                        if self.is_automatic_validation:
                            # We process these positions automatically
                            portfolio.import_positions_at_date(
                                target_portfolio, sync_date, post_processing=post_processing
                            )
                        else:
                            trade_proposal, created = TradeProposal.objects.get_or_create(
                                trade_date=sync_date,
                                portfolio=portfolio,
                                defaults={"comment": "Automatic rebalancing"},
                            )
                            trade_proposal.create_or_update_trades(
                                target_portfolio=target_portfolio, effective_portfolio=effective_portfolio
                            )

                        portfolio.last_synchronization = timezone.now()
                        portfolio.save()

            else:
                logging.info(
                    f"Synchronization invalid: {portfolio.name} synchronization with {self.name} was triggered for {sync_date} but date not valid for crontab schedule {str(self.crontab)}"
                )

    def synchronize_as_task_si(self, portfolio: models.Model, sync_date: date, **kwargs: Any) -> Signature:
        """
        Utility function that returns the signature of the synchronize method
        """
        return synchronize_portfolio_as_task.si(self.id, portfolio.id, sync_date, **kwargs)

    def _tasks_signature(self, sync_date: Optional[date] = None, **kwargs: Any) -> Signature:
        """
        Gather all tasks that needs to run under this synchronization job as a list of celery signatures.
        This method is expected to be implemented at each inheriting class.
        :param args: list
        :param kwargs: dict
        :return: list[signature]
        """
        for portfolio in self.portfolios.all():
            portfolio_sync_dates = []
            if sync_date:
                portfolio_sync_dates = [sync_date]
            elif not sync_date and portfolio.assets.exists() and (latest_asset := portfolio.assets.latest("date")):
                portfolio_sync_dates = map(
                    lambda x: x.date(), pd.date_range(latest_asset.date, date.today(), freq="B", inclusive="left")
                )
            for portfolio_sync_date in portfolio_sync_dates:
                if portfolio.is_active_at_date(portfolio_sync_date):
                    yield synchronize_portfolio_as_task.si(self.id, portfolio.id, portfolio_sync_date, **kwargs)

    @classmethod
    def _default_callback(
        cls,
        portfolio: Portfolio,
        sync_date: date,
        portfolio_created: Optional[Portfolio] = None,
        adjusted_weighting: Optional[Decimal] = Decimal(1.0),
        adjusted_currency_fx_rate: Optional[Decimal] = Decimal(1.0),
        is_estimated: Optional[bool] = False,
        portfolio_total_value: Optional[float] = None,
        **kwargs: Any,
    ):
        """Recursively calculates the position for a portfolio

        Arguments:
            portfolio {portfolio.Portfolio} -- The Portfolio on which the assets will be computed
            sync_date {datetime.date} -- The date on which the assets will be computed

        Keyword Arguments:
            portfolio {portfolio.Portfolio} -- The core portfolio from which the computed position are created (default: {None})
            adjusted_weighting {int} -- the adjusted weight of the current level of index (default: {1})
            adjusted_currency_fx_rate {int} -- the adjusted currency exchange rate on the current level of index (default: {1})

        Yields:
            tuple[dict, dict] -- Two dictionaries: One with filter parameters and one with default values
        """
        is_root_position_estimated = False
        if not portfolio_created:
            if portfolio_created := portfolio.primary_portfolio:
                is_root_position_estimated = (
                    portfolio_created.assets.filter(date=sync_date).count() == 1
                    and portfolio_created.assets.filter(date=sync_date, is_estimated=True).count() == 1
                )
        if portfolio_created:
            child_positions = portfolio_created.assets.filter(date=sync_date)
            asset_positions = child_positions.all()
            # Compute the total portfolio value based on the root position child (otherwise the value is passed as
            # parameters in the recursion
            if not portfolio_total_value:
                portfolio_total_value = child_positions.aggregate(tv=models.Sum(F("total_value_fx_portfolio")))["tv"]
                if not portfolio_total_value:
                    portfolio_total_value = portfolio_created.get_total_value(sync_date)
            for position in child_positions:
                if child_portfolio := position.underlying_instrument.portfolio:
                    if child_portfolio.assets.filter(date=sync_date).exists() and position.weighting is not None:
                        asset_positions = asset_positions.exclude(id=position.id)
                        yield from cls._default_callback(
                            portfolio,
                            sync_date,
                            portfolio_created=child_portfolio,
                            adjusted_weighting=position.weighting * adjusted_weighting,
                            portfolio_total_value=portfolio_total_value,
                            adjusted_currency_fx_rate=position.currency_fx_rate * adjusted_currency_fx_rate,
                            is_estimated=False
                            if is_root_position_estimated
                            else (is_estimated and position.is_estimated),
                        )
            df = pd.DataFrame(
                asset_positions.values_list(
                    "currency_fx_rate",
                    "price",
                    "weighting",
                    "shares",
                    "is_estimated",
                    "underlying_instrument",
                    "currency",
                    "exchange",
                ),
                columns=[
                    "currency_fx_rate",
                    "price",
                    "weighting",
                    "shares",
                    "is_estimated",
                    "underlying_instrument",
                    "currency",
                    "exchange",
                ],
            )
            if not df.empty:
                df.currency_fx_rate = df.currency_fx_rate * adjusted_currency_fx_rate
                df.weighting = df.weighting * adjusted_weighting

                df = (
                    df.groupby(["underlying_instrument", "currency", "exchange"], dropna=False)
                    .agg(
                        {
                            "currency_fx_rate": "first",
                            "price": "first",
                            "weighting": "sum",
                            "shares": "sum",
                            "is_estimated": "first",
                        }
                    )
                    .reset_index()
                )
                df[["underlying_instrument", "currency", "exchange"]] = df[
                    ["underlying_instrument", "currency", "exchange"]
                ].astype("object")
                df[["currency_fx_rate", "price", "weighting", "shares"]] = df[
                    ["currency_fx_rate", "price", "weighting", "shares"]
                ].astype("float")

                df["actual_currency_fx_rate"] = df.underlying_instrument.apply(
                    lambda x: convert_currency(x, sync_date, portfolio.currency)
                ).astype("float")
                df["actual_currency_fx_rate"] = df["actual_currency_fx_rate"].fillna(df["currency_fx_rate"])

                df = df.where(pd.notnull(df), None).set_index("underlying_instrument")
                missing_prices = df.loc[df["price"].isnull(), "price"]
                if not missing_prices.empty:
                    prices_df = pd.DataFrame(
                        Instrument.objects.filter(id__in=missing_prices.index).dl.market_data(
                            values=[MarketData.CLOSE], exact_date=sync_date
                        )
                    )
                    if not prices_df.empty:
                        prices_df = prices_df[["close", "instrument_id"]].set_index("instrument_id").astype("float")
                        df.loc[prices_df.index, "price"] = prices_df

                if portfolio_total_value is not None:
                    df["shares"] = (df["weighting"] * float(portfolio_total_value)) / (
                        df["price"] * df["actual_currency_fx_rate"]
                    )
                if is_estimated:
                    df["is_estimated"] = True
                for underlying_instrument, asset_position in df.to_dict("index").items():
                    if (
                        asset_position["weighting"] or asset_position["shares"]
                    ):  # We don't yield empty position (pos with shares and weight equal to 0 or None)
                        # We return the position as a serialized dictionary
                        yield None, PositionDTO(
                            date=sync_date,
                            asset_valuation_date=sync_date,
                            portfolio_created=portfolio_created.id,
                            underlying_instrument=underlying_instrument,
                            instrument_type=Instrument.objects.get(id=underlying_instrument).security_instrument_type,
                            currency=asset_position["currency"],
                            exchange=asset_position["exchange"],
                            shares=asset_position["shares"],
                            price=asset_position["price"],
                            currency_fx_rate=asset_position["actual_currency_fx_rate"],
                            weighting=asset_position["weighting"],
                            is_estimated=asset_position["is_estimated"],
                        )

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbportfolio:portfoliosynchronizationrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"


@shared_task(queue="portfolio")
def synchronize_portfolio_as_task(synchronization_method_id: int, portfolio_id: int, sync_date: date, **kwargs: Any):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    synchronization_method = PortfolioSynchronization.objects.get(id=synchronization_method_id)
    synchronization_method.synchronize(portfolio, sync_date, **kwargs)
