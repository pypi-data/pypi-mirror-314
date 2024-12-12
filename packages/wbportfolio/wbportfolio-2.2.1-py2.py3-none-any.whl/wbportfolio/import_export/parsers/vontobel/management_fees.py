import re
from datetime import datetime

import pandas as pd
from wbportfolio.models import FeeProductPercentage, Fees

from .utils import get_portfolio_id, get_product

FIELD_MAP = {
    "Transaction_Date": "transaction_date",
    "Trade_Date": "book_date",
    "Value_Date": "value_date",
    "Quantity": "total_value",
    "Currency": "currency__key",
    "Portfolio_Identifier": "linked_product",
    "Booking_Comment": "comment",
}


def parse(import_source):
    df = pd.read_csv(import_source.file, encoding="utf-16", delimiter=";")
    df = df.loc[(df["Order_Type"] == "xfermon_client") & (df["Bookkind"] == "forex_impl_macc"), :]
    date_range_regex = import_source.source.import_parameters.get(
        "date_range_regex", r"\((\b\d{2}\.\d{2}\.\d{4}\b) to (\b\d{2}\.\d{2}\.\d{4}\b)\)"
    )
    data = []
    if not df.empty:
        df = df.rename(columns=FIELD_MAP)
        df.linked_product = df.linked_product.apply(lambda x: get_product(x))
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True)
        df["book_date"] = pd.to_datetime(df["book_date"], dayfirst=True).dt.strftime("%Y-%m-%d")
        df["value_date"] = pd.to_datetime(df["value_date"], dayfirst=True).dt.strftime("%Y-%m-%d")
        df["portfolio"] = df.linked_product.apply(lambda x: get_portfolio_id(x))
        df["base_management_fees"] = df.apply(
            lambda row: float(
                row["linked_product"].get_fees_percent(row["transaction_date"], FeeProductPercentage.Type.MANAGEMENT)
            ),
            axis=1,
        )
        df["base_bank_fees"] = df.apply(
            lambda row: float(
                row["linked_product"].get_fees_percent(row["transaction_date"], FeeProductPercentage.Type.BANK)
            ),
            axis=1,
        )
        df.total_value = -df.total_value

        df_management = df.copy()
        df_management["transaction_subtype"] = Fees.Type.MANAGEMENT
        df_management["total_value"] = (
            df_management["total_value"]
            * df_management["base_management_fees"]
            / (df_management["base_management_fees"] + df_management["base_bank_fees"])
        )

        df_bank = df.copy()
        df_bank["transaction_subtype"] = Fees.Type.ISSUER
        df_bank["total_value"] = (
            df_bank["total_value"]
            * df_bank["base_bank_fees"]
            / (df_bank["base_management_fees"] + df_bank["base_bank_fees"])
        )

        df = pd.concat([df_management, df_bank], axis=0)
        df = df.drop(columns=df.columns.difference(["transaction_subtype", *FIELD_MAP.values()]))

        df["linked_product"] = df.linked_product.apply(lambda x: x.id)
        df = df.dropna(subset=["linked_product"])

        for row in df.to_dict("records"):
            # The fee are sometime aggregated. The aggregate date range information is given in the comment. We therefore try to extract it and duplicate the averaged fees
            if match := re.search(date_range_regex, row["comment"]):
                from_date = datetime.strptime(match.group(1), "%d.%m.%Y").date()
                to_date = datetime.strptime(match.group(2), "%d.%m.%Y").date()
            else:
                from_date = (row["transaction_date"] - pd.tseries.offsets.BDay(1)).date()
                to_date = row["transaction_date"]

            dates = pd.date_range(from_date, to_date, freq="B", inclusive="right")
            for ts in pd.date_range(from_date, to_date, freq="B", inclusive="right"):
                row_copy = row.copy()
                row_copy["transaction_date"] = ts.strftime("%Y-%m-%d")
                row_copy["total_value"] = row["total_value"] / len(dates)
                data.append(row_copy)

    return {"data": data}
