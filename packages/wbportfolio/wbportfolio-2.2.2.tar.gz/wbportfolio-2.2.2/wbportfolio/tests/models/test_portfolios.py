from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.db.models import F, Sum
from django.forms.models import model_to_dict
from faker import Faker
from pandas.tseries.offsets import BDay
from psycopg.types.range import DateRange
from wbcore.contrib.geography.factories import CountryFactory
from wbportfolio.models import (
    AssetPosition,
    Portfolio,
    PortfolioInstrumentPreferredClassificationThroughModel,
    PortfolioSynchronization,
)
from wbportfolio.pms.typing import Portfolio as PortfolioDTO

from .test_synchronization import callback
from .utils import PortfolioTestMixin

fake = Faker()


@pytest.mark.django_db
class TestPortfolioModel(PortfolioTestMixin):
    def test_init(self, portfolio):
        assert portfolio.id is not None

    def test_str(self, portfolio):
        assert str(portfolio) == f"{portfolio.id:06} ({portfolio.name})"

    def test_get_assets(self, portfolio, product, cash, asset_position_factory):
        asset_position_factory.create_batch(4, portfolio=portfolio, underlying_instrument=product)
        asset_position_factory.create(portfolio=portfolio, underlying_instrument=cash)
        assert portfolio._get_assets().count() == 5
        assert portfolio._get_assets(with_cash=False).count() == 4

    def test_get_earliest_asset_position_date(self, portfolio, asset_position_factory):
        asset_position_factory.create_batch(5, portfolio=portfolio)
        assert portfolio.get_earliest_asset_position_date() == AssetPosition.objects.earliest("date").date

    def test_get_latest_asset_position_date(self, portfolio, asset_position_factory):
        asset_position_factory.create_batch(5, portfolio=portfolio)
        assert portfolio.get_latest_asset_position_date() == AssetPosition.objects.latest("date").date

    def test_get_holding(self, portfolio_factory, asset_position_factory, equity, weekday):
        portfolio = portfolio_factory.create()
        asset_position_factory.create(portfolio=portfolio, date=weekday, initial_price=1, initial_shares=10)
        a2 = asset_position_factory.create(
            portfolio=portfolio,
            date=weekday,
            initial_price=1,
            initial_shares=40,
            underlying_instrument=equity,
            portfolio_created=portfolio_factory.create(),
        )
        asset_position_factory.create(portfolio=portfolio, date=weekday, initial_price=1, initial_shares=50)
        a4 = asset_position_factory.create(
            portfolio=portfolio,
            date=weekday,
            initial_price=1,
            initial_shares=30,
            underlying_instrument=equity,
            portfolio_created=portfolio_factory.create(),
        )
        assert (
            portfolio.get_holding(weekday)
            .filter(underlying_instrument=equity)
            .values_list("total_value_fx_portfolio", flat=True)[0]
            == a2._total_value_fx_portfolio + a4._total_value_fx_portfolio
        )

    def test_get_groupeby(self, portfolio, asset_position_factory, weekday):
        a1 = asset_position_factory.create(
            portfolio=portfolio, date=weekday, initial_price=1, initial_shares=10, weighting=0.1
        )
        asset_position_factory.create(
            portfolio=portfolio, date=weekday, initial_price=1, initial_shares=40, weighting=0.4
        )
        asset_position_factory.create(
            portfolio=portfolio, date=weekday, initial_price=1, initial_shares=50, weighting=0.5
        )

        def groupby(qs, **kwargs):
            return qs.annotate(aggregated_title=F("underlying_instrument__ticker"))

        df = portfolio._get_groupedby_df(groupby, weekday)
        assert df.aggregated_title[2] == a1.underlying_instrument.ticker

    def test_get_geographical_breakdown(self, portfolio, asset_position_factory, equity_factory, weekday):
        c1 = CountryFactory.create()
        c2 = CountryFactory.create()
        asset_position_factory.create(
            portfolio=portfolio, underlying_instrument=equity_factory.create(country=c1), date=weekday
        )
        asset_position_factory.create(
            portfolio=portfolio, underlying_instrument=equity_factory.create(country=c1), date=weekday
        )
        asset_position_factory.create(
            portfolio=portfolio, underlying_instrument=equity_factory.create(country=c2), date=weekday
        )
        assert portfolio.get_geographical_breakdown(weekday).shape[0] == 2

    def test_get_currency_exposure(self, portfolio, asset_position_factory, currency_factory, equity_factory, weekday):
        a1 = asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=equity_factory.create(),
            currency=currency_factory.create(),
            date=weekday,
        )
        asset_position_factory.create(
            portfolio=portfolio, underlying_instrument=equity_factory.create(), currency=a1.currency, date=weekday
        )
        asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=equity_factory.create(),
            currency=currency_factory.create(),
            date=weekday,
        )
        assert portfolio.get_currency_exposure(weekday).shape[0] == 2

    def test_get_equity_market_cap_distribution(
        self, portfolio, equity, asset_position_factory, instrument_price_factory
    ):
        price = instrument_price_factory.create(instrument=equity)
        asset_position_factory.create_batch(10, portfolio=portfolio, date=price.date, underlying_instrument=equity)

        assert not portfolio.get_equity_market_cap_distribution(price.date).empty

    def test_get_get_equity_liquidity(self, portfolio, asset_position_factory, equity_factory, weekday):
        asset_position_factory.create_batch(
            10, portfolio=portfolio, date=weekday, underlying_instrument=equity_factory.create()
        )
        assert not portfolio.get_equity_liquidity(weekday).empty

    def test_get_industry_exposure(
        self, portfolio, asset_position_factory, weekday, classification_group, classification_factory, equity_factory
    ):
        parent_classification = classification_factory.create(group=classification_group)
        asset_position_factory.create_batch(
            10,
            portfolio=portfolio,
            date=weekday,
            underlying_instrument=equity_factory.create(
                classifications=[
                    classification_factory.create(group=classification_group, parent=parent_classification)
                ]
            ),
        )
        assert not portfolio.get_industry_exposure(weekday).empty

    def test_get_asset_allocation(self, portfolio, equity, cash, index_factory, asset_position_factory, weekday):
        index = index_factory.create(is_cash=True)
        asset_position_factory.create_batch(10, portfolio=portfolio, date=weekday, underlying_instrument=equity)
        asset_position_factory.create(portfolio=portfolio, date=weekday, underlying_instrument=index)
        asset_position_factory.create(portfolio=portfolio, date=weekday, underlying_instrument=cash)
        assert portfolio.get_asset_allocation(weekday).shape[0] == 2

    def test_get_portfolio_contribution_df(self, portfolio, asset_position_factory, instrument_factory, weekday):
        i1 = instrument_factory.create()
        i2 = instrument_factory.create()
        end = (weekday + BDay(1)).date()
        asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i1,
            date=weekday,
            initial_price=100,
            initial_shares=10,
            initial_currency_fx_rate=1,
            weighting=0.25,
        )
        asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i2,
            date=weekday,
            initial_price=100,
            initial_shares=30,
            initial_currency_fx_rate=1,
            weighting=0.75,
        )
        asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i1,
            date=end,
            initial_price=120,
            initial_shares=10,
            initial_currency_fx_rate=1,
            weighting=0.33,
        )
        asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i2,
            date=end,
            initial_price=80,
            initial_shares=30,
            initial_currency_fx_rate=1,
            weighting=0.66,
        )
        res = portfolio.get_portfolio_contribution_df(weekday, end)
        assert 0.05 == pytest.approx(res.contribution_total[0])
        assert -0.15 == pytest.approx(res.contribution_total[1])
        assert 0.2 == pytest.approx(res.performance_total[0])
        assert -0.2 == pytest.approx(res.performance_total[1])

    def test_get_longshort_distribution(
        self, asset_position_factory, portfolio_factory, cash, index_factory, equity_factory, weekday
    ):
        portfolio = portfolio_factory.create()

        ind1 = index_factory.create(is_cash=False)
        short_underlying_portfolio = ind1.portfolio

        ind2 = index_factory.create(is_cash=False)
        long_underlying_portfolio = ind2.portfolio

        asset_position_factory.create(date=weekday, portfolio=portfolio, weighting=-1.0, underlying_instrument=ind1)
        short_p1 = asset_position_factory.create(
            date=weekday, portfolio=short_underlying_portfolio, underlying_instrument=cash
        )
        short_p2 = asset_position_factory.create(
            date=weekday,
            portfolio=short_underlying_portfolio,
            underlying_instrument=equity_factory.create(is_cash=False),
            weighting=1 - short_p1.weighting,
        )

        asset_position_factory.create(date=weekday, portfolio=portfolio, weighting=1.0, underlying_instrument=ind2)
        long_p1 = asset_position_factory.create(
            date=weekday,
            portfolio=long_underlying_portfolio,
            underlying_instrument=equity_factory.create(is_cash=False),
        )
        long_p2 = asset_position_factory.create(
            date=weekday,
            portfolio=long_underlying_portfolio,
            underlying_instrument=equity_factory.create(is_cash=False),
            weighting=1 - long_p1.weighting,
        )

        res = portfolio.get_longshort_distribution(weekday)
        total_weight = abs(short_p2.weighting) + long_p1.weighting + long_p2.weighting
        assert Decimal(res.weighting[0]) == pytest.approx(
            (long_p1.weighting + long_p2.weighting) / total_weight, rel=Decimal(1e-4)
        )
        assert Decimal(res.weighting[1]) == pytest.approx((abs(short_p2.weighting)) / total_weight, rel=Decimal(1e-4))

    def test_change_at_date(self, asset_position_factory, portfolio, weekday):
        asset_position_factory.create_batch(10, portfolio=portfolio, date=weekday)

        portfolio.change_at_date(weekday)
        total_value = AssetPosition.objects.aggregate(s=Sum("total_value_fx_portfolio"))["s"]
        for pos in AssetPosition.objects.all():
            assert float(pos.weighting) == pytest.approx(float(pos.total_value_fx_portfolio / total_value), rel=1e-2)

    @patch.object(PortfolioSynchronization, "synchronize_as_task_si")
    def test_change_at_date_with_dependent_portfolio(
        self, mock_synchronize, asset_position_factory, portfolio_factory, portfolio_synchronization, weekday
    ):
        mock_synchronize.return_value = callback
        base_portfolio = portfolio_factory.create()
        asset_position_factory.create_batch(10, portfolio=base_portfolio, date=weekday)

        dependent_portfolio1 = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        dependent_portfolio2 = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio1, date=weekday)
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio2, date=weekday)

        dependent_portfolio1.depends_on.add(base_portfolio)
        dependent_portfolio2.depends_on.add(base_portfolio)
        base_portfolio.change_at_date(weekday)

        assert mock_synchronize.call_count == 2

    @patch.object(PortfolioSynchronization, "synchronize_as_task_si")
    @pytest.mark.parametrize("portfolio_synchronization__propagate_history", [True])
    def test_change_at_date_with_dependent_portfolio_and_history(
        self, mock_synchronize, portfolio_synchronization, asset_position_factory, portfolio_factory, weekday
    ):
        mock_synchronize.return_value = callback
        base_portfolio = portfolio_factory.create()
        asset_position_factory.create_batch(10, portfolio=base_portfolio, date=weekday)

        dependent_portfolio1 = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        dependent_portfolio2 = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio1, date=weekday)
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio2, date=weekday)
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio1, date=weekday + BDay(6))
        asset_position_factory.create_batch(10, portfolio=dependent_portfolio2, date=weekday + BDay(6))
        total_nb_days = ((weekday + BDay(6)).date() - weekday).days
        dependent_portfolio1.depends_on.add(base_portfolio)
        dependent_portfolio2.depends_on.add(base_portfolio)
        base_portfolio.change_at_date(weekday)

        assert mock_synchronize.call_count == 2 * (total_nb_days + 1)

    def test_is_active_at_date(
        self,
        portfolio,
        instrument_factory,
    ):
        # a portfolio is active at a date if it is active or the deletion time is greater than that date AND if there is instruments attached, at least one instrument is still active as well

        assert portfolio.is_active
        assert portfolio.is_active_at_date(fake.date_object())

        portfolio.delete()  # soft deletion
        assert portfolio.is_active_at_date(fake.past_date())
        assert not portfolio.is_active_at_date(fake.future_date())

    def test_is_active_at_date_with_instruments(
        self,
        portfolio,
        instrument_factory,
    ):
        i1 = instrument_factory.create(inception_date=date.today(), delisted_date=None)
        i2 = instrument_factory.create(inception_date=date.today(), delisted_date=None)
        portfolio.instruments.add(i1)
        portfolio.instruments.add(i2)

        assert i1.is_active_at_date(fake.future_date())
        assert i2.is_active_at_date(fake.future_date())
        assert portfolio.is_active_at_date(fake.future_date())

        i1.delisted_date = date.today()
        i1.save()
        assert portfolio.is_active_at_date(fake.future_date())

        i2.delisted_date = date.today()
        i2.save()
        assert not portfolio.is_active_at_date(
            fake.date_object()
        )  # as no instrument is active, even if the portfolio is active at any date, the portfolio is consiodered inactive

    def test_propagate_or_update_assets(
        self, portfolio, asset_position_factory, instrument_factory, instrument_price_factory, weekday
    ):
        next_day = (weekday + BDay(1)).date()

        i1 = instrument_factory.create(currency=portfolio.currency)
        price1_1 = instrument_price_factory.create(instrument=i1, date=weekday)
        price1_2 = instrument_price_factory.create(instrument=i1, date=next_day)
        i2 = instrument_factory.create(currency=portfolio.currency)
        price2_1 = instrument_price_factory.create(instrument=i2, date=weekday)
        price2_2 = instrument_price_factory.create(instrument=i2, date=next_day)
        i3 = instrument_factory.create(currency=portfolio.currency)
        price3_1 = instrument_price_factory.create(instrument=i3, date=weekday)
        price3_2 = instrument_price_factory.create(instrument=i3, date=next_day)
        i4 = instrument_factory.create(currency=portfolio.currency)

        a1_1 = asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i1,
            underlying_instrument_price=price1_1,
            date=weekday,
            weighting=Decimal(0.4),
        )
        a2_1 = asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i2,
            underlying_instrument_price=price2_1,
            date=weekday,
            weighting=Decimal(0.3),
        )
        a3_1 = asset_position_factory.create(
            portfolio=portfolio,
            underlying_instrument=i3,
            underlying_instrument_price=price3_1,
            date=weekday,
            weighting=Decimal(0.2),
        )
        a4_1 = asset_position_factory.create(  # noqa
            portfolio=portfolio,
            underlying_instrument=i4,
            underlying_instrument_price=None,  # the price won't be created automatically by the fixture, we expect this position to be removed from the propagated portfolio
            date=weekday,
            weighting=Decimal(0.1),
        )

        # Test basic output
        portfolio.propagate_or_update_assets(weekday, next_day, delete_existing_assets=False)
        a1_2 = AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i1)
        a2_2 = AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i2)
        a3_2 = AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i3)
        with pytest.raises(AssetPosition.DoesNotExist):
            AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i4)

        assert a1_2.initial_price == pytest.approx(price1_2.net_value, rel=Decimal(1e-4))
        assert a2_2.initial_price == pytest.approx(price2_2.net_value, rel=Decimal(1e-4))
        assert a3_2.initial_price == pytest.approx(price3_2.net_value, rel=Decimal(1e-4))

        contrib_1 = a1_1.weighting * price1_2.net_value / price1_1.net_value
        contrib_2 = a2_1.weighting * price2_2.net_value / price2_1.net_value
        contrib_3 = a3_1.weighting * price3_2.net_value / price3_1.net_value
        assert a1_2.weighting == pytest.approx(contrib_1 / (contrib_1 + contrib_2 + contrib_3), rel=Decimal(1e4))
        assert a2_2.weighting == pytest.approx(contrib_2 / (contrib_1 + contrib_2 + contrib_3), rel=Decimal(1e4))
        assert a3_2.weighting == pytest.approx(contrib_3 / (contrib_1 + contrib_2 + contrib_3), rel=Decimal(1e4))

        # Test if a deleted assets is kept if delete_existing_assets is set to True
        a1_1.delete()
        portfolio.propagate_or_update_assets(weekday, next_day, delete_existing_assets=True)
        with pytest.raises(AssetPosition.DoesNotExist):
            a1_2.refresh_from_db()

        a2_2 = AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i2)
        a3_2 = AssetPosition.objects.get(portfolio=portfolio, date=next_day, underlying_instrument=i3)
        assert a2_2
        assert a3_2

        # Test that we don't do anything on target portfolio because there is a non estimated position
        a2_2.is_estimated = False
        a2_2.save()
        portfolio.propagate_or_update_assets(weekday, next_day)
        a2_2_weighting = a2_2.weighting
        a3_2_weighting = a3_2.weighting
        a2_2.refresh_from_db()
        a3_2.refresh_from_db()

        assert a2_2.weighting == a2_2_weighting
        assert a3_2.weighting == a3_2_weighting

    def test_propagate_or_update_assets_active_states(
        self, weekday, active_product, asset_position_factory, instrument
    ):
        next_day = (weekday + BDay(1)).date()

        portfolio = active_product.portfolio

        a1 = asset_position_factory.create(
            portfolio=portfolio, date=weekday, underlying_instrument=instrument, currency=instrument.currency
        )
        asset_position_factory.create(
            portfolio=portfolio,
            date=next_day,
            underlying_instrument=instrument,
            currency=instrument.currency,
            exchange=a1.exchange,
            portfolio_created=a1.portfolio_created,
        )
        active_product.delisted_date = weekday
        active_product.save()
        # Test1: test if unactive portfolio keep having the to date assets. (asset found at next day are suppose to be deleted when the portfolio is non active at the from date)
        portfolio.propagate_or_update_assets(weekday, next_day)
        assert portfolio.assets.filter(date=next_day).exists() is False

        # Activate product
        active_product.delisted_date = None
        active_product.save()

        # Expect proper creation
        portfolio.propagate_or_update_assets(weekday, next_day)
        a_future = AssetPosition.objects.get(portfolio=portfolio, date=next_day)

        # Test if only estimated update existing pos,

        portfolio.propagate_or_update_assets(weekday, next_day)
        initial_shares = a1.initial_shares

        # Test that estimated shares keep being updated
        a1.initial_shares *= 2
        a1.save()
        portfolio.propagate_or_update_assets(weekday, next_day)
        a_future.refresh_from_db()
        assert a_future.initial_shares == initial_shares * 2

        # Test that non-estimated shares are not being updated
        updated_fields = ["initial_currency_fx_rate", "weighting", "initial_price", "initial_shares"]
        for field in updated_fields:
            setattr(a1, field, getattr(a1, field) * 2)
        a1.save()
        a_future_copy = model_to_dict(a_future)
        a_future.is_estimated = False
        a_future.save()
        portfolio.propagate_or_update_assets(weekday, next_day)
        a_future.refresh_from_db()
        for field in updated_fields:
            assert getattr(a_future, field) == a_future_copy[field]

        # Test active (from) portfolio but not active (to) create a zero weight position
        active_product.delisted_date = next_day
        active_product.save()

        a_future.is_estimated = True
        a_future.save()
        portfolio.propagate_or_update_assets(weekday, next_day)
        a_future.refresh_from_db()
        assert a_future.weighting == 0

    @patch.object(PortfolioSynchronization, "synchronize")
    @pytest.mark.parametrize("timedelta_days", [fake.pyint(min_value=1, max_value=10)])
    def test_resynchronize_history(
        self, mock_fct, portfolio, asset_position_factory, weekday, timedelta_days, portfolio_synchronization
    ):
        portfolio.portfolio_synchronization = portfolio_synchronization
        portfolio.save()
        asset_position_factory.create(portfolio=portfolio, date=weekday)
        portfolio.resynchronize_history(weekday, (weekday + BDay(timedelta_days)).date())
        mock_fct.call_count == timedelta_days
        with pytest.raises(ValueError):
            portfolio.resynchronize_history((weekday + BDay(timedelta_days)).date(), weekday)

    def test_update_preferred_classification_per_instrument(
        self, portfolio, asset_position_factory, equity_factory, classification_factory, classification_group_factory
    ):
        primary_group = classification_group_factory.create(is_primary=True)
        other_group = classification_group_factory.create(is_primary=False)
        c1 = classification_factory.create(group=other_group)
        c2_primary = classification_factory.create(group=primary_group)
        c2_secondary = classification_factory.create(group=other_group)
        c3_1 = classification_factory.create(group=other_group)
        c3_2 = classification_factory.create(group=other_group)

        # One classification to this instrument, we expect the relationship to be filled automatically
        i1 = equity_factory.create(classifications=[c1])
        # One classification "Primary" and one "other" to this instrument, we expect the relationship to be filled automatically
        i2 = equity_factory.create(classifications=[c2_secondary, c2_primary])
        # Two non-primary classifications to this instrument, we expect the relationship to not be filled with the classification automatically (created though)
        i3 = equity_factory.create(classifications=[c3_2, c3_1])
        asset_position_factory.create(portfolio=portfolio, underlying_instrument=i1)
        a2 = asset_position_factory.create(portfolio=portfolio, underlying_instrument=i2)
        a3 = asset_position_factory.create(portfolio=portfolio, underlying_instrument=i3)

        assert not portfolio.preferred_instrument_classifications.exists()
        portfolio.update_preferred_classification_per_instrument()
        res1 = PortfolioInstrumentPreferredClassificationThroughModel.objects.get(
            portfolio=portfolio, classification=c1, instrument=i1, classification_group=other_group
        )
        res2 = PortfolioInstrumentPreferredClassificationThroughModel.objects.get(
            portfolio=portfolio, classification=c2_secondary, instrument=i2, classification_group=other_group
        )
        res3 = PortfolioInstrumentPreferredClassificationThroughModel.objects.get(
            portfolio=portfolio, classification=None, instrument=i3, classification_group=None
        )

        assert not PortfolioInstrumentPreferredClassificationThroughModel.objects.exclude(
            id__in=[res1.id, res2.id, res3.id]
        ).exists()

        # We delete portfolio positions and retrigger the function to check that the leftovers relationship are indeed removed
        a3.delete()
        a2.delete()
        portfolio.update_preferred_classification_per_instrument()
        with pytest.raises(PortfolioInstrumentPreferredClassificationThroughModel.DoesNotExist):
            res3.refresh_from_db()
        with pytest.raises(PortfolioInstrumentPreferredClassificationThroughModel.DoesNotExist):
            res2.refresh_from_db()
        res1.refresh_from_db()
        assert res1

    def test_import_positions_at_date(self, portfolio_factory, asset_position_factory, instrument_factory, weekday):
        def _serialize(obj):
            return {
                "portfolio": obj.portfolio.id,
                "portfolio_created": obj.portfolio_created.id if obj.portfolio_created else None,
                "underlying_instrument": obj.underlying_instrument.id,
                "date": obj.date,
                "currency": obj.currency.id,
                "weighting": obj.weighting,
                "initial_currency_fx_rate": obj.initial_currency_fx_rate,
                "initial_shares": obj.initial_shares,
                "initial_price": obj.initial_price,
                "is_estimated": obj.is_estimated,
                "exchange": obj.exchange.id if obj.exchange else None,
                "asset_valuation_date": obj.asset_valuation_date,
            }

        portfolio = portfolio_factory.create()

        i1 = instrument_factory.create()
        i2 = instrument_factory.create()
        a1 = asset_position_factory.build(
            portfolio=portfolio, date=weekday, underlying_instrument=i1, currency=i1.currency, weighting=0.5
        )
        a2 = asset_position_factory.build(
            portfolio=portfolio, date=weekday, underlying_instrument=i2, currency=i2.currency, weighting=0.25
        )
        a3 = asset_position_factory.build(
            portfolio=portfolio,
            currency=i2.currency,
            underlying_instrument=i2,
            initial_price=a2.initial_price,
            date=weekday,
            weighting=0.25,
        )

        portfolio.import_positions_at_date(
            PortfolioDTO([a1._build_dto(), a2._build_dto(), a3._build_dto()]),
            weekday,
        )

        res1 = AssetPosition.objects.get(portfolio=portfolio, date=weekday, underlying_instrument=i1)
        res2 = AssetPosition.objects.get(portfolio=portfolio, date=weekday, underlying_instrument=i2)

        assert portfolio.assets.filter(date=weekday).count() == 2

        assert res1.initial_shares == a1.initial_shares
        assert res1.weighting == a1.weighting / (a1.weighting + a2.weighting + a3.weighting)
        assert res1.initial_currency_fx_rate == a1.initial_currency_fx_rate
        assert res1.initial_price == a1.initial_price

        assert res2.initial_shares == a2.initial_shares + a3.initial_shares
        assert res2.weighting == a2.weighting + a3.weighting
        assert res2.initial_currency_fx_rate == (a2.initial_currency_fx_rate + a3.initial_currency_fx_rate) / 2
        assert res2.initial_price == (a2.initial_price + a3.initial_price) / 2

        assert portfolio.assets.filter(date=weekday, underlying_instrument=a2.underlying_instrument).count() == 1
        assert not portfolio.assets.filter(
            date=weekday, underlying_instrument=a2.underlying_instrument, initial_shares=a3.initial_shares
        ).exists()

        portfolio.import_positions_at_date(
            PortfolioDTO([a1._build_dto()]),
            weekday,
        )
        res1.refresh_from_db()
        with pytest.raises(AssetPosition.DoesNotExist):
            res2.refresh_from_db()

    def test_get_total_value(
        self, portfolio, customer_trade_factory, instrument_factory, instrument_price_factory, weekday
    ):
        i1 = instrument_factory.create()
        i2 = instrument_factory.create()
        previous_day = (weekday - BDay(5)).date()
        price11 = instrument_price_factory.create(instrument=i1, date=weekday, calculated=False)
        price12 = instrument_price_factory.create(instrument=i1, date=previous_day, calculated=False)
        price2 = instrument_price_factory.create(instrument=i2, date=weekday, calculated=False)

        # "noise" trades
        pending_customer_trade_i1 = customer_trade_factory.create(  # noqa
            portfolio=portfolio, transaction_date=weekday, underlying_instrument=i1, pending=True
        )
        marked_for_deletion_customer_trade_i1 = customer_trade_factory.create(  # noqa
            portfolio=portfolio, transaction_date=weekday, underlying_instrument=i1, marked_for_deletion=True
        )

        # valid trade for two different instrument but within the same portfolio
        trade_11 = customer_trade_factory.create(
            portfolio=portfolio, transaction_date=weekday, underlying_instrument=i1
        )
        trade_12 = customer_trade_factory.create(
            portfolio=portfolio, transaction_date=previous_day, underlying_instrument=i1
        )
        trade_2 = customer_trade_factory.create(
            portfolio=portfolio, transaction_date=weekday, underlying_instrument=i2
        )

        assert (
            portfolio.get_total_value(weekday)
            == price11.net_value * (trade_11.shares + trade_12.shares) + price2.net_value * trade_2.shares
        )
        assert portfolio.get_total_value(previous_day) == price12.net_value * trade_12.shares
        assert portfolio.get_total_value(previous_day - BDay(1)) == Decimal(0)

    def test_tracked_object(self, portfolio, asset_position_factory):
        assert not Portfolio.tracked_objects.exists()

        asset_position_factory.create(portfolio=portfolio)
        assert set(Portfolio.tracked_objects.all()) == {
            portfolio,
        }

        portfolio.is_tracked = False
        portfolio.save()
        assert not Portfolio.tracked_objects.exists()

    def test_is_invested_at_date(self, portfolio_factory):
        portfolio = portfolio_factory.create(invested_timespan=DateRange(date(2024, 1, 2), date(2024, 1, 3)))
        assert portfolio.is_invested_at_date(date(2024, 1, 1)) is False
        assert portfolio.is_invested_at_date(date(2024, 1, 2)) is True
        assert portfolio.is_invested_at_date(date(2024, 1, 3)) is False

        assert set(Portfolio.objects.filter_invested_at_date(date(2024, 1, 1))) == set()
        assert set(Portfolio.objects.filter_invested_at_date(date(2024, 1, 2))) == {portfolio}
        assert set(Portfolio.objects.filter_invested_at_date(date(2024, 1, 1))) == set()
