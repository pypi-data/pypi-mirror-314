from dataclasses import asdict, dataclass, field, fields
from datetime import date as date_lib
from decimal import Decimal

import pandas as pd
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property


@dataclass(frozen=True)
class Valuation:
    instrument: int
    net_value: Decimal
    outstanding_shares: Decimal = Decimal(0)


@dataclass(frozen=True)
class Position:
    underlying_instrument: int
    instrument_type: int
    weighting: Decimal
    currency: int
    date: date_lib

    asset_valuation_date: date_lib | None = None
    portfolio_created: int = None
    exchange: int = None
    is_estimated: bool = False
    country: int = None
    shares: Decimal | None = None
    is_cash: bool = False
    primary_classification: int = None
    favorite_classification: int = None
    market_capitalization_usd: float = None
    currency_fx_rate: float = 1
    market_share: float = None
    daily_liquidity: float = None
    volume_usd: float = None
    price: float = None

    def __add__(self, other):
        return Position(
            weighting=self.weighting + other.weighting,
            shares=self.shares + other.shares if (self.shares is not None and other.shares is not None) else None,
            **{f.name: getattr(self, f.name) for f in fields(Position) if f.name not in ["weighting", "shares"]},
        )


@dataclass(frozen=True)
class Portfolio:
    positions: tuple[Position]
    positions_map: dict[Position] = field(init=False, repr=False)

    def __post_init__(self):
        positions_map = {}
        for pos in self.positions:
            if pos.underlying_instrument in positions_map:
                positions_map[pos.underlying_instrument] += pos
            else:
                positions_map[pos.underlying_instrument] = pos
        object.__setattr__(self, "positions_map", positions_map)

    @cached_property
    def total_weight(self):
        return round(sum([pos.weighting for pos in self.positions]), 4)

    @cached_property
    def total_shares(self):
        return sum([pos.target_shares for pos in self.positions if pos.target_shares is not None])

    def to_df(self):
        return pd.DataFrame([asdict(pos) for pos in self.positions])

    def __len__(self):
        return len(self.positions)


@dataclass(frozen=True)
class Trade:
    underlying_instrument: int
    instrument_type: str
    currency: int
    date: date_lib

    effective_weight: Decimal
    target_weight: Decimal
    id: int | None = None
    effective_shares: Decimal = None
    target_shares: Decimal = None

    def __add__(self, other):
        return Trade(
            underlying_instrument=self.underlying_instrument,
            effective_weight=self.effective_weight + other.effective_weight,
            target_weight=self.target_weight + other.target_weight,
            target_shares=self.target_shares + other.target_shares
            if (self.target_shares is not None and other.target_shares is not None)
            else None,
            effective_shares=self.effective_shares + other.effective_shares
            if (self.effective_shares is not None and other.effective_shares is not None)
            else None,
            **{
                f.name: getattr(self, f.name)
                for f in fields(Trade)
                if f.name
                not in [
                    "effective_weight",
                    "target_weight",
                    "target_shares",
                    "effective_shares",
                    "underlying_instrument",
                ]
            },
        )

    @cached_property
    def delta_weight(self) -> Decimal:
        return self.target_weight - self.effective_weight

    def validate(self):
        if self.effective_weight < 0 or self.effective_weight > 1.0:
            raise ValidationError("Effective Weight needs to be in range [0, 1]")
        if self.target_weight < 0 or self.target_weight > 1.0:
            raise ValidationError("Target Weight needs to be in range [0, 1]")

    def normalize_target(self, total_target_weight: Decimal):
        t = Trade(
            target_weight=self.target_weight / total_target_weight if total_target_weight else self.target_weight,
            target_shares=self.target_shares / total_target_weight
            if (self.target_shares and total_target_weight)
            else self.target_shares,
            **{
                f.name: getattr(self, f.name)
                for f in fields(Trade)
                if f.name not in ["target_weight", "target_shares"]
            },
        )
        return t


@dataclass(frozen=True)
class TradeBatch:
    trades: tuple[Trade]
    trades_map: dict[Trade] = field(init=False, repr=False)

    def __post_init__(self):
        trade_map = {}
        for trade in self.trades:
            if trade.underlying_instrument in trade_map:
                trade_map[trade.underlying_instrument] += trade
            else:
                trade_map[trade.underlying_instrument] = trade
        object.__setattr__(self, "trades_map", trade_map)

    @cached_property
    def total_target_weight(self) -> Decimal:
        return round(sum([trade.target_weight for trade in self.trades]), 4)

    @cached_property
    def total_effective_weight(self) -> Decimal:
        return round(sum([trade.effective_weight for trade in self.trades]), 4)

    @cached_property
    def total_shares(self) -> Decimal:
        return sum([trade.target_shares for trade in self.trades if trade.target_shares is not None]) or Decimal(0)

    @cached_property
    def totat_abs_delta_weight(self) -> Decimal:
        return sum([abs(trade.delta_weight) for trade in self.trades])

    def __add__(self, other):
        return TradeBatch(tuple(self.trades + other.trades))

    def __len__(self):
        return len(self.trades)

    def validate(self):
        if float(self.total_target_weight) != 1.0:  # we do that to remove decimal over precision
            raise ValidationError(f"Total Weight cannot be different than 1 ({float(self.total_target_weight)})")

    def convert_to_portfolio(self):
        positions = []
        for instrument, trade in self.trades_map.items():
            positions.append(
                Position(
                    underlying_instrument=trade.underlying_instrument,
                    instrument_type=trade.instrument_type,
                    weighting=trade.target_weight,
                    shares=trade.target_shares,
                    currency=trade.currency,
                    date=trade.date,
                )
            )
        return Portfolio(tuple(positions))
