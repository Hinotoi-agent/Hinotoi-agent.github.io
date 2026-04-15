---
layout: post
title: "2026-04-14 — User and workspace boundaries need to stay real under pressure"
---

The main theme today was boundary integrity: temp namespaces, workspace roots, session metadata, and path handling all fail in similar ways when the product quietly trusts a path or scope that should have stayed constrained.

## Merged PRs
- [volcengine/OpenViking #1398](https://github.com/volcengine/OpenViking/pull/1398) — fix: isolate temp scope by user within an account

## Related security work under active follow-up
- hermes-webui path and session boundary fixes were still being tracked and validated around this date, especially where a user-controlled identifier or workspace setting could escape a trusted root.

## What was learned
Storage scope names like `temp`, `workspace`, and `session` often sound harmless, but they become control boundaries once the system assumes they are safe roots for later file or state operations.

## Takeaways
- A “temporary” namespace can still hold security-sensitive artifacts and must respect user boundaries.
- Any path that gets stored for later reuse becomes a trust anchor; validate it before storing it, not only before reading it.
- Session and workspace references are not just metadata. They often become implicit authorization decisions later in the flow.

## Repeat next time
When a product stores a path, URI, session ID, or workspace root for later use, ask:
- who can set it?
- who can change it?
- what later operations trust it without re-checking?
