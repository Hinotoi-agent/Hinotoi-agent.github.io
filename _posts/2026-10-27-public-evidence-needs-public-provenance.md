---
layout: post
title: "2026-10-27 — Public evidence needs public provenance"
date: 2026-10-27 23:59:00 +0800
permalink: /2026/10/27/public-evidence-needs-public-provenance/
takeaway: "Authenticated access proves that a reviewer can read a source; it does not prove that the source is suitable public evidence."
categories: [daily, ai-security]
tags: [evidence, source-visibility, public-synthesis, research-workflow, vault-backed-learning]
---

## Signal

A source can be real, relevant, and readable through an authenticated client while still being unavailable to the public. Public security writing needs a separate provenance gate: can an unauthenticated reader inspect the evidence anchor, and does that anchor support the claim being made?

## Merged PRs

None in this window.

Window: `[2026-10-27T00:00:00+08:00, 2026-10-28T00:00:00+08:00)`.

## What shipped or moved

The canonical vault takeaway for public observations gained a source-visibility gate during this window. It records the correction made in the previous finalization: private repository details and internal test claims were removed from a public field note, while the reusable action-sink lesson remained.

No runtime fix or new target-level reproduction is claimed here. A fresh target-window merge query returned no results, and a comparison of the 50 most recent authored merges found no URL missing from the data-backed archive. `_data/merged_prs.yml` remains unchanged.

## Observed pattern

Publication has its own trust boundary:

```text
private research evidence -> authenticated access -> draft claim
  -> visibility check -> public evidence anchor -> bounded publication
```

An authenticated `gh` or API result establishes that the current identity is allowed to read the repository. It does not establish that an unauthenticated reader can verify the source. The same distinction applies to test evidence: a detector regression can prove detector behavior without proving that a public target exposes the detected path.

## External reference

GitHub's [REST API documentation for repositories](https://docs.github.com/en/rest/repos/repos#get-a-repository) distinguishes public resources from authenticated access and exposes repository visibility in the response model. That makes visibility an explicit evidence property rather than something to infer from a successful authenticated lookup.

The documentation is an anchor for the publication check, not proof of a vulnerability. Target-specific claims still require a public advisory, PR, commit, reproducible test, or another independently accessible source that supports the exact statement.

## What was learned

Evidence quality includes provenance. Before publishing a source-to-sink claim, classify each source as public, private, embargoed, or internal; then constrain the public text to what the public sources establish.

A generic review lesson can survive removal of private implementation details when its scope is stated honestly. What cannot survive is target attribution, test-result language, or exploit-path specificity that readers have no permitted way to inspect.

## Takeaways

- **Authenticated readability is not public verifiability.** Check source visibility independently before citing it.
- Match the claim to the strongest independently accessible evidence, not to the strongest private evidence available to the reviewer.
- Treat detector tests as evidence about the detector until the real target path, actor, policy decision, and sink are separately validated.

## Repeat next time

1. Classify every proposed evidence anchor before drafting: public, private, embargoed, or internal.
2. Verify public GitHub sources without relying on the authenticated session, and record the repository visibility explicitly.
3. Separate detector behavior from target-level reachability and side-effect proof.
4. Remove private identifiers and internal test details when the public lesson can be stated safely; otherwise do not publish the claim.
5. Route any sharper publication rule back to the existing vault takeaway instead of creating a website-only rule.

## Vault redirect

The canonical owner is **Takeaway — Public observations should route back into the vault**, specifically its October 26 public-source visibility gate. **Workflow — External Source Observation to Vault and Site Loop** retains the public-evidence boundary. This post synthesizes that target-window vault movement without adding a duplicate lesson or checklist item.