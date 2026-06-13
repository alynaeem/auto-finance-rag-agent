import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from auto_finance_rag_agent.agent.state import AgentIntent

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI


load_dotenv()


LOAN_CALCULATION_KEYWORDS = [
    "monthly payment",
    "calculate loan",
    "loan payment",
    "apr",
    "interest",
    "loan term",
    "compare loan",
    "compare loans",
    "48 month",
    "60 month",
]


MISSING_DOCUMENT_KEYWORDS = [
    "documents are missing",
    "missing document",
    "missing documents",
    "documents missing",
    "what is missing",
    "submitted",
    "provided documents",
    "submitted documents",
]


COMPLAINT_TREND_KEYWORDS = [
    "complaint",
    "complaints",
    "refund",
    "repossession",
    "credit reporting",
    "add-on cancellation",
    "consumer dispute",
]


CREDIT_RISK_KEYWORDS = [
    "credit risk",
    "risk score",
    "risk level",
    "predict risk",
    "bad risk",
    "good risk",
    "manual review risk",
]


POLICY_QNA_KEYWORDS = [
    "policy",
    "required documents",
    "documents required",
    "eligibility",
    "manual review",
    "auto finance",
    "salaried applicant",
    "self employed applicant",
]


class IntentClassification(BaseModel):
    intent: AgentIntent = Field(
        description="The best matching intent for the user's request."
    )
    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score from 0 to 1.",
    )
    reason: str = Field(
        description="Brief reason for the selected intent."
    )


def normalize_query(user_query: str) -> str:
    return user_query.lower().strip()


def contains_any_keyword(query: str, keywords: list[str]) -> bool:
    return any(keyword in query for keyword in keywords)


def classify_intent_with_keywords(user_query: str) -> AgentIntent:
    query = normalize_query(user_query)

    if contains_any_keyword(query, MISSING_DOCUMENT_KEYWORDS):
        return "missing_documents"

    if contains_any_keyword(query, LOAN_CALCULATION_KEYWORDS):
        return "loan_calculation"

    if contains_any_keyword(query, COMPLAINT_TREND_KEYWORDS):
        return "complaint_trends"

    if contains_any_keyword(query, CREDIT_RISK_KEYWORDS):
        return "credit_risk"

    if contains_any_keyword(query, POLICY_QNA_KEYWORDS):
        return "policy_qna"

    return "unknown"


def get_intent_classifier_llm() -> "ChatOpenAI":
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_URL"),
        model=os.getenv("OPENROUTER_MODEL"),
        temperature=0,
    )


def classify_intent_with_llm(user_query: str) -> IntentClassification:
    llm = get_intent_classifier_llm()
    structured_llm = llm.with_structured_output(IntentClassification)

    prompt = f"""
You are an intent classifier for an auto-finance AI assistant.

Classify the user's request into exactly one of these intents:

1. policy_qna
Use this when the user asks about auto-finance policies, eligibility, required documents, manual review rules, add-on product rules, or general policy questions.

2. loan_calculation
Use this when the user asks to calculate monthly payments, APR, interest, loan terms, total payment, or compare loan offers.

3. missing_documents
Use this when the user gives documents already submitted and asks what is missing or whether the application file is complete.

4. complaint_trends
Use this when the user asks about customer complaints, complaint patterns, refunds, disputes, repossession complaints, or complaint trends.

5. credit_risk
Use this when the user asks to predict credit risk, risk score, bad risk, good risk, or whether an applicant should go to manual review based on risk.

6. unknown
Use this when the request does not fit any of the above.

User request:
{user_query}
"""

    return structured_llm.invoke(prompt)


def classify_intent(user_query: str) -> AgentIntent:
    try:
        classification = classify_intent_with_llm(user_query)

        if classification.confidence >= 0.6:
            return classification.intent

        return classify_intent_with_keywords(user_query)

    except (ValidationError, Exception):
        return classify_intent_with_keywords(user_query)
