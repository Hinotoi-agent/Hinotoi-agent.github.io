---
layout: post
title: "2026-09-07 — Checkpoint diffs are file-read sinks"
date: 2026-09-07 05:00:00 +0800
permalink: /2026/09/07/ai-security-case-study-checkpoint-diffs-are-file-read-sinks/
takeaway: "A tracked checkpoint path is not proof of a safe filesystem read: classify the entry, read checkpoint blobs rather than mutable worktree paths, and anchor workspace reads."
categories: [case-study, ai-security]
tags: [case-study, symlink, file-disclosure, workspace-containment, agent-security, rollback]
---

## Signal

A rollback preview looks observational. It still reads files with the server's authority and returns their contents. In an agent workspace, that makes the diff renderer a security boundary—not just a convenience attached to restore.

The revealing mistake was treating “Git listed this checkpoint-relative path” as equivalent to “opening this path cannot leave the checkpoint.” A tracked symlink breaks that equivalence.

## Threat model

The public finding concerns Hermes WebUI's authenticated rollback diff surface. The necessary conditions are a symlink in the selected checkpoint or workspace, a target file readable by the WebUI process outside that boundary, and an authenticated request that renders the diff.

The lower-trust input is filesystem content, not necessarily the request's path string. The checkpoint variant requires the link to be present in the checkpoint; this case does not establish that an arbitrary remote attacker can create one. Nor does it claim unauthenticated access, cross-tenant access, or code execution. Its bounded impact is disclosure of outside-root bytes through a feature intended to inspect workspace state.

## Finding and PR

Public PR: [`nesquena/hermes-webui #4410 — [security] fix(rollback): avoid symlinked checkpoint diff reads`](https://github.com/nesquena/hermes-webui/pull/4410).

Merge commit: [`ad9a7edab05f54e8b1c8ff0f323e5d2e80698bc6`](https://github.com/nesquena/hermes-webui/commit/ad9a7edab05f54e8b1c8ff0f323e5d2e80698bc6).

This is a retrospective on an already merged fix, not a claim of new code shipped this week.

Changed files:

- `api/rollback.py` — classifies checkpoint entries, reads checkpoint blobs, and routes workspace reads through the anchored file API; restore uses blob content too.
- `tests/test_rollback_diff_symlink_disclosure.py` — covers checkpoint and workspace symlink disclosure, skipped restore sources, and a post-commit worktree symlink swap.
- `CHANGELOG.md` — records the security change.

The earlier restore-destination hardening addressed writes outside the workspace. This PR covers the sibling read boundary: a contained restore destination does not make a diff renderer's input reads safe.

## Exploit path

```text
symlink planted in checkpoint content
  -> tracked checkpoint-relative entry returned by git ls-files
  -> entry membership is implicitly treated as permission to read
  -> Path.is_file() and Path.read_text() follow the link
  -> outside-root bytes enter the generated diff
  -> /api/rollback/diff returns those bytes to an authenticated caller
```

The workspace side had the same kind of problem: a regular checkpoint file could be compared against a workspace path whose symlink redirected the current-content read outside the root.

The public proof used a temporary marker file rather than real secrets. Before the fix, the checkpoint link made that marker appear as deleted content in the diff. The disclosure occurred while preparing the preview; no restore was required.

## Mitigation

The merged implementation separates membership, file type, and content retrieval:

1. `_checkpoint_entry_modes()` collects Git index modes with `git ls-files -s`. `_checkpoint_entry_is_regular()` accepts only regular-file entries.
2. `_read_checkpoint_text()` reads accepted checkpoint content through `_read_checkpoint_blob()`, using `git show HEAD:<path>` instead of reopening the checkpoint worktree path.
3. `_read_workspace_text()` delegates to the existing `api.workspace.read_file_content()` boundary rather than ordinary pathname reads. Rejected or unreadable workspace content is treated as absent.
4. Restore skips non-regular checkpoint entries and writes Git blob bytes through the anchored destination helpers. Swapping a committed regular file's worktree path to a symlink therefore does not substitute the link target's bytes.

The compatibility trade-off is explicit: symlink and special checkpoint entries are skipped, not rendered by dereferencing their targets. Regular checkpoint content remains available. This is not a new global filesystem policy or a claim to harden every WebUI file surface.

## Verification

The merged test file supplies concrete negative and positive assertions:

- `test_checkpoint_diff_does_not_follow_checkpoint_symlink` commits a link to a temporary outside marker. It requires an empty `files_changed` list and excludes both the marker and `leak.txt` from the diff.
- `test_checkpoint_diff_does_not_follow_workspace_symlink_escape` compares a regular checkpoint file against an escaping workspace link. It excludes the outside marker while retaining `checkpoint content` in the diff—a useful-content control, not just an empty-response check.
- `test_restore_checkpoint_skips_checkpoint_symlink_sources` requires no restored files, no created `leak.txt`, and no copied marker in the workspace.
- `test_restore_checkpoint_reads_git_blob_after_worktree_symlink_swap` commits regular content, replaces the checkout file with a symlink, and then restores. The restored file must contain exactly `checkpoint blob content\n`, not the external marker. This is the positive restore control under an adversarial worktree change.

The PR records focused host and `python:3.11-slim` Docker validation using:

```sh
./scripts/test.sh tests/test_rollback_diff_symlink_disclosure.py tests/test_rollback_restore_symlink_containment.py
```

It reports six passing tests in those recorded runs, plus Ruff and whitespace checks. Its Docker before/after proof records the vulnerable marker appearing in the diff and the patched result as `files_changed=[]`, `marker_in_diff=False`, and an empty diff.

Those execution results are historical evidence from the public PR, not a fresh test run for this article. The test assertions above were checked against the published PR diff, including the blob-based restore change. The disclosure tests prove absence of sensitive response bytes; the restore tests additionally prove no unwanted file creation or copying. They should not be described as an HTTP authentication test or as proof that no filesystem syscall ever occurred.

## What was learned

Containment is about the object whose bytes reach the sink, not the directory-shaped string used to name it. Git membership does not make an ordinary pathname open safe, and checking a stored file type does not justify later reading a mutable checkout path.

The stronger design uses the stored blob for checkpoint content and the established anchored reader for live workspace content. It also keeps read and write claims separate: preventing outside-root restore writes does not prevent outside-root preview reads.

## Repeat next time

- Inventory diff, preview, rollback, export, and manifest-backed readers alongside mutation routes.
- Trace `listed entry -> type decision -> actual content source -> response or destination`; mark every ordinary pathname reopen.
- Exercise checkpoint links and workspace links independently with harmless outside-root markers.
- Swap a committed regular worktree file to a symlink and confirm the operation still uses the intended stored content.
- Pair denial assertions with a regular-content control, and distinguish absent response bytes from absent write side effects.
- State how lower-trust content reaches the checkpoint before making a broader remote-exploit claim.

## Vault redirect

The private research system already retains this rule in its Path Safety Review checklist: checkpoint, rollback, diff, preview, and manifest-backed reads are content sinks; classify entries and prefer blob-backed or anchored no-follow reads over trust in index membership. Its object-binding rule also covers paths swapped after an earlier check.

This case applies those existing checks rather than creating a duplicate lesson. The public PR remains the evidence anchor; private finding details and unrelated disclosure records are not reproduced here.
