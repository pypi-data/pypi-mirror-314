from datetime import timedelta
from decimal import Decimal

from rest_framework import serializers
from rest_framework.reverse import reverse
from wbcore import serializers as wb_serializers
from wbportfolio.models import Portfolio, PortfolioRole, Trade, TradeProposal
from wbportfolio.models.transactions.claim import Claim
from wbportfolio.serializers.custodians import CustodianRepresentationSerializer
from wbportfolio.serializers.portfolios import PortfolioRepresentationSerializer
from wbportfolio.serializers.registers import RegisterRepresentationSerializer

from .transactions import (
    TransactionModelSerializer,
    TransactionRepresentationSerializer,
)


class CopyClaimRepresentationSerializer(wb_serializers.RepresentationSerializer):
    claimant = wb_serializers.StringRelatedField()
    product = wb_serializers.StringRelatedField()
    account = wb_serializers.StringRelatedField()
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:claim-detail")

    class Meta:
        model = Claim
        fields = (
            "id",
            "shares",
            "claimant",
            "bank",
            "product",
            "account",
            "_detail",
        )


class TradeProposalRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:tradeproposal-detail")

    class Meta:
        model = TradeProposal
        fields = ("id", "trade_date", "status", "_detail")


class TradeRepresentationSerializer(TransactionRepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:trade-detail")

    diff_shares = wb_serializers.SerializerMethodField()

    def get_diff_shares(self, obj):
        return obj._diff_shares

    class Meta:
        model = Trade
        fields = ("claimed_shares", "diff_shares", "bank", "shares") + TransactionRepresentationSerializer.Meta.fields


class TradeClaimRepresentationSerializer(TradeRepresentationSerializer):
    def get_filter_params(self, request):
        claim_id = request.parser_context["view"].kwargs.get("pk", None)
        arg = {"marked_for_deletion": False}
        if claim_id:
            claim = Claim.objects.get(id=claim_id)
            arg.update(
                {
                    "underlying_instrument": claim.product.id,
                    "transaction_date__gte": claim.date - timedelta(days=Trade.TRADE_WINDOW_INTERVAL),
                    "transaction_date__lte": claim.date + timedelta(days=Trade.TRADE_WINDOW_INTERVAL),
                }
            )
            if claim.shares:
                if claim.shares > 0:
                    arg["shares__gte"] = claim.shares
                else:
                    arg["shares__lte"] = claim.shares
            return arg
        return {}


class TradeModelSerializer(TransactionModelSerializer):
    marked_for_deletion = wb_serializers.BooleanField(required=False, read_only=True)
    marked_as_internal = wb_serializers.BooleanField()

    approved_claimed_shares = wb_serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, read_only=True, default=Decimal(0.0)
    )
    pending_claimed_shares = wb_serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, read_only=True, default=Decimal(0.0)
    )
    completely_claimed = wb_serializers.BooleanField(required=False, read_only=True, default=Decimal(0.0))
    completely_claimed_if_approved = wb_serializers.BooleanField(required=False, read_only=True, default=Decimal(0.0))

    # We commented it because people needs to filter with lookup equals onto these fields
    # shares = wb_serializers.DecimalField(max_digits=16, decimal_places=2)
    # price = wb_serializers.DecimalField(max_digits=16, decimal_places=2)

    _register = RegisterRepresentationSerializer(source="register")
    claims = wb_serializers.PrimaryKeyRelatedField(queryset=Claim.objects.all(), label="Claims", many=True)
    _claims = CopyClaimRepresentationSerializer(source="claims", many=True)
    _custodian = CustodianRepresentationSerializer(source="custodian")
    _internal_trade = TradeRepresentationSerializer(
        source="internal_trade",
        filter_params={"only_internal_trade": True},
        optional_get_parameters={"underlying_instrument": "underlying_instrument", "transaction_date": "pivot_date"},
        depends_on=[{"field": "marked_as_internal", "options": {"activates_on": [True]}}],
    )

    @wb_serializers.register_only_instance_resource()
    def import_source_file_url(self, instance, request, user, *args, **kwargs):
        if PortfolioRole.is_portfolio_manager(user.profile, instance.underlying_instrument):
            if instance.import_source:
                return {"import_source": instance.import_source.file.url}
        return {}

    @wb_serializers.register_resource()
    def claims_list(self, instance, request, user):
        if instance.is_claimable:
            return {
                "claims": reverse(
                    "wbportfolio:trade-claim-list",
                    args=[instance.id],
                    request=request,
                )
            }
        return {}

    class Meta:
        model = Trade
        decorators = TransactionModelSerializer.Meta.decorators
        read_only_fields = (
            "id",
            "shares",
            "price",
            "transaction_subtype",
            "approved_claimed_shares",
            "pending_claimed_shares",
            "claimed_shares",
            "completely_claimed",
            "completely_claimed_if_approved",
            "register",
            "_register",
            "pending",
            "bank",
            "marked_for_deletion",
            "_claims",
            "claims",
            "transaction_type",
            "transaction_url_type",
            "transaction_underlying_type",
            "portfolio",
            "_portfolio",
            "underlying_instrument",
            "_underlying_instrument",
            "transaction_date",
            "book_date",
            "value_date",
            "currency",
            "_currency",
            "currency_fx_rate",
            "total_value",
            "total_value_fx_portfolio",
            "total_value_gross",
            "total_value_gross_fx_portfolio",
            "external_id",
            "total_value_usd",
            "total_value_gross_usd",
            "_additional_resources",
        )

        fields = (
            "id",
            "shares",
            "price",
            "transaction_subtype",
            "approved_claimed_shares",
            "pending_claimed_shares",
            "claimed_shares",
            "completely_claimed",
            "completely_claimed_if_approved",
            "register",
            "_register",
            "pending",
            "bank",
            "marked_for_deletion",
            "_claims",
            "claims",
            "transaction_type",
            "transaction_url_type",
            "transaction_underlying_type",
            "portfolio",
            "_portfolio",
            "underlying_instrument",
            "_underlying_instrument",
            "transaction_date",
            "book_date",
            "value_date",
            "currency",
            "_currency",
            "currency_fx_rate",
            "total_value",
            "total_value_fx_portfolio",
            "total_value_gross",
            "total_value_gross_fx_portfolio",
            "external_id",
            "comment",
            "total_value_usd",
            "total_value_gross_usd",
            "_custodian",
            "custodian",
            "marked_as_internal",
            "internal_trade",
            "_internal_trade",
            "_additional_resources",
        )


