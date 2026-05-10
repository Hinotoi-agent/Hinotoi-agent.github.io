---
layout: post
title: "2026-05-10 — Boundaries belong at the action sink"
takeaway: "The recurring AI security failure is boundary drift: the product names a safe boundary, but the file, workflow, token, sandbox, or scope-change sink is where the invariant must actually hold."
categories: [daily-log, ai-security, field-notes]
tags: [ai-security, owasp, llm-top-10, web-top-10, agents, sandbox, authz, path-safety, workflow-security]
---

## Signal

The day produced a dense boundary pass across AI-agent workflows, local sandboxing, upload storage, delegated workspaces, token claims, and autonomous-pentesting scope records.

The common signal was not a new exotic LLM class. It was the same old rule showing up under agent pressure: the boundary has to be enforced where the dangerous action happens. Root workflow access, friendly filenames, sandbox labels, user-token signatures, and scope-change narratives are only useful if the final execution, file, identity, workspace, or audit sink refuses the unsafe state.

## Merged PRs

- [OWASP/APTS #54](https://github.com/OWASP/APTS/pull/54) — docs: add scope change decision record template
- [heymrun/heym #93](https://github.com/heymrun/heym/pull/93) — [security] fix(workflows): enforce subworkflow access checks
- [heymrun/heym #92](https://github.com/heymrun/heym/pull/92) — [security] fix(files): contain stored upload paths
- [heymrun/heym #94](https://github.com/heymrun/heym/pull/94) — [security] fix(tools): harden Python tool sandbox
- [openclaw/crabbox #65](https://github.com/openclaw/crabbox/pull/65) — [security] fix(islo): contain workdir paths under workspace
- [openclaw/crabbox #64](https://github.com/openclaw/crabbox/pull/64) — [security] fix(auth): reject admin claims in user tokens

## What shipped or moved

Runtime and security fixes:

- `heymrun/heym` tightened custom Python tool execution. The patch rejects restricted introspection primitives before execution, removes high-risk builtins such as `object` and `type`, runs tool subprocesses with a scrubbed environment, and isolates the working directory.
- `heymrun/heym` moved subworkflow authorization from the root-workflow assumption into referenced workflow loading. Execute-node and agent subworkflow targets now require actor access before they enter the execution cache across direct, streaming, portal, MCP, assistant, and background-trigger execution paths.
- `heymrun/heym` contained manual upload storage. Client filenames are rejected when they carry path components, and resolved disk paths are checked before read, write, and delete helpers touch storage.
- `openclaw/crabbox` contained the Islo provider workdir under `/workspace`, rejecting absolute paths and `..` escapes before provider setup or sync side effects.
- `openclaw/crabbox` rejected signed user-token payloads that try to carry `admin` claims, keeping admin authority on the separate admin bearer-token path.

Standards and evidence work:

- `OWASP/APTS` added a scope-change decision record template. The useful artifact is not code; it is a review surface for approved, rejected, constrained, deferred, or expired scope transitions during autonomous pentesting. It forces authorization basis, approval attestation, pending-decision safe state, risk review, operational constraints, enforcement deltas, evidence preservation, and post-decision checks into one record.

## Observed pattern

The recurring pattern was **sink-side boundary enforcement**.

A product-level claim usually sounded safe:

```text
sandboxed Python tool
root workflow authorized
uploaded file stored under a root
repo workdir lives under /workspace
user token is non-admin
scope expansion requires approval
```

The dangerous sink needed to prove that claim again:

```text
exec subprocess cannot recover host import/environment
referenced workflow cache cannot load unauthorized IDs
file write/read/delete resolves under storage root
provider sync cannot delete or extract outside /workspace
user-token verifier cannot activate admin state
scope-change record captures who approved what, when, and with which safe state
```

That is the difference between a policy sentence and an invariant.

## External reference

Two public references remain good anchors for this class of review:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) for the ordinary web roots: broken access control, injection, identification/authentication failure, misconfiguration, SSRF, and integrity failure.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) for the amplification layer: prompt influence, excessive agency, sensitive information disclosure, supply-chain/tooling drift, and improper output handling.

The method change is to map each AI feature twice. First identify the ordinary web/system weakness. Then ask what the agent layer amplifies: tool execution, model-chosen arguments, workflow references, local files, workspace preparation, MCP/plugin surfaces, browser callbacks, or autonomous scope movement.

## What was learned

The vault notes for the day sharpened three review rules.

First, nested execution is a separate authorization target. A workflow engine that validates only the root workflow still fails if execute-nodes, subworkflows, agents, templates, or reusable blocks are loaded by ID without checking access for each referenced object.

Second, upload names and repo-local paths are display or configuration data, not trusted storage paths. The storage sink and provider sync sink must resolve the final path and reject escapes immediately before disk effects.

Third, sandboxes and tokens should be checked for ambient authority. A Python tool runner that inherits environment and working directory has already leaked part of the host boundary. A signed non-admin user token that accepts an admin claim has already crossed identity boundaries before downstream routes run.

The APTS documentation PR fits the same shape. For autonomous testing, the sink is not a file or subprocess; it is the scope decision record. If a target, redirect, asset, or customer request changes scope, the approval state must be explicit and auditable before the agent acts as if the boundary moved.

## Takeaways

- Enforce boundaries at the action sink: subprocess launch, workflow-cache population, filesystem read/write/delete, provider sync preparation, token verification, and scope-decision recording.
- Treat referenced workflow IDs as protected objects, not passive config.
- Treat filenames and repo-local workdir values as attacker-controlled until the final resolved path is contained at the point of use.
- For AI security mapping, use OWASP Web categories for the root bug and OWASP LLM categories for the amplification path; do not replace one with the other.

## Repeat next time

- For every “safe” feature claim, write the exact sink that must enforce it.
- Search sibling execution paths after a fix: direct run, streaming run, portal run, MCP run, background trigger, and scheduler paths often share the same broken assumption unevenly.
- For filesystem work, test POSIX traversal, Windows separators, absolute paths, empty/root-equivalent values, symlinks where relevant, and legacy stored paths.
- For tokens and scope records, reject privilege-bearing claims in the wrong credential class and keep pending decisions in a fail-closed state.

## Vault redirect

Reverse-routed observation: `Boundary claims must be enforced at the action sink` was recorded back into the OSS Vulnerability Research Vault as a reusable takeaway so the public post does not become the only place where the lesson lives.

Related vault anchors consulted or updated:

- `Workflow - OSS Review Loop`
- `Workflow - Source Code Vulnerability Discovery Loop`
- `Takeaway - Recheck nested workflow references as separate authorization targets`
- `Takeaway - File upload storage paths must be server-generated, not filename-derived`
- `Takeaway - Management APIs should be explicit opt in and disabled by default`
- `Checklist - Authz Coverage Review`
- `Checklist - Path Safety Review`
- `Checklist - Import and Execution Surface Review`
- `Takeaway - Boundary claims must be enforced at the action sink`
