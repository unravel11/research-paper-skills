#!/usr/bin/env python3
"""Produce quote-free descriptive language metrics from temporary plain text."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"'“])")
REFERENCE_HEADING_RE = re.compile(r"(?im)^\s*(?:references|bibliography)\s*$")

TERM_FAMILIES = {
    "first_person": ["we", "our", "ours", "us"],
    "modality": ["may", "might", "can", "could", "should", "would", "must"],
    "hedging": ["may", "might", "could", "likely", "possibly", "potentially", "suggest", "suggests", "indicate", "indicates"],
    "research_action": ["design", "designed", "collect", "collected", "implement", "implemented", "evaluate", "evaluated", "analyze", "analyzed", "compare", "compared", "construct", "constructed"],
    "evidence": ["observe", "observed", "find", "found", "measure", "measured", "show", "shows", "shown", "report", "reported", "reveal", "reveals"],
    "interpretation": ["suggest", "suggests", "indicate", "indicates", "imply", "implies", "explain", "explains", "demonstrate", "demonstrates"],
    "comparison": ["outperform", "outperforms", "differ", "differs", "remain", "remains", "increase", "increases", "decrease", "decreases", "higher", "lower"],
    "boundary": ["limit", "limits", "limited", "restrict", "restricted", "focus", "focuses", "condition", "conditioned", "exclude", "excluded", "only", "scope", "cannot"],
    "negative_result": ["no evidence", "did not", "does not", "cannot", "failed to", "no significant", "not statistically"],
}

OPENING_FAMILIES = {
    "first_person": ["we ", "our "],
    "contrast_or_concession": ["however", "although", "while ", "despite", "nevertheless", "in contrast"],
    "cause_or_consequence": ["therefore", "thus", "consequently", "as a result", "because"],
    "addition_or_enumeration": ["furthermore", "moreover", "additionally", "first", "second", "finally"],
    "evidence_or_example": ["for example", "for instance", "specifically", "in particular"],
    "interpretation": ["these results", "this result", "this finding", "our results"],
    "limitation_or_scope": ["in this study", "within ", "under ", "to limit", "a limitation", "one limitation"],
    "demonstrative": ["this ", "these ", "that ", "those "],
    "numeric": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

TRANSITION_FAMILIES = {
    "contrast_or_concession": ["however", "although", "whereas", "despite", "nevertheless", "in contrast", "on the other hand"],
    "cause_or_consequence": ["therefore", "thus", "consequently", "as a result", "because", "hence"],
    "addition_or_enumeration": ["furthermore", "moreover", "additionally", "first", "second", "finally", "in addition"],
    "evidence_or_example": ["for example", "for instance", "specifically", "in particular"],
    "limitation_or_scope": ["in this study", "within", "under this", "limited to", "out of scope", "a limitation"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def percentile(values: list[int], proportion: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * proportion
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return float(ordered[lower])
    fraction = index - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def rounded(value: float) -> float:
    return round(value, 3)


def strip_references(text: str) -> tuple[str, bool]:
    matches = list(REFERENCE_HEADING_RE.finditer(text))
    if not matches:
        return text, False
    candidate = matches[-1]
    if candidate.start() < len(text) * 0.45:
        return text, False
    return text[: candidate.start()], True


def paragraphs_from_text(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n\n")
    raw_blocks = re.split(r"\n\s*\n+", text)
    paragraphs: list[str] = []
    for block in raw_blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        lines = [line for line in lines if not re.fullmatch(r"(?:page\s+)?\d+", line, flags=re.I)]
        joined = re.sub(r"\s+", " ", " ".join(lines)).strip()
        words = WORD_RE.findall(joined)
        if len(words) < 5:
            continue
        alpha = sum(character.isalpha() for character in joined)
        if alpha / max(len(joined), 1) < 0.45:
            continue
        if len(words) <= 12 and joined.upper() == joined:
            continue
        paragraphs.append(joined)
    return paragraphs


def sentences_from_paragraph(paragraph: str) -> list[str]:
    candidates = SENTENCE_SPLIT_RE.split(paragraph)
    return [sentence.strip() for sentence in candidates if len(WORD_RE.findall(sentence)) >= 3]


def phrase_count(text: str, phrases: list[str]) -> int:
    total = 0
    for phrase in phrases:
        escaped = re.escape(phrase)
        if " " in phrase:
            pattern = rf"(?<![A-Za-z]){escaped}(?![A-Za-z])"
        else:
            pattern = rf"\b{escaped}\b"
        total += len(re.findall(pattern, text, flags=re.I))
    return total


def rate(count: int, denominator: int) -> float:
    return rounded(count * 1000 / denominator) if denominator else 0.0


def opening_category(sentence: str) -> str:
    lowered = sentence.lstrip("([\"'“‘ ").casefold()
    for category, prefixes in OPENING_FAMILIES.items():
        if any(lowered.startswith(prefix) for prefix in prefixes):
            return category
    return "other"


def passive_candidate_count(text: str) -> int:
    pattern = re.compile(
        r"\b(?:is|are|was|were|be|been|being)\s+(?:[A-Za-z-]+\s+){0,2}[A-Za-z-]+(?:ed|en)\b",
        flags=re.I,
    )
    return len(pattern.findall(text))


def tense_signals(text: str) -> dict[str, object]:
    past_aux = phrase_count(text, ["was", "were", "had", "did"])
    past_ed = len(re.findall(r"\b[A-Za-z]{4,}ed\b", text, flags=re.I))
    present_aux = phrase_count(text, ["is", "are", "has", "have", "do", "does"])
    future = phrase_count(text, ["will", "shall"])
    return {
        "past_candidates": past_aux + past_ed,
        "present_candidates": present_aux,
        "future_candidates": future,
        "note": "Heuristic signals, not parsed grammatical tense.",
    }


def analyze_text(text: str) -> dict[str, object]:
    bounded, references_removed = strip_references(text)
    paragraphs = paragraphs_from_text(bounded)
    sentences = [sentence for paragraph in paragraphs for sentence in sentences_from_paragraph(paragraph)]
    words = WORD_RE.findall(" ".join(paragraphs))
    sentence_lengths = [len(WORD_RE.findall(sentence)) for sentence in sentences]
    paragraph_sentence_counts = [len(sentences_from_paragraph(paragraph)) for paragraph in paragraphs]
    joined = " ".join(paragraphs)

    family_counts = {name: phrase_count(joined, terms) for name, terms in TERM_FAMILIES.items()}
    transition_counts = {name: phrase_count(joined, terms) for name, terms in TRANSITION_FAMILIES.items()}
    openings: dict[str, int] = {name: 0 for name in [*OPENING_FAMILIES, "other"]}
    for sentence in sentences:
        openings[opening_category(sentence)] += 1

    paragraph_endings = {"interpretation": 0, "boundary_or_limitation": 0, "other": 0}
    for paragraph in paragraphs:
        paragraph_sentences = sentences_from_paragraph(paragraph)
        if not paragraph_sentences:
            continue
        ending = paragraph_sentences[-1]
        if phrase_count(ending, TERM_FAMILIES["boundary"] + TRANSITION_FAMILIES["limitation_or_scope"]):
            paragraph_endings["boundary_or_limitation"] += 1
        elif phrase_count(ending, TERM_FAMILIES["interpretation"]):
            paragraph_endings["interpretation"] += 1
        else:
            paragraph_endings["other"] += 1

    punctuation = {
        "semicolon": joined.count(";"),
        "colon": joined.count(":"),
        "parenthetical_pairs": min(joined.count("("), joined.count(")")),
        "em_or_en_dash": joined.count("—") + joined.count("–"),
        "question_mark": joined.count("?"),
    }

    return {
        "coverage": {
            "words": len(words),
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
            "references_removed": references_removed,
        },
        "sentence_words": {
            "mean": rounded(statistics.mean(sentence_lengths)) if sentence_lengths else 0.0,
            "median": rounded(statistics.median(sentence_lengths)) if sentence_lengths else 0.0,
            "p25": rounded(percentile(sentence_lengths, 0.25)),
            "p75": rounded(percentile(sentence_lengths, 0.75)),
            "p90": rounded(percentile(sentence_lengths, 0.90)),
        },
        "paragraph_sentences": {
            "mean": rounded(statistics.mean(paragraph_sentence_counts)) if paragraph_sentence_counts else 0.0,
            "median": rounded(statistics.median(paragraph_sentence_counts)) if paragraph_sentence_counts else 0.0,
        },
        "functional_counts": family_counts,
        "functional_rates_per_1000_words": {name: rate(count, len(words)) for name, count in family_counts.items()},
        "passive_candidates": {
            "count": passive_candidate_count(joined),
            "per_1000_words": rate(passive_candidate_count(joined), len(words)),
            "note": "Surface heuristic; inspect examples manually before making a voice rule.",
        },
        "tense_signals": tense_signals(joined),
        "sentence_opening_categories": openings,
        "transition_counts": transition_counts,
        "paragraph_ending_categories": paragraph_endings,
        "punctuation": punctuation,
    }


def parse_labeled_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError(f"expected ID=PATH, got: {value}")
    identifier, raw_path = value.split("=", 1)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", identifier):
        raise ValueError(f"invalid identifier: {identifier}")
    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"text file not found: {path}")
    return identifier, path


def range_summary(papers: dict[str, dict[str, object]]) -> dict[str, object]:
    selectors = {
        "sentence_words_mean": ("sentence_words", "mean"),
        "sentence_words_median": ("sentence_words", "median"),
        "paragraph_sentences_mean": ("paragraph_sentences", "mean"),
        "first_person_per_1000": ("functional_rates_per_1000_words", "first_person"),
        "modality_per_1000": ("functional_rates_per_1000_words", "modality"),
        "evidence_per_1000": ("functional_rates_per_1000_words", "evidence"),
        "boundary_per_1000": ("functional_rates_per_1000_words", "boundary"),
        "passive_candidates_per_1000": ("passive_candidates", "per_1000_words"),
    }
    result: dict[str, object] = {}
    for label, (outer, inner) in selectors.items():
        values = [float(paper[outer][inner]) for paper in papers.values()]
        result[label] = {
            "min": rounded(min(values)),
            "median": rounded(statistics.median(values)),
            "max": rounded(max(values)),
        }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", action="append", required=True, help="Selected anchor as ID=temporary-text-path")
    parser.add_argument("--target", help="Optional target manuscript as ID=text-path")
    parser.add_argument("--output", required=True, help="Destination metrics JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        labeled_papers = [parse_labeled_path(value) for value in args.paper]
        labeled_target = parse_labeled_path(args.target) if args.target else None
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    identifiers = [identifier for identifier, _ in labeled_papers]
    if len(set(identifiers)) != len(identifiers):
        print("paper identifiers must be unique", file=sys.stderr)
        return 2
    if not 3 <= len(identifiers) <= 5:
        print("an aggregate language profile requires three to five papers", file=sys.stderr)
        return 2
    if labeled_target and labeled_target[0] in set(identifiers):
        print("target identifier must differ from paper identifiers", file=sys.stderr)
        return 2

    papers: dict[str, dict[str, object]] = {}
    for identifier, path in labeled_papers:
        text = path.read_text(encoding="utf-8", errors="replace")
        papers[identifier] = analyze_text(text)

    payload: dict[str, object] = {
        "schema": "paper_style_language_metrics_v1",
        "generated_at": utc_now(),
        "papers": papers,
        "corpus_ranges": range_summary(papers),
        "interpretation_boundary": "Derived metrics are descriptive aids, not writing quotas, quality scores, authorship tests, or acceptance predictors.",
    }
    if labeled_target:
        target_id, target_path = labeled_target
        payload["target"] = {"id": target_id, "metrics": analyze_text(target_path.read_text(encoding="utf-8", errors="replace"))}

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "paper_ids": identifiers, "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
