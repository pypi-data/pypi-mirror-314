from zenbt.sdk import BaseStrategy
from zenbt.zbt import Action, PySharedState, Side, Position
from datetime import datetime


class Strategy(BaseStrategy):
    last_pos_id = None

    def on_candle(self, state: PySharedState = None, **kwargs) -> Action:
        index = self.index - 1
        point_3 = self.data["point_3"][index]

        if state.active_position is None:
            if point_3 > 0:
                print("------------------------")
                sl = self.data["point_1"][index]
                entry = self.data["point_2"][index]
                dt = datetime.fromtimestamp(self.data["time"][self.index] / 1000)

                side = Side.Long if sl < entry else Side.Short
                if side == Side.Long:
                    tp = entry + (entry - sl)
                else:
                    tp = entry - (sl - entry)
                print(dt, entry, sl, tp, side)
                order = self.create_limit_order(
                    index,
                    client_order_id="Long",
                    side=side,
                    size=self.default_size,
                    price=entry,
                    sl=sl,
                    tp=tp,
                )
                # self.action.orders = {order.client_order_id: order}
                # self.action.close_all_positions = True
                return Action(
                    orders={order.client_order_id: order},
                    close_all_positions=True,
                )
                print(point_3)
        else:
            pos: Position = state.active_position
            # atr_at_pos = self.get_at("atr", pos.entry_index)
            # if pos.id != self.last_pos_id:
            #     self.last_pos_id = pos.id
            #     print(pos.id, pos.entry_index)
            #     print(atr_at_pos)
        #     print("We are in a position")

        return self.action
