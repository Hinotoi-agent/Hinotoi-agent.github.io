---
layout: post
title: "2026-06-12 — Authorization guards need trusted scope inputs"
takeaway: "A guard is only as strong as the scope value it evaluates; profile, workspace, tenant, and organization selectors become authorization inputs once they steer access decisions, so they must be bound to authenticated server-issued state."
categories: [daily, ai-security]
tags: [authz, session-security, profile-isolation, cookie-trust, scope-binding, oss-hardening]
---

The 2026-06-12 Singapore window shipped one focused WebUI hardening PR. It did not add a new route guard. It fixed the input that an existing guard trusted.

That distinction matters. In agent and local-control-plane systems, a request often carries a convenient selector: active profile, workspace, tenant, project, org, model provider, tool server, or memory namespace. The selector starts as UX state. The moment a guard uses it to decide which sessions, files, tools, secrets, or approvals are visible, it becomes authorization state.

## Signal

One security fix landed in the closed Singapore window `[2026-06-12 00:00, 2026-06-13 00:00)`:

```text
authenticated WebUI session
    -> client-supplied active profile cookie
        -> request-local profile state
            -> profile-scoped session/file guard
                -> cross-profile access decision
```

The signal was a scope-input failure. The endpoint guard can be present and still evaluate the wrong boundary if the active profile comes from an unsigned browser cookie.

## Merged PRs

- [nesquena/hermes-webui #4023](https://github.com/nesquena/hermes-webui/pull/4023) — `[security] fix(auth): bind active profile cookie to session` (merged 2026-06-12 15:46:03 SGT)

## What shipped or moved

Hermes WebUI now binds the `hermes_profile` cookie to the current `hermes_session` when WebUI auth is enabled. Unsigned profile cookies are ignored under auth. Profile cookies signed for a different session are ignored under auth. `/api/profile/switch` now emits the session-bound format for auth-enabled profile switches.

The no-auth local preference path remains compatible: a plain profile-name cookie can still act as per-browser UI state when WebUI auth is not enabled. The security boundary changes only when the profile selector can influence authenticated profile-scoped authorization.

Regression coverage moved with the boundary. The PR added tests for valid signed profile cookies, unsigned forgery rejection, wrong-session rejection, and signed cookie emission from the switch route. That keeps the proof close to the helper layer where request-local active-profile state is derived.

The merged-PR data archive was updated with the new entry for 2026-06-12.

## Observed pattern

Authorization bugs are not always missing-guard bugs. Sometimes the guard exists, but one of its inputs is attacker-selectable.

For profile-scoped access, the durable invariant is not “the server checks active profile.” The invariant is: the active profile used by the guard must be derived from trusted state for the authenticated session. If a browser preference cookie chooses that scope directly, the authorization decision inherits browser-controlled authority.

This pattern generalizes across agent and AI-control-plane surfaces. Active workspace, selected profile, org context, MCP server id, tool namespace, approval target, memory scope, and provider account selectors all need the same question: is this merely display state, or does a policy layer consume it before a file, session, secret, tool, network, or approval sink is reached?

## External reference

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — anchor for enforcing object-level and context-aware authorization rather than relying on client-selected state.
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — anchor for treating session-bound server-issued state as the trust source when browser state influences authenticated behavior.
- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html) — anchor for access decisions evaluated under an attacker-influenced scope.
- [CWE-565: Reliance on Cookies without Validation and Integrity Checking](https://cwe.mitre.org/data/definitions/565.html) — anchor for unsigned cookie values used beyond harmless preference storage.

These references sharpen the public method rather than adding private exploit detail: client-side selectors need integrity and session binding before they become authorization inputs.

## What was learned

The review question should move from “does this route call the guard?” to “what state does the guard believe?” That catches a different class of bypass: route coverage can look correct while request-local identity, tenant, profile, or workspace context remains attacker-chosen.

The useful proof shape is also smaller than a full product redesign. Bind the selector to authenticated server-issued state, preserve explicit compatibility for non-auth/local modes, and test both denial and the safe path. That gives maintainers a narrow patch: secure default for auth-enabled deployments, no surprise breakage for local trusted-user preference behavior, and regression tests at the state-derivation boundary.

Severity still depends on the product trust model. If profiles isolate users, tenants, workspaces, sessions, secrets, or API-backed state, the impact is cross-profile confidentiality and integrity loss. If profiles are only a single trusted local user's convenience, the same bug may be hardening. The report should state that boundary instead of overstating it.

## Takeaways

- Treat active profile, workspace, tenant, organization, memory namespace, and tool-server selectors as authorization inputs as soon as a guard consumes them.
- A present guard is not enough; verify the actor and scope values fed into the guard come from authenticated server-issued state or signed claims.
- Keep compatibility branches explicit: no-auth local preference behavior can remain plain only if it is not claimed as an authenticated isolation boundary.
- Regression tests should cover valid signed state, unsigned forgery rejection, wrong-session rejection, and the route that emits the trusted selector.

## Repeat next time

- For every object-level authorization guard, trace `request cookie/header/body -> session lookup -> request-local scope -> guard -> sink` before deciding coverage is complete.
- When a UI preference becomes policy input, add a negative test for a forged client value and a wrong-session value, not just a positive parsing test.
- Calibrate severity against the target's documented trust model: separate single-user hardening from real cross-profile, cross-tenant, or cross-workspace isolation failure.
- After fixing a scope-input source, enumerate sibling selectors that may feed the same guard family: profile switch, session-by-id routes, file routes, approval routes, memory namespaces, and tool/workspace selectors.

## Vault redirect

- Checklist update: `05 - Workflows/Checklist - Authz Coverage Review.md` now includes a scope-selector rule for active profile, workspace, organization, and client cookie state that becomes authorization-relevant.
- Trust-model anchor: `06 - Lessons/Takeaway - Trust model defines whether auth lifecycle gaps are advisory grade.md` for severity calibration when a finding sits inside a trusted local/operator boundary.
- Review-loop anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially the candidate contract fields for attacker-controlled source, trust boundary crossed, dangerous primitive/sink, impact, and likely false positive.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
