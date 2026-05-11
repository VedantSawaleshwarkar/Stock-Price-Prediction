from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data.features import add_technical_features, latest_feature_row, prepare_training_data
from data.fetcher import fetch_ohlcv_data
from models.classification import (
    load_best_classification_model,
    train_classification_models,
)
from models.regression import load_best_regression_model, train_regression_models


POPULAR_TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NFLX", "META"]

app = FastAPI(title="Stock Price Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrainRequest(BaseModel):
    ticker: str
    start_date: str = "2019-01-01"


class PredictRequest(BaseModel):
    ticker: str


@app.get("/")
def root() -> dict:
    return {"status": "ok", "message": "Stock API running"}


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/tickers")
def tickers() -> list[str]:
    return POPULAR_TICKERS


@app.post("/api/train")
def train_models(payload: TrainRequest) -> dict:
    try:
        df = fetch_ohlcv_data(ticker=payload.ticker, start_date=payload.start_date)
        x, y_reg, y_cls = prepare_training_data(df)

        reg_result = train_regression_models(x, y_reg)
        cls_result = train_classification_models(x, y_cls)

        return {
            "ticker": payload.ticker.upper(),
            "data_points": len(x),
            "regression": reg_result,
            "classification": cls_result,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc


@app.post("/api/predict")
def predict_next(payload: PredictRequest) -> dict:
    try:
        reg_bundle = load_best_regression_model()
        cls_bundle = load_best_classification_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"{exc} Train first via /api/train.") from exc

    try:
        end_date = datetime.utcnow().date().isoformat()
        start_date = (datetime.utcnow().date() - timedelta(days=365)).isoformat()
        df = fetch_ohlcv_data(payload.ticker, start_date=start_date, end_date=end_date)

        x_latest = latest_feature_row(df)
        x_latest = x_latest[reg_bundle["features"]]

        predicted_price = float(reg_bundle["model"].predict(x_latest)[0])
        cls_features = x_latest[cls_bundle["features"]]
        cls_model = cls_bundle["model"]
        cls_pred = int(cls_model.predict(cls_features)[0])
        trend = "UP" if cls_pred == 1 else "DOWN"

        if hasattr(cls_model, "predict_proba"):
            confidence = float(max(cls_model.predict_proba(cls_features)[0]))
        else:
            confidence = 0.5

        return {
            "predicted_price": round(predicted_price, 4),
            "trend": trend,
            "confidence": round(confidence, 4),
            "model_used": f"{reg_bundle['model_name']} + {cls_bundle['model_name']}",
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


@app.get("/api/history/{ticker}")
def history(ticker: str) -> dict:
    try:
        end_date = datetime.utcnow().date().isoformat()
        start_date = (datetime.utcnow().date() - timedelta(days=365)).isoformat()
        df = fetch_ohlcv_data(ticker, start_date=start_date, end_date=end_date)
        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for ticker '{ticker}'",
            )
        featured = add_technical_features(df).tail(90).copy()
        num_cols = featured.select_dtypes(include=["float64", "float32", "int64"]).columns
        featured[num_cols] = featured[num_cols].fillna(0)
        featured["Date"] = pd.to_datetime(featured["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
        return {"ticker": ticker.upper(), "history": featured.to_dict(orient="records")}
    except HTTPException:
        raise
    except ValueError as exc:
        msg = str(exc)
        if "No data" in msg or "No data returned" in msg:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for ticker '{ticker}'",
            ) from exc
        raise HTTPException(status_code=400, detail=msg) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {exc}") from exc
