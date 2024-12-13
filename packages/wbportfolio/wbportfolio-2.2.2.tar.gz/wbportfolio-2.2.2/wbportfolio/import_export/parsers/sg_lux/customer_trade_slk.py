import csv
from io import StringIO

import numpy as np
import pandas as pd
from wbportfolio.models import Product, Trade
from xlrd import xldate_as_datetime

from .sylk import SYLK
from .utils import get_portfolio_id


def parse(import_source):
    data = list()
    sylk_handler = SYLK()
    for line in [_line.decode("cp1252") for _line in import_source.file.open("rb").readlines()]:
        sylk_handler.parseline(line)

    buffer = StringIO()
    csvwriter = csv.writer(buffer, quotechar="'", delimiter=";", lineterminator="\n", quoting=csv.QUOTE_ALL)
    for line in sylk_handler.stream_rows():
        csvwriter.writerow(line)

    buffer.seek(0)
    content = buffer.read().replace('""', "")
    df = pd.read_csv(StringIO(content), sep=";", quotechar="'", usecols=[1, 3, 4, 7, 10, 15, 16, 17, 18, 20, 21])
    if not df.empty:
        # Filter out all non transaction rows and remove record_desc col
        df = df[df["record_desc"].str.strip() == "TRANSACTION"]
        del df["record_desc"]

        # Convert timestamps to json conform date strings
        df["trans_date"] = df["trans_date"].apply(lambda x: xldate_as_datetime(x, datemode=0).date())
        df["trans_date"] = df["trans_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df["settl_date"] = df["settl_date"].apply(lambda x: xldate_as_datetime(x, datemode=0).date())
        df["settl_date"] = df["settl_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

        # Replace all nan values with empty str
        df[["register_firstname", "cust_ref"]] = df[["register_firstname", "cust_ref"]].replace(np.nan, "", regex=True)

        # Merge register_firstname and cust_ref and then remove both cols
        df["note"] = df["register_firstname"] + df["cust_ref"]
        del df["register_firstname"]

        # Create Product Mapping and apply to df
        product_mapping = {
            product["isin"]: product["id"]
            for product in Product.objects.filter(isin__in=df["isin"].unique()).values("id", "isin")
        }
        df["isin"] = df["isin"].apply(lambda x: product_mapping[x])

        del df["cust_ref"]

        # Rename Columns

        df.columns = [
            "register__register_reference",
            "bank",
            "underlying_instrument",
            "transaction_date",
            "value_date",
            "external_id",
            "price",
            "shares",
            "comment",
        ]
        df["transaction_subtype"] = df.shares.apply(
            lambda x: Trade.Type.REDEMPTION.value if x < 0 else Trade.Type.SUBSCRIPTION.value
        )
        df["portfolio"] = df["underlying_instrument"].apply(lambda x: get_portfolio_id(x))
        df["underlying_instrument"] = df["underlying_instrument"].apply(
            lambda x: {"id": x, "instrument_type": "product"}
        )
        df["pending"] = False
        # Convert df to list of dicts
        data = df.to_dict("records")

    return {
        "data": data,
    }
