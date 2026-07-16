---
layout: post
title: "2026-07-16 — Actor proof needs a durable owner"
date: 2026-07-16 23:59:00 +0800
takeaway: "A review heuristic becomes operational only when its canonical vault note states the proof required to kill or deepen the next candidate."
categories: [daily, ai-security]
tags: [actor-proof, authorization, vault-backed-learning, candidate-contract, agent-control-plane, oss-hardening]
---

The 2026-07-16 Singapore window had no merged PRs. The useful movement was the writeback boundary: the actor/scope-proof rule from the previous day's tooling change was committed to its canonical vault takeaway.

That closes a small but important loop. The public post explains the method, while the vault tells the next review exactly what evidence to require.

## Signal

No PR merged during `2026-07-16T00:00:00+08:00` through `2026-07-17T00:00:00+08:00`.

The target-window movement was in the research system:

- the actor/scope-proof contract was written into the existing approval-replay takeaway;
- the note now distinguishes request carriers from server-derived actor and scope evidence;
- the rule includes both outcomes: kill carrier-only candidates, and deepen candidates where identity can detach during replay or handoff;
- no target-window record needed to be added to the merged-PR archive.

## Merged PRs

None in this window.

## What shipped or moved

No code, documentation, or security PR merged in the closed target window.

What moved was the durable review rule in `Takeaway - Approval replay must preserve original caller context`. The vault writeback names `Origin`, loopback peer IP, request headers, idempotency keys, approval payloads, and resume tokens as carriers or constraints—not actor proof by themselves.

The operational question is now explicit: **which server-derived fact binds this request to the actor, tenant, session, workspace, capability, or target scope enforced at the sink?**

This is narrower than creating another authorization checklist. The existing takeaway already owns identity preservation across approval, replay, and resume boundaries, so the new contract was folded into that note rather than split into a website-only rule.

## Observed pattern

Security lessons decay when their evidence requirement remains implicit:

```text
public observation or merged fix
  -> smallest canonical vault owner
  -> explicit proof field
  -> candidate kill/deepen decision
  -> focused validation at the action sink
```

For agent, MCP, tool, workflow, and approval surfaces, possession of a carrier may establish that a request exists without establishing whose authority it should inherit. The review needs the binding step between the carrier and the principal used by policy. If that step is sound, stop. If it is missing, caller-controlled, replayable, or widened after a stateful handoff, follow the path to the sink.

## External reference

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — an anchor for validating permissions on every request and relying on trusted authorization attributes.
- [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) — an anchor for keeping authorization bound to the intended operation rather than treating an earlier approval event as ambient authority.

These references anchor the method; they are not copied content. The vault change makes the method testable by requiring the principal-binding evidence before a candidate is promoted.

## What was learned

Reverse-routing is not clerical cleanup. It is where a public observation becomes a reusable review decision.

The important part of the writeback is not the phrase `actor_or_scope_proof` by itself. It is the paired stop condition. A candidate that only names a header, local address, token, or serialized approval object should not consume broad review time. A candidate becomes stronger when it can show that this carrier is substituted for server-derived identity, survives outside its intended scope, or causes a narrower request to execute with wider authority.

This keeps AI-assisted review compact. The context packet needs the carrier, principal derivation, policy decision, and sink—not an unbounded history of authorization prose.

## Takeaways

- A public security observation is not durable until the canonical research note states how it changes the next review.
- Request carriers can constrain context without proving the actor or scope authorized at the sink.
- Every actor-proof heuristic needs a stop condition for weak candidates and an escalation condition for real identity detachment.
- Update the smallest existing vault owner instead of creating a parallel checklist or website-only memory.

## Repeat next time

- Map `carrier -> server-derived principal -> scope decision -> sink` before promoting an authorization candidate.
- Kill the candidate when it cannot identify a lower-trust actor, a scope crossing, and the trusted fact being bypassed.
- Deepen it when replay, resume, approval, proxying, or caching can detach the carrier from the original principal.
- Prove denial and absence of sink-side effects for the lower-trust path, then preserve one intended compatibility path.

## Vault redirect

- Canonical owner: `06 - Lessons/Takeaway - Approval replay must preserve original caller context.md`, committed during the target window with the actor/scope-proof contract.
- Workflow anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Workflow - OSS Review Loop.md`.
- Public site role: this post records the closed window and public-safe method. The vault remains the system of record for the proof contract and future review changes.