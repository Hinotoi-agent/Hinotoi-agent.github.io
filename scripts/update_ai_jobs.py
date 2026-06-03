#!/usr/bin/env python3
"""Refresh Singapore AI job-search leads for the Hinotoi GitHub Pages site.

Static generator for a weekly, public, Singapore-focused AI/security job search.
It intentionally uses public ATS/job-board JSON endpoints and the Python standard
library only, so GitHub Actions does not need secrets or extra dependencies.

The generator:
- collects public Greenhouse, Lever, Ashby, Remotive, RemoteOK, and MyCareersFuture roles;
- allows Singapore, Remote-Singapore, APAC, Asia, UTC+8, or broad remote roles when text indicates Singapore/APAC eligibility;
- scores against broad non-sensitive CV-fit signals instead of publishing private CV details;
- keeps a small history file to label new/still-open/removed roles across refreshes;
- writes both the rendered feed and a high-priority alert subset for the page/optional digests.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_data" / "ai_jobs.json"
HISTORY_OUT = ROOT / "_data" / "ai_jobs_history.json"
USER_AGENT = "HinotoiJobWatcher/2.0 (+https://hinotoi-agent.github.io/ai-jobs/)"
MAX_JOBS = 10
ALERT_SCORE = 85
PUBLISH_SCORE = 58
MIN_MONTHLY_COMPENSATION_SGD = 11_000
MIN_ANNUAL_COMPENSATION_SGD = MIN_MONTHLY_COMPENSATION_SGD * 12

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
    "Scale AI": "scaleai",
    "GitLab": "gitlab",
}

LEVER_COMPANIES = {
    "Mistral AI": "mistral",
}

ASHBY_BOARDS = {
    "OpenAI": "openai",
    "Cursor": "cursor",
    "Harvey": "harvey",
    "Perplexity": "perplexity",
    "Replit": "replit",
    "Modal": "modal",
}

PRIORITY_COMPANIES = {
    "anthropic", "openai", "google deepmind", "deepmind", "cloudflare", "stripe", "wiz", "snyk",
    "hackerone", "databricks", "okx", "grab", "govtech", "keysight", "bytedance", "tiktok",
    "sea", "singtel", "st engineering", "microsoft", "amazon", "meta", "palantir", "chainguard",
}

SEARCH_QUERIES = [
    "AI security Singapore",
    "AI security manager Singapore",
    "AI security engineer Singapore",
    "LLM security Singapore",
    "agent security Singapore",
    "AI red team Singapore",
    "AI safety security Singapore",
    "machine learning security Singapore",
    "AI secure code review Singapore",
    "AI vulnerability research Singapore",
    "RAG security Singapore",
    "prompt injection Singapore",
    "DevSecOps AI Singapore",
    "cloud security manager Singapore",
    "application security AI Singapore",
    "application security manager Singapore",
    "appsec manager Singapore",
    "application security lead Singapore",
    "software security manager Singapore",
    "product security AI Singapore",
    "product security manager Singapore",
    "penetration testing Singapore",
    "penetration tester Singapore",
    "red team Singapore",
    "offensive security Singapore",
    "vulnerability research Singapore",
    "security engineer machine learning Singapore",
    "trust safety security Singapore",
]

MYCAREERSFUTURE_QUERIES = SEARCH_QUERIES + [
    "cyber security AI",
    "AI security engineer",
    "AI security manager",
    "secure code review",
    "DevSecOps",
    "cloud security manager",
    "cyber range",
    "application security",
    "application security manager",
    "appsec manager",
    "application security lead",
    "software security manager",
    "product security",
    "product security manager",
    "penetration testing",
    "penetration tester",
    "red team",
    "offensive security",
    "vulnerability research",
    "threat research",
    "secure software development",
]

AI_TERMS = [
    "ai", "artificial intelligence", "machine learning", "ml", "llm", "large language model",
    "genai", "generative ai", "agent", "agentic", "deep learning", "model security",
    "prompt injection", "content injection", "guardrail", "rag", "ai safety", "adversarial ml",
    "ai-assisted", "secure code review", "mcp", "model context protocol", "ollama", "azure ai foundry",
    "research engineer",
]

SECURITY_TERMS = [
    "security", "cyber", "cybersecurity", "trust and safety", "safety", "risk", "abuse",
    "red team", "penetration testing", "penetration tester", "pentest", "offensive security",
    "adversary emulation", "attack path", "exploitability", "vapt", "cyber range",
    "application security", "appsec", "product security", "cloud security", "detection",
    "threat", "vulnerability", "incident response", "fraud", "secure sdlc", "code review",
    "source code review", "devsecops", "security automation", "purple team",
]

ENGINEERING_TERMS = ["engineer", "researcher", "scientist", "architect", "analyst", "manager", "lead", "specialist", "consultant"]

CV_MATCH_TERMS = {
    "Offensive Security": ["offensive security", "penetration testing", "penetration tester", "pentest", "red team", "adversary emulation", "attack path", "attack-path validation", "exploitability", "vapt", "cyber range", "crto", "crtp", "oscp", "oswe"],
    "AI Security": ["ai security", "ai security manager", "ai security engineer", "agentic ai", "agent security", "llm security", "model security", "prompt injection", "content injection", "guardrail", "rag", "machine learning security", "cybersecurity ai", "adversarial ml", "ai-assisted secure code review", "mcp", "model context protocol", "azure ai foundry", "ollama"],
    "Vulnerability Research": ["vulnerability research", "vulnerability triage", "source code review", "secure code", "security research", "cve", "open-source", "oss", "product security advisory", "root cause", "variant analysis", "disclosure"],
    "App/Product Security": ["application security", "appsec", "application security manager", "appsec manager", "application security lead", "software security manager", "product security", "product security manager", "cloud security", "cloud security manager", "secure development", "security architect", "security engineer", "secure sdlc", "devsecops", "code review", "secure code review", "security automation"],
    "Incident Response": ["incident response", "detection engineering", "threat hunting", "threat intelligence", "forensics", "purple teaming", "mad20", "mitre attack"],
    "Leadership": ["lead", "manager", "principal", "staff", "architect", "consultant", "governance", "executive reporting", "remediation planning", "stakeholder", "program", "roadmap", "service delivery"],
}

CV_STRONG_TITLE_TERMS = ["offensive security", "penetration testing", "red team", "product security", "product security manager", "application security", "application security manager", "application security lead", "appsec", "appsec manager", "software security manager", "cloud security manager", "devsecops", "ai security", "ai security manager", "ai security engineer", "agentic ai", "llm security", "vulnerability", "incident response", "cyber range"]

EXCLUDED_TITLE_TERMS = [
    "account executive", "partner manager", "field marketing", "marketing manager", "finance & strategy",
    "product support", "support specialist", "account manager", "sales", "business development",
    "customer success", "solutions sales", "talent acquisition", "recruiter", "office manager",
]

BAD_FIT_TERMS = [
    "sales", "account manager", "business development", "pre-sales", "presales", "customer success",
    "support specialist", "help desk", "desktop support", "soc analyst l1", "tier 1", "intern", "internship",
    "fresh graduate", "junior", "governance", "compliance", "audit", "grc", "policy only",
]

TITLE_RELEVANCE_TERMS = [
    *AI_TERMS, *SECURITY_TERMS, "data scientist", "data analyst", "data infra", "model risk", "quant",
    "agent infrastructure", "security research", "threat detection", "software security", "secure code",
]

SINGAPORE_PATTERNS = [re.compile(r"\bsingapore\b", re.I), re.compile(r"\bsg\b", re.I), re.compile(r"remote\s*-?\s*singapore", re.I)]
REMOTE_SG_PATTERNS = [
    re.compile(r"remote\s*-?\s*singapore", re.I), re.compile(r"singapore\s*\(?remote\)?", re.I),
    re.compile(r"\bapac\b", re.I), re.compile(r"\basia\b", re.I), re.compile(r"\butc\+?8\b", re.I),
    re.compile(r"\bglobal remote\b", re.I), re.compile(r"\bworldwide\b", re.I),
]
DISALLOWED_REMOTE_LOCATION_PATTERNS = [
    re.compile(r"\bremote\b.*\b(usa|united states|us only|canada|united kingdom|uk|europe|emea)\b", re.I),
    re.compile(r"\b(san francisco|foster city|seattle|new york|london|toronto|berlin|paris|dublin)\b", re.I),
    re.compile(r"\b(CA|NY|WA|TX|MA|IL|DC)\b"),
    re.compile(r"\b(required|must be based)\b.*\b(usa|united states|uk|united kingdom|europe)\b", re.I),
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
    salary_estimate: str
    tags: tuple[str, ...]
    score: int
    cv_score: int
    fit: tuple[str, ...]
    priority: str
    why_match: str
    possible_gap: str
    compensation_fit: int
    categories: tuple[str, ...]
    score_breakdown: dict[str, int]
    seniority: str
    apply_angle: str
    skillsets_to_build: tuple[str, ...]
    learning_gaps: tuple[str, ...]
    certifications_to_consider: tuple[str, ...]
    alert_reason: str
    next_action: str = ""
    status_badge: str = ""
    first_seen: str = ""
    last_seen: str = ""
    status: str = "New"


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
    return bool(location and any(pattern.search(location) for pattern in SINGAPORE_PATTERNS))


def is_remote_singapore_eligible(location: str, text: str = "") -> bool:
    combined = f"{location} {text}"
    if is_singapore_location(combined):
        return True
    if any(pattern.search(location or "") for pattern in DISALLOWED_REMOTE_LOCATION_PATTERNS):
        return False
    # Keep remote roles only when they explicitly mention APAC/Asia/UTC+8/global eligibility, not US/UK-only remote.
    return bool(combined and any(pattern.search(combined) for pattern in REMOTE_SG_PATTERNS))


def term_hits(text: str, terms: Iterable[str]) -> list[str]:
    haystack = text.lower()
    hits: list[str] = []
    for term in terms:
        lowered = term.lower()
        if len(lowered) <= 3:
            if re.search(rf"(?<![a-z0-9]){re.escape(lowered)}(?![a-z0-9])", haystack):
                hits.append(term.upper() if term in {"ai", "ml", "llm"} else term)
        elif lowered in haystack:
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
        score += 7
    if any(term in title_text for term in ["manager", "lead", "architect", "principal", "staff"]):
        score += 4
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
        return 58
    if age_days <= 90:
        return 32
    return 12


def detect_seniority(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    if any(t in text for t in ["principal", "staff", "head of", "director"]):
        return "Staff/principal"
    if any(t in text for t in ["manager", "lead", "architect"]):
        return "Lead/manager"
    if any(t in text for t in ["senior", "sr."]):
        return "Senior"
    if any(t in text for t in ["intern", "internship", "junior", "graduate"]):
        return "Junior"
    return "Mid/senior"


def company_boost(company: str) -> int:
    lower = company.lower()
    return 8 if any(name in lower for name in PRIORITY_COMPANIES) else 0


def noise_penalty(title: str, summary: str) -> int:
    text = f"{title} {summary}".lower()
    penalty = 0
    for term in BAD_FIT_TERMS:
        if term in text:
            penalty += 14
    if any(term in text for term in ["governance", "compliance", "audit", "grc"]):
        penalty += 12
    if "security" not in text and not any(term in text for term in ["red team", "penetration", "appsec", "vulnerability", "threat", "secure"]):
        penalty += 28
    if "ai" not in text and not any(term in text for term in ["llm", "machine learning", "agent", "model", "red team", "penetration", "appsec", "vulnerability"]):
        penalty += 8
    return min(penalty, 75)


def classify_categories(title: str, summary: str, fit: list[str]) -> list[str]:
    text = f"{title} {summary}".lower()
    categories: list[str] = []
    if "AI Security" in fit or any(term in text for term in ["agentic ai", "ai security", "llm security", "prompt injection", "model security", "adversarial ml"]):
        categories.append("Best AI-security role")
    if "Offensive Security" in fit or any(term in text for term in ["penetration", "pentest", "red team", "offensive security"]):
        categories.append("Best pentest/red-team role")
    if "App/Product Security" in fit or any(term in text for term in ["application security", "appsec", "product security", "secure sdlc", "code review"]):
        categories.append("Best product/AppSec role")
    if "Vulnerability Research" in fit or any(term in text for term in ["research", "vulnerability", "source code review", "cve"]):
        categories.append("Best research role")
    if "Incident Response" in fit or any(term in text for term in ["incident response", "detection engineering", "threat hunting"]):
        categories.append("Best incident-response role")
    if "Leadership" in fit or any(term in text for term in ["lead", "manager", "architect", "principal", "staff"]):
        categories.append("Best leadership role")
    return categories[:4] or ["Best overall match"]


def explain_match(title: str, fit: list[str], categories: list[str], breakdown: dict[str, int], seniority: str) -> tuple[str, str, str, str]:
    if breakdown["final"] >= 85:
        priority = "High"
    elif breakdown["final"] >= 72:
        priority = "Medium-high"
    elif breakdown["final"] >= 58:
        priority = "Medium"
    else:
        priority = "Watchlist"

    fit_text = ", ".join(fit[:3]) if fit else "general Singapore security relevance"
    category_text = ", ".join(label.replace("Best ", "").replace(" role", "") for label in categories[:2])
    why = (
        f"Strong overlap with {fit_text}. Ranked as {category_text}, with CV fit "
        f"{breakdown['cv_fit']}/100, AI/security relevance {breakdown['ai_security']}/100, "
        f"and {seniority.lower()} trajectory."
    )

    lower_title = title.lower()
    if "research" in lower_title or "fellow" in lower_title:
        gap = "Check contract length, publication expectations, and whether the role values hands-on offensive security work."
        angle = "Lead with vulnerability research, threat-model depth, and examples that translated research into practical mitigations."
    elif any(t in lower_title for t in ["architect", "manager", "lead", "principal", "staff"]):
        gap = "Be ready to show senior ownership, stakeholder influence, and examples of turning findings into durable engineering fixes."
        angle = "Position around senior security ownership: prioritization, cross-functional influence, and durable remediation plans."
    elif "product" in lower_title or "application" in lower_title or "appsec" in lower_title:
        gap = "Prepare examples around secure SDLC, code review, and product-risk tradeoffs beyond pure pentesting."
        angle = "Emphasize AppSec/product-security stories with code review, exploitability analysis, and engineering-friendly fixes."
    elif any(t in lower_title for t in ["ai", "agent", "llm", "model"]):
        gap = "Emphasize AI-agent threat models and practical testing evidence, since requirements may expect ML/security depth."
        angle = "Lead with AI-agent trust boundaries, prompt-injection/RAG risks, and practical security validation evidence."
    elif any(t in lower_title for t in ["penetration", "red team", "offensive"]):
        gap = "Confirm the work includes modern application/cloud targets and is not a narrow checklist testing role."
        angle = "Lead with offensive-security delivery, exploitability judgement, adversary emulation, and clear remediation guidance."
    else:
        gap = "Verify the day-to-day scope is technical and not mostly compliance, sales, or generic security operations."
        angle = "Frame the pitch around technical security judgement, practical fixes, and ability to work across engineering teams."
    return priority, why, gap, angle


def alert_for(score: int, title: str, company: str, fit: list[str], status: str = "") -> str:
    lower = f"{title} {company}".lower()
    reasons = []
    if score >= ALERT_SCORE:
        reasons.append("score ≥ 85")
    if "AI Security" in fit or any(t in lower for t in ["llm security", "agent security", "ai security", "model security", "prompt injection"]):
        reasons.append("AI-security signal")
    if "Offensive Security" in fit or any(t in lower for t in ["red team", "penetration", "offensive security"]):
        reasons.append("offensive-security signal")
    if company_boost(company):
        reasons.append("priority employer")
    if status == "New":
        reasons.append("new this week")
    return ", ".join(reasons[:4])


def learning_plan(title: str, summary: str, fit: list[str], categories: list[str]) -> tuple[list[str], list[str]]:
    """Public, non-sensitive study guidance for improving future match scores."""
    text = f"{title} {summary} {' '.join(fit)} {' '.join(categories)}".lower()
    skills: list[str] = []
    gaps: list[str] = []

    def add(skill: str, gap: str) -> None:
        if skill not in skills:
            skills.append(skill)
        if gap not in gaps:
            gaps.append(gap)

    if any(t in text for t in ["ai", "agent", "llm", "model", "machine learning", "agentic"]):
        add("AI/LLM security testing: prompt injection, tool-use boundaries, RAG abuse cases, model/data leakage, and agent sandboxing.",
            "Prepare 2-3 concrete AI-security case studies showing threat model → exploit path → mitigation → verification.")
    if any(t in text for t in ["product security", "application security", "appsec", "secure sdlc", "code review", "architect"]):
        add("Product/AppSec depth: secure design reviews, source-code review, exploitability triage, threat modeling, and engineering remediation.",
            "Build code-level security fixes and concise design-review writeups, not only assessment findings.")
    if any(t in text for t in ["penetration", "red team", "offensive", "vapt", "adversary"]):
        add("Offensive security delivery: web/cloud/API testing, adversary emulation, reporting, and risk-ranked remediation guidance.",
            "Add evidence of modern cloud/API targets and business-impact exploit chains so the profile reads beyond checklist pentesting.")
    if any(t in text for t in ["incident response", "detection", "threat hunting", "forensics"]):
        add("Detection/IR fundamentals: log analysis, incident scoping, containment, cloud telemetry, and post-incident hardening.",
            "Prepare one IR/detection story with signals used, investigation decisions, and hardening outcome.")
    if any(t in text for t in ["research", "fellow", "vulnerability", "cve", "cyber-physical"]):
        add("Vulnerability research craft: root-cause analysis, reproducible PoCs, variant analysis, disclosure-quality writeups, and patch validation.",
            "Keep a public-safe research portfolio with sanitized PoCs, diagrams, and before/after patch evidence.")
    if any(t in text for t in ["manager", "lead", "architect", "principal", "staff", "consultant"]):
        add("Senior influence: prioritization, stakeholder management, roadmap ownership, metrics, and mentoring/security-program design.",
            "Collect examples where you influenced teams, set security direction, and converted findings into durable process or platform changes.")
    if any(t in text for t in ["cloud", "kubernetes", "aws", "azure", "gcp", "container"]):
        add("Cloud/platform security: IAM, Kubernetes/container boundaries, CI/CD, secrets handling, and cloud-native detection.",
            "Strengthen cloud threat-model examples and hands-on validation across at least one major cloud stack.")

    if not skills:
        add("Technical security communication: concise risk framing, exploitability reasoning, and practical remediation planning.",
            "Clarify whether the role is hands-on technical work; prepare examples that prove engineering depth.")
    return skills[:4], gaps[:4]


def certification_plan(title: str, summary: str, fit: list[str], categories: list[str]) -> list[str]:
    """Public certification/course suggestions that make a candidate more relevant for each role type."""
    text = f"{title} {summary} {' '.join(fit)} {' '.join(categories)}".lower()
    certs: list[str] = []

    def add(item: str) -> None:
        if item not in certs:
            certs.append(item)

    if any(t in text for t in ["ai", "agent", "llm", "model", "machine learning", "agentic", "prompt injection", "rag"]):
        add("AI/LLM security specialization: OWASP Top 10 for LLM Apps, MITRE ATLAS, prompt-injection labs, and one public agent/RAG security writeup.")
        add("Cloud Security Alliance Certificate of Competence in Zero Trust or AI Governance micro-courses if the role blends AI platform risk and governance.")
    if any(t in text for t in ["product security", "application security", "appsec", "secure sdlc", "code review", "architect"]):
        add("CSSLP or a secure-code-review course to signal product-security and SDLC depth beyond testing-only experience.")
        add("AWS Security Specialty, Azure Security Engineer, or Google Professional Cloud Security Engineer for platform-heavy AppSec roles.")
    if any(t in text for t in ["penetration", "red team", "offensive", "vapt", "adversary"]):
        add("OSCP/OSWE-style offensive certification path, prioritizing OSWE if the role emphasizes web/app exploitation and code review.")
        add("CRTO/CARTP-style adversary-emulation training if the role asks for red-team operations or attack-path development.")
    if any(t in text for t in ["incident response", "detection", "threat hunting", "forensics", "soc"]):
        add("GCIA/GCIH/GCFA-style detection and incident-response training, or equivalent hands-on cloud telemetry labs.")
    if any(t in text for t in ["research", "fellow", "vulnerability", "cve", "cyber-physical", "security research"]):
        add("Exploit-development / vulnerability-research track: source-code auditing, fuzzing, root-cause analysis, and disclosure-quality report practice.")
    if any(t in text for t in ["manager", "lead", "principal", "staff", "consultant", "architect"]):
        add("Security leadership signal: CISSP/CISM only if the role explicitly values program ownership, governance, or senior stakeholder management.")
    if any(t in text for t in ["cloud", "kubernetes", "aws", "azure", "gcp", "container"]):
        add("Kubernetes/cloud security track: CKS plus one cloud-provider security specialty aligned to the employer stack.")

    if not certs:
        add("Pick one role-aligned hands-on credential or portfolio project, then publish a concise public-safe case study proving practical impact.")
    return certs[:3]


def score_job(title: str, company: str, location: str, summary: str, published_at: str = "") -> tuple[int, list[str], int, list[str], str, str, str, list[str], dict[str, int], str, str, list[str], list[str], list[str], str]:
    text = " ".join([title, company, location, summary])
    title_text = title.lower()
    ai_hits = term_hits(text, AI_TERMS)
    security_hits = term_hits(text, SECURITY_TERMS)
    engineering_hits = term_hits(text, ENGINEERING_TERMS)
    title_hits = term_hits(title, TITLE_RELEVANCE_TERMS)
    cv_raw, cv_labels = cv_fit_score(title, company, location, summary)

    if any(term in title_text for term in EXCLUDED_TITLE_TERMS):
        return 0, [], 0, [], "Filtered", "Excluded by title noise terms.", "", [], {}, "Excluded", "", [], [], [], ""

    seniority = detect_seniority(title, summary)
    cv_fit = bounded(cv_raw * 2.3)
    ai_security = bounded(
        len(set(ai_hits)) * 11
        + len(set(security_hits)) * 9
        + len(set(title_hits)) * 7
        + (18 if ai_hits and security_hits else 0)
        + (14 if any(term in title_text for term in ["ai security", "agentic ai", "llm security", "red team", "penetration", "product security", "application security", "appsec"]) else 0)
    )
    career_upside = bounded(
        40
        + (22 if seniority in {"Staff/principal", "Lead/manager", "Senior"} else 0)
        + (12 if any(term in title_text for term in ["research", "fellow", "engineer", "consultant", "architect"]) else 0)
        + company_boost(company)
    )
    location_fit = 100 if is_singapore_location(location) else 86 if is_remote_singapore_eligible(location, summary) else 0
    freshness = freshness_score(published_at)
    penalty = noise_penalty(title, summary)
    source_company_boost = company_boost(company)
    final = bounded((0.43 * cv_fit) + (0.27 * ai_security) + (0.14 * career_upside) + (0.10 * location_fit) + (0.06 * freshness) + source_company_boost - penalty)

    tags = []
    for hit in list(dict.fromkeys(title_hits + ai_hits + security_hits + engineering_hits))[:7]:
        tags.append(hit.title() if hit.islower() else hit)
    categories = classify_categories(title, summary, cv_labels)
    breakdown = {
        "final": final,
        "cv_fit": cv_fit,
        "ai_security": ai_security,
        "career_upside": career_upside,
        "location_fit": location_fit,
        "freshness": freshness,
        "company_boost": source_company_boost,
        "noise_penalty": penalty,
    }
    priority, why_match, possible_gap, apply_angle = explain_match(title, cv_labels, categories, breakdown, seniority)
    skillsets_to_build, learning_gaps = learning_plan(title, summary, cv_labels, categories)
    certifications_to_consider = certification_plan(title, summary, cv_labels, categories)
    alert_reason = alert_for(final, title, company, cv_labels)
    return final, tags, cv_fit, cv_labels, priority, why_match, possible_gap, categories, breakdown, seniority, apply_angle, skillsets_to_build, learning_gaps, certifications_to_consider, alert_reason


def money_amount(value: object) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = clean_text(value).lower().replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)\s*([km])?", text)
    if not match:
        return None
    amount = float(match.group(1))
    suffix = match.group(2)
    if suffix == "k":
        amount *= 1_000
    elif suffix == "m":
        amount *= 1_000_000
    return int(amount)


def format_compensation(minimum: object = None, maximum: object = None, currency: str = "SGD", interval: str = "year") -> str:
    low = money_amount(minimum)
    high = money_amount(maximum)
    if low is None and high is None:
        return ""
    currency = clean_text(currency or "SGD").upper()
    interval = clean_text(interval or "year").lower()
    if interval.startswith("month") or interval in {"monthly", "mo"}:
        suffix = "/mo"
    elif interval.startswith("hour") or interval in {"hourly", "hr"}:
        suffix = "/hr"
    else:
        suffix = "/yr"
    def compact(amount: int) -> str:
        return f"{amount // 1000}k" if amount >= 10_000 and amount % 1000 == 0 else f"{amount:,}"
    if low is not None and high is not None and low != high:
        value = f"{currency} {compact(low)}–{compact(high)}{suffix}"
    else:
        amount = low if low is not None else high
        if amount is None:
            return ""
        value = f"{currency} {compact(amount)}{suffix}"
    return f"Listed {value}"


def salary_text_from_value(value: object) -> str:
    if not value:
        return ""
    if isinstance(value, dict):
        salary_type = value.get("type") if isinstance(value.get("type"), dict) else {}
        currency = clean_text(value.get("currency") or value.get("currencyCode") or value.get("salaryCurrency") or "SGD")
        interval = clean_text(value.get("interval") or value.get("period") or value.get("unit") or salary_type.get("salaryType") or "year")
        return format_compensation(value.get("minimum") or value.get("min") or value.get("minValue"), value.get("maximum") or value.get("max") or value.get("maxValue"), currency, interval)
    text = clean_text(value, 120)
    return f"Listed {text}" if text else ""


def fallback_salary_estimate(title: str, location: str, company: str) -> str:
    text = f"{title} {location} {company}".lower()
    low, high = 150_000, 230_000
    if any(term in text for term in ["director", "head of"]):
        low, high = 230_000, 360_000
    elif any(term in text for term in ["principal", "staff", "architect"]):
        low, high = 190_000, 300_000
    elif any(term in text for term in ["manager", "lead"]):
        low, high = 170_000, 280_000
    elif any(term in text for term in ["senior", "sr."]):
        low, high = 140_000, 230_000
    elif any(term in text for term in ["analyst", "associate", "junior", "graduate"]):
        low, high = 80_000, 140_000
    if any(term in text for term in ["remote", "global", "worldwide", "united states"]):
        low, high = int(low * 1.1), int(high * 1.25)
    return format_compensation(low, high, "SGD", "year").replace("Listed", "Est.")


def salary_estimate_for(title: str, company: str, location: str, listed_salary: str = "") -> str:
    listed_salary = clean_text(listed_salary, 140)
    if listed_salary:
        return listed_salary
    return fallback_salary_estimate(title, location, company)


def compensation_monthly_range(salary_text: str) -> tuple[int | None, int | None]:
    """Return estimated/listed monthly SGD range from rendered compensation text."""
    text = clean_text(salary_text).lower().replace(",", "")
    if not text:
        return None, None
    amounts = [float(value) * (1000 if suffix == "k" else 1) for value, suffix in re.findall(r"(\d+(?:\.\d+)?)\s*(k)?", text)]
    if not amounts:
        return None, None
    low = int(min(amounts))
    high = int(max(amounts))
    if "/yr" in text or "year" in text or "annual" in text:
        low, high = round(low / 12), round(high / 12)
    return low, high


def compensation_target_score(salary_text: str) -> int:
    """Score against the user's S$11k+/month target; listed ranges must start at S$11k+."""
    low, high = compensation_monthly_range(salary_text)
    if high is None:
        return 55
    if high < MIN_MONTHLY_COMPENSATION_SGD:
        return 0
    if low is not None and low < MIN_MONTHLY_COMPENSATION_SGD:
        return 0
    return 100


