#!/usr/bin/env python3
"""Validate the shape and stage consistency of a paper workflow state file."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


STAGES = [
    "S0_AUTHORITY_RESOLVED",
    "S1_EVIDENCE_LOCKED",
    "S2_ARGUMENT_LOCKED",
    "S3_SECTION_DRAFTED",
    "S4_MANUSCRIPT_INTEGRITY_CHECKED",
    "S5_VENUE_REVIEWED",
    "S6_ARTIFACT_VERIFIED",
    "S7_SUBMISSION_READY",
]

GATES = [
    "authority_resolved",
    "evidence_locked",
    "argument_locked",
    "draft_present",
    "integrity_checked",
    "venue_reviewed",
    "artifact_verified",
    "submission_blockers_resolved",
]

REQUIRED_ARTIFACTS_BY_STAGE = {
    1: ("evidence_ledger", "claim_ledger"),
    2: ("paper_plan",),
    3: ("manuscript",),
    4: ("integrity_report",),
    5: ("venue_review",),
    6: ("final_pdf", "artifact_validation"),
    7: ("submission_readiness",),
}
OPTIONAL_ARTIFACTS = ("question_finding_ledger",)

ALLOWED_VENUE_FAMILIES = {"se", "security", "other", "undecided"}
ALLOWED_AUTHORITY_KINDS = {"file", "repository"}
ALLOWED_WORKTREE_STATUS = {"clean", "dirty", "unknown"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value: Any, name: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{name} must be a list")
        return
    for index, item in enumerate(value):
        if not _nonempty_string(item):
            errors.append(f"{name}[{index}] must be a non-empty string")


def _valid_iso_date(value: Any) -> bool:
    if not _nonempty_string(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_state(data: Any) -> list[str]:
    """Return validation errors; an empty list means the state is consistent."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level JSON must be an object"]

    if data.get("schema_version") != "1":
        errors.append("schema_version must be the string '1'")
    if not _nonempty_string(data.get("paper_id")):
        errors.append("paper_id must be a non-empty string")

    venue = data.get("target_venue")
    if not isinstance(venue, dict):
        errors.append("target_venue must be an object")
    else:
        if not _nonempty_string(venue.get("name")):
            errors.append("target_venue.name must be a non-empty string")
        if venue.get("family") not in ALLOWED_VENUE_FAMILIES:
            allowed = ", ".join(sorted(ALLOWED_VENUE_FAMILIES))
            errors.append(f"target_venue.family must be one of: {allowed}")
        checked_on = venue.get("requirements_checked_on")
        if checked_on is not None and not _valid_iso_date(checked_on):
            errors.append("target_venue.requirements_checked_on must be null or an ISO date YYYY-MM-DD")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    else:
        if authority.get("kind") not in ALLOWED_AUTHORITY_KINDS:
            allowed = ", ".join(sorted(ALLOWED_AUTHORITY_KINDS))
            errors.append(f"authority.kind must be one of: {allowed}")
        if not _nonempty_string(authority.get("workspace")):
            errors.append("authority.workspace must be a non-empty string")
        if not _nonempty_string(authority.get("manuscript")):
            errors.append("authority.manuscript must be a non-empty string")
        if authority.get("status") not in ALLOWED_WORKTREE_STATUS:
            allowed = ", ".join(sorted(ALLOWED_WORKTREE_STATUS))
            errors.append(f"authority.status must be one of: {allowed}")
        for field in ("branch", "head"):
            if field not in authority:
                errors.append(f"authority.{field} must be present as null or a non-empty string")
            elif authority[field] is not None and not _nonempty_string(authority[field]):
                errors.append(f"authority.{field} must be null or a non-empty string")
        if authority.get("branch") is not None and not _nonempty_string(authority.get("head")):
            errors.append("authority.head must identify the current revision when authority.branch is set")
        if authority.get("kind") == "repository":
            if not _nonempty_string(authority.get("branch")):
                errors.append("repository authority requires a non-empty authority.branch")
            if not _nonempty_string(authority.get("head")):
                errors.append("repository authority requires a non-empty authority.head")
        if authority.get("kind") == "file":
            if authority.get("branch") is not None or authority.get("head") is not None:
                errors.append("file authority requires authority.branch and authority.head to be null")

    stage = data.get("stage")
    if stage not in STAGES:
        errors.append(f"stage must be one of: {', '.join(STAGES)}")
        stage_index = None
    else:
        stage_index = STAGES.index(stage)

    gates = data.get("gates")
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
    else:
        for gate in GATES:
            if not isinstance(gates.get(gate), bool):
                errors.append(f"gates.{gate} must be boolean")

        if all(isinstance(gates.get(gate), bool) for gate in GATES):
            seen_false = False
            for gate in GATES:
                value = gates[gate]
                if seen_false and value:
                    errors.append("gates must be monotonic: a later gate is true after an earlier false gate")
                    break
                if not value:
                    seen_false = True

            if stage_index is not None:
                for gate in GATES[: stage_index + 1]:
                    if not gates[gate]:
                        errors.append(f"stage {stage} requires gates.{gate} to be true")
                for gate in GATES[stage_index + 1 :]:
                    if gates[gate]:
                        errors.append(
                            f"stage {stage} cannot retain later completed gate gates.{gate}; "
                            "advance the stage or correct the gate"
                        )

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    elif stage_index is not None:
        for name in OPTIONAL_ARTIFACTS:
            if (
                name in artifacts
                and artifacts[name] is not None
                and not _nonempty_string(artifacts[name])
            ):
                errors.append(f"artifacts.{name} must be null or a non-empty string")
        for required_stage, names in REQUIRED_ARTIFACTS_BY_STAGE.items():
            if stage_index < required_stage:
                continue
            for name in names:
                if not _nonempty_string(artifacts.get(name)):
                    errors.append(f"stage {stage} requires artifacts.{name}")

    _validate_string_list(data.get("claim_ceiling"), "claim_ceiling", errors)
    _validate_string_list(data.get("open_blockers"), "open_blockers", errors)

    if stage == "S7_SUBMISSION_READY" and data.get("open_blockers") != []:
        errors.append("S7_SUBMISSION_READY requires open_blockers to be empty")
    if stage == "S7_SUBMISSION_READY" and isinstance(venue, dict):
        if venue.get("family") == "undecided":
            errors.append("S7_SUBMISSION_READY requires a decided target venue")
        if not _valid_iso_date(venue.get("requirements_checked_on")):
            errors.append("S7_SUBMISSION_READY requires a current official requirements_checked_on date")

    return errors


def main(argv: list[str]) -> int:
    usage = "Usage: validate_paper_state.py <state.json>"
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print(usage)
        return 0
    if len(argv) != 2:
        print(usage, file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        return 2

    errors = validate_state(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
