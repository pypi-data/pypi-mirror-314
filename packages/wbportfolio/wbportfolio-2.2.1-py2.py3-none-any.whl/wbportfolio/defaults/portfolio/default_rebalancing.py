from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional

import pandas as pd
from wbportfolio.models import Portfolio


def callback(
    portfolio: Portfolio,
    sync_date: date,
    rebalancing_freq: Optional[str] = "B",
    equally_weighted: Optional[bool] = False,
    composite: Optional[bool] = False,
    base_assets: Optional[Dict] = dict(),
    **kwargs: Any,
):
    """Recursively calculates the position for a portfolio

    Arguments:
        portfolio {portfolio.Portfolio} -- The Portfolio on which the assets will be computed
        sync_date {datetime.date} -- The date on which the assets will be computed

    Keyword Arguments:
        portfolio {portfolio.Portfolio} -- The core portfolio from which the computed position are created (default: {None})
        adjusted_weighting {int} -- the adjusted weight of the current level of index (default: {1})
        adjusted_currency_fx_rate {int} -- the adjusted currency exchange rate on the current level of index (default: {1})

    Yields:
        tuple[dict, dict] -- Two dictionaries: One with filter parameters and one with default values
    """
    assets = portfolio.assets.filter(date=sync_date)
    if composite:
        last_trade_proposals = portfolio.trade_proposals.filter(trade_date__lte=sync_date)
        if last_trade_proposals.exists():
            base_assets = last_trade_proposals.latest("trade_date").base_assets
    if assets.exists() and assets.filter(date=sync_date).exists():
        for asset in assets.all():
            new_weight = asset.weighting
            if pd.date_range(end=sync_date, periods=1, freq=rebalancing_freq)[0] == pd.Timestamp(sync_date):
                if equally_weighted:
                    new_weight = Decimal(1 / assets.count())
                elif base_assets and (proposed_weight := base_assets.get(asset.underlying_instrument.id, None)):
                    new_weight = proposed_weight
            yield asset._build_dto(), asset._build_dto(new_weight)
