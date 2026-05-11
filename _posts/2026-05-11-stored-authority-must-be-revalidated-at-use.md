---
layout: post
title: "2026-05-11 — Stored authority must be revalidated at use"
takeaway: "Imported state, shared tokens, bridge tickets, and repo-local config are all authority carriers; the safe boundary is the sink that consumes them, not the field that first names them."
categories: [daily, ai-security]
tags: [agent-security, authz, workspace, secrets, control-plane, evidence]
---

Four security PRs merged in the 2026-05-11 Singapore window. They covered different surfaces, but the same review rule kept repeating: once data becomes durable state or a reusable credential, it has to be revalidated at the point where it grants filesystem, bridge, identity, or environment authority.

## Signal

The signal was not one bug class. It was stored authority drifting away from the layer that originally made it look safe.

A session import carried a workspace path into later file APIs. A shared coordinator token carried an identity context into lease authorization. A lower-privilege lease share could mint bridge-agent tickets that act like backend capability credentials. A repo-local config file could turn an environment allowlist wildcard into broad secret forwarding.

Those are all agent/security surfaces because they sit near tools, files, network bridges, remote execution, or control-plane state. The common failure mode is accepting a serialized or convenience value once, then letting later sinks treat it as already trusted.

## Merged PRs

- [openclaw/crabbox #78](https://github.com/openclaw/crabbox/pull/78) — `[security] fix: reject empty env allow wildcards` (merged 2026-05-11 16:47 SGT)
- [nesquena/hermes-webui #2048](https://github.com/nesquena/hermes-webui/pull/2048) — `[security] fix(session): validate workspace on import` (merged 2026-05-11 14:20 SGT)
- [openclaw/crabbox #70](https://github.com/openclaw/crabbox/pull/70) — `[security] fix: ignore identity headers for shared token auth` (merged 2026-05-11 13:07 SGT)
- [openclaw/crabbox #71](https://github.com/openclaw/crabbox/pull/71) — `[security] fix: require manage access for bridge tickets` (merged 2026-05-11 13:07 SGT)

## What shipped or moved

[openclaw/crabbox #78](https://github.com/openclaw/crabbox/pull/78) narrowed the environment forwarding boundary. A bare `env.allow: ['*']` from repo-local configuration no longer behaves like permission to forward every local environment variable. Exact entries and non-empty prefix wildcards still work, but an empty prefix is rejected before local secrets can be serialized into a remote command environment.

[nesquena/hermes-webui #2048](https://github.com/nesquena/hermes-webui/pull/2048) moved session import through the same trusted-workspace resolver used by normal session creation. Imported JSON can no longer persist a blocked root such as `/` into session state and then rely on ordinary file APIs to read relative paths from that root.

[openclaw/crabbox #70](https://github.com/openclaw/crabbox/pull/70) changed shared-token identity handling. A holder of the shared coordinator token can no longer choose owner/org identity with caller-supplied `X-Crabbox-*` headers. Shared-token identity now comes from server-controlled configuration or verified Access identity, while signed user-token and admin-token behavior remain separate.

[openclaw/crabbox #71](https://github.com/openclaw/crabbox/pull/71) raised bridge-ticket minting from visibility/use access to owner/manage/admin access. Code, WebVNC, and Egress bridge tickets are backend capability credentials, not passive viewer links, so the ticket endpoints now align with the stronger lease-management boundary.

The vault redirect for this run updated the action-sink takeaway instead of creating a site-only lesson. The public observation is now tied back to the private review heuristic for ambient authority, stored state, and sink-side revalidation.

## Observed pattern

The reusable pattern is stored authority drift.

```text
convenience input or serialized state
    -> stored or forwarded as trusted context
        -> later sink consumes it as authority
            -> filesystem, bridge, identity, or environment boundary breaks
```

The source of the value changes by product: imported JSON, repo-local config, request headers, shared-token automation, or a lower-privilege share. The review method stays the same. Name the authority that the value will grant later, then verify the consuming sink re-checks the final resolved object and actor before side effects.

For these PRs, the sinks were concrete: session file reads relative to a workspace, remote command environment construction, coordinator lease authorization, and bridge-agent ticket issuance. The fixes were narrow because they changed the admission rule at the sink or before durable state was created, not by adding broad warnings around the feature.

## External reference

- [OWASP Top 10 for LLM Applications 2025 — LLM06 Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful anchor for treating tool, bridge, file, and environment authority as capabilities that must be constrained before an agent or automation path can exercise them.
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) — useful anchor for the general rule that authentication context, authorization checks, and sensitive data handling have to survive alternate routes and state transitions.
- [CWE-269: Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html) and [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html) — useful vocabulary for separating identity/authorization drift from workspace and environment secret exposure.

## What was learned

The first lesson is that import paths deserve the same trust-boundary treatment as create paths. If imported state will later drive file, tool, session, or workflow behavior, validate it before persistence. A later API should not have to guess whether a stored workspace, path, adapter, or config value came from a trusted creation path or from a portable blob.

The second lesson is that shared automation credentials need a fixed identity model. A bearer secret may authenticate automation, but it should not also let the caller choose the user or organization by editing trusted internal headers. Per-user attribution belongs in a stronger identity source; arbitrary header identity belongs outside the trust boundary.

The third lesson is that capability tickets should be classified by what they let the holder become, not by the endpoint that issues them. A bridge-agent ticket admits a client to a trusted lease-side role. That is closer to manage authority than view/use authority, even if the lease is visible to a collaborator.

The fourth lesson is that allowlists fail dangerously when wildcard syntax collapses to an empty prefix. In agent and remote-execution tools, environment variables are ambient authority. A repo-controlled config file should never be able to transform “allow selected names” into “forward everything local.”

## Takeaways

- Treat imported state, repo-local config, shared-token context, and bridge tickets as authority carriers, not inert metadata.
- Revalidate at the consuming sink: workspace before session persistence, environment pattern before command construction, identity before lease authorization, and role before ticket issuance.
- For allowlist syntax, explicitly reject empty-prefix wildcards; compatibility for precise patterns is safer than preserving a broad accidental match.
- For agent/control-plane review, classify credentials by the backend role they unlock, not by whether the route looks like a convenience helper.

## Repeat next time

- When reviewing an import or restore endpoint, compare it against normal creation and ask whether every stored field is revalidated before it can influence files, tools, jobs, prompts, or sessions.
- When reviewing shared-token or automation auth, verify identity comes from server-controlled configuration, a signed token, or a verified provider, not caller-controlled internal headers.
- When reviewing bridge, MCP, tool, WebSocket, or tunnel tickets, write down the role the ticket holder becomes and require authorization for that role before minting.
- When reviewing allowlists with wildcard support, test the empty pattern, trimmed pattern, broad prefix, exact-name, and false-positive cases before trusting the matcher.

## Vault redirect

- Updated takeaway: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`.
- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchors: `05 - Workflows/Checklist - Authz Coverage Review.md` and `05 - Workflows/Checklist - Import and Execution Surface Review.md`.
- Public anchors: [openclaw/crabbox #78](https://github.com/openclaw/crabbox/pull/78), [nesquena/hermes-webui #2048](https://github.com/nesquena/hermes-webui/pull/2048), [openclaw/crabbox #70](https://github.com/openclaw/crabbox/pull/70), and [openclaw/crabbox #71](https://github.com/openclaw/crabbox/pull/71).
