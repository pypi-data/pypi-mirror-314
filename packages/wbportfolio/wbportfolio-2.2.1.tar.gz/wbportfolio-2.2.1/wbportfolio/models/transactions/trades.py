from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal

from celery import shared_task
from django.contrib import admin
from django.db import models
from django.db.models import (
    Case,
    DateField,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
    When,
)
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django_fsm import GET_STATE, FSMField, transition
from ordered_model.models import OrderedModel, OrderedModelManager
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton
from wbcore.models import WBModel
from wbcore.signals.models import pre_collection
from wbfdm.models.instruments.instrument_prices import InstrumentPrice
from wbportfolio.import_export.handlers.trade import TradeImportHandler
from wbportfolio.models.asset import AssetPosition
from wbportfolio.models.custodians import Custodian
from wbportfolio.models.roles import PortfolioRole
from wbportfolio.pms.typing import Trade as TradeDTO

from .transactions import ShareMixin, Transaction


class DefaultTradeManager(OrderedModelManager):
    """This manager is expect to be the trade default manager and annotate by default the effective weight (extracted
    from the associated portfolio) and the target weight as an addition between the effective weight and the delta weight
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                last_effective_date=Subquery(
                    AssetPosition.objects.filter(
                        underlying_instrument=OuterRef("underlying_instrument"),
                        date__lt=OuterRef("transaction_date"),
                        portfolio=OuterRef("portfolio"),
                    )
                    .order_by("-date")
                    .values("date")[:1]
                ),
                effective_weight=Coalesce(
                    Subquery(
                        AssetPosition.objects.filter(
                            underlying_instrument=OuterRef("underlying_instrument"),
                            date=OuterRef("last_effective_date"),
                            portfolio=OuterRef("portfolio"),
                        )
                        .values("portfolio")
                        .annotate(s=Sum("weighting"))
                        .values("s")[:1]
                    ),
                    Decimal(0),
                ),
                target_weight=F("effective_weight") + F("weighting"),
                effective_shares=Coalesce(
                    Subquery(
                        AssetPosition.objects.filter(
                            underlying_instrument=OuterRef("underlying_instrument"),
                            date=OuterRef("last_effective_date"),
                            portfolio=OuterRef("portfolio"),
                        )
                        .values("portfolio")
                        .annotate(s=Sum("shares"))
                        .values("s")[:1]
                    ),
                    Decimal(0),
                ),
                target_shares=F("effective_weight") * F("weighting"),
                diff_shares=F("shares") - F("claimed_shares"),
            )
        )


class ValidCustomerTradeManager(DefaultTradeManager):
    def __init__(self, without_internal_trade: bool = False):
        self.without_internal_trade = without_internal_trade
        super().__init__()

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .filter(
                transaction_subtype__in=[Trade.Type.SUBSCRIPTION, Trade.Type.REDEMPTION],
                marked_for_deletion=False,
                pending=False,
            )
        )
        if self.without_internal_trade:
            qs = qs.exclude(marked_as_internal=True)
        return qs


class Trade(ShareMixin, Transaction, OrderedModel, WBModel):
    import_export_handler_class = TradeImportHandler

    TRADE_WINDOW_INTERVAL = 7

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMIT = "SUBMIT", "Submit"
        EXECUTED = "EXECUTED", "Executed"
        CONFIRMED = "CONFIRMED", "Confirmed"
        FAILED = "FAILED", "Failed"

    class Type(models.TextChoices):
        REBALANCE = "REBALANCE", "Rebalance"
        DECREASE = "DECREASE", "Decrease"
        INCREASE = "INCREASE", "Increase"
        SUBSCRIPTION = "SUBSCRIPTION", "Subscription"
        REDEMPTION = "REDEMPTION", "Redemption"
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    external_identifier2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="A second external identifier that was supplied.",
        verbose_name="External Identifier 2",
    )

    transaction_subtype = models.CharField(
        max_length=32, default=Type.BUY, choices=Type.choices, verbose_name="Trade Type"
    )
    status = FSMField(default=Status.CONFIRMED, choices=Status.choices, verbose_name="Status")
    weighting = models.DecimalField(
        max_digits=16,
        decimal_places=6,
        default=Decimal(0),
        help_text="The weight to be multiplied against the target",
        verbose_name="Weight",
    )
    bank = models.CharField(
        max_length=255,
        help_text="The bank/counterparty/custodian the trade went through.",
        verbose_name="Counterparty",
    )
    custodian = models.ForeignKey(
        "wbportfolio.Custodian", null=True, blank=True, on_delete=models.SET_NULL, related_name="trades"
    )
    marked_for_deletion = models.BooleanField(
        default=False,
        help_text="If this is checked, then the trade is supposed to be deleted.",
        verbose_name="To be deleted",
    )

    # Only valid for subscription and redemption trade
    marked_as_internal = models.BooleanField(
        default=False,
        help_text="If this is checked, then this subscription or redemption is considered internal and will not be considered in any AUM computation",
        verbose_name="Internal",
    )
    internal_trade = models.OneToOneField(
        "wbportfolio.Trade",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="internal_subscription_redemption_trade",
    )

    pending = models.BooleanField(default=False)
    exclude_from_history = models.BooleanField(default=False)
    register = models.ForeignKey(
        to="wbportfolio.Register",
        null=True,
        blank=True,
        related_name="trades",
        on_delete=models.PROTECT,
    )

    trade_proposal = models.ForeignKey(
        to="wbportfolio.TradeProposal",
        null=True,
        blank=True,
        related_name="trades",
        on_delete=models.CASCADE,
        help_text="The Trade Proposal this trade is coming from",
    )
    claimed_shares = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=Decimal(0),
        help_text="The number of shares that were claimed.",
        verbose_name="Claimed Shares",
    )
    objects = DefaultTradeManager()
    valid_customer_trade_objects = ValidCustomerTradeManager()
    valid_external_customer_trade_objects = ValidCustomerTradeManager(without_internal_trade=True)

    @transition(
        field=status,
        source=Status.DRAFT,
        target=Status.SUBMIT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.SEND.icon,
                key="submit",
                label="Submit",
                action_label="Submit",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def submit(self, by=None, description=None, **kwargs):
        pass

    def can_submit(self):
        pass

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.FAILED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
    )
    def fail(self, **kwargs):
        pass

    @cached_property
    def underlying_instrument_price(self) -> InstrumentPrice | None:
        try:
            return self.underlying_instrument.valuations.get(date=self.transaction_date)
        except InstrumentPrice.DoesNotExist:
            return None

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=GET_STATE(
            lambda self, **kwargs: (
                self.Status.EXECUTED if self.underlying_instrument_price is not None else self.Status.FAILED
            ),
            states=[Status.EXECUTED, Status.FAILED],
        ),
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.CONFIRM.icon,
                key="execute",
                label="Execute",
                action_label="Execute",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
        on_error="FAILED",
    )
    def execute(self, **kwargs):
        if self.underlying_instrument_price:
            asset, created = AssetPosition.unannotated_objects.update_or_create(
                underlying_instrument=self.underlying_instrument,
                portfolio=self.portfolio,
                date=self.transaction_date,
                is_estimated=False,
                defaults={
                    "initial_currency_fx_rate": self.currency_fx_rate,
                    "weighting": self._target_weight,
                    "initial_price": self.underlying_instrument_price.net_value,
                    "initial_shares": None,
                    "underlying_instrument_price": self.underlying_instrument_price,
                    "asset_valuation_date": self.transaction_date,
                    "currency": self.currency,
                },
            )
            asset.set_weighting(self._target_weight)
        else:
            self.comment = f"Trade failed because no price is found for {self.underlying_instrument.computed_str} on {self.transaction_date:%Y-%m-%d}"

    def can_execute(self):
        if not self.portfolio.is_manageable:
            return {"portfolio": "The portfolio needs to be a model portfolio in order to execute this trade manually"}

    @transition(
        field=status,
        source=Status.EXECUTED,
        target=Status.CONFIRMED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.CONFIRM.icon,
                key="confirm",
                label="Confirm",
                action_label="Confirme",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def confirm(self, by=None, description=None, **kwargs):
        pass

    def can_confirm(self):
        pass

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.UNDO.icon,
                key="backtodraft",
                label="Back to Draft",
                action_label="backtodraft",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def backtodraft(self, **kwargs):
        pass

    @transition(
        field=status,
        source=Status.EXECUTED,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.UNDO.icon,
                key="reverte",
                label="Revert",
                action_label="revert",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def revert(self, to_date=None, **kwargs):
        with suppress(AssetPosition.DoesNotExist):
            asset = AssetPosition.objects.get(
                underlying_instrument=self.underlying_instrument,
                portfolio=self.portfolio,
                date=self.transaction_date,
                is_estimated=False,
            )
            asset.set_weighting(asset.weighting - self.weighting)

    @property
    def product(self):
        from wbportfolio.models.products import Product

        try:
            return Product.objects.get(id=self.underlying_instrument.id)
        except Product.DoesNotExist:
            return None

    @cached_property
    @admin.display(description="Last Effective Date")
    def _last_effective_date(self) -> date:
        if hasattr(self, "last_effective_date"):
            return self.last_effective_date
        elif (
            assets := AssetPosition.objects.filter(
                underlying_instrument=self.underlying_instrument,
                date__lt=self.transaction_date,
                portfolio=self.portfolio,
            )
        ).exists():
            return assets.latest("date").date

    @cached_property
    @admin.display(description="Effective Weight")
    def _effective_weight(self) -> Decimal:
        return getattr(
            self,
            "effective_weight",
            AssetPosition.objects.filter(
                underlying_instrument=self.underlying_instrument,
                date=self._last_effective_date,
                portfolio=self.portfolio,
            ).aggregate(s=Sum("weighting"))["s"]
            or Decimal(0),
        )

    @cached_property
    @admin.display(description="Effective Shares")
    def _effective_shares(self) -> Decimal:
        return getattr(
            self,
            "effective_shares",
            AssetPosition.objects.filter(
                underlying_instrument=self.underlying_instrument,
                date=self.transaction_date,
                portfolio=self.portfolio,
            ).aggregate(s=Sum("shares"))["s"]
            or Decimal(0),
        )

    @cached_property
    @admin.display(description="Target Weight")
    def _target_weight(self) -> Decimal:
        return getattr(self, "target_weight", self._effective_weight + self.weighting)

    @cached_property
    @admin.display(description="Target Shares")
    def _target_shares(self) -> Decimal:
        return getattr(self, "target_shares", self._effective_shares * self.weighting)

    @cached_property
    @admin.display(description="Diff Claims")
    def _diff_shares(self) -> Decimal:
        if hasattr(self, "diff_shares"):
            return self.diff_shares
        return self.shares - self.claimed_shares

    order_with_respect_to = "trade_proposal"

    class Meta(OrderedModel.Meta):
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
        constraints = [
            models.CheckConstraint(
                check=models.Q(marked_as_internal=False)
                | (
                    models.Q(marked_as_internal=True)
                    & models.Q(transaction_subtype__in=["REDEMPTION", "SUBSCRIPTION"])
                ),
                name="marked_as_internal_only_for_subred",
            ),
            models.CheckConstraint(
                check=models.Q(internal_trade__isnull=True)
                | (
                    models.Q(internal_trade__isnull=False)
                    & models.Q(transaction_subtype__in=["REDEMPTION", "SUBSCRIPTION"])
                ),
                name="internal_trade_set_only_for_subred",
            ),
        ]
        # notification_email_template = "portfolio/email/trade_notification.html"

    def save(self, *args, **kwargs):
        if not self.custodian and self.bank:
            self.custodian = Custodian.get_by_mapping(self.bank)
        if self.price is None:
            # we try to get the price if not provided directly from the underlying instrument
            with suppress(InstrumentPrice.DoesNotExist):
                self.price = self.underlying_instrument.valuations.get(date=self.transaction_date).net_value
        if self.price is not None and self.price_gross is None:
            self.price_gross = self.price

        if self.price is not None and self.shares is not None and self.total_value is None:
            self.total_value = self.price * self.shares

        if self.price_gross is not None and self.shares is not None and self.total_value_gross is None:
            self.total_value_gross = self.price_gross * self.shares

        if self.trade_proposal:
            self.portfolio = self.trade_proposal.portfolio
            self.transaction_date = self.trade_proposal.trade_date
            if effective_shares := self._effective_shares:
                self.shares = effective_shares * self.weighting
        self.transaction_type = Transaction.Type.TRADE

        if self.transaction_subtype is None:
            # if subtype not provided, we extract it automatically from the existing data.
            if self.underlying_instrument.instrument_type.key == "product":
                if self.shares is not None:
                    if self.shares > 0:
                        self.transaction_subtype = Trade.Type.SUBSCRIPTION
                    elif self.shares < 0:
                        self.transaction_subtype = Trade.Type.REDEMPTION
            elif self.weighting is not None:
                if self.weighting > 0:
                    self.transaction_subtype = Trade.Type.BUY
                elif self.weighting < 0:
                    self.transaction_subtype = Trade.Type.SELL
            else:
                self.transaction_subtype = Trade.Type.REBALANCE
        if self.id and hasattr(self, "claims"):
            self.claimed_shares = self.trade.claims.filter(status="APPROVED").aggregate(s=Sum("shares"))[
                "s"
            ] or Decimal(0)
        if self.trade_proposal and self.trade_proposal.status == "DRAFT":
            self.status = self.Status.DRAFT
        if self.internal_trade:
            self.marked_as_internal = True
        super().save(*args, **kwargs)

    def get_transaction_subtype(self) -> str:
        """
        Return the expected transaction subtype based n

        """

    def delete(self, **kwargs):
        pre_collection.send(sender=self.__class__, instance=self)
        super().delete(**kwargs)

    def __str__(self):
        ticker = f"{self.underlying_instrument.ticker}:" if self.underlying_instrument.ticker else ""
        return f"{ticker}{self.shares} ({self.bank})"

    def _build_dto(self) -> TradeDTO:
        """
        Data Transfer Object
        Returns:
            DTO trade object
        """
        return TradeDTO(
            id=self.id,
            underlying_instrument=self.underlying_instrument.id,
            effective_weight=self._effective_weight,
            target_weight=self._target_weight,
            instrument_type=self.underlying_instrument.security_instrument_type,
            currency=self.underlying_instrument.currency,
            date=self.transaction_date,
        )

    def get_alternative_valid_trades(self, share_delta: float = 0):
        return Trade.objects.filter(
            Q(underlying_instrument=self.underlying_instrument)
            & Q(portfolio=self.portfolio)
            & (
                Q(transaction_date__gte=self.transaction_date - timedelta(days=self.TRADE_WINDOW_INTERVAL))
                & Q(transaction_date__lte=self.transaction_date + timedelta(days=self.TRADE_WINDOW_INTERVAL))
            )
            & Q(transaction_subtype=self.transaction_subtype)
            & Q(shares__gte=self.shares * Decimal(1 - share_delta))
            & Q(shares__lte=self.shares * Decimal(1 + share_delta))
            & Q(marked_for_deletion=False)
            & Q(claims__isnull=True)
            & Q(pending=False)
        ).exclude(id=self.id)

    @property
    def is_claimable(self) -> bool:
        return self.is_customer_trade and not self.marked_for_deletion and not self.pending

    @property
    def is_customer_trade(self) -> bool:
        return self.transaction_subtype in [Trade.Type.REDEMPTION.name, Trade.Type.SUBSCRIPTION.name]

    @classmethod
    def subquery_shares_per_underlying_instrument(
        cls, val_date, underlying_instrument_name="pk", only_customer_trade=True
    ):
        """Returns a Subquery that returns the shares at a certain price date
        or 0

        Arguments:
            val_date {datetime.date} -- The  date that is used to determine which tradesare filtered

        Keyword Arguments:
            underlying_instrument_name {str} -- The reference to the underlying_instrument pk of the outer query (default: {"pk"})

        Returns:
            django.db.models.Subquery -- Subquery containing the sum of shares of each underlying_instrument
        """

        qs = cls.valid_customer_trade_objects
        if not only_customer_trade:
            qs = cls.objects
        qs = qs.filter(
            underlying_instrument=OuterRef(underlying_instrument_name),
            transaction_date__lt=val_date,
        )
        return Coalesce(
            Subquery(
                qs.values("underlying_instrument").annotate(sum_shares=Sum("shares")).values("sum_shares")[:1],
                output_field=models.DecimalField(),
            ),
            Decimal(0),
        )

    def link_to_internal_trade(self):
        qs = Trade.objects.filter(
            Q(underlying_instrument__instrument_type__key="product")
            & Q(shares=self.shares)
            & Q(underlying_instrument=self.underlying_instrument)
            & Q(transaction_date__gte=self.transaction_date - timedelta(days=self.TRADE_WINDOW_INTERVAL))
            & Q(transaction_date__lte=self.transaction_date + timedelta(days=self.TRADE_WINDOW_INTERVAL))
        ).exclude(id=self.id)
        if self.transaction_subtype in [Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION]:
            qs = qs.exclude(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])
            if qs.count() == 1:
                self.internal_trade = qs.first()
                self.save()
        else:
            qs = qs.filter(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])
            if qs.count() == 1:
                trade = qs.first()
                trade.internal_trade = self
                trade.save()

    @classmethod
    def subquery_net_money(
        cls, date_gte=None, date_lte=None, underlying_instrument_name="pk", only_positive=False, only_negative=False
    ):
        """Return a subquery which computes the net negative/positive money per underlying_instrument

        Arguments:
            val_date1 {datetime.date} -- The start date, including
            val_date2 {datetime.date} -- The end date, including

        Keyword Arguments:
            underlying_instrument_name {str} -- The reference to the underlying_instrument pk from the outer query (default: {"pk"})

        Returns:
            django.db.models.Subquery -- The subquery containing the net negative money per underlying_instrument
        """
        qs = cls.valid_external_customer_trade_objects.annotate(
            date_considered=ExpressionWrapper(F("transaction_date") + 1, output_field=DateField())
        )

        if date_gte:
            qs = qs.filter(date_considered__gte=date_gte)
        if date_lte:
            qs = qs.filter(date_considered__lte=date_lte)

        if only_positive:
            qs = qs.filter(shares__gt=0)
        elif only_negative:
            qs = qs.filter(shares__lt=0)
        return Coalesce(
            Subquery(
                qs.filter(underlying_instrument=OuterRef(underlying_instrument_name))
                .annotate(
                    _price=Case(
                        When(
                            price__isnull=True,
                            then=InstrumentPrice.subquery_closest_value(
                                "net_value",
                                date_name="date_considered",
                                instrument_pk_name="underlying_instrument__pk",
                            ),
                        ),
                        default=F("price"),
                    ),
                    net_value=ExpressionWrapper(F("shares") * F("_price"), output_field=models.FloatField()),
                )
                .values("underlying_instrument")
                .annotate(sum_net_value=Sum(F("net_value")))
                .values("sum_net_value"),
                output_field=models.FloatField(),
            ),
            0.0,
        )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbportfolio:trade"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbportfolio:traderepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{|:-}}{{transaction_date}}{{|::}}{{bank}}{{|-:}} {{claimed_shares}} / {{shares}} (∆ {{diff_shares}})"


@shared_task
def align_custodian():
    unaligned_qs = Trade.objects.annotate(
        proper_custodian_id=Subquery(Custodian.objects.filter(mapping__contains=OuterRef("bank")).values("id")[:1])
    ).exclude(custodian__id=F("proper_custodian_id"))

    unaligned_qs.update(custodian__id=F("proper_custodian_id"))


@receiver(post_save, sender="wbportfolio.Claim")
def compute_claimed_shares_on_claim_save(sender, instance, created, raw, **kwargs):
    if not raw and instance.trade:
        instance.trade.save()
