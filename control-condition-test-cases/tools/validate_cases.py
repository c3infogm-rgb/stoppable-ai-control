from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "test-cases"

AXES = {
    "REPRESENTATION", "CONFIGURATION", "AUTHORITY", "STATE", "SEQUENCE",
    "TIMING", "TARGET", "PAYLOAD", "RETRY_RECOVERY",
    "ENFORCEMENT_PLACEMENT", "CONTEXT", "MODEL_REVIEWER", "ERROR_PATH",
}
RELATION_MODES = {"ORDERED", "UNORDERED", "DECLARED_ADJACENCY"}
TOP_KEYS = {
    "schema_version", "case_id", "title", "variant_axis", "relation_mode",
    "control_statement", "protected_effect", "baseline_value", "variant_value",
    "comparator_policy", "claim_boundary", "synthetic_fixture",
}
COMPARATOR_KEYS = {
    "invariant", "preserved_if", "counterexample_if", "undefined_if",
    "unobserved_if", "required_evidence",
}
CLAIM_KEYS = {
    "evidence_class", "not_a_safety_claim", "not_a_third_party_finding",
    "single_replay_boundary_forbidden",
}
REQUEST_KEYS = {
    "approval_present", "approval_expiry_epoch", "now_epoch", "approved_target",
    "target", "denied_previously", "retry_count", "sequence", "route",
}
FORBIDDEN_RESULT_KEYS = {
    "result", "verdict", "observed_classification", "boundary", "operating_envelope",
    "safe", "certified", "conformant",
}


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case(data: dict, path: Path) -> list[str]:
    errors: list[str] = []
    extra = set(data) - TOP_KEYS
    missing = TOP_KEYS - set(data)
    if extra:
        errors.append(f"unknown top-level keys: {sorted(extra)}")
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")
    if set(data) & FORBIDDEN_RESULT_KEYS:
        errors.append("planning case must not contain observed/result fields")
    if data.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1")
    if not str(data.get("case_id", "")).startswith("CCG-"):
        errors.append("case_id must start with CCG-")
    if data.get("variant_axis") not in AXES:
        errors.append("variant_axis is not in the 13-axis taxonomy")
    if data.get("relation_mode") not in RELATION_MODES:
        errors.append("invalid relation_mode")
    if data.get("baseline_value") == data.get("variant_value"):
        errors.append("baseline_value and variant_value must differ")

    comparator = data.get("comparator_policy")
    if not isinstance(comparator, dict):
        errors.append("comparator_policy must be an object")
    else:
        if set(comparator) != COMPARATOR_KEYS:
            errors.append("comparator_policy keys must be exact")
        evidence = comparator.get("required_evidence")
        if not isinstance(evidence, list) or not evidence or len(evidence) != len(set(evidence)):
            errors.append("required_evidence must be a non-empty unique list")

    claim = data.get("claim_boundary")
    if not isinstance(claim, dict):
        errors.append("claim_boundary must be an object")
    else:
        if set(claim) != CLAIM_KEYS:
            errors.append("claim_boundary keys must be exact")
        if claim.get("evidence_class") != "GENERIC_PUBLIC_TEST_CASE":
            errors.append("evidence_class must remain GENERIC_PUBLIC_TEST_CASE")
        for key in ("not_a_safety_claim", "not_a_third_party_finding", "single_replay_boundary_forbidden"):
            if claim.get(key) is not True:
                errors.append(f"{key} must be true")

    fixture = data.get("synthetic_fixture")
    if not isinstance(fixture, dict) or set(fixture) != {"baseline", "variant"}:
        errors.append("synthetic_fixture must contain baseline and variant only")
    else:
        for label in ("baseline", "variant"):
            request = fixture.get(label)
            if not isinstance(request, dict) or set(request) != REQUEST_KEYS:
                errors.append(f"{label} synthetic request keys must be exact")
        if fixture.get("baseline") == fixture.get("variant"):
            errors.append("baseline and variant synthetic requests must differ")

    return [f"{path}: {error}" for error in errors]


def validate_all() -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    paths = sorted(CASE_ROOT.rglob("*.json"))
    if len(paths) != 6:
        errors.append(f"expected exactly 6 public cases, found {len(paths)}")
    for path in paths:
        data = load_case(path)
        case_id = data.get("case_id")
        if case_id in seen_ids:
            errors.append(f"duplicate case_id: {case_id}")
        seen_ids.add(case_id)
        errors.extend(validate_case(data, path))
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("PASS generic public test cases: 6/6")
    print("PASS claim ceiling: no observed result, no safety claim, no third-party finding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
