from datetime import date

import pandas as pd
from django.utils import timezone
from faker import Faker
from pandas.tseries.offsets import BusinessMonthEnd
from wbfdm.factories import (
    CashFactory,
    ClassificationFactory,
    ClassificationGroupFactory,
    EquityFactory,
    InstrumentFactory,
)
from wbportfolio.factories import (
    AssetPositionFactory,
    InstrumentPriceFactory,
    PortfolioFactory,
    PortfolioSynchronizationFactory,
    PriceComputationFactory,
    ProductFactory,
)
from wbportfolio.models import (
    InstrumentPortfolioThroughModel,
    PortfolioPortfolioThroughModel,
)

fake = Faker()


def setup_product(today):
    product = ProductFactory.create()
    product.related_instruments.add(InstrumentFactory.create())
    primary_group = ClassificationGroupFactory.create(is_primary=True, max_depth=3)
    classification_parent_1 = ClassificationFactory.create(group=primary_group)
    classification_parent_2 = ClassificationFactory.create(group=primary_group)

    i1 = EquityFactory.create(classifications=[classification_parent_1.children.first().children.first()])
    i2 = EquityFactory.create(classifications=[classification_parent_2.children.first().children.first()])
    i3 = CashFactory.create()
    for _d in pd.date_range(
        today - BusinessMonthEnd(1), today + BusinessMonthEnd(0), freq="B"
    ):  # Build a complete factsheet month
        _d = _d.date()
        InstrumentPriceFactory.create(instrument=product, date=_d)
        pos = [
            AssetPositionFactory.create(
                portfolio=product.portfolio,
                date=_d,
                underlying_instrument=i1,
                underlying_instrument_price=InstrumentPriceFactory.create(instrument=i1, date=_d, calculated=False),
            ),
            AssetPositionFactory.create(
                portfolio=product.portfolio,
                date=_d,
                underlying_instrument=i2,
                underlying_instrument_price=InstrumentPriceFactory.create(instrument=i2, date=_d, calculated=False),
            ),
            AssetPositionFactory.create(
                portfolio=product.portfolio,
                date=_d,
                underlying_instrument=i3,
                underlying_instrument_price=InstrumentPriceFactory.create(instrument=i3, date=_d, calculated=False),
            ),
        ]
        for p in pos:
            InstrumentPriceFactory.create(instrument=p.underlying_instrument, date=_d)
    return product


class ValidTodayProductSetupMixin:
    def setup_method(self, method=None):
        product = setup_product(timezone.now().date())
        self.product = product


class ValidTodayMultiThematicProductSetupMixin:
    def setup_method(self, method=None):
        today = date.today()
        main_product = ProductFactory.create(price_computation=PriceComputationFactory.create())
        main_product.related_instruments.add(InstrumentFactory.create())

        # Create two valid products that will span our portfolio
        product1 = setup_product(today)
        product2 = setup_product(today)

        # Create a computed portfolio (model to allow automatic sync), linked throught he primary portfolio with a Thematic relationship
        computed_portfolio = PortfolioFactory.create(
            portfolio_synchronization=PortfolioSynchronizationFactory.create(),
        )
        PortfolioPortfolioThroughModel.objects.create(
            portfolio=computed_portfolio, dependency_portfolio=main_product.primary_portfolio
        )

        InstrumentPortfolioThroughModel.objects.update_or_create(
            instrument=main_product, defaults={"portfolio": computed_portfolio}
        )

        # Loop through the date range and create an equally weighted portfolio of products and synchronize the computed portfolio and compute the estimate NAV
        for _d in pd.date_range(today - BusinessMonthEnd(1), today + BusinessMonthEnd(0), freq="B"):
            _d = _d.date()
            AssetPositionFactory.create(
                portfolio=main_product.primary_portfolio,
                underlying_instrument=product1,
                date=_d,
                weighting=0.5,
                initial_price=product1.prices.get(date=_d).net_value,
            )
            AssetPositionFactory.create(
                portfolio=main_product.primary_portfolio,
                underlying_instrument=product2,
                date=_d,
                weighting=0.5,
                initial_price=product2.prices.get(date=_d).net_value,
            )
            computed_portfolio.portfolio_synchronization.synchronize(
                computed_portfolio, _d, override_execution_datetime_validity=True
            )
            main_product.price_computation.compute(main_product, _d, override_execution_datetime_validity=True)
        main_product.prices.update(calculated=False)
        self.product = main_product
        self.theme_portfolio = main_product.primary_portfolio
