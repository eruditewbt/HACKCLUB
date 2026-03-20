from __future__ import annotations

from typing import Any, Dict, List

from ai_platform.rag.answer import synthesize_answer


def generate_brief(*, query: str, hits: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a structured brief from retrieved context.

    Deterministic scaffolding (no LLM). Later you can swap in an LLM-based generator.
    """

    ans = synthesize_answer(query=query, hits=hits, max_sentences=8)
    issues = []
    recs = []
    if not ans.get("answer"):
        issues.append("Insufficient context found for the question.")
        recs.append("Ingest more documents or refine the query terms.")
    else:
        recs.append("Validate the cited chunks and convert them into explicit requirements." )
        recs.append("Turn requirements into tasks/workflows (tie into AUTOMATION platform).")

    return {
        "question": query,
        "executive_summary": ans.get("answer"),
        "key_issues": issues,
        "recommendations": recs,
        "citations": ans.get("citations"),
    }
