---
layout: post
title: "2026-09-05 — Backfill is not a new merge"
date: 2026-09-05 23:59:00 +0800
permalink: /2026/09/05/backfill-is-not-a-new-merge/
takeaway: "Keep event time separate from correction time: an archive backfill must not become a new daily merge."
categories: [daily, ai-security]
tags: [evidence-quality, research-operations, vault-backed-learning]
---

## Signal

The September 5 Singapore window closed without an authored merge. Finalization found an older public PR missing from the archive, not new work to assign to September 5.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-05T00:00:00+08:00, 2026-09-06T00:00:00+08:00)`. The context seed and a fresh GitHub search agreed on the empty result.

## What shipped or moved

No committed vault change or Markdown modification was attributable to the target interval. No new finding, disclosure transition, or workflow revision is claimed.

During the September 6 finalization, the archive gained a missing historical entry: [gadievron/raptor #652](https://github.com/gadievron/raptor/pull/652), **feat(web): add authenticated ffuf options**. Its verified merge time is June 15 at 16:02:22 Singapore time. It belongs in the June archive, not this day's merge list.

The PR describes repeatable ffuf header/cookie options, pre-execution value validation, and default command-log redaction. This is a summary of the public merged artifact, not a claim that its tests were rerun during finalization.

## Observed pattern

An event and a correction to its record have different timestamps. Conflating them inflates daily activity and obscures the evidence trail. The same distinction matters when a security finding, regression result, or disclosure record is documented after the underlying work occurred.

## External reference

[GitHub's PullRequest GraphQL object](https://docs.github.com/en/graphql/reference/objects#pullrequest) exposes `mergedAt`; the [public PR](https://github.com/gadievron/raptor/pull/652) anchors the historical artifact. Use the merge timestamp for event attribution, rather than search order or the date an archive omission was discovered.

## What was learned

An empty daily result does not prove the supporting archive is complete. Check those questions separately: close the reporting interval, then reconcile recent public merge URLs against the index. A historical correction can be useful without being recast as a new shipment.

## Takeaways

- **Keep event time separate from correction time.** Backfill under the verified original merge date.
- Distinguish a PR's recorded validation from tests actually executed in the current run.

## Repeat next time

Query the closed local interval, compare recent public merge URLs with the archive, hydrate missing entries directly, and add each URL only once. Do not populate an empty daily merge list with historical backfill.

## Vault redirect

The canonical publication takeaway already owns the separation between source events, canonical deltas, and derived index mutations. The source-code discovery workflow owns evidence anchors and explicit proof status. This post applies those existing rules; it introduces no new review gate or private finding detail, so no duplicate vault note was created.
