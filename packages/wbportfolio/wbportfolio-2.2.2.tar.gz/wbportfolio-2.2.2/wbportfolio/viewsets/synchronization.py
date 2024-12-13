from wbcore import viewsets
from wbcore.permissions.permissions import InternalUserPermissionMixin
from wbportfolio.models import PortfolioSynchronization, PriceComputation
from wbportfolio.serializers import (
    PortfolioSynchronizationRepresentationSerializer,
    PriceComputationRepresentationSerializer,
)


class PortfolioSynchronizationRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:portfoliosynchronization"

    ordering_fields = ordering = ("name",)
    search_fields = ("name",)
    queryset = PortfolioSynchronization.objects.all()
    serializer_class = PortfolioSynchronizationRepresentationSerializer


class PriceComputationRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:portfoliosynchronization"

    ordering_fields = ordering = ("name",)
    search_fields = ("name",)
    queryset = PriceComputation.objects.all()
    serializer_class = PriceComputationRepresentationSerializer
