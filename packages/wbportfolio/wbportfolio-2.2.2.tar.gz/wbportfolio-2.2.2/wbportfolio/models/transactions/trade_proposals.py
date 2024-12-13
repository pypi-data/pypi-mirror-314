from contextlib import suppress
from datetime import timedelta
from typing import TypeVar

import pandas as pd
from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django_fsm import FSMField, transition
from pandas.tseries.offsets import BDay
from wbcompliance.models.risk_management.mixins import RiskCheckMixin
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton
from wbcore.models import WBModel
from wbfdm.models.instruments.instruments import Instrument
from wbportfolio.models.roles import PortfolioRole
from wbportfolio.pms.trading import TradingService
from wbportfolio.pms.typing import Portfolio as PortfolioDTO
from wbportfolio.pms.typing import TradeBatch as TradeBatchDTO

from .trades import Trade

SelfTradeProposal = TypeVar("SelfTradeProposal", bound="TradeProposal")


class TradeProposal(RiskCheckMixin, WBModel):
    trade_date = models.DateField(verbose_name="Trading Date")

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMIT = "SUBMIT", "Submit"
        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"

    comment = models.TextField(default="", verbose_name="Trade Comment", blank=True)
    status = FSMField(default=Status.DRAFT, choices=Status.choices, verbose_name="Status")
    model_portfolio = models.ForeignKey(
        "wbportfolio.Portfolio",
        blank=True,
        null=True,
        related_name="model_trade_proposals",
        on_delete=models.PROTECT,
        verbose_name="Model Portfolio",
    )
    portfolio = models.ForeignKey(
        "wbportfolio.Portfolio", related_name="trade_proposals", on_delete=models.PROTECT, verbose_name="Portfolio"
    )
    creator = models.ForeignKey(
        "directory.Person",
        blank=True,
        null=True,
        related_name="trade_proposals",
        on_delete=models.PROTECT,
        verbose_name="Owner",
    )

    def _get_checked_object_field_name(self) -> str:
        """
        Mandatory function from the Riskcheck mixin that returns the field (aka portfolio), representing the object to check the rules against.
        """
        return "portfolio"

    @cached_property
    def validated_trading_service(self) -> TradingService:
        """
        This property holds the validated trading services and cache it.This property expect to be set only if is_valid return True
        """
        return TradingService(
            self.trade_date,
            effective_portfolio=self.portfolio._build_dto(self.trade_date),
            trades_batch=self._build_dto(),
        )

    @property
    def previous_trade_proposal(self) -> SelfTradeProposal | None:
        future_proposals = TradeProposal.objects.filter(portfolio=self.portfolio).filter(
            trade_date__lt=self.trade_date, status=TradeProposal.Status.APPROVED
        )
        if future_proposals.exists():
            return future_proposals.latest("trade_date")
        return None

    @property
    def next_trade_proposal(self) -> SelfTradeProposal | None:
        future_proposals = TradeProposal.objects.filter(portfolio=self.portfolio).filter(
            trade_date__gt=self.trade_date, status=TradeProposal.Status.APPROVED
        )
        if future_proposals.exists():
            return future_proposals.earliest("trade_date")
        return None

    @cached_property
    def base_assets(self):
        """
        Return a dictionary representation (instrument_id: target weight) of this trade proposal
        Returns:
            A dictionary representation

        """
        return {
            v["underlying_instrument"]: v["target_weight"]
            for v in self.trades.filter(status=Trade.Status.EXECUTED).values("underlying_instrument", "target_weight")
        }

    def __str__(self) -> str:
        return f"{self.portfolio.name}: {self.trade_date} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.model_portfolio:
            self.model_portfolio = self.portfolio
        super().save(*args, **kwargs)

    def _build_dto(self) -> TradeBatchDTO:
        """
        Data Transfer Object
        Returns:
            DTO trade object
        """
        return (
            TradeBatchDTO(tuple([trade._build_dto() for trade in self.trades.all()])) if self.trades.exists() else None
        )

    # Start tools methods
    def clone(self, **kwargs) -> SelfTradeProposal:
        """
        Method to clone self as a new trade proposal. It will automatically shift the trade date if a proposal already exists
        Args:
            **kwargs: The keyword arguments
        Returns:
            The cloned trade proposal
        """
        trade_date = kwargs.get("trade_date", self.trade_date)

        # Find the next valid trade date
        while TradeProposal.objects.filter(portfolio=self.portfolio, trade_date=trade_date).exists():
            trade_date += timedelta(days=1)

        trade_proposal_clone = TradeProposal.objects.create(
            trade_date=trade_date,
            comment=kwargs.get("comment", self.comment),
            status=TradeProposal.Status.DRAFT,
            model_portfolio=self.model_portfolio,
            portfolio=self.portfolio,
            creator=self.creator,
        )

        # For all existing trades, copy them to the new trade proposal
        for trade in self.trades.all():
            trade.pk = None
            trade.trade_proposal = trade_proposal_clone
            trade.transaction_date = trade_proposal_clone.trade_date
            trade.save()
        return trade_proposal_clone

    def normalize_trades(self):
        """
        Call the trading service with the existing trades and normalize them in order to obtain a total sum target weight of 100%
        The existing trade will be modified directly with the given normalization factor
        """
        service = TradingService(self.trade_date, trades_batch=self._build_dto())
        service.normalize()
        leftovers_trades = self.trades.all()
        for _, trade in service.trades_batch.trades_map.items():
            with suppress(Trade.DoesNotExist):
                self.trades.update_or_create(
                    id=trade.id,
                    defaults={
                        "weighting": trade.delta_weight,
                        "shares": trade.target_shares,
                    },
                )
                leftovers_trades = leftovers_trades.exclude(id=trade.id)
        leftovers_trades.delete()

    def reset_trades(self):
        """
        Will delete all existing trades and recreate them from the method `create_or_update_trades`
        """
        # delete all existing trades
        self.trades.all().delete()
        # recreate them from scratch (if the portfolio has positions)
        self.create_or_update_trades()

    def apply_trades(self):
        # We validate trade which will create or update the initial asset positions
        self.trades.exclude(status=Trade.Status.SUBMIT).update(status=Trade.Status.SUBMIT)
        for trade in self.trades.all():
            trade.execute()
            trade.save()
        # We propagate the new portfolio composition until the next trade proposal or today if it doesn't exist yet
        to_date = self.next_trade_proposal.trade_date if self.next_trade_proposal else timezone.now().date()

        for from_date in pd.date_range(self.trade_date, to_date - timedelta(days=1), freq="B"):
            to_date = (from_date + BDay(1)).date()
            self.portfolio.propagate_or_update_assets(
                from_date.date(),
                to_date,
                forward_price=False,
                base_assets=self.base_assets,
                delete_existing_assets=True,
            )
            self.portfolio.change_at_date(to_date, base_assets=self.base_assets, force_recompute_weighting=True)

    def revert_trades(self):
        self.trades.exclude(status=Trade.Status.EXECUTED).update(status=Trade.Status.EXECUTED)
        for trade in self.trades.all():
            trade.revert()
            trade.save()
        if previous_trade_proposal := self.previous_trade_proposal:
            previous_trade_proposal.apply_trades()

    def create_or_update_trades(
        self, target_portfolio: PortfolioDTO = None, effective_portfolio: PortfolioDTO = None, reset: bool = False
    ):
        """
        This function talk to the trading service layer in order to generate a list of valid trades to attach to the proposal

        Args:
            target_portfolio: The target portfolio that the trades needs to execute to. Absence of position means a sell
            effective_portfolio: The current or effective portfolio to derivative effective weight from. Absence of position means a buy
            reset: If true, delete the current attached trades
        """
        # if the target portfolio is not provided, we try to build it
        if (
            not target_portfolio
            and (assets := self.model_portfolio.assets.filter(date__lte=self.trade_date)).exists()
            and (latest_pos := assets.latest("date"))
        ):
            target_portfolio = self.model_portfolio._build_dto(latest_pos.date)

        # if the effective portfolio is not provided, we try to build it
        if (
            not effective_portfolio
            and (assets := self.portfolio.assets.filter(date__lte=self.trade_date)).exists()
            and (latest_pos := assets.latest("date"))
        ):
            effective_portfolio = self.portfolio._build_dto(latest_pos.date)
        # Build trades DTO from the attached trades
        trade_batch = self._build_dto()
        if target_portfolio or effective_portfolio or trade_batch:
            service = TradingService(
                self.trade_date,
                effective_portfolio=effective_portfolio,
                target_portfolio=target_portfolio,
                trades_batch=trade_batch,
            )
            # with suppress(ValidationError):
            # Normalize the trades and validate it
            service.normalize()
            service.is_valid()
            if reset:
                self.trades.all().delete()
            for trade_dto in service.validated_trades:
                instrument = Instrument.objects.get(id=trade_dto.underlying_instrument)
                t, c = Trade.objects.update_or_create(
                    underlying_instrument=instrument,
                    currency=instrument.currency,
                    transaction_date=self.trade_date,
                    trade_proposal=self,
                    portfolio=self.portfolio,
                    defaults={
                        "shares": trade_dto.target_shares,
                        "weighting": trade_dto.delta_weight,
                        "status": Trade.Status.DRAFT,
                        "currency_fx_rate": instrument.currency.convert(self.trade_date, self.portfolio.currency),
                    },
                )

    # End tools methods

    # Start FSM logics

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
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.SEND.icon,
                key="submit",
                label="Submit",
                action_label="Submit",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def submit(self, by=None, description=None, **kwargs):
        self.trades.update(status=Trade.Status.SUBMIT)
        self.evaluate_active_rules(
            self.trade_date, self.validated_trading_service.target_portfolio, asynchronously=True
        )

    def can_submit(self):
        errors = dict()
        errors_list = []
        if self.trades.exists() and self.trades.exclude(status=Trade.Status.DRAFT).exists():
            errors_list.append("All trades need to be draft before submitting")
        service = self.validated_trading_service
        try:
            service.is_valid(ignore_error=True)
            # if service.trades_batch.totat_abs_delta_weight == 0:
            #     errors_list.append(
            #         "There is no change detected in this trade proposal. Please submit at last one valid trade"
            #     )
            if len(service.validated_trades) == 0:
                errors_list.append("There is no valid trade on this proposal")
            if service.errors:
                errors_list.extend(service.errors)
            if errors_list:
                errors["non_field_errors"] = errors_list
        except ValidationError:
            errors["non_field_errors"] = service.errors
            with suppress(KeyError):
                del self.__dict__["validated_trading_service"]
        return errors

    @property
    def can_be_approved_or_denied(self):
        return self.has_no_rule_or_all_checked_succeed and self.portfolio.is_manageable

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.APPROVED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.can_be_approved_or_denied,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.APPROVE.icon,
                key="approve",
                label="Approve",
                action_label="Approve",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def approve(self, by=None, description=None, **kwargs):
        apply_trades_proposal_as_task.delay(self.id)

    def can_approve(self):
        errors = dict()
        if self.trades.exclude(status=Trade.Status.SUBMIT).exists():
            errors["non_field_errors"] = "At least one trade needs to be submitted to be able to approve this proposal"
        if not self.portfolio.is_manageable:
            errors[
                "portfolio"
            ] = "The portfolio needs to be a model portfolio in order to approve this trade proposal manually"
        if self.has_assigned_active_rules and not self.has_all_check_completed_and_succeed:
            errors["non_field_errors"] = "The pre trades rules did not passed successfully"
        return errors

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DENIED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.can_be_approved_or_denied,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.DENY.icon,
                key="deny",
                label="Deny",
                action_label="Deny",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def deny(self, by=None, description=None, **kwargs):
        self.trades.all().delete()
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]

    def can_deny(self):
        errors = dict()
        if self.trades.exclude(status=Trade.Status.SUBMIT).exists():
            errors["non_field_errors"] = "At least one trade needs to be submitted to be able to deny this proposal"
        return errors

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.has_all_check_completed,  # we wait for all checks to succeed before proposing the back to draft transition
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.UNDO.icon,
                key="backtodraft",
                label="Back to Draft",
                action_label="backtodraft",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def backtodraft(self, **kwargs):
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]
        self.trades.update(status=Trade.Status.DRAFT)
        self.checks.delete()

    def can_backtodraft(self):
        errors = dict()
        if self.trades.exclude(status=Trade.Status.SUBMIT).exists():
            errors["non_field_errors"] = "All trades need to be submitted before reverting back to draft"
        return errors

    @transition(
        field=status,
        source=Status.APPROVED,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.REGENERATE.icon,
                key="revert",
                label="Revert",
                action_label="revert",
                description_fields="<p>Unapply trades and move everything back to draft (i.e. The underlying asset positions will change like the trades were never applied)</p>",
            )
        },
    )
    def revert(self, **kwargs):
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]
        revert_trade_proposal_as_task.delay(self.id, **kwargs)

    def can_revert(self):
        errors = dict()
        if self.trades.exclude(status=Trade.Status.EXECUTED).exists():
            errors["non_field_errors"] = "All trades need to be executed before reverting"
        if not self.portfolio.is_manageable:
            errors[
                "portfolio"
            ] = "The portfolio needs to be a model portfolio in order to revert this trade proposal manually"
        return errors

    # End FSM logics

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbportfolio:tradeproposal"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbportfolio:tradeproposalrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{_portfolio.name}} ({{trade_date}})"

    class Meta:
        verbose_name = "Trade Proposal"
        verbose_name_plural = "Trade Proposals"
        unique_together = ["portfolio", "trade_date"]


@shared_task(queue="portfolio")
def apply_trades_proposal_as_task(trade_proposal_id):
    trade_proposal = TradeProposal.objects.get(id=trade_proposal_id)
    trade_proposal.apply_trades()


@shared_task(queue="portfolio")
def revert_trade_proposal_as_task(trade_proposal_id, **kwargs):
    trade_proposal = TradeProposal.objects.get(id=trade_proposal_id)
    trade_proposal.revert_trades()


@receiver(post_save, sender="wbportfolio.TradeProposal")
def post_save_trade_proposal(sender, instance, created, raw, **kwargs):
    if created and not raw and instance.portfolio.assets.filter(date__lte=instance.trade_date).exists():
        instance.create_or_update_trades(reset=True)
