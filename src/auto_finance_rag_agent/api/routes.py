from fastapi import APIRouter
from auto_finance_rag_agent.agent.graph import run_agent
from auto_finance_rag_agent.generation.rag_service import ask_policy_question
from auto_finance_rag_agent.tools.missing_documents import check_missing_documents
from auto_finance_rag_agent.schemas import (
    AgentRequest,
    AgentResponse,
    LoanCalculationRequest,
    LoanCalculationResponse,
    LoanComparisonRequest,
    LoanComparisonResponse,
    MissingDocumentsRequest,
    MissingDocumentsResponse,
    RAGRequest,
    RAGResponse,
)
from auto_finance_rag_agent.tools.loan_calculator import (
    calculate_loan_offer,
    compare_loan_offers,
)


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/ask", response_model=RAGResponse)
def ask(request: RAGRequest) -> RAGResponse:
    return ask_policy_question(
        query=request.question,
        k=request.top_k,
    )


@router.post("/calculate-loan", response_model=LoanCalculationResponse)
def calculate_loan(request: LoanCalculationRequest) -> LoanCalculationResponse:
    result = calculate_loan_offer(
        amount_financed=request.amount_financed,
        annual_apr=request.annual_apr,
        term_months=request.term_months,
    )

    return LoanCalculationResponse(**result)

@router.post("/compare-loans", response_model=LoanComparisonResponse)
def compare_loans(request: LoanComparisonRequest) -> LoanComparisonResponse:
    result = compare_loan_offers(
        amount_financed=request.amount_financed,
        annual_apr=request.annual_apr,
        terms_months=request.terms_months,
    )

    return LoanComparisonResponse(**result)

@router.post("/check-missing-documents", response_model=MissingDocumentsResponse)
def check_documents(request: MissingDocumentsRequest) -> MissingDocumentsResponse:
    result = check_missing_documents(
        employment_status=request.employment_status,
        documents_provided=request.documents_provided,
    )

    return MissingDocumentsResponse(**result)

@router.post("/agent", response_model=AgentResponse)
def run_agent_endpoint(request: AgentRequest) -> AgentResponse:
    state = run_agent(
        user_query=request.user_query,
        input_data=request.input_data,
        thread_id=request.thread_id,
    )

    return AgentResponse(
        thread_id=request.thread_id,
        intent=state.get("intent", "unknown"),
        final_answer=state.get("final_answer", ""),
        result=state.get("result", {}),
    )