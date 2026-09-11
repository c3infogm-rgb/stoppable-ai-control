from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "examples" / "synthetic_gate"))

from validate_cases import AXES, validate_all  # noqa: E402
from gate import classify_variant, known_gap_gate, reference_gate  # noqa: E402


class PublicPackTests(unittest.TestCase):
    def test_cases_validate(self) -> None:
        self.assertEqual(validate_all(), [])

    def test_taxonomy_has_13_axes(self) -> None:
        self.assertEqual(len(AXES), 13)

    def test_reference_gate_preserves_all_six_variants(self) -> None:
        paths = sorted((ROOT / "test-cases").rglob("*.json"))
        self.assertEqual(len(paths), 6)
        for path in paths:
            case = json.loads(path.read_text(encoding="utf-8"))
            result = reference_gate(case["synthetic_fixture"]["variant"])
            self.assertEqual(result.verdict, "HOLD", path)
            self.assertFalse(result.permit_issued, path)
            self.assertFalse(result.synthetic_effect_observed, path)
            self.assertEqual(classify_variant(result), "PRESERVED", path)

    def test_known_gap_is_counterexample_on_alternate_route(self) -> None:
        path = ROOT / "test-cases" / "enforcement-placement-alternate-route.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        result = known_gap_gate(case["synthetic_fixture"]["variant"])
        self.assertEqual(result.verdict, "PASS")
        self.assertTrue(result.permit_issued)
        self.assertTrue(result.synthetic_effect_observed)
        self.assertEqual(classify_variant(result), "COUNTEREXAMPLE_OBSERVED")

    def test_cases_do_not_publish_observed_results(self) -> None:
        forbidden = {"result", "verdict", "observed_classification", "boundary", "operating_envelope", "safe"}
        for path in sorted((ROOT / "test-cases").rglob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(forbidden & set(case), path)


if __name__ == "__main__":
    unittest.main()
