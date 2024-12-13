from datetime import date, timedelta

from psycopg.types.range import DateRange
from wbcore import filters as wb_filters
from wbportfolio.models import Fees, Portfolio, Trade, Transaction


def get_transaction_gte_default(field, request, view):
    filter_date = date.today() - timedelta(days=90)
    qs = Transaction.objects.none()
    if "instrument_id" in view.kwargs:
        qs = Transaction.objects.filter(underlying_instrument__id=view.kwargs["instrument_id"])
    elif "portfolio_id" in view.kwargs:
        qs = Transaction.objects.filter(portfolio__id=view.kwargs["portfolio_id"])
    if qs.exists():
        filter_date = qs.earliest("transaction_date").transaction_date
    return filter_date


def get_transaction_underlying_type_choices(*args):
    models = [Fees, Trade]
    choices = []
    for model in models:
        for choice in model.Type.choices:
            choices.append(choice)
    return choices


def get_transaction_lte_default(field, request, view):
    filter_date = date.today() + timedelta(days=7)
    qs = Transaction.objects.none()
    if "instrument_id" in view.kwargs:
        qs = Transaction.objects.filter(underlying_instrument__id=view.kwargs["instrument_id"])
    elif "portfolio_id" in view.kwargs:
        qs = Transaction.objects.filter(portfolio__id=view.kwargs["portfolio_id"])
    if qs.exists():
        filter_date = qs.latest("transaction_date").transaction_date
    return filter_date


def get_transaction_default_date_range(*args, **kwargs):
    return DateRange(get_transaction_gte_default(*args, **kwargs), get_transaction_lte_default(*args, **kwargs))


class TransactionFilterSet(wb_filters.FilterSet):
    transaction_date = wb_filters.DateRangeFilter(
        method=wb_filters.DateRangeFilter.base_date_range_filter_method,
        label="Date Range",
        default=get_transaction_default_date_range,
    )

    portfolio = wb_filters.ModelChoiceFilter(
        label="Portfolio",
        queryset=Portfolio.objects.all(),
        endpoint=Portfolio.get_representation_endpoint(),
        value_key=Portfolio.get_representation_value_key(),
        label_key=Portfolio.get_representation_label_key(),
    )
    total_value_usd__gte = wb_filters.NumberFilter(
        lookup_expr="gte", field_name="total_value_usd", label="Total Value ($)"
    )
    total_value_usd__lte = wb_filters.NumberFilter(
        lookup_expr="lte",
        label="Total Value ($)",
        field_name="total_value_usd",
    )

    transaction_underlying_type = wb_filters.ChoiceFilter(
        label="Underlying Type",
        choices=get_transaction_underlying_type_choices(),
        method="filter_transaction_underlying_type",
    )

    def filter_transaction_underlying_type(self, queryset, name, value):
        if value:
            queryset = queryset.filter(transaction_underlying_type=value)
        return queryset

    class Meta:
        model = Transaction
        fields = {
            "transaction_type": ["exact"],
            "underlying_instrument": ["exact"],
            "currency": ["exact"],
            "total_value": ["gte", "exact", "lte"],
            "total_value_fx_portfolio": ["gte", "exact", "lte"],
        }


class TransactionPortfolioFilterSet(TransactionFilterSet):
    portfolio = transaction_date__gte = transaction_date__lte = None
    transaction_date = wb_filters.DateFilter(
        label="Transaction Date",
        lookup_expr="exact",
        field_name="transaction_date",
        default=get_transaction_lte_default,
        required=True,
    )
