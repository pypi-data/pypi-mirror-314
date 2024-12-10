from zenbt.zbt import (
    OrderType,
    Side,
    Strategy,
    PySharedState,
    Action,
    Order,
)
from typing import Optional


class BaseStrategy(Strategy):
    state: PySharedState
    """The current state of the backtest"""

    def _on_candle(self, state=None):
        self.update_index()
        return self.on_candle(state)

    def get(self, col: str):
        return self.data[col][self.index]

    def get_at(self, col: str, index: int):
        return self.data[col][index]

    # def create_market_order(
    #     self,
    #     index,
    #     client_order_id: str,
    #     side: Side,
    #     size: float,
    #     sl: Optional[float] = None,
    #     tp: Optional[float] = None,
    # ) -> Order:
    #     return Order(
    #         index=index,
    #         client_order_id=client_order_id,
    #         order_type=OrderType.Market,
    #         side=side,
    #         size=size,
    #         price=None,
    #         sl=sl,
    #         tp=tp,
    #     )

    # def active_long_positions(self) -> list[Position]:
    #     positions = []
    #     for pos in self.state.active_positions:
    #         if pos.side == Side.Long:
    #             positions.append(pos)
    #     return positions

    # def active_short_positions(self) -> list[Position]:
    #     positions = []
    #     for pos in self.state.active_positions:
    #         if pos.side == Side.Short:
    #             positions.append(pos)
    #     return positions

    # def has_position(self) -> bool:
    #     return len(self.state.active_positions) > 0
