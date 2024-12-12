from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import PropertyMock, patch

import pytest
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from faker import Faker
from pandas.tseries.offsets import BDay
from wbcore.contrib.currency.models import Currency
from wbportfolio.models import Trade
from wbportfolio.models.synchronization.portfolio_synchronization import (
    PortfolioSynchronization,
    synchronize_portfolio_as_task,
)
from wbportfolio.models.synchronization.price_computation import (
    PriceComputation,
    compute_price_as_task,
)
from wbportfolio.pms.typing import Position as PositionDTO

from .utils import PortfolioTestMixin

fake = Faker()


@shared_task()
def callback(*args, **kwargs):
    return True


@pytest.mark.django_db
class TestSynchronizationTaskModel(PortfolioTestMixin):
    def test_init(self, synchronization_task):
        assert synchronization_task.id is not None

    def test_args(self, synchronization_task):
        content_type = ContentType.objects.get_for_model(synchronization_task)
        assert (
            synchronization_task.args
            == f'["{synchronization_task.id}", "{content_type.app_label}", "{content_type.model}"]'
        )

    def test_import_method(self, synchronization_task):
        with pytest.raises(NotImplementedError):
            method = synchronization_task._import_method
            method()

    def test_import_method_with_custom_callback(self, synchronization_task_factory):
        synchronization_task = synchronization_task_factory.create(
            import_path="wbportfolio.tests.models.test_synchronization"
        )
        callback_si_task = callback.si().task.replace("modules.wbportfolio.", "")
        test_callback_si_task = synchronization_task._import_method.si().task.replace("modules.wbportfolio.", "")
        assert callback_si_task == test_callback_si_task

    def test_tasks_signature(self, synchronization_task):
        with pytest.raises(NotImplementedError):
            synchronization_task._tasks_signature()

    def test_default_callback(self, synchronization_task):
        with pytest.raises(NotImplementedError):
            synchronization_task._default_callback()

    def test_end_task_signature(self, synchronization_task):
        assert synchronization_task._end_task_signature() is None

    def test_end_task_signature_with_signature(self, synchronization_task_factory, periodic_task_factory):
        dependent_task = synchronization_task_factory.create(
            task="wbportfolio.tests.models.test_synchronization.callback"
        )

        synchronization_task = synchronization_task_factory.create()
        synchronization_task.dependent_task = dependent_task
        synchronization_task.save()

        assert (
            synchronization_task._end_task_signature().task
            == "wbportfolio.models.synchronization.synchronization.task"
        )


