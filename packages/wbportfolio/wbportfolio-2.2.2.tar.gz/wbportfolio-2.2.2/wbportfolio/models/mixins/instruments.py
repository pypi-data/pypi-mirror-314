from contextlib import suppress
from datetime import date
from decimal import Decimal
from typing import Optional

import numpy as np
import pandas as pd
from django.contrib import admin
from django.db import models
from wbcore.contrib.currency.models import CurrencyFXRates
from wbfdm.models.instruments import Instrument, InstrumentPrice


class PMSInstrument(Instrument):
    class Meta:
        proxy = True

    @property
    def total_aum_usd(self):
        if last_nav := self.get_latest_valid_price():
            if (
                fx_rate := CurrencyFXRates.objects.filter(currency=self.currency, date__lte=last_nav.date)
                .order_by("-date")
                .first()
            ):
                return last_nav.net_value * last_nav.valid_outstanding_shares / fx_rate.value
        return Decimal(0)

    @property
    def net_value_key(self):
        return "net_value"

    @property
    @admin.display(description="Invested")
    def _is_invested(self) -> bool:
        """
        Return True if the associated asset portfolio is invested
        """
        return getattr(self, "is_invested", self.portfolio and self.portfolio.is_invested_at_date(date.today()))

    def total_value(self, val_date: date):
        try:
            last_price = self.prices.filter(date__lte=val_date).latest("date")
            return self.total_shares(val_date) * last_price.net_value
        except InstrumentPrice.DoesNotExist:
            return Decimal(0)

    def total_shares(self, val_date):
        from wbportfolio.models.transactions.trades import Trade

        trades = Trade.valid_customer_trade_objects.filter(
            underlying_instrument=self,
        )
        if val_date:
            trades = trades.filter(transaction_date__lt=val_date)
        return trades.aggregate(s=models.Sum("shares"))["s"] or Decimal(0)

    def nominal_value(self, val_date):
        return self.total_shares(val_date) * self.share_price

    def get_latest_valid_price(self, val_date: Optional[date] = None) -> models.Model:
        qs = self.valuations.exclude(net_value=0)
        if val_date and qs.filter(date__lte=val_date).exists():
            qs = qs.filter(date__lte=val_date)
        return qs.latest("date") if qs.exists() else None

    def get_earliest_valid_price(self, val_date: Optional[date] = None) -> models.Model:
        qs = self.valuations.exclude(net_value=0)
        if val_date:
            qs = qs.filter(date__gte=val_date)
        return qs.earliest("date") if qs.exists() else None

    def get_price_range(self, val_date: Optional[date] = None) -> dict:
        prices = self.valuations.order_by("net_value")
        if val_date:
            prices = prices.filter(date__lte=val_date)
        if prices.exists():
            low = prices.first()
            high = prices.last()
            return {
                "high": {"price": float(high.net_value), "date": high.date},
                "low": {"price": float(low.net_value), "date": low.date},
            }
        return {}

    def get_cumulative_shares(self, from_date: date, to_date: date) -> pd.Series:
        from wbportfolio.models.transactions import Trade

        df = pd.DataFrame(
            Trade.valid_customer_trade_objects.filter(underlying_instrument=self).values("transaction_date", "shares"),
            columns=["transaction_date", "shares"],
        )
        df["shares"] = df["shares"].astype(float)
        df["transaction_date"] = df["transaction_date"] + pd.tseries.offsets.BDay(1)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        ts = pd.bdate_range(from_date, to_date, freq="B")
        try:
            shares = df.groupby("transaction_date").sum(numeric_only=True)["shares"].sort_index().fillna(0).cumsum()
            return shares.reindex(ts, method="ffill").fillna(0)
        except KeyError:
            return pd.Series(0, index=ts).rename("shares")

    def update_outstanding_shares(self, clear: bool = False):
        if (from_date := self.inception_date) and (to_date := self.last_price_date):
            update_objs = []
            cumshares = self.get_cumulative_shares(from_date, to_date)
            df = pd.concat([cumshares, (cumshares - cumshares.shift(1)).rename("volume")], axis=1)
            df["volume"] = df["volume"].astype(float)
            df["volume_50d"] = df.volume.rolling(50).mean()
            df["volume_200d"] = df.volume.rolling(50).mean()
            df = df.replace([np.inf, -np.inf, np.nan], None)
            for val_date, row in df.to_dict("index").items():
                with suppress(InstrumentPrice.DoesNotExist):
                    shares = row["shares"]
                    volume = row["volume"]
                    price = InstrumentPrice.objects.get(instrument=self, date=val_date, calculated=True)
                    if (price.outstanding_shares != row["shares"]) or (price.volume != volume) or clear:
                        price.outstanding_shares = shares
                        price.outstanding_shares_consolidated = shares
                        price.volume = volume
                        price.volume_50d = row["volume_50d"]
                        price.volume_200d = row["volume_200d"]
                        update_objs.append(price)
            InstrumentPrice.objects.bulk_update(
                update_objs,
                ["outstanding_shares", "outstanding_shares_consolidated", "volume", "volume_50d", "volume_200d"],
            )
