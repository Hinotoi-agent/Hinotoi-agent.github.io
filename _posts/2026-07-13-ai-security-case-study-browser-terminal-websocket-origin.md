---
layout: post
title: "2026-07-13 — Browser terminal WebSockets need an origin gate"
date: 2026-07-13 05:00:26 +0800
permalink: /2026/07/13/ai-security-case-study-browser-terminal-websocket-origin/
takeaway: "A browser WebSocket carrier is not actor proof; cookie-authenticated terminal sockets need same-origin admission before the terminal hub accepts the connection."
categories: [daily, case-study, ai-security]
tags: [case-study, browser-origin, websocket, csrf, terminal, control-plane, oss-hardening]
---

The useful case this week is a browser-origin boundary on a terminal WebSocket. The bug class is familiar, but the sink changes the impact: once a socket is accepted, the browser carrier can become a terminal-control channel under the victim's cookie-backed session.

## Signal

[`openclaw/crabfleet #67`](https://github.com/openclaw/crabfleet/pull/67) fixed `/api/terminal/ws` so browser-cookie terminal WebSocket upgrades are checked against the browser-visible Crabfleet origin before they reach the terminal hub.

The signal was not just "WebSocket endpoint exists." The stronger signal was:

```text
browser-controlled page -> cross-site WebSocket handshake -> ambient session cookie -> terminal hub -> terminal output/input
```

For agent and automation products, terminal-like surfaces are control-plane sinks. If the route accepts a browser carrier without proving same origin, a signed-in user's session can be reused by a page they did not intend to grant terminal access to.

## Merged PRs

None in this window.

The case-study anchor below is an earlier merge from 2026-07-01, not a merge from the closed Singapore window `2026-07-13T00:00:00+08:00` through `2026-07-14T00:00:00+08:00`.

## What shipped or moved

No PR merged in the target window, so `_data/merged_prs.yml` did not need an archive entry.

What moved was the evidence model. This case study turned the earlier Crabfleet fix into a reusable browser-to-control-plane review chain: identify the browser carrier, separate ambient session proof from origin proof, place the admission gate before socket acceptance, and verify both the rejected side effect and the intended compatibility lanes.

The vault-side owner was also made explicit. The public observation routes back to the source-code discovery workflow and the existing public-observation takeaway rather than becoming a website-only rule.

## Observed pattern

**A credential-bearing carrier is not actor proof.** A session cookie can establish who the server associates with a request without proving that the browser context using that cookie is allowed to reach a terminal, agent, MCP, workflow, or automation sink.

For browser WebSockets, the boundary is admission order:

```text
carrier -> session proof -> browser-origin proof -> route authorization -> socket acceptance -> sink
```

If origin validation happens after the terminal hub accepts the socket, the check is too late. If compatibility is preserved through non-browser or service-authenticated paths, those lanes should be named and tested rather than left as implicit exceptions.

## Threat model

The attacker controls a web page. The victim is signed in to a Crabfleet deployment and visits that page.

Browsers can initiate cross-site WebSocket handshakes and attach ambient cookies. CORS response-read protections are not the boundary here; the server has to decide whether the WebSocket `Origin` is allowed before accepting the upgrade.

The case is strongest when the victim has terminal-control grants and a live or discoverable session ID. Under those conditions, the attacker's page can try to open the terminal socket as the victim's browser session.

## Finding and PR

Public PR: [`openclaw/crabfleet #67 — [security] fix(terminal): validate browser websocket origin`](https://github.com/openclaw/crabfleet/pull/67).

Merge commit: `ebc61eabc18488289251d68c66a7d12263a19fb4`.

The PR changed:

- `src/worker/session-terminal-route.ts` — added the terminal WebSocket origin validator using the existing browser-visible origin helper.
- `src/worker/worker-application.ts` — called the validator before opening the terminal hub and kept service-authenticated terminal paths explicit.
- `tests/session-terminal-route.test.ts` — added regression coverage for rejected cross-origin browser handshakes and allowed compatibility paths.

The important boundary was admission order. Browser-origin validity had to be checked before `/api/terminal/ws` was handed to `TerminalHub.open(...)`.

## Exploit path

The source-to-sink chain was:

```text
attacker.example page
  -> opens wss://<crabfleet>/api/terminal/ws
  -> browser includes the victim's Crabfleet session cookie
  -> route resolves a browser-authenticated user
  -> terminal hub accepts the WebSocket without comparing Origin
  -> attacker-controlled page can interact with terminal sessions the victim may access
```

The failure was not a missing terminal permission check. The drift was earlier: the route treated the browser-carried cookie as enough proof that the request came from the Crabfleet UI.

For this class, the actor proof has two parts:

- session proof: the cookie identifies a signed-in user;
- browser-origin proof: the handshake came from the browser-visible Crabfleet origin, not an attacker-controlled site.

Pre-fix, the second proof was missing for the browser terminal WebSocket path.

## Mitigation

The fix added `validateTerminalWebSocketOrigin(...)` before the terminal hub accepts non-service terminal WebSocket requests.

The guard compares the request `Origin` with the browser-visible request origin via the existing `browserRequestOrigin(request, env)` primitive. That matters because deployments can sit behind trusted proxies or be reached through direct tenant/local origins. The mitigation did not invent a parallel origin policy; it reused the product's existing browser-visible origin calculation.

The compatibility lanes stayed explicit:

- same-origin browser terminal requests remain allowed;
- direct tenant/local browser origins remain allowed when they are the visible request origin;
- trusted-proxy public origins remain allowed;
- non-browser clients without an `Origin` remain allowed;
- SSH gateway and GitHub Actions agent terminal requests remain on the service-authenticated path.

That shape is the useful trade-off: deny cross-site browser carriers without breaking deliberate non-browser or service-authenticated terminal flows.

## Verification

The PR named both regression tests and a redacted runtime proof.

Regression coverage was added in `tests/session-terminal-route.test.ts` for:

- canonical same-origin browser terminal handshakes;
- direct tenant/local same-origin handshakes;
- trusted-proxy public-origin handshakes;
- cross-origin browser rejection;
- origin-less non-browser clients;
- service-authenticated terminal requests.

The PR test plan recorded these commands:

```text
pnpm exec node --test --experimental-strip-types tests/session-terminal-route.test.ts tests/deployment.test.ts tests/terminal-hub.test.ts
docker run --rm -v "$PWD":/repo:ro -w /repo node:22 node --test --experimental-strip-types tests/session-terminal-route.test.ts tests/deployment.test.ts tests/terminal-hub.test.ts
node --experimental-strip-types .huntpack/terminal-origin-runtime-proof.mjs
docker run --rm -v "$PWD":/repo:ro -w /repo node:22 node --experimental-strip-types .huntpack/terminal-origin-runtime-proof.mjs
pnpm run check && pnpm test
git diff --check
```

The redacted proof shape is the part to repeat:

```text
cross-origin browser terminal: REJECT status=403
same-origin browser terminal: ACCEPT status=101
direct tenant browser terminal: ACCEPT status=101
service-authenticated terminal: ACCEPT status=101
```

That proves both sides of the boundary: the bad browser carrier is denied before socket acceptance, while the intended same-origin, direct/local, and service-authenticated paths still work.

## External reference

- [`openclaw/crabfleet #67`](https://github.com/openclaw/crabfleet/pull/67) is the public evidence anchor: affected route, mitigation, changed files, merge commit, regression cases, and redacted runtime proof.
- [OWASP WebSocket Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html) is the method anchor for server-side origin validation and explicit WebSocket authorization.

The review-method change is narrower than either source alone: map the carrier and actor proof separately, enforce the browser-origin gate before the control-plane sink accepts state, and test the deliberate compatibility paths alongside the denial.

## What was learned

A WebSocket route needs its own browser-origin admission rule when the sink is authenticated by ambient browser state.

For terminal, agent, MCP, workflow, and automation surfaces, the server should not collapse "has a cookie" into "came from the product UI." The carrier and the actor are different facts. The carrier is a browser handshake; the actor proof is the authenticated session plus the origin boundary that says the browser context is allowed to use that session for this sink.

The reusable review question is: **before accepting the socket or starting the side effect, what proves this browser-carried credential came from the intended origin?**

## Takeaways

- Treat cookie authentication and browser-origin admission as separate proofs on WebSocket control-plane routes.
- Put the origin decision before `accept`, `upgrade`, `open`, subscription, terminal dispatch, or any other sink-side state transition.
- A security regression should prove the cross-origin carrier is denied and that the socket, session, terminal, process, file, network, or stored-state sink was not partially reached.
- Preserve intended same-origin, direct/local, origin-less non-browser, and service-authenticated paths with explicit positive tests rather than broad bypasses.

## Repeat next time

- Map browser WebSocket paths as `page origin -> handshake -> credential source -> route admission -> hub/dispatcher -> sink`.
- For cookie-authenticated sockets, require an `Origin` check before `accept`, `upgrade`, `open`, `subscribe`, or terminal/session dispatch.
- Compare against the browser-visible origin, not only an internal service URL; trusted proxy and direct/local deployments need deliberate compatibility handling.
- Keep service-authenticated and non-browser lanes explicit so compatibility does not become an accidental bypass.
- Test both the denial and the sink-side absence: cross-origin browser input should not reach socket acceptance, subscription, terminal output, terminal input, or session mutation.

## Vault redirect

The durable private owner is the OSS Vulnerability Research Vault's source-code discovery workflow and the public-observation routing takeaway.

This post keeps the public synthesis narrow: the public PR, the browser terminal WebSocket boundary, and the reusable proof shape. The underlying vault rule remains: name the carrier, actor proof, admission gate, sink, denial, and compatibility lanes before treating a control-plane WebSocket fix as complete.
