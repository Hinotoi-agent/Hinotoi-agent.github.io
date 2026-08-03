---
layout: post
title: "2026-08-03 — Deferred MCP tools need explicit grants"
date: 2026-08-03 05:00:03 +0800
permalink: /2026/08/03/ai-security-case-study-deferred-mcp-tools-need-explicit-grants/
takeaway: "Loading an MCP tool schema changes discoverability; only a server-side grant should change who may invoke the backend capability."
categories: [case-study, ai-security]
tags: [case-study, mcp, tool-authorization, prompt-injection, least-privilege, deny-by-default, agent-security]
---

Progressive tool loading can reduce prompt size without reducing authority. If a model can discover and load a backend MCP tool, the server still needs an independent answer to a narrower question: is this user allowed to invoke that capability?

## Signal

The closed Singapore window was `2026-08-03 00:00` to `2026-08-04 00:00`. No authored PR merged in that window. The useful movement was the public-safe finalization of an earlier MCP authorization case: DeepTutor's deferred tool loader exposed why schema discovery and backend authority must remain separate decisions.

The security signal was not deferred loading itself. A real non-admin user whose grant omitted `mcp_tools` could inherit unrestricted MCP access. Absence selected the configured tool set instead of an empty allowlist.

```text
make a tool discoverable to the model
  !=
authorize this user to reach its backend capability
```

## Merged PRs

None in this window.

