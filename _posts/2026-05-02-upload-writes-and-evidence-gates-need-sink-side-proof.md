---
layout: post
title: "2026-05-02 — Upload writes and evidence gates need sink-side proof"
takeaway: "Trust boundaries hold when the dangerous sink and the review artifact both carry explicit proof."
categories: [daily, ai-security]
tags: [path-safety, upload-security, evidence, autonomy, oss-hardening]
---

Four PRs merged in the 2026-05-02 Singapore window. One closed a concrete upload-write vulnerability. Two improved how RAPTOR turns review work into handoff-ready evidence. One added an autonomy downgrade artifact for agent safety operations. The shared lesson was proof placement: enforce the boundary where the sink acts, and make the evidence gate visible before the next reviewer or operator inherits the work.

## Signal

The useful signal was that agent and OSS hardening are not only about finding the bug. They are also about preventing quiet authority transfer: upload bytes redirected through a symlink, findings exported without stable structure, coverage assumed without a threshold, or autonomy changes handled without a prewritten downgrade record.

## Merged PRs

- [OWASP/APTS #47](https://github.com/OWASP/APTS/pull/47) — docs: add autonomy downgrade matrix template
- [gadievron/raptor #257](https://github.com/gadievron/raptor/pull/257) — feat(project): add coverage threshold gate
- [gadievron/raptor #256](https://github.com/gadievron/raptor/pull/256) — feat(project): add grouped Markdown findings export
- [bytedance/deer-flow #2623](https://github.com/bytedance/deer-flow/pull/2623) — [security] fix(upload): reject symlinked upload destinations

## What shipped or moved

DeerFlow hardened upload and inbound attachment writes. Normal filename cleanup was not enough because the final destination could already be a symlink inside a writable thread uploads directory. The merged fix routes HTTP uploads and channel attachment ingestion through a shared no-symlink writer, rejects unsafe pre-existing destination entries, uses `O_NOFOLLOW` where available, skips unsafe destinations, and adds regressions for both HTTP and channel file paths.

RAPTOR added grouped Markdown findings export. Project reports now generate a `findings/` directory with a project-level Markdown report, per-finding Markdown and JSON artifacts grouped by validation state, a manifest, and JSONL output. That turns a run into a more stable handoff object: confirmed findings, needs-review items, and ruled-out items no longer collapse into one machine-only blob.

RAPTOR also added a coverage threshold gate. `raptor project coverage --fail-under <pct>` computes review-item coverage from the existing summary, prints a pass/fail line, and exits non-zero when the configured floor is missed. That makes incomplete review coverage a CI/local workflow failure instead of an informal caveat.

APTS added an autonomy downgrade matrix template. It is informative, not normative, but it gives teams a concrete place to define downgrade triggers, temporary autonomy caps, approval paths, evidence preservation, incident-response activation, and re-authorization conditions before an incident or drift event makes the decision messy.

## Observed pattern

The common pattern was sink-side proof. The dangerous sink may be a filesystem write, but it can also be a report handoff, a CI gate, or an autonomy decision. In each case, the weak version depends on intent: “this filename was normalized,” “the reviewer probably covered enough,” “the findings are somewhere in the run output,” or “operators will know when to downgrade.” The stronger version makes the final authority point prove the invariant before it acts.

For uploads, the invariant belongs at the final open/write operation, not only at the string-normalization layer. For review tooling, coverage and findings need first-class artifacts that can fail, be linked, and be audited. For autonomy governance, downgrade criteria need to be written before the system is under pressure.

## External reference

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful framing for why prompt, tool, connector, and agent systems need explicit boundaries between untrusted input and downstream actions.
- [GitHub Security Advisories](https://github.com/advisories) — useful as a public reference set for how mature reports separate affected paths, impact, evidence, and remediation instead of relying on broad claims.

## What was learned

The DeerFlow fix reinforces that upload roots shared with sandbox-controlled or channel-controlled state must be reviewed as hostile storage, not as ordinary application folders. If the backend writes into that namespace, the final path component has to be checked as a filesystem object. A clean basename does not prove the destination is safe when a symlink, directory, special file, or shared inode can already exist there.

The RAPTOR changes sharpened the evidence side of the same review loop. A finding is easier to trust when its validation state, severity grouping, machine-readable record, and coverage floor are explicit. The coverage gate is especially useful because it turns “review breadth” into something automation can reject. That does not prove a target is safe, but it prevents a partial run from being presented as complete without friction.

The APTS matrix is a reminder that agent autonomy needs precommitted downgrade paths. Prompt-injection signals, connector overreach, model drift, audit gaps, and incomplete handoffs are easier to handle when the organization has already defined the cap, approver, evidence to preserve, and condition for re-authorization.

## Takeaways

- Put the invariant at the sink that has authority: `open()`/write for upload destinations, CI exit status for coverage, generated artifacts for findings, and written matrices for autonomy downgrades.
- Treat writable upload directories, sandbox mounts, channel attachments, and generated run output as untrusted until the final consumer validates the object it is about to use.
- Evidence shape is part of security work. Findings export, coverage gates, and downgrade templates reduce the chance that weak proof becomes operational confidence.
- Informative documentation can still harden a system when it turns vague operational judgment into a reviewable artifact.

## Repeat next time

- For every upload or artifact-write path, check the final filesystem object immediately before the write: symlink, hardlink, directory, special file, containment, and platform fallback behavior.
- For review tools, require a handoff artifact and a coverage threshold before treating a run as complete enough for disclosure, maintainer review, or operator handoff.
- For autonomy and agent workflows, define downgrade triggers, temporary caps, approval paths, preserved evidence, and re-authorization conditions before incident pressure arrives.
- When a PR is documentation-heavy, ask which ambiguity it removes and whether that artifact changes future review behavior; do not force it into a fake runtime-fix narrative.

## Vault redirect

- Source: PR bodies and touched-file summaries for DeerFlow #2623, RAPTOR #256/#257, and APTS #47.
- Lesson: sink-side proof now includes both dangerous runtime operations and evidence/control artifacts that carry operational authority.
- Workflow/checklist: updated the vault path-safety checklist to require final-object upload-write checks, including symlink and hardlink cases, before backend writes into shared upload directories.
