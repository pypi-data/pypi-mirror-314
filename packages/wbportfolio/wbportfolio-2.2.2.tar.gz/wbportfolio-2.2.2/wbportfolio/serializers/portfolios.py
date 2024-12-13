from rest_framework.reverse import reverse
from wbcore import serializers as wb_serializers
from wbcore.contrib.currency.serializers import CurrencyRepresentationSerializer
from wbcore.contrib.directory.models import BankingContact
from wbportfolio.models import Portfolio, PortfolioPortfolioThroughModel
from wbportfolio.serializers.synchronization import (
    PortfolioSynchronizationRepresentationSerializer,
)


class PortfolioRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:portfolio-detail")
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbportfolio:portfolio-detail")

    class Meta:
        model = Portfolio
        fields = ("id", "name", "_detail", "_detail_preview")


class PortfolioModelSerializer(wb_serializers.ModelSerializer):
    _currency = CurrencyRepresentationSerializer(source="currency")
    _depends_on = PortfolioRepresentationSerializer(source="depends_on", many=True)
    _portfolio_synchronization = PortfolioSynchronizationRepresentationSerializer(source="portfolio_synchronization")
    dependent_portfolios = wb_serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, label="Dependency Portfolios"
    )
    _dependent_portfolios = PortfolioSynchronizationRepresentationSerializer(many=True, source="dependent_portfolios")

    @wb_serializers.register_only_instance_resource()
    def cash_management(self, instance, request, user, **kwargs):
        additional_resources = dict()
        if instance.daily_cashflows.exists():
            additional_resources["daily_cashflows"] = reverse(
                "wbportfolio:portfolio-portfoliocashflow-list", args=[instance.id], request=request
            )
        b = BankingContact.objects.filter(wbportfolio_products__id__in=instance.instruments.all().values("id"))
        if b.exists():
            base_url = reverse("wbaccounting:futurecashflow-list", request=request)
            additional_resources[
                "cash_flow"
            ] = f'{base_url}?banking_contact={",".join([str(i) for i in b.distinct("id").values_list("id", flat=True)])}'

        return additional_resources

    @wb_serializers.register_only_instance_resource()
    def additional_resources(self, instance, request, user, **kwargs):
        additional_resources = dict()
        additional_resources["distribution_chart"] = reverse(
            "wbportfolio:portfolio-distributionchart-list", args=[instance.id], request=request
        )
        additional_resources["distribution_table"] = reverse(
            "wbportfolio:portfolio-distributiontable-list", args=[instance.id], request=request
        )
        if instance.assets.exists():
            additional_resources["assets"] = reverse(
                "wbportfolio:portfolio-asset-list", args=[instance.id], request=request
            )
            additional_resources["contributor"] = reverse(
                "wbportfolio:portfolio-contributor-list",
                args=[instance.id],
                request=request,
            )
        if user.profile.is_internal:
            additional_resources["instruments"] = reverse(
                "wbportfolio:portfolio-instrument-list",
                args=[instance.id],
                request=request,
            )

        if instance.portfolio_synchronization:
            additional_resources["resynchronize"] = reverse(
                "wbportfolio:portfolio-resynchronize",
                args=[instance.id],
                request=request,
            )
        additional_resources["dependencyportfolios"] = reverse(
            "wbportfolio:portfolio-dependencyportfolio-list",
            args=[instance.id],
            request=request,
        )
        additional_resources["trade_proposals"] = reverse(
            "wbportfolio:portfolio-tradeproposal-list",
            args=[instance.id],
            request=request,
        )

        additional_resources["preferredclassification"] = reverse(
            "wbportfolio:portfolio-preferredclassification-list",
            args=[instance.id],
            request=request,
        )
        additional_resources["modelcomposition"] = reverse(
            "wbportfolio:portfolio-modelcompositionpandas-list",
            args=[instance.id],
            request=request,
        )

        return additional_resources

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "last_synchronization",
            "_depends_on",
            "_portfolio_synchronization",
            "depends_on",
            "portfolio_synchronization",
            "_dependent_portfolios",
            "dependent_portfolios",
            "_currency",
            "currency",
            "_additional_resources",
        )


class ModelPortfolioModelSerializer(PortfolioModelSerializer):
    @wb_serializers.register_only_instance_resource()
    def rebalance(self, instance, request, user, **kwargs):
        return {
            "modelcomposition": reverse(
                "wbportfolio:portfolio-modelcompositionpandas-list",
                args=[instance.id],
                request=request,
            )
        }


class PortfolioPortfolioThroughModelSerializer(wb_serializers.ModelSerializer):
    _portfolio = PortfolioRepresentationSerializer(source="portfolio")
    _dependency_portfolio = PortfolioRepresentationSerializer(source="dependency_portfolio")

    class Meta:
        model = PortfolioPortfolioThroughModel
        fields = (
            "id",
            "_portfolio",
            "portfolio",
            "_dependency_portfolio",
            "dependency_portfolio",
            "type",
        )
