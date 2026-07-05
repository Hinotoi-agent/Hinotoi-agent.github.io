---
layout: post
title: "Case study: approval replay must not rewrite the caller"
date: 2026-07-05 21:00:00 +0000
permalink: /2026/07/06/ai-security-case-study-approval-replay-caller-context/
takeaway: "An approval queue should authorize the original scoped request, not replay it as a broader host action."
categories: [case-study, ai-security]
tags: [case-study, approval, caller-context, confused-deputy, agent-control-plane, cli-dispatch, oss-hardening]
---

Approval systems are easy to review too narrowly. The click path may be correct while the replay path quietly changes the actor that reaches the command sink.

This case study is based on the public fix in [`nanocoai/nanoclaw #2611`](https://github.com/nanocoai/nanoclaw/pull/2611). The reusable boundary is approval replay: pending work must preserve the caller context that downstream policy and handlers use.

## Signal

A security PR fixed caller-context loss in an approval-gated CLI replay path:

- PR: [`nanocoai/nanoclaw #2611`](https://github.com/nanocoai/nanoclaw/pull/2611) — `[security] fix(cli): preserve caller context after approval`.
- Merge commit: `05dc1b0a3cac085a568b1608bfd69a919b5d7239`.
- Changed files: `src/cli/dispatch.ts`, `src/cli/dispatch.test.ts`.

The issue is not an unauthorized approval-click bypass. The narrower problem is identity drift after legitimate approval: a command that entered as an agent-scoped request could be replayed with host caller semantics.

## Threat model

The lower-trust actor is an agent/container-originated `ncl` command. It reaches the CLI dispatcher with caller context such as `caller: agent`, `sessionId`, `agentGroupId`, and `messagingGroupId`.

The higher-trust machinery is the approval queue and replay handler. Approval is allowed to resume the requested action, but it should not change the actor, session, group, or scope that the command handler sees after replay.

The security-sensitive assumption is simple: if a handler branches on `ctx.caller`, session, or group fields, those fields are part of the authorization boundary and must survive the delayed handoff.

## Finding and PR

Public PR: [`nanocoai/nanoclaw #2611`](https://github.com/nanocoai/nanoclaw/pull/2611).

Before the fix, approval-gated commands stored the request frame but not the original `CallerContext`. When the approval handler replayed the approved frame, it reconstructed the caller as `{ caller: 'host' }`.

That created a confused-deputy shape. The approver reviewed an agent-originated command, but the final command handler could receive host caller context. Any command whose behavior differs for agent versus host callers could become broader after approval than it was before approval.

## Exploit path

The public PR describes the vulnerable chain as:

```text
container-originated ncl request
    -> dispatch() receives caller: agent with session/group context
        -> approval-gated command stores only the request frame
            -> approval handler replays the frame as caller: host
                -> handler can take broader host behavior after approval
```

The source is the agent-originated CLI request. The carrier is the approval payload that serializes pending work. The transform is replay after approval. The policy decision and sink are the command dispatch and handler behavior that branch on caller/session/group context.

The important failure is at the carrier/transform boundary: the approval payload preserved the command text but not the actor proof. Once replay defaulted to host, the sink no longer saw the same principal that submitted the original request.

## Mitigation

The fix preserves caller identity through the approval queue:

- approval payloads now include the request frame and original caller context;
- replay calls `dispatch(frame, callerContext, { approved: true })` with the preserved context;
- the internal `approved` option prevents a recursive approval loop without skipping normal scope checks;
- legacy pending approvals without `callerContext` keep a host fallback for compatibility.

That trade-off is the right shape for maintainer-friendly hardening: secure new approval payloads, avoid breaking old pending state, and keep replay inside the normal dispatcher rather than creating a special privileged path.

## Verification

The PR added regression coverage in `src/cli/dispatch.test.ts`. The key proof shape is sink-shaped:

- register an approval-gated CLI command whose handler records the `CallerContext` it receives;
- dispatch it as an agent with session and group context;
- invoke the registered `cli_command` approval handler;
- assert the final handler receives the original agent context, not `{ caller: 'host' }`;
- assert approved replay does not queue a second approval prompt.

The PR validation listed these commands:

- `corepack pnpm exec vitest run src/cli/dispatch.test.ts --reporter=verbose`
- `corepack pnpm exec vitest run src/cli/dispatch.test.ts --reporter=dot`
- `corepack pnpm run typecheck`
- `corepack pnpm exec eslint src/cli/dispatch.ts src/cli/dispatch.test.ts`
- `corepack pnpm test -- --run`
- `corepack pnpm exec prettier --check src/cli/dispatch.ts src/cli/dispatch.test.ts`
- `git diff --check`

The negative proof is that approved replay no longer reaches the handler as host when the original request came from an agent. The positive compatibility path is that host-originated or legacy approval payloads without stored caller context remain bounded by the explicit fallback.

## What was learned

Approval is not only a user-interface event. It is a stateful authorization handoff. The queue owns the identity evidence needed by the replayed action.

For AI-agent, MCP, workflow, and CLI control planes, the review should follow the full chain: original actor, approval payload, replay transform, policy decision, and sink-side effect. If the payload does not carry the actor fields that the sink uses, the replay path may be rebuilding authority from local defaults.

The small implementation detail matters: an `approved` marker should suppress another prompt, not suppress authorization or rewrite the caller. Replay should re-enter the normal dispatcher with the original context intact.

## Repeat next time

- For approval-gated actions, map `source -> approval payload -> replay -> policy decision -> sink` before accepting the boundary.
- Compare the pending-approval schema with every identity field used after replay: caller, session, group, tenant, target, and capability.
- Add a regression where a lower-trust caller receives approval but the sink still sees the lower-trust context.
- Assert absence of sink-side widening, not only that an approval prompt appeared.
- Keep compatibility fallbacks explicit, narrow, and tested so legacy state does not define the new security model.

## Vault redirect

The public-safe lesson routes back to `06 - Lessons/Takeaway - Approval replay must preserve original caller context.md` in the OSS vulnerability research vault.

The reusable vault rule is to treat approval replay as an identity-preserving state transition. Detailed private notes, if any, stay in the vault. The public artifact is the boundary pattern, the public PR, and the verification shape.
