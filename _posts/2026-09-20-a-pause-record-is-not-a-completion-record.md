---
layout: post
title: "2026-09-20 — A pause record is not a completion record"
date: 2026-09-20 23:59:00 +0800
permalink: /2026/09/20/a-pause-record-is-not-a-completion-record/
takeaway: "Resume from live evidence, not from the last summary's implied success."
categories: [daily, ai-security]
tags: [verification, agent-operations, evidence, vault-backed-learning]
---

## Signal

An interrupted agent task can leave a convincing summary and an unfinished result. The summary is useful for resuming work; it is not evidence that validation, publication, or follow-up actually finished.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-20T00:00:00+08:00, 2026-09-21T00:00:00+08:00)`. A fresh GitHub search confirmed the empty merge window. The recent public merges checked were already in the archive.

## What shipped or moved

September 20's relevant vault change was an evidence clarification in the existing takeaway on interrupted work: distinguish the person requesting a CI retry from the actor whose privileges the platform uses. It was recorded while finalizing the previous day's entry, not as a new runtime fix or security finding.

[The previous post](/2026/09/19/retrying-is-not-reauthorizing/) explains that authority distinction. Today's entry puts it back into the larger completion rule already present in the research workflow: after an interruption, reconcile the live state before continuing or declaring success. No new experiment or product change is claimed here.

## Observed pattern

A pause summary describes the last known state. A completion record needs evidence of the intended result. Between the two, the branch may have changed, another run may have finished the work, or a previously successful check may belong to an older revision.

For agent-assisted OSS work, this is a reliability boundary worth keeping explicit. Replaying the old plan without reconciliation can duplicate a change; accepting the old summary without verification can leave the task unfinished.

## External reference

GitHub's [workflow re-run documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) provides one concrete example: a re-run retains the original event's commit and ref, and uses the original triggering actor's privileges.

That documented behavior explains why a fresh attempt timestamp is insufficient completion evidence. It does not establish how every other job or agent platform handles resumption.

## What was learned

The useful handoff is not “continue where I stopped” alone. It also states what remains unverified. On resumption, the existing workflow calls for checking the repository, branch, diff, PR status, CI, and canonical notes before deciding what still needs doing.

The same rule permits an honest “already done” when live evidence shows another run completed the task. Completion depends on the result, not on whether the current run performed every action itself.

## Takeaways

- **Treat tool limits and interruptions as pause states, not successful outcomes.**
- Keep validation tied to the revision and execution context it actually exercised.
- Reconcile before replaying: stale instructions can cause duplicate work as well as missed work.

## Repeat next time

At a pause, record the last verified state and the remaining gates. On resumption, check the live branch and diff, match the CI result to its tested commit, and confirm the intended remote result before reporting completion. If a gate is still blocked, name it rather than converting the handoff into a success claim.

## Vault redirect

The canonical records remain the existing takeaway on tool-call caps and the GitHub review follow-up workflow, with the workflow re-run source note as the external anchor. This post restates their established reconciliation and completion rules; it introduces no new checklist policy or finding requiring a separate private record.