def build_job(title: str, company: str, location: str, url: str, source: str, published_at: str, summary: str, min_score: int, listed_salary: str = "") -> Job | None:
    title = clean_text(title)
    company = clean_text(company) or "Unknown employer"
    location = clean_text(location) or "Remote / APAC"
    summary = clean_text(summary, 320)
    if not title or not url:
        return None
    if not is_remote_singapore_eligible(location, f"{title} {summary}"):
        return None
    score, tags, cv_score, fit, priority, why_match, possible_gap, categories, score_breakdown, seniority, apply_angle, skillsets_to_build, learning_gaps, certifications_to_consider, alert_reason = score_job(title, company, location, summary, published_at)
    if score <= 0 or not score_breakdown:
        return None
    salary_estimate = salary_estimate_for(title, company, location, listed_salary)
    compensation_fit = compensation_target_score(salary_estimate)
    if compensation_fit <= 0:
        return None
    score = bounded(score + (6 if compensation_fit >= 100 else 2 if compensation_fit >= 72 else 0))
    score_breakdown = {**score_breakdown, "final": score, "compensation_fit": compensation_fit, "target_monthly_sgd": MIN_MONTHLY_COMPENSATION_SGD}
    priority, why_match, possible_gap, apply_angle = explain_match(title, fit, categories, score_breakdown, seniority)
    alert_reason = alert_for(score, title, company, fit)
    if score < min_score:
        return None
    return Job(
        title=title, company=company, location=location, url=str(url), source=source, published_at=published_at,
        summary=summary or "Role matched by title/company/location metadata.", salary_estimate=salary_estimate, tags=tuple(tags), score=score,
        cv_score=cv_score, fit=tuple(fit), priority=priority, why_match=why_match, possible_gap=possible_gap, compensation_fit=compensation_fit,
        categories=tuple(categories), score_breakdown=score_breakdown, seniority=seniority, apply_angle=apply_angle,
        skillsets_to_build=tuple(skillsets_to_build), learning_gaps=tuple(learning_gaps),
        certifications_to_consider=tuple(certifications_to_consider), alert_reason=alert_reason,
    )


