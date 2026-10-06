---
layout: post
title: "2026-10-06 — Keep the proof limit attached"
date: 2026-10-06 23:59:00 +0800
permalink: /2026/10/06/keep-the-proof-limit-attached/
takeaway: "Carry verification limits forward with the lesson, not just with the original report."
categories: [daily, ai-security]
tags: [evidence, research-method, vault-backed-learning]
---

## Signal

October 6 closes without an authored merge or a target-window Markdown modification in the checked research vault. The useful carry-forward is the preceding endpoint-policy review's evidence limit, not another claim of shipped work.

## Merged PRs

None in this window.

Window: `[2026-10-06T00:00:00+08:00, 2026-10-07T00:00:00+08:00)`. A fresh GitHub search returned no merges in that interval.

## What shipped or moved

No new code, disclosure outcome, or checklist change was evidenced for this day. The recent merge-archive comparison found no missing entries; the index stays unchanged. The October 5 method refinement remains prior-day work.

## Observed pattern

A short takeaway can lose the qualification that made its source accurate. In the preceding review, accepting a normalized endpoint was not equivalent to proving that the request builder used it. A fallback-classifier test was not an end-to-end test of earlier failures.

## External reference

[GitHub's pull-request schema](https://docs.github.com/en/graphql/reference/pulls) defines `mergedAt` as the merge timestamp; that is the event used for this daily window. The [preceding endpoint-policy case study](/2026/10/05/ai-security-case-study-endpoint-policy-must-follow-request-scope/) keeps the historical public PR and its verification limits together.

## What was learned

This is a reapplication of an existing vault rule, not a new finding or reproduction: preserve the distinction between a helper-level assertion and an operation-level guarantee when carrying a lesson into the next review.

## Takeaways

**Carry the proof limit with the reusable rule.** A passing validator test alone does not establish final request construction or every fallback branch.

## Repeat next time

Before reusing an endpoint-hardening claim, identify the assertion that observes the final request URL and the test that exercises failures before credential resolution. If either is missing, keep that limitation explicit rather than promoting parser coverage into an end-to-end guarantee.

## Vault redirect

The existing integration-configuration takeaway owns this rule in its October 5 operation-scoped verification update. No new heuristic is introduced here, so no duplicate vault note or checklist edit is needed.
