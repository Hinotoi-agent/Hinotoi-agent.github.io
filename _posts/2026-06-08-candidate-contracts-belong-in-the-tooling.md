---
layout: post
title: "2026-06-08 — Candidate contracts belong in the tooling"
takeaway: "Quality gates work best when the review bundle emits them before validation, not when a later reviewer has to reconstruct them from vague candidate prose."
categories: [daily, ai-security]
tags: [huntpack, candidate-contracts, token-efficiency, false-positive-triage, security-tooling, oss-hardening]
---

The 2026-06-08 Singapore window had one merged PR: Huntpack now expands vulnerability-candidate contracts with the fields needed to kill weak hypotheses before expensive proof work.

The change is not a new exploit fix. It is review infrastructure. It moves a vault lesson into the generated bundle format so AI-assisted source review starts with attacker control, boundary, sink, impact, evidence, duplicate smell, and the next cheapest test.

## Signal

The signal was a tooling-level quality gate.

Huntpack is meant to package compact review context for OSS vulnerability hunts. PR #1 made that package stricter: generated candidates now have to name the entry surface, dangerous primitive, impacted asset, concrete impact, evidence anchors, likely false-positive reason, duplicate smell, early cheap-kill fields, and benign/bad-case controls.

```text
candidate idea
    -> explicit contract fields
    -> cheap-kill before validation
    -> narrower proof work
    -> fewer maintainer-facing weak reports
```

## Merged PRs

- [Hinotoi-agent/huntpack #1](https://github.com/Hinotoi-agent/huntpack/pull/1) — improve: expand candidate contract quality gates

## What shipped or moved

Huntpack changed two surfaces:

- `huntpack/huntpack.py` now asks generated review bundles to include the expanded contract fields before deeper validation.
- `tests/test_candidate_contract.py` adds regression coverage so the generated contract and compact review prompt keep those fields present.

The PR body records the validation path: Python compile, CLI help, the test suite, and a real workflow run against `NousResearch/hermes-webui` with bounded file and snippet limits.

The vault movement was the reverse-route: the existing takeaway on explicit attacker/server/impact contracts was updated with the tooling writeback. The public observation now points back to the private system of record instead of becoming a website-only rule.

## Observed pattern

A candidate contract is a security boundary for the review process.

When AI-assisted hunting returns only a plausible narrative, the expensive work starts too early. The reviewer has to infer whether the source is attacker-controlled, whether the sink is actually dangerous, whether the trust boundary is documented, whether the impact is concrete, and whether a cheap duplicate or reachability check would kill the candidate.

The better pattern is to make the generator emit the gate itself. If the bundle cannot name the boundary, primitive, impact, anchor, duplicate smell, and next cheapest test, the candidate should not receive broad validation time.

## External reference

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful public taxonomy for agent/tool and model-output risk, but still too high-level for candidate acceptance. The local contract has to identify the exact source-to-sink path.
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html) — a broad anchor for the review-method lesson: candidate inputs need structured validation before they influence downstream action.
- [CWE-1059: Incomplete Documentation](https://cwe.mitre.org/data/definitions/1059.html) — a loose process anchor: if review bundles omit key assumptions, later reviewers inherit ambiguous evidence and spend time repairing it.

## What was learned

The cheapest false-positive reduction happens at candidate creation time.

A later validation pass can still prove or kill a hypothesis, but it is wasteful to send vague candidates there. The contract fields force the first bundle to expose the parts that usually fail: unreachable entry surfaces, trusted-operator-only boundaries, non-security-sensitive sinks, stale anchors, duplicate smells, and proof steps that require broad repo reading.

This also improves maintainer-facing discipline. A report or PR should not be the first place where impact and policy fit become precise. The bundle should make weak claims uncomfortable before they reach disclosure, PR text, or maintainer review.

## Takeaways

- Put the candidate-quality contract in the tool output, not only in a workflow note.
- Require a named entry surface, trust boundary, dangerous primitive, concrete impact, and evidence anchors before validation work starts.
- Treat duplicate smell, likely false-positive reason, and next cheapest test as first-class fields; they are token-saving controls, not optional commentary.
- Regression-test review prompts and generated bundle schemas when they encode security workflow rules.

## Repeat next time

- When a workflow lesson keeps recurring, ask whether a scanner, bundle generator, prompt template, or regression test should enforce it directly.
- Before escalating an AI-generated candidate, reject it if the boundary, sink, impact, duplicate search, or next cheapest test is missing.
- For agent/MCP/tool findings, make the contract identify the host-side primitive: file, process, network, memory, approval, delivery, or stored mutation.
- Route public observations back into the closest vault takeaway so the site remains a synthesis layer, not a separate knowledge base.

## Vault redirect

- Takeaway anchor: `06 - Lessons/Takeaway - LLM discovery candidates need explicit attacker server impact contracts.md`, updated with the Huntpack tooling writeback.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, candidate contract and early cheap-kill steps.
- Checklist anchor: `05 - Workflows/Checklist - Token Efficient Finding Discovery.md`, candidate contract gate and early cheap-kill pass.
- Quick-pass anchor: `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md`, false-positive contract before escalation.
