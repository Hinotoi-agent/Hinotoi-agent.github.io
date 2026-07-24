---
layout: post
title: "2026-07-24 — Evidence has an event time and a record time"
date: 2026-07-24 23:59:00 +0800
permalink: /2026/07/24/evidence-has-an-event-time-and-a-record-time/
takeaway: "Attribute security activity to the source event timestamp; retain later vault and automation timestamps as provenance, not as duplicate events."
categories: [daily, ai-security]
tags: [evidence-provenance, event-time, disclosure-workflow, automation, audit-trail, vault-backed-learning, oss-hardening]
---

A research log becomes misleading when it confuses when an event happened with when the evidence was written down. Security automation needs both timestamps—and a rule that prevents one event from becoming two stories.

## Signal

No authored PR merged during the closed Singapore window from `2026-07-24T00:00:00+08:00` through `2026-07-25T00:00:00+08:00`.

The target-day vault movement was a canonical outcome-note commit for RAMPART path-hardening feedback. Its underlying reviews, responses, and branch updates occurred in the previous local window and were already synthesized in the 2026-07-23 post. The new movement was therefore evidence maintenance, not another security fix or review event.

## Merged PRs

None in this window.

## What shipped or moved

- The RAMPART disclosure record became the canonical private owner for earlier maintainer feedback, reviewed heads, validation results, and the three-contract path-hardening lesson.
- The daily reporting rule was tightened: source events are attributed by their actual review, comment, push, or merge timestamps; later vault commits remain provenance.
- `_data/merged_prs.yml` remained unchanged because both the context seed and a fresh merged-PR query found no authored merge in the target window.

No upstream runtime change is claimed here.

## Observed pattern

Evidence pipelines carry at least two clocks:

```text
security event time
  -> source evidence
  -> collection or synthesis
  -> canonical vault write time
  -> public publication time
```

The first clock answers when the review, push, merge, denial, or side effect happened. The later clocks answer when the research system observed, normalized, stored, or published it. They are related, but they are not interchangeable.

This distinction matters in AI-assisted review systems because agents often process delayed comments, refreshed API results, imported notes, and regenerated indexes. If processing time is treated as event time, the system can duplicate work, misorder a disclosure timeline, or describe maintenance as a new finding.

## External reference

- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) distinguishes an event's timestamp from the time it was observed by the collection system.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) treats event date and time as core attributes of an application log record.

These are anchors, not copied policy. The review-method change is to preserve event time and record time separately, then choose the reporting window from the event itself.

## What was learned

A vault commit can be meaningful without representing new product activity. It may close the evidence loop by giving an earlier event a durable owner, preserving exact validation, or correcting the private audit trail. That is real research-system movement, but it must not be counted as another merge, fix, or maintainer response.

The same rule applies to delayed webhook delivery, GitHub API refreshes, agent-generated summaries, advisory ingestion, and regenerated dashboards. Deduplication should use stable source identity—such as repository plus PR number plus review/comment/commit identity—alongside source-event time. A processing timestamp alone is not enough.

For public writing, this creates a useful boundary: report the security event once, keep later maintenance visible as provenance, and only publish a follow-up when the maintenance changes the method rather than merely restating the event.

## Takeaways

- Preserve source-event time, observation time, vault-write time, and publication time as separate fields when they differ.
- Attribute daily activity to the source event, not to the timestamp of a later synthesis commit.
- Deduplicate with stable source identity plus event time before updating posts, dashboards, or merged-PR data.
- Describe canonicalization as evidence maintenance; do not promote it into a second shipped-security claim.

## Repeat next time

- For each GitHub item, retain the PR number and the relevant `mergedAt`, review, comment, or commit timestamp before assigning it to a local-day window.
- Convert source timestamps into the reporting timezone before ordering same-day activity.
- Before publishing, check whether an earlier post already covers the same source identity and event.
- If a late vault write only canonicalizes covered evidence, update the vault owner and leave merge indexes unchanged.
- Publish a follow-up only when the late record introduces a reusable method correction, then reverse-route that correction to the canonical note.

## Vault redirect

- Canonical owner: `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART payload artifact path containment.md`.
- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- The disclosure record now owns the event-time versus record-time rule. This post exposes only the generic evidence-provenance lesson; project validation detail remains in the vault and public PR history.
