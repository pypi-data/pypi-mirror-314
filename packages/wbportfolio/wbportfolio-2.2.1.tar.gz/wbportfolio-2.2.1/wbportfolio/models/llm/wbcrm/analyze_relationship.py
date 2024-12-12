import json
from typing import TYPE_CHECKING

from django.db.models import F, FloatField, Sum
from django.db.models.functions import Cast, ExtractYear
from langchain_core.messages import HumanMessage, SystemMessage
from wbfdm.models import Instrument

if TYPE_CHECKING:
    from langchain_core.messages import BaseMessage
    from wbcrm.models import Account


def get_holding_prompt(account: "Account") -> list["BaseMessage"]:
    from wbportfolio.models import Product
    from wbportfolio.models.transactions.claim import Claim

    products = (
        Claim.get_valid_and_approved_claims(account=account)
        .distinct("product")
        .values_list("product", "product__isin")
    )

    performances = {}
    for product_id, product_name in products:
        performances[product_name] = Instrument.extract_annual_performance_df(
            Product.objects.get(id=product_id).get_prices_df()
        ).to_dict()

    return [
        SystemMessage(
            "The following products are held by the account holder. Analyze their performances and check correlations between the holdings and their performances/interactions."
        ),
        HumanMessage(json.dumps(performances)),
    ]


def get_performances_prompt(account: "Account") -> list["BaseMessage"]:
    from wbportfolio.models.transactions.claim import Claim

    holdings = (
        Claim.get_valid_and_approved_claims(account=account)
        .annotate(year=ExtractYear("date"))
        .values("year", "product")
        .annotate(
            sum_shares=Cast(Sum("shares"), FloatField()),
            product_name=F("product__name"),
            product_isin=F("product__isin"),
        )
        .values("product_name", "product_isin", "sum_shares", "year")
    )

    return [
        SystemMessage(
            "The following holdings (subscriptions/redemptions) have been found for this account. Please include this data in the analysis and check if there is any correlation between the holding data and the interactions."
        ),
        HumanMessage(json.dumps(list(holdings.order_by("year", "product")))),
    ]
