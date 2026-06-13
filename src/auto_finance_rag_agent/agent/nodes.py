from auto_finance_rag_agent.agent.intent import classify_intent
from auto_finance_rag_agent.agent.state import AgentState


def classify_intent_node(state: AgentState) -> AgentState:
    user_query = state.get("user_query", "").strip()

    if not user_query:
        return {
            "intent": "unknown",
            "error": "User query is missing.",
        }

    intent = classify_intent(user_query)

    return {
        "intent": intent,
    }