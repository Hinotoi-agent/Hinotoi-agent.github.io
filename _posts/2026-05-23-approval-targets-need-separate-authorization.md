---
layout: post
title: "2026-05-23 — Approval targets need separate authorization"
takeaway: "Approval permission and target permission are separate decisions; the final selected object must be authorized at the mutation point before channel, agent, or control-plane wiring changes."
categories: [daily, ai-security]
tags: [authz, approval-flows, agent-security, channel-registration, scoped-admin, oss-hardening]
---

The 2026-05-23 Singapore window had one merged security PR in `nanocoai/nanoclaw`: a scoped-admin authorization fix for channel approval target selection.

## Signal

The useful signal was the split between approval context and mutation target.

A scoped admin could be allowed to respond to a pending channel-registration approval because the approval row was associated with one agent group. That did not automatically mean the same admin was allowed to connect the unknown channel to a different agent group selected later through `connect:<agentGroupId>`.

The boundary was not the card, the pending approval row, or the first group used to choose an approver. The boundary was the final channel-to-agent-group wiring.

## Merged PRs

- [nanocoai/nanoclaw #2566](https://github.com/nanocoai/nanoclaw/pull/2566) — [security] fix(permissions): scope channel approval targets

## What shipped or moved

`nanoclaw` now scopes channel approval targets to the actual approver:

- initial approval options are filtered to agent groups the approver can administer;
- follow-up target-selection cards use the approver identity instead of showing all groups;
- the response handler re-checks target-group authorization before accepting `connect:<agentGroupId>`;
- forged, stale, hidden, or out-of-scope target values leave the pending approval in place and do not create channel wiring;
- regression coverage verifies both UI filtering and server-side rejection for the scoped-admin cross-group case.

The patch stayed narrow: owner/global-admin behavior and the general unknown-channel registration flow were left intact. The changed invariant is that a delegated admin may approve only the target group inside their delegated scope.

## Observed pattern

Approval flows often hide a second object-level authorization decision.

```text
pending approval row
    -> approver chosen from reference context
        -> card / callback / stored response value
            -> selected target object
                -> durable wiring or control-plane mutation
```

The weak pattern checks whether the actor may respond to the approval row and then treats the later selected target as trusted. The stronger pattern treats the selected target as a new protected object and authorizes it immediately before the mutation.

This matters more in AI and agent systems because approval surfaces often bridge external channels, agents, tools, workspaces, and human operators. A stale callback value or forged response can become a control-plane mutation if the final handler only trusts the earlier UI path.

## External reference

- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html) — public anchor for cases where a system performs an action without verifying the actor is authorized for the actual object affected.
- [OWASP API1: Broken Object Property Level Authorization / Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) — useful framing for object-specific checks that must follow the selected resource, not only the route or role.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — category-level anchor for agent/tool systems where control-plane actions can be influenced through prompts, callbacks, channels, or tool-facing workflows.

## What was learned

An approval permission is not a target permission. The approval context answers “may this actor respond to this pending approval?” The target context answers “may this actor bind this channel to this agent group?” Those decisions can diverge when the response can carry an object ID, when cards become stale, or when callback values are directly submitted.

The right fix shape is two-layered. UI filtering reduces normal-path confusion, but the server-side response handler must still reject the unauthorized target immediately before it writes durable state. The regression test should prove both: the target is not offered, and a forged target does not create wiring.

For future reviews, approval and invite flows deserve the same variant expansion as workflow references and tool calls. If the first object is authorized, ask what second object is selected later and whether that later object has its own guard at the sink.

## Takeaways

- Treat approval context and selected target as separate authorization objects when a callback, card, invite, or workflow response can carry an ID.
- Filter UI options by the actor's scope, but never rely on option filtering as the security boundary.
- Re-check the final selected object immediately before durable mutations such as channel wiring, ACL creation, agent registration, route binding, task creation, or credential attachment.
- Regression tests should cover stale/forged callback values and assert that the sensitive sink remains unchanged.

## Repeat next time

- For every approval or invitation flow, write the chain as `approval context -> actor -> selected object -> mutation sink`.
- Add a sibling-variant check: if the actor may approve object `A`, try selecting object `B` from the same capability family.
- Test both visible denial and sink absence: no wiring row, no ACL row, no task, no agent binding, and the pending approval remains safe.
- Route the lesson back into the authz/checklist layer instead of leaving it only in the public daily post.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchor: `05 - Workflows/Checklist - Authz Coverage Review.md`, especially object-level authorization and host-side delivery/action mutation checks.
- Takeaway anchors: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md` and `06 - Lessons/Takeaway - Host delivery actions must authorize at mutation point.md`.
- PR anchor: `nanocoai/nanoclaw#2566`, merged during the 2026-05-23 Singapore window.
