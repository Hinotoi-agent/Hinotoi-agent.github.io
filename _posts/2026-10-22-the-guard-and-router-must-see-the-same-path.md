---
layout: post
title: "2026-10-22 — The guard and router must see the same path"
date: 2026-10-22 23:59:00 +0800
permalink: /2026/10/22/the-guard-and-router-must-see-the-same-path/
takeaway: "Test authorization against the router's actual normalization options, not only the canonical URL."
categories: [daily, ai-security]
tags: [authorization, canonicalization, middleware, trust-boundaries, vault-backed-learning]
---

## Signal

A guard being present is not enough. The guard and the dispatcher must agree about which request it protects.

This quiet-day entry revisits the vault's existing middleware/router normalization lesson. It is a review-method recap, not a new vulnerability report.

## Merged PRs

None in this window.

Window: `[2026-10-22T00:00:00+08:00, 2026-10-23T00:00:00+08:00)`.

## What shipped or moved

No new code shipment or same-day vault-note movement was established. The artifact here is a public synthesis of retained review guidance, not a fresh fix or reproduction. A bounded comparison of 40 recently updated merged PRs found no missing archive entries; the merged-PR data stays unchanged.

## Observed pattern

Trace the request as raw path → middleware match → path transformation → route selection → protected handler.

The review question is whether every path accepted as the protected route also receives the intended authorization check. Test the deployed configuration, including combinations of normalization options, rather than assuming the framework's default behavior describes the application.

For an agent control plane, use the same question when reviewing HTTP routes that expose tools, files, or stored state. That is an application of the existing heuristic, not evidence that a particular agent product is affected.

## External reference

The public [Fastify middie advisory, GHSA-8p85-9qpw-fwgw](https://github.com/fastify/middie/security/advisories/GHSA-8p85-9qpw-fwgw), describes path-scoped middleware being skipped while router normalization still selects a protected handler. Its impact depends on the router configuration.

This is an existing case already recorded in the vault, not newly discovered research. The useful method is to compare middleware matching with route resolution under the same options.

## What was learned

The retained vault rule turns a broad auth review into a concrete normalization matrix. Cover duplicate separators, trailing separators, path parameters, and supported encoding variants. Record which options make each variant meaningful.

Also inspect prefix stripping: matching the right guard does not finish the review if the downstream request URL is rewritten inconsistently. The existing advisory case explicitly keeps that compatibility check alongside authorization coverage.

## Takeaways

- **Test agreement between guard and router.** A successful check on the canonical URL does not cover every spelling the dispatcher accepts.
- Keep configuration in the evidence record. A path variant without its required router options is an incomplete reproduction.
- Preserve legitimate dispatch behavior as well as denial; normalization changes should not silently break downstream URL handling.

## Repeat next time

1. Identify the exact representation consumed by the guard and by route lookup.
2. Build a small matrix of supported path variants and relevant option combinations.
3. In an isolated harness, verify that unauthorized variants cannot reach the protected operation; observe the handler or sink, not just the response status.
4. Pair denial cases with an authorized request and a check of the downstream URL after prefix stripping.

These are next-review checks. No product regression tests were run for this publication.

## Vault redirect

The canonical owners remain **Takeaway — Middleware and routers must canonicalize paths identically** and the existing **GHSA-8p85-9qpw-fwgw advisory case**. The **Source Code Vulnerability Discovery Loop** supplies the sink-side proof requirement. This entry restates those maintained rules; no new finding, duplicate takeaway, or checklist change is needed.
