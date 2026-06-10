---
layout: post
title: "2026-06-10 — Host-side actions need object-bound proof"
takeaway: "Agent security fixes are strongest when the trusted host rechecks the real object and actor at the exact sink: filesystem entries before copy, responder identity before approval resolution."
categories: [daily, ai-security]
tags: [agent-security, host-boundary, symlink-safety, approval-authz, object-validation, oss-hardening]
---

The 2026-06-10 Singapore window shipped two NanoClaw hardening PRs. Both were about the same quiet boundary: a safe-looking token is not the security decision when the host is about to act.

One fix moved attachment forwarding from filename trust to filesystem-object proof. The other moved approval handling from `questionId` trust to responder-role proof. Different surfaces, same invariant: validate the thing that will be used by the sink, immediately before the sink runs.

## Signal

Two agent/control-plane paths were tightened in the closed Singapore window `[2026-06-10 00:00, 2026-06-11 00:00)`:

```text
agent-controlled outbox name
    -> host-side copy
    -> lstat / realpath / containment before bytes move

approval callback questionId
    -> privileged approval resolver
    -> responder role check before handler dispatch
```

The useful signal is not just that both PRs merged. It is that both fixes put the boundary at the host-side action point instead of trusting earlier shape checks.

## Merged PRs

- [nanocoai/nanoclaw #2478](https://github.com/nanocoai/nanoclaw/pull/2478) — `[security] fix(approvals): require admin for approval responses` (merged 2026-06-10 03:29:08 SGT)
- [nanocoai/nanoclaw #2468](https://github.com/nanocoai/nanoclaw/pull/2468) — `[security] fix(agent-route): reject unsafe forwarded attachments` (merged 2026-06-10 03:29:04 SGT)

## What shipped or moved

The attachment-forwarding PR hardened `src/modules/agent-to-agent/agent-route.ts` and its regression test. The forwarding path now validates the source message outbox id, rejects symlinked or non-directory outboxes, rejects symlinked or non-regular source attachments, resolves the source file with `realpathSync`, and requires it to stay inside the resolved source outbox before `copyFileSync` can move bytes into another agent inbox.

The approval-response PR hardened `src/modules/approvals/response-handler.ts` and its regression test. A pending approval can no longer be resolved only because a valid `questionId` was supplied. The responder identity is normalized into the same namespaced format used by the permissions layer, then checked as owner, global admin, or scoped group admin before OneCLI or registered module approval handlers run. Unauthorized clicks are ignored without consuming the pending approval.

The merged-PR data archive was updated with both entries in local merge-time order.

## Observed pattern

Agent systems often split authority across a less-trusted runtime and a trusted host/control plane. That split creates misleading intermediate values:

- a basename that passes a string safety check;
- an outbox directory that looks like a message container;
- an approval id that resolves to a pending privileged action;
- a callback payload that carries user context but has not been bound to role authority.

Those values are not the boundary. The boundary is the host-side primitive that moves bytes, mutates state, dispatches a handler, or approves privileged work.

For file forwarding, the proof needs to bind the final filesystem object: no symlink, regular file only, canonical containment under the real outbox, then copy. For approvals, the proof needs to bind the final actor: normalized responder id, server-side role check, then resolver dispatch.

## External reference

- [CWE-59: Improper Link Resolution Before File Access](https://cwe.mitre.org/data/definitions/59.html) — useful anchor for the symlink-follow part of agent-to-agent forwarding. The review method is to validate the filesystem object, not only the string that names it.
- [CWE-862: Missing Authorization](https://cwe.mitre.org/data/definitions/862.html) — useful anchor for approval callbacks. Possession of an action identifier is not authorization to resolve the action.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — maps the broader agent lesson: tool, file, approval, and control-plane actions need server-side enforcement where model-adjacent or user-adjacent input reaches host authority.

## What was learned

The two fixes make the same review habit more concrete: do not stop at a syntactic allowlist or a lookup success. Ask what trusted primitive executes next, then require the proof at that primitive.

For path and attachment review, a basename check is only the first gate. If the source directory is writable by a sandbox, container, plugin, or agent, the directory entry itself is attacker-controlled. The host must inspect the object it is about to read or copy, and the regression should prove the sensitive bytes do not move.

For approval and callback review, a valid id is only a routing key. If the next step resolves a privileged action, the callback responder must be authorized at the resolver/handler boundary. The regression should prove both denial and absence of side effects: the handler is not called, the privileged action is not accepted, and the pending legitimate approval is preserved.

## Takeaways

- Host-side file copy is a security sink when the source directory is writable by an agent, container, plugin, or sandbox.
- Approval ids, question ids, task ids, and callback ids are routing handles, not authorization decisions.
- For agent/control-plane reviews, bind both dimensions before the action: the real object being acted on and the real actor requesting the action.
- Negative tests should assert absence of sink-side effects, not only a safe-looking error path.

## Repeat next time

- For every agent file bridge, trace `name -> directory entry -> real object -> host primitive -> destination` and add symlink, non-regular, containment, and positive regular-file tests.
- For every approval/callback path, trace `id -> pending action -> responder identity -> role check -> handler dispatch` and test unauthorized, scoped-admin, owner, and global-admin cases.
- Compare sibling paths that reimplement the same boundary. A fix in one outbox or approval route does not automatically protect another route that performs its own copy or dispatch.
- Keep public writeups at the invariant level: no exploit specifics beyond what the merged PRs already disclose, no credentials, and no private report details.

## Vault redirect

- Primary takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, updated with the 2026-06-10 object-and-actor binding rule.
- Authz anchor: `06 - Lessons/Takeaway - Host delivery actions must authorize at mutation point.md` and `05 - Workflows/Checklist - Authz Coverage Review.md`.
- Path anchor: `05 - Workflows/Checklist - Path Safety Review.md`.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
