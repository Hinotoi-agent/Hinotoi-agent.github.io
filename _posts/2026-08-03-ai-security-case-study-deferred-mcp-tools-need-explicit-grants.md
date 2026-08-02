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

DeepTutor's multi-user chat pipeline supported deferred MCP tools: tool names could be exposed to the agent and loaded into the live tool set only when needed. The security signal was not the deferred-loading mechanism itself. It was the default used when a real non-admin user's grant omitted `mcp_tools`: absence resolved to unrestricted MCP access.

That collapsed two different decisions:

```text
make a tool discoverable to the model
  !=
authorize this user to reach its backend capability
```

## Threat model

The bounded threat model is a multi-user DeepTutor deployment with at least one sensitive MCP server configured. A low-privilege user can start a chat turn, or untrusted content can influence that turn through prompt injection. The configured MCP tools may bridge to filesystem, shell, browser, or internal-service actions, depending on the deployment.

The issue did not create a sensitive MCP server or bypass administrator access. Impact required such a server to be configured. The boundary failure was that a real non-admin user with no explicit MCP grant could still inherit the deployment's configured MCP tool set.

## Finding and PR

Public PR: [`HKUDS/DeepTutor #579 — [security] fix(multi-user): deny MCP tools until explicitly granted`](https://github.com/HKUDS/DeepTutor/pull/579).

Merge commit: `90046374b3dcd4f8a866d2d64a64440bc08eb2ef`.

Security-relevant files:

- `deeptutor/multi_user/tool_access.py` — changes an absent real-user MCP grant from unrestricted access to an empty allowlist.
- `deeptutor/multi_user/grants.py` — documents the split between built-in optional-tool defaults and MCP host-capability defaults.
- `deeptutor/agents/chat/agentic_pipeline.py` — applies real-user MCP grants while preserving explicit partner and synthetic-turn metadata filters.
- `tests/multi_user/test_tool_access.py` — covers missing-grant denial and explicit MCP allowlists.

The root cause was shared null semantics. `None` represented unrestricted access for ordinary optional tools and was also applied to MCP tools, even though MCP adapters can expose deployment-defined backend capabilities.

## Exploit path

The public source-to-sink chain was:

```text
low-privilege chat user or prompt-injected content
  -> agent receives the deferred MCP tool manifest
  -> model selects load_tools for a configured tool
  -> loaded schema becomes callable in the turn
  -> registry dispatches the MCP adapter
  -> backend MCP server performs the configured host-side action
```

Before the patch, omitting `mcp_tools` from a real non-admin user's grant did not stop this chain; it selected all configured MCP tools. The model's `load_tools` call was therefore able to move a deployment capability from hidden to callable without an explicit user-specific MCP grant.

The impact remained configuration-dependent. A harmless MCP tool produced harmless reachability; a server exposing filesystem, command, browser, or internal-service operations gave the same authorization error a more sensitive sink.

## Mitigation

The merged patch makes MCP access fail closed for real non-admin users:

- an absent `mcp_tools` grant resolves to an empty set;
- an explicit grant exposes only the named MCP tools;
- administrators remain unrestricted;
- partner and synthetic turns retain their explicit metadata-scoped allowlists;
- built-in optional tools keep their existing default-pool behavior.

This is a narrow compatibility trade-off: ordinary users now need explicit MCP grants, while unrelated tool classes and established owner-scoped paths retain their prior semantics.

The patch fixes the concrete grant-resolution boundary. A broader defense-in-depth rule still applies to agent systems: schema loading should be treated as discoverability, and especially sensitive host actions may warrant an additional server-side approval or capability check immediately before dispatch.

## Verification

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

This is the correct proof shape for the merged change: verify the resolver denies the missing-grant case and preserves intentional compatibility paths. It does not claim that every MCP server or every host-side action was exercised.

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

Authorization has to survive that whole chain. A prompt instruction, a hidden schema, or a model-selected load step cannot replace a server-derived grant at the action boundary. Defaults also need to reflect capability strength: semantics suitable for optional built-in helpers may be unsafe when reused for deployment-defined host tools.

## Repeat next time

- Separate tool discovery, schema loading, authorization, and execution in the boundary map.
- Search for `None`, empty-set, wildcard, and omitted-field semantics at every grant resolver; write down whether each means deny, inherit, default pool, or unrestricted.
- Treat MCP, shell, filesystem, browser, and internal-service tools as backend capabilities rather than prompt features.
- Test missing grant, empty grant, explicit subset, admin access, and any partner or synthetic compatibility path.
- Verify denial at the sink-facing resolver: the unauthorized tool should not enter the callable set or reach backend dispatch.
- If a tool can cause high-impact host actions, consider a second per-call approval or capability check even after visibility is correctly scoped.

## Vault redirect

The durable research record remains in the private OSS Vulnerability Research Vault, where this case is linked to the existing takeaway that deferred tool loading is not authorization for MCP host tools and to the broader action-sink review rule.

The public lesson is intentionally narrower than the private research graph: an absent non-admin MCP grant meant unrestricted access, the merged fix changed that default to deny, and the focused tests proved both denial and explicit-grant compatibility. Future reviews should route reusable observations back into those canonical vault notes rather than creating a parallel public-only knowledge silo.
