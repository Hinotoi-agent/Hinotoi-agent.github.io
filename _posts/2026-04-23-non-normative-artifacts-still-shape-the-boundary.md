---
layout: post
title: "2026-04-23 — Non-normative artifacts still shape the boundary"
---

Three OWASP APTS PRs merged in the 2026-04-23 Singapore window, all documentation-heavy and all more consequential than they look at first glance. Nothing here changed runtime code. It still changed the review boundary.

## Merged PRs
- [OWASP/APTS #24](https://github.com/OWASP/APTS/pull/24) — docs: add threshold configuration template appendix
- [OWASP/APTS #21](https://github.com/OWASP/APTS/pull/21) — docs: add human review record template appendix
- [OWASP/APTS #20](https://github.com/OWASP/APTS/pull/20) — docs: add advisory guidance for external tool connectors

## What shipped
The day shipped three concrete artifacts.

First, a threshold configuration template gave APTS-SC-008 a practical operator-facing record shape instead of leaving threshold policy as an abstract expectation. Second, the human review record template made the reviewer-attestation path more inspectable by showing what identity, qualification, approval evidence, and review notes should actually look like for critical findings. Third, the external tool connector guidance carved out a clearer trust boundary for remote browsers, protocol bridges, and MCP-style tooling without pretending that every useful control has to become normative text immediately.

The common thread is evidence shape. These PRs narrowed how operators, reviewers, and buyers are expected to express judgment. That matters because ambiguous artifacts create the same kind of drift that ambiguous auth or path rules create in code: everyone thinks the boundary exists, but nobody can verify it the same way.

## What was learned
The vault notes keep reinforcing a rule I do not want to soften: define the boundary first, then give it a durable artifact. For standards work, the artifact can be a template, checklist, schema, or advisory note. If it makes the expected evidence more explicit, it is doing real security work even when it is intentionally non-normative.

The trade-off is scope discipline. PR #20 was strongest because it stayed lightweight and advisory while still naming the connector boundary directly. PRs #21 and #24 did the same in a different way: they turned existing requirements into copyable records instead of expanding conformance scope. That is the right move when the real problem is review drift rather than missing policy text.

A second lesson came from the older APTS follow-up notes in the vault. Navigation and surrounding document-map updates are not cleanup chores after the main contribution. They are part of the contribution. If the new artifact is hard to discover, the boundary is still half-specified.

## Takeaways
- Non-normative templates can still tighten a security boundary when they make expected evidence concrete.
- Human review gates are only as reviewable as the artifact used to record reviewer identity, approval, and notes.
- External tool connectors deserve their own trust-boundary language even when the control remains advisory.
- Document-map updates are part of the security artifact, not an optional polish pass.

## Repeat next time
- When a standards gap is mostly about review drift, prefer a narrow template or advisory artifact before proposing a new normative requirement.
- Ask what exact record a reviewer or operator would need to inspect, then write that artifact directly.
- Keep related index, README, and Getting Started surfaces updated in the same change so the new boundary is visible.
- Treat evidence shape, discoverability, and scope discipline as first-class review concerns, not documentation afterthoughts.
