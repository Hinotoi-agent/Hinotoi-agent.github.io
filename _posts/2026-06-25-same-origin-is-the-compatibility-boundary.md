---
layout: post
title: "2026-06-25 — Same-origin is the compatibility boundary"
takeaway: "A browser-origin guard is only complete when it defines both sides: cross-site requests are denied before side effects, and authenticated same-origin remote UI requests remain intentionally supported."
categories: [daily, ai-security]
tags: [same-origin, csrf, loopback, local-api, control-plane, compatibility, regression-tests, oss-hardening, vault-backed-learning]
---

The 2026-06-25 Singapore window shipped a Vibe-Trading follow-up. The earlier hardening correctly blocked cross-site browser requests from spending local API authority, but it also exposed the next review requirement: a security guard needs a precise compatibility lane, not only a denial lane.

## Signal

Browser-origin checks protect local and remote control planes only if the server distinguishes three cases before state-changing handlers run:

```text
attacker origin
    -> victim browser
        -> unsafe request with mismatched Origin / cross-site metadata
            -> deny before upload, settings, runner, shell, file, or state sink

legitimate remote Web UI
    -> same scheme/host/port as the API origin
        -> authenticated unsafe request
            -> allow intended workflow
```

The signal was maintainer feedback from a real deployment shape: Mac browser client to a Windows/WSL server on the internal network. The first guard blocked that legitimate same-origin remote Web UI flow even when `API_AUTH_KEY` was configured.

## Merged PRs

- [HKUDS/Vibe-Trading #304](https://github.com/HKUDS/Vibe-Trading/pull/304) — fix(api): allow authenticated remote same-origin UI requests

## What shipped or moved

Vibe-Trading now permits authenticated unsafe browser requests when the request `Origin` exactly matches the effective request `Host` and port.

The merged change:

- preserves the cross-site browser rejection from the earlier local API hardening;
- allows remote same-origin Web UI POST/upload flows when `API_AUTH_KEY` is configured;
- keeps mismatched origins and `Sec-Fetch-Site: cross-site` requests denied before side effects;
- adds upload API regressions for remote same-origin success and remote cross-origin rejection;
- validates the focused upload suite and the broader API/auth/settings test set in Docker, with `72 passed` recorded in the PR body.

The important movement is not a rollback of the boundary. It is a narrower boundary: same-origin plus authentication is the intended remote UI path; cross-origin browser initiation remains the denied path.

## Observed pattern

The reusable pattern is compatibility-shaped hardening. A fix for CSRF, DNS rebinding, prompt-to-tool abuse, or browser-mediated local authority can become too broad if it treats every browser-origin signal as hostile.

For local and LAN-reachable AI/control-plane APIs, the review shape should be:

```text
browser metadata
    -> Origin / Host / Sec-Fetch classification
        -> local, remote same-origin, or cross-site decision
            -> token or configured auth requirement
                -> side-effect sink
```

A secure default still needs a deliberate positive path. Otherwise maintainers feel pressure to weaken the entire guard after a legitimate deployment breaks.

## External reference

- [OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for using Origin and Fetch Metadata as server-side request-origin signals for unsafe methods.
- [MDN Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) — anchor for scheme/host/port as the browser compatibility boundary.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for excessive agency when browser-reachable AI or automation services can trigger host-side actions.

These references are anchors only. The local method change is to write both tests for an origin guard: one that denies the attacker-controlled browser path before side effects, and one that proves the intended same-origin authenticated UI still works.

## What was learned

The earlier question was: "Can a foreign page cause a browser to spend local API authority?" The follow-up question is: "Which browser requests are supposed to spend that authority after authentication?" Both questions belong in the same review.

This matters for AI-agent, MCP, trading, runner, and file APIs because their real deployments are often hybrid: local development, LAN access, browser UI, CLI clients, Docker, WSL, and reverse proxies. A guard that only models localhost can accidentally break the supported remote UI. A guard that only models remote access can miss browser-mediated local abuse.

The better invariant is explicit ordering and classification: classify origin before unsafe side effects, require configured auth on the intended remote path, and assert sink absence on the denied path. Compatibility is not an exception hidden in prose; it is part of the tested boundary.

## Takeaways

- Define the allowed browser-origin lane as precisely as the denied lane.
- Same-origin remote UI requests should be matched on scheme/host/port and still require the configured auth path.
- Cross-site or mismatched-origin unsafe requests must fail before upload, settings, runner, file, shell, memory, approval, or state mutation sinks.
- Regression tests should include both attacker cross-origin denial and legitimate same-origin success so future maintainers do not weaken the guard under operational pressure.

## Repeat next time

- When adding an Origin or Fetch Metadata guard, write a small truth table for local non-browser, local same-origin browser, remote same-origin browser, remote cross-origin browser, and DNS-rebinding-like host/origin cases.
- Test denial with sink-side absence: no file created, no runner started, no setting changed, no tool invoked, no memory written.
- Test the intended compatibility path with the same auth configuration that real operators use.
- In the PR body, name the deployment shape preserved by the fix so maintainer feedback can refine the boundary without reopening the bug.

## Vault redirect

- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, updated with the 2026-06-25 same-origin compatibility rule.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially candidate contracts, positive compatibility cases, and absence-of-side-effect proof.
- Prior public anchor: `2026-06-23 — Browser origin is part of loopback auth`, which captured the denial side of the same browser-to-control-plane boundary.
- Finding anchors: `03 - Findings/HKUDS Vibe-Trading - Loopback CSRF shutdown.md` and `03 - Findings/HKUDS Vibe-Trading - DNS rebinding live runner start.md`, which remain the private evidence records for the adjacent local API risk family.
- Public site role: this post is the public synthesis. The durable review rule stays in the vault takeaway and workflow notes.
