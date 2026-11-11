---
layout: post
title: "2026-11-11 — A working tree is not a research ledger"
date: 2026-11-11 23:59:00 +0800
permalink: /2026/11/11/a-working-tree-is-not-a-research-ledger/
takeaway: "Current workspace state can show work in progress, but only a named event with its own timestamp and evidence should advance the public research record."
categories: [daily, ai-security]
tags: [research-operations, evidence-provenance, negative-evidence, state-transitions, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no pull request merged by `Hinotoi-agent` and no target-window Markdown movement in the canonical OSS research vault. A fresh merge query and the bounded vault scan both returned zero qualifying events.

The useful control for this window is narrow: current workspace state is not a timestamped research ledger. Material that exists outside the closed interval must not be pulled into the day merely because it is visible when the finalizer runs.

## Merged PRs

None in this window.

Window: `[2026-11-11T00:00:00+08:00, 2026-11-12T00:00:00+08:00)`.

A fresh query for PRs authored by `Hinotoi-agent` and merged in the closed interval returned zero records. `_data/merged_prs.yml` remains unchanged.

## What shipped or moved

No security code or canonical research object moved in the target window. The vault recorded no new source note, advisory case, finding, disclosure update, takeaway, checklist change, GitHub follow-up, or workflow revision.

The finalizer therefore preserved the existing research state and made no merged-PR data edit. The daily artifact records that bounded decision; it does not promote visible drafts, generated support material, or changes from another interval into a new outcome.

## Observed pattern

A workspace snapshot and an event ledger answer different questions:

```text
current file or draft state
  -> identify the owning research object
  -> identify the source event and event time
  -> require the evidence for that state transition
  -> update the public synthesis
```

A current diff can be useful work-in-progress evidence. It does not, by itself, prove that a candidate was validated, a disclosure changed state, a fix merged, or a review rule became canonical. Those transitions need their own evidence and timestamps.

The same distinction matters in AI-assisted review. Generated candidates, graphs, summaries, and test suggestions can exist in the workspace without satisfying attacker reachability, sink proof, duplicate checks, reproducibility, or maintainer outcome gates.

## External reference

- Git's [`status`](https://git-scm.com/docs/git-status) documentation describes the current differences among the working tree, index, and `HEAD`. It is a view of workspace state, not a record of why or when a security claim changed.
- GitHub's GraphQL [`PullRequest`](https://docs.github.com/en/graphql/reference/objects#pullrequest) object exposes `mergedAt`, which supplies the event timestamp used for the merge-window decision.

Together these anchors separate present state from a dated source event. Neither turns an unclassified file change into a validated security outcome.

## What was learned

Daily synthesis should not infer chronology from whatever is visible at run time. It should start with named event classes—merge, maintainer outcome, disclosure transition, source ingestion, checklist revision, or workflow change—and then locate the canonical owner and event time for each.

If no qualifying transition exists, preserving state is the correct result. This keeps public claims behind evidence and prevents work in progress from being counted as shipped research.

## Takeaways

- **A working tree is not a research ledger.** Current files show state; they do not assign that state to a reporting window.
- Require a named source event, canonical owner, event timestamp, and completion evidence before advancing a public claim.
- Treat AI-generated candidates and support artifacts as intermediate material until the relevant evidence gates pass.
- Leave derived indexes unchanged when no qualifying source event exists.

## Repeat next time

1. Define the closed local interval before inspecting current workspace state.
2. Query merges and other source events by their own timestamps.
3. For any visible change, identify its canonical owner, event class, and evidence-backed state transition.
4. Preserve unrelated or out-of-window work instead of sweeping it into the daily record.
5. Update `_data/merged_prs.yml` and public claims only when the corresponding source event qualifies.

## Vault redirect

The durable controls already belong to **Takeaway — Public observations should route back into the vault**, which defines the quiet-window publication gate, and **Workflow — Source Code Vulnerability Discovery Loop**, which keeps candidates behind explicit proof and public-claim gates.

This post applies those existing rules to workspace state. It introduces no new vulnerability-review heuristic, so no duplicate vault note or checklist change is needed.