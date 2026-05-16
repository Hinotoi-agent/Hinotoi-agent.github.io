#!/usr/bin/env python3
"""Refresh Singapore AI / AI-security job leads for the Hinotoi GitHub Pages site.

The script intentionally uses public ATS/job-board JSON endpoints and the Python
standard library only, so the weekly GitHub Actions job does not need secrets or
extra dependencies. Results are strict to Singapore / Remote-Singapore locations
and then ranked for AI, LLM, security, trust/safety, and adjacent engineering
signals.
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_data" / "ai_jobs.json"
USER_AGENT = "HinotoiJobWatcher/1.0 (+https://hinotoi-agent.github.io/ai-jobs/)"

GREENHOUSE_BOARDS = {
    "Anthropic": "anthropic",
    "Cloudflare": "cloudflare",
    "Datadog": "datadog",
    "Elastic": "elastic",
    "Google DeepMind": "deepmind",
    "MongoDB": "mongodb",
    "OKX": "okx",
    "Stripe": "stripe",
    "Wiz": "wizinc",
}

REMOTE_FEEDS = [
    ("Remotive", "https://remotive.com/api/remote-jobs?search={query}"),
    ("RemoteOK", "https://remoteok.com/api"),
]

SEARCH_QUERIES = [
    "AI security Singapore",
    "LLM security Singapore",
    "machine learning security Singapore",
    "AI red team Singapore",
    "AI safety Singapore",
    "security engineer machine learning Singapore",
    "AI engineer Singapore security",
]

AI_TERMS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "llm",
    "large language model",
    "genai",
    "generative ai",
    "agent",
    "deep learning",
    "research engineer",
]

SECURITY_TERMS = [
    "security",
    "cyber",
    "trust and safety",
    "safety",
    "risk",
    "abuse",
    "red team",
    "application security",
    "product security",
    "cloud security",
    "detection",
    "threat",
    "fraud",
]

ENGINEERING_TERMS = [
    "engineer",
    "researcher",
    "scientist",
    "architect",
    "analyst",
    "manager",
    "lead",
    "specialist",
]

EXCLUDED_TITLE_TERMS = [
    "account executive",
    "partner manager",
    "field marketing",
    "marketing manager",
    "finance & strategy",
    "product support",
    "support specialist",
]

TITLE_RELEVANCE_TERMS = [
    *AI_TERMS,
    *SECURITY_TERMS,
    "data scientist",
    "data analyst",
    "data infra",
    "compliance",
    "model risk",
    "quant",
    "agent infrastructure",
]

SINGAPORE_PATTERNS = [
    re.compile(r"\bsingapore\b", re.I),
    re.compile(r"\bsg\b", re.I),
    re.compile(r"remote\s*-?\s*singapore", re.I),
]

TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class Job:
    title: str
    company: str
    location: str
    url: str
    source: str
    published_at: str
    summary: str
    tags: tuple[str, ...]
    score: int


def clean_text(value: object, limit: int | None = None) -> str:
    text = str(value or "")
    for _ in range(3):
        text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = TAG_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text).strip()
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def fetch_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)


def is_singapore_location(location: str) -> bool:
    if not location:
        return False
    return any(pattern.search(location) for pattern in SINGAPORE_PATTERNS)


def term_hits(text: str, terms: Iterable[str]) -> list[str]:
    haystack = text.lower()
    hits: list[str] = []
    for term in terms:
        if len(term) <= 3:
            if re.search(rf"(?<![a-z0-9]){re.escape(term.lower())}(?![a-z0-9])", haystack):
                hits.append(term.upper() if term in {"ai", "ml", "llm"} else term)
        elif term.lower() in haystack:
            hits.append(term)
    return hits


def score_job(title: str, company: str, location: str, summary: str) -> tuple[int, list[str]]:
    text = " ".join([title, company, location, summary])
    title_text = title.lower()
    ai_hits = term_hits(text, AI_TERMS)
    security_hits = term_hits(text, SECURITY_TERMS)
    engineering_hits = term_hits(text, ENGINEERING_TERMS)
    title_hits = term_hits(title, TITLE_RELEVANCE_TERMS)

    if any(term in title_text for term in EXCLUDED_TITLE_TERMS):
        return 0, []

    score = 0
    score += 4 * len(set(ai_hits))
    score += 4 * len(set(security_hits))
    score += 1 * len(set(engineering_hits))
    score += 3 * len(set(title_hits))
    if ai_hits and security_hits:
        score += 8
    if "security" in title_text or "red team" in title_text:
        score += 5
    if any(term in title_text for term in ["ai", "llm", "machine learning", "research engineer", "applied ai", "data scientist"]):
        score += 5
    if not title_hits and not (ai_hits and security_hits):
        score -= 8
    if "singapore" in location.lower():
        score += 3

    tags = []
    for hit in list(dict.fromkeys(title_hits + ai_hits + security_hits + engineering_hits))[:6]:
        tags.append(hit.title() if hit.islower() else hit)
    return score, tags


def from_greenhouse(company: str, board: str) -> list[Job]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    try:
        payload = fetch_json(url)
    except Exception as exc:  # noqa: BLE001 - keep weekly refresh resilient
        print(f"warn: greenhouse {company}: {exc}", file=sys.stderr)
        return []

    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("jobs", []):
        if not isinstance(item, dict):
            continue
        location = clean_text((item.get("location") or {}).get("name"))
        if not is_singapore_location(location):
            continue
        title = clean_text(item.get("title"))
        summary = clean_text(item.get("content"), 280)
        score, tags = score_job(title, company, location, summary)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("absolute_url") or f"https://boards.greenhouse.io/{board}",
                source="Greenhouse",
                published_at=clean_text(item.get("updated_at") or item.get("first_published"))[:10],
                summary=summary or "Singapore role matched by title/company/location metadata.",
                tags=tuple(tags),
                score=score,
            )
        )
    return jobs


def from_remotive(query: str) -> list[Job]:
    url = "https://remotive.com/api/remote-jobs?search=" + urllib.parse.quote(query)
    try:
        payload = fetch_json(url)
    except Exception as exc:  # noqa: BLE001
        print(f"warn: remotive {query}: {exc}", file=sys.stderr)
        return []

    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("jobs", []):
        if not isinstance(item, dict):
            continue
        location = clean_text(item.get("candidate_required_location"))
        if not is_singapore_location(location):
            continue
        title = clean_text(item.get("title"))
        company = clean_text(item.get("company_name"))
        summary = clean_text(item.get("description"), 280)
        score, tags = score_job(title, company, location, summary)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("url") or item.get("job_url") or "https://remotive.com/remote-jobs",
                source="Remotive",
                published_at=clean_text(item.get("publication_date"))[:10],
                summary=summary,
                tags=tuple(tags),
                score=score,
            )
        )
    return jobs


def from_remoteok() -> list[Job]:
    try:
        payload = fetch_json("https://remoteok.com/api")
    except Exception as exc:  # noqa: BLE001
        print(f"warn: remoteok: {exc}", file=sys.stderr)
        return []

    rows = payload[1:] if isinstance(payload, list) and payload else []
    jobs = []
    for item in rows:
        location = clean_text(item.get("location"))
        if not is_singapore_location(location):
            continue
        title = clean_text(item.get("position"))
        company = clean_text(item.get("company"))
        tags_text = " ".join(clean_text(t) for t in item.get("tags", []))
        summary = clean_text(" ".join([tags_text, item.get("description", "")]), 280)
        score, tags = score_job(title, company, location, summary)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("url") or "https://remoteok.com/",
                source="RemoteOK",
                published_at=clean_text(item.get("date"))[:10],
                summary=summary or "Singapore remote role matched by title/location metadata.",
                tags=tuple(tags),
                score=score,
            )
        )
    return jobs


def dedupe(jobs: Iterable[Job]) -> list[Job]:
    seen = set()
    unique = []
    for job in jobs:
        key = (job.title.lower(), job.company.lower(), job.location.lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return sorted(unique, key=lambda j: (-j.score, j.company.lower(), j.title.lower()))


def main() -> int:
    all_jobs: list[Job] = []
    for company, board in GREENHOUSE_BOARDS.items():
        all_jobs.extend(from_greenhouse(company, board))
        time.sleep(0.2)
    for query in SEARCH_QUERIES:
        all_jobs.extend(from_remotive(query))
        time.sleep(0.2)
    all_jobs.extend(from_remoteok())

    jobs = dedupe(all_jobs)[:40]
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data = {
        "updated_at": now,
        "location_filter": "Singapore / Remote-Singapore",
        "source_note": "Weekly public ATS/feed scan for Singapore AI, LLM, AI-security, product-security, trust/safety, and adjacent security-engineering roles. Links go to the original job posts; verify current availability before applying.",
        "jobs": [
            {
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.url,
                "source": job.source,
                "published_at": job.published_at,
                "summary": job.summary,
                "tags": list(job.tags),
                "score": job.score,
            }
            for job in jobs
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(jobs)} Singapore AI/security jobs to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
