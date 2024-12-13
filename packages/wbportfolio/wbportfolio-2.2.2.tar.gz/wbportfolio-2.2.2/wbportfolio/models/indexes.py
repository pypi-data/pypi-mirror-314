from django.db import models
from wbfdm.models.instruments import InstrumentType

from .mixins.instruments import PMSInstrument


class Index(PMSInstrument):
    price_computation = models.ForeignKey(
        "wbportfolio.PriceComputation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="indexes",
        verbose_name="Price Computation Method",
    )
    risk_scale = models.PositiveIntegerField(null=True, blank=True, verbose_name="Risk Scale")

    def pre_save(self):
        super().pre_save()
        self.instrument_type = InstrumentType.INDEX
        if "market_data" not in self.dl_parameters:
            # we default to the internal dataloader
            self.dl_parameters["market_data"] = {
                "path": "wbfdm.contrib.internal.dataloaders.market_data.MarketDataDataloader"
            }
        self.is_managed = True

    class Meta:
        verbose_name = "Index"
        verbose_name_plural = "Indexes"

    def compute_str(self):
        return f"{self.name}  ({self.ticker} - {self.isin})"
