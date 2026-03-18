import json
import os
import unittest

from dataanalysis_platform.pipelines.orchestration import run_pipeline_csv


class TestPipeline(unittest.TestCase):
    def test_profile_and_validate(self):
        root = os.path.dirname(os.path.dirname(__file__))
        csv_path = os.path.join(root, "datasets", "samples", "sales.csv")
        rules_path = os.path.join(root, "datasets", "samples", "sales.rules.json")

        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)

        art = run_pipeline_csv(
            csv_path=csv_path,
            rules_spec=rules,
            artifacts_dir=os.path.join(root, "artifacts"),
            max_rows=100,
        )
        self.assertIn("run_id", art)
        self.assertIn("profile", art)
        self.assertIn("validation", art)
        self.assertTrue(os.path.exists(art["artifact_path"]))
        self.assertTrue(os.path.exists(art["report_html"]))


if __name__ == "__main__":
    unittest.main()

