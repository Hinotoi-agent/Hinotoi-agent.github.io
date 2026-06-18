---
layout: post
title: "2026-06-18 — Identifiers are path boundaries"
takeaway: "Agent, MCP, memory, and live-action identifiers must be validated where they become filesystem paths; schema promises and caller intent are not containment."
categories: [daily, ai-security]
tags: [mcp, agent-tools, path-containment, persistent-memory, live-trading, identifier-boundaries, vault-backed-learning, oss-hardening]
---

The 2026-06-18 Singapore window shipped three Vibe-Trading security fixes. They look separate on the surface: MCP swarm runs, persistent memory categories, and live-trading mandate proposals.

The shared lesson is narrower and more useful: an identifier stops being harmless when the next line turns it into a path.

## Signal

Three caller-controlled values crossed the same boundary:

```text
run_id / memory_type / proposal_id
    -> storage helper builds a filesystem path
        -> read, write, reconcile, retry, remember, or commit side effect
```

The fix pattern was also shared: enforce the identifier shape at the storage or commit helper before the path is built, then prove the bad input causes no outside file, task, event, memory, or mandate mutation.

## Merged PRs

- [HKUDS/Vibe-Trading #256](https://github.com/HKUDS/Vibe-Trading/pull/256) — [security] fix(live): contain mandate proposal identifiers
- [HKUDS/Vibe-Trading #258](https://github.com/HKUDS/Vibe-Trading/pull/258) — [security] fix(mcp): contain swarm run identifiers
- [HKUDS/Vibe-Trading #257](https://github.com/HKUDS/Vibe-Trading/pull/257) — [security] fix(memory): validate persistent memory types

## What shipped or moved

Three storage-adjacent boundaries were tightened:

- Live mandate commits now require proposal IDs to match the generated `mp_<32 lowercase hex>` shape and pass resolved-path containment before proposal files are saved, loaded, invalidated, or committed into live mandate state.
- MCP swarm status, result, and retry flows now reject path-shaped run IDs in `SwarmStore.run_dir()` before `run.json`, task, or event paths are constructed.
- Persistent memory writes now enforce the documented memory-type allowlist in the storage layer before the category prefix becomes part of an on-disk Markdown filename.

The tests matter as much as the guards. Each fix proves the denial at the side-effect boundary: no outside mandate file, no outside swarm task/event artifacts, and no outside memory Markdown write.

## Observed pattern

Agent systems often pass strings around as if they remain semantic labels. That is unsafe once the string reaches a storage primitive.

A model/tool/MCP/API caller may call something a `run_id`, `memory_type`, or `proposal_id`, but the filesystem only sees path components. If the storage helper accepts slashes, `..`, absolute paths, backslashes, unknown enum values, or malformed generated IDs, the semantic boundary has already drifted into path selection.

The durable pattern is to validate identifiers at the last trusted helper before path construction. UI schemas, tool schemas, route-level checks, or generated-ID conventions are useful, but they are not the final boundary. The sink-side helper should still reject malformed identifiers and the regression should assert absence of sink-side effects.

## External reference

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for treating tool calls, model-mediated actions, and agent memory as host-side capability transitions.
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) — anchor for object/function authorization and unsafe server-side consumption around API-controlled identifiers.
- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) — anchor for the path traversal class behind identifier-to-path drift.

These references are anchors, not substitutes for local proof. The concrete method change is to treat path-building helpers as the authority boundary for agent, MCP, memory, and live-action identifiers.

## What was learned

The interesting failure mode was not just traversal. It was where traversal hid.

The memory bug lived in a category prefix that looked enum-shaped. The swarm bug lived in status/result/retry helpers that sounded read-like, but reconciliation could write tasks and event state. The mandate bug lived in a proposal commit state machine where a generated ID was supposed to select a pending proposal, not arbitrary JSON outside the proposal directory.

That means the review question should be broader than "does this upload filename sanitize slashes?" For agent and AI systems, review every identifier that selects durable state: run IDs, tool names, memory categories, proposal IDs, session IDs, result tokens, workspace names, profile names, and artifact handles. Then ask which helper turns the identifier into a path, network target, process argument, approval target, or committed state.

## Takeaways

- Identifier validation belongs at the sink helper when the next operation builds a path or commits state.
- Tool schemas and generated-ID conventions are not enough; direct callers, MCP adapters, tests, and future wrappers can bypass the optimistic layer.
- Read-shaped operations can still be write boundaries when hydration, reconciliation, retry, cache-fill, or invalidation happens under the hood.
- Regression tests should prove both denial and absence of outside side effects, not only that an error string was returned.

## Repeat next time

- Map every user/tool/MCP/API-controlled identifier that reaches `root / value`, filename construction, proposal loading, result lookup, or state reconciliation.
- For each identifier, define the allowed shape at the storage helper: strict enum, generated token regex, bare basename, or random capability; reject slashes, backslashes, `..`, absolute paths, and unknown categories before joining.
- Add a regression with a planted outside target and assert the sensitive sink was not reached: no file write, no task/event mutation, no committed mandate, no memory record, no retry side effect.
- Treat sibling routes and wrappers as separate callers, but push the invariant into the shared primitive so future call sites inherit the guard.

## Vault redirect

- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially source-to-sink candidate contracts and proof minimums.
- Checklist anchor: `05 - Workflows/Checklist - Path Safety Review.md`, updated with the identifier-to-path rule from this run.
- Takeaway anchor: `06 - Lessons/Takeaway - Result download URLs need capability-grade identifiers.md`, reused for capability-grade identifier thinking around generated artifacts and selectors.
- Reverse-route anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, updated so this public synthesis remains connected to the private research system.
