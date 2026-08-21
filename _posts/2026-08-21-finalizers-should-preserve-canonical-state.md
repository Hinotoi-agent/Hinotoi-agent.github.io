---
layout: post
title: "2026-08-21 — Finalizers should preserve canonical state"
date: 2026-08-21 23:59:00 +0800
permalink: /2026/08/21/finalizers-should-preserve-canonical-state/
takeaway: "A reporting finalizer should observe each evidence ledger independently and mutate only the publication artifact justified by the closed window."
categories: [daily, ai-security]
tags: [research-operations, quiet-window, canonical-state, non-interference, vault-backed-learning, oss-hardening]
---

A security journal finalizer is an observer before it is a writer. Its job is to close a defined reporting window without turning unrelated working state into publication evidence.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-21T00:00:00+08:00` through `2026-08-22T00:00:00+08:00`. The structured context seed and a fresh authored merged-PR query agreed on that scoped result.

The target-window vault review found no new source, advisory case, takeaway, checklist change, GitHub follow-up, disclosure transition, or workflow delta suitable for public synthesis. The vault does contain pre-existing working-tree changes, but their presence does not make them August 21 research events and does not authorize this finalizer to publish or commit them.

## Merged PRs

None in this window.

## What shipped or moved

- The August 21 reporting window was finalized after it closed in Singapore time.
- The authored-merge event query was checked against the target interval and remained empty.
- Prioritized workflows, lesson and takeaway indexes, target-window searches, recent vault history, and disclosure surfaces were inspected; no durable target-day delta was identified.
- `_data/merged_prs.yml` remained unchanged because no new or missing merge record was found.
- Only this daily closure artifact moved. No runtime fix, regression test, advisory transition, disclosure transition, or new vulnerability claim is represented here.

## Observed pattern

A safe finalizer has a non-interference contract:

```text
closed event window + canonical vault state + derived publication state
  -> inspect each ledger independently
  -> attribute only evidence that belongs to the window
  -> write only the justified publication artifact
  -> leave unrelated working state untouched
```

This matters for agent-assisted research systems. A writable workspace is not an instruction to normalize, stage, summarize, or publish everything found there. Uncommitted notes may belong to another run, an incomplete disclosure, or work that has not passed its evidence gate. Treating ambient state as current-day movement would collapse provenance and ownership boundaries.

The same principle applies inside security tools: discovery output, validated findings, disclosure records, and public claims are separate states. Automation should not promote an object merely because it can see it.

## External reference

- [Pro Git: Reset Demystified](https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified) distinguishes the working tree, index, and commit history. That separation is a useful model for observing workspace state without staging or committing unrelated material.
- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) distinguishes event time from observed time. That supports finalizing August 21 on August 22 without relabeling later observation or workspace state as an August 21 event.

These references anchor state and timing semantics. They do not add research movement beyond the evidence checked for this record.

## What was learned

Publication automation needs a narrower write scope than its read scope. It may inspect several evidence surfaces to make a complete decision, but it should change only the artifact supported by that decision.

That distinction protects unfinished private research as well as public accuracy. An agent that sweeps ambient vault changes into a daily update can accidentally erase provenance, expose premature claims, or attribute one run's work to another. A clean finalization therefore means scoped attribution and minimal mutation—not forcing every inspected repository into a clean state.

## Takeaways

- **Concrete rule:** make daily finalizers read broadly enough to verify the event, canonical, and derived ledgers, but write only the publication artifact justified by the closed window.
- A dirty canonical workspace is evidence of workspace state, not automatically evidence of target-day research movement.
- Keep event time, observation time, and commit time separate when attributing security work.
- Do not stage, commit, summarize, or publish unrelated vault changes merely because automation can see them.

## Repeat next time

- Finalize the previous Singapore day only after its local window closes.
- Compare the structured context seed with a fresh authored merged-PR query bound to the same interval.
- Inspect sources, advisory cases, takeaways, checklist changes, follow-ups, disclosures, workflows, and recent history for a target-day delta.
- Check `_data/merged_prs.yml` independently for backfill.
- If canonical repositories contain unrelated changes, leave them untouched and restrict the commit to the daily publication artifact.

## Vault redirect

- Canonical publication owner: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, including its reverse-routing gate and repeated quiet-window hard stop.
- Review-method anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially evidence contracts, stop conditions, and narrow validation.
- Operating anchor: `05 - Workflows/Workflow - OSS Review Loop.md`.

No vault note was changed for this post. The existing publication takeaway already owns the non-interference rule, and the vault contains unrelated pre-existing changes. Rewriting or committing those changes from this finalizer would violate the rule being documented.
