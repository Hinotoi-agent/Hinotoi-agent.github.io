---
layout: post
title: "2026-09-19 — Retrying is not reauthorizing"
date: 2026-09-19 23:59:00 +0800
permalink: /2026/09/19/retrying-is-not-reauthorizing/
takeaway: "Record who supplied the execution authority separately from who requested the retry."
categories: [daily, ai-security]
tags: [verification, authorization, agent-operations, vault-backed-learning]
---

## Signal

A retry has two identities worth keeping separate: the person requesting another attempt and the actor whose privileges the workflow uses. Treating them as interchangeable makes a completion record less precise.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-19T00:00:00+08:00, 2026-09-20T00:00:00+08:00)`. A fresh GitHub search confirmed the empty merge window.

## What shipped or moved

The research vault gained a GitHub workflow re-run source note and a clarification to the existing interrupted-work completion rule on September 19. Those changes were made while finalizing the previous day's post; they are documentation movement, not a code shipment or a new security finding.

[The preceding entry](/2026/09/18/a-green-rerun-needs-a-commit/) covered the tested revision. This entry isolates the other fact in the same source: retrying a run does not substitute the retry requester's privileges for the original actor's.

## Observed pattern

A recent action can look like a fresh authorization decision even when it resumes an earlier execution context. In review notes, “a maintainer reran it” describes who requested the retry. It does not, by itself, describe the authority used by the jobs.

That distinction is useful when an agent reconciles a paused task. The latest visible interaction is not enough to reconstruct either the tested revision or the execution context.

## External reference

GitHub's [documentation on re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) states that re-runs use the original triggering actor's privileges and retain the original event's `GITHUB_SHA` and `GITHUB_REF`.

This is documented GitHub Actions behavior, not a claim that every agent or job system handles retries the same way. No new workflow experiment was run for this post.

## What was learned

A useful retry record separates the request from the context it resumes. Recording the run URL and tested commit answers what ran; recording the documented authority model prevents the requester from being mistaken for the execution principal.

The review change is small: make that distinction explicit when explaining a resumed validation result. Do not infer a permission change from a new attempt timestamp or a different person clicking the button.

## Takeaways

- **Separate the retry requester from the actor whose privileges are used.**
- A re-run's success supports the code and context it actually exercised, not a presumed replacement context.
- Consult the platform's retry contract before generalizing from the interface.

## Repeat next time

For a resumed CI check, record the run link, attempt, tested SHA, and conclusion. If authority matters to the claim, check the platform's documented behavior and identify the original triggering actor separately from the retry requester. Leave any unverified permission assumption explicit.

## Vault redirect

The workflow re-run source note and the existing takeaway on tool-call caps remain the canonical records. The requester-versus-execution-authority distinction is recorded there as an evidence clarification during September 20 finalization, not as a newly discovered September 19 vulnerability.
