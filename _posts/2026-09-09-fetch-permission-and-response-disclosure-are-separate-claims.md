---
layout: post
title: "2026-09-09 — Fetch permission and response disclosure are separate claims"
date: 2026-09-09 23:59:00 +0800
permalink: /2026/09/09/fetch-permission-and-response-disclosure-are-separate-claims/
takeaway: "Prove caller access, destination control, and returned information separately; a parser error is not an egress guard."
categories: [daily, ai-security]
tags: [ssrf, network-boundaries, evidence-quality, oss-hardening, vault-backed-learning]
---

## Signal

A server-side fetch has more than one security question. Who may request it? Where may it connect? What information may come back to the caller? Collapsing those questions into a single “SSRF” label makes both mitigation and impact statements less precise.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-09T00:00:00+08:00, 2026-09-10T00:00:00+08:00)`. A fresh GitHub merge search confirmed the empty window. The recent public merges checked during finalization were already indexed.

## What shipped or moved

No new code shipment or September 9 vault edit is claimed. This entry draws on the existing Arcane advisory case, whose September 7 maintenance sharpened a review rule: establish caller reachability, destination control, and response reflection independently.

The maintained URL-fetch checklist already covers the corresponding controls, including the actual network client, redirect handling, and reflected errors. This is a synthesis of that recorded improvement, not a newly discovered issue or a new product validation result.

## Observed pattern

Response parsing happens after the network action. Rejecting an unexpected document format does not establish that the connection was prevented. Conversely, reaching a destination does not by itself prove that its complete response can be disclosed.

For agent media loaders, template importers, and MCP-related network clients, keep those boundaries distinct. Enforce destination policy before network I/O, then separately limit what response content and diagnostics can reach the caller. Authentication is another independent decision; it does not replace destination restrictions.

## External reference

[GHSA-ff24-4prj-gpmj](https://github.com/advisories/GHSA-ff24-4prj-gpmj), published in April, describes Arcane's unauthenticated template-fetch SSRF with conditional response reflection. Its details distinguish compatible structured responses from more limited information exposed through parsing and transport errors.

That distinction is the evidence anchor: response disclosure depends on observed handling, not merely on the presence of a fetch. No reproduction or product regression suite was run for this post.

## What was learned

A useful security record should say which boundary failed and how far the evidence goes. “The server attempted a prohibited connection” and “the caller received sensitive response content” are different claims with different proof requirements.

The same discipline improves defensive tests. A denied destination should produce no prohibited outbound request, rather than merely an eventual parse error. An allowed fetch should still work through the intended client. Response filtering needs its own assertions instead of borrowing confidence from the destination check.

## Takeaways

- **Separate access, egress, and disclosure evidence.** Do not let one successful observation stand in for the other two.
- Treat parser failures as response-handling outcomes, not proof that network policy held.
- Keep reflected-data impact conditional on what the caller can actually receive.

## Repeat next time

Before reviewing a URL-consuming feature, write down the caller policy, destination policy, and response policy separately. Use isolated, controlled fixtures to verify that denied requests do not reach the network sink and that permitted requests still succeed. Check that redirects and fallback clients use the same destination controls. Record response exposure independently and bound the report to those observations.

## Vault redirect

The existing Arcane advisory case owns the three-part evidence rule. The URL Fetch and SSRF Review checklist owns destination and reflected-response checks; the transport-redirect lesson owns coverage of the real network path. The source-code discovery workflow already requires denial without side effects and a positive compatibility control. This post restates those maintained rules without creating a parallel finding or a duplicate checklist.
