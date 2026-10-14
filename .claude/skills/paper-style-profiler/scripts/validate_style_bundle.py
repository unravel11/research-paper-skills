#!/usr/bin/env python3
"""Validate a repository-local paper language-style bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {
    "CORPUS_INVENTORIED",
    "ANCHORS_FROZEN",
    "PROFILE_SAVED",
    "TARGET_AUDITED",
    "STYLE_APPLIED",
    "INSUFFICIENT_REPOSITORY_STYLE_CORPUS",
    "BLOCKED_AUTHORITY_AMBIGUOUS",
}

COMPLETE_STATUSES = {"PROFILE_SAVED", "TARGET_AUDITED", "STYLE_APPLIED"}
ANCHOR_READY_STATUSES = COMPLETE_STATUSES | {"ANCHORS_FROZEN"}
REQUIRED_ROLES = {"empirical-results", "method-mechanism", "discussion-boundaries"}
ALLOWED_ROLES = REQUIRED_ROLES | {
    "introduction-framing",
    "artifact-reproducibility",
    "venue-register",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PRIVATE_PATH_RE = re.compile(r"(?:/Users/|/home/|/Volumes/|[A-Za-z]:\\)")

ARTIFACT_MARKERS = {
    "SELECTION-REPORT.md": "<!-- paper-style-profiler: selection-report-v1 -->",
    "LANGUAGE-STYLE-PROFILE.md": "<!-- paper-style-profiler: language-profile-v1 -->",
    "WRITING-CONTRACT.md": "<!-- paper-style-profiler: writing-contract-v1 -->",
    "TARGET-GAP-AUDIT.md": "<!-- paper-style-profiler: target-gap-audit-v1 -->",
}

EXPECTED_ARTIFACTS = {
    "inventory": "CORPUS-INVENTORY.json",
    "selection": "SELECTION-REPORT.md",
    "profile": "LANGUAGE-STYLE-PROFILE.md",
    "contract": "WRITING-CONTRACT.md",
    "metrics": "metrics.json",
    "target_audit": "TARGET-GAP-AUDIT.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing required file: {path.name}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path.name} must contain a JSON object")
        return None
    return payload


def is_relative_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return value != "." and not path.is_absolute() and ".." not in path.parts and not PRIVATE_PATH_RE.search(value)


def require_fields(payload: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields - set(payload)):
        errors.append(f"{label} missing field: {field}")


def validate_markdown(path: Path, marker: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing required file: {path.name}")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if first_nonempty != marker:
        errors.append(f"{path.name} must start with marker {marker}")


def validate_artifact_map(state: dict[str, Any], errors: list[str]) -> None:
    artifacts = state.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("STYLE-STATE.json artifacts must be an object")
        return
    status = state.get("status")
    required_keys: set[str] = set()
    if status != "BLOCKED_AUTHORITY_AMBIGUOUS":
        required_keys.add("inventory")
    if status in ANCHOR_READY_STATUSES | {"INSUFFICIENT_REPOSITORY_STYLE_CORPUS"}:
        required_keys.add("selection")
    if status in COMPLETE_STATUSES:
        required_keys.update({"profile", "contract", "metrics"})
    if status in {"TARGET_AUDITED", "STYLE_APPLIED"}:
        required_keys.add("target_audit")
    for key in sorted(required_keys):
        expected = EXPECTED_ARTIFACTS[key]
        if artifacts.get(key) != expected:
            errors.append(f"STYLE-STATE.json artifacts.{key} must be {expected!r}")
    for key, value in artifacts.items():
        if not isinstance(key, str) or not is_relative_repo_path(value):
            errors.append(f"STYLE-STATE.json contains an unsafe artifact mapping: {key!r}")


def validate_target_structure(state: dict[str, Any], errors: list[str]) -> None:
    target = state.get("target")
    if not isinstance(target, dict):
        errors.append("STYLE-STATE.json target must be an object")
        return
    paths = target.get("paths")
    hashes = target.get("hashes")
    if not isinstance(paths, list) or not all(is_relative_repo_path(path) for path in paths):
        errors.append("STYLE-STATE.json target.paths must be a list of safe repository-relative file paths")
        return
    if len(paths) != len(set(paths)):
        errors.append("STYLE-STATE.json target.paths contains duplicates")
    if not isinstance(hashes, dict):
        errors.append("STYLE-STATE.json target.hashes must be an object")
        return
    for relative, digest in hashes.items():
        if not is_relative_repo_path(relative) or not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"invalid target hash entry: {relative!r}")
    if set(paths) != set(hashes):
        errors.append("STYLE-STATE.json target.paths and target.hashes must name the same files")


def validate_anchor_structure(state: dict[str, Any], errors: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    anchors = state.get("anchors")
    if not isinstance(anchors, list):
        errors.append("STYLE-STATE.json anchors must be a list")
        return []
    status = state.get("status")
    if status in ANCHOR_READY_STATUSES and not 3 <= len(anchors) <= 5:
        errors.append(f"status {status} requires three to five anchors; found {len(anchors)}")
    if status == "INSUFFICIENT_REPOSITORY_STYLE_CORPUS" and len(anchors) >= 3:
        errors.append("insufficient-corpus status conflicts with three or more anchors")

    required = {"id", "relative_path", "sha256", "title", "primary_role", "selection_score", "selection_basis"}
    ids: set[str] = set()
    paths: set[str] = set()
    hashes: set[str] = set()
    roles: set[str] = set()
    valid: list[dict[str, Any]] = []
    for index, anchor in enumerate(anchors, start=1):
        if not isinstance(anchor, dict):
            errors.append(f"anchor #{index} must be an object")
            continue
        require_fields(anchor, required, f"anchor #{index}", errors)
        identifier = anchor.get("id")
        relative_path = anchor.get("relative_path")
        digest = anchor.get("sha256")
        if not isinstance(identifier, str) or not re.fullmatch(r"A[1-9][0-9]*", identifier):
            errors.append(f"anchor #{index} has invalid id: {identifier!r}")
        elif identifier in ids:
            errors.append(f"duplicate anchor id: {identifier}")
        else:
            ids.add(identifier)
        if not is_relative_repo_path(relative_path):
            errors.append(f"anchor {identifier!r} has non-relative or unsafe path")
        elif relative_path in paths:
            errors.append(f"duplicate anchor path: {relative_path}")
        else:
            paths.add(relative_path)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"anchor {identifier!r} has invalid SHA-256")
        elif digest in hashes:
            errors.append(f"duplicate anchor hash: {digest}")
        else:
            hashes.add(digest)
        score = anchor.get("selection_score")
        if not isinstance(score, (int, float)) or not 0 <= score <= 30:
            errors.append(f"anchor {identifier!r} selection_score must be between 0 and 30")
        if not isinstance(anchor.get("selection_basis"), str) or not anchor.get("selection_basis", "").strip():
            errors.append(f"anchor {identifier!r} needs a non-empty selection_basis")
        if not isinstance(anchor.get("title"), str) or not anchor.get("title", "").strip():
            errors.append(f"anchor {identifier!r} needs a non-empty title")
        primary_role = anchor.get("primary_role")
        if primary_role in ALLOWED_ROLES:
            roles.add(primary_role)
        else:
            errors.append(f"anchor {identifier!r} has invalid primary_role: {primary_role!r}")
        secondary_roles = anchor.get("secondary_roles", [])
        if isinstance(secondary_roles, list):
            invalid_secondary = [role for role in secondary_roles if role not in ALLOWED_ROLES]
            if invalid_secondary:
                errors.append(f"anchor {identifier!r} has invalid secondary_roles: {invalid_secondary}")
            roles.update(role for role in secondary_roles if role in ALLOWED_ROLES)
        else:
            errors.append(f"anchor {identifier!r} secondary_roles must be a list when present")
        valid.append(anchor)

    if status in ANCHOR_READY_STATUSES:
        missing_roles = REQUIRED_ROLES - roles
        if missing_roles:
            errors.append(f"anchor set lacks required complementary roles: {', '.join(sorted(missing_roles))}")
    elif anchors:
        warnings.append("anchors are recorded but the state is not anchor-ready")
    return valid


def validate_inventory(inventory: dict[str, Any], anchors: list[dict[str, Any]], errors: list[str]) -> None:
    if inventory.get("schema") != "paper_style_inventory_v1":
        errors.append("CORPUS-INVENTORY.json has unexpected schema")
    records = inventory.get("records")
    if not isinstance(records, list):
        errors.append("CORPUS-INVENTORY.json records must be a list")
        return
    by_path: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"inventory record #{index} must be an object")
            continue
        path = record.get("path")
        if not is_relative_repo_path(path):
            errors.append(f"inventory record #{index} has an unsafe path")
            continue
        if path in by_path:
            errors.append(f"duplicate inventory path: {path}")
        by_path[path] = record
    for anchor in anchors:
        path = anchor.get("relative_path")
        record = by_path.get(path)
        if record is None:
            errors.append(f"selected anchor missing from inventory: {path}")
            continue
        if record.get("sha256") != anchor.get("sha256"):
            errors.append(f"inventory hash mismatch for selected anchor: {path}")
        if record.get("source_class") != "external_published_full_text":
            errors.append(f"selected anchor is not classified as external_published_full_text: {path}")
        if record.get("eligibility") != "eligible":
            errors.append(f"selected anchor is not marked eligible: {path}")


def validate_metrics(metrics: dict[str, Any], anchors: list[dict[str, Any]], errors: list[str]) -> None:
    if metrics.get("schema") != "paper_style_language_metrics_v1":
        errors.append("metrics.json has unexpected schema")
    papers = metrics.get("papers")
    if not isinstance(papers, dict):
        errors.append("metrics.json papers must be an object")
        return
    expected = {anchor.get("id") for anchor in anchors if isinstance(anchor.get("id"), str)}
    actual = set(papers)
    if expected != actual:
        errors.append(f"metrics paper IDs do not match anchors: expected {sorted(expected)}, found {sorted(actual)}")
    if "interpretation_boundary" not in metrics:
        errors.append("metrics.json missing interpretation_boundary")


def verify_repository_hashes(repo_root: Path, state: dict[str, Any], anchors: list[dict[str, Any]], errors: list[str]) -> None:
    for anchor in anchors:
        relative = anchor.get("relative_path")
        if not is_relative_repo_path(relative):
            continue
        source = repo_root / str(relative)
        if not source.is_file():
            errors.append(f"anchor source missing from repository: {relative}")
            continue
        if sha256_file(source) != anchor.get("sha256"):
            errors.append(f"anchor source is stale: {relative}")

    target = state.get("target", {})
    if not isinstance(target, dict):
        return
    hashes = target.get("hashes", {})
    if not isinstance(hashes, dict):
        return
    for relative, expected_hash in hashes.items():
        if not is_relative_repo_path(relative) or not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
            continue
        source = repo_root / relative
        if not source.is_file():
            errors.append(f"target source missing from repository: {relative}")
        elif sha256_file(source) != expected_hash:
            errors.append(f"target source is stale: {relative}")


def scan_bundle(bundle: Path, errors: list[str], warnings: list[str]) -> None:
    for path in bundle.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(bundle)
        lowered_parts = {part.casefold() for part in relative.parts}
        if path.suffix.casefold() in {".pdf", ".txt", ".text"} or lowered_parts & {"raw", "extracted", "source-text", "source_text"}:
            errors.append(f"bundle contains prohibited raw-source-like artifact: {relative.as_posix()}")
        if path.suffix.casefold() in {".json", ".md", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if PRIVATE_PATH_RE.search(text):
                errors.append(f"bundle contains a private absolute path: {relative.as_posix()}")
            if len(text) > 2_000_000:
                warnings.append(f"unusually large text artifact; inspect for copied source text: {relative.as_posix()}")


def validate_bundle(bundle: Path, repo_root: Path | None) -> tuple[list[str], list[str], str | None]:
    errors: list[str] = []
    warnings: list[str] = []
    state = load_json(bundle / "STYLE-STATE.json", errors)
    if state is None:
        return errors, warnings, None
    require_fields(
        state,
        {"schema", "skill", "status", "generated_at", "repository", "target", "anchors", "artifacts", "refresh_conditions"},
        "STYLE-STATE.json",
        errors,
    )
    if state.get("schema") != "paper_style_state_v1":
        errors.append("STYLE-STATE.json has unexpected schema")
    if state.get("skill") != "paper-style-profiler":
        errors.append("STYLE-STATE.json has unexpected skill")
    status = state.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"STYLE-STATE.json has invalid status: {status!r}")
    repository = state.get("repository")
    if not isinstance(repository, dict) or repository.get("root") != ".":
        errors.append("STYLE-STATE.json repository.root must be '.'")
    validate_artifact_map(state, errors)
    validate_target_structure(state, errors)
    if not isinstance(state.get("refresh_conditions"), list):
        errors.append("STYLE-STATE.json refresh_conditions must be a list")

    anchors = validate_anchor_structure(state, errors, warnings)
    inventory: dict[str, Any] | None = None
    if status != "BLOCKED_AUTHORITY_AMBIGUOUS":
        inventory = load_json(bundle / "CORPUS-INVENTORY.json", errors)
        if inventory is not None:
            validate_inventory(inventory, anchors, errors)

    if status in ANCHOR_READY_STATUSES | {"INSUFFICIENT_REPOSITORY_STYLE_CORPUS"}:
        validate_markdown(bundle / "SELECTION-REPORT.md", ARTIFACT_MARKERS["SELECTION-REPORT.md"], errors)

    if status in COMPLETE_STATUSES:
        validate_markdown(bundle / "LANGUAGE-STYLE-PROFILE.md", ARTIFACT_MARKERS["LANGUAGE-STYLE-PROFILE.md"], errors)
        validate_markdown(bundle / "WRITING-CONTRACT.md", ARTIFACT_MARKERS["WRITING-CONTRACT.md"], errors)
        metrics = load_json(bundle / "metrics.json", errors)
        if metrics is not None:
            validate_metrics(metrics, anchors, errors)

    if status in {"TARGET_AUDITED", "STYLE_APPLIED"}:
        validate_markdown(bundle / "TARGET-GAP-AUDIT.md", ARTIFACT_MARKERS["TARGET-GAP-AUDIT.md"], errors)

    if repo_root is not None:
        verify_repository_hashes(repo_root, state, anchors, errors)
    scan_bundle(bundle, errors, warnings)
    if status not in COMPLETE_STATUSES:
        warnings.append(f"state {status} is not a complete profile and must not be used for writing")
    return errors, warnings, status if isinstance(status, str) else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_dir", help="Repository-local style bundle directory")
    parser.add_argument("--repo-root", help="Authoritative repository root for source hash verification")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = Path(args.bundle_dir).expanduser().resolve()
    if not bundle.is_dir():
        print(json.dumps({"status": "FAIL", "errors": [f"bundle directory not found: {bundle}"], "warnings": []}, indent=2))
        return 2
    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else None
    if repo_root is not None and not repo_root.is_dir():
        print(json.dumps({"status": "FAIL", "errors": [f"repository root not found: {repo_root}"], "warnings": []}, indent=2))
        return 2
    errors, warnings, lifecycle = validate_bundle(bundle, repo_root)
    payload = {
        "status": "FAIL" if errors else "PASS",
        "lifecycle": lifecycle,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
