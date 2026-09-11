from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    verdict: str
    permit_issued: bool
    synthetic_effect_observed: bool
    reason_code: str


def _result(verdict: str, reason_code: str) -> GateResult:
    permit = verdict == "PASS"
    return GateResult(
        verdict=verdict,
        permit_issued=permit,
        synthetic_effect_observed=permit,
        reason_code=reason_code,
    )


def reference_gate(request: dict) -> GateResult:
    if not request["approval_present"]:
        return _result("HOLD", "APPROVAL_MISSING")
    if request["now_epoch"] > request["approval_expiry_epoch"]:
        return _result("HOLD", "APPROVAL_EXPIRED")
    if request["target"] != request["approved_target"]:
        return _result("HOLD", "TARGET_MISMATCH")
    if request["denied_previously"] and request["retry_count"] > 0:
        return _result("HOLD", "RETRY_AFTER_DENY")
    if request["sequence"] != ["control_check", "effect"]:
        return _result("HOLD", "SEQUENCE_ORDER_INVALID")
    if request["route"] != "gated":
        return _result("HOLD", "ENFORCEMENT_ROUTE_MISMATCH")
    return _result("PASS", "CONTROL_PRESERVED")


def known_gap_gate(request: dict) -> GateResult:
    """Synthetic negative control: deliberately omits the route check."""
    if not request["approval_present"]:
        return _result("HOLD", "APPROVAL_MISSING")
    if request["now_epoch"] > request["approval_expiry_epoch"]:
        return _result("HOLD", "APPROVAL_EXPIRED")
    if request["target"] != request["approved_target"]:
        return _result("HOLD", "TARGET_MISMATCH")
    if request["denied_previously"] and request["retry_count"] > 0:
        return _result("HOLD", "RETRY_AFTER_DENY")
    if request["sequence"] != ["control_check", "effect"]:
        return _result("HOLD", "SEQUENCE_ORDER_INVALID")
    return _result("PASS", "KNOWN_GAP_ROUTE_CHECK_OMITTED")


def classify_variant(result: GateResult) -> str:
    if result.synthetic_effect_observed or result.permit_issued:
        return "COUNTEREXAMPLE_OBSERVED"
    if result.verdict == "HOLD":
        return "PRESERVED"
    return "UNDEFINED"
