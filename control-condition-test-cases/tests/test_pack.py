from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "examples" / "synthetic_gate"))

from validate_cases import AXES, load_case, validate_all, validate_case, validate_manifest  # noqa: E402
from gate import classify_no_effect_variant, known_gap_gate, reference_gate  # noqa: E402


class PublicPackTests(unittest.TestCase):
    def test_cases_validate(self) -> None:
        self.assertEqual(validate_all(), [])

    def test_taxonomy_has_13_axes(self) -> None:
        self.assertEqual(len(AXES), 13)

    def test_machine_readable_docs_parse_and_manifest_is_zero_effect(self) -> None:
        json.loads((ROOT / "schema" / "test-case.schema.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["case_count"], 6)
        self.assertTrue(all(value is False for value in manifest["authority_ceiling"].values()))

    def test_reference_gate_preserves_all_six_variants(self) -> None:
        paths = sorted((ROOT / "test-cases").rglob("*.json"))
        self.assertEqual(len(paths), 6)
        for path in paths:
            case = load_case(path)
            result = reference_gate(case["synthetic_fixture"]["variant"])
            self.assertEqual(result.verdict, "HOLD", path)
            self.assertFalse(result.permit_issued, path)
            self.assertFalse(result.synthetic_effect_observed, path)
            self.assertEqual(classify_no_effect_variant(result), "PRESERVED", path)

    def test_known_gap_is_counterexample_on_alternate_route(self) -> None:
        path = ROOT / "test-cases" / "enforcement-placement-alternate-route.json"
        case = load_case(path)
        result = known_gap_gate(case["synthetic_fixture"]["variant"])
        self.assertEqual(result.verdict, "PASS")
        self.assertTrue(result.permit_issued)
        self.assertTrue(result.synthetic_effect_observed)
        self.assertEqual(classify_no_effect_variant(result), "COUNTEREXAMPLE_OBSERVED")

    def test_cases_do_not_publish_observed_results(self) -> None:
        forbidden = {"result", "verdict", "observed_classification", "boundary", "operating_envelope", "safe"}
        for path in sorted((ROOT / "test-cases").rglob("*.json")):
            case = load_case(path)
            self.assertFalse(forbidden & set(case), path)

    def test_unknown_axis_fails_closed(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["variant_axis"] = "NOT_AN_AXIS"
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("13-axis taxonomy" in error for error in errors))

    def test_claim_widening_fails_closed(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["claim_boundary"]["not_a_safety_claim"] = False
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("not_a_safety_claim must be true" in error for error in errors))

    def test_observed_result_field_fails_closed(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["observed_classification"] = "PRESERVED"
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("observed/result fields" in error for error in errors))

    def test_empty_title_fails_schema_mirror_validation(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["title"] = ""
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("title must be a non-empty string" in error for error in errors))

    def test_numeric_control_statement_fails_schema_mirror_validation(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["control_statement"] = 123
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("control_statement must be a non-empty string" in error for error in errors))

    def test_incomplete_case_id_fails_schema_mirror_validation(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["case_id"] = "CCG-"
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("case_id must match" in error for error in errors))

    def test_non_object_case_document_fails_closed(self) -> None:
        errors = validate_case(["not", "an", "object"], Path("synthetic"))
        self.assertTrue(any("case document must be an object" in error for error in errors))

    def test_unhashable_case_id_fails_without_crashing(self) -> None:
        path = ROOT / "test-cases" / "authority-approval-missing.json"
        case = copy.deepcopy(load_case(path))
        case["case_id"] = ["CCG", "BAD"]
        errors = validate_case(case, Path("synthetic"))
        self.assertTrue(any("case_id must match" in error for error in errors))

    def test_manifest_case_ids_must_match_discovered_ids(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        discovered = list(manifest["case_ids"])
        mutated = copy.deepcopy(manifest)
        mutated["case_ids"][0] = "CCG-STALE-001"
        errors = validate_manifest(mutated, discovered)
        self.assertTrue(any("case_ids do not match" in error for error in errors))

    def test_manifest_case_count_must_match_discovered_count(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        discovered = list(manifest["case_ids"])
        mutated = copy.deepcopy(manifest)
        mutated["case_count"] = 5
        errors = validate_manifest(mutated, discovered)
        self.assertTrue(any("case_count" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
