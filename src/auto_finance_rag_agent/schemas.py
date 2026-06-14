from pydantic import BaseModel, Field
from typing import Literal
from typing import Any


class RAGRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)


class SourceInfo(BaseModel):
    source_file: str | None = None
    source_type: str | None = None
    page: int | None = None
    section_path: str | None = None
    score: float | None = None
    chunk_id: str | None = None


class RAGResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceInfo]
    safety_note: str

class LoanCalculationRequest(BaseModel):
    amount_financed: float = Field(..., gt=0)
    annual_apr: float = Field(..., ge=0, le=100)
    term_months: int = Field(..., ge=1, le=120)


class LoanCalculationResponse(BaseModel):
    amount_financed: float
    annual_apr: float
    term_months: int
    monthly_payment: float
    total_payment: float
    total_interest: float

class LoanComparisonRequest(BaseModel):
    amount_financed: float = Field(..., gt=0)
    annual_apr: float = Field(..., ge=0, le=100)
    terms_months: list[int] = Field(..., min_length=2)


class LoanComparisonResponse(BaseModel):
    amount_financed: float
    annual_apr: float
    offers: list[LoanCalculationResponse]
    lowest_monthly_payment_term: int
    lowest_total_interest_term: int

class MissingDocumentsRequest(BaseModel):
    employment_status: Literal["salaried", "self_employed"]
    documents_provided: list[str] = Field(default_factory=list)


class MissingDocumentsResponse(BaseModel):
    employment_status: str
    required_documents: list[str]
    documents_provided: list[str]
    missing_documents: list[str]
    is_complete: bool

class AgentRequest(BaseModel):
    user_query: str = Field(..., min_length=1)
    thread_id: str = Field(default="default-thread", min_length=1)
    input_data: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    thread_id: str
    intent: str
    final_answer: str
    result: dict[str, Any] = Field(default_factory=dict)