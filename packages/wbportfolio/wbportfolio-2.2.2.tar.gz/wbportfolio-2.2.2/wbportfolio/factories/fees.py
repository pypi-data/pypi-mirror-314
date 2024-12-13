import factory
from faker import Faker
from wbportfolio.models import Fees

from .transactions import TransactionFactory

faker = Faker()


class FeesFactory(TransactionFactory):
    class Meta:
        model = Fees

    transaction_subtype = factory.Faker("random_element", elements=[x[0] for x in Fees.Type.choices])
    linked_product = factory.SubFactory("wbportfolio.factories.ProductFactory")
