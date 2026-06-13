import zipfile
from pathlib import Path

import pandas as pd


RAW_ZIP = Path("data/raw/credit/statlog_german_credit_data.zip")
PROCESSED_DIR = Path("data/processed")

FEATURES_OUTPUT = PROCESSED_DIR / "credit_features.csv"
TARGET_OUTPUT = PROCESSED_DIR / "credit_targets.csv"


COLUMN_NAMES = [
    "checking_account_status",
    "duration_months",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings_account",
    "employment_since",
    "installment_rate",
    "personal_status_sex",
    "other_debtors",
    "present_residence_since",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "people_liable",
    "telephone",
    "foreign_worker",
    "target",
]


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(RAW_ZIP, "r") as zip_file:
        with zip_file.open("german.data") as data_file:
            data = pd.read_csv(
                data_file,
                sep=r"\s+",
                header=None,
                names=COLUMN_NAMES,
            )

    features = data.drop(columns=["target"])
    target = data["target"]

    features.to_csv(FEATURES_OUTPUT, index=False)
    target.to_csv(TARGET_OUTPUT, index=False)

    print(f"Rows loaded: {len(data)}")
    print(f"Features saved to: {FEATURES_OUTPUT}")
    print(f"Targets saved to: {TARGET_OUTPUT}")
    print()
    print("Target distribution:")
    print(target.value_counts().sort_index())


if __name__ == "__main__":
    main()