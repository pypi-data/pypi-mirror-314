from wbcore import serializers as wb_serializers
from wbportfolio.models import Fees

from .transactions import (
    TransactionModelSerializer,
    TransactionRepresentationSerializer,
)


class FeesRepresentationSerializer(TransactionRepresentationSerializer):
    class Meta:
        model = Fees
        fields = ("transaction_subtype",) + TransactionRepresentationSerializer.Meta.fields


class FeesModelSerializer(TransactionModelSerializer):
    @wb_serializers.register_resource()
    def additional_resources(self, instance, request, user):
        if (view := request.parser_context.get("view")) and view.is_manager and instance.import_source:
            return {"import_source": instance.import_source.file.url}
        return {}

    class Meta:
        model = Fees
        decorators = TransactionModelSerializer.Meta.decorators
        fields = (
            "_additional_resources",
            "transaction_subtype",
            "calculated",
            "fee_date",
            "linked_product",
        ) + TransactionModelSerializer.Meta.fields
