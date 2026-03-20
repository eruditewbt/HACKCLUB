import os
import tempfile
import unittest

from ai_platform.core.config import Settings
from ai_platform.rag.rag_pipeline import RagPipeline
from ai_platform.rag.sqlite_store import SqliteRagStore


class TestRag(unittest.TestCase):
    def test_ingest_and_search(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = os.path.join(td, "rag.sqlite")
            settings = Settings(db_path=db_path, max_chunk_chars=200, chunk_overlap_chars=20)
            pipe = RagPipeline(store=SqliteRagStore(path=db_path), settings=settings)
            pipe.init()

            pipe.ingest_text(org_id="o", doc_id="d", title="t", text="hello world\n\nthis is a test")
            hits = pipe.search(org_id="o", query="hello", top_k=5)
            self.assertTrue(len(hits) >= 1)
            self.assertIn("chunk_id", hits[0])


if __name__ == "__main__":
    unittest.main()