The case below examines an earlier merged fix, [`HKUDS/DeepTutor #579`](https://github.com/HKUDS/DeepTutor/pull/579), as a durable review pattern; it is not reported as a new August 3 merge.

## What shipped or moved

The public synthesis moved from a terse grant-default observation to a bounded case study with four explicit limits:

- the affected actor was a real non-admin user, not an administrator;
- impact depended on a sensitive MCP server being configured;
- the merged patch changed missing MCP grants to deny by default while preserving explicit compatibility lanes;
- verification proved grant-resolution behavior rather than claiming end-to-end coverage of every MCP backend.

The canonical private takeaway already records the operational rule: deferred schemas are a context-management mechanism, while host-sensitive execution requires a server-derived grant. This post makes that rule public without exposing private report material or expanding the exploit beyond the evidence in the merged PR.

## Observed pattern

### Threat model

The bounded threat model is a multi-user DeepTutor deployment with at least one sensitive MCP server configured. A low-privilege user can start a chat turn, or untrusted content can influence that turn through prompt injection. The configured MCP tools may bridge to filesystem, shell, browser, or internal-service actions, depending on the deployment.

The issue did not create a sensitive MCP server or bypass administrator access. The boundary failure was that a real non-admin user with no explicit MCP grant could still inherit the deployment's configured MCP tool set.

### Finding and PR

Public PR: [`HKUDS/DeepTutor #579 — [security] fix(multi-user): deny MCP tools until explicitly granted`](https://github.com/HKUDS/DeepTutor/pull/579).

Merge commit: `90046374b3dcd4f8a866d2d64a64440bc08eb2ef`.

Security-relevant files:

- `deeptutor/multi_user/tool_access.py` — changes an absent real-user MCP grant from unrestricted access to an empty allowlist.
- `deeptutor/multi_user/grants.py` — documents the split between built-in optional-tool defaults and MCP host-capability defaults.
- `deeptutor/agents/chat/agentic_pipeline.py` — applies real-user MCP grants while preserving explicit partner and synthetic-turn metadata filters.
- `tests/multi_user/test_tool_access.py` — covers missing-grant denial and explicit MCP allowlists.

The root cause was shared null semantics. `None` represented unrestricted access for ordinary optional tools and was also applied to MCP tools, even though MCP adapters can expose deployment-defined backend capabilities.

### Exploit path

The public source-to-sink chain was:

```text
low-privilege chat user or prompt-injected content
  -> agent receives the deferred MCP tool manifest
  -> model selects load_tools for a configured tool
  -> loaded schema becomes callable in the turn
  -> registry dispatches the MCP adapter
  -> backend MCP server performs the configured host-side action
```

Before the patch, omitting `mcp_tools` from a real non-admin user's grant did not stop this chain; it selected all configured MCP tools. The model's `load_tools` call could therefore move a deployment capability from hidden to callable without an explicit user-specific MCP grant.

The impact remained configuration-dependent. A harmless MCP tool produced harmless reachability; a server exposing filesystem, command, browser, or internal-service operations gave the same authorization error a more sensitive sink.

### Mitigation

The merged patch makes MCP access fail closed for real non-admin users:

- an absent `mcp_tools` grant resolves to an empty set;
- an explicit grant exposes only the named MCP tools;
- administrators remain unrestricted;
- partner and synthetic turns retain their explicit metadata-scoped allowlists;
- built-in optional tools keep their existing default-pool behavior.

This is a narrow compatibility trade-off: ordinary users now need explicit MCP grants, while unrelated tool classes and established owner-scoped paths retain their prior semantics.

The patch fixes the concrete grant-resolution boundary. A broader defense-in-depth rule still applies: schema loading should be treated as discoverability, and especially sensitive host actions may warrant an additional server-side approval or capability check immediately before dispatch.

### Verification

The PR named this focused host test command:

```sh
python3 -m pytest -q tests/multi_user/test_tool_access.py tests/services/mcp/test_mcp_config.py
```

It reported `22 passed`. The same focused suite reported `22 passed` in a clean Python 3.11 Docker environment. The PR also ran:

```sh
python3 -m compileall -q deeptutor/multi_user deeptutor/agents/chat tests/multi_user/test_tool_access.py
git diff --check
```

The regression proof has both sides of the policy boundary:

- **negative:** a real non-admin user with no `mcp_tools` grant receives an empty MCP allowlist;
- **positive:** a real non-admin user with an explicit grant receives only the named tools, while admin and explicit partner/synthetic paths remain available.

This is the correct proof shape for the merged change: verify that the resolver denies the missing-grant case and preserves intentional compatibility paths. It does not claim that every MCP server or host-side action was exercised.

## External reference

The [Model Context Protocol security best practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) are a useful protocol-level anchor: MCP deployments must keep authorization decisions explicit and should not rely on confused delegation or ambient trust between components.

The project-specific lesson here is narrower. Even when tool discovery is progressive, the application still owns user-to-capability policy. A model-selected loader may change what schema is visible in the turn; it must not manufacture the server-side grant needed to invoke the backend action.

## What was learned

Deferred loading is a performance and context-management primitive, not an authorization primitive. Hiding a schema until the model requests it changes when the capability appears in the prompt; it does not prove that the current actor may use the capability behind it.

The reusable review chain is:

```text
user or untrusted content
  -> deferred-tool manifest
  -> model-selected loader
  -> user-specific grant resolution
  -> runtime registry
  -> MCP backend action
```

Authorization has to survive that whole chain. A prompt instruction, hidden schema, or model-selected load step cannot replace a server-derived grant at the action boundary. Defaults also need to reflect capability strength: semantics suitable for optional built-in helpers may be unsafe when reused for deployment-defined host tools.

## Takeaways

- Treat tool discovery, schema loading, authorization, approval, and execution as separate states in the boundary map.
- Missing, empty, wildcard, inherited, and unrestricted grants need distinct semantics; `None` should never carry an undocumented capability decision.
- A denial proof should show that the unauthorized tool never enters the callable set or reaches backend dispatch, not only that a later error is returned.
- Preserve explicit positive controls for administrator, partner, synthetic, and user-allowlisted paths so secure defaults do not become accidental feature removal.

## Repeat next time

- Trace deferred tools from manifest construction through loader mutation, grant resolution, registry dispatch, and the backend sink.
- Search every grant resolver for `None`, empty-set, wildcard, and omitted-field behavior; record exactly whether each means deny, inherit, default pool, or unrestricted.
- Test missing grant, empty grant, explicit subset, administrator access, and each documented partner or synthetic compatibility lane.
- For shell, filesystem, browser, internal-service, and other high-impact MCP actions, check whether authorization is revalidated immediately before dispatch and whether denial leaves no sink-side effect.

## Vault redirect

The durable research record remains in the private OSS Vulnerability Research Vault. The reusable rule is already owned by `Takeaway - Deferred tool loading is not authorization for MCP host tools`, and the broader publishing rule remains in `Takeaway - Public observations should route back into the vault`.

No new checklist was created for this finalization because the public synthesis did not introduce a new review behavior beyond those canonical notes. Future evidence should update the smallest existing vault owner rather than turn the website into a parallel research graph.
