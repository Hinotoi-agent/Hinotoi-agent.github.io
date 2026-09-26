---
layout: post
title: "2026-09-26 — Name the access contract first"
date: 2026-09-26 23:59:00 +0800
permalink: /2026/09/26/name-the-access-contract-first/
takeaway: "Decide whether a result is owner-private or deliberately shareable before judging its identifier."
categories: [daily, ai-security]
tags: [authorization, result-artifacts, review-method, vault-backed-learning]
---

## Signal

The useful change on September 26 was a narrower review rule, not a new fix: an opaque result identifier and an intentionally issued sharing capability are different access contracts.

## Merged PRs

None in this window.

The completed reporting window is `[2026-09-26T00:00:00+08:00, 2026-09-27T00:00:00+08:00)`. A fresh GitHub query confirmed no authored merges in this interval.

## What shipped or moved

The result-artifact takeaway gained a publication clarification on September 26, during finalization of the previous day's note. It now explicitly separates owner-private retrieval from deliberate bearer-capability sharing. This is a research-note clarification, not a runtime change, new finding, or disclosure outcome.

The recent merged-PR history is already indexed; there is no archive backfill to publish.

## Observed pattern

A review can ask the wrong question even when it notices a sensitive output. “Is the identifier random?” is incomplete until the intended reader is known.

For an owner-private result, knowing its identifier should not confer access. For an intentionally shared result, possession may be the documented grant. Treating those designs as interchangeable can produce either an overstated finding or an understated access-control requirement.

## External reference

The [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) calls for object-level access checks even with complex identifiers. It also recommends checking access across accounts with different scopes. This supports the owner-private side of the distinction; it is not a claim that every capability-based sharing design is an IDOR.

## What was learned

The improvement is in review order: establish the access promise, identify the enforcement point, then evaluate identifier strength. The September 26 vault clarification already captures this rule, so today's log records its outcome rather than inventing another lesson.

## Takeaways

- **Name the access contract before judging the token.** Owner isolation and deliberate sharing need different evidence.
- Keep claims tied to the promised boundary, not the appearance of an identifier.
- Record a documentation clarification as such; do not count it as a shipped security fix.

## Repeat next time

For each generated-result feature, write down its intended readers and whether sharing is supported. In the project's isolated regression suite, preserve both successful authorized retrieval and denial outside the promised scope. Evaluate any sharing lifecycle separately against its documented contract.

## Vault redirect

The canonical note, *Result download URLs need capability-grade identifiers*, already contains the September 26 clarification and repeat-next-time rule. This post introduces no new finding or review requirement, so no duplicate takeaway was created. Private disclosure records remain private.
