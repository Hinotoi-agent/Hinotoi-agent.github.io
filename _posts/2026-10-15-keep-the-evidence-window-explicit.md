---
layout: post
title: "2026-10-15 — Keep the evidence window explicit"
date: 2026-10-15 23:59:00 +0800
permalink: /2026/10/15/keep-the-evidence-window-explicit/
takeaway: "An activity check needs a time window and a scope; neither is a substitute for security validation."
categories: [daily, ai-security]
tags: [evidence, bounded-review, vault-backed-learning]
---

## Signal

A quiet reporting window: no authored PR merges were returned, and no target-day Markdown modifications were found in the research vault. This is a closure record, not a new finding.

## Merged PRs

None in this window.

Window: `[2026-10-15T00:00:00+08:00, 2026-10-16T00:00:00+08:00)`. The finalization check used the corresponding UTC merge-time range.

## What shipped or moved

No new code shipment, disclosure update, or validation result was established for this window. A separate check of 50 recently updated merged PRs found their URLs already in the archive, so the merged-PR data remains unchanged. That bounded check is not a full-history reconciliation.

## Observed pattern

A daily merge window and a recent-history archive check answer different questions. The first records events for the day; the second catches missing entries. Neither proves that an agent, tool, or storage boundary has been tested.

## External reference

[GitHub's issue and pull-request search documentation](https://github.com/github/docs/blob/main/content/search-github/searching-on-github/searching-issues-and-pull-requests.md) describes the `merged:` date filter. It anchors the activity query, not a claim about runtime behavior.

## What was learned

No new review rule was established. The existing vault guidance remains sufficient: keep source events, canonical note changes, and index-update decisions separate. Do not manufacture research movement to fill a date.

## Takeaways

**Attach negative evidence to its scope.** “No merges in this window” is useful; “nothing happened” exceeds the check.

## Repeat next time

Check the closed local merge window, inspect vault deltas separately, and reconcile recent merge URLs before changing the archive. Require a new proof result before advancing a security claim.

## Vault redirect

This applies the existing closed-window evidence rule in the public-observation takeaway and the proof requirements in the source-code discovery workflow. No new heuristic needs reverse-routing, and no duplicate vault note is created.
