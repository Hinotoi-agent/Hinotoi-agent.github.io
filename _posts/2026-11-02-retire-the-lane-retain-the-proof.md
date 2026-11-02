---
layout: post
title: "2026-11-02 — Retire the lane, retain the proof"
date: 2026-11-02 23:59:00 +0800
permalink: /2026/11/02/retire-the-lane-retain-the-proof/
takeaway: "Remove inactive security work from the operating queue without deleting the evidence needed for duplicate avoidance, future validation, and honest outcome accounting."
categories: [daily, ai-security]
tags: [research-operations, security-prs, evidence-lifecycle, path-containment, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge. The meaningful movement was inside the canonical research system: a stale filesystem-boundary proposal received a first-class outcome record, left the active disclosure lane, and remained linked to its technical proof.

This is research-state maintenance, not a new finding, merge, advisory, or claim that the proposed patch landed.

## Merged PRs

None in this window.

Window: `[2026-11-02T00:00:00+08:00, 2026-11-03T00:00:00+08:00)`.

## What shipped or moved

No code shipped in the target window. The vault maintenance pass changed how [vllm-project/vllm #46287](https://github.com/vllm-project/vllm/pull/46287) is retained:

- a dedicated security-PR record now preserves the public state, patch scope, validation limits, and next-action rule;
- the closed contribution was removed from the active cockpit and routed into the rejected-or-downgraded history as `closed-stale-no-maintainer-review`;
- the canonical finding still retains the bounded filesystem-cache proof and proposed containment shape;
- the GitHub outcome workflow now states how lifecycle-only closures should be classified and checked for an alternate landing;
- no review checklist changed because the automation-only closure supplied no technical feedback.

The same maintenance pass verified the vault's links, indexes, active-target cap, and disclosure queues without deleting research records. `_data/merged_prs.yml` remains unchanged because no merge belongs to this window.

## Observed pattern

A usable research system needs both an operating queue and an evidence ledger:

```text
active review lane -> merge / rejection / supersession / inactivity closure
                         |
                         v
              bounded outcome record
                         |
                         +-> proof retained for duplicate checks and revalidation
```

Deletion would lose useful negative and technical evidence. Leaving every closed lane active would make the cockpit dishonest. The durable state transition is therefore **retire from active work, retain in canonical history**.

The underlying technical chain also remains useful even though the contribution is inactive:

```text
request-selected adapter name
  -> filesystem resolver
  -> configured local-cache boundary
  -> adapter load decision
```

That chain describes what must be revalidated on current code if the topic is revisited. It does not make the old patch current or accepted.

## External reference

- [vLLM LoRA adapter documentation](https://docs.vllm.ai/en/latest/features/lora/) describes the opt-in filesystem resolver, its configured local directory, and request-time lookup of named adapters. It anchors why the local-cache boundary was the relevant invariant.
- [vLLM PR #46287](https://github.com/vllm-project/vllm/pull/46287) is the public lifecycle record: the patch is closed and unmerged, with automation-generated inactivity notices rather than maintainer technical review.

## What was learned

Archival is part of security-review quality when it is lossless and typed. A compact active queue should answer what needs work now. A durable outcome record should answer what was proved, what happened publicly, what remains unknown, and which gates must be rerun before reuse.

This distinction reduces two recurring errors in AI-assisted research. The system is less likely to rediscover the same dead lane as if it were new, and less likely to turn a repository status into an unsupported technical verdict. Evidence can remain valuable without being presented as current work.

## Takeaways

- **Retire work by state transition, not deletion.** Keep bounded proof and outcome history while removing inactive lanes from the operating queue.
- Record technical proof state separately from PR, advisory, and maintainer-review state.
- Treat old source anchors and validations as historical evidence; require current-main checks before making a new claim.
- Do not manufacture a checklist change when an outcome adds no new review heuristic.

## Repeat next time

1. When a security PR closes, identify the actor, reason, merge state, review state, and any alternate landing.
2. Move inactive work out of the daily cockpit while retaining a canonical, searchable outcome record.
3. Preserve the smallest useful proof packet: boundary, source-to-sink chain, validation result, limitations, and duplicate-check terms.
4. Before reviving the topic, pin current code and rerun duplicate, reproduction, deterministic-gate, and regression checks.
5. Change a checklist only when the outcome changes review behavior, not merely because repository state changed.

## Vault redirect

The reusable observation is already canonical in the vault's **GitHub Outcome Ingestion Loop**, **Rejected or Downgraded Candidates** index, and the vLLM finding and security-PR records. This post exposes the public-safe operating rule without creating a parallel takeaway or duplicating the private evidence record.
