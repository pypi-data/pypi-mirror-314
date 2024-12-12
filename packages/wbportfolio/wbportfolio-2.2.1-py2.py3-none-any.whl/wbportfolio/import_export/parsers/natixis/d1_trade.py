import xlrd
from wbportfolio.models import Product, Trade


def get_isin(sheet):
    for row in sheet.get_rows():
        if row[0].value == "ISIN":
            return row[1].value


def parse(import_source):
    book = xlrd.open_workbook(file_contents=import_source.file.read())

    product = Product.objects.get(isin=get_isin(book.sheet_by_name("Certificate")))
    valuation_sheet = book.sheet_by_name("Transaction Fees")

    trade_date_column = None
    shares_column = None
    price_column = None
    currency_fx_rate_column = None
    isin_column = None
    execution_fees_column = None

    data = list()
    for i, row in enumerate(valuation_sheet.get_rows()):
        if i == 0:
            for column in range(0, valuation_sheet.ncols):
                if "Trade date" == row[column].value:
                    trade_date_column = column

                if "Quantity" == row[column].value:
                    shares_column = column

                if "Price" == row[column].value:
                    price_column = column

                if "Forex" == row[column].value:
                    currency_fx_rate_column = column

                if "Reference" == row[column].value:
                    isin_column = column

                if "Exec Fees" in row[column].value:
                    execution_fees_column = column

        else:
            transaction_date = xlrd.xldate.xldate_as_datetime(row[trade_date_column].value, 0)
            shares = row[shares_column].value
            price = row[price_column].value
            currency_fx_rate = row[currency_fx_rate_column].value
            row[execution_fees_column].value

            traded_product = Product.objects.get(isin=row[isin_column].value)

            data.append(
                {
                    "portfolio": product.primary_portfolio.id,
                    "transaction_subtype": Trade.Type.REBALANCE,
                    "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                    "shares": shares,
                    "price": price,
                    "currency__key": traded_product.currency.key,
                    "currency_fx_rate": currency_fx_rate,
                    "underlying_instrument": {"id": traded_product.id, "instrument_type": "product"},
                    # 'execution_fees_percent': 0,
                    # 'market_fees_percent': 0,
                }
            )

    return {"data": data}