@pytest.mark.django_db
class TestPortfolioSynchronization(PortfolioTestMixin):
    def test_init(self, portfolio_synchronization):
        assert portfolio_synchronization.id is not None

    @patch.object(PortfolioSynchronization, "_import_method", new_callable=PropertyMock)
    @patch.object(PortfolioSynchronization, "is_valid_date")
    def test_synchronize_automatic_approval(
        self,
        mock_is_valid_date,
        mock_import_method,
        portfolio_synchronization,
        portfolio_factory,
        asset_position_factory,
        equity_factory,
        currency_factory,
        trade_factory,
        instrument_portfolio_through_model_factory,
        active_product,
        weekday,
    ):
        portfolio = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        instrument_portfolio_through_model_factory.create(instrument=active_product, portfolio=portfolio)
        trade_factory.create(
            underlying_instrument=active_product,
            transaction_date=weekday,
            transaction_subtype=Trade.Type.SUBSCRIPTION,
            shares=100,
        )

        portfolio.save()

        def callback(*args, **kwargs):
            for i in range(10):
                position = asset_position_factory.build(
                    underlying_instrument=equity_factory.create(), currency=currency_factory.create()
                )
                yield None, PositionDTO(
                    underlying_instrument=position.underlying_instrument.id,
                    instrument_type=position.underlying_instrument.instrument_type,
                    date=weekday,
                    asset_valuation_date=weekday,
                    currency=position.currency.id,
                    price=position.initial_price,
                    shares=position.initial_shares,
                    currency_fx_rate=position.initial_currency_fx_rate,
                    weighting=position.weighting,
                    is_estimated=position.is_estimated,
                )

        mock_import_method.return_value = callback
        mock_is_valid_date.return_value = True
        portfolio_synchronization.synchronize(portfolio, weekday, override_execution_datetime_validity=True)
        assert portfolio.assets.count() == 10
        assert 1.0 == pytest.approx(float(portfolio.assets.aggregate(s=Sum("weighting"))["s"]), rel=1e-4)

    @patch.object(PortfolioSynchronization, "_import_method", new_callable=PropertyMock)
    @patch.object(PortfolioSynchronization, "is_valid_date")
    @patch.object(Currency, "convert")
    def test_synchronize_tradeprosal(
        self,
        mock_convert,
        mock_is_valid_date,
        mock_import_method,
        portfolio_synchronization_factory,
        portfolio_factory,
        asset_position_factory,
        equity_factory,
        currency_factory,
        active_product,
        weekday,
        trade_factory,
        instrument_portfolio_through_model_factory,
    ):
        portfolio_synchronization = portfolio_synchronization_factory(is_automatic_validation=False)

        portfolio = portfolio_factory.create()
        portfolio.portfolio_synchronization = portfolio_synchronization
        portfolio.save()

        instrument_portfolio_through_model_factory.create(instrument=active_product, portfolio=portfolio)
        trade_factory.create(
            underlying_instrument=active_product,
            transaction_date=weekday,
            transaction_subtype=Trade.Type.SUBSCRIPTION,
            shares=100,
        )

        def callback(*args, **kwargs):
            for i in range(10):
                position = asset_position_factory.build(
                    underlying_instrument=equity_factory.create(), currency=currency_factory.create()
                )
                position_dict = PositionDTO(
                    underlying_instrument=position.underlying_instrument.id,
                    instrument_type=position.underlying_instrument.instrument_type,
                    date=weekday,
                    asset_valuation_date=weekday,
                    currency=position.currency.id,
                    price=position.initial_price,
                    shares=position.initial_shares,
                    currency_fx_rate=position.initial_currency_fx_rate,
                    weighting=position.weighting,
                    is_estimated=position.is_estimated,
                )
                yield position_dict, position_dict

        mock_is_valid_date.return_value = True
        mock_import_method.return_value = callback
        mock_convert.return_value = Decimal(1.0)
        portfolio_synchronization.synchronize(portfolio, weekday, override_execution_datetime_validity=True)
        assert portfolio.trade_proposals.count() == 1
        assert portfolio.transactions.count() == 10

    def test_synchronize_as_task_si(self, portfolio_synchronization, portfolio, weekday):
        assert portfolio_synchronization.synchronize_as_task_si(
            portfolio, weekday
        ) == synchronize_portfolio_as_task.si(portfolio_synchronization.id, portfolio.id, weekday)

    def test_tasks_signature(
        self,
        portfolio_synchronization,
        portfolio_factory,
        weekday,
        trade_factory,
        product_factory,
        instrument_portfolio_through_model_factory,
    ):
        p1 = portfolio_factory.create()
        p1.portfolio_synchronization = portfolio_synchronization
        p1.save()
        product1 = product_factory.create(delisted_date=None, inception_date=weekday - timedelta(days=30))
        instrument_portfolio_through_model_factory.create(instrument=product1, portfolio=p1)
        trade_factory.create(
            underlying_instrument=product1,
            transaction_date=weekday,
            transaction_subtype=Trade.Type.SUBSCRIPTION,
            shares=100,
        )

        p2 = portfolio_factory.create()
        p2.portfolio_synchronization = portfolio_synchronization
        p2.save()
        product2 = product_factory.create(delisted_date=None, inception_date=weekday - timedelta(days=30))
        instrument_portfolio_through_model_factory.create(instrument=product2, portfolio=p2)
        trade_factory.create(
            underlying_instrument=product2,
            transaction_date=weekday,
            transaction_subtype=Trade.Type.SUBSCRIPTION,
            shares=100,
        )

        signatures = portfolio_synchronization._tasks_signature(sync_date=weekday)
        assert len(list(signatures)) == 2

    @patch.object(PortfolioSynchronization, "is_valid_date")
    def test_default_callback(
        self,
        mock_is_valid_date,
        active_product,
        weekday,
        portfolio_synchronization,
        portfolio_factory,
        index_factory,
        equity_factory,
        asset_position_factory,
        trade_factory,
        instrument_price_factory,
        instrument_portfolio_through_model_factory,
    ):
        while weekday.weekday() in [5, 6]:
            weekday += timedelta(days=1)
        mock_is_valid_date.return_value = True
        root_index = index_factory.create()
        root_index_portfolio = root_index.portfolio

        index1 = index_factory.create()
        index1_portfolio = index1.portfolio

        a1 = asset_position_factory.create(
            underlying_instrument=index1,
            portfolio=root_index_portfolio,
            weighting=0.6,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )

        index2 = index_factory.create()
        index2_portfolio = index2.portfolio

        a2 = asset_position_factory.create(
            underlying_instrument=index2,
            portfolio=root_index_portfolio,
            weighting=0.4,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )

        a1_1 = asset_position_factory.create(
            underlying_instrument=equity_factory.create(),
            portfolio=index1_portfolio,
            weighting=0.2,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )
        a2_1 = asset_position_factory.create(
            underlying_instrument=equity_factory.create(),
            portfolio=index1_portfolio,
            weighting=0.3,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )
        a3_1 = asset_position_factory.create(
            underlying_instrument=equity_factory.create(),
            portfolio=index1_portfolio,
            weighting=0.5,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )

        a1_2 = asset_position_factory.create(
            underlying_instrument=equity_factory.create(),
            portfolio=index2_portfolio,
            weighting=0.7,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )
        a2_2 = asset_position_factory.create(
            underlying_instrument=equity_factory.create(),
            portfolio=index2_portfolio,
            weighting=0.3,
            initial_shares=None,
            initial_price=100,
            date=weekday,
        )

        product_base_portfolio = active_product.primary_portfolio
        product_portfolio = portfolio_factory.create(portfolio_synchronization=portfolio_synchronization)
        instrument_portfolio_through_model_factory.create(instrument=active_product, portfolio=product_portfolio)
        trade_factory.create(
            underlying_instrument=active_product,
            transaction_date=weekday,
            transaction_subtype=Trade.Type.SUBSCRIPTION,
            shares=100,
        )

        product_portfolio.depends_on.add(root_index_portfolio)

        instrument_portfolio_through_model_factory.create(instrument=active_product, portfolio=product_portfolio)

        instrument_price_factory.create(instrument=active_product, date=weekday)
        trade_factory.create(
            underlying_instrument=active_product,
            portfolio=product_base_portfolio,
            transaction_date=weekday,
            shares=1000,
            transaction_subtype="SUBSCRIPTION",
        )

        portfolio_synchronization.synchronize(product_portfolio, weekday, override_execution_datetime_validity=True)
        assert product_portfolio.assets.filter(date=weekday).count() == 5
        assert float(a1_1.weighting) * float(a1.weighting) == pytest.approx(
            float(
                product_portfolio.assets.filter(
                    portfolio_created=index1_portfolio,
                    underlying_instrument=a1_1.underlying_instrument,
                    date=weekday,
                )
                .first()
                .weighting
            )
        )
        assert float(a2_1.weighting) * float(a1.weighting) == pytest.approx(
            float(
                product_portfolio.assets.filter(
                    portfolio_created=index1_portfolio,
                    underlying_instrument=a2_1.underlying_instrument,
                    date=weekday,
                )
                .first()
                .weighting
            )
        )
        assert float(a3_1.weighting) * float(a1.weighting) == pytest.approx(
            float(
                product_portfolio.assets.filter(
                    portfolio_created=index1_portfolio,
                    underlying_instrument=a3_1.underlying_instrument,
                    date=weekday,
                )
                .first()
                .weighting
            )
        )
        assert float(a1_2.weighting) * float(a2.weighting) == pytest.approx(
            float(
                product_portfolio.assets.filter(
                    portfolio_created=index2_portfolio,
                    underlying_instrument=a1_2.underlying_instrument,
                    date=weekday,
                )
                .first()
                .weighting
            )
        )
        assert float(a2_2.weighting) * float(a2.weighting) == pytest.approx(
            float(
                product_portfolio.assets.filter(
                    portfolio_created=index2_portfolio,
                    underlying_instrument=a2_2.underlying_instrument,
                    date=weekday,
                )
                .first()
                .weighting
            )
        )
        assert Decimal(1.0) == pytest.approx(product_portfolio.assets.aggregate(s=Sum("weighting"))["s"])

    @patch.object(PortfolioSynchronization, "synchronize")
    def test_synchronize_portfolio_as_task(self, mock_synchronize, portfolio_synchronization, portfolio, weekday):
        synchronize_portfolio_as_task(portfolio_synchronization.id, portfolio.id, weekday)
        assert mock_synchronize.call_count == 1


