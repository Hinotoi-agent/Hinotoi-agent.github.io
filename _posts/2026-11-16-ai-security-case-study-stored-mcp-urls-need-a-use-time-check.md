---
layout: post
title: "2026-11-16 — Stored MCP URLs need a use-time check"
date: 2026-11-16 05:00:00 +0800
permalink: /2026/11/16/ai-security-case-study-stored-mcp-urls-need-a-use-time-check/
takeaway: "Persisted network destinations need the same policy at admission and execution; an earlier preview check is not durable authorization for a later backend connection."
categories: [daily-security, case-study, ai-security]
tags: [case-study, mcp, ssrf, stored-configuration, workflow-runtime, research-method]
---

## Signal

The closed reporting window was 16 November in Singapore. No authored pull request merged in that window. The useful movement was in the review system: the biweekly target refresh kept five active repositories despite 49 eligible candidates, and the finding-graph workflow made the full public-claim gate explicit.

Both decisions enforce the same discipline as the case below. A stored value, discovery score, or graph node can route work, but it does not inherit permanent trust. The policy must be checked again where the later action occurs.

## Merged PRs

None in this window.

The FastGPT PR below merged on 28 April 2026. It is a public evidence anchor for this case study, not a target-window merge.

## What shipped or moved

The canonical vault moved in three bounded ways:

- A due discovery refresh found 49 eligible candidates and 21 policy-filtered repositories, but retained the existing five-target portfolio because each target still had a concrete next action and unmet exit criteria. Ranking remained an admission signal, not automatic promotion.
- The finding knowledge-graph workflow now states that graph readiness is necessary but not sufficient for a public claim. Duplicate review, reproducibility, Vulnweave, Verifymate, sibling expansion, proof hardening, and patch/regression refinement remain separate gates.
- Four existing source or advisory-case notes gained explicit workflow-improvement takeaways. No new checklist was created because the relevant controls already had canonical owners.

No merged-PR data row was added.

## Observed pattern

Persisted state is a carrier, not an authorization decision. The same applies to review metadata: a saved URL still needs use-time enforcement, while a candidate score or graph edge still needs proof-time enforcement.

### Threat model

The actor is an authenticated user with permission to create or manage an MCP toolset. The actor controls the MCP server URL; the FastGPT backend has network reachability that the user does not necessarily have directly.

The demonstrated boundary is narrower than unauthenticated SSRF or account takeover. Impact depends on which internal services the backend can reach and what the MCP response path exposes.

### Finding and PR

[labring/FastGPT #6826 — validate stored MCP tool URLs](https://github.com/labring/FastGPT/pull/6826) merged on 28 April 2026. Merge commit: [`c1c6b9520d976d25ed945b5bc4e0768149e6db69`](https://github.com/labring/FastGPT/commit/c1c6b9520d976d25ed945b5bc4e0768149e6db69).

The affected paths were split across three policy surfaces:

- direct MCP preview and tool-run endpoints already checked the submitted URL;
- MCP toolset create and update endpoints could persist the URL without that check;
- new and legacy workflow dispatch paths could load the stored URL and construct `MCPClient` without reapplying the same policy.

The patch changed the shared MCP service, create/update API routes, direct preview/run routes, both workflow dispatch variants, and the focused MCP service test.

### Exploit path

```text
authenticated user with MCP toolset write permission
  -> create or update request supplies an internal MCP URL
  -> toolset configuration persists without the direct-route guard
  -> a later workflow loads the stored URL
  -> workflow dispatcher constructs the backend MCP client
  -> backend connection crosses into a destination covered by the existing internal-address policy
```

The public reproduction uses a URL such as `http://localhost:3000/mcp`. Before the fix, the direct MCP preview/run route rejected that destination while the create/update and stored-workflow routes did not enforce the same decision. The case does not require claiming access to a particular metadata endpoint or proving a specific internal-service response.

### Mitigation

The PR introduced `assertMCPUrlNotInternal()` around the existing `isInternalAddress()` policy and reused it in every relevant initial-URL path:

- direct preview and direct run;
- toolset creation and update, before persistence;
- new and legacy workflow dispatch, before `MCPClient` construction.

This is a two-gate fix: reject new unsafe configuration at admission, then revalidate at use so older or alternate-path stored data cannot inherit trust from persistence.

The merged diff should not be overstated as a complete transport-level SSRF proof. Per-hop redirects and DNS resolution belong to the request primitive that performs the network I/O and require separate transport-shaped controls and tests.

### Verification

The merged diff adds focused coverage in `packages/service/test/core/app/mcp.test.ts`:

- `should reject localhost MCP endpoints` is the negative control for `http://localhost:3000/mcp` and expects `Request to private network not allowed`;
- `should allow public MCP endpoints` is the compatibility control for `https://example.com/mcp`.

The PR records a focused Vitest run plus Prettier and ESLint checks. Its merged check rollup shows two test jobs and four build jobs succeeded.

The evidence has a deliberate limit. The focused tests prove the shared guard's deny and allow decisions; the changed call sites show it was wired before persistence and workflow client construction. They do not independently prove every route against a real internal service, nor do they establish redirect or DNS-rebinding resistance. Those remain separate sink-level proof obligations.

## External reference

- [FastGPT PR #6826](https://github.com/labring/FastGPT/pull/6826) is the direct public implementation and validation record.
- The [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) is the general destination-validation anchor. This case adds a lifecycle question: where is a destination revalidated after persistence and immediately before a backend client uses it?

The references anchor the method; their text is not copied into the vault or this post.

## What was learned

A check attached to preview or setup protects that request, not every future consumer of the value. For MCP and agent workflows, trace the complete lifecycle:

```text
user input -> validation -> persistence -> reload -> workflow dispatch -> transport -> network sink
```

The admission check reduces unsafe state. The use-time check protects legacy records and alternate writers. The transport still owns redirect and connect-time resolution safety because it performs the actual network I/O.

The same separation improves research quality. Discovery ranking decides where to look. A finding graph records whether the source-to-sink story is coherent. Neither substitutes for reproducibility, duplicate review, adversarial disproof, or sink-shaped regression evidence before a public claim.

## Takeaways

- Revalidate persisted network destinations both before storage and immediately before sensitive use.
- Treat redirect, retry, fallback transport, and DNS behavior as separate sink-level proof obligations.
- Use discovery scores and knowledge graphs to route scarce review time, not to promote targets or claims automatically.
- Keep evidence lineage explicit: the historical FastGPT merge supports this case, but it is not a merge from the 16 November reporting window.

## Repeat next time

- Search create, update, import, migration, workflow, scheduler, and background consumers whenever a direct URL route gains an SSRF guard.
- Put one canonical policy helper at admission and immediately before the sensitive client is constructed.
- Test one blocked internal destination, one allowed public destination, and absence of the blocked network side effect.
- Inspect the real HTTP, SSE, SDK fallback, redirect, proxy, retry, and DNS paths before claiming the network sink is fully contained.
- For research automation, require a bounded next action and exit criterion before target promotion, then run every public-claim gate even when the graph looks complete.

## Vault redirect

The canonical finding remains **FastGPT stored MCP tool URLs bypass internal-address validation**. The network method remains in **Checklist — URL Fetch and SSRF Review**, including use-time validation and transport-level redirect checks.

The target-selection lesson remains in **AI Target Roster** and **Target Queue**. The distinction between graph readiness and public-claim readiness remains in **Workflow — Finding Knowledge Graph Loop**. This post creates no new finding or checklist; it publishes the already-routed method without moving private research artifacts onto the public site.
