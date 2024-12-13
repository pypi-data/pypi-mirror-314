from wbportfolio.models import DividendTransaction

from .transactions import (
    TransactionModelSerializer,
    TransactionRepresentationSerializer,
)


class DividendRepresentationSerializer(TransactionRepresentationSerializer):
    class Meta:
        model = DividendTransaction
        fields = TransactionRepresentationSerializer.Meta.fields


class DividendModelSerializer(TransactionModelSerializer):
    class Meta:
        model = DividendTransaction
        fields = TransactionModelSerializer.Meta.fields
