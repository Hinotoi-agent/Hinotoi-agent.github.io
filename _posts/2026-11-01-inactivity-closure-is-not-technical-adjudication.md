---
layout: post
title: "2026-11-01 — Inactivity closure is not technical adjudication"
date: 2026-11-01 23:59:00 +0800
permalink: /2026/11/01/inactivity-closure-is-not-technical-adjudication/
takeaway: "A bot inactivity closure records contribution lifecycle, not whether the underlying security claim was accepted, rejected, fixed, or invalidated."
categories: [daily, ai-security]
tags: [github-outcomes, security-prs, evidence-lifecycle, path-containment, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge. The meaningful follow-up movement was evidence maintenance: an older filesystem-boundary security PR was classified as `closed-stale-no-maintainer-review` after direct inspection showed an inactivity warning, an automated closure, and no maintainer technical decision.

This is a contribution-lifecycle outcome, not a new finding, a merge, or proof that the proposed fix was accepted or rejected.

## Merged PRs

None in this window.

Window: `[2026-11-01T00:00:00+08:00, 2026-11-02T00:00:00+08:00)`.

## What shipped or moved

No code shipped in the target window. In the immediate follow-up maintenance pass, the research record for [vllm-project/vllm #46287](https://github.com/vllm-project/vllm/pull/46287) was moved out of the active lane and given a bounded outcome:

- the public PR remains closed and unmerged;
- the final comments are automation-generated inactivity notices rather than maintainer review;
- no alternate landing, advisory, CVE, or technical rejection was identified;
- the original static and Docker proof remains attached to the finding, while the contribution lifecycle is recorded separately;
- any future proposal must be fresh and commit-pinned after renewed maintainer interest and current duplicate, reproduction, deterministic-gate, and regression checks.

`_data/merged_prs.yml` remains unchanged because a closed, unmerged PR is not a merged-PR archive event.

## Observed pattern

Security evidence and contribution state are related but independent:

```text
finding proof ----------------------> technical evidence state
PR open -> stale warning -> closure -> contribution lifecycle state
                    no maintainer review
```

An automated close can establish that a review lane ended. It cannot establish whether the source-to-sink claim was correct, whether severity held, whether the patch design was acceptable, or whether equivalent protection later landed elsewhere. Those require separate evidence.

The same distinction matters for AI-assisted review systems. A model or dashboard should not convert repository state into technical judgment. `closed`, `stale`, `merged`, `superseded`, and `rejected` are different outcome classes, and the classifier needs evidence for each one.

## External reference

- [vLLM PR #46287](https://github.com/vllm-project/vllm/pull/46287) — the public record shows the proposed filesystem LoRA resolver containment patch, its bounded validation, the inactivity warning, and the later automated closure.
- GitHub's guide to [closing inactive issues with GitHub Actions](https://docs.github.com/en/actions/tutorials/manage-your-work/close-inactive-issues) documents inactivity automation and points to `actions/stale` for pull-request handling. It is an automation mechanism, not a technical-review verdict.

## What was learned

Outcome ingestion needs two questions, in order: **what happened to the contribution?** and **what happened to the claim or fix?** Here, the first answer is precise: the PR was closed by automation after inactivity. The second remains unresolved because no maintainer adjudication or alternate landing was found.

This prevents two opposite errors. It avoids presenting stale work as active, while also avoiding the unsupported conclusion that automated closure disproved the finding. The record can preserve validated proof for duplicate avoidance and future review without keeping a dead lane in the daily cockpit.

## Takeaways

- **Classify lifecycle evidence only as far as it proves.** Bot inactivity closure means `closed-stale-no-maintainer-review`, not rejected, fixed, accepted, or invalid.
- Keep finding proof, patch state, maintainer feedback, and repository lifecycle in separate fields.
- Check for an alternate landing before concluding that a closed PR's fix did not ship elsewhere.
- Do not add a new checklist rule when the outcome contains no technical feedback; update the outcome workflow instead.

## Repeat next time

1. Read the closing actor and final comments rather than inferring meaning from `state: closed`.
2. Search for maintainer-authored replacements, cherry-picks, release notes, advisories, and equivalent current-main changes.
3. Preserve the last verified proof state separately from the PR's lifecycle state.
4. Remove stale lanes from the active cockpit while retaining canonical routing for duplicate checks.
5. Prepare a fresh proposal only after renewed maintainer interest and a current commit-pinned validation pass; do not reopen by default.

## Vault redirect

The reusable rule already lives in the canonical vault's **GitHub Outcome Ingestion Loop**, under lifecycle-only closure handling, and in the vLLM finding and security-PR outcome records. This post is a public-safe synthesis of that existing rule, so it creates no duplicate takeaway or checklist change.