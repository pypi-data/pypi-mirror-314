from django.contrib import admin
from wbportfolio.models import PriceComputation

from .admin import SynchronizationAdmin


@admin.register(PriceComputation)
class PriceComputationModelAdmin(SynchronizationAdmin):
    fieldsets = (
        *SynchronizationAdmin.fieldsets,
        (
            "Synchronization",
            {
                "fields": (
                    "import_path",
                    "dependent_task",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
    )
