#!/usr/bin/env python3
"""Validate a strict figure/table review record and its artifact bindings."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


MAX_RECORD_BYTES = 2_000_000
MAX_ARTIFACT_BYTES = 250_000_000
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_ROLES = {"visual_design", "statistical_graphics", "venue_production"}
SCORE_FIELDS = ("figure_score", "table_score", "overall_score")


class ReviewError(ValueError):
    """Raised for a malformed or unsafe review record."""


def _load_record(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise ReviewError("review record must not be a symlink")
    if not path.is_file():
        raise ReviewError(f"review record not found: {path}")
    if path.stat().st_size > MAX_RECORD_BYTES:
        raise ReviewError("review record exceeds 2 MB")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"cannot read review record: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReviewError("review record must be a JSON object")
    return payload


def _safe_artifact(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ReviewError("artifact path must be a non-empty relative string")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ReviewError(f"unsafe artifact path: {relative!r}")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ReviewError(f"artifact escapes artifact root: {relative!r}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ReviewError(f"artifact is missing or a symlink: {relative!r}")
    if resolved.stat().st_size > MAX_ARTIFACT_BYTES:
        raise ReviewError(f"artifact exceeds 250 MB: {relative!r}")
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _score(value: Any, field: str, reviewer_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReviewError(f"{reviewer_id}: {field} must be numeric")
    result = float(value)
    if not math.isfinite(result) or not 0 <= result <= 10:
        raise ReviewError(f"{reviewer_id}: {field} must be between 0 and 10")
    return result


def validate_record(payload: dict[str, Any], artifact_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must equal '1.0'")
    for field in ("round_id", "rubric_version"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            errors.append(f"{field} must be a non-empty string")

    threshold_value = payload.get("threshold")
    if isinstance(threshold_value, bool) or not isinstance(threshold_value, (int, float)):
        errors.append("threshold must be numeric")
        threshold = 10.1
    else:
        threshold = float(threshold_value)
        if not math.isfinite(threshold) or not 9 <= threshold <= 10:
            errors.append("threshold must be between 9 and 10")

    artifacts = payload.get("artifacts")
    artifact_ids: set[str] = set()
    verified_artifacts: list[dict[str, Any]] = []
    if not isinstance(artifacts, list) or len(artifacts) < 2:
        errors.append("artifacts must contain at least figure and table entries")
    else:
        for index, item in enumerate(artifacts, start=1):
            if not isinstance(item, dict):
                errors.append(f"artifact #{index} must be an object")
                continue
            artifact_id = item.get("id")
            relative = item.get("path")
            expected_hash = item.get("sha256")
            if not isinstance(artifact_id, str) or not artifact_id.strip():
                errors.append(f"artifact #{index}: id must be non-empty")
                continue
            if artifact_id in artifact_ids:
                errors.append(f"duplicate artifact id: {artifact_id}")
                continue
            artifact_ids.add(artifact_id)
            if not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
                errors.append(f"{artifact_id}: sha256 must be 64 lowercase hex characters")
                continue
            try:
                actual_path = _safe_artifact(artifact_root, relative)
                actual_hash = _sha256(actual_path)
            except ReviewError as exc:
                errors.append(str(exc))
                continue
            if actual_hash != expected_hash:
                errors.append(f"{artifact_id}: artifact hash mismatch")
            verified_artifacts.append(
                {"id": artifact_id, "path": relative, "sha256": actual_hash}
            )
        for required in ("figure", "table"):
            if required not in artifact_ids:
                errors.append(f"missing required artifact id: {required}")

    reviewers = payload.get("reviewers")
    reviewer_ids: set[str] = set()
    roles: set[str] = set()
    review_results: list[dict[str, Any]] = []
    all_clear = True
    if not isinstance(reviewers, list) or not 3 <= len(reviewers) <= 4:
        errors.append("reviewers must contain 3 or 4 entries")
        all_clear = False
    else:
        for index, reviewer in enumerate(reviewers, start=1):
            if not isinstance(reviewer, dict):
                errors.append(f"reviewer #{index} must be an object")
                all_clear = False
                continue
            reviewer_id = reviewer.get("reviewer_id")
            role = reviewer.get("role")
            if not isinstance(reviewer_id, str) or not reviewer_id.strip():
                errors.append(f"reviewer #{index}: reviewer_id must be non-empty")
                all_clear = False
                continue
            if reviewer_id in reviewer_ids:
                errors.append(f"duplicate reviewer_id: {reviewer_id}")
            reviewer_ids.add(reviewer_id)
            if not isinstance(role, str) or not role.strip():
                errors.append(f"{reviewer_id}: role must be non-empty")
            else:
                roles.add(role)
            if reviewer.get("independent") is not True:
                errors.append(f"{reviewer_id}: independent must be true")
                all_clear = False
            summary = reviewer.get("summary")
            if not isinstance(summary, str) or not summary.strip():
                errors.append(f"{reviewer_id}: summary must be non-empty")
            scores: dict[str, float] = {}
            for field in SCORE_FIELDS:
                try:
                    scores[field] = _score(reviewer.get(field), field, reviewer_id)
                except ReviewError as exc:
                    errors.append(str(exc))
                    all_clear = False
                    continue
                if scores[field] < threshold:
                    errors.append(
                        f"{reviewer_id}: {field} {scores[field]:g} is below threshold {threshold:g}"
                    )
                    all_clear = False
            hard_failures = reviewer.get("hard_gate_failures")
            required_changes = reviewer.get("required_changes")
            if not isinstance(hard_failures, list):
                errors.append(f"{reviewer_id}: hard_gate_failures must be a list")
                all_clear = False
                hard_failures = []
            if not isinstance(required_changes, list):
                errors.append(f"{reviewer_id}: required_changes must be a list")
                all_clear = False
                required_changes = []
            if hard_failures or required_changes:
                all_clear = False
            review_results.append(
                {
                    "reviewer_id": reviewer_id,
                    "role": role,
                    **scores,
                    "hard_gate_failure_count": len(hard_failures),
                    "required_change_count": len(required_changes),
                }
            )

    missing_roles = REQUIRED_ROLES - roles
    if missing_roles:
        errors.append("missing required reviewer roles: " + ", ".join(sorted(missing_roles)))
        all_clear = False

    computed_status = "PASS" if not errors and all_clear else "FAIL"
    declared_status = payload.get("status")
    if declared_status not in {"PASS", "FAIL"}:
        errors.append("status must be 'PASS' or 'FAIL'")
    elif declared_status != computed_status:
        errors.append(
            f"declared status {declared_status!r} does not match computed status {computed_status!r}"
        )
        computed_status = "FAIL"

    return {
        "schema_version": "1.0",
        "round_id": payload.get("round_id"),
        "threshold": threshold_value,
        "computed_status": computed_status,
        "verified_artifacts": verified_artifacts,
        "reviewers": review_results,
        "errors": errors,
        "notice": (
            "This validator checks record structure, score thresholds, and artifact hashes. "
            "It does not prove reviewer independence, scientific validity, venue compliance, "
            "submission readiness, or acceptance."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", help="JSON review record")
    parser.add_argument(
        "--artifact-root",
        required=True,
        help="root used to resolve artifact paths from the record",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable report")
    args = parser.parse_args()

    try:
        payload = _load_record(Path(args.record))
        report = validate_record(payload, Path(args.artifact_root))
    except ReviewError as exc:
        report = {"computed_status": "FAIL", "errors": [str(exc)]}

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"visual review: {report['computed_status']}")
        for error in report.get("errors", []):
            print(f"- {error}")
    return 0 if report.get("computed_status") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
