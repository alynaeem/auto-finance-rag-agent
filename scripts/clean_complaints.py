import json
from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/complaints/cfpb_vehicle_loan_lease_500.json")
OUTPUT_FILE = Path("data/processed/complaints_clean.csv")


def extract_complaint_items(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        hits = payload.get("hits", {})

        if isinstance(hits, dict):
            complaint_items = hits.get("hits", [])
            if isinstance(complaint_items, list):
                return complaint_items

    raise ValueError("Unsupported CFPB complaints JSON structure.")


def main() -> None:
    raw_text = RAW_FILE.read_text(encoding="utf-8")
    payload = json.loads(raw_text)

    complaint_items = extract_complaint_items(payload)

    rows = []

    for item in complaint_items:
        source = item.get("_source", {})

        rows.append(
            {
                "date_received": source.get("date_received"),
                "product": source.get("product"),
                "sub_product": source.get("sub_product"),
                "issue": source.get("issue"),
                "sub_issue": source.get("sub_issue"),
                "company": source.get("company"),
                "state": source.get("state"),
                "submitted_via": source.get("submitted_via"),
                "company_response": source.get("company_response"),
                "timely": source.get("timely"),
                "consumer_disputed": source.get("consumer_disputed"),
                "narrative": source.get("complaint_what_happened"),
            }
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Complaints found: {len(rows)}")
    print(f"Saved cleaned CSV to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
