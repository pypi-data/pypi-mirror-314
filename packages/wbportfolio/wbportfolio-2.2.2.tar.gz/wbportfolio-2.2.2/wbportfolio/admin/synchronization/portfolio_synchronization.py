from django.contrib import admin
from wbportfolio.models import PortfolioSynchronization

from .admin import SynchronizationAdmin


@admin.register(PortfolioSynchronization)
class PortfolioSynchronizationModelAdmin(SynchronizationAdmin):
    fieldsets = (
        *SynchronizationAdmin.fieldsets,
        (
            "Synchronization",
            {
                "fields": ("import_path", "dependent_task", "is_automatic_validation"),
                "classes": ("extrapretty", "wide"),
            },
        ),
    )
