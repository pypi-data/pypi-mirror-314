import time
import talib
import pandas as pd
import polars as pl
import numpy as np
from zenbt.sdk import Stats
from zenbt.zbt import Backtest, BacktestParams, indicators
from zenbt.sdk.trade_record import get_trades_df

from slpeters.strategy import Strategy
from tradingtoolbox.utils import resample, TimeManip
from tradingtoolbox.clickhouse import ClickhouseSync


def get_data():
    from zenbt.data import get_sample_btc_data
    from zenbt.sdk import create_session

    # df = get_sample_btc_data()
    df = pl.read_parquet("./data/cme/@MES.parquet")
    df = df.with_columns((pl.col("time") * 1000).alias("time"))
    df = df.rename({"real_volume": "volume"})
    df = df.drop(["tick_volume", "spread"])

    _df = df.to_pandas()
    _df["time"] = pd.to_datetime(_df["time"], unit="ms")
    _df = resample(_df, tf="1H", on="time")
    _df.reset_index(inplace=True)
    _df["time"] = TimeManip().convert_datetime_to_ms(_df["time"])
    _df.dropna(inplace=True)
    df = pl.from_pandas(_df)

    df = create_session(
        df, session_name="japan", session_hour_start=0, session_hour_end=9
    )
    df = create_session(
        df, session_name="london", session_hour_start=8, session_hour_end=5
    )
    df = create_session(
        df, session_name="ny", session_hour_start=13, session_hour_end=10
    )
    df[-10000:].write_parquet("./data/cme/main.parquet")

    return df


def hello():
    df = get_data()

    df = pl.read_parquet("./data/cme/main.parquet")
    df = df[-200:]

    window = 150
    ind_123 = indicators.indicator_123(
        window,
        df["high"].to_numpy(),
        df["low"].to_numpy(),
        talib.MAX(df["high"], window).to_numpy(),
        talib.MIN(df["low"].to_numpy(), window),
    )
    # print(ind_123.keys())
    # slow_ma = talib.SMA(df["close"], timeperiod=50)
    df = df.with_columns(
        pl.Series("point_1", ind_123["point_1"]),
        pl.Series("point_2", ind_123["point_2"]),
        pl.Series("point_3", ind_123["point_3"]),
    )

    slpeters = Strategy(df, default_size=1)
    slpeters.pickl("/tmp/slpeters")
    bt_params = BacktestParams(
        commission_pct=0.02 / 100,  # This is 2 bps
        initial_capital=100_000,
        provide_active_position=True,
    )
    bt = Backtest(df, bt_params, slpeters)

    start = time.time()
    bt.backtest()
    print(f"Backtest took: {(time.time() - start) * 1000:.2f} ms")

    trades = get_trades_df(bt)
    print(trades)
    # print(trades.dtypes)
    ch = ClickhouseSync.create()
    ch.insert_df(trades, "trades")

    stats = Stats(bt, df)
    # stats.print()

    # df = df.with_columns(pl.col("time").cast(pl.Datetime("ms")).alias("datetime"))
    df = df.with_columns(pl.col("time").cast(pl.Datetime("ms")))
    df = df.to_pandas()
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df.drop(["japan", "london", "ny", "volume"], axis=1, inplace=True)

    ch = ClickhouseSync.create()
    ch.insert_df(df, "ohlc")
