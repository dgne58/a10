import os
import sys
import unittest


BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")

sys.path.insert(0, os.path.abspath(BACKEND_DIR))
sys.path.insert(0, os.path.abspath(SCRIPTS_DIR))

import router  # noqa: E402
import run_eval  # noqa: E402


class RouterEvalContractTests(unittest.TestCase):
    def test_select_model_returns_mid_tier_for_medium_label(self):
        label = {"complexity": "medium", "domain": "factual"}
        self.assertEqual(
            router.select_model(label),
            "meta-llama/llama-3.1-70b-instruct",
        )

    def test_select_model_routes_project_queries_to_cheap_model(self):
        label = {"complexity": "simple", "domain": "factual"}
        self.assertEqual(
            router.select_model(label),
            "meta-llama/llama-3.1-8b-instruct",
        )

    def test_extract_answer_reads_single_letter(self):
        self.assertEqual(run_eval.extract_answer("The answer is C."), "C")


if __name__ == "__main__":
    unittest.main()
