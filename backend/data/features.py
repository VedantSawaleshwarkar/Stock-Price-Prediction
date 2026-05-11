from __future__ import annotations

import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, SMAIndicator
from ta.volatility import BollingerBands


FEATURE_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "RSI_14",
    "MACD",
    "MACD_signal",
    "MACD_diff",
    "BB_upper",
    "BB_middle",
    "BB_lower",
    "SMA_20",
    "SMA_50",
    "EMA_12",
    "EMA_26",
    "Volume_change_pct",
    "Daily_return_pct",
    "Close_lag_1",
    "Close_lag_3",
    "Close_lag_7",
]


def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute TA indicators and lag features; TA calls are guarded for short series."""
    data = df.copy()
    data = data.sort_values("Date").reset_index(drop=True)

    close = data["Close"]
    volume = data["Volume"]

    try:
        data["RSI_14"] = RSIIndicator(close=close, window=14).rsi()
    except Exception:
        data["RSI_14"] = np.nan

    try:
        macd = MACD(close=close)
        data["MACD"] = macd.macd()
        data["MACD_signal"] = macd.macd_signal()
        data["MACD_diff"] = macd.macd_diff()
    except Exception:
        data["MACD"] = np.nan
        data["MACD_signal"] = np.nan
        data["MACD_diff"] = np.nan

    try:
        bb = BollingerBands(close=close, window=20, window_dev=2)
        data["BB_upper"] = bb.bollinger_hband()
        data["BB_middle"] = bb.bollinger_mavg()
        data["BB_lower"] = bb.bollinger_lband()
    except Exception:
        data["BB_upper"] = np.nan
        data["BB_middle"] = np.nan
        data["BB_lower"] = np.nan

    try:
        data["SMA_20"] = SMAIndicator(close=close, window=20).sma_indicator()
        data["SMA_50"] = SMAIndicator(close=close, window=50).sma_indicator()
        data["EMA_12"] = EMAIndicator(close=close, window=12).ema_indicator()
        data["EMA_26"] = EMAIndicator(close=close, window=26).ema_indicator()
    except Exception:
        data["SMA_20"] = np.nan
        data["SMA_50"] = np.nan
        data["EMA_12"] = np.nan
        data["EMA_26"] = np.nan

    data["Volume_change_pct"] = volume.pct_change() * 100.0
    data["Daily_return_pct"] = close.pct_change() * 100.0

    data["Close_lag_1"] = close.shift(1)
    data["Close_lag_3"] = close.shift(3)
    data["Close_lag_7"] = close.shift(7)

    data["Target_regression"] = close.shift(-1)
    data["Target_classification"] = np.where(close.shift(-1) > close, 1, 0)

    return data


def prepare_training_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Prepare model features and targets after dropping NaN rows."""
    featured = add_technical_features(df)
    featured.dropna(inplace=True)
    featured.reset_index(drop=True, inplace=True)

    if len(featured) < 50:
        raise ValueError("Not enough data to train models")

    x = featured[FEATURE_COLUMNS]
    y_reg = featured["Target_regression"]
    y_cls = featured["Target_classification"].astype(int)
    return x, y_reg, y_cls


def latest_feature_row(df: pd.DataFrame) -> pd.DataFrame:
    """Return the latest row with complete features for prediction."""
    featured = add_technical_features(df)
    latest = featured.dropna(subset=FEATURE_COLUMNS).tail(1)
    if latest.empty:
        raise ValueError("Insufficient data to compute prediction features.")
    return latest[FEATURE_COLUMNS]
