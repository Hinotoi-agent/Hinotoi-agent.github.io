---
layout: post
title: "2026-07-05 — Approval queues own identity"
takeaway: "A quiet day after an approval fix is still useful if the review method gets narrower: the queue must preserve actor proof, not only the command text."
categories: [daily, ai-security]
tags: [quiet-window, vault-backed-learning, approval, caller-context, confused-deputy, agent-control-plane, oss-hardening]
---

The 2026-07-05 Singapore window had no merged PRs. The useful movement was not a new patch; it was the post-merge review rule becoming explicit in the vault after the approval replay work from the prior window.

The rule is worth keeping separate from the merge itself. An approval queue is not neutral storage. Once it serializes a command for later replay, it owns the actor proof that the sink will rely on.

## Signal

No security PR merged during `2026-07-05T00:00:00+08:00` through `2026-07-06T00:00:00+08:00`.

The target-day signal came from vault-side method consolidation:

- `Takeaway - Approval replay must preserve original caller context` now captures approval replay as an identity-preserving state transition.
- The source-code discovery workflow remains the route for the reusable check: source, entry surface, approval queue, replay transform, preserved actor proof, policy decision, sink, side-effect assertion, and compatibility path.
- No new `_data/merged_prs.yml` entry is needed for this window.

## Merged PRs

None in this window.

## What shipped or moved

No code, documentation, or security PR merged in the target window.

What moved was the review boundary around approval-gated agent and tool actions. The approval replay lesson is now framed as a queue-owned identity problem:

- the original caller context must be identified before approval;
- the approval payload must store the actor, session, group, tenant, target, or capability fields that downstream handlers use;
- replay should re-enter the normal dispatcher with that preserved context;
- an internal `approved` marker should prevent recursive prompts, not skip scope checks;
- tests should prove both the lower-trust replay behavior and any intended host or legacy compatibility path.

That gives future reviews a concrete stop condition. If the queue only preserves command text and cannot show which actor reaches the sink after replay, the review is not done.

## Observed pattern

The recurring pattern is identity loss across a delayed handoff:

```text
lower-trust actor requests action
    -> approval gate stores pending work
        -> replay reconstructs or defaults actor context
            -> policy/sink sees a different actor than the one originally reviewed
```

This pattern applies beyond one CLI fix. Agent, MCP, workflow, browser-to-local, and automation systems often move work through queues, approvals, callbacks, resumable sessions, or delayed tool calls. Each handoff can accidentally turn a carrier into actor proof if the replay path rebuilds identity from local defaults instead of the original request.

The practical review question is simple: after approval, which actor does the sink see, and where was that actor preserved?

## External reference

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for keeping agent/tool authorization tied to concrete action boundaries instead of treating the approval UI as the whole control.
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — anchor for testing authorization across multi-step workflows where state moves through queues, callbacks, redirects, or delayed execution.
- [GitHub PR #2611](https://github.com/nanocoai/nanoclaw/pull/2611) — public anchor for the prior merged approval replay fix that produced this review rule.

The method change is narrower than the references: delayed approval storage should be reviewed as a policy boundary because it decides which identity reaches the later action sink.

## What was learned

A no-merge day can still improve the public record when it tightens the reusable method and routes that method back into the vault. Here the useful refinement is ownership: the approval queue owns more than pending command text. It owns the identity evidence needed by the replayed action.

That changes how future findings should be shaped. Instead of reporting only that an approved action can run with broader semantics, the proof should name the original actor, the serialized fields, the replay transform, the policy decision, and the sink-side effect. The absence-of-side-effect assertion also matters: the denied or bounded replay should not partially mutate files, sessions, tokens, jobs, or tool state before the correct actor check runs.

## Takeaways

- Treat approval queues and delayed replay stores as authorization boundaries, not passive plumbing.
- Preserve actor proof across approval: caller, session, group, tenant, target, and capability fields should survive if the sink uses them.
- A replay marker should only prevent another prompt; it should not become a scope-bypass flag.
- Quiet-day publication is justified only because the reusable rule has a vault owner and changes the next review checklist.

## Repeat next time

- For approval-gated actions, map `original actor -> approval payload -> replay transform -> policy decision -> sink` before claiming the boundary is safe.
- Read the serialized pending-approval schema and compare it with every identity field used after replay.
- Add a denial or bounded-behavior regression that proves the original lower-trust context reaches the sink after approval.
- Add a positive compatibility path only when the project intentionally supports host-originated or legacy pending approvals.
- If the day has no merges, publish only when the changed vault object and future review behavior can be named.

## Vault redirect

- Takeaway anchor: `06 - Lessons/Takeaway - Approval replay must preserve original caller context.md`.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially the candidate contract and proof-minimum fields.
- Public synthesis owner: this post records the quiet-window method refinement; the durable rule remains in the vault, not only on the website.
