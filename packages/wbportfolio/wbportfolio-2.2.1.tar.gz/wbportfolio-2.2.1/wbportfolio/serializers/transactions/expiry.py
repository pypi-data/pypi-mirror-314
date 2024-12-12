from wbportfolio.models import Expiry

from .transactions import (
    TransactionModelSerializer,
    TransactionRepresentationSerializer,
)


class ExpiryRepresentationSerializer(TransactionRepresentationSerializer):
    class Meta:
        model = Expiry
        fields = TransactionRepresentationSerializer.Meta.fields


class ExpiryModelSerializer(TransactionModelSerializer):
    class Meta:
        model = Expiry
        fields = TransactionModelSerializer.Meta.fields
