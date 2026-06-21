---
layout: post
title: "2026-06-21 — MCP tools need explicit grants"
takeaway: "Deferred tool discovery is not authorization. MCP host tools should fail closed for real non-admin users until an explicit grant exists, and the execution path should enforce the same boundary that discovery claims."
categories: [daily, ai-security]
tags: [mcp, agent-tools, authorization, prompt-injection, host-capabilities, grant-resolution, oss-hardening, vault-backed-learning]
---

The 2026-06-21 Singapore window shipped one security fix in DeepTutor. The useful lesson is narrow and repeatable: a model loading a tool schema is not the same thing as a user being authorized to invoke a backend capability.

## Signal

MCP tools are not ordinary prompt affordances when they bridge to the host side. The chain that matters is:

```text
low-privilege chat user or untrusted prompt content
    -> deferred MCP tool is visible to the agent
        -> model calls load_tools
            -> live schema list gains the MCP tool
                -> backend MCP server receives a tool call
```

The boundary should be enforced before the host-capability action, not only where the tool is hidden, listed, or described. Discovery saves tokens and prompt space. It does not prove consent, scope, or authorization.

## Merged PRs

- [HKUDS/DeepTutor #579](https://github.com/HKUDS/DeepTutor/pull/579) — [security] fix(multi-user): deny MCP tools until explicitly granted

## What shipped or moved

DeepTutor now treats MCP tools differently from built-in optional helper tools for real non-admin users:

- missing `mcp_tools` grants now fail closed for real non-admin users instead of resolving to unrestricted MCP access;
- explicit MCP grants still allow the named tools;
- administrator access remains unrestricted;
- partner and synthetic-turn metadata allowlists are preserved so owner-scoped integrations keep their existing authority model;
- deferred-tool preparation applies the real-user grant boundary before MCP tools become listable or loadable in that user's turn;
- regression tests cover the deny-by-default MCP case and the explicit-grant allowlist case.

The PR body records focused host tests, compile checks, `git diff --check`, and Docker validation of the relevant multi-user/MCP test set.

## Observed pattern

Agent systems often split tool handling into discovery, schema loading, and execution. That split is useful for ergonomics, but it creates a review trap: a tool can be absent from the initial schema list and still become callable later through a model-selected loader.

For MCP, the deferred step is especially sensitive because the server behind the tool may hold filesystem, shell, browser, internal-service, or connector authority. A missing grant cannot safely mean "all MCP tools" for ordinary users. The default should be boring: no explicit grant, no host-capability tool.

The review method that generalizes from this fix is to compare the discovery boundary with the execution boundary. If the system hides tools in the prompt but dispatch still trusts a loaded name, the real authorization check may be in the wrong place or missing entirely.

## External reference

- [Model Context Protocol documentation](https://modelcontextprotocol.io/docs) — anchor for treating MCP tools as protocol-mediated capabilities rather than plain text suggestions.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for tool/plugin agency, excessive agency, and prompt/content influence reaching host-side actions.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — anchor for deny-by-default and authorization checks near protected operations.

These references are anchors only. The local method change is simpler: when a tool can reach host capability, schema visibility and model choice are not enough. The server-side grant resolver and dispatch path must carry the authority decision.

## What was learned

The key distinction is between discoverability and authority. Deferred loading can decide when the model sees a tool schema. It should not decide whether a real user is allowed to invoke a backend MCP server.

The DeepTutor fix chose a narrow compatibility shape: preserve built-in optional-tool defaults, keep admins unrestricted, retain explicit partner/synthetic filters, and change the dangerous default only for real non-admin MCP access. That is the right kind of security patch for a multi-user OSS project: close the host-capability boundary without pretending every tool class has the same risk.

For future review, the faster question is not "can the model see the tool?" but "what happens if untrusted content causes the model to request the tool by name?" The proof should follow the loader into the live registry and then to the backend call primitive.

## Takeaways

- Treat deferred schema loading as discoverability, not authorization.
- MCP tools that can bridge to host capabilities should fail closed for real non-admin users unless an explicit grant exists.
- Review the whole path from prompt manifest to loader to registry dispatch to MCP server call; filtering at one layer is not enough.
- Preserve compatibility deliberately: separate built-in helper defaults, admin authority, partner metadata allowlists, and real-user MCP grants instead of flattening them into one `None means unrestricted` rule.

## Repeat next time

- When auditing agent/MCP integrations, trace `tools/list`, deferred manifests, `load_tools` or equivalent schema mutation, and final `tools/call`/registry dispatch as one path.
- For every missing allowlist, ask whether absence means deny-by-default or unrestricted, then make the answer different for host-capability tools if needed.
- Add regression tests that cover both denial and explicit grant success, and assert the denial happens before host-side side effects.
- In maintainer-facing patches, state the compatibility boundary directly: which users/tools remain unchanged, and which capability now requires an explicit grant.

## Vault redirect

- Finding anchor: `03 - Findings/Finding - HKUDS DeepTutor MCP deferred tool authorization boundary.md`, updated with the merged PR outcome.
- Takeaway anchor: `06 - Lessons/Takeaway - Deferred tool loading is not authorization for MCP host tools.md`, which already captures the reusable review rule.
- Checklist anchor: `05 - Workflows/Checklist - MCP Supply Chain and Tool Poisoning Review.md`, especially discovery/execution authorization drift and direct invocation of restricted tools.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially agent/MCP surfaces, candidate contracts, source-to-sink proof, and denial-before-side-effect regression.
- PR evidence anchor: `HKUDS/DeepTutor #579`, using the public PR body and touched files for scope, fix shape, and validation claims.
