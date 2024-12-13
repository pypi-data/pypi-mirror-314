from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from wbcompliance.viewsets.risk_management.mixins import RiskCheckViewSetMixin
from wbcore import viewsets
from wbcore.metadata.configs.display.instance_display import (
    Display,
    create_simple_display,
)
from wbcore.permissions.permissions import InternalUserPermissionMixin
from wbcore.utils.views import CloneMixin
from wbportfolio.models import TradeProposal
from wbportfolio.models.transactions.trade_proposals import (
    apply_trades_proposal_as_task,
)
from wbportfolio.serializers import (
    TradeProposalModelSerializer,
    TradeProposalRepresentationSerializer,
)

from ..configs import (
    TradeProposalButtonConfig,
    TradeProposalDisplayConfig,
    TradeProposalEndpointConfig,
    TradeProposalPortfolioEndpointConfig,
)


class TradeProposalRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:trade"
    queryset = TradeProposal.objects.all()
    serializer_class = TradeProposalRepresentationSerializer


class TradeProposalModelViewSet(CloneMixin, RiskCheckViewSetMixin, InternalUserPermissionMixin, viewsets.ModelViewSet):
    ordering_fields = ("trade_date",)
    ordering = ("-trade_date",)
    search_fields = ("comment",)
    filterset_fields = {"trade_date": ["exact", "gte", "lte"], "status": ["exact"]}

    queryset = TradeProposal.objects.select_related("model_portfolio", "portfolio")
    serializer_class = TradeProposalModelSerializer
    display_config_class = TradeProposalDisplayConfig
    button_config_class = TradeProposalButtonConfig
    endpoint_config_class = TradeProposalEndpointConfig

    @classmethod
    def get_clone_instance_display(cls) -> Display:
        return create_simple_display(
            [
                ["comment"],
                ["trade_date"],
            ]
        )

    @classmethod
    def _get_risk_checks_button_title(cls) -> str:
        return "Pre-Trade Checks"

    @action(detail=True, methods=["PATCH"])
    def reset(self, request, pk=None):
        trade_proposal = get_object_or_404(TradeProposal, pk=pk)
        if trade_proposal.status == TradeProposal.Status.DRAFT:
            trade_proposal.reset_trades()
            return Response({"send": True})

    @action(detail=True, methods=["PATCH"])
    def normalize(self, request, pk=None):
        trade_proposal = get_object_or_404(TradeProposal, pk=pk)
        if trade_proposal.status == TradeProposal.Status.DRAFT:
            trade_proposal.normalize_trades()
            return Response({"send": True})

    @action(detail=True, methods=["PATCH"])
    def replay(self, request, pk=None):
        trade_proposal = get_object_or_404(TradeProposal, pk=pk)
        if trade_proposal.portfolio.is_manageable:
            apply_trades_proposal_as_task.delay(trade_proposal.id)
            return Response({"send": True})

    @action(detail=True, methods=["PATCH"])
    def deleteall(self, request, pk=None):
        trade_proposal = get_object_or_404(TradeProposal, pk=pk)
        if trade_proposal.status == TradeProposal.Status.DRAFT:
            trade_proposal.trades.all().delete()
            return Response({"send": True})


class TradeProposalPortfolioModelViewSet(TradeProposalModelViewSet):
    endpoint_config_class = TradeProposalPortfolioEndpointConfig

    def get_queryset(self):
        return TradeProposal.objects.filter(portfolio=self.kwargs["portfolio_id"])
