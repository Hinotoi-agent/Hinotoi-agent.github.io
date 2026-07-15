---
layout: post
title: "2026-07-15 — Request carriers are not actor proof"
date: 2026-07-15 22:52:47 +0800
takeaway: "A candidate contract should name the server-derived fact that binds a request to the actor and scope authorized at the sink."
categories: [daily, ai-security]
tags: [actor-proof, authorization, candidate-contract, false-positive-gate, agent-control-plane, security-tooling, oss-hardening]
---

The 2026-07-15 Singapore window converted a recurring boundary lesson into a required candidate-contract field. A request can arrive with an origin, peer address, token, approval payload, or reuse key and still lack proof of the actor or scope authorized to reach the sink.

The useful change is small: every generated review candidate must now name its `actor_or_scope_proof`. That makes an implicit authorization assumption visible early enough to kill weak candidates or deepen a real identity-binding gap.

## Signal

One PR merged during `2026-07-15T00:00:00+08:00` through `2026-07-16T00:00:00+08:00`:

- Huntpack added an actor/scope-proof requirement to candidate bundles and compact review prompts.
- The regression test now locks the field into both generated artifacts.
- The reusable signal is that a request carrier reaching a route is not the same as a server-derived principal being authorized for the sink.

## Merged PRs

- [Hinotoi-agent/huntpack #8](https://github.com/Hinotoi-agent/huntpack/pull/8) — Require actor scope proof in candidate contracts. Merged at 22:52 Singapore time; merge commit [`4f64261`](https://github.com/Hinotoi-agent/huntpack/commit/4f64261df835e8e5185d054a9d28178bd270ed89).

## What shipped or moved

The PR added `actor_or_scope_proof` to Huntpack's generated candidate contracts and compact review prompts. It also documented that carriers such as `Origin`, loopback peer IP, request headers, idempotency keys, approval payloads, and resume tokens are not sufficient actor proof by themselves.

The patch touched `huntpack/huntpack.py`, `tests/test_candidate_contract.py`, and `README.md`. Its recorded validation covered Python compilation, CLI help, a workflow smoke run, the complete pytest suite, and an installed-script synchronization check.

This is workflow hardening rather than a new runtime security fix. The output contract now forces a reviewer to state which server-derived identity or scope fact actually governs the action before a candidate is promoted.

## Observed pattern

Authorization claims often collapse a carrier into a principal:

```text
request carrier
  -> route or replay/resume entry
  -> server-side actor and scope derivation
  -> authorization decision
  -> tool / file / network / memory / approval sink
```

The carrier can be security-relevant without being identity proof. Browser `Origin` can constrain request context. A loopback peer address can constrain network location. An approval payload or resume token can preserve state. An idempotency key can identify reusable work. None independently proves which actor, tenant, session, workspace, capability, or target scope the sink should trust.

The review boundary is therefore the binding step between the carrier and the server-derived principal. If that step is missing, replayable, caller-controlled, or reconstructed from a wider default, the route may become a confused deputy. If the binding is sound, a carrier-only hypothesis should be killed before expensive validation.

## External reference

- [Huntpack PR #8](https://github.com/Hinotoi-agent/huntpack/pull/8) — the public patch, changed files, rationale, and validation record.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — an external anchor for validating permissions on every request and enforcing authorization with trusted attributes.

These references anchor the method; they are not copied content. The method change is to require an explicit answer to: **what server-derived fact binds this request to the actor and scope permitted at the sink?**

## What was learned

Candidate quality improves when identity proof is a required field rather than an inference hidden in prose. The field serves two directions at once.

For false-positive control, it exposes candidates that only point to a header, token, local address, or serialized approval object without proving a lower-trust actor can cross a policy boundary. For deeper review, it highlights paths where the server loses identity during queuing, replay, resume, proxying, caching, or tool dispatch and later substitutes host, local, or administrative authority.

This also sharpens evidence budgets. A compact packet should include the carrier, the principal-derivation step, the policy decision, and the sink. If the packet cannot name those anchors, broad model review is unlikely to repair the missing threat model efficiently.

## Takeaways

- A carrier is an input to an authorization decision, not proof of the authorized actor.
- Candidate contracts should name the server-derived actor or scope fact before claiming a boundary bypass.
- Approval, resume, retry, and idempotency objects need identity binding across stateful handoffs; possession alone is not automatically authority.
- A missing actor-proof field is useful both as a false-positive gate and as a signal for confused-deputy review.

## Repeat next time

- Map `carrier -> principal derivation -> scope check -> sink` before promoting an authorization candidate.
- Ask whether the carrier is caller-controlled, replayable, substitutable, or detached from the authenticated principal.
- Compare the scope encoded before a queue/replay/resume boundary with the scope consumed after it.
- Require denial plus absence of sink-side effects for the lower-trust path, and preserve one intended compatibility path.

## Vault redirect

- Canonical takeaway: `06 - Lessons/Takeaway - Approval replay must preserve original caller context.md`, updated with the broader actor/scope-proof contract.
- Workflow anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Workflow - OSS Review Loop.md`.
- Public site role: this post records the public-safe tooling change and review rule. The vault remains the owner of the reusable identity-preservation lesson.
