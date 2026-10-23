---
layout: post
title: "2026-10-23 — Loading a tool is not permission to run it"
date: 2026-10-23 23:59:00 +0800
permalink: /2026/10/23/loading-a-tool-is-not-permission-to-run-it/
takeaway: "Treat deferred schema loading as discovery; authorize sensitive tools separately on the server."
categories: [daily, ai-security]
tags: [mcp, authorization, deferred-tools, trust-boundaries, vault-backed-learning]
---

## Signal

A smaller tool manifest is a context-management decision, not an access-control decision. This quiet-day entry revisits the vault's existing deferred-tool authorization lesson; it does not announce a new finding.

## Merged PRs

None in this window.

Window: `[2026-10-23T00:00:00+08:00, 2026-10-24T00:00:00+08:00)`.

## What shipped or moved

No new code shipment or same-day vault-note movement was established. Today's artifact is this review-method recap. A fresh target-window merge search was empty, and a bounded comparison of 40 recently updated merged PRs found no missing archive entries. The merged-PR data remains unchanged.

## Observed pattern

The retained review path is: deferred manifest → schema loader → callable registry → authorization decision → host-side tool.

Keep two questions separate: can the model discover the tool, and may this caller invoke it? The vault's rule is to check sensitive execution on the server before dispatch, rather than treating provider-side schema filtering as sufficient authorization.

## External reference

[DeepTutor PR #579](https://github.com/HKUDS/DeepTutor/pull/579), merged on June 21, 2026, is the existing public anchor. It changed missing MCP grants for real non-admin users to deny by default while preserving explicit grants, administrator access, and the separate partner/synthetic metadata-scoping behavior. Ordinary built-in optional-tool defaults were intentionally left alone.

The useful distinction is capability-specific grant semantics: an absent value need not mean the same thing for ordinary optional tools and deployment-configured host capabilities. This is historical shipped work, not an October merge or a fresh test result.

## What was learned

The existing takeaway makes the review narrower: inspect the loader that mutates live schemas, then follow the resulting call to its permission check. Do not stop because the initial prompt omitted a sensitive tool.

For future reviews, combine that authorization check with the discovery workflow's proof requirement: denial plus absence of the protected side effect, alongside a permitted control case. No product regression tests were run for this publication.

## Takeaways

- **Schema loading is discovery, not permission.** Keep caller grants authoritative when a tool becomes callable.
- Review missing-grant behavior explicitly for each capability family; do not inherit a permissive default accidentally.
- Preserve intentional compatibility paths without confusing them with ordinary-user permissions.

## Repeat next time

1. Trace manifest generation, schema loading, and dispatch as separate steps.
2. Check absent, empty, and explicit grants for the relevant caller classes.
3. In an isolated harness, verify denial before host-side effects and an authorized control path.
4. Record which layer the test proves; a resolver test alone is not an end-to-end execution test.

## Vault redirect

The canonical rule remains **Takeaway — Deferred tool loading is not authorization for MCP host tools**, with the **Source Code Vulnerability Discovery Loop** supplying the proof requirements. This post restates existing guidance; it creates no new finding or checklist rule, so no duplicate vault note is needed.
