import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES_FILE = Path("data/processed/credit_features.csv")
TARGET_FILE = Path("data/processed/credit_targets.csv")

MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "credit_risk_model.joblib"
METADATA_FILE = MODEL_DIR / "credit_risk_model_metadata.json"


NUMERIC_FEATURES = [
    "duration_months",
    "credit_amount",
    "installment_rate",
    "present_residence_since",
    "age",
    "existing_credits",
    "people_liable",
]


def train_credit_risk_model() -> dict:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(FEATURES_FILE)
    raw_target = pd.read_csv(TARGET_FILE)["target"]

    target = raw_target.map(
        {
            1: 0,
            2: 1,
        }
    )

    categorical_features = [
        column
        for column in features.columns
        if column not in NUMERIC_FEATURES
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    report = classification_report(
        y_test,
        predictions,
        target_names=["good_risk", "bad_risk"],
        output_dict=True,
    )

    joblib.dump(pipeline, MODEL_FILE)

    metadata = {
        "model_type": "LogisticRegression",
        "target_mapping": {
            "0": "good_risk",
            "1": "bad_risk",
        },
        "raw_target_mapping": {
            "1": "good_credit_risk",
            "2": "bad_credit_risk",
        },
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": categorical_features,
        "features_file": str(FEATURES_FILE),
        "target_file": str(TARGET_FILE),
        "model_file": str(MODEL_FILE),
        "accuracy": round(accuracy, 4),
        "roc_auc": round(roc_auc, 4),
        "note": "Portfolio proxy model only. Not suitable for real credit approval decisions.",
    }

    METADATA_FILE.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    return {
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "classification_report": report,
        "model_file": str(MODEL_FILE),
        "metadata_file": str(METADATA_FILE),
    }