from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import pandas as pd
from typing import get_args


class TradeRecord(BaseModel):
    entry_index: int
    exit_index: int = Field(alias="exit index")  # type: ignore
    entry_timestamp: datetime
    exit_timestamp: datetime
    entry_price: float
    exit_price: float
    size: float
    sl: Optional[float] = 0
    tp: Optional[float] = 0
    side: str
    pnl: float
    max_dd: float
    close_reason: str
    commission: float
    commission_pct: float


def get_trades_df(bt):
    records = bt.state.closed_positions
    trades = []

    if len(records) == 0:
        return pd.DataFrame()

    for record in records.values():
        trade = TradeRecord.model_validate(record)
        trades.append(trade.model_dump())

    # Create a DataFrame from the trades
    df = pd.DataFrame(trades)
    for key, value in TradeRecord.model_fields.items():
        try:
            args = get_args(value.annotation)
            if args:
                df[key] = df[key].astype(args[0])
            else:
                df[key] = df[key].astype(value.annotation)
        except Exception as e:
            pass

    df.sort_values("entry_index", inplace=True)
    return df
