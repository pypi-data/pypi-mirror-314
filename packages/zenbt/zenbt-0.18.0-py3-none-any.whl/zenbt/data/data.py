import pandas as pd
from tradingtoolbox.utils import resample
from tradingtoolbox.exchanges.okx import OKXKlines
import polars as pl


def download_okx_data(symbol="PEPE-USDT-SWAP", interval="1m", days_ago=90):
    OKXKlines().load_klines(symbol, interval, days_ago=days_ago)


def read_data(
    sym,
    start=0,
    end=-1,
    resample_tf="1min",
    exchange="binance",
    # ) -> tuple[pd.DataFrame, OHLCs]:
) -> pd.DataFrame:
    # df = pd.read_parquet(f"./data/kline_{sym}-USDT-SWAP_1m.parquet")
    # df.sort_values(by=["date"], ascending=True, inplace=True)
    if exchange == "binance":
        df = pd.read_parquet(f"./data/binance-{sym}USDT-PERPETUAL-1m.parquet")
        df.drop(
            columns=[
                "taker_buy_volume",
                "quote_asset_volume",
                "close_time",
                "number_of_trades",
                "taker_buy_quote_asset_volume",
                "ignore",
            ],
            inplace=True,
        )
        df["volume"] = df["volume"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df.reset_index(inplace=True)
        if resample_tf != "1min":
            df = resample(df, tf=resample_tf, on="time")
            df.reset_index(inplace=True)
        df["time"] = pd.to_datetime(df["time"]).astype(int) / 10**6
        df = df[start:end]
    else:
        df = pd.read_parquet(f"./data/kline_{sym}-USDT-SWAP_1m.parquet")
        df["d"] = pd.to_datetime(df["date"], unit="ms")
        # df["time"] = pd.to_datetime(df["date"]).astype(int) / 10**6
        if resample_tf != "1min":
            df = resample(df, tf=resample_tf, on="time")
            df.reset_index(inplace=True)
        df = df[start:end]
        df.drop(columns=["d"], inplace=True)  # type: ignore

        df["volume"] = df["volume"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

    # ohlcs = OHLCs(df.to_numpy())  # type: ignore
    # return df, ohlcs  # type: ignore
    return df  # type: ignore


def read_data_pl(
    sym,
    start=0,
    end=-1,
    resample_tf="1min",
    exchange="binance",
) -> pl.DataFrame:
    # ) -> tuple[pd.DataFrame, OHLCs]:
    # Read the appropriate Parquet file
    if exchange == "binance":
        df = pl.read_parquet(f"./data/binance-{sym}USDT-PERPETUAL-1m.parquet")

        # Drop unnecessary columns
        df = df.drop(
            [
                "taker_buy_volume",
                "quote_asset_volume",
                "close_time",
                "number_of_trades",
                "taker_buy_quote_asset_volume",
                "ignore",
            ]
        )

        # Cast columns to Float64
        df = df.with_columns(
            [
                pl.col("volume").cast(pl.Float64),
                pl.col("open").cast(pl.Float64),
                pl.col("high").cast(pl.Float64),
                pl.col("low").cast(pl.Float64),
                pl.col("close").cast(pl.Float64),
            ]
        )

        # Resampling if needed
        if resample_tf != "1min":
            df = resample(df, tf=resample_tf, on="time")

        # Convert timestamp and slice
        df = df.with_columns(pl.col("time").cast(pl.Datetime).cast(pl.Int64) // 10**3)
        df = df.slice(start, end - start if end != -1 else None)

    else:
        df = pl.read_parquet(f"./data/kline_{sym}-USDT-SWAP_1m.parquet")
        df.drop_in_place("__index_level_0__")
        # df.drop_in_place("date")
        df.drop_in_place("d")
        df = df.rename({"date": "time"})

        # Resampling if needed
        if resample_tf != "1min":
            df = resample(df, tf=resample_tf, on="date")

        # Slice the DataFrame and drop the date column
        df = df.slice(start, end - start if end != -1 else None)
        # df = df.drop(["date"])

        # Cast columns to Float64
        df = df.with_columns(
            [
                pl.col("volume").cast(pl.Float64),
                pl.col("open").cast(pl.Float64),
                pl.col("high").cast(pl.Float64),
                pl.col("low").cast(pl.Float64),
                pl.col("close").cast(pl.Float64),
            ]
        )

    # Convert DataFrame to numpy array for OHLCs compatibility, if needed
    # ohlcs = OHLCs(df.to_numpy())
    # return df, ohlcs
    return df
