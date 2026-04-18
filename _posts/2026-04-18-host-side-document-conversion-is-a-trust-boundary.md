---
layout: post
title: "2026-04-18 — Host-side document conversion is a trust boundary"
---

One deer-flow fix landed today, but it covered a boundary that is easy to understate. The moment an upload can trigger server-side document conversion, the system has stopped being a passive file receiver and started acting as a parser and transformation service on behalf of the user. That deserves explicit operator choice, not a quiet default.

## Merged PRs
- [bytedance/deer-flow #2332](https://github.com/bytedance/deer-flow/pull/2332) — require explicit opt-in for host-side document conversion

## What shipped
[deer-flow #2332](https://github.com/bytedance/deer-flow/pull/2332) moved host-side document conversion behind an explicit opt-in. That is the right direction for upload handling that can invoke heavyweight parsers or office-conversion tooling on the server. The fix reduces ambient exposure by making operators choose whether they want that capability at all instead of inheriting it as part of ordinary document upload behavior.

## What was learned
The vault baseline keeps reinforcing the same sequence: map the trust boundary first, then name the dangerous sink, then keep the claim narrow. Upload review is not just about extension checks, storage paths, or direct file serving. If the backend will parse, render, or convert the file, the real boundary is the host-side processing step.

That matters because "document conversion" sounds like compatibility plumbing when it is really a privileged parser surface. The same secure-by-default rule that improved management APIs also applies here: if a feature causes the server to process attacker-supplied documents with complex host-side tooling, explicit opt-in is usually safer than default enablement. The useful boundary is not only who may upload, but what work the host is willing to perform after the upload arrives.

## Takeaways
- Host-side document conversion should be reviewed as an active-content surface, not as harmless format normalization.
- Upload security needs a second pass for downstream parsers, converters, and renderers, not just the initial write path.
- Explicit opt-in is a strong default when a feature turns stored input into server-side processing.
- A compact fix can still represent a meaningful trust-boundary correction if it removes ambient parser exposure.

## Repeat next time
- In every upload review, ask separately: can the host parse, convert, thumbnail, render, or otherwise execute complex processing on this file?
- Treat office-conversion and document-normalization helpers as dangerous sinks early in the review, not as implementation detail.
- Write the invariant in plain terms: upload does not imply permission to make the server process the document.
- When a feature is useful but high-risk, look first for a secure-default opt-in design before arguing about narrower mitigations.
