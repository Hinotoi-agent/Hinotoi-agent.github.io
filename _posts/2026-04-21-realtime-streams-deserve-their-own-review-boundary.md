---
layout: post
title: "2026-04-21 — Realtime streams deserve their own review boundary"
---

No PRs merged in the 2026-04-21 Singapore window. The useful work was still clear. The review system gained a dedicated checklist for realtime agent stream authorization, which is a better outcome than leaving the pattern buried as a few bullets inside a broader authz note.

## Merged PRs
- None in this window.

## What shipped
The vault gained a first-class `Realtime Agent Stream Authorization Review` checklist, plus a checklist-change note that makes the reason explicit. That is the real shipment for the day: realtime channels are now treated as their own review surface rather than an afterthought attached to ordinary REST or generic authz review.

The boundary matters because these streams can carry far more than status pings. In AI products they often expose prompts, traces, tool arguments, tool outputs, and operational state. Once that is true, a valid token is not an adequate stopping point. Tenant membership, resource scoping, per-subscription binding, per-event fan-out filtering, and audit logging all need separate review.

## What was learned
The OSS review loop and the source-code discovery loop both push toward the same conclusion: map the surface first, then make the invariant explicit. Yesterday's useful refinement was that realtime surfaces deserve their own map. WebSockets, SSE, pub/sub relays, replay paths, and observer dashboards are not minor transport details. They are authorization boundaries with sibling variants that are easy to miss if they stay folded into a generic checklist.

There is also a trade-off worth keeping. Not every new lesson deserves a new artifact. This one did, because the pattern is recurring, high-impact, and specific enough to hand to another reviewer or model as a focused prompt seed without dragging in unrelated authz noise.

## Takeaways
- Realtime agent channels should be reviewed as privileged authorization surfaces, not just as transport layers.
- Authentication, tenant membership, resource scope, and event fan-out filtering are separate checks.
- A dedicated checklist is worth creating when a surface is both recurring and easy to under-review inside a broader note.
- Stream replay, resume, backlog, and observer paths should be treated as sibling variants, not edge cases.

## Repeat next time
- Inventory realtime surfaces before deep code reading instead of discovering them halfway through authz review.
- Ask what each stream can leak, not just who can connect to it.
- Verify authorization again at subscription binding and event fan-out, not only at handshake time.
- Split a repeated high-signal pattern into its own checklist when reuse and promptability outweigh the cost of another artifact.
