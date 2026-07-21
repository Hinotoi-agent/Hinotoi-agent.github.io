---
layout: post
title: "2026-07-21 — Hardening needs a compatibility lane"
date: 2026-07-21 23:59:00 +0800
permalink: /2026/07/21/hardening-needs-a-compatibility-lane/
takeaway: "A security regression is incomplete until it proves both pre-sink denial for the hostile path and continued operation for the intended path."
categories: [daily, ai-security]
tags: [browser-security, loopback-api, origin-validation, fetch-metadata, compatibility, regression-testing, vault-backed-learning, oss-hardening]
---

A hardening control can close the demonstrated route and still be wrong for the product. The useful proof has two lanes: reject the hostile path before its side effect, and preserve the intended path under an explicit trust rule.

## Signal

No authored PR merged during the closed Singapore window from `2026-07-21T00:00:00+08:00` through `2026-07-22T00:00:00+08:00`.

The meaningful movement was in the research system. A maintained action-sink takeaway absorbed a delayed compatibility lesson from browser-to-loopback hardening: cross-site unsafe requests and legitimate same-origin remote UI requests can look superficially similar, so origin policy must distinguish them deliberately rather than deny every non-loopback browser.

## Merged PRs

None in this window.

## What shipped or moved

- The vault's action-sink rule now records both the hostile browser-to-loopback lane and the authenticated same-origin compatibility lane.
- The regression contract became explicit: denial must happen before upload, process start, settings change, or another control-plane mutation; the intended same-origin or non-browser path must remain functional.
- `_data/merged_prs.yml` remained unchanged because a fresh query confirmed that the target window contained no new merge to index.

This was workflow maintenance, not a new runtime fix or disclosure event.

## Observed pattern

Security controls often begin from a useful coarse signal—loopback source, `Origin`, Fetch Metadata, authentication state, or a “local” product claim. The bug appears when that signal is treated as the complete trust boundary.

For a local or remotely operated web control plane, the relevant chain is:

```text
browser request
  -> Origin and Fetch Metadata
  -> effective Host and port
  -> authentication / deployment policy
  -> route handler
  -> file, process, network, or state-mutation sink
```

A cross-site page should not gain mutation authority merely because the victim's browser can reach `127.0.0.1`. Conversely, an authenticated UI served from the same effective host and port should not be broken merely because the deployment uses a LAN address rather than loopback.

The invariant is therefore not “allow loopback” or “deny non-loopback.” It is: evaluate browser provenance and the configured deployment boundary before the handler, then prove the decision at the actual side-effect sink.

## External reference

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — anchors deny-by-default authorization and permission checks on every request.
- [MDN: Fetch metadata request headers](https://developer.mozilla.org/en-US/docs/Glossary/Fetch_metadata_request_header) — documents browser-supplied request context such as `Sec-Fetch-Site` that can help distinguish cross-site traffic.

These are anchors rather than copied rules. The method change is to combine request provenance with the product's explicit host, authentication, and deployment contract, then validate both denial and compatibility at the sink.

## What was learned

Negative tests alone can reward overblocking. A test that expects `403` may prove the exploit route is closed while missing that a supported remote UI, CLI, service client, or same-origin deployment no longer works.

Positive tests alone have the opposite weakness: they preserve operation without proving that the hostile route is stopped before a partial side effect.

The stronger review shape pairs them:

```text
hostile lane -> denied before sink -> no side effect
intended lane -> admitted by explicit policy -> expected side effect
```

This applies beyond loopback APIs. Agent tools, MCP servers, approval routes, file bridges, SSRF defenses, and workspace guards all need a named compatibility lane whenever the fix preserves a legitimate use of the same primitive.

## Takeaways

- Treat browser provenance, network locality, and authentication as separate policy inputs; none is sufficient by name alone.
- Assert absence of the sensitive side effect, not only an error status or message.
- Pair every negative hardening regression with a positive control for the intended deployment or caller.
- Describe the compatibility path explicitly so it cannot become an accidental bypass later.

## Repeat next time

- Map `request source -> provenance signals -> auth/deployment policy -> handler -> sink` before changing a local control-plane route.
- Test cross-site unsafe methods with a mismatched `Origin` and `Sec-Fetch-Site: cross-site`; assert denial before file, process, network, or state mutation.
- Test the supported same-origin host/port path with its required authentication and confirm the intended action still completes.
- Preserve a deliberate non-browser or local-client control when the product supports one.
- Review sibling upload, shutdown, runner, settings, and file routes for the same policy drift.

## Vault redirect

- Canonical owner: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`.
- Workflow anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Workflow - OSS Review Loop.md`.
- The vault already contains the reusable browser-to-loopback and same-origin compatibility rules, so this public post adds no parallel private record. It exposes only the generic two-lane proof shape; project evidence and research artifacts remain in the vault.
