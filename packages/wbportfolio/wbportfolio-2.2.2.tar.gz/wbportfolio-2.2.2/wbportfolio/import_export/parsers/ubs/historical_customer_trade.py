from io import BytesIO
from typing import Dict

import pandas as pd
from wbcore.contrib.io.models import ImportSource
from wbportfolio.models import Product, Trade


def parse_row(obj: Dict, import_source: ImportSource) -> Dict:
    if _id := obj["underlying_instrument_id"]:
        product = Product.objects.get(id=_id)
        shares = -1 * obj["shares"]
        portfolio = product.primary_portfolio
        return {
            "underlying_instrument": {"id": product.id, "instrument_type": "product"},
            "currency__key": product.currency.key,
            "portfolio": portfolio.id,
            "transaction_date": obj["transaction_date"].strftime("%Y-%m-%d"),
            "shares": shares,
            "bank": obj["custodian"] if obj["custodian"] else "NA",
            "transaction_subtype": Trade.Type.REDEMPTION if shares < 0 else Trade.Type.SUBSCRIPTION,
            "price": round(obj["price"], 6),
        }


def parse(import_source):
    def _get_underlying_instrument_id(isin):
        try:
            product = Product.objects.get(isin=isin)
            return product.id
        except Product.DoesNotExist:
            import_source.log += f"Product with ISIN {isin} does not exists."

            return None

    df_dict = pd.read_excel(BytesIO(import_source.file.read()), engine="openpyxl")
    df_dict = df_dict.rename(
        columns={
            "Trade Date": "transaction_date",
            "ISIN": "underlying_instrument__isin",
            "Client Side": "client_side",
            "Net Quantity": "shares",
            "Price": "price",
            "Custodian": "custodian",
        }
    )
    df_dict = df_dict.where(pd.notnull(df_dict), None)
    df_dict["transaction_date"] = pd.to_datetime(df_dict["transaction_date"])
    df_dict["underlying_instrument__isin"] = df_dict["underlying_instrument__isin"].str.strip()
    df_dict["underlying_instrument_id"] = df_dict["underlying_instrument__isin"].apply(
        lambda x: _get_underlying_instrument_id(x)
    )

    data = list()
    for d in df_dict.to_dict("records"):
        parsed_row = parse_row(d, import_source)
        if parsed_row:
            data.append(parse_row(d, import_source))
    underlying_instruments = [int(_id) for _id in df_dict.underlying_instrument_id.astype("int").unique()]

    return {
        "data": data,
        "history": {
            "underlying_instruments": underlying_instruments,
            "transaction_date": df_dict.transaction_date.max().strftime("%Y-%m-%d"),
        },
    }
