import os
from functools import lru_cache
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from auto_finance_rag_agent.agent.nodes import (
    classify_intent_node,
    complaint_trends_node,
    credit_risk_node,
    format_final_answer_node,
    loan_calculation_node,
    missing_documents_node,
    policy_qna_node,
    prepare_turn_node,
    unknown_intent_node,
)
from auto_finance_rag_agent.agent.state import AgentState

if TYPE_CHECKING:
    from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()


def route_by_intent(state: AgentState) -> str:
    intent = state.get("intent", "unknown")

    if intent == "policy_qna":
        return "policy_qna"

    if intent == "loan_calculation":
        return "loan_calculation"

    if intent == "missing_documents":
        return "missing_documents"

    if intent == "complaint_trends":
        return "complaint_trends"

    if intent == "credit_risk":
        return "credit_risk"

    return "unknown"


def create_checkpointer() -> "MongoDBSaver":
    from langgraph.checkpoint.mongodb import MongoDBSaver
    from pymongo import MongoClient

    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_db = os.getenv("MONGODB_DB", "auto_finance_rag_agent")
    server_selection_timeout_ms = int(
        os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000")
    )

    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=server_selection_timeout_ms,
    )

    return MongoDBSaver(
        client,
        db_name=mongodb_db,
    )


def build_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("prepare_turn", prepare_turn_node)
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("policy_qna", policy_qna_node)
    workflow.add_node("loan_calculation", loan_calculation_node)
    workflow.add_node("missing_documents", missing_documents_node)
    workflow.add_node("complaint_trends", complaint_trends_node)
    workflow.add_node("credit_risk", credit_risk_node)
    workflow.add_node("unknown", unknown_intent_node)
    workflow.add_node("format_final_answer", format_final_answer_node)

    workflow.add_edge(START, "prepare_turn")
    workflow.add_edge("prepare_turn", "classify_intent")

    workflow.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "policy_qna": "policy_qna",
            "loan_calculation": "loan_calculation",
            "missing_documents": "missing_documents",
            "complaint_trends": "complaint_trends",
            "credit_risk": "credit_risk",
            "unknown": "unknown",
        },
    )

    workflow.add_edge("policy_qna", "format_final_answer")
    workflow.add_edge("loan_calculation", "format_final_answer")
    workflow.add_edge("missing_documents", "format_final_answer")
    workflow.add_edge("complaint_trends", "format_final_answer")
    workflow.add_edge("credit_risk", "format_final_answer")
    workflow.add_edge("unknown", "format_final_answer")

    workflow.add_edge("format_final_answer", END)

    checkpointer = create_checkpointer()

    return workflow.compile(checkpointer=checkpointer)


@lru_cache(maxsize=1)
def get_agent_graph():
    return build_agent_graph()


class LazyAgentGraph:
    def __getattr__(self, name: str):
        return getattr(get_agent_graph(), name)


agent_graph = LazyAgentGraph()


def run_agent(
    user_query: str,
    input_data: dict | None = None,
    thread_id: str = "default-thread",
) -> AgentState:
    initial_state: AgentState = {
        "user_query": user_query,
        "input_data": input_data or {},
        "messages": [HumanMessage(content=user_query)],
    }

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    return get_agent_graph().invoke(initial_state, config=config)
