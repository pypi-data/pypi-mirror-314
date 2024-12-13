from __future__ import annotations

import unittest
from pathlib import Path

import pyisg


class TestIdentity(unittest.TestCase):
    maxDiff = None

    def test_example_1(self):
        p = Path("tests/rsc/example.1.isg")
        expected = p.read_text()

        obj = pyisg.loads(expected)
        actual = pyisg.dumps(obj)

        self.assertEqual(expected, actual)

    def test_example_1_3_ncols(self):
        p = Path("tests/rsc/example.1.3 ncols.isg")
        expected = p.read_text()

        obj = pyisg.loads(expected)
        actual = pyisg.dumps(obj)

        self.assertEqual(expected, actual)

    def test_example_2(self):
        p = Path("tests/rsc/example.2.isg")
        expected = p.read_text()

        obj = pyisg.loads(expected)
        actual = pyisg.dumps(obj)

        self.assertEqual(expected, actual)

    def test_example_3(self):
        p = Path("tests/rsc/example.3.isg")
        expected = p.read_text()

        obj = pyisg.loads(expected)
        actual = pyisg.dumps(obj)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
