from wbcore import serializers as wb_serializers
from wbportfolio.models import PortfolioSynchronization, PriceComputation


class PortfolioSynchronizationRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:portfolio-detail")

    class Meta:
        model = PortfolioSynchronization
        fields = ("id", "name", "import_path", "_detail")


class PriceComputationRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:portfolio-detail")

    class Meta:
        model = PriceComputation
        fields = ("id", "name", "import_path", "_detail")
