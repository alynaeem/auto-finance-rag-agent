import json

from auto_finance_rag_agent.ingestion.chunkers import chunk_markdown_documents
from auto_finance_rag_agent.ingestion.loader import load_markdown_policy_files


def main() -> None:
    markdown_docs = load_markdown_policy_files()
    chunks = chunk_markdown_documents(markdown_docs)

    print(f"Markdown files loaded: {len(markdown_docs)}")
    print(f"Markdown chunks created: {len(chunks)}")
    print("-" * 80)

    first_chunk = chunks[0]

    print("First chunk metadata:")
    print(json.dumps(first_chunk.metadata, indent=2))

    print("-" * 80)
    print("First chunk text preview:")
    print(first_chunk.page_content[:700].replace("\n", " "))


if __name__ == "__main__":
    main()