def source_result(name: str, fn) -> tuple[list[Job], dict[str, object]]:
    started = time.time()
    try:
        jobs = fn()
        return jobs, {"source": name, "status": "ok", "count": len(jobs), "seconds": round(time.time() - started, 2)}
    except Exception as exc:  # noqa: BLE001
        print(f"warn: {name}: {exc}", file=sys.stderr)
        return [], {"source": name, "status": "error", "count": 0, "error": clean_text(exc, 160), "seconds": round(time.time() - started, 2)}


def from_greenhouse(company: str, board: str) -> list[Job]:
    payload = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true")
    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("jobs", []):
        if not isinstance(item, dict):
            continue
        location = clean_text((item.get("location") or {}).get("name"))
        title = clean_text(item.get("title"))
        summary = clean_text(item.get("content"), 320)
        published_at = clean_text(item.get("updated_at") or item.get("first_published"))[:10]
        listed_salary = salary_text_from_value(item.get("salary") or item.get("compensation") or item.get("compensationRange"))
        job = build_job(title, company, location, item.get("absolute_url") or f"https://boards.greenhouse.io/{board}", "Greenhouse", published_at, summary, 14, listed_salary)
        if job:
            jobs.append(job)
    return jobs


def from_lever(company: str, slug: str) -> list[Job]:
    payload = fetch_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    rows = payload if isinstance(payload, list) else []
    jobs = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        categories = item.get("categories") if isinstance(item.get("categories"), dict) else {}
        location = clean_text(categories.get("location") or item.get("workplaceType") or "Remote")
        title = clean_text(item.get("text"))
        description = item.get("descriptionPlain") or item.get("description") or ""
        lists = item.get("lists") if isinstance(item.get("lists"), list) else []
        extra = " ".join(clean_text(" ".join(str(v) for v in block.get("content", "") if False)) for block in [])
        summary = clean_text(f"{description} {extra}", 320)
        published_at = ""
        created_at = item.get("createdAt")
        if isinstance(created_at, int) and created_at > 0:
            published_at = datetime.fromtimestamp(created_at / 1000, tz=timezone.utc).date().isoformat()
        listed_salary = salary_text_from_value(item.get("salaryRange") or item.get("compensation") or item.get("salary"))
        job = build_job(title, company, location, item.get("hostedUrl") or item.get("applyUrl") or f"https://jobs.lever.co/{slug}", "Lever", published_at, summary, 18, listed_salary)
        if job:
            jobs.append(job)
    return jobs


