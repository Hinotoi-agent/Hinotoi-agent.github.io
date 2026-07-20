#!/usr/bin/env python3
"""Focused regression checks for AI job classification and scoring."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("update_ai_jobs.py")
SPEC = importlib.util.spec_from_file_location("update_ai_jobs", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def main() -> int:
    applied_title = "Senior Cybersecurity Data Scientist"
    applied_summary = (
        "Build machine-learning systems for threat detection, security analytics, "
        "automated incident triage, and remediation across cloud environments."
    )
    assert MODULE.uses_ai_for_cybersecurity(applied_title, applied_summary)
    _, _, _, fit, _, _, _, categories, breakdown, *_ = MODULE.score_job(
        applied_title, "Example Bank", "Singapore", applied_summary, "2026-07-20"
    )
    assert "AI-enabled Cybersecurity" in fit
    assert "Best AI-enabled cybersecurity role" in categories
    assert breakdown["ai_security"] >= 50

    secure_ai_title = "AI Agent Security Research Engineer"
    secure_ai_summary = "Assess prompt injection and tool-use boundaries in LLM agents."
    assert not MODULE.uses_ai_for_cybersecurity(secure_ai_title, secure_ai_summary)
    _, _, _, _, _, _, _, secure_ai_categories, _, *_ = MODULE.score_job(
        secure_ai_title, "Example AI Lab", "Singapore", secure_ai_summary, "2026-07-20"
    )
    assert "Best AI-security role" in secure_ai_categories

    unrelated_title = "Machine Learning Engineer"
    unrelated_summary = "Build recommendation models for consumer shopping experiences."
    assert not MODULE.uses_ai_for_cybersecurity(unrelated_title, unrelated_summary)

    non_ai_security_title = "Security Analytics Engineer"
    non_ai_security_summary = "Build dashboards and rule-based threat-detection reports."
    assert not MODULE.uses_ai_for_cybersecurity(non_ai_security_title, non_ai_security_summary)
    print("test_ai_jobs_logic: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
