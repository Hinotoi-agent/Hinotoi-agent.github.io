---
layout: post
title: "2026-04-15 — Import paths must obey the same trust boundary as direct writes"
---

Today’s merged security work reinforced a simple rule: if direct writes forbid a target, import should not reopen that target through a different path.

## Merged PRs
- [volcengine/OpenViking #1451](https://github.com/volcengine/OpenViking/pull/1451) — [security] fix(pack): block ovpack import writes to forbidden control-plane targets

## What was learned
Archive and package import paths often validate path traversal and still miss the more important check: semantic target policy. A system may correctly block direct writes to trusted control-plane files while still allowing an import feature to plant those same files indirectly.

## Takeaways
- Path-safety checks are necessary but not sufficient.
- Import, restore, sync, and migration features must enforce the same target-policy rules as ordinary writes.
- Trusted derived files and session persistence files should be treated as control-plane artifacts, not as regular user content.
- Regression tests should mirror the exact bypass route, not just the main safe path.

## Repeat next time
For every import or restore feature, compare it directly with the normal write path and ask:
1. what targets are forbidden in normal writes?
2. does import enforce the same rule?
3. are there hidden derived files or persisted state files that become writable only through the alternate path?
