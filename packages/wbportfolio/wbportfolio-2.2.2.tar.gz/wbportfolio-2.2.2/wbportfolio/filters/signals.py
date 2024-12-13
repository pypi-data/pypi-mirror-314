from datetime import date

from django.db.models import Exists, OuterRef
from django.dispatch import receiver
from wbcore import filters as wb_filters
from wbcore.contrib.directory.filters import CompanyFilter
from wbcore.signals.filters import add_filters
from wbfdm.filters import BaseClassifiedInstrumentFilterSet, ClassificationFilter
from wbfdm.models import InstrumentClassificationThroughModel
from wbportfolio.models import AssetPosition, Portfolio


@receiver(add_filters, sender=CompanyFilter)
def add_bank_product_filter(sender, request=None, *args, **kwargs):
    def method_bank(queryset, name, value):
        if value is True:
            return queryset.filter(issues_products__isnull=False).distinct()
        elif value is False:
            return queryset.filter(issues_products__isnull=True).distinct()
        return queryset

    return {
        "bank_product": wb_filters.BooleanFilter(
            field_name="bank_product",
            label="Is a Bank",
            help_text="Filter for companies that are a bank and serve as the custodian of a product in the PMS",
            method=method_bank,
        )
    }


@receiver(add_filters, sender=ClassificationFilter)
def add_portfolio_filter(sender, request=None, *args, **kwargs):
    def _filter_portfolio(queryset, name, value):
        if value:
            try:
                last_position_date = value.assets.latest("date").date
            except AssetPosition.DoesNotExist:
                last_position_date = (
                    AssetPosition.objects.latest("date").date if AssetPosition.objects.exists() else date.today()
                )
            invested_instruments = AssetPosition.get_invested_instruments(last_position_date, portfolio=value)
            rels = InstrumentClassificationThroughModel.objects.filter(
                instrument__in=invested_instruments.values("root")
            )
            return queryset.filter(id__in=rels.values("classification"))
        return queryset

    def _filter_invested(queryset, name, value):
        if value:
            last_position_date = (
                AssetPosition.objects.latest("date").date if AssetPosition.objects.exists() else date.today()
            )
            invested_instruments = AssetPosition.get_invested_instruments(last_position_date)
            rels = InstrumentClassificationThroughModel.objects.filter(
                instrument__in=invested_instruments.values("root")
            )
            return queryset.filter(id__in=rels.values("classification"))
        return queryset

    return {
        "portfolio": wb_filters.ModelChoiceFilter(
            label="Associated Portfolio",
            queryset=Portfolio.objects.all(),
            endpoint=Portfolio.get_representation_endpoint(),
            value_key=Portfolio.get_representation_value_key(),
            label_key=Portfolio.get_representation_label_key(),
            method=_filter_portfolio,
        ),
        "only_invested": wb_filters.BooleanFilter(
            label="Only invested instruments (anytime)",
            method=_filter_invested,
        ),
    }


@receiver(add_filters, sender=BaseClassifiedInstrumentFilterSet)
def add_classification_instrument_filter(sender, request=None, *args, **kwargs):
    def _filter_invested(queryset, name, value):
        if value:
            last_invested_date = (
                AssetPosition.objects.latest("date").date if AssetPosition.objects.exists() else date.today()
            )
            invested_instruments = AssetPosition.get_invested_instruments(last_invested_date)
            return queryset.filter(Exists(invested_instruments.filter(root=OuterRef("instrument"))))
        return queryset

    return {
        "only_invested": wb_filters.BooleanFilter(
            method=_filter_invested, label="Invested Instruments (last date)", default=False
        )
    }
