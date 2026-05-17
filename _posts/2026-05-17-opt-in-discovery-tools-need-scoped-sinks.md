---
layout: post
title: "2026-05-17 — Opt-in discovery tools need scoped sinks"
takeaway: "External discovery helpers are useful only when opt-in, target scope, command construction, rate limits, and artifact redaction are enforced at the scanner and process sinks."
categories: [daily, ai-security]
tags: [web-scanning, ffuf, scope-control, subprocess, artifact-redaction, oss-hardening]
---

The 2026-05-17 Singapore window was a focused RAPTOR web-scanner day. The shipped change added `ffuf` discovery, but the interesting security shape was the guardrail around it: a fast external discovery tool should not become an ambient network scanner, shell sink, or secret-bearing artifact by default.

## Signal

The signal was controlled extension of scanner capability.

RAPTOR can now run `ffuf` during web scans, but only when the operator supplies `--ffuf-wordlist`. URL templates are checked against the configured target origin, relative templates are anchored to the scanner base URL, command execution uses an argv list rather than a shell, and reports keep raw JSON as a separate artifact while embedding only a compact redacted summary.

That is the useful pattern: adding a more powerful recon helper is acceptable when the default is inert and every risky sink has a local guard.

## Merged PRs

- [gadievron/raptor #489](https://github.com/gadievron/raptor/pull/489) — `feat(web): add opt-in ffuf discovery`.

## What shipped or moved

RAPTOR added an opt-in `ffuf` runner for web scans. The feature is not enabled by scanner presence alone; it runs only when an operator provides a wordlist through `--ffuf-wordlist`.

The PR added scanner controls for the `ffuf` binary, path template, threads, rate, timeout, and report result limit. It also added target-origin checks for absolute templates and base-URL anchoring for relative templates, which keeps discovery tied to the configured scan target instead of letting a convenience template drift into a different host.

The process boundary was tightened too. `ffuf` is invoked through `subprocess.run([...])`, not through shell string construction. Results are split between raw `ffuf_results.json` and a compact `web_scan_report.json` summary with common secret-bearing URL parameters redacted. Tests cover scoping, command construction, validation, redaction, result limiting, and scanner integration.

## Observed pattern

External scanner integration is a trust-boundary expansion, not just a feature flag.

```text
operator scan config / target URL / path template / wordlist
    -> scanner option parsing and target-origin validation
        -> subprocess invocation and network request loop
            -> raw artifact plus public/embedded report summary
```

Each arrow carries a different risk. The config path decides whether the helper is inert by default. The template path decides whether discovery stays on the intended origin. The process path decides whether arguments remain data rather than shell syntax. The artifact path decides whether high-volume URLs, query parameters, and scanner output leak more than the report needs.

## External reference

- [ffuf](https://github.com/ffuf/ffuf) — useful as a fast web fuzzer, but its speed and flexibility make opt-in execution, target scope, and rate controls part of the safety boundary.
- [OWASP Web Security Testing Guide: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/) — discovery is a normal testing phase, but it should remain tied to authorized scope and reproducible evidence.
- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html) — scanner helpers that accept URLs or templates can become server-side request primitives if target validation is not enforced where network I/O occurs.
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html) — argv-based subprocess invocation is the right default when user-controlled paths, templates, or binary names reach a local process sink.

## What was learned

A discovery helper changes the threat model even when it is intended for authorized testing. It adds a new network request generator, a new local process boundary, and new artifacts. The review should therefore ask what happens if an attacker, plugin, model-generated workflow, or mistaken operator controls the template, target, wordlist, binary path, or report consumer.

The strongest part of the change is that the PR did not rely on a single safety claim. It layered the control: explicit enablement, origin-scoped templates, shell-free invocation, bounded runtime knobs, raw artifact separation, report summary limits, and redaction. That makes the feature easier to accept because the default posture stays quiet and the risky edges are testable.

The lesson also generalizes to AI-assisted security tooling. When a model or agent suggests adding a scanner, fuzzer, browser, MCP tool, or recon helper, the safe question is not only "does it find more?" It is "where can it send requests, how is it invoked, what does it persist, and what summary is safe to show?"

## Takeaways

- Treat external scanners, fuzzers, browsers, and recon helpers as capability sinks: opt-in by default, scope checked at the request generator, and bounded by rate, timeout, and result limits.
- URL/path templates need target-origin validation at the point that constructs the concrete scan URL, not only in documentation or CLI help.
- Subprocess integrations should prefer argv lists, avoid shell execution, and test hostile template/argument cases.
- Scanner artifacts need two views: raw evidence for private review and a compact redacted summary for broader reports.

## Repeat next time

- For every new scanner/helper integration, map `config -> template -> request generator -> subprocess -> artifact` before approving the feature.
- Add regression tests for off-origin absolute templates, relative-template anchoring, shell metacharacters, result limits, and secret-bearing query parameters.
- Keep high-volume raw scanner output separate from public or embedded summaries, and redact common token/password/key parameters before report inclusion.
- If a discovery tool can be driven by an agent or workflow later, require an explicit operator opt-in path rather than enabling it through ambient scanner defaults.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchor: `05 - Workflows/Checklist - URL Fetch and SSRF Review.md`; the May 17 observation was routed back there as an external-discovery-helper variant.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`; the sink-level rule now includes scanner helpers that generate network traffic, spawn local processes, and persist artifacts.
- Public artifact: this post keeps the lesson at capability-boundary level and does not include private report details or uncoordinated exploit specifics.
