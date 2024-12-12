from decimal import Decimal

from django.apps import apps
from django.db import models
from django.dispatch import receiver
from wbcore.contrib.io.mixins import ImportMixin
from wbcore.signals import pre_merge
from wbfdm.models.instruments.instruments import Instrument
from wbfdm.signals import add_instrument_to_investable_universe


class ShareMixin(models.Model):
    shares = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="The number of shares that were traded.",
        verbose_name="Shares",
    )
    price = models.DecimalField(
        max_digits=16,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="The price per share.",
        verbose_name="Price",
    )

    price_gross = models.DecimalField(
        max_digits=16,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="The gross price per share.",
        verbose_name="Gross Price",
    )

    class Meta:
        abstract = True


class Transaction(ImportMixin, models.Model):
    class Type(models.TextChoices):
        # Standart Asset Types
        TRADE = "Trade", "Trade"
        DIVIDEND_TRANSACTION = "DividendTransaction", "Dividend Transaction"
        EXPIRY = "Expiry", "Expiry"
        FEES = "Fees", "Fees"

    transaction_type = models.CharField(max_length=255, verbose_name="Type", choices=Type.choices, default=Type.TRADE)

    portfolio = models.ForeignKey(
        "wbportfolio.Portfolio", related_name="transactions", on_delete=models.PROTECT, verbose_name="Portfolio"
    )

    underlying_instrument = models.ForeignKey(
        to="wbfdm.Instrument",
        related_name="transactions",
        limit_choices_to=models.Q(children__isnull=True),
        on_delete=models.PROTECT,
        verbose_name="Underlying Instrument",
        help_text="The instrument that is this transaction.",
    )

    transaction_date = models.DateField(
        verbose_name="Trade Date",
        help_text="The date that this transaction was traded.",
    )
    book_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Trade Date",
        help_text="The date that this transaction was booked.",
    )
    value_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Value Date",
        help_text="The date that this transaction was valuated.",
    )

    currency = models.ForeignKey(
        "currency.Currency",
        related_name="transactions",
        on_delete=models.PROTECT,
        verbose_name="Currency",
    )
    currency_fx_rate = models.DecimalField(
        max_digits=14, decimal_places=8, default=Decimal(1.0), verbose_name="FOREX rate"
    )
    total_value = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Total Value"
    )
    total_value_fx_portfolio = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Total Value Fx Portfolio"
    )
    total_value_gross = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Total Value Gross"
    )
    total_value_gross_fx_portfolio = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Total Value Gross Fx Portfolio"
    )
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="An external identifier that was supplied.",
        verbose_name="External Identifier",
    )
    comment = models.TextField(default="", verbose_name="Comment", blank=True)

    def save(self, *args, **kwargs):
        if not getattr(self, "currency", None) and self.underlying_instrument:
            self.currency = self.underlying_instrument.currency
        if not self.currency_fx_rate:
            self.currency_fx_rate = self.underlying_instrument.currency.convert(
                self.transaction_date, self.portfolio.currency, exact_lookup=True
            )
        if not self.transaction_type:
            self.transaction_type = self.__class__.__name__
        if not self.value_date:
            self.value_date = self.transaction_date
            # try:
            #     # we try to find the next valid date (i.e. the one with position on the underlying instrument"
            #     self.value_date = (
            #         self.underlying_instrument.valuations.filter(date__gt=self.transaction_date).earliest("date").date
            #     )
            # except ObjectDoesNotExist:
            #     self.value_date = (self.transaction_date + BDay(1)).date()
        if not self.book_date:
            self.book_date = self.transaction_date
        if (
            self.total_value is not None
            and self.currency_fx_rate is not None
            and self.total_value_fx_portfolio is None
        ):
            self.total_value_fx_portfolio = self.total_value * self.currency_fx_rate

        if self.total_value is not None and self.total_value_gross is None and self.total_value_gross is None:
            self.total_value_gross = self.total_value

        if (
            self.currency_fx_rate is not None
            and self.total_value_gross is not None
            and self.total_value_gross_fx_portfolio is None
        ):
            self.total_value_gross_fx_portfolio = self.total_value_gross * self.currency_fx_rate

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.total_value} - {self.transaction_date:%d.%m.%Y} : {str(self.underlying_instrument)} (in {str(self.portfolio)})"

    def get_casted_model(self):
        return apps.get_model(app_label="wbportfolio", model_name=self.transaction_type)

    def get_casted_transaction(self) -> models.Model:
        """
        Cast the asset into its child representative
        """
        model = self.get_casted_model()
        return model.objects.get(pk=self.pk)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["underlying_instrument", "transaction_date"]),
            # models.Index(fields=["date", "underlying_instrument"]),
        ]

    objects = models.Manager()

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{total_value}}{{transaction_date}}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbportfolio:transaction"


@receiver(pre_merge, sender="wbfdm.Instrument")
def pre_merge_instrument(sender: models.Model, merged_object: "Instrument", main_object: "Instrument", **kwargs):
    """
    Simply reassign the transactions linked to the merged instrument to the main instrument
    """
    merged_object.transactions.update(underlying_instrument=main_object)


@receiver(add_instrument_to_investable_universe, sender="wbfdm.Instrument")
def add_instrument_to_investable_universe_from_transactions(sender: models.Model, **kwargs) -> list[int]:
    """
    register all instrument linked to assets as within the investible universe
    """
    return list(
        (
            Instrument.objects.annotate(
                transaction_exists=models.Exists(
                    Transaction.objects.filter(underlying_instrument=models.OuterRef("pk"))
                )
            ).filter(transaction_exists=True)
        )
        .distinct()
        .values_list("id", flat=True)
    )
