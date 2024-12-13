from wbcore import serializers as wb_serializers
from wbcore.contrib.currency.serializers import CurrencyRepresentationSerializer
from wbfdm.serializers.instruments import InvestableInstrumentRepresentationSerializer
from wbportfolio.models import Transaction
from wbportfolio.serializers.portfolios import PortfolioRepresentationSerializer


class TransactionRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbportfolio:transaction-detail")

    class Meta:
        model = Transaction
        fields = ("id", "transaction_date", "total_value", "_detail")


class TransactionModelSerializer(wb_serializers.ModelSerializer):
    external_id = wb_serializers.CharField(required=False, read_only=True)
    value_date = wb_serializers.DateField(required=False, read_only=True)
    total_value_usd = wb_serializers.FloatField(default=0, read_only=True, label="Total Value ($)")
    total_value_gross_usd = wb_serializers.FloatField(default=0, read_only=True, label="Total Value Gross ($)")
    transaction_underlying_type = wb_serializers.CharField(read_only=True)
    transaction_url_type = wb_serializers.SerializerMethodField()
    _portfolio = PortfolioRepresentationSerializer(source="portfolio")
    _underlying_instrument = InvestableInstrumentRepresentationSerializer(source="underlying_instrument")
    _currency = CurrencyRepresentationSerializer(source="currency")

    total_value = wb_serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    total_value_fx_portfolio = wb_serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    total_value_gross = wb_serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    total_value_gross_fx_portfolio = wb_serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    def get_transaction_url_type(self, obj):
        return obj.transaction_type.lower()

    # def get_transaction_underlying_type(self, obj):
    #     try:
    #         casted_transaction = obj.get_casted_transaction()
    #         return casted_transaction.Type[casted_transaction.transaction_subtype].label
    #     except Exception as e:
    #         return ""
    class Meta:
        model = Transaction
        decorators = {
            "total_value": wb_serializers.decorator(
                decorator_type="text", position="left", value="{{_currency.symbol}}"
            ),
            "total_value_gross": wb_serializers.decorator(
                decorator_type="text", position="left", value="{{_currency.symbol}}"
            ),
            "total_value_usd": wb_serializers.decorator(decorator_type="text", position="left", value="{{$}}"),
            "total_value_gross_usd": wb_serializers.decorator(decorator_type="text", position="left", value="{{$}}"),
            "total_value_fx_portfolio": wb_serializers.decorator(
                position="left", value="{{_portfolio.currency_symbol}}"
            ),
            "total_value_gross_fx_portfolio": wb_serializers.decorator(
                position="left", value="{{_portfolio.currency_symbol}}"
            )
            # "total_value_fx_portfolio": wb_serializers.decorator(decorator_type="text", position="left", value="{{_portfolio.currency_symbol}}}"),
            # "total_value_gross_fx_portfolio": wb_serializers.decorator(decorator_type="text", position="left", value="{{_portfolio.currency_symbol}}"),
        }
        fields = (
            "id",
            "transaction_type",
            "transaction_url_type",
            "transaction_underlying_type",
            "portfolio",
            "_portfolio",
            "underlying_instrument",
            "_underlying_instrument",
            "transaction_date",
            "book_date",
            "value_date",
            "currency",
            "_currency",
            "currency_fx_rate",
            "total_value",
            "total_value_fx_portfolio",
            "total_value_gross",
            "total_value_gross_fx_portfolio",
            "external_id",
            "comment",
            "total_value_usd",
            "total_value_gross_usd",
        )
