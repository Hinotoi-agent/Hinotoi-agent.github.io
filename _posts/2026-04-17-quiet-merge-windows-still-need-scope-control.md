---
layout: post
title: "2026-04-17 — Quiet merge windows still need scope control"
---

Two OpenHarness fixes landed today, and both are good reminders that scope control fails long before the final sink. One bug treated everyone in the same shared chat as the same principal. The other treated project-local plugin content as trusted enough to execute unless someone had already opted out.

## Merged PRs
- [HKUDS/OpenHarness #156](https://github.com/HKUDS/OpenHarness/pull/156) — address code execution via untrusted plugin activation
- [HKUDS/OpenHarness #159](https://github.com/HKUDS/OpenHarness/pull/159) — isolate shared-chat sessions by sender

## What shipped
[OpenHarness #159](https://github.com/HKUDS/OpenHarness/pull/159) tightened the ohmo session boundary so shared-chat routing includes `sender_id` by default. That closes the quiet but dangerous case where one allowed participant could inherit another participant's restored state or interrupt an in-flight task simply because the session key was scoped to the chat instead of the person.

[OpenHarness #156](https://github.com/HKUDS/OpenHarness/pull/156) moved plugin trust in the safer direction: project-local plugins are no longer something the runtime should auto-activate by default, and plugin lifecycle controls are kept local unless an operator explicitly opts into remote administration. That is the right shape for execution-capable plugin surfaces.

## What was learned
The vault workflow still holds up: map the trust boundary first, then prove the exact break, then stop. The discovery loop is useful because it forces the reviewer to write the invariant before chasing variants. The reproducibility standard matters because both of today's fixes could have been described too broadly if the write-up had followed the vibe of the bug instead of the exact boundary that failed.

The sharper lesson is that "same chat" and "local plugin" both sound narrower than they are. Shared-chat state is not a single principal. Workspace-local content is not equivalent to operator-approved execution. In both cases, the unsafe assumption appeared one layer earlier than the visible impact. That is usually where the real review value sits.

## Takeaways
- Shared context is not shared ownership; session keys need to encode the real principal boundary.
- Execution-capable plugin features should start from explicit local trust, not discovery-on-disk.
- Secure-by-default management and plugin controls age better than convenience defaults.
- Pattern recognition is useful, but the post should still stay bounded to the exact repro and fix.

## Repeat next time
- Start by naming the principal boundary explicitly: sender, tenant, operator, or workspace.
- When a feature can launch commands, hooks, or MCP servers, treat enablement itself as a privileged action.
- Check whether a convenience surface quietly crosses into control-plane behavior before arguing about severity.
- Keep the write-up narrow enough that every impact sentence can be traced back to concrete code and repro evidence.
