from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "saved_models" / "best_classification_model.joblib"


def _classification_models() -> dict[str, object]:
    return {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForestClassifier": RandomForestClassifier(
            n_estimators=250, random_state=42, n_jobs=-1
        ),
        "XGBClassifier": XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            eval_metric="logloss",
        ),
        "KNNClassifier": KNeighborsClassifier(n_neighbors=7),
    }


def train_classification_models(x: pd.DataFrame, y: pd.Series) -> dict:
    """Train classifiers, report metrics, and persist the best one."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, shuffle=False
    )
    if x_train.empty or x_test.empty:
        raise ValueError("Insufficient data for classification training split.")

    metrics = []
    best_f1 = -1.0
    best_bundle = None

    for name, model in _classification_models().items():
        model.fit(x_train, y_train)
        preds = model.predict(x_test)

        accuracy = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)

        metrics.append(
            {
                "model": name,
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1),
            }
        )

        if f1 > best_f1:
            best_f1 = f1
            best_bundle = {"model_name": name, "model": model, "features": list(x.columns)}

    if best_bundle is None:
        raise RuntimeError("No classification model was successfully trained.")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_bundle, MODEL_PATH)
    return {"best_model": best_bundle["model_name"], "metrics": metrics}


def load_best_classification_model() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Classification model is not trained yet.")
    return joblib.load(MODEL_PATH)
