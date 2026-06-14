from auto_finance_rag_agent.agent.intent import classify_intent
from langchain_core.messages import AIMessage
from auto_finance_rag_agent.agent.state import AgentState
from auto_finance_rag_agent.generation.rag_service import ask_policy_question
from auto_finance_rag_agent.ml.credit_prediction import predict_credit_risk
from auto_finance_rag_agent.tools.complaint_trends import lookup_complaint_trends
from auto_finance_rag_agent.tools.loan_calculator import (
    calculate_loan_offer,
    compare_loan_offers,
)
from auto_finance_rag_agent.tools.missing_documents import check_missing_documents


def prepare_turn_node(state: AgentState) -> AgentState:
    return {
        "intent": "unknown",
        "result": {},
        "final_answer": "",
        "error": "",
    }


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


def policy_qna_node(state: AgentState) -> AgentState:
    user_query = state.get("user_query", "").strip()

    if not user_query:
        return {
            "error": "User query is required for policy Q&A.",
        }

    result = ask_policy_question(
        query=user_query,
        k=3,
    )

    return {
        "result": result.model_dump(),
    }


def loan_calculation_node(state: AgentState) -> AgentState:
    input_data = state.get("input_data", {})

    amount_financed = input_data.get("amount_financed")
    annual_apr = input_data.get("annual_apr")
    term_months = input_data.get("term_months")
    terms_months = input_data.get("terms_months")

    if amount_financed is None or annual_apr is None:
        return {
            "error": "Loan calculation requires amount_financed and annual_apr.",
        }

    if terms_months:
        result = compare_loan_offers(
            amount_financed=amount_financed,
            annual_apr=annual_apr,
            terms_months=terms_months,
        )
    elif term_months:
        result = calculate_loan_offer(
            amount_financed=amount_financed,
            annual_apr=annual_apr,
            term_months=term_months,
        )
    else:
        return {
            "error": "Loan calculation requires term_months or terms_months.",
        }

    return {
        "result": result,
    }


def missing_documents_node(state: AgentState) -> AgentState:
    input_data = state.get("input_data", {})

    employment_status = input_data.get("employment_status")
    documents_provided = input_data.get("documents_provided", [])

    if not employment_status:
        return {
            "error": "Missing document check requires employment_status.",
        }

    result = check_missing_documents(
        employment_status=employment_status,
        documents_provided=documents_provided,
    )

    return {
        "result": result,
    }


def complaint_trends_node(state: AgentState) -> AgentState:
    input_data = state.get("input_data", {})

    issue_keyword = input_data.get("issue_keyword")
    top_n = input_data.get("top_n", 5)

    result = lookup_complaint_trends(
        issue_keyword=issue_keyword,
        top_n=top_n,
    )

    return {
        "result": result,
    }


def credit_risk_node(state: AgentState) -> AgentState:
    input_data = state.get("input_data", {})

    if not input_data:
        return {
            "error": "Credit risk prediction requires applicant input_data.",
        }

    result = predict_credit_risk(input_data)

    return {
        "result": result,
    }


def unknown_intent_node(state: AgentState) -> AgentState:
    return {
        "error": "I could not identify which auto-finance task this request belongs to.",
    }


def format_final_answer_node(state: AgentState) -> AgentState:
    error = state.get("error")

    if error:
        final_answer = f"Unable to complete the request: {error}"

        return {
            "final_answer": final_answer,
            "messages": [AIMessage(content=final_answer)],
        }

    intent = state.get("intent")
    result = state.get("result", {})

    if intent == "policy_qna":
        final_answer = result.get("answer", "No policy answer was generated.")

    elif intent == "loan_calculation":
        final_answer = format_loan_answer(result)

    elif intent == "missing_documents":
        final_answer = format_missing_documents_answer(result)

    elif intent == "complaint_trends":
        final_answer = format_complaint_trends_answer(result)

    elif intent == "credit_risk":
        final_answer = format_credit_risk_answer(result)

    else:
        final_answer = "I could not complete this request."

    return {
        "final_answer": final_answer,
        "messages": [AIMessage(content=final_answer)],
    }

def format_loan_answer(result: dict) -> str:
    if "offers" in result:
        lines = [
            "Loan comparison result:",
            "",
        ]

        for offer in result["offers"]:
            lines.append(
                f"- {offer['term_months']} months: "
                f"monthly payment {offer['monthly_payment']}, "
                f"total interest {offer['total_interest']}"
            )

        lines.append("")
        lines.append(
            f"Lowest monthly payment: {result['lowest_monthly_payment_term']} months."
        )
        lines.append(
            f"Lowest total interest: {result['lowest_total_interest_term']} months."
        )

        return "\n".join(lines)

    return (
        f"Loan calculation result:\n\n"
        f"- Amount financed: {result['amount_financed']}\n"
        f"- APR: {result['annual_apr']}%\n"
        f"- Term: {result['term_months']} months\n"
        f"- Monthly payment: {result['monthly_payment']}\n"
        f"- Total payment: {result['total_payment']}\n"
        f"- Total interest: {result['total_interest']}"
    )


def format_missing_documents_answer(result: dict) -> str:
    if result.get("is_complete"):
        return "The application file is complete. No required documents are missing."

    missing_documents = result.get("missing_documents", [])

    lines = [
        "The application file is incomplete.",
        "",
        "Missing documents:",
    ]

    for document in missing_documents:
        lines.append(f"- {document}")

    return "\n".join(lines)


def format_complaint_trends_answer(result: dict) -> str:
    lines = [
        f"Complaint trend matches found: {result.get('total_matches', 0)}",
        "",
        "Top complaint issues:",
    ]

    top_issues = result.get("top_issues", {})

    for issue, count in top_issues.items():
        lines.append(f"- {issue}: {count}")

    return "\n".join(lines)


def format_credit_risk_answer(result: dict) -> str:
    return (
        f"Credit risk prediction result:\n\n"
        f"- Prediction: {result.get('prediction_label')}\n"
        f"- Probability of bad risk: {result.get('probability_bad_risk')}\n"
        f"- Risk level: {result.get('risk_level')}\n"
        f"- Manual review recommended: {result.get('manual_review_recommended')}\n\n"
        f"{result.get('note')}"
    )