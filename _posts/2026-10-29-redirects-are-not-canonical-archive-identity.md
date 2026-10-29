---
layout: post
title: "2026-10-29 — Redirects are not canonical archive identity"
date: 2026-10-29 23:59:00 +0800
permalink: /2026/10/29/redirects-are-not-canonical-archive-identity/
takeaway: "A redirect preserves access, not evidence hygiene: reconcile current repository identity before counting a PR as missing."
categories: [daily, ai-security]
tags: [provenance, data-integrity, github-archives, research-workflow, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge and no established target-window Markdown change in the canonical research vault. A full reconciliation of the public merged-PR archive did expose a different evidence problem: two archived URLs pointed through repository moves, while one older merged security PR was genuinely absent.

That is archive maintenance, not a target-day merge and not a new vulnerability finding.

## Merged PRs

None in this window.

Window: `[2026-10-29T00:00:00+08:00, 2026-10-30T00:00:00+08:00)`.

## What shipped or moved

The data-backed merged-PR archive was reconciled against the complete paginated set of 161 currently returned authored merges:

- `nanocoai/nanoclaw #2001` and `agentenv/agentflow #18` now use their current canonical repository names and URLs rather than stale pre-move locations.
- [volcengine/OpenViking #1624](https://github.com/volcengine/OpenViking/pull/1624) was restored as the genuinely missing record. The PR restricts ordinary account-admin registration from minting globally privileged API keys while preserving the intended root-admin path.
- After correction, the archive contains 161 current records with no unmatched URL in either direction.

No current-day merge was backdated. Each record retains its original local merge date; only canonical identity and archive completeness changed.

## Observed pattern

A redirect can keep a stale reference usable while hiding archive drift:

```text
archived URL -> redirect -> current PR
     |                         |
 raw mismatch             same historical event
     |                         |
     +-> hydrate and classify -+
           rename / transfer
           stale duplicate
           true archive gap
```

String inequality is therefore a discovery signal, not a conclusion. The same discipline applies to vulnerability evidence: resolve the current object, preserve event time, and distinguish an identity change from a new finding before updating counts or narratives.

## External reference

GitHub's [repository-renaming documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository) explains that existing repository information and web traffic are redirected after a rename, while recommending that references move to the new URL. It also warns that reuse of the old name can break those redirects.

The redirect is a compatibility layer. It is not a reason to leave an evidence archive on stale ownership metadata, and it does not identify whether a separate record is actually missing.

## What was learned

Archive integrity needs semantic reconciliation. A current query and a historical data file may describe the same PR under different repository paths. Counting raw URL differences would have reported three missing records; direct PR hydration showed that only one was absent and two were identity updates.

For security research, repository ownership, merge time, PR number, title, and current URL are evidence fields rather than presentation details. Reconcile them before using an archive to support throughput, provenance, disclosure, or selected-work claims.

## Takeaways

- **Redirect reachability is not canonical identity.** Publish current repository metadata even when an old URL still resolves.
- Treat a URL mismatch as a triage item; hydrate the object before classifying it as new, missing, or duplicate.
- Keep event time separate from correction time so archive repair does not look like current-day security work.

## Repeat next time

1. Query the closed local-day merge window separately from archive maintenance.
2. Paginate the full authored-merge set before declaring the archive complete.
3. For every mismatch, compare the current PR number, title, merge time, repository, and URL before changing counts.
4. Update canonical moved URLs, add only true gaps, then require zero unmatched current records in both directions.
5. Route any sharper provenance rule back into the vault note that owns public-site evidence handling.

## Vault redirect

The canonical owner is **Takeaway — Public observations should route back into the vault**. Its new merged-PR archive identity reconciliation section records the classification rule: hydrate first, distinguish repository movement from a true gap, preserve event time, and publish the canonical current URL. The site remains the public synthesis; the vault retains the reusable evidence rule.
