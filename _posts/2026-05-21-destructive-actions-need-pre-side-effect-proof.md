---
layout: post
title: "2026-05-21 — Destructive actions need pre-side-effect proof"
takeaway: "Cleanup, reset, overwrite, and extraction paths need evidence that validation happens immediately before the side effect and that unsafe inputs are denied without touching existing data."
categories: [daily, ai-security]
tags: [verifymate, destructive-actions, path-safety, evidence, oss-hardening]
---

The 2026-05-21 Singapore window had one merged PR in `Hinotoi-agent/Verifymate`. The change tightened the evidence gate for reports that involve destructive filesystem or artifact operations.

## Signal

The useful signal was destructive-action proof quality.

Security reports around cleanup, reset, archive extraction, generated artifacts, and output directories can look convincing while still missing the part that matters: the moment just before deletion, overwrite, reset, or extraction happens.

For AI-security and OSS-hardening work, this boundary appears often. Agent sandboxes create workspaces. MCP or tool fixtures write generated output. Parser and upload paths unpack archives. Review tooling deletes and rewrites artifacts. If the report does not prove validation at the side-effect point, the claim can overstate both safety and exploitability.

## Merged PRs

- [Hinotoi-agent/Verifymate #8](https://github.com/Hinotoi-agent/Verifymate/pull/8) — feat: check destructive action safety evidence

## What shipped or moved

Verifymate gained an `operator_safety` / `destructive_action_safety` checklist row for security-review drafts that mention cleanup, reset, archive extraction, seed corpora, generated artifacts, or output directories.

The new gate asks whether the draft shows:

- validation before recursive delete, reset, overwrite, extraction, or similar side effects;
- source/input and output path invariants;
- regression proof that unsafe paths are rejected without deleting existing operator or project data;
- positive proof that valid dedicated output directories still work when that compatibility path matters.

The check is report-scoped rather than name-scoped. Ordinary helper names such as `cleanup_cache()` should not make unrelated findings non-fileable by themselves. The evidence requirement should activate when the report's actual claim involves destructive or operator-data-risking behavior.

## Observed pattern

Destructive actions need a source-to-sink proof that includes the pre-side-effect boundary.

```text
input or source path
    -> resolver / validator
        -> recursive delete, reset, overwrite, or extraction sink
            -> existing operator or project data at risk
```

The weak version proves only that a path was checked somewhere earlier. The stronger version proves the object acted on by the destructive sink is the object that was validated, and that denial happens before any partial side effect.

This is the same sink-boundary lesson as path traversal, archive extraction, upload writes, and agent workspace cleanup, but with a sharper evidence requirement: a safe negative test must preserve existing data, not merely return an error after damage could already have happened.

## External reference

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) — a public anchor for traversal and containment failures when path-like input crosses into filesystem operations.
- [CWE-59: Improper Link Resolution Before File Access](https://cwe.mitre.org/data/definitions/59.html) — useful for symlink and object-substitution cases where a checked path is not necessarily the object later modified or deleted.
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) — a practical reference for treating filenames, storage locations, and file operations as separate validation boundaries rather than one generic input check.

## What was learned

A destructive-path report is incomplete if it stops at intent.

It is not enough to say an output directory is dedicated, an extraction root is expected, or a cleanup helper should operate on generated files. The review needs evidence at the action sink: what exact path or object is about to be deleted, overwritten, reset, or extracted, and which invariant is enforced immediately before that happens.

The same rule improves false-positive control. If a draft mentions a cleanup helper but cannot show attacker control, reachable destructive behavior, or existing data at risk, Verifymate should keep the reviewer focused on those missing segments rather than letting the report become broad and vague.

## Takeaways

- Treat destructive helpers as action sinks: recursive delete, reset, overwrite, extraction, and generated-artifact writes all need final-object proof.
- Negative regressions should prove absence of side effects, especially that existing operator or project data remains untouched after an unsafe input is denied.
- Positive regressions still matter when the secure fix preserves a legitimate dedicated output directory or dry-run workflow.
- Evidence gates should be scoped to the report's claim, not triggered by incidental helper names that do not participate in the finding.

## Repeat next time

- For cleanup, reset, archive, and output-directory findings, write the chain as `input/source path -> resolver/validator -> destructive sink -> data at risk` before drafting the PR or advisory.
- Add denial tests for traversal, symlink, sibling-prefix, absolute-path, and recomputed-path cases where they fit the codebase.
- Assert both the visible denial and the absence of sink-side effects: no deletion, no overwrite, no extraction outside the root, and no mutation of pre-existing operator data.
- Route reusable evidence-gate lessons back into the vault checklist or takeaway layer before publishing the public synthesis.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchors: `05 - Workflows/Checklist - Path Safety Review.md` and Verifymate's destructive-action safety gate.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, updated with the destructive-action evidence variant.
- PR anchor: `Hinotoi-agent/Verifymate#8`, merged 2026-05-21 Singapore time.
