import random
from datetime import timedelta

import factory
from wbportfolio.models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    currency_fx_rate = 1.0
    portfolio = factory.SubFactory("wbportfolio.factories.PortfolioFactory")
    underlying_instrument = factory.SubFactory("wbfdm.factories.InstrumentFactory")
    transaction_date = factory.Faker("date_object")
    value_date = factory.LazyAttribute(lambda o: o.transaction_date + timedelta(days=1))
    currency = factory.SubFactory("wbcore.contrib.currency.factories.CurrencyFactory")
    total_value = factory.LazyAttribute(lambda o: random.randint(1, 1000))
    total_value_fx_portfolio = factory.LazyAttribute(lambda o: o.currency_fx_rate * o.total_value)
    total_value_gross = factory.LazyAttribute(lambda o: random.randint(1, 1000))
    total_value_gross_fx_portfolio = factory.LazyAttribute(lambda o: o.currency_fx_rate * o.total_value_gross)
