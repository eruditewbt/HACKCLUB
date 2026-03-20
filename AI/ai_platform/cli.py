from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from ai_platform.core.config import load_settings
from ai_platform.rag.rag_pipeline import RagPipeline
from ai_platform.rag.sqlite_store import SqliteRagStore
from ai_platform.rag.answer import synthesize_answer


def main(argv: Any = None) -> int:
    p = argparse.ArgumentParser(prog="ai_platform")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest")
    p_ing.add_argument("--org-id", default="default")
    p_ing.add_argument("--doc-id", required=True)
    p_ing.add_argument("--title", required=True)
    p_ing.add_argument("--text", required=True)

    p_ingf = sub.add_parser("ingest-file")
    p_ingf.add_argument("--org-id", default="default")
    p_ingf.add_argument("--path", required=True, help="Path to .txt/.md/.html/.json/.py (stored as text)")
    p_ingf.add_argument("--doc-id", default=None, help="Defaults to filename")
    p_ingf.add_argument("--title", default=None, help="Defaults to filename")

    p_s = sub.add_parser("search")
    p_s.add_argument("--org-id", default="default")
    p_s.add_argument("--query", required=True)
    p_s.add_argument("--top-k", type=int, default=5)

    p_a = sub.add_parser("answer")
    p_a.add_argument("--org-id", default="default")
    p_a.add_argument("--query", required=True)
    p_a.add_argument("--top-k", type=int, default=5)

    args = p.parse_args(argv)

    settings = load_settings()
    store = SqliteRagStore(path=settings.db_path)
    pipe = RagPipeline(store=store, settings=settings)
    pipe.init()

    if args.cmd == "ingest":
        res = pipe.ingest_text(org_id=args.org_id, doc_id=args.doc_id, title=args.title, text=args.text)
        print(json.dumps(res, indent=2))
        return 0

    if args.cmd == "ingest-file":
        import os

        path = str(args.path)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        name = os.path.basename(path)
        doc_id = args.doc_id or name
        title = args.title or name
        res = pipe.ingest_text(
            org_id=args.org_id,
            doc_id=doc_id,
            title=title,
            text=text,
            metadata={"path": os.path.abspath(path)},
        )
        print(json.dumps(res, indent=2))
        return 0

    if args.cmd == "search":
        hits = pipe.search(org_id=args.org_id, query=args.query, top_k=args.top_k)
        print(json.dumps({"hits": hits}, indent=2))
        return 0

    if args.cmd == "answer":
        hits = pipe.search(org_id=args.org_id, query=args.query, top_k=args.top_k)
        ans = synthesize_answer(query=args.query, hits=hits)
        print(json.dumps({"answer": ans, "hits": hits}, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
