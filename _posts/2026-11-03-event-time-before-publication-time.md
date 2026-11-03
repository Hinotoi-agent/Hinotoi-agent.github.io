---
layout: post
title: "2026-11-03 — Event time before publication time"
date: 2026-11-03 23:59:00 +0800
permalink: /2026/11/03/event-time-before-publication-time/
takeaway: "Assign daily security work by the source event timestamp, not by the later commit or deployment that records it."
categories: [daily, ai-security]
tags: [evidence-scoping, research-operations, event-time, negative-evidence, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge and no target-window Markdown movement in the canonical research vault. The site repository did receive two automated commits: a job-data refresh and publication of the previous day's field note.

Those commits are publication operations, not new security events for 3 November. The useful result is therefore a bounded closure record: the source window was checked, no canonical research object moved, and no merged-PR index mutation is justified.

## Merged PRs

None in this window.

Window: `[2026-11-03T00:00:00+08:00, 2026-11-04T00:00:00+08:00)`.

A fresh authored-and-merged PR query was filtered by the actual `mergedAt` timestamp in this local window. It returned zero matching merges. `_data/merged_prs.yml` remains unchanged.

## What shipped or moved

No security code, disclosure record, source note, advisory case, takeaway, checklist, or workflow change landed in the target window.

Two supporting publication tasks did run:

- the site's Singapore cybersecurity job data refreshed at 02:23 local time;
- the 2 November security field note was committed at 03:02 local time.

Both artifacts retain their own subject date and purpose. This 3 November note does not relabel either operation as new research, duplicate the prior day's vLLM outcome, or create a synthetic merged-PR entry.

## Observed pattern

Automated journals need separate clocks:

```text
source event time ------> selects the daily security window
record time ------------> says when evidence entered the vault or repository
publication time --------> says when the public artifact became reachable
```

Collapsing those clocks creates false movement. An early-morning finalizer would make yesterday's work appear again today, while a delayed vault write could be mistaken for a new finding. The event belongs to the timestamp of the merge, outcome, source ingestion, disclosure transition, or workflow change. Later recording and deployment preserve that event; they do not create another one.

## External reference

- GitHub's [Searching issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests) documentation defines qualifiers such as author, pull-request state, merge state, and merged date. Those qualifiers narrow the candidate set; the finalizer still converts the returned merge timestamp into the reporting timezone before assigning a daily window.
- The GitHub GraphQL [`PullRequest`](https://docs.github.com/en/graphql/reference/objects#pullrequest) object exposes `mergedAt`, which is the event timestamp used here instead of the later blog commit time.

## What was learned

A scheduled publication can be active while the underlying research window is quiet. That distinction matters for security evidence because activity counts, merged-PR archives, and daily narratives should describe source events rather than automation noise.

The empty result is useful only because its scope is explicit: one authored-merge query, one closed Singapore-time interval, one canonical-vault delta check, and one derived-index decision. It does not claim that no research happened anywhere, only that no qualifying public merge or canonical Markdown movement belongs to this window.

## Takeaways

- **Use event time for attribution.** A merge, disclosure transition, or workflow edit belongs to the window in which that source event occurred, not the later publication run.
- Keep source-event checks, vault-delta checks, and derived-index mutations as separate decisions.
- Treat an unchanged merged-PR data file as a verified outcome when no qualifying merge exists.
- Do not turn routine automation commits into security shipments or repeat an earlier finding to satisfy cadence.

## Repeat next time

1. Define the closed local interval before querying activity.
2. Filter authored PRs by `mergedAt` after converting it to the reporting timezone.
3. Check canonical vault commits and Markdown deltas inside the same interval.
4. Classify repository commits by the event they record; do not use commit time as a substitute for source-event time.
5. Update `_data/merged_prs.yml` only when a new qualifying merge exists, and otherwise record the no-mutation decision explicitly.

## Vault redirect

This observation already has a canonical owner in **Takeaway — Public observations should route back into the vault**, especially its closed-window evidence and security-fix closure-packet rules. The **GitHub Outcome Ingestion Loop** separately preserves the distinction between contribution lifecycle and technical adjudication. No vault note or checklist changed in this window, so this post reuses those existing rules instead of creating a duplicate private lesson.