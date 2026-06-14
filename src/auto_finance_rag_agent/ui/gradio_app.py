import json
from uuid import uuid4

import gradio as gr

from auto_finance_rag_agent.agent.graph import run_agent


DEFAULT_INPUT_DATA = """{
  "amount_financed": 20000,
  "annual_apr": 8,
  "terms_months": [48, 60]
}"""


def parse_input_data(input_data_text: str) -> dict:
    text = (input_data_text or "").strip()

    if not text:
        return {}

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as error:
        raise gr.Error(f"input_data must be valid JSON: {error}")

    if not isinstance(parsed, dict):
        raise gr.Error("input_data must be a JSON object.")

    return parsed


def respond(
    message: str,
    history: list[dict],
    thread_id: str,
    input_data_text: str,
):
    if not message.strip():
        raise gr.Error("Please enter a message.")

    thread_id = thread_id.strip() or f"demo-{uuid4()}"
    input_data = parse_input_data(input_data_text)

    state = run_agent(
        user_query=message,
        input_data=input_data,
        thread_id=thread_id,
    )

    answer = state.get("final_answer", "No answer generated.")

    history = history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return history, thread_id, ""


def load_example(example_name: str):
    if example_name == "Loan comparison":
        return (
            "Compare 48 and 60 month loan offers.",
            """{
  "amount_financed": 20000,
  "annual_apr": 8,
  "terms_months": [48, 60]
}""",
        )

    if example_name == "Missing documents":
        return (
            "The applicant submitted ID and salary slip. What documents are missing?",
            """{
  "employment_status": "salaried",
  "documents_provided": [
    "identity_document",
    "salary_slip"
  ]
}""",
        )

    if example_name == "Complaint trends":
        return (
            "Show refund complaint trends for auto loans.",
            """{
  "issue_keyword": "refund",
  "top_n": 5
}""",
        )

    if example_name == "Policy Q&A":
        return (
            "What documents are required for a salaried auto finance applicant?",
            "{}",
        )

    return "", "{}"


def create_gradio_app() -> gr.Blocks:
    with gr.Blocks(
        title="Auto Finance RAG Agent",
    ) as demo:
        gr.Markdown(
            """
# Auto Finance RAG Agent

An agentic AI assistant built with **LangGraph**, **RAG**, **Qwen via OpenRouter**, **Chroma**, **MongoDB memory**, deterministic finance tools, complaint analytics, and a proxy credit-risk model.

Use the same `thread_id` to continue a multi-turn conversation.
"""
        )

        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="Agent Conversation",
                    height=520,
                )

                message = gr.Textbox(
                    label="Your message",
                    placeholder="Ask about policies, loan comparison, missing documents, complaints, or credit risk...",
                    lines=3,
                )

                with gr.Row():
                    send_button = gr.Button("Send", variant="primary")
                    clear_button = gr.Button("Clear Chat")

            with gr.Column(scale=1):
                thread_id = gr.Textbox(
                    label="Thread ID",
                    value="demo-user-001",
                    info="Use the same thread ID to keep MongoDB-backed multi-turn memory.",
                )

                input_data = gr.Textbox(
                    label="input_data JSON",
                    value=DEFAULT_INPUT_DATA,
                    lines=14,
                    info="Structured tool inputs. Keep this as valid JSON.",
                )

                example_selector = gr.Dropdown(
                    label="Load demo example",
                    choices=[
                        "Loan comparison",
                        "Missing documents",
                        "Complaint trends",
                        "Policy Q&A",
                    ],
                    value="Loan comparison",
                )

                load_button = gr.Button("Load Example")

        send_button.click(
            fn=respond,
            inputs=[message, chatbot, thread_id, input_data],
            outputs=[chatbot, thread_id, message],
        )

        message.submit(
            fn=respond,
            inputs=[message, chatbot, thread_id, input_data],
            outputs=[chatbot, thread_id, message],
        )

        clear_button.click(
            fn=lambda: [],
            inputs=[],
            outputs=[chatbot],
        )

        load_button.click(
            fn=load_example,
            inputs=[example_selector],
            outputs=[message, input_data],
        )

    return demo
