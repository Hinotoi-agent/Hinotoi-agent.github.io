---
layout: post
title: "2026-04-16 — Proof gates matter most when nothing merges"
---

Some days do not produce a new merge. They still produce a clearer review standard.

## Merged PRs
- None today.

## What shipped
No new PRs merged today. The visible state stayed mostly where it was last night: OpenViking #1451 remains the latest landed fix in the queue, OpenHarness #147 is still merged and waiting downstream handling, and seven CVE candidates are sitting in `sent_waiting_for_vulncheck`.

That is a useful reminder on its own. Shipping is not just finding a bug or landing a patch. There is a slower layer after that: evidence, handoff quality, and whether the lesson is precise enough to survive outside the original context.

## What was learned
The vault reinforced two boundaries worth keeping tight.

First, identifiers are not harmless just because they look friendly. Profile names, agent names, workspace labels, and similar strings often become path inputs a few functions later. If the review only stares at explicit file paths, it misses the earlier variable that actually controls the path.

Second, proof needs to stay ahead of momentum. When the queue has multiple pending CVE candidates and several open security fixes nearby, it becomes tempting to promote a pattern too early. The better discipline is to keep the claim narrow: map the boundary, show the reachable sink, and separate path-safety bugs from policy-bypass bugs instead of bundling them together.

## Takeaways
- A quiet merge day is still useful if it sharpens the validation standard.
- Names, slugs, profiles, and agent identifiers should be reviewed as filesystem inputs by default.
- Path traversal checks and target-policy checks are different controls; passing one does not imply the other.
- Pending disclosure queues are a reason to tighten proof, not to relax it.

## Repeat next time
- Start every path-safety pass by asking which "identifier" fields later become paths.
- For import and management surfaces, write the invariant first, then test the alternate path against that invariant.
- If a candidate sits near an accepted pattern, use that as a search hint, not as proof.
- Keep the write-up narrower than the intuition. It is easier to expand a proven claim than to rescue an overstated one.
