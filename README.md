Auto Finance RAG Agent
======================

Auto Finance RAG Agent is a FastAPI application for auto-finance policy Q&A,
loan calculations, missing-document checks, complaint trend lookup, and
agent-routed workflows. It combines retrieval over policy documents with
deterministic finance tools and optional MongoDB-backed LangGraph memory.

Features
--------

- Policy Q&A with Chroma retrieval and grounded answer generation.
- OpenRouter-compatible chat generation, defaulting to Qwen 235B.
- Intent classification for routing policy, loan, document, complaint, and
  credit-risk requests.
- Loan payment calculation and loan offer comparison.
- Required-document validation for salaried and self-employed applicants.
- Complaint trend lookup over processed complaint data.
- Optional credit-risk proxy model for portfolio/demo use only.
- FastAPI endpoints plus a mounted Gradio UI at `/demo`.

Project Layout
--------------

```text
src/auto_finance_rag_agent/
  agent/          LangGraph state, nodes, graph, and intent classifier
  api/            FastAPI routes
  generation/     Grounded answer generation and RAG service
  ingestion/      Document loading and chunking
  ml/             Credit-risk model training and prediction
  retrieval/      Chroma vectorstore and retriever
  tools/          Deterministic loan, document, and complaint tools
  ui/             Gradio interface
```

Setup
-----

Create and activate the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Copy the example environment file and fill in secrets:

```bash
cp .env.example .env
```

Core environment variables:

```text
OPENROUTER_API_KEY=...
OPENROUTER_URL=https://openrouter.ai/api/v1
CHAT_MODEL=qwen/qwen3-235b-a22b
CHROMA_DIR=vectorstore/chroma
CHROMA_COLLECTION=auto_finance_policy_chunks
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=auto_finance_rag_agent
```

`WARM_UP_VECTORSTORE=true` is optional. Leave it unset for normal startup so
the API can boot without loading embedding models during application lifespan.

Build Data Artifacts
--------------------

Build or rebuild the policy vectorstore:

```bash
python scripts/build_vectorstore.py
```

Prepare and train the credit-risk proxy model:

```bash
python scripts/prepare_credit_data.py
python scripts/train_credit_model.py
```

Run The API
-----------

Use the project virtual environment, not the base Anaconda interpreter:

```bash
source .venv/bin/activate
python -m uvicorn auto_finance_rag_agent.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

The Gradio UI is mounted at:

```text
http://127.0.0.1:8000/demo
```

API Endpoints
-------------

- `GET /health`
- `POST /ask`
- `POST /calculate-loan`
- `POST /compare-loans`
- `POST /check-missing-documents`
- `POST /agent`

Example loan calculation:

```bash
curl -X POST http://127.0.0.1:8000/calculate-loan \
  -H "Content-Type: application/json" \
  -d '{"amount_financed":20000,"annual_apr":8,"term_months":60}'
```

Example agent request:

```bash
curl -X POST http://127.0.0.1:8000/agent \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "demo-user-001",
    "user_query": "Compare 48 and 60 month loan offers.",
    "input_data": {
      "amount_financed": 20000,
      "annual_apr": 8,
      "terms_months": [48, 60]
    }
  }'
```

Development Checks
------------------

```bash
python -m py_compile src/auto_finance_rag_agent/main.py
ruff check src scripts
```

Notes
-----

- Run commands from the repository root.
- The RAG and agent endpoints require the vectorstore and embedding model to be
  available.
- The `/agent` endpoint requires MongoDB when LangGraph memory is used.
- The credit-risk model is a portfolio proxy model only. It is not suitable for
  real credit approval, underwriting, legal, or financial decisions.
