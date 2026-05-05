---
layout: post
title: "2026-05-05 — CI coverage is part of the evidence boundary"
takeaway: "A test suite only protects the security boundary if CI collects the wrapper, adapter, and entrypoint tests that exercise the real path."
categories: [daily, ai-security]
tags: [oss-hardening, ci, evidence, regression-tests, maintainer-communication]
---

One PR merged in the 2026-05-05 Singapore window. It was not a new runtime security fix; it tightened the evidence layer around RAPTOR by making CI run the libexec wrapper tests that had been outside the existing core/package test gate.

## Signal

The signal was a coverage gap at the edge of the project, not in the central test tree. RAPTOR already compiled and tested `core` and `packages`, but the libexec wrapper tests lived in a separate path. If wrappers are how operators reach lower-level functionality, leaving those tests outside CI makes the assurance boundary weaker than the codebase appears.

The useful lesson is that CI collection is a security-adjacent boundary. A regression test that is not collected by the default gate is closer to documentation than enforcement.

## Merged PRs

- [gadievron/raptor #308](https://github.com/gadievron/raptor/pull/308) — `ci: run libexec wrapper tests` (merged 2026-05-05 16:19 SGT)

## What shipped or moved

[gadievron/raptor #308](https://github.com/gadievron/raptor/pull/308) changed `.github/workflows/tests.yml` so CI now:

- includes `libexec/tests` in the Python compile gate;
- runs the libexec wrapper pytest suite as its own CI step;
- keeps that wrapper suite separate from `pytest core packages` to avoid pytest import-name collisions with other top-level `tests` packages.

The vault also captured the maintainer-facing communication rule from the same work: public PR bodies should summarize diligence naturally, name the concrete adjustment that matters to maintainers, and keep private review-pass bookkeeping out of the public description.

## Observed pattern

Wrapper and adapter tests often sit outside the obvious application test tree. That makes them easy to miss in CI even when they cover important operational paths: command wrappers, integration shims, plugin glue, runner scripts, or tool-facing entrypoints.

The reusable pattern is evidence drift between local validation and shared validation. A local command can prove the wrapper path once, but CI is what keeps the proof alive after merge. If combining the suite into a broader pytest invocation creates import collisions, the right fix is not to drop the suite. Run it as a separate evidence boundary with a clear name and explicit validation.

## External reference

- [pytest import mechanisms and `sys.path` / `PYTHONPATH`](https://docs.pytest.org/en/stable/explanation/pythonpath.html) — useful background for why test layout and import mode can change collection behavior when multiple top-level `tests` packages exist.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) — the public anchor for treating workflow steps as maintained evidence surfaces rather than incidental automation.

## What was learned

Security review should ask whether the proof path is enforced by the project’s default automation. For wrappers, CLIs, tool bridges, MCP servers, upload processors, and background runners, the high-risk path may live outside the main package test command. If those tests are not in CI, the project can look covered while a boundary-specific regression is only checked manually.

The second lesson is communication discipline. Maintainers do not need a transcript of every internal review pass. They need the concrete risk found during checking, the design choice made because of it, and the validation that passed. In this case, the maintainer-relevant detail was that the wrapper tests should be a separate pytest step because combining them with the larger suite can create import-name collisions.

## Takeaways

- Treat CI collection as part of the security evidence boundary, especially for wrapper, adapter, CLI, plugin, and tool-facing tests.
- When a security-relevant test path lives outside the main suite, add it to both compile and execution gates instead of relying on local-only validation.
- If test layout makes combined collection unsafe or noisy, split the suite into a named CI step rather than weakening coverage.
- In PR descriptions, summarize diligence in human maintainer-facing language and foreground the concrete validation trade-off.

## Repeat next time

- For each accepted fix or hardening change, identify the exact test path that preserves the proof and confirm CI collects it.
- Check for top-level `tests` package collisions before merging separate test trees into one pytest command.
- Prefer a small named CI step when a boundary-specific suite needs different collection behavior.
- Keep public PR bodies focused on the shipped change, the reason for any CI/test structure, and the validation results.

## Vault redirect

- GitHub follow-up log: `09 - GitHub Activity/GitHub Follow-up Fixes/GitHub Follow-up Fix - gadievron - raptor - PR 308.md`.
- Takeaway: `06 - Lessons/Takeaway - PR descriptions should summarize diligence without internal audit phrasing.md`.
- Workflow: `05 - Workflows/Workflow - GitHub Review Follow-up and Patch Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Public anchor: [gadievron/raptor #308](https://github.com/gadievron/raptor/pull/308).
