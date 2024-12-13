import random

import factory
from wbportfolio.models import Trade, TradeProposal

from .transactions import TransactionFactory


class TradeFactory(TransactionFactory):
    class Meta:
        model = Trade

    bank = factory.Faker("company")
    marked_for_deletion = False
    shares = factory.Faker("pydecimal", min_value=10, max_value=1000, right_digits=4)
    price = factory.LazyAttribute(lambda o: random.randint(10, 10000))
    # trade_proposal = factory.SubFactory("wbportfolio.factories.TradeProposalFactory")


class TradeProposalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TradeProposal

    trade_date = factory.Faker("date_object")
    comment = factory.Faker("paragraph")
    portfolio = factory.SubFactory("wbportfolio.factories.PortfolioFactory")
    creator = factory.SubFactory("wbcore.contrib.directory.factories.PersonFactory")


class CustomerTradeFactory(TradeFactory):
    transaction_subtype = factory.LazyAttribute(
        lambda o: Trade.Type.REDEMPTION if o.shares < 0 else Trade.Type.SUBSCRIPTION
    )
    underlying_instrument = factory.SubFactory("wbportfolio.factories.ProductFactory")
    portfolio = factory.LazyAttribute(lambda x: x.underlying_instrument.primary_portfolio)
