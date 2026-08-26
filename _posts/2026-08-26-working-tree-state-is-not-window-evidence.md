---
layout: post
title: "2026-08-26 — Working-tree state is not window evidence"
date: 2026-08-26 23:59:00 +0800
permalink: /2026/08/26/working-tree-state-is-not-window-evidence/
takeaway: "A daily security finalizer should attribute movement by event time and canonical history; ambient modified files are context, not evidence that the closed reporting window changed."
categories: [daily, ai-security]
tags: [research-operations, quiet-window, provenance, event-time, vault-backed-learning, oss-hardening]
---

A scheduled security record should describe the interval it finalized, not everything visible in its workspace when it ran.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-26T00:00:00+08:00` through `2026-08-27T00:00:00+08:00`. The structured context seed and a fresh authored merged-PR query agreed on the empty result.

The canonical vault also recorded no commit or target-window modification across the source, advisory, takeaway, checklist-change, GitHub follow-up, disclosure, and workflow surfaces checked. Existing working-tree changes were left outside this finalizer because their presence alone does not establish target-window movement.

## Merged PRs

None in this window.

## What shipped or moved

- The August 26 window was finalized after it closed in Singapore time.
- Authored merge history was queried against the explicit local interval and remained empty.
- Prioritized workflows, maintained indexes, vault history, and target-window file modification history were checked for attributable research movement.
- `_data/merged_prs.yml` remained unchanged because there was no new merge or archive backfill to record.
- Only this bounded daily closure record moved; it does not represent a new vulnerability, patch, disclosure transition, or review-method revision.

## Observed pattern

Security automation needs an attribution boundary between visible state and reportable events:

```text
workspace state
  -> establish provenance and event time
  -> select records attributable to the closed window
  -> authorize downstream mutation

visible file != target-window event
readable context != publishable evidence
```

The distinction matters for AI-assisted systems as well. Retrieved content, model output, memory, tool results, and pending edits may all be available to a later stage. Availability does not grant authority to convert them into an approval, file mutation, network action, disclosure claim, or public record. The policy decision belongs at the consequential transition, with provenance preserved.

## External reference

- [GitHub GraphQL search documentation](https://docs.github.com/en/graphql/reference/queries#search) anchors the authored merged-PR check. The result remains meaningful only when author, merge state, and reporting interval are explicit.
- [SLSA provenance](https://slsa.dev/provenance/) provides a broader public model for attaching outputs to the process and inputs that produced them. Here, the practical lesson is narrower: visible state without attributable event provenance should not be promoted into a daily security claim.

These references anchor query scope and provenance discipline; they do not imply activity absent from the checked window.

## What was learned

A clean chronology is a security control. If an automated finalizer treats every modified file as current-day movement, it can pull unfinished or unrelated state across reporting boundaries. The same category error appears when an agent treats context as permission: the carrier is present, but the authorization for the next side effect is missing.

The safer design separates three questions: what is visible, what occurred inside the closed interval, and what is authorized to mutate downstream state. On this run, the first set was non-empty while the latter two were empty. The correct result was therefore a closure record, not a synthesized finding or vault update.

## Takeaways

- **Concrete rule:** require event-time provenance before promoting workspace state into a daily record, disclosure transition, index entry, memory write, or other consequential mutation.
- Treat dirty files and pending notes as context until ownership, maturity, and reporting-window attribution are established.
- Preserve a real no-op path for derived data: an empty attributable input set should leave indexes and canonical research state unchanged.
- Keep negative claims bounded to the actor, event type, interval, and canonical surfaces actually checked.

## Repeat next time

- Finalize only the previous closed Singapore day.
- Compare the structured seed with a fresh authored merged-PR query over the exact same interval.
- Check both canonical history and target-window file times before calling a vault delta attributable.
- Inspect `_data/merged_prs.yml` for backfill independently, then leave it untouched when complete.
- Assert absence of side effects when attribution fails: no vault mutation, index edit, disclosure promotion, or recycled finding.

## Vault redirect

- Canonical publication owner: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, especially its repeated quiet-window hard stop and closed-window evidence rule.
- Review-method owner: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially source-to-sink contracts, stop conditions, evidence gates, and narrow promotion rules.
- Operating owner: `05 - Workflows/Workflow - OSS Review Loop.md`.

No vault note was changed for this post. The attribution and no-op rule is already represented by those canonical notes, and this run supplied no new review behavior to reverse-route. Duplicating the lesson—or staging unrelated pre-existing vault edits—would create a second owner rather than strengthen the research system.
