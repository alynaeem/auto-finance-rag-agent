from pathlib import Path

import pandas as pd


COMPLAINTS_CSV = Path("data/processed/complaints_clean.csv")


def load_complaints() -> pd.DataFrame:
    return pd.read_csv(COMPLAINTS_CSV)


def lookup_complaint_trends(
    issue_keyword: str | None = None,
    top_n: int = 5,
) -> dict:
    complaints = load_complaints()

    if issue_keyword:
        issue_text = complaints["issue"].fillna("")
        sub_issue_text = complaints["sub_issue"].fillna("")
        narrative_text = complaints["narrative"].fillna("")

        keyword_mask = (
            issue_text.str.contains(issue_keyword, case=False, na=False)
            | sub_issue_text.str.contains(issue_keyword, case=False, na=False)
            | narrative_text.str.contains(issue_keyword, case=False, na=False)
        )

        complaints = complaints[keyword_mask]

    top_issues = (
        complaints["issue"]
        .fillna("Unknown")
        .value_counts()
        .head(top_n)
        .to_dict()
    )

    examples = (
        complaints[
            [
                "date_received",
                "issue",
                "sub_issue",
                "company_response",
                "narrative",
            ]
        ]
        .head(3)
        .fillna("")
        .to_dict("records")
    )

    return {
        "total_matches": len(complaints),
        "top_issues": top_issues,
        "examples": examples,
    }