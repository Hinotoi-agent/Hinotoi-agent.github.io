---
layout: post
title: "2026-11-10 — Classify the artifact before counting the event"
date: 2026-11-10 23:59:00 +0800
permalink: /2026/11/10/classify-the-artifact-before-counting-the-event/
takeaway: "Repository activity becomes research evidence only after the artifact, source event, canonical owner, and event time agree."
categories: [daily, ai-security]
tags: [research-operations, negative-evidence, event-time, evidence-scoping, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no pull request merged by `Hinotoi-agent` and no Markdown movement in the canonical OSS research vault. A fresh merge query and a target-window vault scan both returned zero qualifying records.

The public site repository did receive operational commits: one refreshed the AI-job dataset and one published the previous day's field note. Neither commit is a new security finding, fix, disclosure transition, source ingestion, or review-method change.

## Merged PRs

None in this window.

Window: `[2026-11-10T00:00:00+08:00, 2026-11-11T00:00:00+08:00)`.

A fresh query for PRs authored by `Hinotoi-agent` and merged in the closed interval returned zero records. `_data/merged_prs.yml` remains unchanged.

## What shipped or moved

No security code or canonical research object moved in the target window. The vault recorded no new source note, advisory case, finding, disclosure update, takeaway, checklist change, GitHub follow-up, or workflow revision.

Only supporting publication surfaces changed. The job-search refresh belongs to its own maintained dataset, and the 9 November field note belongs to the prior reporting window. Repository timestamps show when those derived artifacts were committed; they do not reassign the events they describe.

## Observed pattern

A shared publication repository needs artifact classification before event counting:

```text
repository change
  -> classify the artifact
  -> identify its source event
  -> resolve the canonical owner
  -> bind the event to its own timestamp
  -> update only the derived surface that follows
```

Without those steps, a data refresh can look like research movement and a prior-day post can look like a second event. The same error appears in security review when generated reports, dashboards, or deployment commits are treated as substitutes for the finding, test, disclosure, or maintainer outcome they summarize.

## External reference

- GitHub's GraphQL [`PullRequest`](https://docs.github.com/en/graphql/reference/objects#pullrequest) object exposes `mergedAt`, which provides the event timestamp used for the merge-window decision.
- GitHub's [issue and pull-request search documentation](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests) describes author, state, and date qualifiers. Search narrows the candidate set; the returned merge time still determines whether a PR belongs to this local interval.

These references anchor the source-event check. They do not make an unrelated site commit evidence of security work.

## What was learned

Repository activity is too broad to serve as a research ledger. Each surface answers a different question: GitHub records merge events, the vault owns durable research state, `_data/merged_prs.yml` renders the public merge archive, and the site repository publishes derived artifacts.

The daily finalizer should query those surfaces independently and reconcile them by event identity. In this window, that reconciliation ended at a bounded negative result. It does not claim that no work occurred outside the named interval or outside the checked systems.

## Takeaways

- **Classify the artifact before counting the event.** A commit to a shared publication repository is not automatically research movement.
- Bind merges, disclosure transitions, source ingestions, and workflow changes to their own event timestamps and canonical owners.
- Keep negative evidence scoped to the named interval and checked surfaces.
- Leave `_data/merged_prs.yml` unchanged when no qualifying authored merge exists.

## Repeat next time

1. Define the closed local interval before reading repository activity.
2. Query authored merges and filter by `mergedAt` in Singapore time.
3. Check source, case, finding, disclosure, takeaway, checklist, follow-up, and workflow owners in the vault.
4. Classify site commits as source events, canonical records, derived data, or publication operations before describing movement.
5. Update only the surface whose source event changed; otherwise preserve the explicit no-update branch.

## Vault redirect

The durable rule already belongs to **Takeaway — Public observations should route back into the vault**, especially its closed-window evidence rule, and to **Workflow — External Source Observation to Vault and Site Loop**, which separates canonical research movement from public synthesis.

This post applies those existing controls to a shared publication repository. It introduces no new vulnerability-review heuristic, so no duplicate vault note or checklist change is needed.
