from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from xgboost import XGBRegressor


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "saved_models" / "best_regression_model.joblib"


def _regression_models() -> dict[str, object]:
    return {
        "LinearRegression": LinearRegression(),
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=250, random_state=42, n_jobs=-1
        ),
        "XGBRegressor": XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            objective="reg:squarederror",
        ),
        "SVR": SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1),
    }


def train_regression_models(x: pd.DataFrame, y: pd.Series) -> dict:
    """Train regression models, report metrics, and persist the best one."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, shuffle=False
    )
    if x_train.empty or x_test.empty:
        raise ValueError("Insufficient data for regression training split.")

    metrics = []
    best_rmse = np.inf
    best_bundle = None

    for name, model in _regression_models().items():
        model.fit(x_train, y_train)
        preds = model.predict(x_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        metrics.append(
            {
                "model": name,
                "mae": float(mae),
                "rmse": float(rmse),
                "r2": float(r2),
            }
        )

        if rmse < best_rmse:
            best_rmse = rmse
            best_bundle = {"model_name": name, "model": model, "features": list(x.columns)}

    if best_bundle is None:
        raise RuntimeError("No regression model was successfully trained.")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_bundle, MODEL_PATH)

    return {"best_model": best_bundle["model_name"], "metrics": metrics}


def load_best_regression_model() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Regression model is not trained yet.")
    return joblib.load(MODEL_PATH)
