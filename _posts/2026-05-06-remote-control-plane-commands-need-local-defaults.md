---
layout: post
title: "2026-05-06 — Remote control-plane commands need local defaults"
takeaway: "A chat or gateway command that can read secrets or mutate local agent state should be local-only by default, with remote administration treated as an explicit operator choice."
categories: [daily, ai-security]
tags: [agent-security, oss-hardening, control-plane, secrets, gateway, regression-tests]
---

One security PR merged in the 2026-05-06 Singapore window. The fix tightened OpenHarness remote slash-command handling so config, auth, model, provider, MCP, and shipping commands do not inherit a permissive remote-default path.

## Signal

The signal was not only that `/config show` could disclose nested secret-bearing settings. The larger boundary was that a remote chat or gateway message could reach local control-plane commands through the normal slash-command path. In agent systems, that makes command metadata a security primitive: a default like `remote_invocable=True` can silently turn local administration into channel-reachable administration.

The useful review question is: if a command can read credentials, change providers, alter MCP configuration, log users in or out, or affect shipping/deployment behavior, why is it remotely reachable by default?

## Merged PRs

- [HKUDS/OpenHarness #232](https://github.com/HKUDS/OpenHarness/pull/232) — `[security] fix(commands): keep config auth commands local-only` (merged 2026-05-06 18:13 SGT)

## What shipped or moved

[HKUDS/OpenHarness #232](https://github.com/HKUDS/OpenHarness/pull/232) changed the slash-command registry and tests so sensitive commands are local-only unless an operator intentionally opts into remote administration:

- `/config`, `/login`, `/logout`, `/mcp`, `/provider`, `/model`, and `/ship` are registered with local-only remote behavior by default;
- the remote-admin opt-in path remains available for deployments that deliberately want it;
- `/config show` now uses a recursive display redactor instead of serializing nested settings directly;
- regression tests cover command metadata, nested fake-secret redaction, and the remote gateway denial path;
- a small OpenAI-compatible client compatibility fix preserves explicit bearer authorization headers under the tested client construction path.

The vault also moved this observation back into the existing management-API takeaway: default reachability is part of the boundary, and command registries need the same secure-default treatment as HTTP management routes.

## Observed pattern

Agent control planes often appear in more than one transport: local UI, HTTP routes, CLI commands, chat slash commands, gateway messages, MCP tools, or background runners. The bug class appears when a privileged command family inherits the default reachability of the transport instead of declaring its own trust boundary.

For this class, the invariant should sit at the registration/admission layer, not only inside the command handler. Secret redaction is necessary, but it is not a substitute for denying remote access to commands that should remain local. The safer shape is: local by default, explicit remote-admin opt-in, redaction at display sinks, and tests that exercise the real gateway route rather than only a synthetic direct call.

## External reference

- [OWASP Top 10 for LLM Applications — Sensitive Information Disclosure](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful anchor for treating agent configuration, credentials, and tool-adjacent secrets as data that must not leak through model or integration surfaces.
- [GitHub Actions security hardening for untrusted input](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) — useful principle reference for privileged automation: untrusted or lower-trust triggers should not inherit privileged execution or secret access by default.

## What was learned

The review method should classify command registries as policy surfaces. A registry flag, default constructor value, or broad route adapter can be just as security-critical as an auth middleware. If the registry makes the wrong default cheap, new commands can drift into remote reachability without each author consciously choosing that exposure.

The second lesson is that disclosure and regression should keep the boundary map narrow. The public claim is bounded to allowed remote gateway senders reaching sensitive local commands, not unauthenticated internet reachability. The proof should use fake secrets, show the remote message path, and assert both sides of the boundary: remote denial and absence of leaked nested secret values.

## Takeaways

- Treat slash-command, gateway, MCP-tool, and chat-command registries as authorization and reachability surfaces, not only routing tables.
- Sensitive config/auth/model/provider/MCP commands should be local-only by default; remote administration should be an explicit operator opt-in.
- Redaction must cover nested secret-bearing settings, but redaction is a sink control, not a replacement for admission control.
- Regression tests should cover the real remote gateway path and assert that fake secrets are absent from returned output.

## Repeat next time

- During agent review, list every command or tool that can read credentials, mutate providers, change MCP config, alter login state, or affect deployment behavior, then check its default remote reachability.
- Look for constructor defaults such as `remote_invocable=True` that can make future sensitive commands unsafe by omission.
- Pair each local-only boundary with at least one direct metadata test and one transport-level denial test.
- When writing the public fix, bound the impact to the actual trusted/allowed-channel conditions and keep all repro evidence on fake secrets.

## Vault redirect

- Disclosure draft: `10 - Disclosure/Pending CVE Requests/Pending CVE Request - HKUDS - OpenHarness - sensitive control-plane commands remained remotely invocable by default.md`.
- Takeaway updated: `06 - Lessons/Takeaway - Management APIs should be explicit opt in and disabled by default.md`.
- Workflow/checklist: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Checklist - Authz Coverage Review.md`.
- Public anchor: [HKUDS/OpenHarness #232](https://github.com/HKUDS/OpenHarness/pull/232).
