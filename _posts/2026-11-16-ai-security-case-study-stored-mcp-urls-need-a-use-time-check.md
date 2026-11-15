---
layout: post
title: "2026-11-16 — Stored MCP URLs need a use-time check"
date: 2026-11-16 05:00:00 +0800
permalink: /2026/11/16/ai-security-case-study-stored-mcp-urls-need-a-use-time-check/
takeaway: "Persisted network destinations need the same policy at admission and execution; an earlier preview check is not durable authorization for a later backend connection."
categories: [case-study, ai-security]
tags: [case-study, mcp, ssrf, stored-configuration, workflow-runtime]
---

## Signal

FastGPT already rejected internal MCP destinations on direct preview and tool-run routes. The same URL could still take a different route: save it as MCP tool configuration, then let a later workflow load it and construct the backend client.

The useful signal is policy drift across time. A URL checked in one interactive request is not automatically safe when persisted data reaches a later execution path.

## Threat model

The actor is an authenticated user with permission to create or manage an MCP toolset. The actor controls the MCP server URL; the FastGPT backend has network reachability that the user does not necessarily have directly.

The demonstrated boundary is narrower than unauthenticated SSRF or account takeover. Impact depends on which internal services the backend can reach and what the MCP response path exposes.

## Finding and PR

[labring/FastGPT #6826 — validate stored MCP tool URLs](https://github.com/labring/FastGPT/pull/6826) merged on April 28, 2026. Merge commit: [`c1c6b9520d976d25ed945b5bc4e0768149e6db69`](https://github.com/labring/FastGPT/commit/c1c6b9520d976d25ed945b5bc4e0768149e6db69).

The affected paths were split across three policy surfaces:

- direct MCP preview/run endpoints already checked the submitted URL;
- MCP toolset create/update endpoints could persist the URL without that check;
- new and legacy workflow dispatch paths could load the stored URL and construct `MCPClient` without reapplying the same policy.

The patch changed the shared MCP service, create/update API routes, direct preview/run routes, both workflow dispatch variants, and the focused MCP service test.

## Exploit path

```text
authenticated user with MCP toolset write permission
  -> create or update request supplies an internal MCP URL
  -> toolset configuration persists without the direct-route guard
  -> a later workflow loads the stored URL
  -> workflow dispatcher constructs the backend MCP client
  -> backend connection crosses into a destination covered by the existing internal-address policy
```

The public reproduction uses a URL such as `http://localhost:3000/mcp`. Before the fix, the direct MCP preview/run route rejected that destination while the create/update and stored-workflow route did not enforce the same decision. The case does not require claiming access to a particular metadata endpoint or proving a specific internal service response.

## Mitigation

The PR introduced `assertMCPUrlNotInternal()` around the existing `isInternalAddress()` policy and reused it in every relevant initial-URL path:

- direct preview and direct run;
- toolset creation and update, before persistence;
- new and legacy workflow dispatch, before `MCPClient` construction.

This is a two-gate fix: reject new unsafe configuration at admission, then revalidate at use so older or alternate-path stored data cannot inherit trust from persistence.

The merged diff should not be overstated as a complete transport-level SSRF proof. Per-hop redirects and DNS resolution belong to the actual request primitive and require separate transport-shaped controls and tests.

## Verification

The merged diff adds focused coverage in `packages/service/test/core/app/mcp.test.ts`:

- `should reject localhost MCP endpoints` is the negative control for `http://localhost:3000/mcp` and expects `Request to private network not allowed`;
- `should allow public MCP endpoints` is the compatibility control for `https://example.com/mcp`.

The PR records a focused Vitest run plus Prettier and ESLint checks. Its public check rollup shows two test jobs and four build jobs passed on the merged head.

The evidence has a deliberate limit. The focused tests prove the shared guard's deny and allow decisions; the changed call sites show it was wired before persistence and workflow client construction. They do not independently prove every route with a real internal service, nor do they establish redirect or DNS-rebinding resistance. Those remain separate sink-level proof obligations.

## What was learned

Stored configuration is a carrier, not a trust boundary. A security check attached only to preview or setup protects that request, not every future consumer of the value.

For MCP and agent workflows, trace a destination through both phases:

```text
user input -> validation -> persistence -> reload -> workflow dispatch -> transport -> network sink
```

The admission check reduces unsafe state. The use-time check protects legacy records and alternate writers. The transport still owns redirect and connect-time resolution safety because it performs the actual network I/O.

## Repeat next time

- Search create, update, import, migration, and workflow/background consumers whenever a direct URL route gains an SSRF guard.
- Put one canonical policy helper at admission and immediately before the sensitive client is constructed.
- Test one blocked internal destination and one allowed public destination.
- Add route-level or dispatcher-level coverage so helper correctness and real call-site wiring are separate assertions.
- Inspect the real HTTP, SSE, SDK fallback, redirect, proxy, and DNS paths before claiming the network sink is fully contained.

## Vault redirect

The canonical finding remains **FastGPT stored MCP tool URLs bypass internal-address validation**. The reusable method belongs to **Checklist — URL Fetch and SSRF Review**: validate persisted destinations before storage, revalidate them at use, and separately prove that the actual transport enforces redirect and connect-time policy.

This post adds no new finding. It publishes the existing admission-versus-execution lesson without moving private research artifacts onto the public site.
