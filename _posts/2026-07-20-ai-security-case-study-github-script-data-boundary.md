---
layout: post
title: "2026-07-20 — Keep upstream metadata out of GitHub Actions source"
date: 2026-07-20 05:00:26 +0800
permalink: /2026/07/20/ai-security-case-study-github-script-data-boundary/
takeaway: "Externally influenced workflow values must cross into interpreters as data, not be expanded into executable source."
categories: [case-study, ai-security]
tags: [case-study, github-actions, workflow-injection, github-script, supply-chain, ci-security]
---

A monitoring workflow is still a supply-chain boundary. If it fetches another repository and embeds that repository's metadata into interpreter source, passive observation can become authenticated code execution inside CI.

## Signal

[`steipete/CodexBar #2185`](https://github.com/steipete/CodexBar/pull/2185) fixed a scheduled upstream monitor that inserted external commit summaries directly into an `actions/github-script` JavaScript template literal.

The high-signal chain was:

```text
external repository commit subject
  -> git log output
  -> GitHub Actions step output
  -> expression expansion inside JavaScript source
  -> authenticated github-script client
```

The commit subject looked like display text, but the workflow changed its type at the interpreter boundary: it became part of the program before JavaScript parsing.

## Threat model

The workflow periodically fetched the independently controlled Quotio repository and summarized recent commits in a CodexBar issue.

A malicious external contributor could propose a title that later became a squash-merge commit subject. A malicious or compromised upstream collaborator could set such a subject directly. Exploitation therefore required the crafted subject to reach the monitored default branch and then be observed by the scheduled or manually dispatched workflow.

The workflow token was deliberately restricted to:

```yaml
permissions:
  contents: read
  issues: write
```

That bounded the demonstrated impact. Injected JavaScript could act through the authenticated GitHub client within issue-write scope, but the token did not grant source or release write access.

## Finding and PR

Public PR: [`steipete/CodexBar #2185 — [security] Fix upstream monitor script injection`](https://github.com/steipete/CodexBar/pull/2185).

Merge commit: `20906cf867120d6aeb06ff92945e5c112a1fb989`.

Changed file:

- `.github/workflows/upstream-monitor.yml` — moved all six `steps.check.outputs` values into the step's environment and read them through `process.env`.

The vulnerable shape was equivalent to:

```yaml
const quotioSummary = `${{ steps.check.outputs.quotio_summary }}`;
```

GitHub resolves the expression before `actions/github-script` parses the generated JavaScript. A backtick in an upstream commit subject could therefore close the intended template literal and alter the program.

## Exploit path

The source-to-sink chain was:

```text
crafted upstream commit subject
  -> monitored default-branch history
  -> git log --oneline
  -> quotio_summary step output
  -> GitHub expression expansion
  -> github-script JavaScript parser
  -> authenticated github REST client with issues: write
```

A backtick-bearing subject could terminate the string literal, introduce a JavaScript statement, and comment out the remaining generated source. The injected statement then ran in the same script context as the authenticated `github` object.

The important boundary was not `$GITHUB_OUTPUT` alone. Step outputs are valid data carriers. The failure occurred when an externally influenced output was interpolated into interpreter source instead of being supplied through a data channel.

The practical impact was correspondingly scoped: issue creation or modification, comments, labels, state changes, disruption of the automated upstream-review queue, or reuse of the short-lived token within its restricted permissions. No claim of source-code or release modification was needed.

## Mitigation

The fix passed workflow expressions through the action environment:

```yaml
env:
  QUOTIO_SUMMARY: ${{ steps.check.outputs.quotio_summary }}
with:
  script: |
    const quotioSummary = process.env.QUOTIO_SUMMARY ?? '';
```

This preserves the value as data. Backticks, quotes, interpolation markers, and multiline text are no longer parsed as part of the JavaScript program.

The patch applied that rule consistently to all six outputs consumed by the script rather than fixing only the known commit-summary field. It also preserved the existing issue body and update behavior, pinned actions, and least-privilege token permissions.

This is the right abstraction level: do not escape one payload character at a time when the safer primitive is to stop constructing source from the value.

## Verification

The PR recorded three useful proof layers.

First, the workflow passed pinned Docker `actionlint` validation:

```text
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint@sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667 -color -shellcheck= .github/workflows/upstream-monitor.yml
```

Second, a Docker Node 24 regression supplied a crafted backtick-bearing summary and proved both conditions that matter:

```text
negative proof: the harmless injected assignment did not execute
positive control: the complete crafted value remained present in the generated issue body
```

Third, a structural check confirmed that the `github-script` block contained no direct `steps.check.outputs` interpolation and that all six values were read through `process.env`.

`git diff --check` also passed. Repository-wide local Swift checks were blocked by the available Command Line Tools environment, but the remote PR checks passed at the merged head, including lint, build/test shards, Linux CLI tests, macOS Swift tests, and GitGuardian.

The strongest verification is sink-shaped: the hostile string remains intact as issue content, does not become executable JavaScript, and the intended issue-management path still works.

## What was learned

Interpreter boundaries deserve the same treatment as file, network, tool, and agent-action boundaries. A value can remain harmless through fetch, shell capture, and step-output transport, then become dangerous at the final transform into source code.

For AI and automation repositories, this pattern extends beyond commit subjects. Model output, issue text, PR titles, tool results, generated summaries, artifact metadata, and matrix values can all become untrusted workflow inputs. If any of them are expanded into shell, JavaScript, Python, SQL, or template source, the automation has converted content into authority.

The reusable rule is:

```text
source -> carrier -> transform -> interpreter decision -> authenticated sink
```

Trace the value all the way to parsing. Least privilege then limits impact, but it does not replace the data/code separation.

## Repeat next time

- Search workflows for `${{ ... }}` expressions embedded inside `script:`, shell bodies, `actions/github-script`, or other interpreter source.
- Classify commit subjects, PR and issue text, branch names, artifact metadata, matrix values, and tool/model output as untrusted when another principal can influence them.
- Pass values through `env`, files, standard input, or structured serialization, then read them as data inside the interpreter.
- Add hostile fixtures containing backticks, quotes, `${...}`, newlines, and comment delimiters.
- Prove both sides: the payload stays inert, and its full value still reaches the intended issue, report, or log output.
- Keep explicit token permissions narrow so a future parser mistake has a bounded sink.

## Vault redirect

The durable private owner is the OSS Vulnerability Research Vault's source-code discovery and action-sink review workflow.

The public rule is intentionally narrow: external metadata crossed into JavaScript source, the fix restored a data boundary, and verification proved inertness plus compatibility. Future workflow reviews should keep the complete chain visible—external source, transport, parser boundary, ambient credentials, and final mutation scope—without turning the public site into a record of private research artifacts.
