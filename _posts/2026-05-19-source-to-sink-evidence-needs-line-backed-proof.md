---
layout: post
title: "2026-05-19 — Source-to-sink evidence needs line-backed proof"
takeaway: "A vulnerability claim is not ready until the attacker-controlled source, the dangerous sink, and the traversable chain between them are backed by concrete evidence."
categories: [daily, ai-security]
tags: [verifymate, evidence, source-to-sink, false-positive-triage, maintainer-readiness]
---

The 2026-05-19 Singapore window had one merged PR. It tightened Verifymate's pre-submission gate so a finding report has to show a real source-to-sink chain, not only name a dangerous sink or an attacker-controlled input in isolation.

## Signal

The useful signal was evidence quality.

AI-assisted vulnerability discovery can find plausible flows quickly, but plausible is not the same as reportable. The merged Verifymate change turns one recurring review question into a deterministic gate: does the report connect attacker control to the sink with flow language and line-backed evidence for both ends?

That matters for agent, MCP, tool, upload, parser, SSRF, and workspace bugs because the security boundary is usually in the path between input and action. A report that proves only the input or only the sink still leaves the maintainer to guess whether the dangerous path is actually traversable.

## Merged PRs

- [Hinotoi-agent/Verifymate #7](https://github.com/Hinotoi-agent/Verifymate/pull/7) — Add source-to-sink evidence chain checks

## What shipped or moved

Verifymate gained a blocking `source_to_sink_chain` vetting check. The check requires the report to describe the flow from source to sink and to include line-backed evidence for both the source and the sink.

The implementation also extracts report-mentioned source and sink terms into the recorded evidence locations, so the review artifact can show what the report claimed and where the code backs it. Regression coverage now includes both a passing line-backed source-to-sink chain and a failing unbacked source claim.

This is not a runtime product fix. It is a review-system hardening change: weaker findings should fail locally before they become maintainer work, CVE draft material, or public claims.

## Observed pattern

A real finding needs a traversable chain, not two disconnected facts.

```text
attacker-controlled source
    -> parser / router / resolver / loader / tool registry
        -> policy or transformation layer
            -> dangerous sink
                -> concrete security impact
```

The failure mode is easy to miss during AI-assisted review: a model can correctly identify an input and correctly identify a dangerous API, but skip the proof that the same execution path connects them under realistic conditions. Source-to-sink gating makes that missing middle visible.

## External reference

- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html) — useful when the source is accepted without the validation needed before it reaches a sensitive operation.
- [CWE-693: Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html) — useful for cases where a protection exists but does not cover the actual flow to the sink.
- [CodeQL documentation: About data flow analysis](https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/) — a good public anchor for thinking in sources, sinks, and paths without copying any project-specific exploit detail.

## What was learned

The review loop should make the missing-middle problem cheap to catch.

For AI-security work, the expensive mistake is not just a false positive. It is a half-true report: attacker control exists somewhere, the sink exists somewhere else, and the writeup quietly assumes the path between them. Those reports can sound credible while still failing maintainer review because the core chain is unproven.

The better pattern is to require three pieces before escalation: source evidence, sink evidence, and path evidence. If any one is missing, the next step should be narrow verification rather than broader writing. The LLM prompt should ask only for the missing chain segment, sibling route, or proof gap instead of re-reviewing the whole repository.

## Takeaways

- Treat `source -> transformation -> sink -> impact` as a mandatory evidence shape for serious findings.
- A sink name without attacker-controlled reachability is not enough; an attacker-controlled input without a concrete sink is not enough either.
- Deterministic local gates like Verifymate should fail incomplete chains before maintainer-facing PRs or disclosure drafts are written.
- Regression tests for review tooling should include both the valid evidence shape and the tempting incomplete claim.

## Repeat next time

- Before writing a PR or advisory draft, mark the exact source line, sink line, and path segment that connects them.
- If the chain is missing, ask only for targeted proof: reachability, transformation behavior, sibling route coverage, or a minimal harness.
- For agent/tool/MCP/parser/upload findings, include at least one test or static proof that follows the same route as the claimed exploit path.
- Keep source-to-sink wording public-safe: describe the evidence shape and boundary class without publishing unnecessary exploit specifics.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchor: `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md`; the source-to-sink proof rule belongs in the existing quick pass, not a new checklist.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`; this public synthesis is reverse-routed as an evidence-chain variant.
- PR anchor: `Hinotoi-agent/Verifymate#7`, merged 2026-05-19 Singapore time.
