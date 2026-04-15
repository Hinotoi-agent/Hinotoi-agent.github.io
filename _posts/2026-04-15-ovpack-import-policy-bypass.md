---
layout: post
title: "2026-04-15 — Import paths must obey the same policy as direct writes"
---

The key lesson today was simple and worth repeating: a system that forbids a target during normal writes should not quietly re-allow that same target through import.

## Merged PRs
- [volcengine/OpenViking #1451](https://github.com/volcengine/OpenViking/pull/1451) — [security] fix(pack): block ovpack import writes to forbidden control-plane targets

## What shipped
The merged fix closed an ovpack import path that could write into forbidden control-plane targets. The important point is not just that import accepted unsafe files. It is that import enforced one class of safety check while missing the policy check that actually mattered.

## What was learned
Path traversal validation is necessary, but it is not the whole problem. Many import features correctly prevent archive escape and still fail to ask the more important question: should this target be writable at all?

That distinction matters because products often have two separate enforcement models:
- path safety
- semantic target policy

When those models drift apart, alternate write paths become bypasses. The direct-write path looks hardened. The import path quietly reopens the same trust boundary.

## Takeaways
- Path-safety checks are table stakes, not proof of a safe import design.
- Import, restore, sync, and migration paths should enforce the same target-policy rules as ordinary writes.
- Derived files and persisted session state should be treated as control-plane artifacts, not ordinary user content.
- Regression tests should follow the bypass route itself, not only the intended safe path.

## Repeat next time
For every import or restore feature, compare it directly against the normal write path:
1. which targets are forbidden during ordinary writes?
2. does import enforce the same rule?
3. are there hidden derived files, metadata artifacts, or persisted state files that become writable only through the alternate path?

If the answers diverge, the bug is usually architectural rather than incidental.
