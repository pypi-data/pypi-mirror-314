import logging
import math
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Optional

import pandas as pd
from celery import shared_task
from celery.canvas import Signature
from django.db import models
from django.utils import timezone
from pandas.tseries.offsets import BDay
from wbfdm.models import Instrument
from wbfdm.models.instruments.instrument_prices import InstrumentPrice

from .synchronization import SynchronizationTask


class PriceComputation(SynchronizationTask):
    @property
    def instruments(self):
        for instrument in Instrument.active_objects.filter(
            models.Q(id__in=self.products.values("id")) | models.Q(id__in=self.indexes.values("id"))
        ):
            yield instrument

    def compute(
        self,
        instrument: models.Model,
        sync_date: date,
        task_execution_datetime: Optional[datetime] = None,
        override_execution_datetime_validity: Optional[bool] = False,
        **kwargs: Any,
    ):
        """
        Given positions at t and t-1, we compute the performance and estimate the instrument price at t
        If a price already exists at that date and is estimated already, we update it. If no price exists, we create it as estimated.
        Otherwise, we don't do anything to protect imported real prices.
        :param instrument: The instrument to compute the new price from
        :param sync_date: The date at which we need to compute the new price
        :param task_execution_datetime: An optional datetime specifying at which time this task was initially executed.
        :param override_execution_datetime_validity: If true, we don't valide `task_execution_datetime`
        :param kwargs: keyword arguments
        """
        if not task_execution_datetime:
            task_execution_datetime = timezone.now()

        if (
            (self.is_valid_date(task_execution_datetime) or override_execution_datetime_validity)
            and instrument.is_active_at_date(sync_date)
            and not sync_date.weekday() in [5, 6]
        ):
            price_data = self._import_method(instrument, sync_date, **kwargs)
            if (
                price_data
                and (_instrument := price_data.pop("instrument", None))
                and (_date := price_data.pop("date", None))
            ):
                calculated = price_data.pop("calculated", True)
                try:
                    price = InstrumentPrice.objects.get(instrument=_instrument, date=_date, calculated=calculated)
                    for k, v in price_data.items():
                        setattr(price, k, v)
                    price.save()
                except InstrumentPrice.DoesNotExist:
                    price = InstrumentPrice.objects.create(
                        instrument=_instrument, date=_date, calculated=calculated, **price_data
                    )

                price.save()  # trigger explicitly save logic as update_or_create doesn't
                if (
                    _date == _instrument.prices.latest("date").date
                ):  # if price date is the latest instrument price date, we recomputet the last valuation data
                    _instrument.update_last_valuation_date()
        else:
            logging.info(
                f"Price Computation invalid: {str(instrument)} price computation with {self.name} was triggered for {sync_date} but date not valid for crontab schedule {str(self.crontab)}"
            )

    def compute_price_as_task_si(self, instrument: models.Model, sync_date: date, **kwargs: Any) -> Signature:
        """
        Utility function that returns the signature of the compute method
        """
        return compute_price_as_task.si(self.id, instrument.id, sync_date, **kwargs)

    def _tasks_signature(
        self, sync_date: Optional[date] = None, to_date: Optional[date] = None, **kwargs: Any
    ) -> Signature:
        """
        Gather all tasks that needs to run under this synchronization job as a list of celery signatures.
        This method is expected to be implemented at each inheriting class.
        :param args: list
        :param kwargs: dict
        :return: list[signature]
        """
        if not to_date:
            to_date = date.today()
        for instrument in self.instruments:
            # Get latest valuation date + 1 Bday if not given by the key word arguments
            instrument_sync_dates = []
            if sync_date:
                instrument_sync_dates = [sync_date]
            elif not sync_date and instrument.prices.exists() and (last_price := instrument.prices.latest("date")):
                instrument_sync_dates = map(
                    lambda x: x.date(),
                    pd.date_range(
                        max(last_price.date, to_date - timedelta(days=7)),
                        to_date,
                        freq="B",
                        inclusive="left",
                    ),
                )
            for instrument_sync_date in instrument_sync_dates:
                if instrument.is_active_at_date(instrument_sync_date):
                    yield compute_price_as_task.si(self.id, instrument.id, instrument_sync_date, **kwargs)

    @classmethod
    def _default_callback(cls, instrument: Instrument, val_date: date, **kwargs: Any):
        """
        Default NAV computation function. We simply compute the performance given two positions for two dates and estimate the new price
        based on the overall performance.
        TODO: If exit/buy of positions, is this function still correct?
        :param instrument: The instrument to compute the new price from
        :param val_date: The date at which we need to compute the new price
        :param kwargs: keyword arguments
        """
        if portfolio := instrument.portfolio:
            # check if the asset portfolio of this instruments exists and has positions at the synchronization date
            if previous_date := portfolio.get_latest_asset_position_date(val_date - BDay(1), with_estimated=True):
                # Get the previous valid price date before sync_date, checks if it exists and if positions are available
                # at that date.
                # If asset position exists on the previous day but not at the sync date, maybe propagation were not done, and we try it
                if portfolio.assets.filter(date=previous_date).exists():
                    portfolio.propagate_or_update_assets(previous_date, val_date)
                    if portfolio.assets.filter(date=val_date).exists():
                        last_price = None
                        if (
                            last_valuation := instrument.prices.filter(date=previous_date)
                            .order_by("calculated")
                            .first()
                        ):
                            last_price = last_valuation.net_value
                        elif not instrument.valuations.filter(date__lt=previous_date).exists():
                            last_price = instrument.issue_price
                        if last_price:
                            weights = pd.DataFrame(
                                portfolio.assets.filter(date=previous_date).values(
                                    "weighting", "date", "underlying_instrument"
                                )
                            )
                            weights = weights.pivot_table(
                                index="date", columns=["underlying_instrument"], values="weighting", aggfunc="sum"
                            ).astype("float")
                            weights = weights.iloc[-1, :]
                            perfs = pd.DataFrame(
                                portfolio.assets.filter(date__in=[previous_date, val_date]).values(
                                    "date", "price_fx_portfolio", "underlying_instrument"
                                )
                            )
                            perfs = perfs.pivot_table(
                                index="date",
                                columns=["underlying_instrument"],
                                values="price_fx_portfolio",
                                aggfunc="mean",
                            ).astype("float")
                            perfs = perfs / perfs.shift(1, axis=0) - 1.0
                            perfs = perfs.fillna(0).iloc[-1, :]
                            total_perfs = float((perfs * weights).sum())
                            new_gross_valuation = float(last_price) * (1.0 + total_perfs)
                            if new_gross_valuation and not math.isnan(new_gross_valuation):
                                return {
                                    "instrument": instrument,
                                    "date": val_date,
                                    "gross_value": Decimal(new_gross_valuation),
                                    "net_value": Decimal(new_gross_valuation),
                                }

        return None

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbportfolio:pricecomputationrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"


@shared_task(queue="portfolio")
def compute_price_as_task(price_computation_method_id: int, instrument_id: int, sync_date: date, **kwargs: Any):
    instrument = Instrument.objects.get(id=instrument_id)
    price_computation = PriceComputation.objects.get(id=price_computation_method_id)
    price_computation.compute(instrument, sync_date, **kwargs)
