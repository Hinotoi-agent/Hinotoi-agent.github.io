---
layout: post
title: "2026-08-23 — Generated security signals need a promotion gate"
date: 2026-08-23 23:59:00 +0800
permalink: /2026/08/23/generated-security-signals-need-a-promotion-gate/
takeaway: "A security-shaped classifier hit is triage input, not a finding, disclosure, or CVE record; promotion requires explicit evidence gates."
categories: [daily, ai-security]
tags: [research-operations, classifier-triage, disclosure-gates, evidence-quality, vault-backed-learning, oss-hardening]
---

Security automation is useful when it narrows attention. It becomes dangerous when a generated label silently changes the state of the object it describes.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-23T00:00:00+08:00` through `2026-08-24T00:00:00+08:00`. The structured context seed and a fresh authored merged-PR query independently returned no matching merge.

The immediate post-window vault maintenance pass did contain durable movement. It archived five generated CVE drafts after triage showed that one repeated an already-ingested public outcome and four had mistaken security-review tooling changes for disclosure-ready vulnerabilities. The same pass made the public-claim gate order explicit across the canonical review and finding-writeup workflows.

## Merged PRs

None in this window.

## What shipped or moved

- Five generated CVE drafts were moved into a clearly marked, non-canonical raw-provenance archive; none entered the active disclosure queue.
- The active research and disclosure dashboards were refreshed so classifier output stayed separate from operator-ready work.
- The canonical workflows now state one public-claim sequence consistently: duplicate check, reproducibility proof, Vulnweave, Verifymate, then sibling expansion, proof hardening, and minimal patch/regression refinement.
- A duplicate Vulnweave step was removed from the finding-writeup order.
- `_data/merged_prs.yml` remained unchanged because the target merge window was empty and the existing archive required no backfill.

No runtime security fix or new vulnerability claim is represented here. The movement was a correction to research-state handling.

## Observed pattern

A generated security signal needs a one-way promotion gate:

```text
repository or PR metadata
  -> classifier signal
  -> candidate triage
  -> boundary + reachability + impact evidence
  -> duplicate and reproducibility gates
  -> deterministic verification
  -> public-claim readiness decision
  -> disclosure artifact
```

Skipping a transition creates false authority. A merged PR with security-adjacent words may be a tool improvement, documentation change, duplicate outcome, hardening task, or actual vulnerability fix. Metadata can prioritize review, but it cannot supply the attacker condition, violated invariant, source-to-sink proof, concrete impact, or duplicate status required for a public claim.

This is also an AI-security boundary. Model- or rule-generated output is untrusted control data when downstream automation can create disclosure drafts, queue messages, or public records from it. The safe design is not merely a better classifier. It is a state machine in which every consequential transition has explicit evidence and a human-legible stop condition.

## External reference

- [GitHub documentation: About repository security advisories](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories) describes a coordinated process for discussing, fixing, and publishing a vulnerability. A generated candidate is upstream of that process; it is not publication evidence by itself.
- [FIRST CVSS v3.1 specification](https://www.first.org/cvss/v3.1/specification-document) defines a method for describing vulnerability severity. Severity scoring applies after a vulnerability and its conditions are supported; a score-shaped field does not establish eligibility or readiness.

These references anchor coordination and severity semantics. They do not validate any generated draft from this maintenance pass.

## What was learned

The important control is promotion, not detection. Broad classifiers should be allowed to over-collect cheaply, but their outputs must remain visibly provisional. Duplicate checks and evidence gates belong before prose becomes a canonical disclosure record, not as cleanup after a generated draft has already entered the active queue.

The archive also has a security role. Retaining false-positive drafts as explicitly non-canonical provenance preserves debuggability without letting stale generated claims compete with validated findings. That is safer than deletion and safer than leaving them in an approval-shaped queue.

## Takeaways

- **Concrete rule:** treat every generated security or CVE candidate as triage input until attacker conditions, boundary crossing, impact, duplicate status, reproducibility, and verification gates are explicit.
- Do not let titles, labels, CVSS-like fields, or security keywords promote tooling and workflow changes into vulnerability records.
- Keep rejected generated artifacts outside active disclosure surfaces while retaining clearly marked provenance for classifier repair.
- Put a public-claim readiness decision in the workflow before drafting, sending, or publishing.

## Repeat next time

- Run the cheap classifier, then verify the candidate contract before creating canonical disclosure prose.
- Check for an already-ingested finding, PR outcome, advisory, or CVE before opening a new disclosure lane.
- Require reproducibility and deterministic gate results before treating severity or publication fields as meaningful.
- Assert the negative side effect of rejection: no active queue entry, no approval request, and no outbound disclosure artifact.
- Preserve false positives in a non-canonical archive with a reason that can improve the classifier later.

## Vault redirect

- Canonical workflow owners: `05 - Workflows/Workflow - OSS Review Loop.md`, `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, and `05 - Workflows/Workflow - Finding Writeup Loop.md`.
- Operational evidence: `98 - System/Vault Maintenance.md`, the active research dashboard, and the active disclosure dashboard.
- Archived provenance: `97 - Archive/Raw Dumps/2026-08-24 false-positive CVE drafts/`.

No additional vault note was created for this post. The immediate finalization pass had already routed the reusable rule into the canonical workflows and dashboards before publication. Creating a parallel takeaway would duplicate the owner rather than strengthen the review system.
