from datetime import datetime

from wbcore.contrib.currency.import_export.handlers import CurrencyImportHandler
from wbcore.contrib.io.imports import ImportExportHandler
from wbfdm.models.instruments import Cash
from wbportfolio.models.products import Product


class FeesImportHandler(ImportExportHandler):
    MODEL_APP_LABEL: str = "wbportfolio.Fees"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency_handler = CurrencyImportHandler(self.import_source)

    def _deserialize(self, data):
        data["transaction_date"] = datetime.strptime(data["transaction_date"], "%Y-%m-%d").date()
        data["fee_date"] = data["transaction_date"]
        if value_date_str := data.get("value_date", None):
            data["value_date"] = datetime.strptime(value_date_str, "%Y-%m-%d").date()
        if book_date_str := data.get("book_date", None):
            data["book_date"] = datetime.strptime(book_date_str, "%Y-%m-%d").date()

        from wbportfolio.models import Portfolio

        data["linked_product"] = Product.objects.get(id=data["linked_product"])
        if "porfolio" in data:
            data["portfolio"] = Portfolio.objects.get(id=data["portfolio"])
        else:
            data["portfolio"] = data["linked_product"].primary_portfolio
        data["underlying_instrument"] = Cash.objects.filter(currency=data["portfolio"].currency).first()
        if "currency" not in data:
            data["currency"] = data["portfolio"].currency
        else:
            data["currency"] = self.currency_handler.process_object(data["currency"], read_only=True)[0]
        data["currency_fx_rate"] = 1.0
        data["total_value"] = data.get("total_value", data.get("total_value_gross", None))
        data["total_value_gross"] = data.get("total_value_gross", data["total_value"])
        data["calculated"] = data.get("calculated", False)

    def _get_instance(self, data, history=None, **kwargs):
        self.import_source.log += "\nGet Fees Instance."
        self.import_source.log += f"\nParameter: Portfolio={data['portfolio']} Date={data['transaction_date']}"
        fees = self.model.objects.filter(
            linked_product=data["linked_product"],
            fee_date=data["fee_date"],
            transaction_subtype=data["transaction_subtype"],
            calculated=data["calculated"],
        )
        if fees.exists():
            if fees.count() > 1:
                raise ValueError(f'Number of similar fees found > 1: {fees.values_list("id", flat=True)}')
            self.import_source.log += "\nFees Instance Found." ""
            return fees.first()

    def _create_instance(self, data, **kwargs):
        self.import_source.log += "\nCreate Fees."
        return self.model.objects.create(**data, import_source=self.import_source)
