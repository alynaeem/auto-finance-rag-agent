from auto_finance_rag_agent.generation.rag_service import ask_policy_question


def print_sources(sources) -> None:
    print("Sources:")

    for index, source in enumerate(sources, start=1):
        print(f"{index}. {source.source_file}")
        print(f"   Type: {source.source_type}")

        if source.section_path:
            print(f"   Section: {source.section_path}")
        elif source.page is not None:
            print(f"   Page: {source.page}")

        if source.score is not None:
            print(f"   Score: {source.score:.4f}")

        print()


def main() -> None:
    query = "What documents are required for a salaried auto finance applicant?"

    result = ask_policy_question(query, k=3)

    print("=" * 80)
    print("Question:")
    print(result.query)

    print("=" * 80)
    print("Answer:")
    print(result.answer)

    print("=" * 80)
    print_sources(result.sources)

    print("=" * 80)
    print("Safety note:")
    print(result.safety_note)


if __name__ == "__main__":
    main()