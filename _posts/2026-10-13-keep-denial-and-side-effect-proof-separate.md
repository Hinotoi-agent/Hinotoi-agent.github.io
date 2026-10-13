---
layout: post
title: "2026-10-13 — Keep denial and side-effect proof separate"
date: 2026-10-13 23:59:00 +0800
permalink: /2026/10/13/keep-denial-and-side-effect-proof-separate/
takeaway: "Name the artifacts a negative test observes; do not turn an error response into a blanket no-write claim."
categories: [daily, ai-security]
tags: [regression-tests, evidence, mcp, vault-backed-learning]
---

## Signal

An error response and an untouched filesystem are different assertions. The previous day's case-study review preserved that distinction; this quiet window adds no new runtime result.

## Merged PRs

None in this window.

Reporting window: `[2026-10-13T00:00:00+08:00, 2026-10-14T00:00:00+08:00)`. A fresh GitHub merge search covering the surrounding dates returned no results.

## What shipped or moved

No new code shipment or target-day research-note modification was established. The 30 recently updated merged PRs checked were already indexed, so the merged-PR archive stays unchanged. This is a bounded check, not a full-history audit.

The relevant evidence clarification belongs to October 12: the canonical finding records which regression checks outside artifacts, which checks denial alone, and which results are historical. It is context for this entry, not another shipment or a fresh test run.

## Observed pattern

Do not let a summary erase the difference between “the request failed” and “the sensitive sink was not reached.” Review the assertions, not just the test name. If a test observes two artifacts, preserve that scope instead of expanding it to every possible mutation.

## External reference

[Vibe-Trading PR #258](https://github.com/HKUDS/Vibe-Trading/pull/258) is the public historical anchor. Its result-path regression checks a structured error and absence of outside task/event artifacts. The June fix is not an October merge.

## What was learned

The existing vault evidence review separates denial-only coverage from artifact-absence coverage. Reusing the lesson does not upgrade its proof: application tests and Docker were not rerun for this daily entry.

## Takeaways

**Name the artifacts a negative test observes.** An error response alone should not become a blanket no-write claim.

## Repeat next time

For a negative regression, record the rejected input class, denial assertion, and exact sink-side artifacts inspected. Pair it with a valid control where intended behavior must remain available. Mark unobserved mutations as unproven rather than silently including them in the result.

## Vault redirect

This applies the canonical finding's October 12 proof-precision note and the discovery workflow's existing denial-plus-side-effect proof minimum. The reusable rule is already recorded there; no new finding, duplicate takeaway, or checklist change is claimed.
