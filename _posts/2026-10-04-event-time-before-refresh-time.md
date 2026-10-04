---
layout: post
title: "2026-10-04 — Event time before refresh time"
date: 2026-10-04 23:59:00 +0800
permalink: /2026/10/04/event-time-before-refresh-time/
takeaway: "A refreshed research dashboard is not a newly completed security fix."
categories: [daily, ai-security]
tags: [evidence, research-method, vault-backed-learning]
---

## Signal

October 4 closes without an authored merge or target-window Markdown modification in the checked research vault. The follow-up maintenance pass refreshed the research and disclosure dashboards on October 5; that belongs to the verification context, not to October 4's shipped work.

## Merged PRs

None in this window.

Window: `[2026-10-04T00:00:00+08:00, 2026-10-05T00:00:00+08:00)`. A fresh GitHub merge search covering the window and its adjacent UTC dates returned no results.

## What shipped or moved

No new fix, disclosure outcome, or review-method change was evidenced for October 4. The subsequent dashboard refresh distinguishes historical activity snapshots from current next actions and local disclosure-record checks from fresh external confirmation. It does not claim that pending proof or approval gates have passed.

The recent merged-PR archive check found no missing entries, so the index stays unchanged.

## Observed pattern

A record has more than one clock: when the underlying event happened and when someone checked or summarized it. Treating the second as the first can turn maintenance into an apparent security outcome.

## External reference

[GitHub's pull-request schema](https://docs.github.com/en/graphql/reference/pulls) exposes `mergedAt` as the merge timestamp. Use the event timestamp for the daily merge window; keep dashboard refresh time separate.

## What was learned

This is a reapplication of the vault's existing event-time versus record-time rule, not a new finding. A current dashboard can help choose the next review action without making old evidence current or completing an unresolved gate.

## Takeaways

**Check what a timestamp describes before using it as evidence of progress.** A local record scan, an upstream status check, and a completed fix are distinct claims.

## Repeat next time

Record the reporting window, the source checked, and the remaining proof or approval gap separately. Attribute after-midnight maintenance to its actual date rather than backfilling it as a prior-day shipment.

## Vault redirect

The existing *Public observations should route back into the vault* takeaway owns the event-time/record-time and closed-window rules. The research and disclosure dashboards own the next actions. No new heuristic or private finding detail is introduced here, so no duplicate vault note is needed.
