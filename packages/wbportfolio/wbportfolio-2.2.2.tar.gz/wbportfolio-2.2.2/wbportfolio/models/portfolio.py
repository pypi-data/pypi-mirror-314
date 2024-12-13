from contextlib import suppress
from datetime import date, datetime, timedelta
from decimal import Decimal
from math import isclose
from typing import Any

import numpy as np
import pandas as pd
from celery import shared_task
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models import (
    BooleanField,
    Case,
    Exists,
    F,
    OuterRef,
    Q,
    QuerySet,
    Sum,
    Value,
    When,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from psycopg.types.range import DateRange
from wbcore.contrib.currency.models import CurrencyFXRates
from wbcore.models import WBModel
from wbcore.utils.models import ActiveObjectManager, DeleteToDisableMixin
from wbfdm.contrib.metric.dispatch import compute_metrics
from wbfdm.models import Instrument
from wbfdm.models.instruments.instrument_prices import InstrumentPrice
from wbportfolio.models.asset import AssetPosition
from wbportfolio.models.indexes import Index
from wbportfolio.models.portfolio_relationship import (
    InstrumentPortfolioThroughModel,
    PortfolioInstrumentPreferredClassificationThroughModel,
)
from wbportfolio.models.products import Product
from wbportfolio.pms.typing import Portfolio as PortfolioDTO

from .utils import get_casted_portfolio_instrument


class DefaultPortfolioQueryset(QuerySet):
    def filter_invested_at_date(self, val_date: date) -> QuerySet:
        """
        Filter the queryset to get only portfolio invested at the given date
        """
        return self.filter(invested_timespan__startswith__lte=val_date, invested_timespan__endswith__gt=val_date)


class DefaultPortfolioManager(ActiveObjectManager):
    def get_queryset(self):
        return DefaultPortfolioQueryset(self.model).filter(is_active=True)

    def filter_invested_at_date(self, val_date: date):
        return self.get_queryset().filter_invested_at_date(val_date)


class ActiveTrackedPortfolioManager(DefaultPortfolioManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(asset_exists=Exists(AssetPosition.objects.filter(portfolio=OuterRef("pk"))))
            .filter(asset_exists=True, is_tracked=True)
        )


class PortfolioPortfolioThroughModel(models.Model):
    class Type(models.TextChoices):
        PRIMARY = "PRIMARY", "Primary"
        MODEL = "MODEL", "Model"
        BENCHMARK = "BENCHMARK", "Benchmark"
        INDEX = "INDEX", "Index"
        CUSTODIAN = "CUSTODIAN", "Custodian"

    portfolio = models.ForeignKey("wbportfolio.Portfolio", on_delete=models.CASCADE, related_name="dependency_through")
    dependency_portfolio = models.ForeignKey(
        "wbportfolio.Portfolio", on_delete=models.CASCADE, related_name="dependent_through"
    )
    type = models.CharField(choices=Type.choices, default=Type.PRIMARY, verbose_name="Type")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["portfolio", "type"], name="unique_primary", condition=Q(type="PRIMARY")),
            models.UniqueConstraint(fields=["portfolio", "type"], name="unique_model", condition=Q(type="MODEL")),
        ]


