from django.contrib import admin
from wbportfolio.models import Transaction


@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    search_fields = ["portfolio__name", "underlying_instrument__computed_str"]
    list_filter = ("transaction_type", "portfolio")
    list_display = (
        "transaction_type",
        "portfolio",
        "underlying_instrument",
        "transaction_date",
        "currency",
        "currency_fx_rate",
        "total_value",
        "total_value_fx_portfolio",
        "import_source",
    )
    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    ("portfolio", "underlying_instrument", "transaction_type", "import_source", "external_id"),
                    ("transaction_date", "book_date", "value_date"),
                    ("currency", "currency_fx_rate"),
                    ("total_value", "total_value_gross"),
                    ("total_value_fx_portfolio", "total_value_gross_fx_portfolio"),
                    "comment",
                )
            },
        ),
    )
    autocomplete_fields = ["portfolio", "underlying_instrument", "currency"]
    ordering = ("-transaction_date",)
    raw_id_fields = ["import_source"]
