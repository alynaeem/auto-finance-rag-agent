from pydantic import BaseModel, Field


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
