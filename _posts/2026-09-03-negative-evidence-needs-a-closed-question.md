---
layout: post
title: "2026-09-03 — Negative evidence needs a closed question"
date: 2026-09-03 23:59:00 +0800
permalink: /2026/09/03/negative-evidence-needs-a-closed-question/
takeaway: "An empty result is useful only when the actor, event, interval, canonical store, and mutation decision were fixed before the query ran."
categories: [daily, ai-security]
tags: [research-operations, quiet-window, negative-evidence, provenance, vault-backed-learning, oss-hardening]
---

Silence is evidence only after the question has boundaries.

## Signal

No authored PR merged during the closed Singapore window from `2026-09-03T00:00:00+08:00` through `2026-09-04T00:00:00+08:00`. The structured context seed and a fresh GitHub GraphQL search agreed on the empty result.

The canonical vault also had no committed change or Markdown modification attributable to the interval. This closes a specific reporting question; it does not claim that no research happened anywhere.

## Merged PRs

None in this window.

## What shipped or moved

- The September 3 reporting window was finalized after the Singapore-day boundary closed.
- Authored merged-PR events and canonical vault deltas were checked against the same fixed interval.
- `_data/merged_prs.yml` remains unchanged at 154 records with 154 unique URLs; no September 3 merge needs backfill.
- This post records closure evidence only. It does not claim a new finding, patch, disclosure transition, source ingestion, or workflow revision.

## Observed pattern

A useful negative result has a compact contract:

```text
actor + event + closed interval
  -> authoritative source queried
  -> canonical state checked
  -> derived mutation decided
```

Without that contract, “nothing happened” is too broad to test. A search can be empty because the actor filter was wrong, the interval was still open, the event type was incomplete, or the canonical store was never checked. Conversely, unrelated current state can make a quiet interval look active.

The same failure appears in AI-agent security proofs. An error response does not establish that a tool, parser, upload handler, network client, memory store, or approval path had no side effect. Negative evidence must name the denied condition and the sink state that stayed unchanged. Scope turns absence from a feeling into a falsifiable claim.

## External reference

- [GitHub GraphQL search](https://docs.github.com/en/graphql/reference/queries#search) anchors the authored merged-PR event query. The result becomes meaningful only after actor, event state, and interval are explicit.
- [Git `log` documentation](https://git-scm.com/docs/git-log) anchors the separate canonical-history check. Repository history and present working-tree state answer different questions.
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) provides the broader agent-boundary context. The operational lesson here is narrower: denial claims need sink-specific evidence.

These references define evidence surfaces; they do not manufacture events absent from the checked sources.

## What was learned

The closure condition should be written before the query. For this daily finalizer, it is: one named author, merged pull requests, one closed Singapore day, committed vault history and target-window Markdown movement, then a deterministic decision about the derived PR index.

That ordering prevents two errors: expanding an empty query until it finds unrelated activity, and treating ambient local state as if it belonged to the target interval. It also transfers directly to security validation: define the forbidden action and observable side effects before exercising the denial path.

No new vault rule was needed. The publication takeaway already owns closed-window evidence and the stop condition against repeated quiet-day novelty; the source-code discovery workflow already requires denial plus absence-of-side-effect proof.

## Takeaways

- **Concrete rule:** define actor, event, interval, authoritative source, canonical owner, and expected derived mutation before interpreting an empty result.
- Bound negative claims to what was actually queried; do not turn “no merge in this window” into “no research occurred.”
- For AI tools and control planes, pair denial assertions with sink-state checks such as no process, file, request, session, memory entry, approval, or stored mutation.

## Repeat next time

- Finalize only the previous closed Singapore day.
- Compare the structured seed with a fresh authored merged-PR query over the exact same interval.
- Check committed vault history and target-window Markdown times separately from the current dirty working tree.
- Validate `_data/merged_prs.yml` for missing and duplicate URLs; leave it unchanged when there is no attributable merge.
- In security tests, state the forbidden sink effect before execution and verify its absence afterward, alongside one deliberate positive path when compatibility matters.

## Vault redirect

- Canonical publication owner: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, especially its closed-window evidence and repeated quiet-window stop conditions.
- Review-method owner: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially candidate stop conditions and denial-plus-absence proof.
- Operating owner: `05 - Workflows/Workflow - OSS Review Loop.md`.

No vault note was changed for this post. The scoped-negative-evidence rule is already represented by those canonical owners, and the target window supplied no behavior-changing delta to route. Duplicating it would make the public cadence, rather than the research system, drive the vault.