@pytest.mark.django_db
class TestPriceComputation(PortfolioTestMixin):
    def test_init(self, price_computation):
        assert price_computation.id is not None

    def test_compute_price_as_task_si(self, price_computation, instrument, weekday):
        assert price_computation.compute_price_as_task_si(instrument, weekday) == compute_price_as_task.si(
            price_computation.id, instrument.id, weekday
        )

    def test_tasks_signature_with_sync_date(self, price_computation, product_factory, weekday):
        i1 = product_factory.create(inception_date=weekday - BDay(1), delisted_date=None)
        i1.price_computation = price_computation
        i1.save()

        i2 = product_factory.create(inception_date=weekday - BDay(1), delisted_date=None)
        i2.price_computation = price_computation
        i2.save()

        i_inactive = product_factory.create(
            inception_date=weekday - BDay(1), delisted_date=weekday - timedelta(days=1)
        )
        i_inactive.price_computation = price_computation
        i_inactive.save()

        signatures = price_computation._tasks_signature(sync_date=weekday)

        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures)) == {
            (price_computation.id, i1.id, weekday),
            (price_computation.id, i2.id, weekday),
        }

    def test_tasks_signature_without_sync_date(self, price_computation, product_factory, instrument_price_factory):
        thursday = date(2023, 10, 19)
        friday = date(2023, 10, 20)
        saturday = date(2023, 10, 21)
        sunday = date(2023, 10, 22)
        monday = date(2023, 10, 23)
        tuesday = date(2023, 10, 24)
        product = product_factory.create(inception_date=thursday, delisted_date=None)
        product.price_computation = price_computation
        product.save()
        instrument_price_factory.create(date=thursday, instrument=product)

        signatures_friday = price_computation._tasks_signature(to_date=friday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures_friday)) == {
            (price_computation.id, product.id, thursday),
        }

        signatures_saturday = price_computation._tasks_signature(to_date=saturday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures_saturday)) == {
            (price_computation.id, product.id, thursday),
            (price_computation.id, product.id, friday),
        }

        signatures_sunday = price_computation._tasks_signature(to_date=sunday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures_sunday)) == {
            (price_computation.id, product.id, thursday),
            (price_computation.id, product.id, friday),
        }

        signatures_monday = price_computation._tasks_signature(to_date=monday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures_monday)) == {
            (price_computation.id, product.id, thursday),
            (price_computation.id, product.id, friday),
        }

        signatures_tuesday = price_computation._tasks_signature(to_date=tuesday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures_tuesday)) == {
            (price_computation.id, product.id, thursday),
            (price_computation.id, product.id, friday),
            (price_computation.id, product.id, monday),
        }
        instrument_price_factory.create(date=monday, instrument=product)
        signatures = price_computation._tasks_signature(to_date=tuesday)
        assert set(map(lambda x: (x.args[0], x.args[1], x.args[2]), signatures)) == {
            (price_computation.id, product.id, monday),
        }

    @patch.object(PriceComputation, "compute")
    def test_compute_price_as_task(self, mock_compute, price_computation, instrument, weekday):
        compute_price_as_task(price_computation.id, instrument.id, weekday)
        assert mock_compute.call_count == 1

    @patch.object(PriceComputation, "_import_method", new_callable=PropertyMock)
    def test_compute(
        self, mock_import_method, weekday, price_computation, instrument_factory, instrument_price_factory
    ):
        while weekday.weekday() in [5, 6]:
            weekday += timedelta(days=1)
        instrument = instrument_factory.create(inception_date=weekday - timedelta(days=1), delisted_date=None)
        instrument.price_computation = price_computation
        instrument.save()
        price = instrument_price_factory.build(instrument=instrument, date=weekday)

        def callback(*args, **kwargs):
            return {
                "instrument": instrument,
                "date": weekday,
                "gross_value": price.gross_value,
                "net_value": price.net_value,
            }

        mock_import_method.return_value = callback
        price_computation.compute(instrument, weekday, override_execution_datetime_validity=True)
        assert instrument.prices.count() == 1
        assert float(price.net_value) == pytest.approx(float(instrument.prices.first().net_value))

    def test_default_callback(
        self,
        weekday,
        price_computation,
        equity_factory,
        product_factory,
        asset_position_factory,
        instrument_price_factory,
        trade_factory,
    ):
        while weekday.weekday() in [5, 6]:
            weekday += timedelta(days=1)

        previous_sync_date = weekday - timedelta(days=1)
        while previous_sync_date.weekday() in [5, 6]:
            previous_sync_date -= timedelta(days=1)

        product = product_factory.create(
            price_computation=price_computation, inception_date=weekday - timedelta(days=1), delisted_date=None
        )
        portfolio = product.portfolio

        trade_factory.create(
            underlying_instrument=product,
            portfolio=portfolio,
            transaction_date=previous_sync_date,
            shares=1000,
            transaction_subtype="SUBSCRIPTION",
        )

        e1 = equity_factory.create()
        e2 = equity_factory.create()
        e3 = equity_factory.create()

        a1_1 = asset_position_factory.create(
            underlying_instrument=e1,
            portfolio=portfolio,
            date=previous_sync_date,
            weighting=Decimal(0.3),
            initial_price=Decimal(100),
            initial_shares=300,
        )
        a2_1 = asset_position_factory.create(
            underlying_instrument=e2,
            portfolio=portfolio,
            date=previous_sync_date,
            weighting=Decimal(0.5),
            initial_price=Decimal(100),
            initial_shares=500,
        )
        a3_1 = asset_position_factory.create(
            underlying_instrument=e3,
            portfolio=portfolio,
            date=previous_sync_date,
            weighting=Decimal(0.2),
            initial_price=Decimal(100),
            initial_shares=200,
        )

        a1_2 = asset_position_factory.create(
            underlying_instrument=e1,
            portfolio=portfolio,
            date=weekday,
            weighting=Decimal(0.3719),
            initial_price=Decimal(150),
            initial_shares=300,
        )
        a2_2 = asset_position_factory.create(
            underlying_instrument=e2,
            portfolio=portfolio,
            date=weekday,
            weighting=Decimal(0.4959),
            initial_price=Decimal(120),
            initial_shares=500,
        )
        a3_2 = asset_position_factory.create(
            underlying_instrument=e3,
            portfolio=portfolio,
            date=weekday,
            weighting=Decimal(0.1322),
            initial_price=Decimal(80),
            initial_shares=200,
        )

        price = instrument_price_factory.create(instrument=product, date=previous_sync_date, net_value=100)
        price_computation.compute(product, weekday, override_execution_datetime_validity=True)

        total_perf = (
            (a1_2._price / a1_1._price - 1) * a1_1.weighting
            + (a2_2._price / a2_1._price - 1) * a2_1.weighting
            + (a3_2._price / a3_1._price - 1) * a3_1.weighting
        )
        assert product.prices.count() == 2
        assert float(price.net_value * (Decimal(1.0) + total_perf)) == pytest.approx(
            float(product.prices.filter(date=weekday).first().net_value)
        )
