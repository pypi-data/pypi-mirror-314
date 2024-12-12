import json

import pandas as pd
from wbportfolio.models import Fees, Product

BASE_MAPPING = {"managementFee": "total_value", "performanceFee": "total_value", "date": "transaction_date"}


def parse(import_source):
    def _process_df(df, product):
        df = df.rename(columns=BASE_MAPPING).dropna(how="all", axis=1)
        df = df.drop(columns=df.columns.difference(BASE_MAPPING.values()))
        df["currency__key"] = product.currency.key
        df["linked_product"] = product.id
        df["underlying_instrument"] = product.id
        df["portfolio"] = product.primary_portfolio.id
        return df

    content = json.load(import_source.file)
    data = []
    if product := Product.objects.filter(isin=content.get("isin", None)).first():
        if mngt_data := content.get("management_fees", None):
            df = _process_df(pd.DataFrame(mngt_data), product)
            df["transaction_subtype"] = Fees.Type.MANAGEMENT.value
            data.extend(df.to_dict("records"))
        if perf_data := content.get("performance_fees", None):
            df = _process_df(pd.DataFrame(perf_data), product)
            df["transaction_subtype"] = Fees.Type.PERFORMANCE.value
            data.extend(df.to_dict("records"))

    return {"data": data}
