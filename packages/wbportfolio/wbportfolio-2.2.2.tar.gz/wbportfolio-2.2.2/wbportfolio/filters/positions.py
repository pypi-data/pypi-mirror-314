import datetime as dt

from django.db.models import TextChoices
from pandas.tseries.offsets import BDay
from wbcore import filters as wb_filters
from wbcore.contrib.currency.models import CurrencyFXRates
from wbcore.pandas.filterset import PandasFilterSetMixin
from wbcore.utils.date import current_financial_month
from wbportfolio.filters.assets import (
    DateFilterMixin,
    get_latest_end_quarter_date_asset_position,
)
from wbportfolio.models import AssetPosition


class GroupbyChoice(TextChoices):
    UNDERLYING_INSTRUMENT = "UNDERLYING_INSTRUMENT", "Underlying Instrument"
    CURRENCY = "CURRENCY", "Currency"
    COUNTRY = "COUNTRY", "Country"
    PORTFOLIO = "PORTFOLIO", "Portfolio"
    PRIMARY_CLASSIFICATION = "PRIMARY_CLASSIFICATION", "Primary Classification (Specified Height)"
    PREFERRED_CLASSIFICATION = "PREFERRED_CLASSIFICATION", "Preferred Classification (Specified Height)"

    @classmethod
    def get_id(cls, name: str) -> str:
        return {
            "UNDERLYING_INSTRUMENT": "underlying_instrument",
            "CURRENCY": "underlying_instrument__currency",
            "COUNTRY": "underlying_instrument__country",
            "PORTFOLIO": "portfolio",
            "PRIMARY_CLASSIFICATION": "classification_id",
            "PREFERRED_CLASSIFICATION": "classification_id",
        }[name]

    @classmethod
    def get_repr(cls, name: str) -> str:
        return {
            "UNDERLYING_INSTRUMENT": "underlying_instrument__name_repr",
            "CURRENCY": "underlying_instrument__currency__key",
            "COUNTRY": "underlying_instrument__country__name",
            "PORTFOLIO": "portfolio__name",
            "PRIMARY_CLASSIFICATION": "classification_title",
            "PREFERRED_CLASSIFICATION": "classification_title",
        }[name]


def get_latest_date_based_on_multiple_models(field, request, view):
    models = [AssetPosition.objects, CurrencyFXRates.objects]
    default_date = (dt.date.today() - BDay(1)).date()  # default latest date
    if not any(model.exists() for model in models):  # if at least one model is empty, it return the default date.
        return default_date

    def get_most_recent_common_date(date):
        for model in models:
            latest_model_date = model.filter(date__lte=date).latest("date").date
            if latest_model_date != date:
                return get_most_recent_common_date(latest_model_date)
        return date

    latest_date = get_most_recent_common_date(default_date)
    return latest_date


class AssetPositionPandasFilter(DateFilterMixin, PandasFilterSetMixin, wb_filters.FilterSet):
    # price_start = wb_filters.NumberFilter(label="Price Start")
    # price_end = wb_filters.NumberFilter(label="Price End")

    date = total_value_fx_usd = total_value_fx_usd__gte = total_value_fx_usd__lte = None

    date = wb_filters.FinancialPerformanceDateRangeFilter(
        method=wb_filters.DateRangeFilter.base_date_range_filter_method,
        label="Date Range",
        required=True,
        clearable=False,
        default=current_financial_month,
    )

    group_by = wb_filters.ChoiceFilter(
        label="Group By",
        choices=GroupbyChoice.choices,
        default=GroupbyChoice.UNDERLYING_INSTRUMENT,
        method="fake_filter",
        clearable=False,
        required=True,
    )

    groupby_classification_height = wb_filters.NumberFilter(
        method="fake_filter", label="Classification Height (groupby)", default=0, clearable=False, required=True
    )

    class Meta:
        model = AssetPosition
        fields = {
            # "price_start" : ["gte", "exact", "lte"],
            # "price_end" : ["gte", "exact", "lte"],
            "underlying_instrument": ["exact"],
            "portfolio": ["exact"],
            "currency": ["exact"],
            "exchange": ["exact"],
        }
        df_fields = {
            "total_value_start__gte": wb_filters.NumberFilter(
                precision=1, label="Total Value Start", lookup_expr="gte", field_name="total_value_start"
            ),
            "total_value_end__gte": wb_filters.NumberFilter(
                precision=1, label="Total Value End", lookup_expr="gte", field_name="total_value_end"
            ),
            "allocation_start__gte": wb_filters.NumberFilter(
                precision=2, label="Weighting Start", lookup_expr="gte", field_name="allocation_start"
            ),
            "allocation_end__gte": wb_filters.NumberFilter(
                precision=2, label="Weighting End", lookup_expr="gte", field_name="allocation_end"
            ),
            "performance_total__gte": wb_filters.NumberFilter(
                precision=2, label="Total Performance", lookup_expr="gte", field_name="performance_total"
            ),
            "contribution_total__gte": wb_filters.NumberFilter(
                precision=2, label="Total Contribution", lookup_expr="gte", field_name="contribution_total"
            ),
            "performance_forex__gte": wb_filters.NumberFilter(
                precision=2, label="Forex Performance", lookup_expr="gte", field_name="performance_forex"
            ),
            "contribution_forex__gte": wb_filters.NumberFilter(
                precision=2, label="Forex  Contribution", lookup_expr="gte", field_name="contribution_forex"
            ),
            "market_share__gte": wb_filters.NumberFilter(
                precision=2, label="Market Shares", lookup_expr="gte", field_name="market_share"
            ),
            "total_value_start__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="total_value_start", precision=1, label="Total Value Start"
            ),
            "total_value_end__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="total_value_end", precision=1, label="Total Value End"
            ),
            "allocation_start__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="allocation_start", precision=2, label="Weighting Start"
            ),
            "allocation_end__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="allocation_end", precision=2, label="Weighting End"
            ),
            "performance_total__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="performance_total", precision=2, label="Total Performance"
            ),
            "contribution_total__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="contribution_total", precision=2, label="Total Contribution"
            ),
            "performance_forex__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="performance_forex", precision=2, label="Forex Performance"
            ),
            "contribution_forex__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="contribution_forex", precision=2, label="Forex  Contribution"
            ),
            "market_share__lte": wb_filters.NumberFilter(
                lookup_expr="lte", field_name="market_share", precision=2, label="Market Shares"
            ),
        }


class AggregatedAssetPositionLiquidityFilter(PandasFilterSetMixin, wb_filters.FilterSet):
    historic_date = wb_filters.DateFilter(
        label="Historic Date",
        method=lambda queryset, label, value: queryset,
        default=get_latest_date_based_on_multiple_models,
        required=True,
    )
    compared_date = wb_filters.DateFilter(
        label="Compared Date",
        method=lambda queryset, label, value: queryset,
        default=get_latest_end_quarter_date_asset_position,
        required=True,
    )
    bigger_than_x = wb_filters.NumberFilter(
        label="Bigger Than..", method=lambda queryset, label, value: queryset, default=1.00, required=True, precision=2
    )

    class Meta:
        model = AssetPosition
        fields = {}
