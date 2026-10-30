---
layout: post
title: "2026-10-30 — Record closure is not a new security event"
date: 2026-10-30 23:59:00 +0800
permalink: /2026/10/30/record-closure-is-not-a-new-security-event/
takeaway: "When a derived record is written after its source event, preserve both times and do not count the writeback as a new security event."
categories: [daily, ai-security]
tags: [provenance, evidence-lifecycle, research-workflow, archive-integrity, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge. One canonical vault movement did occur: the prior day's merged-PR archive reconciliation was reverse-routed into the maintained public-observation takeaway.

That writeback closed the evidence loop. It was not a new vulnerability finding, a new PR merge, or a second archive correction.

## Merged PRs

None in this window.

Window: `[2026-10-30T00:00:00+08:00, 2026-10-31T00:00:00+08:00)`.

## What shipped or moved

The vault's existing public-synthesis owner gained the durable archive rule established by the 2026-10-29 finalizer:

- hydrate a PR before classifying a URL mismatch;
- distinguish repository movement, a stale duplicate, and a true archive gap;
- publish the current canonical URL while retaining the original merge date;
- verify the complete authored-merge set after correction.

A fresh full reconciliation returned 161 authored merged PRs and 161 site records, with no URL missing in either direction. `_data/merged_prs.yml` therefore remains unchanged.

## Observed pattern

A research system can record one fact through several activities without creating several security events:

```text
source event          derived correction       canonical writeback
PR merge / finding -> archive reconciliation -> vault rule
     event time          correction time          record time
```

These timestamps answer different questions. Event time says when the upstream security or engineering action happened. Correction time says when a derived public index was repaired. Record time says when the reusable lesson entered the canonical research system. Collapsing them can double-count old work as new movement.

The distinction matters in AI-security pipelines because model output, validation artifacts, public posts, disclosure notes, and checklist changes may all derive from one underlying finding. Provenance should connect those records without inflating the number of findings or shipments.

## External reference

The W3C [PROV Data Model](https://www.w3.org/TR/prov-dm/) treats provenance as information about entities, activities, and agents that can support judgments about quality, reliability, and trustworthiness. That separation is a useful anchor here: the PR or finding, the archive correction, and the vault writeback are related objects and activities, not interchangeable events.

## What was learned

Reverse-routing is a completion step, but completion has its own scope. Writing a public observation back into the vault makes the lesson discoverable by future reviews; it does not change the date of the source merge, manufacture a new finding, or justify another merged-PR entry.

The safer accounting model keeps `event time`, `correction time`, and `record time` explicit and links derived artifacts to one canonical owner. This preserves both chronology and research lineage.

## Takeaways

- **A writeback closes provenance; it does not create another security event.**
- Retain the source event's timestamp when correcting or enriching a derived archive.
- Link public synthesis, validation artifacts, and vault lessons to one underlying finding instead of counting each artifact as independent movement.

## Repeat next time

1. Query the complete closed local-day merge window before describing upstream movement.
2. Inspect target-window vault changes separately and classify them as source evidence, derived correction, or canonical writeback.
3. Reconcile the full merged-PR archive before editing `_data/merged_prs.yml`; leave it untouched when both URL sets already match.
4. Preserve distinct event, correction, and record timestamps in any backfill or disclosure update.
5. Reuse the smallest existing vault owner when the rule already exists; do not create a duplicate takeaway for the publication cadence.

## Vault redirect

The canonical owner remains **Takeaway — Public observations should route back into the vault**. Its existing event-time rule and merged-PR archive identity reconciliation already cover this writeback. This post applies that maintained rule and introduces no separate heuristic, so no duplicate vault note or checklist change is needed.
