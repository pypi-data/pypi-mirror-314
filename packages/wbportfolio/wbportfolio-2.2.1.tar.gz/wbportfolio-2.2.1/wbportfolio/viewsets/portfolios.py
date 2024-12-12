from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from wbcore import viewsets
from wbcore.contrib.currency.models import Currency
from wbcore.permissions.permissions import InternalUserPermissionMixin
from wbcore.utils.date import get_date_interval_from_request
from wbportfolio.filters import PortfolioFilterSet
from wbportfolio.models import (
    Portfolio,
    PortfolioPortfolioThroughModel,
    PortfolioSynchronization,
    PriceComputation,
    TradeProposal,
)
from wbportfolio.models.portfolio import resynchronize_history_as_task
from wbportfolio.serializers import (
    ModelPortfolioModelSerializer,
    PortfolioModelSerializer,
    PortfolioPortfolioThroughModelSerializer,
    PortfolioRepresentationSerializer,
)

from .configs import (
    ModelPortfolioButtonConfig,
    ModelPortfolioDisplayConfig,
    ModelPortfolioEndpointConfig,
    ModelPortfolioTitleConfig,
    PortfolioButtonConfig,
    PortfolioDisplayConfig,
    PortfolioEndpointConfig,
    PortfolioPortfolioThroughModelDisplayConfig,
    PortfolioPortfolioThroughModelEndpointConfig,
    PortfolioPreviewConfig,
    PortfolioTitleConfig,
)
from .mixins import UserPortfolioRequestPermissionMixin


class PortfolioRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:portfolio"

    ordering_fields = ordering = search_fields = ("name",)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioRepresentationSerializer
    filterset_class = PortfolioFilterSet


class PortfolioModelViewSet(UserPortfolioRequestPermissionMixin, InternalUserPermissionMixin, viewsets.ModelViewSet):
    filterset_class = PortfolioFilterSet
    serializer_class = PortfolioModelSerializer
    queryset = Portfolio.objects.all()

    search_fields = ("currency__key", "name")
    ordering_fields = search_fields
    ordering = ["name"]

    display_config_class = PortfolioDisplayConfig
    button_config_class = PortfolioButtonConfig
    title_config_class = PortfolioTitleConfig
    endpoint_config_class = PortfolioEndpointConfig
    preview_config_class = PortfolioPreviewConfig

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "currency",
                "portfolio_synchronization",
            )
            .prefetch_related(
                "depends_on",
                "dependent_portfolios",
            )
        )

    @action(detail=True, methods=["PATCH"])
    def rebalance(self, request, pk=None):
        if (date_str := request.POST.get("trade_date", None)) and (
            model_portfolio_id := request.POST.get("model_portfolio", None)
        ):
            TradeProposal.objects.create(
                portfolio=Portfolio.objects.get(id=pk),
                model_portfolio=Portfolio.objects.get(id=model_portfolio_id),
                trade_date=datetime.strptime(date_str, "%Y-%m-%d"),
            )
            return Response({"send": True})
        raise HttpResponse("Bad Request", status=400)

    @action(detail=True, methods=["PATCH"])
    def resynchronize(self, request, pk=None):
        if request.user.has_perm("wbportfolio.administrate_instrument"):
            portfolio = get_object_or_404(Portfolio, pk=pk)
            instrument = request.GET.get("instrument", None)
            start, end = get_date_interval_from_request(request, request_type="POST")
            resynchronize_history_as_task.delay(portfolio.id, start, end, instrument_id=instrument)
            return Response({"send": True})
        return HttpResponse("Unauthorized", status=401)


class ModelPortfolioModelViewSet(PortfolioModelViewSet):
    serializer_class = ModelPortfolioModelSerializer
    endpoint_config_class = ModelPortfolioEndpointConfig
    display_config_class = ModelPortfolioDisplayConfig
    title_config_class = ModelPortfolioTitleConfig
    button_config_class = ModelPortfolioButtonConfig

    @action(detail=False, methods=["POST"])
    def createmodelportfolio(self, request, pk=None):
        if self.is_portfolio_manager:
            name = request.POST["name"]
            currency_id = request.POST["currency"]
            currency = Currency.objects.get(id=currency_id)
            portfolio_synchronization_id = request.POST.get("portfolio_synchronization", None)
            price_computation_id = request.POST.get("price_computation", None)
            portfolio_synchronization = (
                PortfolioSynchronization.objects.get(id=portfolio_synchronization_id)
                if portfolio_synchronization_id
                else None
            )
            create_index = request.POST.get("create_index", "false") == "true"
            index_parameters = {}
            if create_index:
                index_parameters["price_computation"] = (
                    PriceComputation.objects.get(id=price_computation_id) if price_computation_id else None
                )
            Portfolio.create_model_portfolio(
                name, currency, portfolio_synchronization=portfolio_synchronization, index_parameters=index_parameters
            )
            return Response({"send": True})
        raise HttpResponse("Unauthorized", status=403)

    def get_queryset(self):
        model_portfolios = PortfolioPortfolioThroughModel.objects.filter(
            type=PortfolioPortfolioThroughModel.Type.MODEL
        ).values("dependency_portfolio")
        return super().get_queryset().filter(id__in=model_portfolios)


class PortfolioPortfolioThroughModelViewSet(InternalUserPermissionMixin, viewsets.ModelViewSet):
    serializer_class = PortfolioPortfolioThroughModelSerializer
    queryset = PortfolioPortfolioThroughModel.objects.all()

    search_fields = ["dependency_portfolio__name"]

    display_config_class = PortfolioPortfolioThroughModelDisplayConfig
    endpoint_config_class = PortfolioPortfolioThroughModelEndpointConfig

    def get_queryset(self):
        return super().get_queryset().filter(portfolio=self.kwargs["portfolio_id"])
