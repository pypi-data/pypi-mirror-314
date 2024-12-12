import random
from decimal import Decimal

import pytest
from faker import Faker
from psycopg.types.range import NumericRange
from wbcompliance.factories.risk_management import RuleThresholdFactory
from wbportfolio.risk_management.backends.stop_loss_instrument import (
    RuleBackend as StopLossInstrumentRuleBackend,
)
from wbportfolio.tests.models.utils import PortfolioTestMixin

fake = Faker()


@pytest.mark.django_db
class TestStopLossPortfolioRuleModel(PortfolioTestMixin):
    @pytest.fixture
    def stop_loss_portfolio_backend(self, weekday, date_interval_option, freq, product):
        parameters = {"freq": freq, "date_interval_option": date_interval_option}
        lower = random.random()
        upper = random.uniform(lower, 1)
        return StopLossInstrumentRuleBackend(
            weekday,
            product,
            parameters,
            [RuleThresholdFactory.create(range=NumericRange(lower=lower, upper=upper))],  # type: ignore
        )

    @pytest.mark.parametrize(
        "date_interval_option, freq",
        [
            ("ROLLING_WINDOWS", StopLossInstrumentRuleBackend.FreqChoices.BUSINESS_DAY),
            *[("FREQUENCY", option) for option in StopLossInstrumentRuleBackend.FreqChoices.values],
        ],
    )
    def test_check_rule_frequency(
        self,
        weekday,
        date_interval_option,
        freq,
        product,
        portfolio,
        instrument_price_factory,
        asset_position_factory,
        stop_loss_portfolio_backend,
        instrument_portfolio_through_model_factory,
    ):
        instrument_portfolio_through_model_factory.create(
            instrument=product,
            portfolio=portfolio,
            primary_portfolio=True,
        )

        d1 = stop_loss_portfolio_backend._get_start_interval()

        threshold = stop_loss_portfolio_backend.thresholds[0]
        breach_perf = random.uniform(threshold.range.lower, threshold.range.upper)

        i1 = instrument_price_factory.create(date=d1, net_value=100, calculated=False, instrument=product)
        instrument_price_factory.create(
            date=weekday, net_value=Decimal(breach_perf + 1) * i1.net_value, calculated=False, instrument=product
        )

        asset_position_factory.create(date=weekday, underlying_instrument=product, portfolio=portfolio)
        asset_position_factory.create(date=weekday, underlying_instrument=product, portfolio=portfolio)

        res = list(stop_loss_portfolio_backend.check_rule())
        assert len(res) == 1
        assert res[0].breached_object.id == product.id

    @pytest.mark.parametrize(
        "date_interval_option, freq",
        [
            ("ROLLING_WINDOWS", StopLossInstrumentRuleBackend.FreqChoices.BUSINESS_DAY),
            *[("FREQUENCY", option) for option in StopLossInstrumentRuleBackend.FreqChoices.values],
        ],
    )
    def test_check_rule_frequency_2(
        self,
        weekday,
        date_interval_option,
        freq,
        product,
        portfolio,
        instrument_price_factory,
        asset_position_factory,
        instrument_factory,
        stop_loss_portfolio_backend,
        instrument_portfolio_through_model_factory,
    ):
        instrument_portfolio_through_model_factory.create(
            instrument=product,
            portfolio=portfolio,
            primary_portfolio=True,
        )
        d1 = stop_loss_portfolio_backend._get_start_interval()
        benchmark = instrument_factory.create()

        threshold = stop_loss_portfolio_backend.thresholds[0]
        threshold.range = NumericRange(upper=-0.5, lower=None)  # type: ignore
        threshold.save()

        instrument_price_factory.create(date=d1, net_value=100, calculated=False, instrument=product)
        instrument_price_factory.create(date=weekday, net_value=100, calculated=False, instrument=product)

        instrument_price_factory.create(date=d1, net_value=100, calculated=False, instrument=benchmark)
        instrument_price_factory.create(date=weekday, net_value=300, calculated=False, instrument=benchmark)

        asset_position_factory.create(date=weekday, underlying_instrument=product, portfolio=portfolio)
        asset_position_factory.create(date=weekday, underlying_instrument=product, portfolio=portfolio)

        res = list(stop_loss_portfolio_backend.check_rule())
        assert len(res) == 0

        setattr(stop_loss_portfolio_backend, "static_benchmark", benchmark)
        res = list(stop_loss_portfolio_backend.check_rule())
        assert len(res) == 1
        assert res[0].breached_object.id == product.id