class TradeTradeProposalModelSerializer(TradeModelSerializer):
    status = wb_serializers.ChoiceField(default=Trade.Status.DRAFT, choices=Trade.Status.choices)
    target_weight = wb_serializers.DecimalField(max_digits=16, decimal_places=6, required=False, default=0)
    effective_weight = wb_serializers.DecimalField(read_only=True, max_digits=16, decimal_places=6, default=0)

    def validate(self, data):
        if self.instance and "underlying_instrument" in data:
            raise serializers.ValidationError(
                {
                    "underlying_instrument": "You cannot modify the underlying instrument other than creating a new entry"
                }
            )
        effective_weight = self.instance._effective_weight if self.instance else Decimal(0.0)
        if (target_weight := data.pop("target_weight", None)) is not None:
            data["weighting"] = target_weight - effective_weight
        if data["weighting"] >= 0:
            data["transaction_subtype"] = "BUY"
        else:
            data["transaction_subtype"] = "SELL"
        return data

    class Meta:
        model = Trade
        percent_fields = ["effective_weight", "target_weight", "weighting"]
        read_only_fields = (
            "transaction_subtype",
            "shares"
            # "underlying_instrument",
            # "_underlying_instrument",
        )
        fields = (
            "id",
            "shares",
            "underlying_instrument",
            "_underlying_instrument",
            "transaction_subtype",
            "status",
            # "total_value",
            # "total_value_fx_portfolio",
            # "total_value_gross",
            # "total_value_gross_fx_portfolio",
            "comment",
            # "total_value_usd",
            # "total_value_gross_usd",
            "effective_weight",
            "target_weight",
            "weighting",
            "trade_proposal",
            "order",
        )


class ReadOnlyTradeTradeProposalModelSerializer(TradeTradeProposalModelSerializer):
    class Meta(TradeTradeProposalModelSerializer.Meta):
        read_only_fields = TradeTradeProposalModelSerializer.Meta.fields


class TradeProposalModelSerializer(wb_serializers.ModelSerializer):
    _model_portfolio = PortfolioRepresentationSerializer(source="model_portfolio")
    model_portfolio = wb_serializers.PrimaryKeyRelatedField(
        queryset=Portfolio.objects.all(),
        default=wb_serializers.DefaultFromKwargs("portfolio_id"),
        read_only=lambda view: not view.new_mode,
    )
    trade_date = wb_serializers.DateField(read_only=lambda view: not view.new_mode)

    def create(self, validated_data):
        if request := self.context.get("request"):
            validated_data["creator"] = request.user.profile
        return super().create(validated_data)

    @wb_serializers.register_only_instance_resource()
    def additional_resources(self, instance, request, user, **kwargs):
        res = {}
        if instance.status == TradeProposal.Status.APPROVED:
            res["replay"] = reverse("wbportfolio:tradeproposal-replay", args=[instance.id], request=request)
        if instance.model_portfolio:
            res["reset"] = reverse("wbportfolio:tradeproposal-reset", args=[instance.id], request=request)
        res["trades"] = reverse(
            "wbportfolio:tradeproposal-trade-list",
            args=[instance.id],
            request=request,
        )
        return res

    class Meta:
        model = TradeProposal
        only_fsm_transition_on_instance = True
        fields = (
            "id",
            "trade_date",
            "comment",
            "status",
            "portfolio",
            "_model_portfolio",
            "model_portfolio",
            "_additional_resources",
        )
