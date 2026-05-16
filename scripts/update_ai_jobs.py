#!/usr/bin/env python3
"""Refresh Singapore AI / AI-security job leads for the Hinotoi GitHub Pages site.

The script intentionally uses public ATS/job-board JSON endpoints and the Python
standard library only, so the weekly GitHub Actions job does not need secrets or
extra dependencies. Results are strict to Singapore / Remote-Singapore locations
and then ranked for AI-security, penetration testing, red-team, AppSec,
product-security, trust/safety, and adjacent security-engineering signals. The
ranking is also weighted with broad, non-contact CV-fit signals: offensive
security leadership, incident response, VAPT, adversary emulation, AI security,
agent trust boundaries, vulnerability research, and cloud/application/product
security. The generated page intentionally publishes only the top 10 roles each
week.
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

MAX_JOBS = 10

SEARCH_QUERIES = [
    "AI security Singapore",
    "LLM security Singapore",
    "AI red team Singapore",
    "AI safety security Singapore",
    "machine learning security Singapore",
    "application security AI Singapore",
    "product security AI Singapore",
    "penetration testing Singapore",
    "penetration tester Singapore",
    "red team Singapore",
    "offensive security Singapore",
    "security engineer machine learning Singapore",
]

MYCAREERSFUTURE_QUERIES = SEARCH_QUERIES + [
    "cyber security AI",
    "application security",
    "product security",
    "penetration testing",
    "penetration tester",
    "red team",
    "offensive security",
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
    "cybersecurity",
    "trust and safety",
    "safety",
    "risk",
    "abuse",
    "red team",
    "penetration testing",
    "penetration tester",
    "pentest",
    "offensive security",
    "application security",
    "appsec",
    "product security",
    "cloud security",
    "detection",
    "threat",
    "vulnerability",
    "incident response",
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

CV_MATCH_TERMS = {
    "Offensive Security": [
        "offensive security",
        "penetration testing",
        "penetration tester",
        "pentest",
        "red team",
        "adversary emulation",
        "attack path",
        "exploitability",
        "vapt",
    ],
    "AI Security": [
        "ai security",
        "agentic ai",
        "agent security",
        "llm security",
        "model security",
        "prompt injection",
        "rag",
        "machine learning security",
        "cybersecurity ai",
        "cyber-physical security",
    ],
    "Vulnerability Research": [
        "vulnerability research",
        "vulnerability triage",
        "source code review",
        "secure code",
        "security research",
        "cve",
        "open-source",
        "oss",
        "product security advisory",
    ],
    "App/Product Security": [
        "application security",
        "appsec",
        "product security",
        "cloud security",
        "secure development",
        "security architect",
        "security engineer",
    ],
    "Incident Response": [
        "incident response",
        "detection engineering",
        "threat hunting",
        "threat intelligence",
        "forensics",
        "purple teaming",
    ],
    "Leadership": [
        "lead",
        "manager",
        "principal",
        "staff",
        "architect",
        "consultant",
        "governance",
        "executive reporting",
        "remediation planning",
    ],
}

CV_STRONG_TITLE_TERMS = [
    "offensive security",
    "penetration testing",
    "red team",
    "product security",
    "application security",
    "ai security",
    "agentic ai",
    "vulnerability",
    "incident response",
]

EXCLUDED_TITLE_TERMS = [
    "account executive",
    "partner manager",
    "field marketing",
    "marketing manager",
    "finance & strategy",
    "product support",
    "support specialist",
    "account manager",
    "sales",
    "business development",
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
    "penetration testing",
    "penetration tester",
    "pentest",
    "red team",
    "offensive security",
    "application security",
    "appsec",
    "product security",
    "vulnerability",
    "threat detection",
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
    cv_score: int
    fit: tuple[str, ...]
    priority: str
    why_match: str
    possible_gap: str
    categories: tuple[str, ...]
    score_breakdown: dict[str, int]


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


def fetch_json(url: str, extra_headers: dict[str, str] | None = None) -> object:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
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


def cv_fit_score(title: str, company: str, location: str, summary: str) -> tuple[int, list[str]]:
    text = " ".join([title, company, location, summary])
    title_text = title.lower()
    score = 0
    labels: list[str] = []
    for label, terms in CV_MATCH_TERMS.items():
        hits = set(term_hits(text, terms))
        if not hits:
            continue
        labels.append(label)
        score += 5 + min(len(hits), 4) * 2
        if any(term in title_text for term in terms):
            score += 4
    if any(term in title_text for term in CV_STRONG_TITLE_TERMS):
        score += 6
    if "manager" in title_text or "lead" in title_text or "architect" in title_text:
        score += 3
    return score, labels[:4]


def bounded(value: float, lower: int = 0, upper: int = 100) -> int:
    return max(lower, min(upper, round(value)))


def freshness_score(published_at: str) -> int:
    if not published_at:
        return 45
    try:
        published = datetime.fromisoformat(published_at[:10]).replace(tzinfo=timezone.utc)
    except ValueError:
        return 45
    age_days = max(0, (datetime.now(timezone.utc) - published).days)
    if age_days <= 7:
        return 100
    if age_days <= 21:
        return 82
    if age_days <= 45:
        return 65
    if age_days <= 90:
        return 45
    return 25


def noise_penalty(title: str, summary: str) -> int:
    text = f"{title} {summary}".lower()
    penalty = 0
    if any(term in text for term in ["sales", "account manager", "business development", "pre-sales", "presales"]):
        penalty += 35
    if any(term in text for term in ["intern", "internship", "fresh graduate", "junior"]):
        penalty += 22
    if any(term in text for term in ["governance", "compliance", "audit", "grc"]):
        penalty += 10
    if "security" not in text and not any(term in text for term in ["red team", "penetration", "appsec", "vulnerability"]):
        penalty += 25
    return penalty


def classify_categories(title: str, summary: str, fit: list[str]) -> list[str]:
    text = f"{title} {summary}".lower()
    categories: list[str] = []
    if "AI Security" in fit or any(term in text for term in ["agentic ai", "ai security", "llm security", "prompt injection", "model security"]):
        categories.append("Best AI-security role")
    if "Offensive Security" in fit or any(term in text for term in ["penetration", "pentest", "red team", "offensive security"]):
        categories.append("Best pentest/red-team role")
    if "App/Product Security" in fit or any(term in text for term in ["application security", "appsec", "product security", "secure sdlc"]):
        categories.append("Best product/AppSec role")
    if "Vulnerability Research" in fit or any(term in text for term in ["research", "vulnerability", "source code review", "cve"]):
        categories.append("Best research role")
    if "Leadership" in fit or any(term in text for term in ["lead", "manager", "architect", "principal", "staff"]):
        categories.append("Best leadership role")
    return categories[:3] or ["Best overall match"]


def explain_match(title: str, fit: list[str], categories: list[str], breakdown: dict[str, int]) -> tuple[str, str, str]:
    if breakdown["final"] >= 85:
        priority = "High"
    elif breakdown["final"] >= 70:
        priority = "Medium-high"
    elif breakdown["final"] >= 58:
        priority = "Medium"
    else:
        priority = "Watchlist"

    fit_text = ", ".join(fit[:3]) if fit else "general Singapore security relevance"
    category_text = ", ".join(label.replace("Best ", "").replace(" role", "") for label in categories[:2])
    why = (
        f"Strong overlap with {fit_text}. The ranking also weights this as {category_text}, "
        f"with CV fit {breakdown['cv_fit']}/100 and AI/security relevance {breakdown['ai_security']}/100."
    )

    lower_title = title.lower()
    if "research" in lower_title or "fellow" in lower_title:
        gap = "Check academic contract length, publication expectations, and whether the role values hands-on offensive security work."
    elif "architect" in lower_title or "manager" in lower_title or "lead" in lower_title:
        gap = "Be ready to show senior ownership, stakeholder influence, and examples of turning findings into durable engineering fixes."
    elif "product" in lower_title or "application" in lower_title:
        gap = "Prepare examples around secure SDLC, code review, and product-risk tradeoffs beyond pure pentesting."
    elif "ai" in lower_title or "agent" in lower_title or "llm" in lower_title:
        gap = "Emphasize AI-agent threat models and practical testing evidence, since requirements may expect ML/security depth."
    else:
        gap = "Verify the day-to-day scope is technical and not mostly compliance, sales, or generic security operations."
    return priority, why, gap


def score_job(title: str, company: str, location: str, summary: str, published_at: str = "") -> tuple[int, list[str], int, list[str], str, str, str, list[str], dict[str, int]]:
    text = " ".join([title, company, location, summary])
    title_text = title.lower()
    ai_hits = term_hits(text, AI_TERMS)
    security_hits = term_hits(text, SECURITY_TERMS)
    engineering_hits = term_hits(text, ENGINEERING_TERMS)
    title_hits = term_hits(title, TITLE_RELEVANCE_TERMS)
    cv_raw, cv_labels = cv_fit_score(title, company, location, summary)

    if any(term in title_text for term in EXCLUDED_TITLE_TERMS):
        return 0, [], 0, [], "Filtered", "Excluded by title noise terms.", "", [], {}

    cv_fit = bounded(cv_raw * 2.25)
    ai_security = bounded(
        len(set(ai_hits)) * 11
        + len(set(security_hits)) * 9
        + len(set(title_hits)) * 7
        + (18 if ai_hits and security_hits else 0)
        + (12 if any(term in title_text for term in ["ai security", "agentic ai", "llm security", "red team", "penetration", "product security", "application security"]) else 0)
    )
    career_upside = bounded(
        42
        + (20 if any(term in title_text for term in ["lead", "manager", "principal", "staff", "architect", "senior"]) else 0)
        + (12 if any(term in title_text for term in ["research", "fellow", "engineer", "consultant"]) else 0)
        + (8 if company.lower() in {"okx", "national university of singapore", "nanyang technological university"} or "keysight" in company.lower() else 0)
    )
    location_fit = 100 if "singapore" in location.lower() else 80 if is_singapore_location(location) else 0
    freshness = freshness_score(published_at)
    penalty = noise_penalty(title, summary)
    final = bounded((0.45 * cv_fit) + (0.25 * ai_security) + (0.15 * career_upside) + (0.10 * location_fit) + (0.05 * freshness) - penalty)

    tags = []
    for hit in list(dict.fromkeys(title_hits + ai_hits + security_hits + engineering_hits))[:6]:
        tags.append(hit.title() if hit.islower() else hit)
    categories = classify_categories(title, summary, cv_labels)
    breakdown = {
        "final": final,
        "cv_fit": cv_fit,
        "ai_security": ai_security,
        "career_upside": career_upside,
        "location_fit": location_fit,
        "freshness": freshness,
        "noise_penalty": penalty,
    }
    priority, why_match, possible_gap = explain_match(title, cv_labels, categories, breakdown)
    return final, tags, cv_fit, cv_labels, priority, why_match, possible_gap, categories, breakdown


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
        published_at = clean_text(item.get("updated_at") or item.get("first_published"))[:10]
        score, tags, cv_score, fit, priority, why_match, possible_gap, categories, score_breakdown = score_job(title, company, location, summary, published_at)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("absolute_url") or f"https://boards.greenhouse.io/{board}",
                source="Greenhouse",
                published_at=published_at,
                summary=summary or "Singapore role matched by title/company/location metadata.",
                tags=tuple(tags),
                score=score,
                cv_score=cv_score,
                fit=tuple(fit),
                priority=priority,
                why_match=why_match,
                possible_gap=possible_gap,
                categories=tuple(categories),
                score_breakdown=score_breakdown,
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
        published_at = clean_text(item.get("publication_date"))[:10]
        score, tags, cv_score, fit, priority, why_match, possible_gap, categories, score_breakdown = score_job(title, company, location, summary, published_at)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("url") or item.get("job_url") or "https://remotive.com/remote-jobs",
                source="Remotive",
                published_at=published_at,
                summary=summary,
                tags=tuple(tags),
                score=score,
                cv_score=cv_score,
                fit=tuple(fit),
                priority=priority,
                why_match=why_match,
                possible_gap=possible_gap,
                categories=tuple(categories),
                score_breakdown=score_breakdown,
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
        published_at = clean_text(item.get("date"))[:10]
        score, tags, cv_score, fit, priority, why_match, possible_gap, categories, score_breakdown = score_job(title, company, location, summary, published_at)
        if score < 9:
            continue
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=item.get("url") or "https://remoteok.com/",
                source="RemoteOK",
                published_at=published_at,
                summary=summary or "Singapore remote role matched by title/location metadata.",
                tags=tuple(tags),
                score=score,
                cv_score=cv_score,
                fit=tuple(fit),
                priority=priority,
                why_match=why_match,
                possible_gap=possible_gap,
                categories=tuple(categories),
                score_breakdown=score_breakdown,
            )
        )
    return jobs


def mcf_company(item: dict) -> str:
    for key in ("postedCompany", "hiringCompany"):
        value = item.get(key)
        if isinstance(value, dict) and value.get("name"):
            return clean_text(value.get("name"))
    return "MyCareersFuture employer"


def mcf_location(item: dict) -> str:
    address = item.get("address") if isinstance(item.get("address"), dict) else {}
    if address.get("isOverseas"):
        country = clean_text(address.get("overseasCountry"))
        return country or "Overseas"
    districts = address.get("districts") if isinstance(address.get("districts"), list) else []
    if districts and isinstance(districts[0], dict) and districts[0].get("region"):
        return f"Singapore · {clean_text(districts[0].get('region'))}"
    return "Singapore"


def from_mycareersfuture(query: str, limit: int = 20) -> list[Job]:
    params = urllib.parse.urlencode({"search": query, "limit": limit, "page": 0})
    url = f"https://api.mycareersfuture.gov.sg/v2/jobs?{params}"
    try:
        payload = fetch_json(
            url,
            {
                "mcf-client": "jobseeker",
                "Origin": "https://www.mycareersfuture.gov.sg",
                "Referer": "https://www.mycareersfuture.gov.sg/",
            },
        )
    except Exception as exc:  # noqa: BLE001
        print(f"warn: mycareersfuture {query}: {exc}", file=sys.stderr)
        return []

    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("results", []):
        if not isinstance(item, dict):
            continue
        location = mcf_location(item)
        if not is_singapore_location(location):
            continue
        title = clean_text(item.get("title"))
        company = mcf_company(item)
        description_bits = [item.get("description", ""), item.get("otherRequirements", "")]
        summary = clean_text(" ".join(str(bit or "") for bit in description_bits), 280)
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        published_at = clean_text(metadata.get("newPostingDate") or metadata.get("originalPostingDate") or metadata.get("createdAt"))[:10]
        score, tags, cv_score, fit, priority, why_match, possible_gap, categories, score_breakdown = score_job(title, company, location, summary, published_at)
        if score < 12:
            continue
        job_url = metadata.get("jobDetailsUrl") or f"https://www.mycareersfuture.gov.sg/job/{item.get('uuid', '')}"
        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=job_url,
                source="MyCareersFuture",
                published_at=published_at,
                summary=summary or "Singapore role matched from MyCareersFuture job metadata.",
                tags=tuple(tags),
                score=score + 2,
                cv_score=cv_score,
                fit=tuple(fit),
                priority=priority,
                why_match=why_match,
                possible_gap=possible_gap,
                categories=tuple(categories),
                score_breakdown={**score_breakdown, "final": score + 2, "source_boost": 2},
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
    for query in MYCAREERSFUTURE_QUERIES:
        all_jobs.extend(from_mycareersfuture(query))
        time.sleep(0.2)

    jobs = dedupe(all_jobs)[:MAX_JOBS]
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data = {
        "updated_at": now,
        "location_filter": "Singapore / Remote-Singapore",
        "source_note": "Weekly top-10 public ATS/feed scan for Singapore AI-security, LLM-security, penetration-testing, red-team, AppSec, product-security, trust/safety, and adjacent security-engineering roles. Ranking is weighted against broad CV-fit signals: offensive security leadership, incident response, VAPT/adversary emulation, AI security, agent trust boundaries, vulnerability research, and cloud/application/product security. Links go to the original job posts; verify current availability before applying.",
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
                "cv_score": job.cv_score,
                "fit": list(job.fit),
                "priority": job.priority,
                "why_match": job.why_match,
                "possible_gap": job.possible_gap,
                "categories": list(job.categories),
                "score_breakdown": job.score_breakdown,
            }
            for job in jobs
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(jobs)} top Singapore CV-weighted AI-security/pentest jobs to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
