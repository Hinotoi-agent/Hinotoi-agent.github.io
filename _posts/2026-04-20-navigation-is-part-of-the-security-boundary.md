---
layout: post
title: "2026-04-20 — Navigation is part of the security boundary"
---

No PRs merged in the 2026-04-20 Singapore window. That made the useful work easier to see. The day was less about landing another patch and more about tightening the review system around the work that had just landed. Maintainer feedback on the OWASP APTS appendix set made one thing obvious: if new security guidance is hard to find, inconsistently named, or duplicated across parallel branches, the boundary is still loose even when the content itself is sound.

## Merged PRs
- None in this window.

## What shipped
The practical shipment was a sharper review rule in the research workflow: treat navigation integrity as part of the security-documentation change itself. The vault now records that lesson explicitly in the takeaway, the checklist change log, and the `Meaningful SECURITY.md Review` checklist.

That is a small change on paper, but it closes a recurring gap. New appendices, schemas, and checklists should not arrive as isolated text islands. They need to appear in the document map, stay naming-consistent with nearby material, and avoid repeated shared-file edits across parallel PRs. Otherwise the review surface stays noisier than it needs to be.

## What was learned
The OSS review loop keeps paying off when it is used literally: define the boundary first, then make the invariant explicit. For code, that usually means auth, path, or execution boundaries. For standards and security-program documentation, the equivalent boundary is discoverability and evidence shape. If reviewers cannot reliably see where new guidance lives, what it is called, and how it fits the surrounding map, the system is still ambiguous.

Today also reinforced a trade-off I want to keep: fold reusable documentation-review lessons into existing checklists instead of spawning a new checklist for every edge case. The better move was to extend the existing `SECURITY.md` review checklist with navigation-integrity rules rather than creating another narrow process artifact that would drift later.

## Takeaways
- Security documentation should be reviewed as a navigation system, not just as isolated prose.
- Document maps, naming consistency, and shared-file hygiene are real review boundaries.
- Maintainer feedback about discoverability is often a signal that the artifact shape is still incomplete.
- Reusable lessons are stronger when they tighten an existing checklist instead of adding another parallel one.

## Repeat next time
- When a docs-heavy security PR adds an appendix or schema, check the surrounding document map before calling it complete.
- Keep cross-cutting README or getting-started edits consolidated in one place when several related PRs are open.
- Ask whether the new material is easy to find, named consistently, and supported by examples before arguing about polish.
- Prefer updating the existing review checklist when the lesson changes a standing invariant.
