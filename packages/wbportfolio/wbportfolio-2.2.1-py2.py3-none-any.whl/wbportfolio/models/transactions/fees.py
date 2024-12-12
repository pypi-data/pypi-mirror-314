import importlib
from contextlib import suppress

from celery import shared_task
from django.db import models
from django.db.models import Exists, OuterRef, Q, QuerySet
from django.dispatch import receiver
from wbfdm.models.instruments.instrument_prices import InstrumentPrice
from wbportfolio.import_export.handlers.fees import FeesImportHandler
from wbportfolio.models.products import Product

from .transactions import Transaction


class ValidFeesQueryset(QuerySet):
    def filter_only_valid_fees(self) -> QuerySet:
        """
        Filter the queryset to remove duplicate in case calculated and non-calculated fees are present for the same date/product/type
        """
        return self.annotate(
            real_fees_exists=Exists(
                self.filter(
                    transaction_subtype=OuterRef("transaction_subtype"),
                    linked_product=OuterRef("linked_product"),
                    fee_date=OuterRef("fee_date"),
                    calculated=False,
                )
            )
        ).filter(Q(calculated=False) | (Q(real_fees_exists=False) & Q(calculated=True)))


class DefaultFeesManager(models.Manager):
    def get_queryset(self) -> ValidFeesQueryset:
        return ValidFeesQueryset(self.model)

    def filter_only_valid_fees(self) -> QuerySet:
        return self.get_queryset().filter_only_valid_fees()


class ValidFeesManager(DefaultFeesManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter_only_valid_fees()


class Fees(Transaction):
    import_export_handler_class = FeesImportHandler

    class Type(models.TextChoices):
        TRANSACTION = "TRANSACTION", "Transaction"
        PERFORMANCE_CRYSTALIZED = "PERFORMANCE_CRYSTALIZED", "Performance Crystalized"
        PERFORMANCE = "PERFORMANCE", "Performance"
        MANAGEMENT = "MANAGEMENT", "Management"
        ISSUER = "ISSUER", "Issuer"
        OTHER = "OTHER", "Other"

    transaction_subtype = models.CharField(
        max_length=255, verbose_name="Fees Type", choices=Type.choices, default=Type.MANAGEMENT
    )

    fee_date = models.DateField()  # needed for indexing
    calculated = models.BooleanField(
        default=True,
        help_text="A marker whether the fees were calculated or supplied.",
        verbose_name="Is calculated",
    )

    linked_product = models.ForeignKey(
        "wbportfolio.Product",
        related_name="transactionfees",
        on_delete=models.PROTECT,
        verbose_name="Product",
    )

    class Meta:
        verbose_name = "Fees"
        verbose_name_plural = "Fees"
        indexes = [
            models.Index(fields=["linked_product"]),
            models.Index(fields=["transaction_subtype", "linked_product", "fee_date", "calculated"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["linked_product", "fee_date", "transaction_subtype", "calculated"], name="unique_fees"
            ),
        ]

    objects = DefaultFeesManager()
    valid_objects = ValidFeesManager()

    def save(self, *args, **kwargs):
        self.fee_date = self.transaction_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_date:%d.%m.%Y} - {self.Type[self.transaction_subtype]}: {self.portfolio.name}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbportfolio:fees"


class FeeCalculation(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    import_path = models.CharField(max_length=512, verbose_name="Import Path", default="restbench.fees.default")

    @classmethod
    def compute_fee_from_price(cls, price):
        product = Product.objects.get(id=price.instrument.id)
        if (fee_calculation := product.fee_calculation) and (import_path := fee_calculation.import_path):
            calculation_module = importlib.import_module(import_path)
            for new_fees in calculation_module.fees_calculation(price.id):
                Fees.objects.update_or_create(
                    linked_product=new_fees.pop("linked_product"),
                    transaction_date=new_fees.pop("transaction_date"),
                    transaction_subtype=new_fees.pop("transaction_subtype"),
                    calculated=True,
                    defaults=new_fees,
                )

    def __str__(self) -> str:
        return self.name


@shared_task
def compute_fee_from_price_as_task(price_id):
    price = InstrumentPrice.objects.get(id=price_id)
    FeeCalculation.compute_fee_from_price(price)


@receiver(models.signals.post_save, sender="wbfdm.InstrumentPrice")
def update_or_create_fees_post(sender, instance, created, raw, **kwargs):
    """Gets or create the fees for a given price and updates them if necessary"""
    if not raw and created and not instance.calculated and instance.instrument:
        with suppress(Product.DoesNotExist):
            product = Product.objects.get(id=instance.instrument.id)
            if product.fee_calculation:
                compute_fee_from_price_as_task.delay(instance.id)


# @receiver(models.signals.pre_save, sender="wbportfolio.Fees")
# def check_uniqueness(sender, instance, raw, **kwargs):
#     if (
#         Fees.objects.exclude(id=instance.id)
#         .filter(
#             transaction_date=instance.transaction_date,
#             transaction_subtype=instance.transaction_subtype,
#             linked_product=instance.linked_product,
#         )
#         .exists()
#     ):
#         raise ValueError(
#             f"A fees object already exists with date, type and product = {instance.transaction_date}, {instance.transaction_subtype}, {instance.linked_product}"
#         )
