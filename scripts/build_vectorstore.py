from auto_finance_rag_agent.ingestion.pipeline import build_document_chunks
from auto_finance_rag_agent.retrieval.vector_store import build_vectorstore


def main() -> None:
    chunks = build_document_chunks()

    print(f"Chunks ready for embedding: {len(chunks)}")

    build_vectorstore(chunks, reset=True)

    print("Vectorstore built successfully.")


if __name__ == "__main__":
    main()