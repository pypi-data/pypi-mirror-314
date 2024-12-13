import numpy as np
import pandas as pd

from .utils import _get_exchange_from_ticker, _get_ticker, file_name_parse

COLUMN_MAP = {
    "Ticker": "underlying_instrument__ticker",
    "Underlying": "underlying_instrument__name",
    "Underlying ISIN": "underlying_instrument__isin",
    "Div Crncy": "currency__key",
    "Quantity": "shares",
    "Fx Rate": "currency_fx_rate",
    "Net Amount": "total_value_fx_portfolio",
    "Retro in%": "retrocession",
    "Gross Div": "price_gross",
    "Ex Div Date": "transaction_date",
    "Value Date": "value_date",
}


def parse(import_source):
    parts = file_name_parse(import_source.file.name)
    product = parts["product"]

    df = pd.read_csv(import_source.file, sep=";", skipinitialspace=True)
    df = df.rename(columns=COLUMN_MAP).astype("str")

    df["underlying_instrument__exchange"] = df["underlying_instrument__ticker"].apply(
        lambda x: _get_exchange_from_ticker(x)
    )
    df["underlying_instrument__ticker"] = df["underlying_instrument__ticker"].apply(lambda x: _get_ticker(x))
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True).dt.strftime("%Y-%m-%d")
    df["value_date"] = pd.to_datetime(df["value_date"], dayfirst=True).dt.strftime("%Y-%m-%d")
    df = df[df["underlying_instrument__isin"].str.contains("([A-Z]{2})([A-Z0-9]{9})([0-9]{1})", regex=True)]
    float_columns = ["shares", "total_value_fx_portfolio", "price_gross", "currency_fx_rate", "retrocession"]
    for float_column in float_columns:
        df[float_column] = df[float_column].str.replace(" ", "").astype("float")
    df = df.drop(columns=df.columns.difference(COLUMN_MAP.values()))

    df["retrocession"] = df["retrocession"] / 100.0
    df["total_value"] = df["total_value_fx_portfolio"] / df["currency_fx_rate"]
    df["price"] = df["total_value"] / df["shares"] / df["retrocession"]
    df["total_value_gross"] = df["price_gross"] * df["shares"] * df["retrocession"]
    df["total_value_gross_fx_portfolio"] = df["total_value_gross"] * df["currency_fx_rate"]
    df["portfolio"] = product.primary_portfolio.id
    df = df.replace([np.inf, -np.inf, np.nan], None)
    return {
        "data": df.to_dict("records"),
        "history": {
            "transaction_date": parts["valuation_date"].strftime("%Y-%m-%d"),
            "portfolio": product.primary_portfolio.id,
        },
    }
