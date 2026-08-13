---
layout: post
title: "2026-08-13 — Window boundaries must win over query recency"
date: 2026-08-13 23:59:00 +0800
permalink: /2026/08/13/window-boundaries-must-win-over-query-recency/
takeaway: "A recent merge discovered during finalization belongs to its actual local event window, not to the day being finalized."
categories: [daily, ai-security]
tags: [research-operations, event-time, windowing, automation, negative-evidence, vault-backed-learning, oss-hardening]
---

The fresh merge query was not empty, but the closed reporting window was. A later merge must remain attached to its actual Singapore event date rather than being pulled backward into the day under finalization.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-13T00:00:00+08:00` through `2026-08-14T00:00:00+08:00`.

A fresh query did find a merge at `2026-08-14T02:23:30+08:00`. That event is outside this post's half-open interval and belongs to the August 14 record. The target-window vault review found no new source, advisory case, takeaway, checklist change, GitHub follow-up, disclosure record, or workflow delta that should replace that bounded result.

## Merged PRs

None in this window.

## What shipped or moved

- The August 13 Singapore reporting window was finalized only after it closed.
- The pre-run merge seed was checked against a fresh authored merged-PR query.
- The fresh query's later event was classified by local merge time and excluded from the August 13 record.
- Prioritized vault workflows, indexes, checklist history, source watchlist, and recent research state were reviewed; no target-window durable delta qualified for public synthesis.
- `_data/merged_prs.yml` remained unchanged because no merge belonged to this window.

The daily closure record is the only public artifact that moved. No product fix, test change, disclosure movement, or new vulnerability claim is attributed to August 13.

## Observed pattern

A “recent” query and a daily reporting window answer different questions:

```text
fresh recent-event query
  -> convert event timestamp to reporting timezone
  -> test start <= event < end
       -> true: include in target-day post and index
       -> false: preserve for its actual event day
```

Without the explicit interval check, a finalizer can backdate work merely because the event is visible when the job runs. That creates chronology drift: the daily post, merged-PR archive, and eventual case-study context no longer agree about when the underlying change happened.

This is especially important in AI-assisted security publishing. A model can see a highly relevant security merge and produce a plausible summary, but topical relevance does not override event time. The reporting boundary is a policy decision and should be enforced before content generation.

## External reference

- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) distinguishes event time from observed time. The merge occurred when GitHub recorded it, not when the daily finalizer discovered it.
- [Python `datetime` documentation](https://docs.python.org/3/library/datetime.html) anchors the timezone-aware conversion needed before comparing an event against a local reporting interval.
- [GitHub GraphQL search documentation](https://docs.github.com/en/graphql/reference/queries#search) anchors the broad discovery query; application-side window filtering remains necessary when the query returns recent events beyond the target day.

These are method anchors, not proof of repository risk. The review improvement is to make local-time interval membership a deterministic admission gate before drafting or mutating derived indexes.

## What was learned

Freshness is not membership. The later merge is useful evidence for the next reporting window, but it is negative evidence for this one: it proves the query is working while also proving why timestamp filtering cannot be replaced by “latest result” reasoning.

The safe order is deterministic. Query broadly enough to catch timezone-boundary and backfill cases, convert each event timestamp to the reporting timezone, apply the half-open local interval, and only then hydrate PR details or edit the daily post and merged-PR data. This keeps expensive synthesis downstream of a cheap temporal gate.

The same discipline applies beyond PRs. Advisory publication, disclosure updates, workflow changes, and vault notes should keep event time separate from observation or processing time. A later discovery may justify a backfill, but only into the event's correct record and with that decision made explicitly.

## Takeaways

- **Concrete rule:** admit an event only when `window_start <= event_time_local < window_end`; query recency and topical relevance are not substitutes.
- Convert GitHub UTC timestamps to the reporting timezone before ordering or assigning daily records.
- Keep event time, observation time, and processing time separate in security automation.
- Do not hydrate, summarize, or index an out-of-window PR merely because it is the newest result.

## Repeat next time

- Run the broad authored-merge query, then apply the closed Singapore interval before fetching PR bodies or files.
- Order accepted same-day PRs by actual local merge time descending.
- Leave `_data/merged_prs.yml` unchanged when the target interval is empty, even if a later merge is already visible.
- Carry an out-of-window event forward to its proper finalization run rather than pulling it backward.
- For any backfill, name the original event time and the later observation time separately.

## Vault redirect

The durable owners already exist in `06 - Lessons/Takeaway - Public observations should route back into the vault.md` and the canonical source-code and OSS review workflows. They preserve the distinction between source events, canonical vault deltas, and derived writes, including the closed-window evidence rule.

No vault note was changed for this post. The site synthesis applies that existing rule to a concrete timing boundary but does not introduce a new review behavior, so another private note would duplicate the canonical owner. The unrelated pre-existing vault working-tree changes were left untouched.
