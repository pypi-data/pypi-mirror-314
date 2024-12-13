from decimal import Decimal

from django.db.models import (
    Case,
    DecimalField,
    ExpressionWrapper,
    F,
    OuterRef,
    Subquery,
    Sum,
    When,
)
from wbcore import viewsets
from wbcore.contrib.currency.models import CurrencyFXRates
from wbcore.permissions.permissions import InternalUserPermissionMixin
from wbcore.utils.strings import format_number
from wbportfolio.filters import TransactionFilterSet, TransactionPortfolioFilterSet
from wbportfolio.models import Fees, Trade, Transaction
from wbportfolio.serializers import (
    TransactionModelSerializer,
    TransactionRepresentationSerializer,
)

from ..configs import (
    TransactionDisplayConfig,
    TransactionEndpointConfig,
    TransactionPortfolioDisplayConfig,
    TransactionPortfolioEndpointConfig,
    TransactionPortfolioTitleConfig,
)
from ..mixins import UserPortfolioRequestPermissionMixin


class TransactionRepresentationViewSet(InternalUserPermissionMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbportfolio:transaction"
    filterset_class = TransactionFilterSet
    search_fields = ("portfolio__name", "underlying_instrument__name", "comment")
    ordering_fields = (
        "transaction_date",
        "currency__key",
        "underlying_instrument__name",
        "portfolio__name",
        "transaction_type",
        "book_date",
        "value_date",
        "currency_fx_rate",
        "total_value",
        "total_value_fx_portfolio",
        "total_value_gross",
        "total_value_gross_fx_portfolio",
    )
    ordering = ["-transaction_date"]

    serializer_class = TransactionRepresentationSerializer
    queryset = Transaction.objects.all()


class TransactionModelViewSet(UserPortfolioRequestPermissionMixin, InternalUserPermissionMixin, viewsets.ModelViewSet):
    IDENTIFIER = "wbportfolio:transaction"

    serializer_class = TransactionModelSerializer

    filterset_class = TransactionFilterSet
    ordering_fields = TransactionRepresentationViewSet.ordering_fields
    search_fields = TransactionRepresentationViewSet.search_fields
    ordering = TransactionRepresentationViewSet.ordering

    queryset = Transaction.objects.all()
    display_config_class = TransactionDisplayConfig
    endpoint_config_class = TransactionEndpointConfig

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                fx_rate=CurrencyFXRates.get_fx_rates_subquery(
                    "transaction_date", currency="currency", lookup_expr="exact"
                ),
                total_value_usd=ExpressionWrapper(F("total_value") * F("fx_rate"), output_field=DecimalField()),
                total_value_gross_usd=ExpressionWrapper(
                    F("total_value_gross") * F("fx_rate"), output_field=DecimalField()
                ),
                transaction_underlying_type_trade=Subquery(
                    Trade.objects.filter(id=OuterRef("pk")).values("transaction_subtype")[:1]
                ),
                transaction_underlying_type_fees=Subquery(
                    Fees.objects.filter(id=OuterRef("pk")).values("transaction_subtype")[:1]
                ),
                transaction_underlying_type=Case(
                    When(
                        transaction_underlying_type_trade__isnull=False,
                        then=F("transaction_underlying_type_trade"),
                    ),
                    When(transaction_underlying_type_fees__isnull=False, then=F("transaction_underlying_type_fees")),
                ),
            )
            .select_related("underlying_instrument")
            .select_related("portfolio")
            .select_related("currency")
        )

    def get_aggregates(self, queryset, paginated_queryset):
        return {
            "total_value_usd": {
                "Σ": format_number(queryset.aggregate(s=Sum("total_value_usd"))["s"] or Decimal(0)),
            }
        }


class TransactionPortfolioModelViewSet(TransactionModelViewSet):
    IDENTIFIER = "wbportfolio:transaction"

    filterset_class = TransactionPortfolioFilterSet
    display_config_class = TransactionPortfolioDisplayConfig
    endpoint_config_class = TransactionPortfolioEndpointConfig
    title_config_class = TransactionPortfolioTitleConfig

    def get_queryset(self):
        qs = super().get_queryset().filter(portfolio=self.portfolio)
        if self.is_portfolio_manager:
            return qs
        return qs.exclude(transaction_type=Transaction.Type.FEES)
