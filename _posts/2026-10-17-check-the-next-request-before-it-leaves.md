---
layout: post
title: "2026-10-17 — Check the next request before it leaves"
date: 2026-10-17 23:59:00 +0800
permalink: /2026/10/17/check-the-next-request-before-it-leaves/
takeaway: "A rejected fetch is not proof that the forbidden destination received no request."
categories: [daily, ai-security]
tags: [ssrf, transport-security, mcp, evidence, vault-backed-learning]
---

## Signal

No authored PR merges were found for October 17 in Singapore time, and the vault scan found no target-day Markdown updates. This entry revisits an existing transport-security lesson; it does not present an older finding as new work.

## Merged PRs

None in this window.

Window: `[2026-10-17T00:00:00+08:00, 2026-10-18T00:00:00+08:00)`.

## What shipped or moved

No new code shipment, disclosure transition, or security test result was established for this window. The public PR archive needed no backfill among the 50 recently updated merged PRs checked. The daily record is the only publication change.

## Observed pattern

The vault's transport-redirect takeaway distinguishes checking a configured URL from controlling the client that actually sends requests. A guard at the API entry point does not settle what an SDK, fallback transport, or reconnect path will do next.

The review question is narrower than “does the fetch return an error?” It is “was the forbidden request prevented before network I/O?” A final response check can be too late to establish that property.

## External reference

The [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html#application-layer) recommends disabling redirect following to prevent input-validation bypass. This is a defensive reference, not evidence of a new project-specific issue.

The existing vault rule applies that concern to downstream request adapters: if redirects are required, validate each next destination before following it rather than relying on the initial URL check.

## What was learned

The established lesson is to review the request path, not just the URL field. For agent and MCP integrations, the relevant inventory includes the primary client, fallback clients, and retry or reconnect paths. Each needs an explicit answer about where destination policy is enforced.

## Takeaways

**Pair denial with evidence that the forbidden destination received no request.** An error result alone does not establish that the network boundary held.

## Repeat next time

- Identify the request primitive behind each transport, including fallbacks.
- Check redirect behavior at that primitive, not only at configuration save time.
- In an isolated test harness, record whether the denied destination receives a request and assert that it does not.
- Include an allowed destination as a positive control so a broken client cannot masquerade as a successful security guard.

These are checks to repeat, not tests executed during this finalization.

## Vault redirect

The canonical rule remains in “Transport redirect validation must live in the actual fetch path,” linked to the URL Fetch and SSRF Review checklist and the source-code discovery workflow's positive-control proof requirement. This post restates those existing rules; it introduces no new finding or heuristic requiring a duplicate vault note.
