import os
import sys
import unittest


SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")

sys.path.insert(0, os.path.abspath(SCRIPTS_DIR))
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

import run_humaneval  # noqa: E402


PROMPT = """from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\"Check if any values are close.\"\"\"
"""

TEST = """
def check(candidate):
    assert candidate([1.0, 2.0], 0.5) is False
    assert candidate([1.0, 1.2], 0.3) is True
"""


class RunHumanEvalTests(unittest.TestCase):
    def test_extract_code_preserves_body_indentation(self):
        raw = "    numbers.sort()\n    return False\n"
        self.assertEqual(run_humaneval.extract_code(raw), "    numbers.sort()\n    return False")

    def test_run_tests_accepts_body_only_completion(self):
        completion = (
            "    numbers.sort()\n"
            "    for i in range(len(numbers) - 1):\n"
            "        if numbers[i + 1] - numbers[i] < threshold:\n"
            "            return True\n"
            "    return False\n"
        )
        self.assertTrue(
            run_humaneval.run_tests(PROMPT, completion, TEST, "has_close_elements")
        )

    def test_run_tests_reindents_first_line_when_model_returns_flush_left_body(self):
        completion = (
            "numbers.sort()\n"
            "    for i in range(len(numbers) - 1):\n"
            "        if numbers[i + 1] - numbers[i] < threshold:\n"
            "            return True\n"
            "    return False\n"
        )
        self.assertEqual(
            run_humaneval.normalize_body_completion(completion),
            (
                "numbers.sort()\n"
                "for i in range(len(numbers) - 1):\n"
                "    if numbers[i + 1] - numbers[i] < threshold:\n"
                "        return True\n"
                "return False"
            ),
        )
        self.assertTrue(
            run_humaneval.run_tests(PROMPT, completion, TEST, "has_close_elements")
        )

    def test_run_tests_accepts_full_function_completion(self):
        completion = """
def has_close_elements(numbers: list[float], threshold: float) -> bool:
    numbers.sort()
    for i in range(len(numbers) - 1):
        if numbers[i + 1] - numbers[i] < threshold:
            return True
    return False
""".strip()
        self.assertTrue(
            run_humaneval.run_tests(PROMPT, completion, TEST, "has_close_elements")
        )


if __name__ == "__main__":
    unittest.main()
