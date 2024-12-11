"""
Unit test file.
"""

import os
import unittest
from pathlib import Path

from haystack.run import find_plus_context

HERE = Path(__file__).parent.resolve()
TEST_DIR = HERE / "test_data"
TEXT_TXT = TEST_DIR / "text.txt"

assert TEST_DIR.exists(), f"Test directory not found: {TEST_DIR}"
assert TEXT_TXT.exists(), f"Test file not found: {TEXT_TXT}"

COMMAND = "haystack --term1 this --term2 that"


class CliTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        print(f"Running command: {COMMAND}")
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)

    def test_other(self) -> None:
        for result in find_plus_context("test", Path.cwd(), context_lines=20):
            print(result)


if __name__ == "__main__":
    unittest.main()
