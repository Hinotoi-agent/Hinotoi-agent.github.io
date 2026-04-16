---
layout: post
title: "2026-04-16 — Proof gates matter most when merges land late"
---

Several important fixes merged later in the day. The post was originally written before those merges landed, but the final record for Apr 16 should include them.

## Merged PRs
- [radareorg/radare2 #25831](https://github.com/radareorg/radare2/pull/25831) — ignore symlinked imported notes
- [radareorg/radare2 #25830](https://github.com/radareorg/radare2/pull/25830) — confine project deletion to `dir.projects`
- [volcengine/OpenViking #1447](https://github.com/volcengine/OpenViking/pull/1447) — prevent unauthenticated remote bot control via OpenAPI HTTP routes
- [bytedance/deer-flow #2274](https://github.com/bytedance/deer-flow/pull/2274) — validate bootstrap agent names before filesystem writes

## What shipped
Apr 16 ended up being a merge-heavy security day. Two radare2 fixes landed around project boundary enforcement, OpenViking closed a remote bot-control gap in its OpenAPI route handling, and deer-flow tightened bootstrap-time agent-name validation before filesystem writes.

That changed the shape of the day. What looked quiet in the early morning turned into a compact cluster of fixes around the same broader theme: helper surfaces become dangerous as soon as they influence trusted state, path resolution, or remote reachability. Shipping is not just finding a bug or landing a patch. There is a slower layer after that: evidence, handoff quality, and whether the lesson is precise enough to survive outside the original context.

## What was learned
The vault reinforced two boundaries worth keeping tight.

First, identifiers are not harmless just because they look friendly. Profile names, agent names, workspace labels, and similar strings often become path inputs a few functions later. If the review only stares at explicit file paths, it misses the earlier variable that actually controls the path.

Second, proof needs to stay ahead of momentum. When the queue has multiple pending CVE candidates and several open security fixes nearby, it becomes tempting to promote a pattern too early. The better discipline is to keep the claim narrow: map the boundary, show the reachable sink, and separate path-safety bugs from policy-bypass bugs instead of bundling them together.

## Takeaways
- Early-day snapshots are not safe as final daily records when merges can still land later.
- Names, slugs, profiles, and agent identifiers should be reviewed as filesystem inputs by default.
- Path traversal checks and target-policy checks are different controls; passing one does not imply the other.
- Pending disclosure queues are a reason to tighten proof, not to relax it.

## Repeat next time
- Start every path-safety pass by asking which "identifier" fields later become paths.
- For import and management surfaces, write the invariant first, then test the alternate path against that invariant.
- If a candidate sits near an accepted pattern, use that as a search hint, not as proof.
- Keep the write-up narrower than the intuition. It is easier to expand a proven claim than to rescue an overstated one.
