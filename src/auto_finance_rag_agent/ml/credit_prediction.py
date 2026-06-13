from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


MODEL_FILE = Path("models/credit_risk_model.joblib")


@lru_cache(maxsize=1)
def load_credit_risk_model() -> Any:
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Credit risk model not found at {MODEL_FILE}. "
            "Run `python scripts/train_credit_model.py` first."
        )

    return joblib.load(MODEL_FILE)


def get_risk_level(probability_bad_risk: float) -> str:
    if probability_bad_risk < 0.35:
        return "low"

    if probability_bad_risk < 0.65:
        return "medium"

    return "high"


def predict_credit_risk(applicant_features: dict[str, Any]) -> dict[str, Any]:
    model = load_credit_risk_model()

    input_frame = pd.DataFrame([applicant_features])

    prediction = int(model.predict(input_frame)[0])
    probability_bad_risk = float(model.predict_proba(input_frame)[0][1])

    prediction_label = "bad_risk" if prediction == 1 else "good_risk"
    risk_level = get_risk_level(probability_bad_risk)

    return {
        "prediction": prediction,
        "prediction_label": prediction_label,
        "probability_bad_risk": round(probability_bad_risk, 4),
        "risk_level": risk_level,
        "manual_review_recommended": risk_level in ["medium", "high"],
    }