from wbcore import filters as wb_filters
from wbfdm.models import Instrument
from wbportfolio.models import Portfolio


class PortfolioFilterSet(wb_filters.FilterSet):
    instrument = wb_filters.ModelChoiceFilter(
        label="Instrument",
        queryset=Instrument.objects.all(),
        endpoint=Instrument.get_representation_endpoint(),
        value_key=Instrument.get_representation_value_key(),
        label_key=Instrument.get_representation_label_key(),
        filter_params={"is_managed": True},
        method="filter_instrument",
    )

    def filter_instrument(self, queryset, name, value):
        if value:
            return queryset.filter(instruments=value)
        return queryset

    class Meta:
        model = Portfolio
        fields = {"currency": ["exact"], "is_manageable": ["exact"]}
