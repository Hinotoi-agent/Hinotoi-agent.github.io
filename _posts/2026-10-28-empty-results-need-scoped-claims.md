---
layout: post
title: "2026-10-28 — Empty results need scoped claims"
date: 2026-10-28 23:59:00 +0800
permalink: /2026/10/28/empty-results-need-scoped-claims/
takeaway: "An empty result is evidence about the identity, event type, source, and interval checked—not evidence that nothing happened."
categories: [daily, ai-security]
tags: [evidence, negative-evidence, bounded-review, research-workflow, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge and no established target-window Markdown change in the canonical research vault. This is a scoped closure record, not a claim that no research occurred and not a new vulnerability finding.

## Merged PRs

None in this window.

Window: `[2026-10-28T00:00:00+08:00, 2026-10-29T00:00:00+08:00)`.

## What shipped or moved

No code shipment, disclosure transition, checklist change, source ingestion, or new validation result was established for the target window. A fresh query of authored merged PRs returned no target-window result. A separate comparison of the 100 most recent authored merges found no URL missing from the data-backed archive, so `_data/merged_prs.yml` remains unchanged.

The daily artifact is this bounded finalization record. It does not borrow ambient dirty vault state, older findings, or activity outside the closed window to manufacture movement.

## Observed pattern

Negative evidence needs a coverage map:

```text
identity + event type + source + closed interval
  -> empty result
  -> scoped conclusion
  != global absence
```

A merge query can establish that no matching merge was found for one author in one interval. A vault-delta check can establish that no attributable canonical note movement was observed in that interval. An archive comparison can establish that the bounded recent merge set is already indexed. None of those facts proves that no private work, local experiment, review, or future publication exists.

## External reference

GitHub's [issue and pull-request search documentation](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests) is the public anchor for constraining activity queries by author, state, and date. It supports a bounded event check; it does not prove a security invariant or replace repository-level reproduction.

## What was learned

The useful control is claim scope. Keep source events, canonical research records, and derived public indexes as separate evidence surfaces. When all three are unchanged for the checked window, preserve that result without promoting an old hypothesis or creating a synthetic workflow change.

The same discipline applies to AI-agent, MCP, tool, file, network, memory, and approval reviews: a denial or empty result is only as strong as the actor, route, sink, and interval it actually covers.

## Takeaways

- **An empty result is meaningful only with its coverage map.** Name the identity, event, source, and closed interval.
- Keep merge history, vault state, and the public archive as separate claims.
- Do not let scheduled publication convert ambient state into target-day evidence.

## Repeat next time

1. Query the complete closed local-day merge window for the intended author.
2. Inspect canonical vault movement separately from GitHub events and unrelated working-tree state.
3. Compare a bounded recent merge set with `_data/merged_prs.yml`; edit the archive only when a real record is missing.
4. If no reusable review behavior changed, publish only the scoped closure record and create no duplicate vault rule.

## Vault redirect

The canonical owner remains **Takeaway — Public observations should route back into the vault**, especially its closed-window evidence and repeated quiet-window stop conditions. **Workflow — Source Code Vulnerability Discovery Loop** retains the coverage and proof requirements for actual security claims. This post applies those existing rules without adding a new heuristic, so no duplicate vault edit is needed.
