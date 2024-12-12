from django.db import models
from wbportfolio.import_export.handlers.dividend import DividendImportHandler

from .transactions import ShareMixin, Transaction


class DividendTransaction(Transaction, ShareMixin, models.Model):
    import_export_handler_class = DividendImportHandler
    retrocession = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        if (
            self.shares is not None
            and self.price is not None
            and self.retrocession is not None
            and self.total_value is None
        ):
            self.total_value = self.shares * self.price * self.retrocession

        if self.price is not None and self.price_gross is None:
            self.price_gross = self.price

        if (
            self.price_gross is not None
            and self.retrocession is not None
            and self.shares is not None
            and self.total_value_gross is None
        ):
            self.total_value_gross = self.shares * self.price_gross * self.retrocession

        super().save(*args, **kwargs)
