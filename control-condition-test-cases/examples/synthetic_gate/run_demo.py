from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from gate import classify_no_effect_variant, known_gap_gate, reference_gate  # noqa: E402


def load_cases() -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "test-cases").rglob("*.json"))]


def main() -> int:
    rows = []
    for case in load_cases():
        variant = case["synthetic_fixture"]["variant"]
        result = reference_gate(variant)
        rows.append((case["case_id"], case["variant_axis"], result.verdict, classify_no_effect_variant(result)))

    print("REFERENCE_GATE")
    for row in rows:
        print(" | ".join(row))

    alternate = next(case for case in load_cases() if case["variant_axis"] == "ENFORCEMENT_PLACEMENT")
    negative = known_gap_gate(alternate["synthetic_fixture"]["variant"])
    print("\nKNOWN_GAP_NEGATIVE_CONTROL")
    print(
        " | ".join(
            [
                alternate["case_id"],
                alternate["variant_axis"],
                negative.verdict,
                classify_no_effect_variant(negative),
            ]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
