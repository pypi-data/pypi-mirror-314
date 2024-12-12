from wbcore import filters as wb_filters
from wbcore.filters.defaults import current_quarter_date_range
from wbcore.pandas.filterset import PandasFilterSetMixin
from wbportfolio.models import Fees

from .transactions import TransactionFilterSet, get_transaction_default_date_range


class FeesFilter(TransactionFilterSet):
    """FilterSet for Fees

    Currently filters:
    - date: daterange

    """

    fee_date = wb_filters.DateRangeFilter(
        method=wb_filters.DateRangeFilter.base_date_range_filter_method,
        label="Date Range",
        default=get_transaction_default_date_range,
    )
    total_value_usd__gte = total_value_usd__lte = transaction_underlying_type = transaction_date = None

    class Meta:
        model = Fees
        fields = {
            "transaction_subtype": ["exact"],
            "currency_fx_rate": ["gte", "exact", "lte"],
            "portfolio": ["exact"],
            "currency": ["exact"],
            "total_value": ["gte", "exact", "lte"],
            "total_value_fx_portfolio": ["gte", "exact", "lte"],
            "total_value_gross": ["gte", "exact", "lte"],
            "total_value_gross_fx_portfolio": ["gte", "exact", "lte"],
        }


class FeesPortfolioFilterSet(FeesFilter):
    portfolio = None

    class Meta:
        model = Fees
        fields = {
            "calculated": ["exact"],
            "transaction_subtype": ["exact"],
            "currency_fx_rate": ["gte", "exact", "lte"],
            "currency": ["exact"],
            "total_value": ["gte", "exact", "lte"],
            "total_value_fx_portfolio": ["gte", "exact", "lte"],
            "total_value_gross": ["gte", "exact", "lte"],
            "total_value_gross_fx_portfolio": ["gte", "exact", "lte"],
        }


class FeesAggregatedFilter(PandasFilterSetMixin, wb_filters.FilterSet):
    transaction_date = wb_filters.DateRangeFilter(
        label="Date Range",
        method=wb_filters.DateRangeFilter.base_date_range_filter_method,
        required=True,
        clearable=False,
        default=current_quarter_date_range,
    )

    class Meta:
        model = Fees
        fields = {}
