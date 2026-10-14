#!/usr/bin/env python3
"""Validate the structure of a persisted paper-review record (paper_review_record_v1).

The validator checks completeness and controlled vocabulary only: required
core gates for the level, allowed venue gates, enums, snapshot binding, and
that official-source URLs start with the venue's declared official prefixes.
It cannot establish scientific validity, evidence truth, submission readiness
or likely acceptance.

Usage:
    python3 validate_review_record.py REVIEW-RECORD.json
    python3 validate_review_record.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA = "paper_review_record_v1"
LEVELS = {"L1", "L2", "L1+L2", "L3"}
GATE_STATUSES = {"PASS", "PARTIAL", "FAIL", "ABSTAIN"}
TIERS = {
    "P3_STRONG",
    "P2_VIABLE_CONDITIONAL",
    "P1_WEAK_OR_UNFOCUSED",
    "P0_NO_GO_CURRENT_DIRECTION",
    "PU_ABSTAIN",
}
TIER_BASES = {"prospective", "evidence"}
EXPERIMENT_DECISIONS = {
    "NO_MORE_CORE_EXPERIMENTS",
    "ANALYSIS_ONLY",
    "TARGETED_EXPERIMENTS",
    "MAJOR_REDESIGN",
    "ABSTAIN_MISSING_INPUTS",
}
RECOMMENDATIONS = {
    "GO_INTERNAL_REVIEW",
    "GO_AFTER_TARGETED_REVISIONS",
    "NO_GO_MAJOR_REVISION",
    "NO_GO_EVIDENCE_GAP",
    "ABSTAIN_INCOMPLETE_MANUSCRIPT",
}
OFFICIAL_STATUSES = {"VERIFIED_CURRENT", "ABSTAIN_NOT_VERIFIED", "NOT_REQUESTED"}
FRAMING_SELECTIONS = {"A", "B", "NO_CREDIBLE_FRAMING", "ABSTAIN"}

L1_GATES = {f"L1-G{i}" for i in range(10)}
L2_GATES = {f"L2-G{i}" for i in range(10)}
L3_GATES = {f"L3-G{i}" for i in range(10)}
VENUE_GATE_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-L[123])?-G\d+$")

FORBIDDEN_KEYS = {
    "acceptance_probability",
    "predicted_acceptance_rate",
    "probability_of_acceptance",
    "estimated_acceptance_chance",
}


def is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def find_forbidden_keys(value: Any, prefix: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            if str(key).strip().lower() in FORBIDDEN_KEYS:
                found.append(path)
            found.extend(find_forbidden_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_forbidden_keys(child, f"{prefix}[{index}]"))
    return found


def validate(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["root must be a JSON object"]

    for path in find_forbidden_keys(record):
        errors.append(f"forbidden acceptance-prediction key: {path}")

    if record.get("schema") != SCHEMA:
        errors.append(f"schema must equal {SCHEMA}")

    level = record.get("review_level")
    if level not in LEVELS:
        errors.append(f"review_level must be one of {sorted(LEVELS)}")
    if not is_iso_date(record.get("review_date")):
        errors.append("review_date must be an ISO date (YYYY-MM-DD)")

    prefixes: list[str] = []
    target = record.get("target")
    if not isinstance(target, dict):
        errors.append("target must be an object")
    else:
        if not nonempty_string(target.get("venue")):
            errors.append("target.venue must be a non-empty abbreviation such as TSE or ICSE")
        if not nonempty_string(target.get("name")):
            errors.append("target.name must be the venue's full name")
        if not nonempty_string(target.get("profile")):
            errors.append("target.profile must name the venue profile file or 'generic'")
        raw_prefixes = target.get("official_source_prefixes")
        if not isinstance(raw_prefixes, list) or not all(nonempty_string(p) for p in raw_prefixes):
            errors.append("target.official_source_prefixes must be a list of official URL prefixes (may be empty only for NOT_REQUESTED)")
        else:
            prefixes = [p.strip() for p in raw_prefixes]
            for prefix in prefixes:
                if not prefix.startswith("https://"):
                    errors.append(f"official source prefix must be an https URL: {prefix}")

    snapshot = record.get("snapshot")
    if not isinstance(snapshot, dict):
        errors.append("snapshot must be an object")
    else:
        for field in ("repository_or_source", "branch", "head", "worktree_status"):
            if not nonempty_string(snapshot.get(field)):
                errors.append(f"snapshot.{field} must be a non-empty string (use NOT_APPLICABLE when there is no repository)")
        head = snapshot.get("head")
        if nonempty_string(head) and head != "NOT_APPLICABLE" and not re.fullmatch(r"[0-9a-fA-F]{40}", head):
            errors.append("snapshot.head must be a full 40-character Git hash or NOT_APPLICABLE")
        hashes = snapshot.get("manuscript_hashes", {})
        if not isinstance(hashes, dict):
            errors.append("snapshot.manuscript_hashes must be an object when present")
        else:
            for path, digest in hashes.items():
                if not nonempty_string(path) or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                    errors.append(f"invalid SHA-256 entry in snapshot.manuscript_hashes: {path!r}")

    gate_results = record.get("gate_results")
    gate_ids: set[str] = set()
    if not isinstance(gate_results, list) or not gate_results:
        errors.append("gate_results must be a non-empty list")
    else:
        for index, gate in enumerate(gate_results):
            location = f"gate_results[{index}]"
            if not isinstance(gate, dict):
                errors.append(f"{location} must be an object")
                continue
            gate_id = gate.get("id")
            if not nonempty_string(gate_id):
                errors.append(f"{location}.id must be a non-empty string")
            elif gate_id in gate_ids:
                errors.append(f"duplicate gate id: {gate_id}")
            else:
                gate_ids.add(gate_id)
                if gate_id not in L1_GATES | L2_GATES | L3_GATES and not VENUE_GATE_RE.match(gate_id):
                    errors.append(f"{location}.id {gate_id!r} is neither a core gate (L1-G0..L3-G9) nor a venue gate (<VENUE>-G<n>)")
            if gate.get("status") not in GATE_STATUSES:
                errors.append(f"{location}.status must be one of {sorted(GATE_STATUSES)}")
            evidence = gate.get("evidence")
            if not isinstance(evidence, list) or not evidence or not all(nonempty_string(item) for item in evidence):
                errors.append(f"{location}.evidence must contain at least one non-empty pointer or abstention reason")
            if not nonempty_string(gate.get("impact")):
                errors.append(f"{location}.impact must be a non-empty string")

    if level == "L1":
        required = L1_GATES
    elif level in {"L2", "L1+L2"}:
        required = L1_GATES | L2_GATES
    elif level == "L3":
        required = L3_GATES
    else:
        required = set()
    missing = sorted(required - gate_ids)
    if missing:
        errors.append(f"missing required gates for {level}: {', '.join(missing)}")

    framing = record.get("framing")
    if not isinstance(framing, dict):
        errors.append("framing must be an object")
    else:
        if not nonempty_string(framing.get("a")):
            errors.append("framing.a must be a non-empty string")
        if not nonempty_string(framing.get("b")):
            errors.append("framing.b must be a non-empty string or NO_CREDIBLE_ALTERNATIVE")
        if framing.get("selection") not in FRAMING_SELECTIONS:
            errors.append(f"framing.selection must be one of {sorted(FRAMING_SELECTIONS)}")

    if record.get("potential_tier") not in TIERS:
        errors.append(f"potential_tier must be one of {sorted(TIERS)}")
    if record.get("tier_basis") not in TIER_BASES:
        errors.append(f"tier_basis must be one of {sorted(TIER_BASES)} (prospective = R1 before experiments)")
    if record.get("experiment_decision") not in EXPERIMENT_DECISIONS:
        errors.append(f"experiment_decision must be one of {sorted(EXPERIMENT_DECISIONS)}")

    findings = record.get("major_findings")
    if not isinstance(findings, list) or not findings or not all(nonempty_string(item) for item in findings):
        errors.append("major_findings must contain at least one non-empty finding")
    questions = record.get("author_questions")
    if not isinstance(questions, list) or not all(nonempty_string(item) for item in questions):
        errors.append("author_questions must be a list of non-empty strings (an empty list is allowed)")
    if not nonempty_string(record.get("next_stop_rule")):
        errors.append("next_stop_rule must be a non-empty string")

    official = record.get("official_requirements")
    if not isinstance(official, dict):
        errors.append("official_requirements must be an object")
    else:
        status = official.get("status")
        if status not in OFFICIAL_STATUSES:
            errors.append(f"official_requirements.status must be one of {sorted(OFFICIAL_STATUSES)}")
        if level == "L3" and status == "NOT_REQUESTED":
            errors.append("L3 may not use NOT_REQUESTED for current official requirements")
        verified_at = official.get("verified_at")
        sources = official.get("sources")
        if not isinstance(sources, list) or not all(nonempty_string(item) for item in sources):
            errors.append("official_requirements.sources must be a list of non-empty URLs")
            sources = []
        if status in {"VERIFIED_CURRENT", "ABSTAIN_NOT_VERIFIED"}:
            if not is_iso_date(verified_at):
                errors.append("verified_at must record the verification or attempted-access date")
            if not sources:
                errors.append("current or abstained official checks must list the attempted official sources")
            if not prefixes:
                errors.append("target.official_source_prefixes must be declared when official requirements were checked")
            for source in sources:
                if prefixes and not any(source.startswith(prefix) for prefix in prefixes):
                    errors.append(f"source is not under a declared official prefix: {source}")
        elif status == "NOT_REQUESTED" and verified_at is not None:
            errors.append("verified_at must be null when official requirements were not requested")

    if level == "L3":
        if record.get("recommendation") not in RECOMMENDATIONS:
            errors.append(f"L3 recommendation must be one of {sorted(RECOMMENDATIONS)}")
    elif "recommendation" in record and record.get("recommendation") not in RECOMMENDATIONS:
        errors.append(f"recommendation must be one of {sorted(RECOMMENDATIONS)}")

    return errors


def make_self_test_record() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "review_level": "L1",
        "review_date": "2026-10-10",
        "target": {
            "venue": "TSE",
            "name": "IEEE Transactions on Software Engineering",
            "profile": "references/venues/tse.md",
            "official_source_prefixes": ["https://example.org/journals/tse"],
        },
        "snapshot": {
            "repository_or_source": "supplied manuscript",
            "branch": "NOT_APPLICABLE",
            "head": "NOT_APPLICABLE",
            "worktree_status": "NOT_APPLICABLE",
            "manuscript_hashes": {},
            "evidence_bundle": "supplied evidence packet",
            "artifact_version": "NOT_APPLICABLE",
        },
        "gate_results": [
            {"id": gate_id, "status": "ABSTAIN", "evidence": ["self-test placeholder"], "impact": "structural self-test only"}
            for gate_id in sorted(L1_GATES)
        ] + [{"id": "TSE-G1", "status": "ABSTAIN", "evidence": ["self-test placeholder"], "impact": "venue gate accepted"}],
        "framing": {"a": "Current framing", "b": "NO_CREDIBLE_ALTERNATIVE", "selection": "ABSTAIN"},
        "potential_tier": "PU_ABSTAIN",
        "tier_basis": "evidence",
        "experiment_decision": "ABSTAIN_MISSING_INPUTS",
        "major_findings": ["The self-test checks structure only."],
        "author_questions": [],
        "next_stop_rule": "Stop until the manuscript and evidence packet are supplied.",
        "official_requirements": {"status": "NOT_REQUESTED", "verified_at": None, "sources": []},
    }


def run_self_test() -> int:
    valid_l1 = make_self_test_record()
    errors_l1 = validate(valid_l1)

    bad_gate = json.loads(json.dumps(valid_l1))
    bad_gate["gate_results"].append({"id": "random-gate", "status": "PASS", "evidence": ["x"], "impact": "y"})
    bad_gate["acceptance_probability"] = 0.8
    errors_bad_gate = validate(bad_gate)

    valid_l3 = json.loads(json.dumps(valid_l1))
    valid_l3["review_level"] = "L3"
    valid_l3["gate_results"] = [
        {"id": gate_id, "status": "ABSTAIN", "evidence": ["self-test placeholder"], "impact": "structural self-test only"}
        for gate_id in sorted(L3_GATES)
    ]
    valid_l3["official_requirements"] = {
        "status": "ABSTAIN_NOT_VERIFIED",
        "verified_at": "2026-10-10",
        "sources": ["https://example.org/journals/tse/guide-for-authors"],
    }
    valid_l3["recommendation"] = "ABSTAIN_INCOMPLETE_MANUSCRIPT"
    errors_l3 = validate(valid_l3)

    bad_l3 = json.loads(json.dumps(valid_l3))
    bad_l3["official_requirements"]["sources"] = ["https://example.com/not-official"]
    bad_l3.pop("recommendation")
    errors_bad_l3 = validate(bad_l3)

    bad_l2 = json.loads(json.dumps(valid_l1))
    bad_l2["review_level"] = "L2"
    errors_bad_l2 = validate(bad_l2)

    checks = {
        "valid_l1": not errors_l1,
        "valid_l3": not errors_l3,
        "rejects_random_gate_and_probability": any("neither a core gate" in e for e in errors_bad_gate)
        and any("forbidden acceptance-prediction key" in e for e in errors_bad_gate),
        "rejects_non_official_source_and_missing_recommendation": any("not under a declared official prefix" in e for e in errors_bad_l3)
        and any("L3 recommendation" in e for e in errors_bad_l3),
        "rejects_l2_without_l2_gates": any("missing required gates for L2" in e for e in errors_bad_l2),
    }
    passed = all(checks.values())
    print(json.dumps({"self_test": "PASS" if passed else "FAIL", "checks": checks, "valid_l1_errors": errors_l1, "valid_l3_errors": errors_l3}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("record", nargs="?", type=Path, help="REVIEW-RECORD.json")
    parser.add_argument("--self-test", action="store_true", help="run embedded positive and negative tests")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.record is None:
        parser.error("record is required unless --self-test is used")
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1
    errors = validate(record)
    print(json.dumps({"valid": not errors, "record": str(args.record), "errors": errors,
                      "note": "Structural validation does not establish scientific validity or likely acceptance."}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
