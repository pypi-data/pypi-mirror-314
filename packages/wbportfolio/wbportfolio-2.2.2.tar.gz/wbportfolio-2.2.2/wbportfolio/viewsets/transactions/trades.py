from decimal import Decimal

import pandas as pd
import plotly.graph_objects as go
from django.contrib.messages import warning
from django.db.models import BooleanField, Case, F, OuterRef, Subquery, Sum, Value, When
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django_filters.rest_framework import DjangoFilterBackend
from wbcore import viewsets
from wbcore.permissions.permissions import InternalUserPermissionMixin
from wbcore.utils.strings import format_number
from wbcrm.models import Account
from wbcore.viewsets.mixins import OrderableMixin
from wbportfolio.filters import (
    SubscriptionRedemptionFilterSet,
    SubscriptionRedemptionPortfolioFilterSet,
    TradeFilter,
    TradeInstrumentFilterSet,
    TradePortfolioFilter,
)
from wbportfolio.import_export.resources.trades import TradeProposalTradeResource
from wbportfolio.models import Trade, TradeProposal
from wbportfolio.models.transactions.claim import Claim
from wbportfolio.serializers import (
    ReadOnlyTradeTradeProposalModelSerializer,
    TradeModelSerializer,
    TradeProposalRepresentationSerializer,
    TradeRepresentationSerializer,
    TradeTradeProposalModelSerializer,
)
from wbportfolio.viewsets.configs.titles.trades import (
    CustomerDistributionInstrumentTitleConfig,
)

from ..configs import (
    CustodianDistributionInstrumentEndpointConfig,
    CustodianDistributionInstrumentTitleConfig,
    SubscriptionRedemptionDisplayConfig,
    SubscriptionRedemptionEndpointConfig,
    SubscriptionRedemptionTitleConfig,
    TradeButtonConfig,
    TradeDisplayConfig,
    TradeEndpointConfig,
    TradeInstrumentButtonConfig,
    TradeInstrumentEndpointConfig,
    TradeInstrumentTitleConfig,
    TradePortfolioDisplayConfig,
    TradePortfolioEndpointConfig,
    TradePortfolioTitleConfig,
    TradeTitleConfig,
    TradeTradeProposalButtonConfig,
    TradeTradeProposalDisplayConfig,
    TradeTradeProposalEndpointConfig,
)
from ..mixins import UserPortfolioRequestPermissionMixin
from .transactions import TransactionModelViewSet


class TradeProposalRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:trade"
    queryset = TradeProposal.objects.all()
    serializer_class = TradeProposalRepresentationSerializer


class TradeRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    filterset_class = TradeFilter

    ordering_fields = ("transaction_date", "shares")
    ordering = ["-transaction_date"]
    search_fields = (
        "underlying_instrument__name",
        "bank",
        "shares",
        "comment",
        "external_id",
        "register__register_name_1",
        "register__register_name_2",
        "register__custodian_name_1",
        "register__custodian_name_2",
    )

    queryset = Trade.objects.select_related("underlying_instrument")
    serializer_class = TradeRepresentationSerializer

    def get_queryset(self):
        return (
            Trade.objects.filter(marked_for_deletion=False, pending=False)
            .select_related("portfolio")
            .select_related("underlying_instrument")
            .prefetch_related("claims")
        )


