---
layout: post
title: "2026-10-07 — Backfill is not new work"
date: 2026-10-07 23:59:00 +0800
permalink: /2026/10/07/backfill-is-not-new-work/
takeaway: "Repair the record without moving the event."
categories: [daily, ai-security]
tags: [evidence, research-method, vault-backed-learning]
---

## Signal

October 7 closes without an authored merge. The finalization pass found something different: five older public merges absent from the site's archive. Correcting that record does not make those fixes October work.

## Merged PRs

None in this window.

Window: `[2026-10-07T00:00:00+08:00, 2026-10-08T00:00:00+08:00)`. A fresh GitHub merge search covering the surrounding UTC dates returned no results.

## What shipped or moved

No target-window Markdown modification was found in the research vault. During the October 8 finalization pass, the archive comparison identified five missing entries from May: two OpenHarness local-only command changes and three PaddleOCR configuration/deserialization changes. Direct PR lookups confirmed their merge timestamps and changed files. The archive now records them under their original May dates, not this reporting window.

This is an index repair, not a new patch, fresh reproduction, or disclosure outcome.

## Observed pattern

A daily activity query and an archive reconciliation answer different questions. An empty daily window does not prove that the historical index is complete. Conversely, repairing an omission does not establish new engineering activity on the repair date.

## External reference

The public records are [OpenHarness #253](https://github.com/HKUDS/OpenHarness/pull/253), [OpenHarness #252](https://github.com/HKUDS/OpenHarness/pull/252), [PaddleOCR #17930](https://github.com/PaddlePaddle/PaddleOCR/pull/17930), [PaddleOCR #17931](https://github.com/PaddlePaddle/PaddleOCR/pull/17931), and [PaddleOCR #17950](https://github.com/PaddlePaddle/PaddleOCR/pull/17950). They anchor the backfill only; this post does not reassess their security claims.

## What was learned

The existing vault rule separating event time from record time applies to archive maintenance too. Keep the daily merge query bounded to the reporting window, and reconcile historical records separately. State the repair time when the repair happens during a later finalization run.

## Takeaways

**Repair the record without moving the event.** A newly indexed PR is not a newly merged PR, and a checked title or file list is not a rerun of its tests.

## Repeat next time

Compare public PR URLs against the data-backed archive, hydrate missing records directly, and retain their original local merge dates. Keep the bounded comparison distinct from a claim of complete lifetime coverage. Do not change a quiet day's merge count to accommodate historical backfill.

## Vault redirect

The existing public-observation takeaway owns the separation of source events, canonical vault deltas, and derived-index decisions, including its closed-window evidence and event-time/record-time rules. This applies that method to a concrete archive correction; no new checklist rule or duplicate vault note is needed.
