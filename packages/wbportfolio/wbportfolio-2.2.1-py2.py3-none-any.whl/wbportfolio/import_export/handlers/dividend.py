import math
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from django.db import models
from wbcore.contrib.currency.import_export.handlers import CurrencyImportHandler
from wbcore.contrib.io.exceptions import DeserializationError
from wbcore.contrib.io.imports import ImportExportHandler
from wbfdm.import_export.handlers.instrument import InstrumentImportHandler


class DividendImportHandler(ImportExportHandler):
    MODEL_APP_LABEL = "wbportfolio.DividendTransaction"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument_handler = InstrumentImportHandler(self.import_source)
        self.currency_handler = CurrencyImportHandler(self.import_source)

    def _deserialize(self, data):
        data["transaction_date"] = datetime.strptime(data["transaction_date"], "%Y-%m-%d").date()
        data["value_date"] = datetime.strptime(data["value_date"], "%Y-%m-%d").date()
        from wbportfolio.models import Portfolio

        data["portfolio"] = Portfolio.objects.get(id=data["portfolio"])
        instrument = self.instrument_handler.process_object(
            data["underlying_instrument"], only_security=False, read_only=True
        )[0]
        if not instrument:
            raise DeserializationError("Can't process this data: underlying instrument not found")
        data["underlying_instrument"] = instrument
        if "currency" not in data:
            data["currency"] = data["portfolio"].currency
        else:
            data["currency"] = self.currency_handler.process_object(data["currency"], read_only=True)[0]

        for field in self.model._meta.get_fields():
            if not (value := data.get(field.name, None)) is None and isinstance(field, models.DecimalField):
                q = 1 / (math.pow(10, 4))
                data[field.name] = Decimal(value).quantize(Decimal(str(q)))

    def _get_instance(self, data, history=None, **kwargs):
        self.import_source.log += "\nGet DividendTransaction Instance."
        self.import_source.log += f"\nParameter: Portfolio={data['portfolio']} Underlying={data['underlying_instrument']} Date={data['transaction_date']}"
        dividends = history if history is not None else self.model.objects

        dividends = dividends.filter(
            portfolio=data["portfolio"],
            transaction_date=data["transaction_date"],
            value_date=data["value_date"],
            underlying_instrument=data["underlying_instrument"],
            price_gross=data["price_gross"],
        )
        if dividends.count() == 1:
            self.import_source.log += "\nDividendTransaction Instance Found." ""
            return dividends.first()

    def _create_instance(self, data, **kwargs):
        self.import_source.log += "\nCreate DividendTransaction."
        return self.model.objects.create(**data, import_source=self.import_source)

    def _get_history(self: models.Model, history: Dict[str, Any]) -> models.QuerySet:
        val_date = datetime.strptime(history["transaction_date"], "%Y-%m-%d")
        if portfolio_id := history.get("portfolio", None):
            dividends = self.model.objects.filter(transaction_date__lte=val_date, portfolio=portfolio_id)
            if underlying_instrument_id := history.get("underlying_instrument", None):
                dividends = dividends.filter(underlying_instrument=underlying_instrument_id)
            return dividends

    def _post_processing_history(self: models.Model, history: models.QuerySet):
        self.import_source.log += "===================="
        self.import_source.log += (
            "It was a historical import and the following DividendTransaction have to be deleted:"
        )
        for dividend in history.order_by("transaction_date"):
            self.import_source.log += (
                f"\n{dividend.transaction_date:%d.%m.%Y}: {dividend.shares} {dividend.price} ==> Deleted"
            )
            dividend.delete()
