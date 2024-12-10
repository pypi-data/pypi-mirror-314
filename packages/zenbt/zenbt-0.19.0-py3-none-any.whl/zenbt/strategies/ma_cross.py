from zenbt.sdk.base import BaseStrategy
from zenbt.zbt import (
    Side,
    Action,
)


class MaCross(BaseStrategy):
    default_size = 3

    def on_candle(self, state=None, **kwargs) -> Action:  # type: ignore
        cross_below = self.data["cross_below"][self.index]
        cross_above = self.data["cross_above"][self.index]

        # Check for bullish cross over
        if cross_above:
            order = self.create_market_order(
                self.index,
                client_order_id="Long",
                side=Side.Long,
                size=self.default_size,
            )
            # self.action.orders = {order.client_order_id: order}
            # self.action.close_all_positions = True
            return Action(
                orders={order.client_order_id: order},
                close_all_positions=True,
            )

        # Check for bearish crossover
        if cross_below:
            order = self.create_market_order(
                self.index,
                client_order_id="Short",
                side=Side.Short,
                size=self.default_size,
            )
            # self.action.orders = {order.client_order_id: order}
            # self.action.close_all_positions = True
            return Action(
                orders={order.client_order_id: order},
                close_all_positions=True,
            )

        return self.action
