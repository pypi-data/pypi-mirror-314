from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse
from wbcore import serializers as wb_serializers
from wbcore.contrib.currency.serializers import CurrencyRepresentationSerializer
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.buttons.view_config import ButtonViewConfig
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbportfolio.models import Portfolio, PriceComputation
from wbportfolio.serializers import (
    PortfolioSynchronizationRepresentationSerializer,
    PriceComputationRepresentationSerializer,
)


def get_portfolio_start_end_serializer_class(portfolio):
    today = date.today()

    class StartEndDateSerializer(wb_serializers.Serializer):
        start = wb_serializers.DateField(
            label="Start",
            default=portfolio.assets.earliest("date").date if portfolio.assets.exists() else today,
        )
        end = wb_serializers.DateField(
            label="End", default=portfolio.assets.latest("date").date if portfolio.assets.exists() else today
        )

    return StartEndDateSerializer


class PortfolioButtonConfig(ButtonViewConfig):
    def get_custom_instance_buttons(self):
        portfolio_buttons = [
            bt.WidgetButton(key="assets", label="Assets"),
            bt.WidgetButton(key="contributor", label="Contributor"),
            bt.WidgetButton(key="distribution_chart", label="Distribution Chart"),
            bt.WidgetButton(key="distribution_table", label="Distribution Table"),
            bt.WidgetButton(key="modelcomposition", label="Portfolio Composition vs. Dependant Portfolios"),
        ]
        if pk := self.view.kwargs.get("pk", None):
            portfolio = get_object_or_404(Portfolio, pk=pk)

            portfolio_buttons.append(
                bt.ActionButton(
                    method=RequestType.PATCH,
                    identifiers=("wbportfolio:portfolio",),
                    key="resynchronize",
                    label="Resynchronize/Rebalance",
                    description_fields="""
                    <p>Resynchronize portfolio from {{start}} to {{end}}</p>
                    """,
                    serializer=get_portfolio_start_end_serializer_class(portfolio),
                    action_label="resynchronize",
                    title="Resynchronize/Rebalance",
                    instance_display=create_simple_display([["start"], ["end"]]),
                )
            )

        return {
            bt.DropDownButton(label="Portfolio", icon=WBIcon.UNFOLD.icon, buttons=tuple(portfolio_buttons)),
        }

    def get_custom_list_instance_buttons(self):
        return self.get_custom_instance_buttons()


class CreateModelPortfolioSerializer(wb_serializers.ModelSerializer):
    create_index = wb_serializers.BooleanField(default=False, label="Create Underlying Index")
    name = wb_serializers.CharField(required=True)
    _currency = CurrencyRepresentationSerializer(source="currency")
    _portfolio_synchronization = PortfolioSynchronizationRepresentationSerializer(source="portfolio_synchronization")
    price_computation = wb_serializers.PrimaryKeyRelatedField(queryset=PriceComputation.objects.all(), required=False)
    _price_computation = PriceComputationRepresentationSerializer(source="price_computation")

    class Meta:
        model = Portfolio
        dependency_map = {
            "price_computation": ["create_index"],
        }
        fields = (
            "name",
            "currency",
            "portfolio_synchronization",
            "create_index",
            "price_computation",
            "_price_computation",
            "_currency",
            "_portfolio_synchronization",
        )


class ModelPortfolioButtonConfig(PortfolioButtonConfig):
    # pass
    def get_custom_buttons(self):
        if not self.view.kwargs.get("pk", None):
            return {
                bt.ActionButton(
                    method=RequestType.POST,
                    identifiers=("wbportfolio:portfolio",),
                    endpoint=reverse("wbportfolio:modelportfolio-createmodelportfolio", request=self.request),
                    label="Create New Model Portfolio",
                    serializer=CreateModelPortfolioSerializer,
                    action_label="create",
                    title="Create Model Portfolio",
                    instance_display=create_simple_display(
                        [["name", "currency", "portfolio_synchronization"], ["create_index", "price_computation", "."]]
                    ),
                )
            }
        return set()
