from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime
import pandas as pd
from rich import print


class TradeRecord(BaseModel):
    index: int
    exit_index: int = Field(alias="exit index")  # type: ignore
    entry_timestamp: datetime
    exit_timestamp: datetime
    entry_price: Decimal
    exit_price: Decimal
    size: Decimal
    sl: Decimal
    tp: Decimal
    side: str
    pnl: Decimal
    max_dd: Decimal
    close_reason: str
    commission: Decimal
    commission_pct: Decimal


def get_trades_df(state):
    records = state["closed_positions"]
    print(records)
    trades = []
    for record in records:
        trade = TradeRecord.model_validate(record)
        trades.append(trade.model_dump())
    df = pd.DataFrame(trades)
    return df
