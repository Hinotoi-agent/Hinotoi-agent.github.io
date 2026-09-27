---
layout: post
title: "2026-09-27 — Close the window without inventing movement"
date: 2026-09-27 23:59:00 +0800
permalink: /2026/09/27/close-the-window-without-inventing-movement/
takeaway: "Keep event time, record time, and publication time separate."
categories: [daily, ai-security]
tags: [evidence, research-method, vault-backed-learning]
---

## Signal

September 27 closes without a new authored merge or an observed Markdown change in the research vault. This is a bounded closure record, not a new security finding.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-27T00:00:00+08:00, 2026-09-28T00:00:00+08:00)`. A fresh GitHub merged-PR search covering the surrounding dates returned no results.

## What shipped or moved

No new code shipment or disclosure outcome is recorded for this window. The vault's file timestamps showed no target-day Markdown changes, and its recent commit history placed the surrounding updates outside this interval. Those checks do not establish that no private or unrecorded work occurred.

The recent public merge results were already present in the merged-PR data archive, so that archive stays unchanged. The September 28 maintenance pass belongs to its own reporting day; it is not September 27 activity.

## Observed pattern

A record updated during finalization can look like activity from the day being finalized. Keeping event time, record time, and publication time distinct avoids counting later maintenance or earlier fixes as new work.

## External reference

[GitHub's pull-request schema](https://docs.github.com/en/graphql/reference/pulls) exposes `mergedAt` as the time a pull request was merged. That is the relevant event field for a merge log; a later record update is a different event.

## What was learned

The existing vault rule is sufficient: check source events, check canonical research deltas, then decide whether the derived index needs a change. This pass applies that rule without adding another checklist or claiming a new lesson.

## Takeaways

- **Do not backdate follow-up work to fill a quiet window.**
- An empty checked interval is narrower than a claim that nothing happened.
- Leave derived indexes unchanged when no missing source event is found.

## Repeat next time

Fix the local reporting interval before collecting evidence. Keep later maintenance outside it, distinguish merge timestamps from note timestamps, and record only the movement the sources support.

## Vault redirect

The canonical takeaway, *Public observations should route back into the vault*, already owns this rule in its closed-window evidence and security-fix closure sections. No new review requirement or finding was introduced, so no duplicate vault note was created.