class TradeModelViewSet(TransactionModelViewSet):
    IDENTIFIER = "wbportfolio:trade"

    ordering_fields = (
        "id",
        "transaction_subtype",
        "transaction_date",
        "underlying_instrument__name",
        "shares",
        "approved_claimed_shares",
        "pending_claimed_shares",
        "price",
        "total_value",
        "total_value_fx_portfolio",
        "total_value_usd",
        "currency_fx_rate",
        "currency__key",
        "bank",
        "register__computed_str",
        "comment",
    )
    search_fields = (
        "portfolio__name",
        "underlying_instrument__name",
        "bank",
        "comment",
        "external_id",
        "register__computed_str",
        "register__register_name_1",
        "register__register_name_2",
        "register__custodian_name_1",
        "register__custodian_name_2",
    )

    filterset_class = TradeFilter
    queryset = Trade.objects.all()
    serializer_class = TradeModelSerializer

    display_config_class = TradeDisplayConfig
    endpoint_config_class = TradeEndpointConfig
    title_config_class = TradeTitleConfig
    button_config_class = TradeButtonConfig

    def get_aggregates(self, queryset, paginated_queryset):
        return {
            "shares": {
                "Σ": format_number(queryset.aggregate(s=Sum("shares"))["s"] or Decimal(0)),
            },
            **super().get_aggregates(queryset, paginated_queryset),
        }

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.is_portfolio_manager:
            qs = qs.filter(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])
        qs = (
            qs.annotate(
                approved_claimed_shares=Coalesce(
                    Subquery(
                        Claim.objects.filter(status=Claim.Status.APPROVED, trade=OuterRef("pk"))
                        .values("trade")
                        .annotate(sum_shares=Sum("shares"))
                        .values("sum_shares")[:1]
                    ),
                    Decimal(0.0),
                ),
                pending_claimed_shares=Coalesce(
                    Subquery(
                        Claim.objects.filter(
                            status__in=[Claim.Status.PENDING, Claim.Status.DRAFT], trade=OuterRef("pk")
                        )
                        .values("trade")
                        .annotate(sum_shares=Sum("shares"))
                        .values("sum_shares")[:1]
                    ),
                    Decimal(0.0),
                ),
                completely_claimed=Case(
                    When(shares=F("approved_claimed_shares"), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                completely_claimed_if_approved=Case(
                    When(completely_claimed=True, then=Value(False)),
                    When(shares=F("approved_claimed_shares") + F("pending_claimed_shares"), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
            .select_related("underlying_instrument")
            .select_related("register")
            .select_related("portfolio")
            .select_related("currency")
            .select_related("custodian")
            .select_related("import_source")
            .prefetch_related("claims")
            .prefetch_related("claims__account")
            .prefetch_related("claims__claimant")
            .prefetch_related("claims__product")
        )
        return qs


class SubscriptionRedemptionModelViewSet(TradeModelViewSet):
    IDENTIFIER = "wbportoflio:subscriptionredemption"
    filterset_class = SubscriptionRedemptionFilterSet
    display_config_class = SubscriptionRedemptionDisplayConfig
    title_config_class = SubscriptionRedemptionTitleConfig
    endpoint_config_class = SubscriptionRedemptionEndpointConfig

    def get_queryset(self):
        return super().get_queryset().filter(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])


class TradePortfolioModelViewSet(TradeModelViewSet):
    IDENTIFIER = "wbportfolio:trade"
    filterset_class = TradePortfolioFilter
    title_config_class = TradePortfolioTitleConfig
    endpoint_config_class = TradePortfolioEndpointConfig
    display_config_class = TradePortfolioDisplayConfig

    def get_aggregates(self, queryset, paginated_queryset):
        if queryset.exists():
            return {
                "total_value_fx_portfolio": {
                    "Σ": format_number(queryset.aggregate(s=Sum(F("total_value_fx_portfolio")))["s"])
                },
                **super().get_aggregates(queryset, paginated_queryset),
            }
        return dict()

    def get_queryset(self):
        return super().get_queryset().filter(portfolio=self.portfolio)


class TradeInstrumentModelViewSet(TradeModelViewSet):
    IDENTIFIER = "wbportfolio:trade"

    filterset_class = TradeInstrumentFilterSet

    title_config_class = TradeInstrumentTitleConfig
    endpoint_config_class = TradeInstrumentEndpointConfig
    button_config_class = TradeInstrumentButtonConfig

    def get_aggregates(self, queryset, paginated_queryset):
        if queryset.exists():
            return {
                "total_value": {"Σ": format_number(queryset.aggregate(s=Sum(F("total_value")))["s"])},
                **super().get_aggregates(queryset, paginated_queryset),
            }
        return dict()

    def get_queryset(self):
        return (
            super().get_queryset().filter(underlying_instrument__in=self.instrument.get_descendants(include_self=True))
        )


class SubscriptionRedemptionInstrumentModelViewSet(SubscriptionRedemptionModelViewSet):
    filterset_class = SubscriptionRedemptionPortfolioFilterSet

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                underlying_instrument__in=self.instrument.get_descendants(include_self=True),
                transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION],
            )
        )


class CustodianDistributionInstrumentChartViewSet(UserPortfolioRequestPermissionMixin, viewsets.ChartViewSet):
    IDENTIFIER = "wbportfolio:custodiandistribution"
    filterset_fields = {
        "transaction_date": ["lte"],
    }
    filter_backends = (DjangoFilterBackend,)
    queryset = Trade.objects.all()

    title_config_class = CustodianDistributionInstrumentTitleConfig
    endpoint_config_class = CustodianDistributionInstrumentEndpointConfig

    def get_plotly(self, queryset):
        fig = go.Figure()
        if queryset.exists():
            df = pd.DataFrame(queryset.values("custodian__name", "custodian__id", "shares"))
            df = df.groupby("custodian__id").agg({"custodian__name": "first", "shares": "sum"})
            fig = go.Figure(data=[go.Pie(labels=df.custodian__name, values=df.shares)])
        return fig

    def get_queryset(self):
        return Trade.objects.filter(underlying_instrument=self.instrument)


class CustomerDistributionInstrumentChartViewSet(UserPortfolioRequestPermissionMixin, viewsets.ChartViewSet):
    IDENTIFIER = "wbportfolio:custodiandistribution"
    filterset_fields = {
        "transaction_date": ["lte"],
    }
    filter_backends = (DjangoFilterBackend,)
    queryset = Trade.objects.all()

    title_config_class = CustomerDistributionInstrumentTitleConfig
    endpoint_config_class = CustodianDistributionInstrumentEndpointConfig

    # TODO: Consider moving into a helper class?
    def group_smaller_items(self, df, threshold=0.01, text="Others"):
        df["weight"] = df.sum_shares / df.sum_shares.sum()
        group_sum = df.loc[df["weight"] < threshold].sum().to_frame().T
        group_sum["account_name"] = text
        rest = df.loc[df["weight"] >= threshold]
        return pd.concat([group_sum, rest])

    def get_plotly(self, queryset):
        fig = go.Figure()
        if queryset.exists():
            df = self.group_smaller_items(
                pd.DataFrame(queryset.values("account_name", "sum_shares")),
            )

            fig = go.Figure(data=[go.Pie(labels=df.account_name, values=df.sum_shares)])
        return fig

    def get_queryset(self):
        return (
            Trade.objects.filter(
                underlying_instrument=self.instrument, transaction_subtype__in=["SUBSCRIPTION", "REDEMPTION"]
            )
            .values("claims")
            .annotate(
                shares=F("claims__shares"),
                account_tree_id=F("claims__account__tree_id"),
                status=F("claims__status"),
            )
            .filter(status="APPROVED")
            .values("account_tree_id")
            .annotate(
                account_name=Subquery(
                    Account.objects.filter(tree_id=OuterRef("account_tree_id"), level=0).values("title")[:1]
                ),
                sum_shares=Sum("shares"),
            )
            .filter(account_name__isnull=False)
        )


class TradeTradeProposalModelViewSet(
    UserPortfolioRequestPermissionMixin, InternalUserPermissionMixin, OrderableMixin, viewsets.ModelViewSet
):
    ordering = (
        "trade_proposal",
        "order",
    )
    IDENTIFIER = "wbportfolio:tradeproposal"
    search_fields = ("underlying_instrument__name",)
    filterset_fields = {}
    queryset = Trade.objects.all()

    display_config_class = TradeTradeProposalDisplayConfig
    endpoint_config_class = TradeTradeProposalEndpointConfig
    serializer_class = TradeTradeProposalModelSerializer
    button_config_class = TradeTradeProposalButtonConfig

    @cached_property
    def trade_proposal_status(self):
        return get_object_or_404(TradeProposal, pk=self.kwargs["trade_proposal_id"]).status

    def get_resource_class(self):
        return TradeProposalTradeResource

    def get_aggregates(self, queryset, paginated_queryset):
        if queryset.exists():
            aggregates = queryset.aggregate(
                sum_target_weight=Sum(F("target_weight")),
                sum_effective_weight=Sum(F("effective_weight")),
                sum_weighting=Sum(F("weighting")),
            )
            return {
                "target_weight": {"Σ": format_number(aggregates["sum_target_weight"], decimal=5)},
                "effective_weight": {"Σ": format_number(aggregates["sum_effective_weight"], decimal=5)},
                "weighting": {"Σ": format_number(aggregates["sum_weighting"], decimal=5)},
            }
        return {}

    def get_serializer_class(self):
        if self.trade_proposal_status != TradeProposal.Status.DRAFT:
            return ReadOnlyTradeTradeProposalModelSerializer
        return TradeTradeProposalModelSerializer

    def add_messages(self, request, queryset=None, paginated_queryset=None, instance=None, initial=False):
        if queryset:
            total_target_weight = float(queryset.aggregate(c=Sum(F("target_weight")))["c"]) or 0
            if round(total_target_weight, 3) != 1:
                warning(request, "The total target weight does not equals to 1")

    def get_queryset(self):
        if self.is_portfolio_manager:
            return super().get_queryset().filter(trade_proposal=self.kwargs["trade_proposal_id"])
        return TradeProposal.objects.none()
