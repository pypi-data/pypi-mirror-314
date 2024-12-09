import pandas as pd
import quantstats as qs


def tearsheet(bt, original_df):
    state = bt.state
    cutoff = 9900
    pos = state.closed_positions
    df = pd.DataFrame(pos.values())
    df.sort_values("entry_index", inplace=True)
    print(df)
    print(df["pnl"])
    return

    qs.extend_pandas()

    df = pd.DataFrame(state.equity[1:cutoff], columns=["equity"])
    df["time"] = original_df["time"][0 : (cutoff - 1)]
    df["equity"] = df["equity"].astype(float)

    df["returns"] = df["equity"].pct_change()
    df.dropna(inplace=True)  # Drop NaN caused by pct_change()
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df.set_index("time", inplace=True)
    df.drop("equity", axis=1, inplace=True)

    print(df)

    qs.reports.html(df["returns"], benchmark=None, output="report.html")
