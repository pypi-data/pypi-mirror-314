from wbportfolio.models import Product


def get_product(identifier):
    return Product.objects.filter(identifier=identifier).first()


def get_portfolio_id(identifier):
    if (product := get_product(identifier)) and (portfolio := product.primary_portfolio):
        return portfolio.id


def get_perf_fee_isin(source):
    default_perf_fee_isin = "CH0040602242"
    if source:
        return source.import_parameters.get("performance_fees_instrument_isin", default_perf_fee_isin)
    return default_perf_fee_isin
