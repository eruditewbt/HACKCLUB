# AI (AI Platform)

This directory is evolving into a production-shaped, monetizable **AI platform**:

- Text + document intelligence (RAG, extraction, reporting)
- Code intelligence (repo indexing + search)
- Vision + audio scaffolds (optional dependencies)
- Agent + tool execution scaffolds (ties into your `AUTOMATION/` platform)

## What Works Today (Implemented)

### 1) Local RAG (stdlib-only)
A practical retrieval system using SQLite FTS5:

- Ingest docs into a local SQLite database
- Chunking + metadata
- Search (`bm25`) + citations
- Deterministic answer synthesis (no LLM required)

### 2) AI Gateway Service (optional FastAPI)
A minimal API wrapper that exposes RAG endpoints.

## Quickstart

### CLI

```bash
python -m ai_platform ingest --org-id demo --doc-id intro --title "Intro" --text "Hello world"
python -m ai_platform search --org-id demo --query "hello" --top-k 5
python -m ai_platform answer --org-id demo --query "What is this project?" --top-k 5
```

### API (optional)

```bash
pip install fastapi uvicorn pydantic
uvicorn services.ai_gateway.app:app --reload --port 8010
```

Then:
- `POST /ingest`
- `POST /search`
- `POST /answer`

## Environment

- `AI_DB_PATH` (default: `ai_platform_state/ai_rag.sqlite`)
- `AI_MAX_CHUNK_CHARS` (default: 1200)
- `AI_CHUNK_OVERLAP_CHARS` (default: 150)

## Next (Planned)

- Multi-tenant + API keys
- Doc parsing (PDF/HTML) with optional dependencies
- Better reranking + embeddings (optional)
- Agent execution + guardrails (integrate with `AUTOMATION/` as a tool)
