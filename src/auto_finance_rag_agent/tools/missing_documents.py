REQUIRED_DOCUMENTS_BY_EMPLOYMENT_STATUS = {
    "salaried": [
        "identity_document",
        "salary_slip",
        "employment_verification_letter",
        "recent_bank_statement",
        "vehicle_quotation_or_invoice",
    ],
    "self_employed": [
        "identity_document",
        "business_registration_proof",
        "recent_bank_statement",
        "business_income_evidence",
        "vehicle_quotation_or_invoice",
    ],
}


def check_missing_documents(
    employment_status: str,
    documents_provided: list[str],
) -> dict:
    required_documents = REQUIRED_DOCUMENTS_BY_EMPLOYMENT_STATUS.get(
        employment_status,
        [],
    )

    provided_documents = set(documents_provided)

    missing_documents = [
        document
        for document in required_documents
        if document not in provided_documents
    ]

    is_complete = len(missing_documents) == 0

    return {
        "employment_status": employment_status,
        "required_documents": required_documents,
        "documents_provided": documents_provided,
        "missing_documents": missing_documents,
        "is_complete": is_complete,
    }