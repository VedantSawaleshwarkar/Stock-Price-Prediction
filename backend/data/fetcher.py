from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _parse_iso_date(value: str):
    """Parse YYYY-MM-DD from API / frontend."""
    return datetime.fromisoformat(value.strip()).date()


def _normalize_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex columns (single-ticker downloads often return (Field, Ticker))."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.droplevel(1)
    return df


def _coerce_ohlcv_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure OHLCV columns are numeric (CSV cache and some yfinance paths use strings)."""
    out = df.copy()
    out["Date"] = pd.to_datetime(out["Date"], errors="coerce")
    for col in ("Open", "High", "Low", "Close", "Volume"):
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def _cache_path(ticker: str, start_date: str, end_date: str) -> Path:
    safe_ticker = ticker.upper().strip().replace("/", "_")
    return CACHE_DIR / f"{safe_ticker}_{start_date}_{end_date}.csv"


def fetch_ohlcv_data(
    ticker: str,
    start_date: str | None = None,
    end_date: str | None = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a ticker from yfinance and cache locally.
    Defaults to 5 years of data when date range is not provided.
    """
    ticker = ticker.upper().strip()
    if not ticker:
        raise ValueError("Ticker symbol is required.")

    today = datetime.today().date()

    if end_date is None:
        end_d = today
    else:
        end_d = _parse_iso_date(end_date)
    if end_d > today:
        end_d = today

    if start_date is None:
        start_d = today - timedelta(days=5 * 365)
    else:
        start_d = _parse_iso_date(start_date)
    if start_d >= today:
        start_d = today - timedelta(days=5 * 365)

    if start_d >= end_d:
        start_d = end_d - timedelta(days=5 * 365)

    start_date = start_d.isoformat()
    end_date = end_d.isoformat()

    cache_file = _cache_path(ticker, start_date, end_date)
    if use_cache and cache_file.exists():
        cached_df = pd.read_csv(cache_file, parse_dates=["Date"])
        if not cached_df.empty:
            cached_df = _coerce_ohlcv_types(cached_df)
            cached_df = cached_df.dropna(subset=["Date", "Close"]).reset_index(drop=True)
            if not cached_df.empty:
                return cached_df

    df = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if df is None or df.empty:
        raise ValueError(f"No data returned for {ticker}")

    df = _normalize_yfinance_columns(df)
    df = df.reset_index()
    required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    df = df[required_cols].copy()
    df = _coerce_ohlcv_types(df)
    df = df.dropna(subset=["Date", "Close"]).reset_index(drop=True)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}")
    df.to_csv(cache_file, index=False)
    return df
