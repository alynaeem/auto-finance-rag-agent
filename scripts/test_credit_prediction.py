import json

from auto_finance_rag_agent.ml.credit_prediction import predict_credit_risk


def main() -> None:
    applicant = {
        "checking_account_status": "A11",
        "duration_months": 48,
        "credit_history": "A34",
        "purpose": "A43",
        "credit_amount": 12000,
        "savings_account": "A61",
        "employment_since": "A73",
        "installment_rate": 4,
        "personal_status_sex": "A93",
        "other_debtors": "A101",
        "present_residence_since": 2,
        "property": "A123",
        "age": 28,
        "other_installment_plans": "A143",
        "housing": "A152",
        "existing_credits": 2,
        "job": "A173",
        "people_liable": 1,
        "telephone": "A191",
        "foreign_worker": "A201",
    }

    result = predict_credit_risk(applicant)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()