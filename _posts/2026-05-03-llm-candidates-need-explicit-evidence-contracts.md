---
layout: post
title: "2026-05-03 — LLM candidates need explicit evidence contracts"
takeaway: "AI-assisted vulnerability discovery needs a structured attacker/server/impact/policy/proof contract before a candidate deserves escalation."
categories: [daily, ai-security]
tags: [ai-for-security, llm-agents, false-positive-triage, authz, oss-hardening]
---

No PRs merged in the 2026-05-03 Singapore window. The useful movement was in the research system: a source-ingestion pass turned an external LLM-assisted vulnerability-discovery writeup into a tighter false-positive gate for the vault, especially for authz and business-logic candidates.

## Signal

The signal was not a shipped patch. It was a review-quality boundary. Broad AI agents can generate many plausible vulnerability candidates, but the candidate only becomes useful when it states the attacker condition, server condition, concrete impact, security-policy fit, and proof status in a form that a skeptical reviewer can reject or reproduce.

## Merged PRs

None in this window.

## What shipped or moved

The vault ingested Hyunseo Shin's CyKor writeup on using an LLM multi-agent workflow to find open-source 0-days. The raw source note, advisory-case synthesis, and takeaway note were added to the research system, then folded back into existing workflows instead of creating a parallel checklist.

The source-code discovery workflow now treats candidate quality as an explicit contract: attacker control, server/environment prerequisite, security impact, project policy fit, and proof status must be written down before escalation. The quick-pass checklist gained the same false-positive gate. The authz checklist gained a sharper object-scope question: does the permission engine evaluate the exact target resource, tenant, workspace, or UID, or only a generic role/action?

## Observed pattern

The reusable pattern is a funnel, not a monolithic agent. Cheap discovery can stay broad and noisy. Semi-triage should kill candidates that cannot name the attacker, environment, impact, policy fit, or proof. Final verification should spend expensive model and human attention only on candidates that survived that contract.

For authorization review, the key invariant is scope binding. A check that proves "the actor has this action" is not enough when the dangerous operation affects a specific object. The review question has to follow the target identifier into the permission engine and confirm that the exact object or tenant scope is part of the decision.

## External reference

- [How I Found Open-Source 0-days with an LLM Multi-Agent Workflow](https://blog.cykor.kr/2026/02/How-I-Found-Open-Source-0-days-with-an-LLM-Multi-Agent-Workflow) — useful because it describes a tiered AI workflow where false positives dropped after attacker condition, server condition, and concrete impact became required output fields.
- [GitHub Security Advisories](https://github.com/advisories) — useful as a public anchor for why mature vulnerability records separate affected conditions, impact, proof, and remediation instead of relying on broad danger language.

## What was learned

The important part of LLM-assisted review is not that a model can point at suspicious code. It is whether the workflow makes the model produce a claim that can be tested. A candidate without attacker control, a reachable sink, a realistic server condition, and a concrete impact is only review noise. The false-positive gate should be structural, not a reminder buried in the prompt.

This also changes how authz candidates should be triaged. Generic permission checks are not inherently wrong, but they are incomplete evidence when the operation mutates or reveals a specific resource. The reviewer needs to compare route intent, action permission, object identifier, service-layer enforcement, storage namespace, and documented security model before claiming IDOR or privilege escalation.

## Takeaways

- Treat LLM-generated vulnerability candidates as incomplete until they carry attacker condition, server condition, concrete impact, policy fit, and proof status.
- Use cheaper or broader agents for candidate generation, but reserve escalation for candidates that pass a structured false-positive contract.
- For authz and business-logic review, ask whether the exact target object or tenant scope reaches the permission decision; generic action checks are not enough evidence by themselves.
- Consult `SECURITY.md`, advisory scope, and trust-model language before severity claims, especially when a behavior may be trusted-operator, admin-only, or intentionally out of scope.

## Repeat next time

- Before spending PR or disclosure time on an AI-discovered candidate, write the five fields first: attacker, server/environment, impact, policy fit, proof status.
- For each authz candidate, trace the target resource ID from route input through service checks into the permission engine and storage operation.
- Kill candidates early when they cannot show real attacker control, reachable sink, project-policy fit, or reproducible proof.
- Fold workflow improvements into the smallest existing checklist or takeaway note instead of creating duplicate one-off process notes.

## Vault redirect

- Source: `07 - Sources/Blog Posts/Source - CyKor - LLM multi-agent workflow for open-source 0-days.md`.
- Case: `08 - Advisory Cases/Case - Tiered LLM multi-agent workflow for open-source 0-days.md`.
- Lesson: `06 - Lessons/Takeaway - LLM discovery candidates need explicit attacker server impact contracts.md`.
- Workflow/checklist: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md`, and `05 - Workflows/Checklist - Authz Coverage Review.md` now carry the reusable false-positive and object-scope gates.
