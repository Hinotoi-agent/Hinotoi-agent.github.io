---
layout: post
title: "2026-07-01 — Admission gates before stateful handoff"
takeaway: "Browser and automation carriers are not identity proof; validate origin and owner before a terminal, action session, or token rotation can spend authority."
categories: [daily, ai-security]
tags: [daily, websocket, browser-origin, csrf, github-actions, owner-proof, session-tokens, agent-control-plane, oss-hardening]
---

The 2026-07-01 Singapore window had two merged Crabfleet hardening PRs. They touched different surfaces, but the same review rule: a stateful handoff is the wrong place to discover that the request never proved the right actor.

One fix closed a browser terminal WebSocket origin gap. The other closed an action-session resume path that could rotate an agent token without proving the stable owner of the work. Both are AI/automation control-plane problems: a carrier reached a powerful session boundary, and the server needed to bind the carrier to the intended principal before accepting the handoff.

## Signal

Two target-window merges landed in `openclaw/crabfleet`:

- a browser-cookie terminal WebSocket path now rejects cross-origin browser handshakes before the terminal hub accepts the socket;
- a GitHub Actions action-session registration path now requires owner proof for resumes as well as new work before rotating a session-scoped agent token.

The shared signal is admission ordering. Browser `Origin` and stable work ownership are not cleanup checks after the route has already entered the terminal/session machinery. They are preconditions for entering it.

## Merged PRs

- [openclaw/crabfleet #67](https://github.com/openclaw/crabfleet/pull/67) — `[security] fix(terminal): validate browser websocket origin` — merged `2026-07-01 14:24 +08:00`.
- [openclaw/crabfleet #68](https://github.com/openclaw/crabfleet/pull/68) — `[security] fix(openclaw): require owner proof to resume action work` — merged `2026-07-01 14:16 +08:00`.

## What shipped or moved

The terminal fix shipped a narrow browser WebSocket boundary:

- `src/worker/session-terminal-route.ts` adds terminal WebSocket origin validation using the browser-visible request origin;
- `src/worker/worker-application.ts` applies that validation before handing non-service browser requests to the terminal hub;
- `tests/session-terminal-route.test.ts` covers cross-origin rejection plus same-origin, direct tenant/local-origin, trusted-proxy public-origin, origin-less non-browser, and service-authenticated paths.

The action-session fix shipped a matching owner-proof boundary:

- `src/worker/github-actions-session-registration.ts` requires a resolved owner for every action-session registration, including existing `workKey` resumes;
- `tests/github-actions-session-registration.test.ts` verifies ownerless resume rejection without token-hash rotation, matching-owner resume success, wrong-owner rejection, and new-registration owner persistence;
- `README.md`, `docs/api.md`, and `docs/github-actions-sessions.md` now document that `owner` is required for new registrations and resumes.

Both PRs included focused local and Docker validation. The terminal proof showed cross-origin browser terminal rejection with same-origin/direct/service terminal success. The action-session proof showed ownerless resume returning `400` with the existing token hash preserved, while matching-owner resume still rotated after proof.

## Observed pattern

The reusable pattern is pre-handoff identity binding:

```text
request carrier
    -> browser origin / owner proof / service-auth classification
        -> admission decision
            -> terminal hub, action session, token rotation, or other stateful sink
```

For browser paths, the carrier can be an attacker page using a victim's ambient cookie. For automation paths, the carrier can be a service-token-authenticated component presenting a reusable work key. In both cases, the carrier's ability to reach the route is not enough.

The review question is: what identity or intent proof must be true before the route enters the stateful subsystem?

For WebSockets, that proof is same-origin browser admission or an explicit non-browser/service-authenticated lane. For resumable automation work, that proof is a stable owner subject bound to the existing work. The invariant should be enforced before the terminal socket is accepted, before the session resets, and before a new plaintext agent token is returned.

## External reference

- [OWASP Cross-Site WebSocket Hijacking](https://owasp.org/www-community/attacks/Cross-Site_WebSocket_Hijacking) — anchor for treating browser WebSocket handshakes as CSRF-like when cookies are ambient and the server does not validate `Origin`.
- [OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for unsafe browser-triggered state changes and pre-sink denial.
- [MDN: Origin header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Origin) — anchor for the browser-origin signal used to distinguish same-origin application traffic from attacker-controlled pages.
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) — anchor for treating workflow automation identity, token exposure, and least privilege as security boundaries.

The references are only anchors. The local review method change is narrower: when a route hands control to a terminal, runner, action session, memory store, tool executor, or token issuer, actor proof has to happen before the handoff.

## What was learned

The two fixes make the same boundary visible from different sides.

The terminal route is a browser-origin problem. WebSocket handshakes are stateful and can carry ambient cookies; ordinary same-origin response-reading rules do not protect the server if the socket is accepted. The proof has to show a cross-origin browser handshake is denied before the terminal hub accepts it, and that legitimate same-origin/direct/service lanes still work.

The action-session route is an ownership-continuity problem. A `workKey` is a lookup key, not proof that the caller owns the existing work. If a resume path can omit `owner`, skip the stable-owner mismatch check, and still rotate `agent_token_hash`, then the token rotation sink is reached before the ownership invariant is proven. The proof has to show no session reset and no token-hash rotation on ownerless resume.

For AI security reviews, this is a useful bridge between browser CSRF/CSWSH and agent automation trust. The bug class is not only "missing Origin check" or "missing owner field." It is admission logic that lets a weak carrier reach a powerful state transition before the server binds the request to the actor allowed to spend that authority.

## Takeaways

- Treat browser-origin checks and automation-owner checks as admission gates, not terminal/session cleanup.
- A reusable key such as `workKey` can identify state without proving the caller is allowed to resume or rotate it.
- For WebSocket control planes, prove both cross-origin `403` and absence of socket acceptance; a blocked response after acceptance is too late.
- For token-rotation paths, prove the denied path preserves the existing token hash or session state.
- Compatibility coverage matters: keep same-origin, direct local/tenant, non-browser, service-authenticated, and matching-owner lanes explicit so the security fix does not become an accidental product break.

## Repeat next time

- Map every stateful handoff route: WebSocket accept, terminal attach, action resume, job start, token rotation, memory write, tool call, and approval response.
- For browser-cookie paths, require same-origin validation before WebSocket acceptance or unsafe method side effects.
- For resumable automation paths, require stable owner/tenant/session proof before reset, rebind, or token rotation.
- Write denial tests that assert the sink was not reached: no accepted socket, no queued action, no rotated hash, no created file, no stored mutation.
- Add positive controls for the intended lane instead of weakening the guard later under compatibility pressure.

## Vault redirect

- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially the candidate contract requirement to name source, trust boundary, sink, invariant, and next-cheapest proof.
- Takeaway anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, updated with the 2026-07-01 pre-handoff identity-binding rule.
- Related proof-shape anchor: `06 - Lessons/Takeaway - Loopback browser unsafe methods need pre-sink origin gates.md` for browser-carried local/control-plane requests.
- Related trust-model anchor: `06 - Lessons/Takeaway - Explicit reuse tokens are not isolation boundaries.md` for distinguishing reusable lookup/dedup tokens from authorization boundaries.
- Public site role: this post is the public-safe synthesis. Private target notes, proof artifacts, and future checklist changes belong in the vault, not on the website.
