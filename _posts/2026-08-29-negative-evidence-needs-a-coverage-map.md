---
layout: post
title: "2026-08-29 — Negative evidence needs a coverage map"
date: 2026-08-29 23:59:00 +0800
permalink: /2026/08/29/negative-evidence-needs-a-coverage-map/
takeaway: "An empty security result is useful only when it names the actor, event, closed interval, canonical ledgers, and downstream state that were actually checked."
categories: [daily, ai-security]
tags: [research-operations, quiet-window, negative-evidence, coverage, provenance, vault-backed-learning, oss-hardening]
---

An empty result is not universal evidence. It is a scoped statement about the surfaces that were actually measured.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-29T00:00:00+08:00` through `2026-08-30T00:00:00+08:00`. The structured context seed and a fresh query of the 100 most recently updated authored merged PRs agreed after merge timestamps were filtered to the exact UTC-equivalent interval.

The canonical vault recorded no commit or Markdown modification attributable to the target window. Prioritized workflows, maintained indexes, and relevant publication-routing guidance were consulted. Unrelated pre-existing working-tree changes were treated as ambient state and left untouched.

## Merged PRs

None in this window.

## What shipped or moved

- The August 29 reporting window was finalized only after it closed in Singapore time.
- Authored merge history was checked against the explicit interval and returned no matching PR.
- Vault history and target-window Markdown modification times were checked for source, advisory, takeaway, checklist, follow-up, disclosure, or workflow movement; none was attributable to the interval.
- `_data/merged_prs.yml` was verified as a 154-record archive with no duplicate URLs and no missing August 29 record, so it remained unchanged.
- Only this required daily closure artifact moved. It does not claim a new finding, fix, disclosure transition, or review-method revision.

## Observed pattern

Negative evidence needs a coverage map:

```text
claim
  -> actor and event type
  -> closed time interval
  -> canonical ledgers queried
  -> attribution rule
  -> protected derived state checked
  -> bounded conclusion
```

The same discipline applies to agent and tool systems. A guard that checks one route, tool registry, memory namespace, approval path, or filesystem helper does not prove that sibling paths are safe. Likewise, a denial response does not prove safety unless the consequential sink—process, file, request, session, memory, approval, or stored mutation—remained untouched.

## External reference

- [GitHub GraphQL search](https://docs.github.com/en/graphql/reference/queries#search) anchors the authored merged-PR event check. The result is meaningful only after the actor, merge state, timestamp field, and reporting interval are fixed.
- [Git status documentation](https://git-scm.com/docs/git-status) distinguishes committed history from index, working-tree, and untracked state. That separation prevents ambient edits from being misdated as target-window events.
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) provides a public frame for risks across agent goals, tools, identities, memory, and orchestration. The operational lesson here is narrower: evidence from one control surface should not be generalized beyond the boundary it actually covers.

These references anchor the coverage model; they do not supply activity absent from the canonical ledgers.

## What was learned

A negative claim should be reviewable as a compact proof packet. “Nothing happened” is too broad. “No PR authored by this account has a merge timestamp inside this closed interval, and no canonical vault object moved in the checked window” is narrower and reproducible.

This is also a useful test-design rule. Security regressions should identify the denied path and the sink whose non-mutation matters. Coverage should then expand deliberately across sibling routes and compatibility lanes rather than being inferred from one passing assertion.

## Takeaways

- **Concrete rule:** attach a coverage map to every empty-window, denial, or no-side-effect claim.
- Scope negative evidence by actor, event, interval, canonical source, and sink—not by intuition.
- Do not generalize one guarded route or one passing regression to sibling tools, handlers, namespaces, or storage primitives.
- Leave derived archives and unrelated working state unchanged when the attributable input set is empty.

## Repeat next time

- Finalize only the previous closed Singapore day.
- Compare the structured seed with a fresh authored merged-PR query filtered to the identical interval.
- Check canonical vault history and target-window file times before attributing research movement.
- Validate the merged-PR archive for omissions and duplicate URLs, then leave it untouched when complete.
- For security denials, assert both the visible rejection and absence of side effects at the named sink; enumerate sibling paths separately.

## Vault redirect

- Canonical publication owner: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, especially its closed-window evidence, negative-evidence ownership, and repeated quiet-window hard-stop rules.
- Review-method owner: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially candidate evidence anchors, sibling expansion, stop conditions, and denial-plus-absence proof.
- Operating owner: `05 - Workflows/Workflow - OSS Review Loop.md`.

No vault note was changed for this post. The bounded negative-evidence and coverage rules are already represented by those canonical notes, and the target window supplied no new review behavior to reverse-route. Creating another lesson—or staging unrelated vault changes—would duplicate ownership rather than strengthen it.
