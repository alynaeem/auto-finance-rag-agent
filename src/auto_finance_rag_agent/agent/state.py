from typing import Any, Literal, TypedDict


AgentIntent = Literal[
    "policy_qna",
    "loan_calculation",
    "missing_documents",
    "complaint_trends",
    "credit_risk",
    "unknown",
]


class AgentState(TypedDict, total=False):
    user_query: str
    intent: AgentIntent
    input_data: dict[str, Any]
    result: dict[str, Any]
    final_answer: str
    error: str