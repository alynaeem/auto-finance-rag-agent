import os

from dotenv import load_dotenv


load_dotenv()

CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen/qwen3-235b-a22b")
CHAT_BASE_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1")
CHAT_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")


def format_contexts(contexts: list[dict]) -> str:
    formatted_parts = []

    for index, context in enumerate(contexts, start=1):
        source_file = context.get("source_file", "unknown source")
        page = context.get("page")
        section_path = context.get("section_path")
        content = context.get("content", "")

        if section_path:
            location = section_path
        elif page is not None:
            location = f"page {page}"
        else:
            location = "unknown location"

        formatted_parts.append(
            f"Source {index}\n"
            f"File: {source_file}\n"
            f"Location: {location}\n"
            f"Content:\n{content}"
        )

    return "\n\n---\n\n".join(formatted_parts)


def generate_grounded_answer(query: str, contexts: list[dict]) -> str:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        api_key=CHAT_API_KEY,
        base_url=CHAT_BASE_URL,
        model=CHAT_MODEL,
        temperature=0.2,
    )

    context_text = format_contexts(contexts)

    prompt = f"""
You are an auto-finance assistant for a portfolio demo.

Answer the user's question using only the provided context.

Rules:
- Do not use outside knowledge.
- If the context is not enough, say that the available context is not enough.
- Do not give legal, financial, or credit approval advice.
- Mention the source file or section you used.
- Keep the answer clear and professional.

User question:
{query}

Retrieved context:
{context_text}
"""

    response = llm.invoke(prompt)

    return response.content
