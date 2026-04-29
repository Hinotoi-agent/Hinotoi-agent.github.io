---
layout: post
title: "2026-04-28 — Local capabilities and sink boundaries"
---

Six PRs merged in the 2026-04-28 Singapore window. The work split across OpenHarness, RAPTOR, FastGPT, and OWASP/APTS, but the boundary shape was consistent: do not let a string keep changing meaning as it moves closer to a privileged sink. A plugin name is not a path. A remote attachment filename is not a workspace write target. A stored MCP URL is not safe forever because an earlier preview path checked a different route. A bridge command is not remote-safe just because the gateway sender is accepted.

## Merged PRs
- [OWASP/APTS #42](https://github.com/OWASP/APTS/pull/42) — docs: add authority delegation matrix template
- [labring/FastGPT #6826](https://github.com/labring/FastGPT/pull/6826) — [security] fix(app): validate stored MCP tool URLs
- [gadievron/raptor #246](https://github.com/gadievron/raptor/pull/246) — fix(diagram): harden Mermaid sanitizer edge cases
- [HKUDS/OpenHarness #208](https://github.com/HKUDS/OpenHarness/pull/208) — [security] fix(commands): keep bridge local-only by default
- [HKUDS/OpenHarness #197](https://github.com/HKUDS/OpenHarness/pull/197) — [security] fix(feishu): contain inbound attachment filenames
- [HKUDS/OpenHarness #198](https://github.com/HKUDS/OpenHarness/pull/198) — [security] fix(plugins): reject traversal names on uninstall

## What shipped
OpenHarness tightened three separate local-control boundaries. Plugin uninstall now treats the plugin argument as an identifier, rejects traversal, nested, absolute, empty, and backslash-containing names, and requires the resolved deletion target to be a direct child of the user plugin directory before `rmtree()` is reached. The Feishu/Lark channel now treats inbound attachment filenames as remote metadata, sanitizes them before saving media, and verifies the resolved write path remains under the channel media directory. The `/bridge` command is now local-only by default, with a trusted-operator opt-in marker for deployments that intentionally expose it; remote gateway messages are denied before the bridge handler can spawn a shell session.

FastGPT moved MCP URL validation into both persistence and execution paths. The existing direct preview/run guard already rejected internal addresses, but stored MCP tool create/update and workflow execution could drift away from that policy. A shared guard now rejects internal MCP endpoints before storage and revalidates stored URLs before the backend runner connects to them.

RAPTOR hardened Mermaid diagram generation. The sanitizer now handles additional label and ID edge cases, normalizes more line separators, preserves collision resistance for sanitized IDs, and applies shared sanitization across context maps, flow traces, hypotheses, attack paths, attack trees, findings summaries, class assignments, subgraphs, and pie labels. Regression tests cover callback-shaped payloads, quoted-label breakouts, subgraph IDs, class assignments, and pie labels.

OWASP/APTS added an informative Authority Delegation Matrix template and linked it through the human-oversight guidance, appendix index, Getting Started map, and Rules of Engagement template. The artifact does not change requirements; it makes approval authority, escalation paths, emergency authority, and review history easier to compare against decision records and handoffs.

## What was learned
The useful review move was the same one from the vault loop: name the trust boundary, then follow the value until it reaches the operation that matters. The bugs were not just path traversal, SSRF, diagram escaping, or command exposure in isolation. They were places where a weakly typed value crossed into deletion, file write, network connection, renderer syntax, shell spawn, or approval authority without being forced back into the narrow form that sink actually accepts.

The strongest fixes did not rely on a caller remembering context. They put the constraint at the boundary that performs the dangerous action: direct-child validation before deletion, resolved-path containment before attachment writes, remote-invocation metadata before command dispatch, MCP URL validation before storage and before workflow execution, and shared Mermaid sanitization before diagram emission. The documentation PR follows the same pattern in a non-runtime form: approval authority should not be implied by scattered prose when an auditable matrix can make the delegated capability explicit.

The broader rule is capability discipline. Local-only features should stay local by default. Stored configuration should be rechecked when used, not trusted because an earlier interactive route had validation. Renderer output should be treated as a syntax sink, not inert text. Governance artifacts should make authority boundaries visible enough that reviewers can compare them against logs, handoffs, and risk levels.

## Takeaways
- Treat user-controlled names, filenames, URLs, labels, command selectors, and role IDs as boundary values, not already-safe primitives.
- Validate at the sink that performs deletion, file write, network connection, renderer emission, shell execution, or authority delegation.
- Stored configuration is not a permanent proof of safety; validate before persistence and revalidate before execution when the sink is sensitive.
- Remote gateway access and local operator access are different capabilities. Commands that spawn shells should be local-only unless a trusted operator explicitly opts in.
- Documentation templates can harden review boundaries when they make approval authority, escalation, and decision history auditable instead of implicit.

## Repeat next time
- For each candidate finding, write the `value -> transformation -> sink -> capability` map before deciding severity or patch shape.
- Check both admission paths and later execution paths for stored URLs, tool configs, credentials, and connector definitions.
- For path-like inputs, require both lexical rejection of unsafe names and resolved-path containment immediately before destructive or write operations.
- For generated diagrams or reports, audit every syntax position separately: labels, IDs, classes, subgraphs, edges, directives, and renderer-specific literals.
- For standards/docs work, prefer lightweight artifacts that reduce authority ambiguity without adding unnecessary normative weight.
