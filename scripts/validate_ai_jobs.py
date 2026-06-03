#!/usr/bin/env python3
"""Validate generated public AI jobs data before GitHub Pages deployment.

The checks are intentionally standard-library only so they can run in GitHub
Actions immediately after scripts/update_ai_jobs.py.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "_data" / "ai_jobs.json"
HISTORY_PATH = ROOT / "_data" / "ai_jobs_history.json"
MAX_JOBS = 10
REQUIRED_JOB_FIELDS = {
    "title",
    "company",
    "location",
    "url",
    "source",
    "score",
    "priority",
    "why_match",
    "possible_gap",
    "compensation_fit",
    "salary_estimate",
    "salary_confidence",
    "apply_angle",
    "skillsets_to_build",
    "learning_gaps",
    "certifications_to_consider",
    "next_action",
    "status_badge",
    "status",
}
ALLOWED_STATUS_BADGES = {"New this week", "Still open", "Repeated high match", "Watchlist"}
ALLOWED_SALARY_CONFIDENCE_PREFIXES = ("Listed —", "Estimated —")
REQUIRED_EXPANDED_SOURCES = {
    "Greenhouse/Chainguard",
    "Greenhouse/Databricks",
    "Greenhouse/Zscaler",
    "Lever/Palantir",
    "Ashby/HackerOne",
    "Ashby/LangChain",
    "Ashby/Linear",
}
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
MAILTO_RE = re.compile(r"mailto:", re.I)
URL_RE = re.compile(r"https?://\S+", re.I)
# Singapore mobile numbers start with 8/9 and are 8 digits; tolerate separators.
SG_MOBILE_RE = re.compile(r"(?<!\d)(?:\+65\s*)?[89](?:[\s.-]*\d){7}(?!\d)")


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"missing required file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def public_text_without_urls(data: object) -> str:
    text = json.dumps(data, ensure_ascii=False, sort_keys=True)
    text = URL_RE.sub("[URL]", text)
    return text


def fail(message: str) -> None:
    print(f"validate_ai_jobs: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_nonempty_string(row: dict[str, object], field: str, label: str) -> None:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} missing non-empty {field!r}")


def require_nonempty_list(row: dict[str, object], field: str, label: str) -> None:
    value = row.get(field)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{label} missing non-empty string list {field!r}")


def validate_privacy(name: str, data: object) -> None:
    text = public_text_without_urls(data)
    if EMAIL_RE.search(text):
        fail(f"{name} contains an email-looking string")
    if MAILTO_RE.search(text):
        fail(f"{name} contains a mailto link")
    match = SG_MOBILE_RE.search(text)
    if match:
        fail(f"{name} contains a Singapore-mobile-looking number near {match.group(0)!r}")


def main() -> int:
    loaded_data = load_json(DATA_PATH)
    loaded_history = load_json(HISTORY_PATH)
    if not isinstance(loaded_data, dict):
        fail("ai_jobs.json root must be an object")
    if not isinstance(loaded_history, dict):
        fail("ai_jobs_history.json root must be an object")
    data = cast(dict[str, Any], loaded_data)
    history = cast(dict[str, Any], loaded_history)

    raw_jobs = data.get("jobs")
    if not isinstance(raw_jobs, list):
        fail("ai_jobs.json jobs must be a list")
    jobs = cast(list[Any], raw_jobs)
    if not (1 <= len(jobs) <= MAX_JOBS):
        fail(f"expected 1-{MAX_JOBS} published jobs after strict fit/salary filtering, found {len(jobs)}")

    raw_alerts = data.get("alerts")
    if raw_alerts is not None and not isinstance(raw_alerts, list):
        fail("alerts must be a list when present")
    alerts = cast(list[Any], raw_alerts or [])

    raw_stats = data.get("stats")
    if not isinstance(raw_stats, dict):
        fail("stats must be present")
    stats = cast(dict[str, Any], raw_stats)
    if stats.get("published_count") != len(jobs):
        fail("stats.published_count does not match jobs length")
    if int(stats.get("candidates_scored") or 0) < len(jobs):
        fail("stats.candidates_scored is lower than published job count")

    source_health = data.get("source_health")
    if not isinstance(source_health, list) or not source_health:
        fail("source_health must be a non-empty list")
    health_rows = cast(list[Any], source_health)
    health_sources = {str(row.get("source")) for row in health_rows if isinstance(row, dict)}
    missing_expanded_sources = REQUIRED_EXPANDED_SOURCES.difference(health_sources)
    if missing_expanded_sources:
        fail(f"expanded source coverage missing from source_health: {', '.join(sorted(missing_expanded_sources))}")

    seen_companies: dict[str, int] = {}
    for idx, raw_row in enumerate(jobs, start=1):
        if not isinstance(raw_row, dict):
            fail(f"job #{idx} is not an object")
        row = cast(dict[str, Any], raw_row)
        missing = REQUIRED_JOB_FIELDS.difference(row)
        if missing:
            fail(f"job #{idx} missing required fields: {', '.join(sorted(missing))}")
        label = f"job #{idx} ({row.get('company', 'unknown')} / {row.get('title', 'unknown')})"
        for field in ["title", "company", "location", "url", "source", "salary_estimate", "salary_confidence", "why_match", "possible_gap", "apply_angle", "next_action", "status_badge"]:
            require_nonempty_string(row, field, label)
        for field in ["skillsets_to_build", "learning_gaps", "certifications_to_consider"]:
            require_nonempty_list(row, field, label)
        score = row.get("score")
        if not isinstance(score, int) or not (0 <= score <= 100):
            fail(f"{label} has invalid score {score!r}")
        compensation_fit = row.get("compensation_fit")
        if not isinstance(compensation_fit, int) or compensation_fit < 1:
            fail(f"{label} has invalid compensation_fit {compensation_fit!r}")
        if row.get("status_badge") not in ALLOWED_STATUS_BADGES:
            fail(f"{label} has unexpected status_badge {row.get('status_badge')!r}")
        salary_confidence = str(row.get("salary_confidence") or "")
        if not salary_confidence.startswith(ALLOWED_SALARY_CONFIDENCE_PREFIXES):
            fail(f"{label} has unexpected salary_confidence {salary_confidence!r}")
        company_key = str(row.get("company", "")).casefold()
        seen_companies[company_key] = seen_companies.get(company_key, 0) + 1

    overrepresented = {company: count for company, count in seen_companies.items() if count > 2}
    if overrepresented:
        fail(f"company cap exceeded: {overrepresented}")

    raw_history_jobs = history.get("jobs")
    if not isinstance(raw_history_jobs, dict):
        fail("ai_jobs_history.json jobs must be an object")
    history_jobs = cast(dict[str, Any], raw_history_jobs)
    for key, raw_row in history_jobs.items():
        if not re.fullmatch(r"[a-z2-7]{12,24}", str(key)):
            fail(f"history key is not base32-style/privacy-safe: {key!r}")
        if not isinstance(raw_row, dict):
            fail(f"history row {key!r} is not an object")
        row = cast(dict[str, Any], raw_row)
        if "url" in row:
            fail(f"history row {key!r} must not store raw job URLs")

    validate_privacy("ai_jobs.json", data)
    validate_privacy("ai_jobs_history.json", history)
    print(f"validate_ai_jobs: ok ({len(jobs)} jobs, {len(alerts or [])} alerts, {stats.get('candidates_scored')} scored candidates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
