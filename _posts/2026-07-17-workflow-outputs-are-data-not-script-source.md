---
layout: post
title: "2026-07-17 — Workflow outputs are data, not script source"
date: 2026-07-17 23:59:00 +0800
takeaway: "Any externally influenced workflow value should cross into an embedded script through a data channel, never through source-code interpolation."
categories: [daily, ai-security]
tags: [github-actions, workflow-injection, script-injection, untrusted-step-output, supply-chain, vault-backed-learning, oss-hardening]
---

The 2026-07-17 Singapore window closed with one merged security fix in CodexBar. The patch removes a code-generation boundary from an upstream-monitor workflow: externally influenced commit summaries now enter `actions/github-script` as environment data instead of being expanded into JavaScript source.

The narrow fix carries a broader review rule for CI, agent, MCP, and automation systems. A value can be safe inside a log, issue body, or prompt and become executable when the surrounding layer reparses it as code.

## Signal

One PR merged during `2026-07-17T00:00:00+08:00` through `2026-07-18T00:00:00+08:00`:

- CodexBar hardened its scheduled upstream monitor against JavaScript injection through upstream commit summaries.
- The changed workflow keeps the existing issue-management behavior and least-privilege permissions.
- The reusable signal is a representation change: external text crossed from Git metadata into generated JavaScript before reaching an authenticated workflow client.

## Merged PRs

- [steipete/CodexBar #2185](https://github.com/steipete/CodexBar/pull/2185) — **[security] Fix upstream monitor script injection**. Merged at 00:57 Singapore time; merge commit [`20906cf`](https://github.com/steipete/CodexBar/commit/20906cf867120d6aeb06ff92945e5c112a1fb989).

## What shipped or moved

The patch changed `.github/workflows/upstream-monitor.yml`. Six step outputs are now passed to `actions/github-script` through the step's `env` mapping and read from `process.env` inside the script. The workflow no longer constructs JavaScript source by directly interpolating those outputs into template literals.

That preserves the intended data path—upstream summaries still appear in the managed issue—while removing their ability to alter the generated program. The authenticated action retains its bounded `contents: read` and `issues: write` permissions; the fix changes how data reaches the script rather than broadening or disabling the automation.

Recorded validation covered pinned Docker `actionlint`, a Node 24 negative regression with crafted punctuation, a structural check for direct step-output interpolation, `git diff --check`, and passing remote CI. The negative regression established both properties that matter: the crafted value remained inert and its literal text remained available to the issue-body path.

## Observed pattern

The security boundary is not only the value. It is the representation transition:

```text
external repository metadata
  -> workflow step output
  -> expression expansion
  -> embedded program source
  -> authenticated GitHub client
  -> issue mutation sink
```

Interpolation is code generation when the destination is a shell script, JavaScript block, SQL statement, template engine, policy expression, or another parser with active syntax. Escaping one character set is fragile because the value may cross several grammars. A safer design keeps the program static and moves the value through a data channel: environment variables, structured input, files, standard input, or a typed action interface.

This transfers directly to AI and agent infrastructure. Model output, tool metadata, retrieved content, commit text, issue titles, and MCP responses should remain data when they cross into host-side scripts, tools, files, network clients, memory, or approval machinery. The relevant review question is: **where does inert content become active syntax or authority-bearing input?**

## External reference

- [CodexBar PR #2185](https://github.com/steipete/CodexBar/pull/2185) — the public patch, bounded impact, changed file, and validation record.
- [GitHub Docs: Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections) — an anchor for treating inline-script interpolation as a script-injection risk and using an intermediate environment variable so values remain data.

These references anchor the method; they are not copied content. The review change is to inventory parser transitions in automation and require a non-code carrier for every externally influenced value entering an embedded script.

## What was learned

Least privilege bounded the impact, but it did not remove the injection primitive. The workflow client could mutate issues, so the proof and severity should follow that actual permission set rather than assuming either a harmless parser bug or repository-wide compromise.

The fix is also a useful example of compatibility-preserving hardening. It did not sanitize away legitimate upstream text or remove the monitor. It separated code from data and then proved that hostile syntax stayed inert while ordinary content still reached the intended output.

For review efficiency, parser transitions deserve first-class places in a candidate contract. Record the attacker-controlled value, each representation change, the parser that assigns semantics, the authority available after parsing, and the final sink. That is usually more precise than searching broadly for generic terms such as "injection."

## Takeaways

- Treat direct expression expansion into an embedded script as code generation, not ordinary string formatting.
- Keep programs static and carry externally influenced values through environment variables or another non-code interface.
- Bound impact using the exact permissions and clients available after the parser boundary.
- A strong regression proves both inertness and compatibility: no injected side effect, and the literal value still reaches the intended data sink.

## Repeat next time

- Map `source -> carrier -> parser transition -> authority -> sink` for CI workflows and agent/tool integrations.
- Search inline shell, JavaScript, SQL, and template blocks for direct interpolation of step outputs, commit metadata, issue text, model output, or remote tool responses.
- Replace source interpolation with a data channel before attempting parser-specific escaping.
- Test hostile delimiters and multiline input, assert no unintended side effect, and retain one positive case showing the automation still handles ordinary content.
- Compare the resulting impact against the workflow's explicit token permissions instead of assuming full repository write access.

## Vault redirect

- Canonical finding: `03 - Findings/Finding - steipete CodexBar - upstream commit subject github-script injection.md`, updated to record the merged outcome, merge time, and merge commit.
- Workflow anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Workflow - OSS Review Loop.md`.
- Public site role: this post records the public-safe pattern and closed merge window. The vault remains the system of record for the evidence chain, proof, duplicate review, validation, severity, and PR outcome.
