from django.contrib import admin
from wbportfolio.admin.transactions import TransactionModelAdmin
from wbportfolio.models import DividendTransaction


@admin.register(DividendTransaction)
class DividendAdmin(TransactionModelAdmin):
    fieldsets = (
        ("Transactions Information", TransactionModelAdmin.fieldsets[0][1]),
        (
            "Dividend Information",
            {"fields": (("retrocession",),)},
        ),
    )
