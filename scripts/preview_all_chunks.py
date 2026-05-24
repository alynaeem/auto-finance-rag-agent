import json
from collections import Counter

from auto_finance_rag_agent.ingestion.pipeline import build_document_chunks


def main() -> None:
    chunks = build_document_chunks()

    print(f"Total chunks created: {len(chunks)}")
    print("-" * 80)

    source_counts = Counter(
        chunk.metadata.get("source_file", "unknown")
        for chunk in chunks
    )

    strategy_counts = Counter(
        chunk.metadata.get("chunk_strategy", "unknown")
        for chunk in chunks
    )

    print("Chunks by source file:")
    for source_file, count in source_counts.items():
        print(f"- {source_file}: {count}")

    print("-" * 80)

    print("Chunks by strategy:")
    for strategy, count in strategy_counts.items():
        print(f"- {strategy}: {count}")

    print("-" * 80)

    first_chunk = chunks[0]

    print("First chunk metadata:")
    print(json.dumps(first_chunk.metadata, indent=2))

    print("-" * 80)
    print("First chunk text preview:")
    print(first_chunk.page_content[:700].replace("\n", " "))


if __name__ == "__main__":
    main()