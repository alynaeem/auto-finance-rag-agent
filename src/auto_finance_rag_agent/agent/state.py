from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


AgentIntent = Literal[
    "policy_qna",
    "loan_calculation",
    "missing_documents",
    "complaint_trends",
    "credit_risk",
    "unknown",
]


class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    user_query: str
    intent: AgentIntent
    input_data: dict[str, Any]
    result: dict[str, Any]
    final_answer: str
    error: str