def from_ashby(company: str, board: str) -> list[Job]:
    payload = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}")
    rows = payload.get("jobs", []) if isinstance(payload, dict) else []
    jobs = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        location = clean_text(item.get("location") or item.get("locationName") or "Remote")
        title = clean_text(item.get("title"))
        summary = clean_text(item.get("descriptionPlain") or item.get("descriptionHtml") or "", 320)
        published_at = clean_text(item.get("publishedDate") or item.get("createdAt"))[:10]
        url = item.get("jobUrl") or item.get("externalLink") or f"https://jobs.ashbyhq.com/{board}"
        listed_salary = salary_text_from_value(item.get("compensationTierSummary") or item.get("compensation") or item.get("salary"))
        job = build_job(title, company, location, url, "Ashby", published_at, summary, 18, listed_salary)
        if job:
            jobs.append(job)
    return jobs


def from_remotive(query: str) -> list[Job]:
    url = "https://remotive.com/api/remote-jobs?search=" + urllib.parse.quote(query)
    payload = fetch_json(url)
    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("jobs", []):
        if not isinstance(item, dict):
            continue
        job = build_job(
            item.get("title"), item.get("company_name"), item.get("candidate_required_location"),
            item.get("url") or item.get("job_url") or "https://remotive.com/remote-jobs", "Remotive",
            clean_text(item.get("publication_date"))[:10], item.get("description"), 18,
            salary_text_from_value(item.get("salary")),
        )
        if job:
            jobs.append(job)
    return jobs


