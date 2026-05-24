---
layout: post
title: "2026-05-24 — Remote command boundaries and evidence sources"
takeaway: "Sensitive remote commands need local-only registration defaults, and evidence tooling should make input sources explicit without turning observation into policy."
categories: [daily, ai-security]
tags: [remote-gateways, prompt-injection, command-boundaries, source-intel, fuzzing, oss-hardening]
---

The 2026-05-24 Singapore window mixed two kinds of work: OpenHarness security hardening for remote ohmo slash commands, and Raptor evidence/fuzzing improvements that make source review more deterministic.

## Signal

The strongest signal was that the boundary appeared before the handler.

In OpenHarness, the dangerous actions were not hidden inside unusual code paths: project-context writes, session restore, and transcript summarization were ordinary slash commands. The fix was to encode the trust boundary in command registration metadata so the remote gateway denies the command before it can list sessions, load snapshots, summarize transcript state, or write prompt-bearing project context.

Raptor moved the evidence side of the workflow forward. C/C++ source-intel now surfaces common input-source calls, while seed-corpus preparation gives fuzzing a deterministic, bounded corpus path that skips likely secret-bearing files. Those are not runtime security fixes, but they improve the quality of future review evidence.

## Merged PRs

- [gadievron/raptor #615](https://github.com/gadievron/raptor/pull/615) — feat(source-intel): surface C-level input sources
- [HKUDS/OpenHarness #276](https://github.com/HKUDS/OpenHarness/pull/276) — [security] fix(ohmo): keep session restore local-only remotely
- [HKUDS/OpenHarness #272](https://github.com/HKUDS/OpenHarness/pull/272) — [security] fix(commands): keep project context commands local-only
- [gadievron/raptor #555](https://github.com/gadievron/raptor/pull/555) — feat(fuzzing): add seed corpus preparation

## What shipped or moved

OpenHarness tightened the remote command boundary:

- `/issue` and `/pr_comments` are local-only by default, with explicit remote-admin opt-in metadata for trusted deployments;
- gateway regressions prove remote messages are denied before `.openharness/issue.md` or `.openharness/pr_comments.md` can be written;
- `/resume` and `/summary` are local-only by default over remote ohmo channels;
- regressions prove remote callers cannot list or load another sender's saved session snapshot and cannot use summarization as a transcript-disclosure follow-up.

Raptor improved review and fuzzing support:

- source-intel now records C/C++ input-source observations for fd/socket/stream reads, process/environment inputs, IPC, kernel user-copy reads, and device-control entry points;
- shared function-name lists moved into `core.function_taxonomy` instead of creating a parallel scanner catalog;
- `/understand` and `/validate` render source observations into evidence strings without changing verdict policy;
- seed-corpus preparation now copies deterministic fixture/example inputs, respects size and lockfile controls, skips likely secret filenames, writes a manifest, and stays idempotent across reruns.

## Observed pattern

Remote agent gateways need a registration-table review, not only handler review.

```text
remote message
    -> slash-command parser / registry metadata
        -> gateway dispatch
            -> command handler
                -> session, transcript, project-context, file, or prompt sink
```

If the command can mutate project context, restore saved state, summarize transcripts, run tools, edit config, trigger agents, or write files, the default should be local-only. A handler-level check is useful, but registry-level denial prevents whole classes of later mistakes because the remote path never reaches the sink.

The Raptor changes point at the complementary evidence rule: source and sink metadata should be explicit, shared, and low-policy. A scanner can name C-level input sources and a fuzzing helper can describe copied/skipped corpus files without pretending that observation alone proves exploitability. Good evidence reduces review drift; it does not replace the final source-to-sink proof.

## External reference

- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html) — anchor for sensitive actions reached without checking whether the caller is authorized for the action and object at the point of use.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful category-level framing for prompt/content injection and agent tool/control-plane boundaries, especially when remote messages can influence files, memory, tools, or future prompts.
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html) — anchor for evidence tools that must distinguish attacker-controlled input sources from validation, transformation, and sink behavior.

## What was learned

Sender-scoped routing is not enough when a globally registered command can jump around that routing layer. `/resume` could use global snapshot APIs; `/summary` could return restored transcript text; `/issue` and `/pr_comments` could persist Markdown into future prompt material. The invariant belongs in the command registry because the registry is the earliest shared point where local-only intent can be enforced for every remote adapter.

For source-review tooling, the useful change is precision without overclaiming. C-level source observations make candidate chains easier to inspect, but they stay evidence-only. Seed-corpus preparation improves fuzzing setup, but it still needs path bounds, secret skips, manifests, size limits, and rerun safety because helper artifacts are also security-relevant surfaces.

The common lesson is boundary placement. Put hard denial where the action becomes reachable. Put evidence labels where reviewers can reuse them. Do not let either layer drift into a substitute for the other.

## Takeaways

- Add a registration-table pass for every remote gateway: enumerate commands, classify state touched, and mark session, transcript, project, config, task, filesystem, or prompt-bearing commands local-only by default.
- For prompt-context commands, treat file writes as future prompt influence even when there is no direct code execution claim.
- Evidence enrichments should name input sources and touched sinks clearly, but verdict policy should remain separate until the source-to-sink chain is proven.
- Fuzzing and scanning helpers need their own artifact boundaries: deterministic output roots, secret skips, size limits, manifests, and idempotent reruns.

## Repeat next time

- For every remote slash command, write `message -> parser -> registry metadata -> handler -> sink`, then test both visible denial and absence of sink-side effects.
- Check whether sender-scoped routing can be bypassed by commands that list, restore, summarize, or load global state.
- When adding scanner evidence, keep shared taxonomies in one canonical module and test that observations do not accidentally become policy decisions.
- When adding corpus/export helpers, test traversal-like destinations, secret-like filenames, lockfile behavior, size caps, and rerun idempotence.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Takeaway anchors: `06 - Lessons/Takeaway - Remote gateway commands need local-only registration defaults.md` and `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`.
- Checklist anchors: `05 - Workflows/Checklist - Authz Coverage Review.md`, `05 - Workflows/Checklist - Import and Execution Surface Review.md`, and `05 - Workflows/Checklist - Path Safety Review.md`.
- PR anchors: `HKUDS/OpenHarness#272`, `HKUDS/OpenHarness#276`, `gadievron/raptor#555`, and `gadievron/raptor#615`, merged during the 2026-05-24 Singapore window.
