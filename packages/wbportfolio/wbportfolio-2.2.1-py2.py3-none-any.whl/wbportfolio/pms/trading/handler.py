from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from wbportfolio.pms.typing import Portfolio, Trade, TradeBatch


class TradingService:
    """
    This class represents the trading service. It can be instantiated either with the target portfolio and the effective portfolio or given a direct list of trade
    In any case, it will compute all three states
    """

    def __init__(
        self,
        trade_date: date,
        effective_portfolio: Portfolio | None = None,
        target_portfolio: Portfolio | None = None,
        trades_batch: TradeBatch | None = None,
        total_value: Decimal = None,
    ):
        if not target_portfolio and not trades_batch:
            raise ValueError("Either target positions or trades needs to be provided")
        self.total_value = total_value
        self.trade_date = trade_date
        # If effective portfoolio and trades batch is provided, we ensure the trade batch contains at least one trade for every position
        if effective_portfolio and trades_batch:
            trades_batch = self.build_trade_batch(effective_portfolio, trades_batch=trades_batch)
        # if no trade but a effective portfolio is provided, we get the trade batch only from the effective portofolio (and the target portfolio if provided, but optional. Without it, the trade delta weight will be 0 )
        elif not trades_batch and effective_portfolio:
            # If no trade batch is provided but effetive_portfolio is, we estimate the trade from the given portfolios
            trades_batch = self.build_trade_batch(effective_portfolio, target_portfolio=target_portfolio)
        # Finally, we compute the target portfolio
        if trades_batch and not target_portfolio:
            target_portfolio = trades_batch.convert_to_portfolio()

        self.trades_batch = trades_batch
        self.effective_portfolio = effective_portfolio
        self.target_portfolio = target_portfolio

    @property
    def errors(self) -> list[str]:
        """
        Returned the list of errors stored during the validation process. Can only be called after is_valid
        """
        if not hasattr(self, "_errors"):
            msg = "You must call `.is_valid()` before accessing `.errors`."
            raise AssertionError(msg)
        return self._errors

    @property
    def validated_trades(self) -> list[Trade]:
        """
        Returned the list of validated trade stored during the validation process. Can only be called after is_valid
        """
        if not hasattr(self, "_validated_trades"):
            msg = "You must call `.is_valid()` before accessing `.validated_trades`."
            raise AssertionError(msg)
        return self._validated_trades

    def run_validation(self, validated_trades: list[Trade]):
        """
        Test the given value against all the validators on the field,
        and either raise a `ValidationError` or simply return.
        """
        TradeBatch(validated_trades).validate()
        if self.effective_portfolio:
            for trade in validated_trades:
                if (
                    trade.effective_weight
                    and trade.underlying_instrument not in self.effective_portfolio.positions_map
                ):
                    raise ValidationError("All effective position needs to be matched with a validated trade")

    def build_trade_batch(
        self,
        effective_portfolio: Portfolio,
        target_portfolio: Portfolio | None = None,
        trades_batch: TradeBatch | None = None,
    ) -> TradeBatch:
        """
        Given combination of effective portfolio and either a trades batch or a target portfolio, ensure all theres variables are set

        Args:
            effective_portfolio: The effective portfolio
            target_portfolio: The optional target portfolio
            trades_batch: The optional trades batch

        Returns: The normalized trades batch
        """
        instruments = list(effective_portfolio.positions_map.keys())
        if target_portfolio:
            instruments.extend(list(target_portfolio.positions_map.keys()))
        if trades_batch:
            instruments.extend(list(trades_batch.trades_map.keys()))
        _trades: list[Trade] = []
        for instrument in set(instruments):
            effective_weight = target_weight = 0
            effective_shares = target_shares = 0
            instrument_type = currency = None
            if effective_pos := effective_portfolio.positions_map.get(instrument, None):
                effective_weight = target_weight = effective_pos.weighting
                effective_shares = target_shares = effective_pos.shares
                instrument_type, currency = effective_pos.instrument_type, effective_pos.currency
            if target_portfolio and (target_pos := target_portfolio.positions_map.get(instrument, None)):
                target_weight = target_pos.weighting
                target_shares = target_pos.shares
            if trades_batch and (trade := trades_batch.trades_map.get(instrument, None)):
                effective_weight, target_weight = trade.effective_weight, trade.target_weight
                effective_shares, target_shares = trade.effective_shares, trade.target_shares
                instrument_type, currency = trade.instrument_type, trade.currency

            _trades.append(
                Trade(
                    underlying_instrument=instrument,
                    effective_weight=effective_weight,
                    target_weight=target_weight,
                    effective_shares=effective_shares,
                    target_shares=target_shares,
                    date=self.trade_date,
                    instrument_type=instrument_type,
                    currency=currency,
                )
            )
        return TradeBatch(tuple(_trades))

    def is_valid(self, ignore_error: bool = False) -> bool:
        """
        Validate the trade batch against a set of default rules. Populate the validated_trades and errors property.
        Ignore error by default
        Args:
            ignore_error: If true, will raise the error. False by default

        Returns: True if the trades batch is valid
        """
        if not hasattr(self, "_validated_trades"):
            self._validated_trades = []
            self._errors = []
            # Run validation for every trade. If a trade is not valid, we simply exclude it from the validated trades list
            for _, trade in self.trades_batch.trades_map.items():
                try:
                    trade.validate()
                    self._validated_trades.append(trade)
                except ValidationError as exc:
                    self._errors.append(exc.message)
            try:
                # Check the overall validity of the trade batch. If this fail, we consider all trade invalids
                self.run_validation(self._validated_trades)
            except ValidationError as exc:
                self._validated_trades = []
                self._errors.append(exc.message)

            if self._errors and not ignore_error:
                raise ValidationError(self.errors)

        return not bool(self._errors)

    def normalize(self):
        """
        Normalize the instantiate trades batch so that the target weight is 100%
        """
        self.trades_batch = TradeBatch(
            [trade.normalize_target(self.trades_batch.total_target_weight) for trade in self.trades_batch.trades]
        )
