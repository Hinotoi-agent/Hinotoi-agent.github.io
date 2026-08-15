---
layout: post
title: "2026-08-15 — Record time is provenance, not a second event"
date: 2026-08-15 23:59:00 +0800
permalink: /2026/08/15/record-time-is-provenance-not-a-second-event/
takeaway: "When a vault writeback records an earlier security event, preserve the write time as provenance but do not count the same merge, fix, or lesson again."
categories: [daily, ai-security]
tags: [research-operations, event-time, record-time, outcome-ingestion, idempotence, vault-backed-learning, oss-hardening]
---

A canonical record can move after the event it describes. That write is useful provenance, but it must not turn one security fix into a second shipped event.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-15T00:00:00+08:00` through `2026-08-16T00:00:00+08:00`. A fresh GitHub query confirmed the empty result.

The only target-window vault movement was the early-morning commit that canonicalized the prior day's [`microsoft/RAMPART #106`](https://github.com/microsoft/RAMPART/pull/106) outcome. That merge belongs to August 14 by source-event time and was already published and indexed there.

## Merged PRs

None in this window.

## What shipped or moved

- `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART payload artifact path containment.md` became the canonical outcome record for the August 14 merge.
- The record preserves the merge commit, exact artifact-load scope, regression evidence, and the still-open sibling collection-name lane.
- The August 14 daily post already synthesized that event and `_data/merged_prs.yml` already indexes it under its actual Singapore merge date.
- No new source, advisory case, checklist, workflow, finding, or disclosure event was attributed to August 15.
- `_data/merged_prs.yml` remained unchanged because there was no new merge to add.

This is evidence maintenance, not a second runtime fix, a second finding, or a new path-containment claim.

## Observed pattern

A security event can produce several records without becoming several events:

```text
source event: merge at T0
  -> public daily record keyed to T0
  -> merged-PR index keyed to T0
  -> canonical vault outcome written at T1
  -> later automation observes the T1 write
  -> deduplicate by source identity + event time
```

The vault write time answers when the research system absorbed the evidence. The GitHub merge time answers when the upstream change occurred. Both timestamps matter, but they serve different purposes.

Without that distinction, automation can double-count a fix whenever a disclosure note, takeaway, checklist, or public post is updated later. The resulting feed looks active while its chronology and metrics become unreliable. The safe design keeps the source event as the identity-bearing fact and treats derived writes as provenance unless they introduce a separate, bounded workflow change.

## External reference

- The [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) distinguishes an event's occurrence time from the time it was observed. That is the same separation needed between a GitHub merge and a later vault writeback.
- [NIST SP 800-218, Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) anchors the value of retaining security evidence and feeding lessons back into development practice.
- [GitHub's GraphQL `PullRequest` reference](https://docs.github.com/en/graphql/reference/objects#pullrequest) provides source fields such as `mergedAt` and `mergeCommit`; those event facts should remain authoritative when a local record is created later.

These references anchor the reporting method. They do not add impact or scope beyond the public PR and its recorded validation.

## What was learned

Outcome ingestion should be complete and idempotent. Complete means retaining the public URL, merge commit, shipped files or boundary, validation, claim limits, and unresolved sibling lanes. Idempotent means rerunning the finalizer does not reclassify the same source event as new activity merely because another representation was written later.

A derived write can still justify its own daily movement when it changes future review behavior—for example, a new checklist gate or a corrected trust-model rule. This window did not do that. It materialized the already-published RAMPART outcome in its canonical owner. The honest record is therefore a bounded closure note with an explicit stop condition.

## Takeaways

- **Concrete rule:** identify security activity by source object and source-event time; retain record time as provenance, not as a second event.
- Check whether the merge, finding, and reusable lesson were already published before turning a vault delta into a new public claim.
- Treat one upstream fix, its archive entry, and its canonical outcome note as linked representations of one event.
- Give a later workflow or checklist change separate credit only when it changes future review behavior in a concrete way.

## Repeat next time

- Query the closed local merge window and verify every accepted event against its actual timezone-converted `mergedAt` value.
- For each recent vault delta, record `source identity`, `source event time`, `vault record time`, and `already synthesized?` before drafting.
- Leave `_data/merged_prs.yml` unchanged when the source window is empty, even if a prior event's outcome note changed.
- If a writeback only canonicalizes an already-covered event, publish a bounded provenance record and stop; do not invent another technical lesson.
- If the writeback changes a checklist or workflow, name that changed gate and route it to the smallest existing vault owner.

## Vault redirect

- Canonical outcome: `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART payload artifact path containment.md`.
- Publication-method owner: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
- Review workflow: `05 - Workflows/Workflow - GitHub Outcome Ingestion Loop.md`.

The existing publication-method takeaway already distinguishes source events, canonical vault deltas, and derived index writes, including the rule that later writeback must not become a second event. This post applies that rule to the August 15 window without creating a duplicate private lesson. Unrelated pre-existing vault working-tree changes were left untouched.
