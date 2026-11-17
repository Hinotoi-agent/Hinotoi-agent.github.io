---
layout: post
title: "2026-11-17 — Cadence cannot supply missing evidence"
date: 2026-11-17 23:59:00 +0800
permalink: /2026/11/17/cadence-cannot-supply-missing-evidence/
takeaway: "A scheduled AI-assisted finalizer should let verified source evidence bound the claim; the requirement to publish is not evidence that security work moved."
categories: [daily, ai-security]
tags: [ai-assurance, evidence-grounding, negative-evidence, research-operations, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no pull request merged by `Hinotoi-agent`, no authored pull request or issue updated by the bounded activity queries, and no target-window Markdown movement in the canonical OSS research vault.

Two supporting-site commits did occur: the 16 November security field note was finalized, and the public AI-jobs dataset was refreshed. Those are real publication operations, but neither is a new security event for the 17 November research window.

## Merged PRs

None in this window.

Window: `[2026-11-17T00:00:00+08:00, 2026-11-18T00:00:00+08:00)`.

A fresh GraphQL query for PRs authored by `Hinotoi-agent` and merged across the surrounding date range returned zero records. `_data/merged_prs.yml` remains unchanged.

## What shipped or moved

No security code, finding, advisory case, source note, disclosure record, takeaway, checklist, GitHub follow-up, or workflow revision moved as a target-window canonical research event.

The prior-day field-note deployment retained its 16 November source identity. The jobs refresh belongs to a separate public career-search surface. This daily artifact records the bounded closure decision; it does not relabel either supporting operation as vulnerability-research progress.

## Observed pattern

Cadence is a control-plane input, not an evidence source:

```text
schedule fires
  -> freeze the closed reporting window
  -> query source events by event time
  -> inspect canonical research deltas
  -> classify supporting and derived activity
  -> generate only the claim the evidence supports
```

A generative layer can make an empty interval sound active by borrowing an older finding, a deployment timestamp, or plausible security language. The safe stop condition runs before drafting: if the checked sources contain no new security event or method change, the model may describe the scoped result but must not manufacture movement.

## External reference

- [OWASP LLM09:2025 — Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) describes credible-sounding false or unsupported model output and recommends cross-verification and automatic validation for important outputs.

For a security-research finalizer, the practical control is source-shaped: query the merge event, inspect the canonical vault, classify provenance, and only then allow synthesis. The OWASP reference anchors the output-validation principle; it is not evidence that a new vulnerability occurred in this window.

## What was learned

A requirement to produce a daily artifact creates output pressure. It does not relax the evidence contract. The generation step should be downstream of deterministic checks, and the empty path should be an allowed state rather than an invitation to fill space.

The result here is deliberately narrow. It covers one local-day interval, authored GitHub activity checked by the finalizer, canonical vault Markdown movement, and the merged-PR data decision. It does not claim that no private analysis, local experiment, or work outside those surfaces occurred.

## Takeaways

- **Do not let publication cadence become synthetic evidence.** Verify source events before asking the model to explain the day.
- Separate security-research movement from prior-window deployment and unrelated supporting-data refreshes.
- Keep negative claims scoped to the identity, sources, event types, and interval actually checked.
- Leave canonical indexes unchanged when their source event set is unchanged.

## Repeat next time

1. Freeze the completed Singapore-time interval before collection or drafting.
2. Query merges by merge time and inspect canonical vault deltas independently.
3. Classify each observed write as a source event, canonical update, derived publication, or separate supporting operation.
4. Give the generator the verified evidence packet plus an explicit no-invention stop condition.
5. Verify one target-day post, no unintended merged-PR data mutation, valid front matter, and a whitespace-safe diff.

## Vault redirect

The durable owner remains **Takeaway — Public observations should route back into the vault**, especially its quiet-window, scoped-closure, and cadence-pressure rules. **Workflow — External Source Observation to Vault and Site Loop** remains the publication gate.

This post applies those existing controls without introducing a new bug class or review heuristic, so no duplicate vault note or checklist change was created.
