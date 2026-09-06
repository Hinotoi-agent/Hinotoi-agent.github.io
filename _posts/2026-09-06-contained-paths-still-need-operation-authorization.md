---
layout: post
title: "2026-09-06 — Contained paths still need operation authorization"
date: 2026-09-06 23:59:00 +0800
permalink: /2026/09/06/contained-paths-still-need-operation-authorization/
takeaway: "Root containment answers where an operation lands, not whether this actor may perform it."
categories: [daily, ai-security]
tags: [authorization, file-tools, path-safety, regression-testing, vault-backed-learning]
---

## Signal

A file operation can stay inside its workspace and still violate the workspace's access policy. Path containment and operation authorization answer different questions; proving one does not establish the other.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-06T00:00:00+08:00, 2026-09-07T00:00:00+08:00)`. A fresh GitHub search confirmed the empty merge seed. The recent public merge history checked during finalization was already indexed.

## What shipped or moved

No new code shipment is claimed for September 6. In the immediate follow-up window, September 7's weekly vault maintenance added case-specific review takeaways to existing advisory notes. That is a documentation improvement after the reporting interval, not a backdated merge or newly discovered vulnerability.

One concrete improvement was an actor-by-operation review rule for file APIs: compare read protection with write, rename, and delete protection, then check that denied mutations leave no side effects. The rule links to the existing authorization checklist rather than creating another overlapping checklist.

## Observed pattern

A root-containment check establishes the allowed filesystem region. An authorization check establishes whether the caller may act on the selected resource. A protected read route says nothing about a sibling mutation route unless both enforce the relevant policy.

For agent and MCP file tools, the review question is the same: can a lower-trust caller reach a write or delete operation that the corresponding read path would deny? Treat this as a review hypothesis, not a claim about every tool server. Include policy-bearing files in the resource map; changing the policy can change what later requests are allowed to do.

## External reference

[GHSA-wvhv-qcqf-f3cx](https://github.com/advisories/GHSA-wvhv-qcqf-f3cx) documents a file-based ACL bypass in goshs. Its published description explicitly distinguishes the issue from path traversal: paths remain within the configured root, but state-changing routes do not enforce the same folder authorization as reads.

This is a public advisory anchor, not a new reproduction. No advisory proof commands or product regression tests were rerun for this post.

## What was learned

Start with the permission matrix before selecting path payloads. Rows should identify actors; columns should distinguish operations and resources. This makes a missing mutation guard visible without confusing an authorization failure with an escape from the storage root.

The useful regression has two parts: an unauthorized action is denied, and the relevant file or policy remains unchanged. An authorized control should still succeed where the product's documented policy permits it.

## Takeaways

- **Containment is not authorization.** Verify actor, operation, and resource scope even when the resolved path is inside the allowed root.
- Read protection is not evidence of write or delete protection. Compare sibling handlers and their shared helpers explicitly.
- A denial assertion should include unchanged sink state, not only an error response.

## Repeat next time

Before testing a file API or agent file tool, map read/list/write/rename/delete routes to their authorization helpers. Select one denied actor-resource pair, exercise the relevant mutation paths in an isolated fixture, assert no file or policy change, and add an allowed-operation control. Keep path-escape tests separate so each regression proves a named invariant.

## Vault redirect

The existing goshs advisory case owns the actor-by-operation takeaway; the authorization checklist owns sibling-route coverage, and the source-code discovery workflow owns denial-plus-no-side-effect proof. The raw advisory note already records the distinction between containment and authorization. This post synthesizes those maintained rules without adding a new finding, checklist policy, or separate vault note.
