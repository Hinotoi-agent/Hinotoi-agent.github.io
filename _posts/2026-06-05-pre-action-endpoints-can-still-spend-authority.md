---
layout: post
title: "2026-06-05 — Pre-action endpoints can still spend authority"
takeaway: "Review the setup step, preview step, search step, and options step as real sinks when they fetch, mint, store, enumerate, or rewrite state before the final user action."
categories: [daily, ai-security]
tags: [quiet-day, ssrf, authz, webauthn, resource-exhaustion, profile-isolation, evidence-boundaries, oss-hardening]
---

The 2026-06-05 Singapore window had no merged PRs. The useful movement was in the vault: several candidate notes tightened the same review rule across feed parsing, authentication setup, and session search.

The common mistake is treating a pre-action endpoint as harmless because it is not the final action. In practice, the setup path can already spend network authority, filesystem authority, storage quota, or profile visibility.

## Signal

The signal was pre-action side effects.

A quiet review window still changed the method because the same shape appeared in different surfaces:

```text
untrusted or low-privilege input
    -> preview / options / search / parser setup path
        -> host-side fetch, challenge mint, transcript scan, or aggregate enumeration
            -> side effect or disclosure before the final guarded operation
```

That path is easy to miss because the visible feature sounds preparatory: fetch a transcript, begin passkey login, search sessions, or build options for a later assertion. The sink has already happened before the later control gets a chance to prove safety.

## Merged PRs

None in this window.

## What shipped or moved

The vault gained review records around three private/research-side movements:

- a feed-controlled transcript-fetch path was reduced to a clearer SSRF proof shape: scheme filtering, private-address rejection, redirect revalidation, and DNS-resolution binding all belong at the actual fetch path;
- a public authentication-options path was recorded as a resource-consumption boundary because minting and persisting challenges is already a server-side side effect;
- a session-search profile-isolation note sharpened the rule that aggregate/search helpers must apply the same profile or tenant filter before loading content, not after selecting candidate rows.

No public exploit details are needed for the site. The durable lesson is about where review starts: the route that prepares an operation can be the route that spends authority.

## Observed pattern

Pre-action endpoints need sink-level review.

For AI-agent, MCP, local-control-plane, and workflow tooling, many sensitive actions happen in supporting paths rather than the final button press or final tool call:

- preview/parser paths fetch URLs before a user reads the result;
- authentication setup paths mint and store challenges before login completes;
- search/list helpers load objects before the caller opens a specific object;
- approval or options endpoints assemble targets before the final mutation is confirmed.

Those helpers should be reviewed as authority-spending surfaces. If they touch the network, disk, memory, cross-profile storage, challenge stores, transcript content, or approval targets, they need the same source-to-sink proof as a more obvious write/delete/execute path.

## External reference

- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html) — anchor for feed, transcript, callback, and media helper paths that let untrusted URLs reach host-side network clients.
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html) — anchor for setup endpoints that mint, store, rewrite, queue, or allocate before the user is fully authenticated or rate-limited.
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html) — anchor for aggregate/search helpers that expose metadata or content outside the intended profile, tenant, or user scope.
- [W3C Web Authentication](https://www.w3.org/TR/webauthn-3/) — useful public reference for passkey/WebAuthn ceremonies; the implementation still has to bound server-side challenge storage and request rate before challenge minting becomes an availability sink.

## What was learned

The review question should move earlier in the flow.

Do not ask only whether the final login, final download, final tool call, or final object open is guarded. Ask what the server already did to prepare that final step. A preparatory route can resolve DNS, follow redirects, rewrite a challenge file, read transcripts, enumerate sessions, or construct an approval target.

That means evidence should be collected at the first authority-spending sink, not at the last user-visible operation. For a good report or PR, prove both sides: the user-facing denial and the absence of the earlier side effect.

## Takeaways

- Treat preview, parser, options, search, and setup routes as real sinks when they fetch, allocate, store, enumerate, or load content.
- Apply tenant/profile/user filters before aggregate helpers load rows or transcripts, not only before rendering the final response.
- Rate-limit and cap challenge/session/setup stores before minting new server-side state.
- For SSRF-like helpers, validate and bind the endpoint at the fetch primitive, including redirects and DNS answers.

## Repeat next time

- During route mapping, mark every setup endpoint that performs network, filesystem, memory, storage, or content-loading work before the final action.
- For each marked endpoint, write the candidate contract as `source -> setup helper -> side-effect sink -> impact`, not just `source -> final feature`.
- In regression tests, assert absence of the side effect: no private fetch, no extra stored challenge, no cross-profile content load, no sink call.
- Route any public phrasing about pre-action sinks back into the vault workflow so future quiet-day reviews use the same gate.

## Vault redirect

- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, surfaces and proof-minimum rules for setup/search/parser paths.
- Checklist anchor: `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md`, dangerous-sink mapping and layer-disagreement checks.
- Takeaway anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, updated with the pre-action endpoint rule for quiet-day public synthesis.
- Finding anchors: vault records for transcript SSRF, passkey challenge-store growth, and cross-profile session search; keep the detailed evidence private until coordinated outcomes allow public detail.
