from django.contrib import admin
from wbportfolio.admin.transactions import TransactionModelAdmin
from wbportfolio.models import Trade, TradeProposal


@admin.register(Trade)
class TradeAdmin(TransactionModelAdmin):
    search_fields = [*TransactionModelAdmin.search_fields, "bank"]
    list_filter = (*TransactionModelAdmin.list_filter, "pending")
    list_display = (
        "transaction_subtype",
        "status",
        "shares",
        "price",
        "pending",
        "marked_for_deletion",
        "exclude_from_history",
        *TransactionModelAdmin.list_display[1:],
    )
    readonly_fields = [
        "_effective_weight",
        "_target_weight",
        "_effective_shares",
        "_target_shares",
    ]
    fieldsets = (
        ("Transaction Information", TransactionModelAdmin.fieldsets[0][1]),
        (
            "Trade Information",
            {
                "fields": (
                    ("transaction_subtype", "status", "pending", "marked_for_deletion", "exclude_from_history"),
                    ("price", "price_gross"),
                    ("register", "custodian", "bank", "external_identifier2"),
                    ("_effective_weight", "_target_weight", "weighting"),
                    ("_effective_shares", "_target_shares", "shares"),
                )
            },
        ),
    )
    autocomplete_fields = [*TransactionModelAdmin.autocomplete_fields, "register", "custodian"]


@admin.register(TradeProposal)
class TradeProposalAdmin(admin.ModelAdmin):
    search_fields = ["portfolio__name", "model_portfolio__name", "comment"]

    list_display = ("portfolio", "model_portfolio", "trade_date", "status")
    autocomplete_fields = ["portfolio", "model_portfolio"]
