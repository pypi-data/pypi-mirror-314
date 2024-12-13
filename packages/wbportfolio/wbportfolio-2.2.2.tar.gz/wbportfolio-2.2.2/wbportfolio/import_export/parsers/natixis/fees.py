import pandas as pd
from pandas.tseries.offsets import BDay

from .utils import file_name_parse

FIELD_MAP = {
    "Date": "transaction_date",
    "Manag. Fees Natixis": "ISSUER",
    "Manag. Fees Client": "MANAGEMENT",
    "Perf fees amount": "PERFORMANCE"
    # "Currency": "currency"
}


def parse(import_source):
    # Parse the Parts of the filename into the different parts
    parts = file_name_parse(import_source.file.name)
    # Get the valuation date and investment from the parts list
    parts["valuation_date"]
    product = parts["product"]

    df = pd.read_csv(import_source.file, encoding="utf-8", delimiter=";")
    df = df.rename(columns=FIELD_MAP)
    df = df.drop(columns=df.columns.difference(FIELD_MAP.values()))
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True)

    # Switch the weeekend day fees to the next monday
    df["transaction_date"] = df["transaction_date"].apply(lambda x: x + BDay(1) if x.weekday() in [5, 6] else x)

    # Ensure float columns are number
    for col in ["MANAGEMENT", "ISSUER", "PERFORMANCE"]:
        df[col] = df[col].astype("str").str.replace(" ", "").astype("float")

    # Groupby and sum similar fees (e.g. Monday)
    df = df.groupby("transaction_date").sum().reset_index()
    df = pd.melt(
        df,
        id_vars=["transaction_date"],
        value_vars=["MANAGEMENT", "ISSUER", "PERFORMANCE"],
        var_name="transaction_subtype",
        value_name="total_value",
    )
    df = df[df["total_value"] != 0]

    df["portfolio"] = product.primary_portfolio.id
    df["linked_product"] = product.id
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
    df["calculated"] = False
    df["total_value_gross"] = df["total_value"]
    df["total_value_fx_portfolio"] = df["total_value"]
    df["total_value_gross_fx_portfolio"] = df["total_value"]

    return {"data": df.to_dict("records")}
