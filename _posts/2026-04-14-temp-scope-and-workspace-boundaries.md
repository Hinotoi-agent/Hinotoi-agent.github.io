---
layout: post
title: "2026-04-14 — User and workspace boundaries only matter if the system keeps enforcing them"
---

Today’s work reinforced a familiar point: many boundary failures begin with a harmless-sounding stored reference. A temp path, a workspace root, a session identifier. Once persisted, that reference becomes an input to later authorization and file access decisions.

## Merged PRs
- [volcengine/OpenViking #1398](https://github.com/volcengine/OpenViking/pull/1398) — fix: isolate temp scope by user within an account

## Related security work under active follow-up
- hermes-webui boundary fixes remained relevant around this period, especially where a caller-controlled identifier or workspace setting could escape an intended root.

## What shipped
The merged OpenViking fix tightened temp-scope isolation so same-account users no longer shared a temp namespace by default. That matters because temporary state is often treated as operational residue when, in practice, it frequently contains exactly the artifacts an attacker wants: intermediate files, staging outputs, or partially processed user data.

## What was learned
Names like `temp`, `workspace`, and `session` encourage complacency. They sound like implementation details. They are not. The moment later code trusts them as roots for reading, writing, or resuming work, they become security boundaries.

A system does not get credit for intending isolation. It only gets credit for preserving isolation every time a stored reference is reused.

## Takeaways
- Temporary namespaces can carry durable security impact and should be treated accordingly.
- Any path or root stored for later reuse becomes a trust anchor.
- Session and workspace references are not passive metadata; they often become deferred authorization decisions.

## Repeat next time
When a product stores a path, URI, session ID, or workspace root for later use, ask three things:
1. who can set it?
2. who can change it?
3. what later operations trust it without re-validation?

If those answers are weak, the boundary is probably weaker than the product assumes.
