import numpy as np
import pandas as pd
from wbportfolio.models import Trade

from .utils import file_name_parse

UNVALID_CUSTODIANS = ["init"]

FIELD_MAP = {
    "Trade Date": "transaction_date",
    "Value Date": "value_date",
    "Counterparty": "bank",
    "Identifier": "external_id",
    "Note price in%": "price",
    "Nominal Increase/Decrease": "shares",
}


def _check_if_count_towards_total_aum(row, df):
    previous_accumulated_shares = row["Accumulated Nominal"] - row["shares"]
    dff = df[
        (df["transaction_date"] < row["transaction_date"]) & (df["Accumulated Nominal"] == previous_accumulated_shares)
    ]
    return not dff["shares"].sum() == row["shares"]


def parse(import_source):
    # Load file into a CSV DictReader
    df = pd.read_csv(import_source.file, encoding="utf-8", delimiter=";")
    df = df.rename(columns=FIELD_MAP)
    parts = file_name_parse(import_source.file.name)

    # Get the valuation date and product from the parts list
    valuation_date = parts["valuation_date"]
    product = parts["product"]

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    df["value_date"] = pd.to_datetime(df["value_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    df["bank"] = df["bank"].str.strip()
    df["shares"] = df["shares"] / product.share_price

    df["bank"] = df["bank"].fillna("<not specified>")

    # Use the accumulated nominal (outstanding shares) to detect internal natixis accounting trade that shouldn't be imported
    # If a trade is marked "INIT" and the previous trade sum equals to that trade shares, we assume these two groups are double accounted and we don't import the INIT trade
    df["Accumulated Nominal"] = df["Accumulated Nominal"] / product.share_price
    df["count_towards_total_aum"] = df.apply(_check_if_count_towards_total_aum, args=[df], axis=1)
    init_rows = df[~df["count_towards_total_aum"] & df["bank"].str.lower().isin(UNVALID_CUSTODIANS)].index
    df = df.drop(init_rows)

    df = df.drop(columns=df.columns.difference(FIELD_MAP.values()))

    df["portfolio"] = product.primary_portfolio.id
    df["currency__key"] = product.currency.key
    df["underlying_instrument"] = product.id
    df.loc[df["shares"] < 0, "transaction_subtype"] = Trade.Type.REDEMPTION
    df.loc[df["shares"] >= 0, "transaction_subtype"] = Trade.Type.SUBSCRIPTION

    return {
        "data": df.replace([np.inf, -np.inf, np.nan], None).to_dict(orient="records"),
        "history": {"underlying_instrument": product.id, "transaction_date": valuation_date.strftime("%Y-%m-%d")},
    }
