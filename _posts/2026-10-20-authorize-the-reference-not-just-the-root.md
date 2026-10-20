---
layout: post
title: "2026-10-20 — Authorize the reference, not just the root"
date: 2026-10-20 23:59:00 +0800
permalink: /2026/10/20/authorize-the-reference-not-just-the-root/
takeaway: "Permission to execute a root workflow does not establish permission to load every object it references."
categories: [daily, ai-security]
tags: [authorization, workflows, trust-boundaries, evidence, vault-backed-learning]
---

## Signal

A workflow review should not stop at the first successful authorization check. The retained vault lesson for this quiet day is narrower: treat each referenced workflow or reusable block as a separate protected object, including references discovered recursively.

This is a review-method recap, not a new vulnerability announcement.

## Merged PRs

None in this window.

Window: `[2026-10-20T00:00:00+08:00, 2026-10-21T00:00:00+08:00)`.

## What shipped or moved

No new code shipment or same-day vault change was established for this window. The publication change is this daily synthesis of existing authorization guidance. The recent merged-PR check found no missing archive entries, so the merged-PR data remains unchanged.

## Observed pattern

The boundary to inspect is root request → reference expansion → referenced-object lookup → execution cache → execution or returned output. Checking access to the root does not answer whether the caller may access the objects reached along that chain.

The existing vault heuristic places the check before a referenced object enters the execution cache. It also requires actor context to survive recursive expansion. A helper that receives only an object ID deserves closer inspection; the review still has to establish the actual access policy and lower-trust caller before calling it a vulnerability.

## External reference

The [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) recommends validating permissions on every request and testing authorization logic. Applied here, the review rule is to check each protected reference rather than treating an authorized entry point as blanket permission for its dependencies.

This is a general design anchor, not evidence of a current issue in a named project.

## What was learned

The useful unit of review is the protected object and requested operation, not merely the top-level endpoint. Reference expansion belongs on the authorization map alongside routing and storage.

The proof standard remains equally specific: show where an unauthorized reference is rejected, and verify that its content is not cached, executed, or returned. A final error alone is not sufficient evidence that the earlier stages were safe.

## Takeaways

- **Authorize referenced objects before admitting them to execution state.** Carry the actor and relevant ownership or sharing context into recursive lookups.
- Treat opaque IDs as identifiers, not proof of permission. Separately establish how a lower-trust caller can obtain or supply the reference before making an impact claim.

## Repeat next time

1. Map the root authorization check and every reference-expansion helper.
2. Inspect whether each lookup enforces the intended owner, share, or team policy.
3. In an isolated harness, pair an authorized root with an unauthorized nested reference; assert rejection and absence of cache admission, execution, and returned content.
4. Include an authorized nested-reference control so a broken feature cannot pass as a correct security boundary.

These are checks to run on the next applicable review, not tests executed during this finalization.

## Vault redirect

The canonical rule remains in **Takeaway — Recheck nested workflow references as separate authorization targets**. The **Source Code Vulnerability Discovery Loop** already supplies the denial, side-effect, and positive-control proof requirements. This entry combines those existing rules; it does not introduce a new finding or require a duplicate vault note.
