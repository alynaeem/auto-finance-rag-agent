from collections import Counter

from auto_finance_rag_agent.ingestion.pipeline import build_document_chunks


MAX_CHARS_WARNING = 4000


def main() -> None:
    chunks = build_document_chunks()

    print(f"Total chunks checked: {len(chunks)}")
    print("-" * 80)

    empty_chunks = []
    missing_metadata = []
    large_chunks = []

    for chunk in chunks:
        text = chunk.page_content.strip()
        metadata = chunk.metadata

        if not text:
            empty_chunks.append(metadata.get("chunk_id", "unknown_chunk"))

        required_keys = [
            "source_file",
            "source_type",
            "chunk_id",
            "chunk_strategy",
        ]

        for key in required_keys:
            if not metadata.get(key):
                missing_metadata.append(
                    {
                        "chunk_id": metadata.get("chunk_id", "unknown_chunk"),
                        "missing_key": key,
                    }
                )

        if metadata.get("source_type") == "public_pdf" and metadata.get("page") is None:
            missing_metadata.append(
                {
                    "chunk_id": metadata.get("chunk_id", "unknown_chunk"),
                    "missing_key": "page",
                }
            )

        if metadata.get("source_type") == "synthetic_policy" and not metadata.get("section_path"):
            missing_metadata.append(
                {
                    "chunk_id": metadata.get("chunk_id", "unknown_chunk"),
                    "missing_key": "section_path",
                }
            )

        if len(text) > MAX_CHARS_WARNING:
            large_chunks.append(
                {
                    "chunk_id": metadata.get("chunk_id", "unknown_chunk"),
                    "source_file": metadata.get("source_file"),
                    "length": len(text),
                }
            )

    strategy_counts = Counter(
        chunk.metadata.get("chunk_strategy", "unknown")
        for chunk in chunks
    )

    print("Chunk strategies:")
    for strategy, count in strategy_counts.items():
        print(f"- {strategy}: {count}")

    print("-" * 80)
    print(f"Empty chunks: {len(empty_chunks)}")
    print(f"Missing metadata issues: {len(missing_metadata)}")
    print(f"Large chunk warnings: {len(large_chunks)}")

    if missing_metadata:
        print("-" * 80)
        print("First missing metadata issues:")
        for issue in missing_metadata[:10]:
            print(issue)

    if large_chunks:
        print("-" * 80)
        print("First large chunk warnings:")
        for issue in large_chunks[:10]:
            print(issue)


if __name__ == "__main__":
    main()