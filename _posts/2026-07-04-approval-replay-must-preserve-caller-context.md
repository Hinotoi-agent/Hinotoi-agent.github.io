---
layout: post
title: "2026-07-04 — Approval replay must preserve caller context"
takeaway: "An approval click should authorize the original scoped request, not replay it with broader host semantics."
categories: [daily, ai-security]
tags: [merged-pr, approval, caller-context, confused-deputy, agent-control-plane, cli-dispatch, oss-hardening]
---

The 2026-07-04 Singapore window had one merged security PR. The patch tightened an approval replay boundary in `nanocoai/nanoclaw`: an agent-originated CLI command that waits for approval now keeps its original caller context when it is replayed.

The useful lesson is small and sharp. Approval is not only a click. It is a stateful handoff. If the handoff serializes the request but drops the actor, the approved action can come back with a different scope than the one that was reviewed.

## Signal

One security PR merged during `2026-07-04T00:00:00+08:00` through `2026-07-05T00:00:00+08:00`:

- [nanocoai/nanoclaw #2611](https://github.com/nanocoai/nanoclaw/pull/2611) — `[security] fix(cli): preserve caller context after approval`, merged at `2026-07-04T16:08:39+08:00`.

The pre-run day context reported no merged PRs, but a fresh GitHub query found the merge in the target window. `_data/merged_prs.yml` was updated from the direct PR record rather than leaving the archive stale.

## Merged PRs

- [nanocoai/nanoclaw #2611](https://github.com/nanocoai/nanoclaw/pull/2611) — `[security] fix(cli): preserve caller context after approval`.

## What shipped or moved

The PR preserves the original `CallerContext` across an approval-gated CLI replay path.

Before the fix, an agent-originated CLI request could enter dispatch with agent/session/group context, reach an approval gate, and store only the request frame. When the approval handler replayed the command, it reconstructed the caller as `host`. That meant handlers branching on `ctx.caller`, `sessionId`, or group context could see broader host semantics after approval.

After the fix:

- approval payloads store the request frame and the original caller context;
- approved replay re-enters `dispatch()` with the preserved context;
- an internal `approved` dispatch option prevents an approval loop without bypassing scope checks;
- legacy pending approvals without stored caller context retain a host fallback for compatibility;
- regression coverage proves an agent-originated approved command still executes with the agent context.

Touched files were `src/cli/dispatch.ts` and `src/cli/dispatch.test.ts`. The PR body records focused dispatch tests, typecheck, focused ESLint, full Vitest, Prettier, whitespace, and added-line secret scan validation.

## Observed pattern

The recurring pattern is approval replay as an identity-preserving state transition:

```text
agent/container-originated command
    -> dispatcher receives scoped caller context
        -> approval queue serializes request and actor
            -> approval handler replays through normal dispatch
                -> sink sees the original scoped actor, not a widened host actor
```

The vulnerable shape is the same chain with one missing field: the approval payload keeps the command but loses the actor. That turns approval into a confused-deputy boundary. The approver may approve a narrow agent request, while the replay executes as a wider host request.

For agent, MCP, tool, and workflow systems, this is the part to review early: approval queues, resumable actions, pending commands, delayed tool calls, and any path where a lower-trust caller hands work to a higher-trust executor.

## External reference

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for keeping agent/tool authorization tied to concrete action boundaries rather than treating approval UX as the whole control.
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — anchor for testing authorization state across multi-step workflows, including the state that survives redirects, queues, callbacks, and delayed execution.
- [GitHub PR #2611](https://github.com/nanocoai/nanoclaw/pull/2611) — public evidence anchor for the specific merged fix, affected files, bounded impact statement, CVSS assessment, and validation commands.

The method change is narrower than the references: when an approved action is replayed, review the serialized approval payload as a policy boundary. The payload must carry the same actor proof that the sink will use.

## What was learned

Approval should authorize the original requested action. It should not change the identity, session, group, tenant, or capability scope that reaches the sink.

The important distinction is between approval authority and execution identity. A legitimate approver can allow a request to continue, but that does not mean the request should become host-originated. If handlers branch on caller context, the original transport-supplied context is part of the security decision and must survive the queue.

The compatibility trade-off also matters. The patch keeps a host fallback for legacy approval payloads without `callerContext`, while making new payloads preserve the actor. That is the right shape for maintainer-friendly hardening: secure the default path, keep old pending state from breaking, and prove the replay does not skip normal scope enforcement.

## Takeaways

- Treat approval replay as a source-to-sink chain, not as a single UI click.
- The approval payload must preserve the original actor proof when downstream handlers use caller/session/group context.
- An `approved` replay marker should prevent recursive prompts only; it must not become a scope-bypass flag.
- Regression tests should assert the sink receives the original lower-trust context and that approved replay does not queue a second approval.
- Compatibility fallbacks should be explicit and bounded so old pending approvals do not silently define the new security model.

## Repeat next time

- For every approval-gated command/tool/action, map: original caller context → approval payload → replay transform → policy check → sink.
- Check whether the serialized approval object stores actor, session, group, tenant, target, and capability fields used after replay.
- Add a negative or bounded-behavior test where a lower-trust caller receives approval but still reaches the sink with the lower-trust context.
- Add a positive compatibility path for legitimate host-originated or legacy approval payloads when the project needs it.
- In PR text, separate “who can approve” from “which actor executes after approval” so the security claim stays narrow.

## Vault redirect

- New takeaway: `06 - Lessons/Takeaway - Approval replay must preserve original caller context.md`.
- Index route: `06 - Lessons/Takeaways Index.md` now links the approval replay takeaway.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially the candidate contract fields for source, entry surface, trust boundary, policy layer, sink, proof command, false positive, and next-cheapest test.
- Public-site data route: `_data/merged_prs.yml` now includes `nanocoai/nanoclaw #2611` for the 2026-07 archive.
- Public site role: this post is the public-safe synthesis. Detailed private follow-up, if any, belongs in the vault rather than becoming a separate website-only memory.
