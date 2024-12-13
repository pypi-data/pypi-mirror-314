from django.contrib import admin
from django.db.models import Prefetch
from wbportfolio.admin.transactions import TransactionModelAdmin
from wbportfolio.models import Fees, Portfolio
from wbportfolio.models.transactions.fees import FeeCalculation


@admin.register(Fees)
class FeesAdmin(TransactionModelAdmin):
    list_filter = [*TransactionModelAdmin.list_filter, "linked_product"]
    list_display = ["transaction_subtype", *TransactionModelAdmin.list_display[1:], "calculated"]
    fieldsets = (
        ("Transaction Information", TransactionModelAdmin.fieldsets[0][1]),
        ("Fees Information", {"fields": (("transaction_subtype", "calculated", "linked_product"),)}),
    )
    autocomplete_fields = [*TransactionModelAdmin.autocomplete_fields, "linked_product"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(Prefetch("portfolio", queryset=Portfolio.objects.all().only("id", "name")))
        )

    def calculate(self, request, queryset):
        for fees in queryset:
            fees.calculate_as_task.delay(fees)

    calculate.short_description = "Recalculate selected Fees"
    actions = [calculate]


@admin.register(FeeCalculation)
class FeeCalculationModelAdmin(admin.ModelAdmin):
    search_fields = ("name",)