def from_remoteok() -> list[Job]:
    payload = fetch_json("https://remoteok.com/api")
    rows = payload[1:] if isinstance(payload, list) and payload else []
    jobs = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        tags_text = " ".join(clean_text(t) for t in item.get("tags", []) if t)
        listed_salary = format_compensation(item.get("salary_min"), item.get("salary_max"), item.get("salary_currency") or "USD", "year")
        job = build_job(
            item.get("position"), item.get("company"), item.get("location"), item.get("url") or "https://remoteok.com/",
            "RemoteOK", clean_text(item.get("date"))[:10], f"{tags_text} {item.get('description', '')}", 18, listed_salary,
        )
        if job:
            jobs.append(job)
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


def from_mycareersfuture(query: str, limit: int = 25) -> list[Job]:
    params = urllib.parse.urlencode({"search": query, "limit": limit, "page": 0})
    payload = fetch_json(
        f"https://api.mycareersfuture.gov.sg/v2/jobs?{params}",
        {"mcf-client": "jobseeker", "Origin": "https://www.mycareersfuture.gov.sg", "Referer": "https://www.mycareersfuture.gov.sg/"},
    )
    if not isinstance(payload, dict):
        return []
    jobs = []
    for item in payload.get("results", []):
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        url = metadata.get("jobDetailsUrl") or f"https://www.mycareersfuture.gov.sg/job/{item.get('uuid', '')}"
        job = build_job(
            item.get("title"), mcf_company(item), mcf_location(item), url, "MyCareersFuture",
            clean_text(metadata.get("newPostingDate") or metadata.get("originalPostingDate") or metadata.get("createdAt"))[:10],
            " ".join(str(bit or "") for bit in [item.get("description", ""), item.get("otherRequirements", "")]), 14,
            salary_text_from_value(item.get("salary")),
        )
        if job:
            bumped = min(100, job.score + 2)
            breakdown = {**job.score_breakdown, "final": bumped, "source_boost": 2}
            jobs.append(replace(job, score=bumped, score_breakdown=breakdown, alert_reason=alert_for(bumped, job.title, job.company, list(job.fit))))
    return jobs


