#!/usr/bin/env python3
"""Validate shape and fail-closed states for a question-finding ledger."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ORIGINS = {
    "AUTHOR_DEFINED",
    "LITERATURE_DERIVED",
    "FINDING_DERIVED",
    "REVIEWER_CHALLENGE",
}
LITERATURE_POSITIONS = {
    "CONFIRM",
    "CONTRADICT",
    "REFINE",
    "EXTEND",
    "REFRAME",
    "UNRESOLVED",
}
LITERATURE_TIMINGS = {
    "PRE_PROTOCOL",
    "POST_FINDING_CONTEXT",
    "BOTH",
    "NOT_CHECKED",
}
ANSWERABILITY = {
    "ANSWERABLE_FROM_FROZEN_EVIDENCE",
    "PROPOSE_TARGETED_ANALYSIS",
    "PROPOSE_NEW_EXPERIMENT",
    "OUT_OF_SCOPE_FUTURE_STUDY",
    "FATAL_CLAIM_GAP",
    "UNRESOLVED_ABSTAIN",
}
AUTHORIZATION = {
    "NOT_REQUIRED_EXISTING_EVIDENCE",
    "NOT_REQUESTED",
    "PROPOSED",
    "AUTHORIZED",
    "REJECTED",
    "NOT_APPLICABLE",
}
PROTOCOL = {
    "FROZEN",
    "PROPOSED_NOT_FROZEN",
    "NOT_APPLICABLE",
    "UNRESOLVED",
}
EXECUTION = {
    "NOT_APPLICABLE",
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    "FAILED",
    "INVALIDATED",
}
ANOMALY = {
    "NOT_ANOMALOUS",
    "SUSPECTED_TECHNICAL_DEFECT",
    "NONREPRODUCIBLE_OR_UNRESOLVED",
    "REPRODUCIBLE_ANOMALY",
}
CLAIM_IMPACTS = {
    "NO_CHANGE",
    "SUPPORT_IF_VALIDATED",
    "WEAKEN",
    "REMOVE",
    "REOPEN_S1",
    "REOPEN_S2",
    "UNRESOLVED",
}
MANUSCRIPT_DISPOSITIONS = {
    "RESULTS",
    "DISCUSSION",
    "LIMITATION",
    "FUTURE_STUDY",
    "DO_NOT_CLAIM",
    "REDESIGN_REQUIRED",
    "PENDING",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nullable_string(value: Any) -> bool:
    return value is None or _nonempty_string(value)


def _string_list(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{field} must be a list")
        return
    for index, item in enumerate(value):
        if not _nonempty_string(item):
            errors.append(f"{field}[{index}] must be a non-empty string")


def _enum(value: Any, allowed: set[str], field: str, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{field} must be one of: {', '.join(sorted(allowed))}")


def validate_ledger(data: Any) -> list[str]:
    """Return validation errors; an empty list means a consistent ledger."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level JSON must be an object"]
    if data.get("schema_version") != "1":
        errors.append("schema_version must be the string '1'")
    if not _nonempty_string(data.get("paper_id")):
        errors.append("paper_id must be a non-empty string")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append("questions must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for index, item in enumerate(questions):
        prefix = f"questions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        question_id = item.get("question_id")
        if not _nonempty_string(question_id):
            errors.append(f"{prefix}.question_id must be a non-empty string")
        elif question_id in seen_ids:
            errors.append(f"{prefix}.question_id must be unique: {question_id}")
        else:
            seen_ids.add(question_id)

        if not _nonempty_string(item.get("question")):
            errors.append(f"{prefix}.question must be a non-empty string")
        _enum(item.get("origin"), ORIGINS, f"{prefix}.origin", errors)
        _string_list(item.get("evidence_ids"), f"{prefix}.evidence_ids", errors)
        _string_list(
            item.get("competing_explanations"),
            f"{prefix}.competing_explanations",
            errors,
        )
        for field in (
            "data_statement",
            "finding",
            "bounded_implication",
            "lineage_note",
            "stop_condition",
        ):
            if field not in item:
                errors.append(f"{prefix}.{field} must be present as null or a non-empty string")
                continue
            if not _nullable_string(item.get(field)):
                errors.append(f"{prefix}.{field} must be null or a non-empty string")

        _enum(
            item.get("literature_position"),
            LITERATURE_POSITIONS,
            f"{prefix}.literature_position",
            errors,
        )
        _enum(
            item.get("literature_timing"),
            LITERATURE_TIMINGS,
            f"{prefix}.literature_timing",
            errors,
        )
        _enum(
            item.get("answerability_disposition"),
            ANSWERABILITY,
            f"{prefix}.answerability_disposition",
            errors,
        )
        _enum(
            item.get("authorization_status"),
            AUTHORIZATION,
            f"{prefix}.authorization_status",
            errors,
        )
        _enum(
            item.get("protocol_status"),
            PROTOCOL,
            f"{prefix}.protocol_status",
            errors,
        )
        _enum(
            item.get("execution_status"),
            EXECUTION,
            f"{prefix}.execution_status",
            errors,
        )
        _enum(
            item.get("anomaly_status"),
            ANOMALY,
            f"{prefix}.anomaly_status",
            errors,
        )
        _enum(
            item.get("claim_impact"),
            CLAIM_IMPACTS,
            f"{prefix}.claim_impact",
            errors,
        )
        _enum(
            item.get("manuscript_disposition"),
            MANUSCRIPT_DISPOSITIONS,
            f"{prefix}.manuscript_disposition",
            errors,
        )

        timing = item.get("literature_timing")
        position = item.get("literature_position")
        if position in LITERATURE_POSITIONS - {"UNRESOLVED"} and timing == "NOT_CHECKED":
            errors.append(
                f"{prefix} cannot record literature_position {position} when literature_timing is NOT_CHECKED"
            )

        disposition = item.get("answerability_disposition")
        authorization = item.get("authorization_status")
        protocol = item.get("protocol_status")
        execution = item.get("execution_status")
        anomaly = item.get("anomaly_status")
        manuscript = item.get("manuscript_disposition")
        claim_impact = item.get("claim_impact")

        if anomaly in ANOMALY - {"NOT_ANOMALOUS"} and not _nonempty_string(item.get("lineage_note")):
            errors.append(f"{prefix} anomalous result requires a non-empty lineage_note")

        if execution in {"IN_PROGRESS", "COMPLETED"} and authorization not in {
            "AUTHORIZED",
            "NOT_REQUIRED_EXISTING_EVIDENCE",
        }:
            errors.append(f"{prefix} work cannot be in progress or completed without authorization")

        if disposition == "ANSWERABLE_FROM_FROZEN_EVIDENCE":
            if protocol != "FROZEN":
                errors.append(f"{prefix} frozen-evidence answer requires protocol_status FROZEN")
            if not item.get("evidence_ids"):
                errors.append(f"{prefix} frozen-evidence answer requires at least one evidence_id")
            if execution not in {"NOT_APPLICABLE", "COMPLETED"}:
                errors.append(f"{prefix} frozen-evidence answer cannot depend on unfinished work")

        if disposition in {"PROPOSE_TARGETED_ANALYSIS", "PROPOSE_NEW_EXPERIMENT"}:
            if authorization in {"NOT_REQUIRED_EXISTING_EVIDENCE", "NOT_APPLICABLE"}:
                errors.append(f"{prefix} proposal cannot bypass explicit authorization")
            if not _nonempty_string(item.get("stop_condition")):
                errors.append(f"{prefix} proposal requires a non-empty stop_condition")
            if authorization == "AUTHORIZED" and protocol != "FROZEN":
                errors.append(f"{prefix} authorized work requires protocol_status FROZEN")

        if manuscript == "RESULTS":
            if not item.get("evidence_ids"):
                errors.append(f"{prefix} RESULTS disposition requires at least one evidence_id")
            if not _nonempty_string(item.get("finding")):
                errors.append(f"{prefix} RESULTS disposition requires a non-empty finding")
            if disposition in {"PROPOSE_TARGETED_ANALYSIS", "PROPOSE_NEW_EXPERIMENT"}:
                if authorization != "AUTHORIZED" or protocol != "FROZEN" or execution != "COMPLETED":
                    errors.append(
                        f"{prefix} proposed work cannot enter RESULTS before authorization, protocol freeze, and completion"
                    )

        if disposition == "UNRESOLVED_ABSTAIN" and manuscript == "RESULTS":
            errors.append(f"{prefix} unresolved abstention cannot be routed to RESULTS")
        if disposition == "FATAL_CLAIM_GAP" and claim_impact in {"NO_CHANGE", "SUPPORT_IF_VALIDATED"}:
            errors.append(f"{prefix} fatal claim gap must weaken, remove, reopen, or remain unresolved")
        if disposition == "FATAL_CLAIM_GAP" and manuscript not in {
            "DO_NOT_CLAIM",
            "REDESIGN_REQUIRED",
            "PENDING",
        }:
            errors.append(f"{prefix} fatal claim gap cannot be routed as an ordinary manuscript section")
        if disposition == "OUT_OF_SCOPE_FUTURE_STUDY" and manuscript not in {
            "LIMITATION",
            "FUTURE_STUDY",
            "PENDING",
        }:
            errors.append(f"{prefix} out-of-scope question must remain a limitation, future study, or pending")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_question_finding_ledger.py <ledger.json>", file=sys.stderr)
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
    errors = validate_ledger(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
