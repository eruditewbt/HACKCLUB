import json
import os
import tempfile
import unittest
import uuid

from automation.engine.runner import WorkflowRunner
from automation.engine.workflow import load_workflow
from automation.tasks import default_registry


class TestRunner(unittest.TestCase):
    def test_run_echo(self):
        with tempfile.TemporaryDirectory() as td:
            wf_path = os.path.join(td, "wf.json")
            with open(wf_path, "w", encoding="utf-8") as f:
                json.dump({
                    "workflow_id": "t",
                    "tasks": [{"id": "a", "type": "core.echo", "inputs": {"message": "hello"}, "retry": {"max_attempts": 1}}]
                }, f)

            wf = load_workflow(wf_path)
            r = WorkflowRunner(registry=default_registry())
            run_id = uuid.uuid4().hex
            summary = r.run(wf=wf, run_id=run_id, org_id="demo", artifacts_root=os.path.join(td, "artifacts"), state_root=os.path.join(td, "state"))
            self.assertTrue(summary.ok)
            self.assertIn("a", summary.tasks)


if __name__ == "__main__":
    unittest.main()