class Portfolio(DeleteToDisableMixin, WBModel):
    assets: models.QuerySet[AssetPosition]

    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        default="",
        help_text="The Name of the Portfolio",
    )

    currency = models.ForeignKey(
        to="currency.Currency",
        related_name="portfolios",
        on_delete=models.PROTECT,
        verbose_name="Currency",
        help_text="The currency of the portfolio.",
    )
    hedged_currency = models.ForeignKey(
        to="currency.Currency",
        related_name="hedged_portfolios",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Hedged Currency",
        help_text="The hedged currency of the portfolio.",
    )
    depends_on = models.ManyToManyField(
        "wbportfolio.Portfolio",
        symmetrical=False,
        related_name="dependent_portfolios",
        through="wbportfolio.PortfolioPortfolioThroughModel",
        through_fields=("portfolio", "dependency_portfolio"),
        blank=True,
        verbose_name="The portfolios this portfolio depends on",
    )

    portfolio_synchronization = models.ForeignKey(
        "wbportfolio.PortfolioSynchronization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="portfolios",
        verbose_name="Portfolio Synchronization Method",
    )
    preferred_instrument_classifications = models.ManyToManyField(
        "wbfdm.Instrument",
        limit_choices_to=(models.Q(instrument_type__is_classifiable=True) & models.Q(level=0)),
        related_name="preferred_portfolio_classifications",
        through="wbportfolio.PortfolioInstrumentPreferredClassificationThroughModel",
        through_fields=("portfolio", "instrument"),
        blank=True,
        verbose_name="The Preferred classification per instrument",
    )
    instruments = models.ManyToManyField(
        "wbfdm.Instrument",
        through=InstrumentPortfolioThroughModel,
        related_name="portfolios",
        blank=True,
        verbose_name="Instruments",
        help_text="Instruments linked to this instrument",
    )
    invested_timespan = DateRangeField(
        null=True, blank=True, help_text="Define when this portfolio is considered invested"
    )

    is_manageable = models.BooleanField(
        default=False,
        help_text="True if the portfolio can be manually modified (e.g. Trade proposal be submitted or total weight recomputed)",
    )
    is_tracked = models.BooleanField(
        default=True,
        help_text="True if the internal updating mechanism (e.g., Propagation, Synchronization etc...) needs to apply to this portfolio",
    )
    only_weighting = models.BooleanField(
        default=False,
        help_text="Indicates that this portfolio is only utilizing weights and disregards shares, e.g. a model portfolio",
    )

    last_synchronization = models.DateTimeField(blank=True, null=True, verbose_name="Last Synchronization Date")
    bank_accounts = models.ManyToManyField(
        to="directory.BankingContact",
        related_name="wbportfolio_portfolios",
        through="wbportfolio.PortfolioBankAccountThroughModel",
        blank=True,
    )
    objects = DefaultPortfolioManager()
    tracked_objects = ActiveTrackedPortfolioManager()

    @property
    def primary_portfolio(self):
        with suppress(PortfolioPortfolioThroughModel.DoesNotExist):
            return PortfolioPortfolioThroughModel.objects.get(
                portfolio=self, type=PortfolioPortfolioThroughModel.Type.PRIMARY
            ).dependency_portfolio

    @property
    def model_portfolio(self):
        with suppress(PortfolioPortfolioThroughModel.DoesNotExist):
            return PortfolioPortfolioThroughModel.objects.get(
                portfolio=self, type=PortfolioPortfolioThroughModel.Type.MODEL
            ).dependency_portfolio

    @property
    def benchmark_portfolio(self):
        with suppress(PortfolioPortfolioThroughModel.DoesNotExist):
            return PortfolioPortfolioThroughModel.objects.get(
                portfolio=self, type=PortfolioPortfolioThroughModel.Type.BENCHMARK
            ).dependency_portfolio

    @property
    def imported_assets(self):
        return self.assets.filter(is_estimated=False)

    def delete(self, **kwargs):
        super().delete(**kwargs)
        # We check if for all linked instruments, this portfolio was the last active one (if yes, we disable the instrument)
        if self.id:
            for instrument in self.instruments.iterator():
                if not instrument.portfolios.filter(is_active=True).exists():
                    instrument.delisted_date = date.today() - timedelta(days=1)
                    instrument.save()

    def _build_dto(self, val_date: date, **extra_filter_kwargs) -> PortfolioDTO:
        "returns the dto representation of this portfolio at the specified date"
        return PortfolioDTO(
            tuple([pos._build_dto() for pos in self.assets.filter(date=val_date, **extra_filter_kwargs)])
        )

    def is_invested_at_date(self, val_date: date) -> bool:
        return (
            self.invested_timespan
            and self.invested_timespan.upper > val_date
            and self.invested_timespan.lower <= val_date
        )

    def __str__(self):
        return f"{self.id:06} ({self.name})"

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

        notification_types = [
            (
                "wbportfolio.portfolio.check_custodian_portfolio",
                "Check Custodian Portfolio",
                "Sends a notification when a portfolio does not match with its custodian portfolio",
                True,
                True,
                True,
            ),
        ]

    @classmethod
    def create_model_portfolio(cls, name, currency, portfolio_synchronization=None, index_parameters=dict()):
        portfolio = cls.objects.create(
            is_manageable=True,
            name=name,
            currency=currency,
            portfolio_synchronization=portfolio_synchronization,
        )
        if index_parameters:
            index = Index.objects.create(name=name, currency=currency, **index_parameters)
            index.portfolios.all().delete()
            InstrumentPortfolioThroughModel.objects.update_or_create(
                instrument=index, defaults={"portfolio": portfolio}
            )
        return portfolio

    def is_active_at_date(self, val_date: date) -> bool:
        """
        Return if the base instrument has a total aum greater than 0
        :val_date: the date at which we need to evaluate if the portfolio is considered active
        """
        active_portfolio = self.is_active or self.deletion_datetime.date() > val_date
        if self.instruments.exists():
            return active_portfolio and any(
                [instrument.is_active_at_date(val_date) for instrument in self.instruments.all()]
            )
        return active_portfolio

    def get_aum(self, val_date: date) -> Decimal:
        """
        Return the total asset under management of the portfolio at the specified valuation date
        Args:
            val_date: The date at which aum needs to be computed
        Returns:
            The total AUM (0 if there is no position)
        """
        return self.assets.filter(date=val_date).aggregate(s=Sum("total_value_fx_portfolio"))["s"] or Decimal(0.0)

    def get_total_value(self, val_date):
        from wbportfolio.models.transactions.trades import Trade

        trades = Trade.valid_customer_trade_objects.filter(portfolio=self, transaction_date__lte=val_date)

        total_aum = Decimal(0)
        for underlying_instrument_id, sum_shares in (
            trades.values("underlying_instrument")
            .annotate(
                sum_shares=Sum("shares"),
            )
            .values_list("underlying_instrument", "sum_shares")
        ):
            with suppress(Instrument.DoesNotExist, InstrumentPrice.DoesNotExist):
                instrument = Instrument.objects.get(id=underlying_instrument_id)
                last_price = instrument.valuations.filter(date__lte=val_date).latest("date").net_value
                fx_rate = instrument.currency.convert(val_date, self.currency)
                total_aum += last_price * sum_shares * fx_rate
        return total_aum

    def _get_assets(self, with_estimated=True, with_cash=True):
        qs = self.assets
        if not with_estimated:
            qs = qs.filter(is_estimated=False)
        if not with_cash:
            qs = qs.exclude(underlying_instrument__is_cash=True)
        return qs

    def get_earliest_asset_position_date(self, val_date=None, with_estimated=False):
        qs = self._get_assets(with_estimated=with_estimated)
        if val_date:
            qs = qs.filter(date__gte=val_date)
        if qs.exists():
            return qs.earliest("date").date
        return None

    def get_latest_asset_position_date(self, val_date=None, with_estimated=False):
        qs = self._get_assets(with_estimated=with_estimated)
        if val_date:
            qs = qs.filter(date__lte=val_date)

        if qs.exists():
            return qs.latest("date").date
        return None

    # Asset Position Utility Functions
    def get_holding(self, val_date, exclude_cash=True, exclude_index=True):
        qs = self._get_assets(with_cash=not exclude_cash).filter(date=val_date, weighting__gt=0)
        if exclude_index:
            qs = qs.exclude(underlying_security_instrument_type_key="index")
        return (
            qs.values("underlying_instrument__name")
            .annotate(total_value_fx_portfolio=Sum("total_value_fx_portfolio"), weighting=Sum("weighting"))
            .order_by("-total_value_fx_portfolio")
        )

    def _get_groupedby_df(
        self,
        group_by,
        val_date: date,
        exclude_cash: bool | None = False,
        exclude_index: bool | None = False,
        extra_filter_parameters: dict[str, Any] = None,
        **groupby_kwargs,
    ):
        qs = self._get_assets(with_cash=not exclude_cash).filter(date=val_date)
        if exclude_index:
            # We exclude only index that are not considered as cash. Setting exclude_cash to true convers this case.
            qs = qs.exclude(
                Q(underlying_security_instrument_type_key="index") & Q(underlying_instrument__is_cash=False)
            )
        if extra_filter_parameters:
            qs = qs.filter(**extra_filter_parameters)
        qs = group_by(qs, **groupby_kwargs).annotate(sum_weighting=Sum(F("weighting"))).order_by("-sum_weighting")
        df = pd.DataFrame(
            qs.values_list("aggregated_title", "sum_weighting"), columns=["aggregated_title", "weighting"]
        )
        if not df.empty:
            df.weighting = df.weighting.astype("float")
            df.weighting = df.weighting / df.weighting.sum()
            df = df.sort_values(by=["weighting"])
        return df.where(pd.notnull(df), None)

    def get_geographical_breakdown(self, val_date, **kwargs):
        df = self._get_groupedby_df(
            AssetPosition.country_group_by, val_date=val_date, exclude_cash=True, exclude_index=True, **kwargs
        )
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_currency_exposure(self, val_date, **kwargs):
        df = self._get_groupedby_df(AssetPosition.currency_group_by, val_date=val_date, **kwargs)
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_equity_market_cap_distribution(self, val_date, **kwargs):
        df = self._get_groupedby_df(
            AssetPosition.marketcap_group_by,
            val_date=val_date,
            exclude_cash=True,
            exclude_index=True,
            extra_filter_parameters={"underlying_security_instrument_type_key": "equity"},
            **kwargs,
        )
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_equity_liquidity(self, val_date, **kwargs):
        df = self._get_groupedby_df(
            AssetPosition.liquidity_group_by,
            val_date=val_date,
            exclude_cash=True,
            exclude_index=True,
            extra_filter_parameters={"underlying_security_instrument_type_key": "equity"},
            **kwargs,
        )
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_industry_exposure(self, val_date=None, **kwargs):
        df = self._get_groupedby_df(
            AssetPosition.group_by_primary, val_date=val_date, exclude_cash=True, exclude_index=True, **kwargs
        )
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_asset_allocation(self, val_date=None, **kwargs):
        df = self._get_groupedby_df(AssetPosition.cash_group_by, val_date=val_date, **kwargs)
        if not df.empty:
            df = df[df["weighting"] != 0]
        return df

    def get_adjusted_child_positions(self, val_date):
        if (
            child_positions := self.assets.exclude(underlying_instrument__is_cash=True).filter(date=val_date)
        ).count() == 1:
            if portfolio := child_positions.first().underlying_instrument.primary_portfolio:
                child_positions = portfolio.assets.exclude(underlying_instrument__is_cash=True).filter(date=val_date)
        for position in child_positions:
            if child_portfolio := position.underlying_instrument.primary_portfolio:
                index_positions = child_portfolio.assets.exclude(underlying_instrument__is_cash=True).filter(
                    date=val_date
                )

                for index_position in index_positions.all():
                    weighting = index_position.weighting * position.weighting
                    if weighting != 0:
                        yield {
                            "underlying_instrument_id": index_position.underlying_instrument.id,
                            "weighting": weighting,
                        }

    def get_longshort_distribution(self, val_date):
        df = pd.DataFrame(self.get_adjusted_child_positions(val_date))

        if not df.empty:
            df["is_cash"] = df.underlying_instrument_id.apply(lambda x: Instrument.objects.get(id=x).is_cash)
            df = df[~df["is_cash"]]
            df = (
                df[["underlying_instrument_id", "weighting"]].groupby("underlying_instrument_id").sum().astype("float")
            )
            df.weighting = df.weighting / df.weighting.sum()
            short_weight = df[df.weighting < 0].weighting.abs().sum()
            long_weight = df[df.weighting > 0].weighting.sum()
            total_weight = long_weight + short_weight
            return pd.DataFrame(
                [
                    {"title": "Long", "weighting": long_weight / total_weight},
                    {"title": "Short", "weighting": short_weight / total_weight},
                ]
            )
        return df

    def get_portfolio_contribution_df(self, start, end, with_cash=True, hedged_currency=None, only_equity=False):
        qs = self._get_assets(with_cash=with_cash).filter(date__gte=start, date__lte=end)
        if only_equity:
            qs = qs.filter(underlying_security_instrument_type_key="equity")
        return Portfolio.get_contribution_df(qs, hedged_currency=hedged_currency)

    def check_related_portfolio_at_date(self, val_date: date, related_portfolio: "Portfolio"):
        assets = AssetPosition.objects.filter(
            date=val_date, underlying_instrument__is_cash=False, underlying_instrument__is_cash_equivalent=False
        ).values("underlying_instrument__parent", "shares")
        assets1 = assets.filter(portfolio=self)
        assets2 = assets.filter(portfolio=related_portfolio)
        return assets1.difference(assets2)

    def change_at_date(
        self,
        val_date: date,
        recompute_weighting: bool = False,
        force_recompute_weighting: bool = False,
        synchronize: bool = True,
        **sync_kwargs,
    ):
        qs = (
            self.assets.filter(date=val_date)
            .filter(Q(total_value_fx_portfolio__isnull=False) | Q(weighting__isnull=False))
            .distinct()
        )

        # We normalize weight across the portfolio for a given date
        if (self.portfolio_synchronization or self.is_manageable or force_recompute_weighting) and qs.exists():
            total_weighting = qs.aggregate(s=Sum("weighting"))["s"]
            # We check if this actually necessary
            # (i.e. if the weight is already summed to 100%, it is already normalized)
            if not total_weighting or not isclose(total_weighting, Decimal(1.0), abs_tol=0.001) or recompute_weighting:
                total_value = qs.aggregate(s=Sum("total_value_fx_portfolio"))["s"]
                # TODO we change this because postgres doesn't support join statement in update (and total_value_fx_portfolio is a joined annoted field)
                for asset in qs:
                    if total_value:
                        asset.weighting = asset._total_value_fx_portfolio / total_value
                    elif total_weighting:
                        asset.weighting = asset.weighting / total_weighting
                    asset.save()
        if synchronize:
            for dependent_portfolio in self.dependent_portfolios.exclude(id=self.id).distinct():
                # Check if the dependent portfolio has a synchronization method and has assets at the specified date
                if (synchronization := dependent_portfolio.portfolio_synchronization) and (
                    dependent_portfolio.assets.filter(date__gte=val_date).exists()
                ):
                    # If this is true, we want to apply the synchronization at every synchronization period
                    # (scheduled crontab) from val_date to now.
                    if synchronization.propagate_history:
                        for _d in synchronization.dates_range(
                            val_date, dependent_portfolio.assets.latest("date").date, filter_daily=True
                        ):
                            synchronization.synchronize_as_task_si(
                                dependent_portfolio, _d, override_execution_datetime_validity=True
                            ).apply_async()
                    # Otherwise, we simply call a unique task for that date
                    else:
                        synchronization.synchronize_as_task_si(
                            dependent_portfolio, val_date, override_execution_datetime_validity=True
                        ).apply_async()

            # We check if there is an instrument attached to the portfolio with calculated NAV and price computation method
            for instrument in self.instruments.all():
                if price_computation := getattr(
                    get_casted_portfolio_instrument(instrument), "price_computation", None
                ):
                    inception_date = instrument.inception_date
                    if isinstance(inception_date, datetime):
                        inception_date = inception_date.date()

                    if isinstance(val_date, datetime):
                        val_date = val_date.date()

                    if inception_date is None or inception_date > val_date:
                        instrument.inception_date = val_date
                        instrument.save()
                    price_computation.compute(instrument, val_date, override_execution_datetime_validity=True)
            compute_metrics(val_date, basket=self)

    def propagate_or_update_assets(
        self,
        from_date: date,
        to_date: date,
        forward_price: bool | None = True,
        base_assets: dict[str, str] | None = None,
        delete_existing_assets: bool | None = False,
    ):
        # we don't propagate on already imported portfolio by default
        is_target_portfolio_imported = self.assets.filter(date=to_date, is_estimated=False).exists()
        if not base_assets:
            base_assets = dict()

        def _get_next_asset_valuation_date(current_asset_valuation_date):
            return (current_asset_valuation_date + pd.offsets.BDay(np.busday_count(from_date, to_date))).date()

        last_fx_date = CurrencyFXRates.objects.filter(date__lte=to_date).latest("date").date
        fx_rates = CurrencyFXRates.objects.filter(date=last_fx_date)
        assets = self.assets.filter(date=from_date)

        from_is_active = self.is_active_at_date(from_date)
        to_is_active = self.is_active_at_date(to_date)
        # # We check is the current assets are already stored and if there is no already stored valid assets
        # # With this, we ensure that we don't overwrite imported asset position with propagated ones.
        # assets_positions_next_day_count = self.assets.filter(date=to_date).count()
        if assets.exists() or base_assets:
            # Remove already existing assets
            if delete_existing_assets:
                self.assets.filter(date=to_date).delete()
            asset_list = list()
            # If base_assets is provided,
            # we assume that the portfolio composition is injected by this list of dictionary
            if base_assets:
                base_assets = (
                    base_assets
                    if isinstance(base_assets, dict)
                    else {asset_id: Decimal(1 / len(base_assets)) for asset_id in base_assets}
                )

            remaining_base_assets = base_assets.copy()
            # Loop over existing assets and construct the propagation assets list
            for asset in assets.all():
                # if a composition is provided, we ensure that existing assets don't deviate from it
                if (base_assets and asset.underlying_instrument.id in base_assets.keys()) or not base_assets:
                    next_asset_valuation_date = _get_next_asset_valuation_date(asset.asset_valuation_date)
                    with suppress(ValueError):
                        asset_list.append(
                            {
                                "initial_price": (
                                    asset.initial_price
                                    if asset._price is not None
                                    else asset.underlying_instrument.get_price(from_date)
                                ),
                                "asset_valuation_date": next_asset_valuation_date,
                                "weighting": asset.weighting,
                                "next_initial_price": asset.underlying_instrument.get_price(next_asset_valuation_date),
                                "underlying_instrument": asset.underlying_instrument,
                                "exchange": asset.exchange,
                                "portfolio": asset.portfolio,
                                "portfolio_created": asset.portfolio_created,
                                "currency": asset.currency,
                                "initial_shares": asset.initial_shares,
                            }
                        )
                remaining_base_assets.pop(asset.underlying_instrument.id, None)
            # We ensure that the propagation assets list contains the proposed composition
            for asset_id, weighting in remaining_base_assets.items():
                instrument = Instrument.objects.get(id=asset_id)
                with suppress(ValueError):
                    asset_list.append(
                        {
                            "underlying_instrument": instrument,
                            "initial_price": instrument.get_price(from_date),
                            "next_initial_price": instrument.get_price(to_date),
                            "asset_valuation_date": to_date,
                            "initial_shares": None,
                            "portfolio": self,
                            "currency": instrument.currency,
                            "weighting": weighting,
                        }
                    )

            df = pd.DataFrame(asset_list)
            if not df.empty:
                df[["initial_price", "weighting", "next_initial_price"]] = df[
                    ["initial_price", "weighting", "next_initial_price"]
                ].astype("float")
                idxx = pd.isnull(df["initial_price"]) & ~pd.isnull(df["next_initial_price"])
                df.loc[idxx, "initial_price"] = df.loc[idxx, "next_initial_price"]
                if forward_price:
                    idx = pd.isnull(df["next_initial_price"])
                    df.loc[idx, "next_initial_price"] = df.loc[idx, "initial_price"]
                df = df.dropna(axis=0, subset=["next_initial_price", "initial_price"])
                # Normalize weight to 100%. Exclude portfolio were sum of weight equals 0 (e.g. short/long portfolio)
                if df.weighting.sum() != 0:
                    df["weighting"] /= df.weighting.sum()
                df.loc[:, "perf"] = df.loc[:, "next_initial_price"] / df.loc[:, "initial_price"]
                df["contribution"] = df.perf * df.weighting
                df.loc[:, "next_weighting"] = df.contribution

                if df.contribution.sum() != 0:
                    df.loc[:, "next_weighting"] /= df.contribution.sum()

                # Normalize next weighting
                if df.next_weighting.sum() != 0:
                    df.next_weighting /= df.next_weighting.sum()
                df = df.replace([np.inf, -np.inf, np.nan], None)
                df.loc[(df["next_weighting"] < -1) | (df["next_weighting"] > 1), "next_weighting"] = df.loc[
                    (df["next_weighting"] < -1) | (df["next_weighting"] > 1), "weighting"
                ]  # if the next weighting is not including within -1 and 1 range, we default to the initial weighting
                if not df.empty:
                    for row in df.to_dict("records"):
                        weighting = Decimal(row["next_weighting"]) if row["next_weighting"] else row["weighting"]
                        if from_is_active and not to_is_active:
                            weighting = Decimal(0.0)
                        try:
                            initial_currency_fx_rate = (
                                fx_rates.get(currency=self.currency).value
                                / fx_rates.get(currency=row["currency"]).value
                            )
                        except CurrencyFXRates.DoesNotExist:
                            initial_currency_fx_rate = Decimal(1)
                        defaults = {
                            "initial_currency_fx_rate": initial_currency_fx_rate,
                            "weighting": weighting,
                            "initial_price": Decimal(row["next_initial_price"]),
                            "initial_shares": row["initial_shares"],
                            "asset_valuation_date": row["asset_valuation_date"],
                            "is_estimated": True,
                        }
                        get_parameters = {
                            "underlying_instrument": row["underlying_instrument"],
                            "portfolio": self,
                            "currency": row["currency"],
                            "date": to_date,
                        }
                        if exchange := row.get("exchange", None):
                            get_parameters["exchange"] = exchange
                        if portfolio_created := row.get("portfolio_created", None):
                            get_parameters["portfolio_created"] = portfolio_created
                        # We check if an asset position already exists and if so, if it is estimated
                        # (otherwise we don't propagate it)
                        if _asset := AssetPosition.objects.filter(**get_parameters).first():
                            _asset.underlying_instrument_price = None  # we unset the previously linked underlying instrument price in case it was linked to the wrong underlying price (e.g too early)
                            if not from_is_active and not to_is_active:
                                _asset.delete()
                            elif not is_target_portfolio_imported and _asset.is_estimated:
                                for k, v in defaults.items():
                                    setattr(_asset, k, v)
                                _asset.save()
                        elif from_is_active and to_is_active and not is_target_portfolio_imported:
                            AssetPosition.objects.create(**get_parameters, **defaults)

    def import_positions_at_date(self, portfolio: PortfolioDTO, val_date: date, post_processing: bool = False):
        if not portfolio:
            return
        left_over_positions = self.assets.filter(date=val_date)

        # We convert the positions into a dataframe in order to handle positions that are considered duplicates
        # In that case, we sum up fields such as weighting and shares.
        # Position are assumed serialized otherwise the groupby on dataframe can't handle django object
        index_columns = ["portfolio_id", "date", "underlying_instrument_id", "portfolio_created_id"]
        float_columns = [
            "weighting",
            "initial_currency_fx_rate",
            "initial_shares",
            "initial_price",
        ]
        df = portfolio.to_df().rename(
            columns={
                "currency_fx_rate": "initial_currency_fx_rate",
                "shares": "initial_shares",
                "price": "initial_price",
                "currency": "currency_id",
                "underlying_instrument": "underlying_instrument_id",
                "portfolio_created": "portfolio_created_id",
                "exchange": "exchange_id",
            }
        )
        df["portfolio_id"] = self.id
        df = df[index_columns + float_columns + ["is_estimated", "currency_id"]]
        df[float_columns] = df[float_columns].astype("float")
        df = df.groupby(index_columns, as_index=False, dropna=False).agg(
            {
                **{field: "first" for field in df.columns.difference(index_columns + float_columns)},
                "weighting": "sum",
                "initial_shares": "sum",
                "initial_currency_fx_rate": "mean",
                "initial_price": "mean",
            }
        )
        df = df.replace([np.inf, -np.inf, np.nan], None)

        for position in df.to_dict("records"):
            obj, _ = AssetPosition.unannotated_objects.update_or_create(
                portfolio_id=position["portfolio_id"],
                date=position["date"],
                underlying_instrument_id=position["underlying_instrument_id"],
                portfolio_created_id=position["portfolio_created_id"],
                defaults=position,
            )
            left_over_positions = left_over_positions.exclude(id=obj.id)
        left_over_positions.delete()
        if post_processing:
            trigger_portfolio_change_as_task.delay(self.id, val_date)

    def resynchronize_history(self, from_date: date, to_date: date, instrument: Instrument | None = None):
        if (synchronisation_method := self.portfolio_synchronization) and self.assets.exists():
            if not from_date:
                from_date = self.assets.earliest("date").date
            if not to_date:
                to_date = self.assets.latest("date").date
            # loop over every week day and trigger synchronization task in order
            if to_date <= from_date:
                raise ValueError("bound needs to be valid")
            for sync_datetime in synchronisation_method.dates_range(from_date, to_date, filter_daily=True):
                synchronisation_method.synchronize(
                    self, sync_datetime.date(), override_execution_datetime_validity=True
                )
        if instrument:
            price_computation_method = None
            try:
                price_computation_method = Product.objects.get(id=instrument.id).price_computation
            except Product.DoesNotExist:
                with suppress(Index.DoesNotExist):
                    price_computation_method = Index.objects.get(id=instrument.id).price_computation
            if price_computation_method and instrument.prices.exists():
                if to_date <= from_date:
                    raise ValueError("bound needs to be valid")
                if not from_date:
                    from_date = instrument.prices.earliest("date").date
                if not to_date:
                    to_date = instrument.prices.latest("date").date
                # loop over every week day and trigger synchronization task in order
                for sync_datetime in price_computation_method.dates_range(from_date, to_date, filter_daily=True):
                    price_computation_method.compute(
                        instrument, sync_datetime.date(), override_execution_datetime_validity=True
                    )

    def update_preferred_classification_per_instrument(self):
        # Function to automatically assign Preferred instrument based on the assets' underlying instruments of the
        # attached wbportfolio
        instruments = filter(
            None,
            map(
                lambda x: Instrument.objects.get(id=x["underlying_instrument"]).get_classifable_ancestor(
                    include_self=True
                ),
                self.assets.values("underlying_instrument").distinct("underlying_instrument"),
            ),
        )
        leftovers_instruments = list(
            PortfolioInstrumentPreferredClassificationThroughModel.objects.filter(portfolio=self).values_list(
                "instrument", flat=True
            )
        )
        for instrument in instruments:
            other_classifications = instrument.classifications.filter(group__is_primary=False)
            default_classification = None
            if other_classifications.count() == 1:
                default_classification = other_classifications.first()
            if not PortfolioInstrumentPreferredClassificationThroughModel.objects.filter(
                portfolio=self, instrument=instrument
            ).exists():
                PortfolioInstrumentPreferredClassificationThroughModel.objects.create(
                    portfolio=self,
                    instrument=instrument,
                    classification=default_classification,
                    classification_group=default_classification.group if default_classification else None,
                )
            if instrument.id in leftovers_instruments:
                leftovers_instruments.remove(instrument.id)

        for instrument_id in leftovers_instruments:
            PortfolioInstrumentPreferredClassificationThroughModel.objects.filter(
                portfolio=self, instrument=instrument_id
            ).delete()

    @classmethod
    def get_endpoint_basename(cls):
        return "wbportfolio:portfolio"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbportfolio:portfoliorepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{name}}"

    @classmethod
    def _get_or_create_portfolio(cls, instrument_handler, portfolio_data):
        if isinstance(portfolio_data, int):
            return Portfolio.objects.get(id=portfolio_data)
        instrument = portfolio_data
        if isinstance(portfolio_data, dict):
            instrument = instrument_handler.process_object(instrument, only_security=False, read_only=True)[0]
        return instrument.primary_portfolio

    def check_share_diff(self, val_date: date) -> bool:
        return self.assets.filter(Q(date=val_date) & ~Q(initial_shares=F("initial_shares_at_custodian"))).exists()

    @classmethod
    def get_contribution_df(
        cls,
        qs,
        need_normalize=False,
        groupby_label_id="underlying_security",
        groubpy_label_title="underlying_instrument__name_repr",
        currency_fx_rate_label="currency_fx_rate",
        hedged_currency=None,
    ):
        # qs = AssetPosition.annotate_underlying_instrument(qs)
        weight_label = "weighting" if not need_normalize else "total_value_fx_portfolio"
        qs = qs.annotate(
            is_hedged=Case(
                When(
                    underlying_instrument__currency__isnull=False,
                    underlying_instrument__currency=hedged_currency,
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            coalesce_currency_fx_rate=Case(
                When(is_hedged=True, then=Value(Decimal(1.0))),
                default=F(currency_fx_rate_label),
                output_field=models.BooleanField(),
            ),
        ).select_related("underlying_instrument")
        df = pd.DataFrame(
            qs.values(
                "date",
                "price",
                "coalesce_currency_fx_rate",
                groupby_label_id,
                groubpy_label_title,
                weight_label,
            ),
            columns=[
                "date",
                "price",
                "coalesce_currency_fx_rate",
                groupby_label_id,
                groubpy_label_title,
                weight_label,
            ],
        )
        if not df.empty:
            df = df[df[weight_label] != 0]
            df.date = pd.to_datetime(df.date)
            df["price_fx_portfolio"] = df.price * df.coalesce_currency_fx_rate

            df[["price", "price_fx_portfolio", weight_label, "coalesce_currency_fx_rate"]] = df[
                ["price", "price_fx_portfolio", weight_label, "coalesce_currency_fx_rate"]
            ].astype("float")

            df[groupby_label_id] = df[groupby_label_id].fillna(0)
            df[groubpy_label_title] = df[groubpy_label_title].fillna("N/A")
            df_static = df[[groupby_label_id, groubpy_label_title]].groupby(groupby_label_id, dropna=False).first()

            df = (
                df[
                    [
                        groupby_label_id,
                        "date",
                        "price",
                        "price_fx_portfolio",
                        weight_label,
                        "coalesce_currency_fx_rate",
                    ]
                ]
                .groupby(["date", groupby_label_id], dropna=False)
                .agg(
                    {
                        "price": "mean",
                        "price_fx_portfolio": "mean",
                        weight_label: "sum",
                        "coalesce_currency_fx_rate": "mean",
                    }
                )
                .reset_index()
                .set_index("date")
                .sort_index()
            )
            df[weight_label] = df[weight_label].fillna(0)
            value = df.pivot_table(
                index="date",
                columns=[groupby_label_id],
                values=weight_label,
                fill_value=0,
                aggfunc="sum",
            )
            weights_ = value
            if need_normalize:
                total_value_price = df[weight_label].groupby("date", dropna=False).sum()
                weights_ = value.divide(total_value_price, axis=0)
            prices_usd = (
                df.pivot_table(
                    index="date",
                    columns=[groupby_label_id],
                    values="price_fx_portfolio",
                    aggfunc="mean",
                )
                .replace(0, np.nan)
                .bfill()
            )

            rates_fx = (
                df.pivot_table(
                    index="date",
                    columns=[groupby_label_id],
                    values="coalesce_currency_fx_rate",
                    aggfunc="mean",
                )
                .replace(0, np.nan)
                .bfill()
            )

            prices_usd = prices_usd.ffill()
            performance_prices = prices_usd / prices_usd.shift(1, axis=0) - 1
            contributions_prices = performance_prices.multiply(weights_.shift(1, axis=0)).dropna(how="all")
            total_contrib_prices = (1 + contributions_prices.sum(axis=1)).shift(1, fill_value=1.0).cumprod()
            contributions_prices = contributions_prices.multiply(total_contrib_prices, axis=0).sum(skipna=False)
            monthly_perf_prices = (1 + performance_prices).dropna(how="all").product(axis=0, skipna=False) - 1

            rates_fx = rates_fx.ffill()
            performance_rates_fx = rates_fx / rates_fx.shift(1, axis=0) - 1
            contributions_rates_fx = performance_rates_fx.multiply(weights_.shift(1, axis=0)).dropna(how="all")
            total_contrib_rates_fx = (1 + contributions_rates_fx.sum(axis=1)).shift(1, fill_value=1.0).cumprod()
            contributions_rates_fx = contributions_rates_fx.multiply(total_contrib_rates_fx, axis=0).sum(skipna=False)
            monthly_perf_rates_fx = (1 + performance_rates_fx).dropna(how="all").product(axis=0, skipna=False) - 1

            res = pd.concat(
                [
                    df_static,
                    monthly_perf_prices,
                    monthly_perf_rates_fx,
                    contributions_prices,
                    contributions_rates_fx,
                    weights_.iloc[0, :],
                    weights_.iloc[-1, :],
                    value.iloc[0, :],
                    value.iloc[-1, :],
                ],
                axis=1,
            ).reset_index()
            res.columns = [
                groupby_label_id,
                groubpy_label_title,
                "performance_total",
                "performance_forex",
                "contribution_total",
                "contribution_forex",
                "allocation_start",
                "allocation_end",
                "total_value_start",
                "total_value_end",
            ]

            return res.replace([np.inf, -np.inf, np.nan], 0)
        return pd.DataFrame()


@receiver(post_save, sender="wbportfolio.Product")
@receiver(post_save, sender="wbportfolio.ProductGroup")
@receiver(post_save, sender="wbportfolio.Index")
def post_product_creation(sender, instance, created, raw, **kwargs):
    if not raw and (created or not InstrumentPortfolioThroughModel.objects.filter(instrument=instance).exists()):
        portfolio = Portfolio.objects.create(
            name=f"Portfolio: {instance.name}",
            currency=instance.currency,
            invested_timespan=DateRange(instance.inception_date if instance.inception_date else date.min, date.max),
        )
        InstrumentPortfolioThroughModel.objects.get_or_create(instrument=instance, defaults={"portfolio": portfolio})


@shared_task(queue="portfolio")
def resynchronize_history_as_task(portfolio_id: int, from_date: date, to_date: date, instrument_id: int | None = None):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    instrument = Instrument.objects.get(id=instrument_id) if instrument_id else None
    portfolio.resynchronize_history(from_date, to_date, instrument=instrument)


@shared_task(queue="portfolio")
def trigger_portfolio_change_as_task(portfolio_id, val_date, **kwargs):
    portfolio = Portfolio.all_objects.get(id=portfolio_id)
    portfolio.change_at_date(val_date, **kwargs)


@shared_task(queue="portfolio")
def propagate_or_update_portfolio_assets_as_task(portfolio_id, from_date, to_date, **kwargs):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    portfolio.propagate_or_update_assets(from_date, to_date, **kwargs)