def stable_key(value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).digest()
    # Base32 avoids 8/9-heavy hexadecimal substrings that look like Singapore mobile numbers in public privacy scans.
    return base64.b32encode(digest).decode("ascii").rstrip("=").lower()[:18]


def normalized_history_key(title: str, company: str, fallback: str = "") -> str:
    normalized_company = re.sub(r"\b(pte\.? ltd\.?|pte|ltd|limited|inc\.?|corp\.?|corporation|llc|singapore|sales)\b", "", company.lower())
    normalized_company = SPACE_RE.sub(" ", re.sub(r"[^a-z0-9]+", " ", normalized_company)).strip()
    normalized_title = SPACE_RE.sub(" ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()
    if normalized_company and normalized_title:
        return stable_key(f"{normalized_company}|{normalized_title}")
    return stable_key(fallback or f"{title}|{company}".lower())



def status_badge_for(status: str, score: int, first_seen: str, now_date: str) -> str:
    """Compact public badge for rendering; no private tracker state."""
    if status == "New":
        return "New this week"
    if score >= ALERT_SCORE:
        return "Repeated high match"
    if first_seen and first_seen != now_date:
        return "Still open"
    return "Watchlist"


def next_action_for(job: Job, status: str) -> str:
    """Public, role-specific next step that avoids private CV/contact details."""
    text = f"{job.title} {' '.join(job.categories)} {' '.join(job.fit)}".lower()
    if status == "New" and job.score >= ALERT_SCORE:
        prefix = "Apply this refresh"
    elif job.score >= ALERT_SCORE:
        prefix = "Prioritize follow-up"
    elif job.priority in {"High", "Medium-high"}:
        prefix = "Shortlist"
    else:
        prefix = "Watch"

    if any(term in text for term in ["ai", "agent", "llm", "model"]):
        focus = "lead with AI/LLM trust-boundary testing, prompt-injection/RAG abuse cases, and concrete mitigation evidence"
    elif any(term in text for term in ["product", "application", "appsec", "secure sdlc", "code review"]):
        focus = "lead with AppSec/product-security stories: code review, exploitability triage, and engineering-ready fixes"
    elif any(term in text for term in ["penetration", "red team", "offensive"]):
        focus = "lead with offensive-security delivery, impact-based exploit chains, and remediation guidance"
    elif any(term in text for term in ["research", "vulnerability", "cve"]):
        focus = "lead with vulnerability research craft: root cause, reproducible evidence, variant analysis, and patch validation"
    elif any(term in text for term in ["manager", "lead", "architect", "principal", "staff"]):
        focus = "lead with senior ownership, roadmap tradeoffs, stakeholder influence, and durable security-program improvements"
    else:
        focus = "verify the role is hands-on technical security work, then tailor around practical risk judgement and fixes"

    return f"{prefix}: {focus}."

def job_key(job: Job) -> str:
    return normalized_history_key(job.title, job.company, job.url or f"{job.title}|{job.company}|{job.location}")


def dedupe(jobs: Iterable[Job]) -> list[Job]:
    best: dict[str, Job] = {}
    for job in jobs:
        key = job_key(job)
        existing = best.get(key)
        if existing is None or job.score > existing.score:
            best[key] = job
    return sorted(best.values(), key=lambda j: (-j.score, -j.cv_score, j.company.lower(), j.title.lower()))


def select_top_jobs(ranked: list[Job], limit: int = MAX_JOBS, per_company: int = 2) -> list[Job]:
    """Pick a useful public top list without letting one employer dominate it."""
    selected: list[Job] = []
    company_counts: dict[str, int] = {}
    deferred: list[Job] = []
    for job in ranked:
        key = clean_text(job.company).lower()
        if company_counts.get(key, 0) < per_company:
            selected.append(job)
            company_counts[key] = company_counts.get(key, 0) + 1
        else:
            deferred.append(job)
        if len(selected) >= limit:
            break
    if len(selected) < limit:
        selected.extend(deferred[: limit - len(selected)])
    return selected[:limit]


def load_history() -> dict[str, dict[str, object]]:
    if not HISTORY_OUT.exists():
        return {}
    try:
        data = json.loads(HISTORY_OUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    rows = data.get("jobs", {}) if isinstance(data, dict) else {}
    if not isinstance(rows, dict):
        return {}

    # Normalize old cache rows so the public history file does not keep raw URLs
    # or hex-like identifiers that can trip public phone-number privacy scans.
    migrated: dict[str, dict[str, object]] = {}
    for old_key, row in rows.items():
        if not isinstance(row, dict):
            continue
        title = clean_text(row.get("title"))
        company = clean_text(row.get("company"))
        if not title or not company:
            continue
        key = normalized_history_key(title, company, str(old_key))
        migrated[key] = {
            "title": title,
            "company": company,
            "source": clean_text(row.get("source")),
            "first_seen": clean_text(row.get("first_seen")),
            "last_seen": clean_text(row.get("last_seen")),
            "last_score": int(row.get("last_score") or 0),
        }
    return migrated


def apply_history(jobs: list[Job], history: dict[str, dict[str, object]], now_date: str) -> tuple[list[Job], dict[str, dict[str, object]], list[dict[str, str]]]:
    seen_now = set()
    enriched = []
    for job in jobs:
        key = job_key(job)
        seen_now.add(key)
        old = history.get(key, {})
        first_seen = str(old.get("first_seen") or now_date)
        previous = bool(old)
        # Keep roles discovered in the current weekly refresh labelled as New even
        # across repeated local/test runs before the commit is deployed.
        status = "Still open" if previous and first_seen != now_date else "New"
        alert = alert_for(job.score, job.title, job.company, list(job.fit), status)
        badge = status_badge_for(status, job.score, first_seen, now_date)
        next_action = next_action_for(job, status)
        enriched.append(replace(job, first_seen=first_seen, last_seen=now_date, status=status, status_badge=badge, next_action=next_action, alert_reason=alert))
        history[key] = {
            "title": job.title,
            "company": job.company,
            "source": job.source,
            "first_seen": first_seen,
            "last_seen": now_date,
            "last_score": job.score,
        }
    removed = []
    for key, row in list(history.items()):
        if key not in seen_now and row.get("last_seen") != now_date:
            removed.append({"title": str(row.get("title", "")), "company": str(row.get("company", "")), "last_seen": str(row.get("last_seen", ""))})
    return enriched, history, removed[:20]


def job_to_dict(job: Job) -> dict[str, object]:
    return {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "url": job.url,
        "source": job.source,
        "published_at": job.published_at,
        "summary": job.summary,
        "salary_estimate": job.salary_estimate,
        "tags": list(job.tags),
        "score": job.score,
        "cv_score": job.cv_score,
        "fit": list(job.fit),
        "priority": job.priority,
        "why_match": job.why_match,
        "possible_gap": job.possible_gap,
        "compensation_fit": job.compensation_fit,
        "categories": list(job.categories),
        "score_breakdown": job.score_breakdown,
        "seniority": job.seniority,
        "apply_angle": job.apply_angle,
        "skillsets_to_build": list(job.skillsets_to_build),
        "learning_gaps": list(job.learning_gaps),
        "certifications_to_consider": list(job.certifications_to_consider),
        "alert_reason": job.alert_reason,
        "next_action": job.next_action,
        "status_badge": job.status_badge,
        "first_seen": job.first_seen,
        "last_seen": job.last_seen,
        "status": job.status,
    }


def main() -> int:
    now_dt = datetime.now(timezone.utc).replace(microsecond=0)
    now = now_dt.isoformat().replace("+00:00", "Z")
    today = now_dt.date().isoformat()
    all_jobs: list[Job] = []
    health: list[dict[str, object]] = []

    for company, board in GREENHOUSE_BOARDS.items():
        jobs, row = source_result(f"Greenhouse/{company}", lambda c=company, b=board: from_greenhouse(c, b))
        all_jobs.extend(jobs); health.append(row); time.sleep(0.15)
    for company, slug in LEVER_COMPANIES.items():
        jobs, row = source_result(f"Lever/{company}", lambda c=company, s=slug: from_lever(c, s))
        all_jobs.extend(jobs); health.append(row); time.sleep(0.15)
    for company, board in ASHBY_BOARDS.items():
        jobs, row = source_result(f"Ashby/{company}", lambda c=company, b=board: from_ashby(c, b))
        all_jobs.extend(jobs); health.append(row); time.sleep(0.15)
    for query in SEARCH_QUERIES:
        jobs, row = source_result(f"Remotive/{query}", lambda q=query: from_remotive(q))
        all_jobs.extend(jobs); health.append(row); time.sleep(0.15)
    jobs, row = source_result("RemoteOK", from_remoteok)
    all_jobs.extend(jobs); health.append(row)
    for query in MYCAREERSFUTURE_QUERIES:
        jobs, row = source_result(f"MyCareersFuture/{query}", lambda q=query: from_mycareersfuture(q))
        all_jobs.extend(jobs); health.append(row); time.sleep(0.15)

    ranked = [job for job in dedupe(all_jobs) if job.score >= PUBLISH_SCORE]
    history = load_history()
    ranked, history, removed = apply_history(ranked, history, today)
    ranked = sorted(ranked, key=lambda j: (0 if j.status == "New" and j.score >= 78 else 1, -j.score, -j.cv_score, j.company.lower(), j.title.lower()))
    jobs = select_top_jobs(ranked, MAX_JOBS, per_company=2)
    alerts = [job for job in ranked if job.alert_reason and (job.score >= ALERT_SCORE or job.status == "New")][:6]

    status_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    for job in ranked:
        status_counts[job.status] = status_counts.get(job.status, 0) + 1
        source_counts[job.source] = source_counts.get(job.source, 0) + 1
        for category in job.categories:
            category_counts[category] = category_counts.get(category, 0) + 1

    data = {
        "updated_at": now,
        "location_filter": "Singapore / Remote-Singapore / APAC remote eligible",
        "salary_target": "S$11k+/month onwards target (S$132k+/year equivalent); clear listed ranges starting below target are filtered out.",
        "minimum_monthly_compensation_sgd": MIN_MONTHLY_COMPENSATION_SGD,
        "search_focus": "Singapore AI job search tailored to a senior cybersecurity manager / AI security engineer profile: AI-security, LLM/RAG/agent security, prompt/content injection, AI-assisted secure code review, offensive security, incident response support, Cyber Range, AppSec/product security, vulnerability research, cloud/DevSecOps, and adjacent security-engineering leadership roles.",
        "search_behavior": "Query public ATS and job-board feeds, allow Singapore/Remote-Singapore/APAC-eligible metadata, score all candidates before truncating to the top 10, require an estimated or listed S$11k+/month compensation path, label new/still-open roles, and penalize sales, junior-only, compliance-heavy, SOC-only, or non-technical noise.",
        "minimum_score": PUBLISH_SCORE,
        "sources": ["Greenhouse public boards", "Lever public postings", "Ashby public boards", "Remotive", "RemoteOK", "MyCareersFuture"],
        "source_note": "Weekly top-10 public ATS/feed scan for Singapore and Singapore-eligible remote AI/security roles. Ranking is weighted against broad CV-fit signals from the uploaded CV without publishing private details: cybersecurity management, offensive security leadership, incident response support, VAPT/adversary emulation, AI security engineering, RAG/agent/MCP trust boundaries, prompt/content injection testing, vulnerability research/CVEs, Cyber Range delivery, Azure/LLM tooling, and cloud/application/product security. Links go to original job posts; verify current availability and compensation before applying.",
        "stats": {
            "candidates_scored": len(ranked),
            "published_count": len(jobs),
            "alert_count": len(alerts),
            "removed_since_last_refresh": len(removed),
            "status_counts": status_counts,
            "source_counts": source_counts,
            "category_counts": category_counts,
        },
        "source_health": health,
        "alerts": [job_to_dict(job) for job in alerts],
        "removed_recently": removed,
        "jobs": [job_to_dict(job) for job in jobs],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HISTORY_OUT.write_text(json.dumps({"updated_at": now, "jobs": history}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(jobs)} top matches from {len(ranked)} scored candidates to {OUT}")
    print(f"alerts={len(alerts)} sources_ok={sum(1 for row in health if row.get('status') == 'ok')} removed={len(removed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
