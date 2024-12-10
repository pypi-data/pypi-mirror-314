import pandas as pd
import matplotlib
from zenbt.rs import Backtest


def plot_equity(df: pd.DataFrame, bt: Backtest):
    state = bt.get_state()
    equity = state["equity"]
    equity = pd.DataFrame(equity)
    equity["time"] = df["time"]
    equity["time"] = pd.to_datetime(equity["time"], unit="ms")
    equity.set_index("time", inplace=True)
    main_col = equity.columns[0]
    equity[main_col] = equity[main_col].astype(float)
    print("Preparing to plot")
    if len(equity) > 25000:
        freq = len(df) // 100000  # This gives us the step size
        # Apply the resampling (using 'freq' days if daily)
        equity = equity.resample(f"{freq}D").mean()
    equity.plot()
