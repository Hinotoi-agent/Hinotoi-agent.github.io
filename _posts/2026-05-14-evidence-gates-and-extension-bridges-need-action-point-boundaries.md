---
layout: post
title: "2026-05-14 — Evidence gates and extension bridges need action-point boundaries"
takeaway: "Security evidence and browser automation both become safer when authority is checked at the final sink, not only at the earlier workflow or feature boundary."
categories: [daily, ai-security]
tags: [evidence, browser-extension, tool-calls, redaction, local-control-plane, verifymate]
---

The 2026-05-14 Singapore window mixed a new evidence-checking toolchain with several extension and local-control-plane hardening PRs. The common thread was action-point control: a broad feature flag, a trusted-looking route, or a generated report is not enough. The boundary has to be enforced where data is emitted, where tools execute, where extension storage is touched, and where local credentials are rewritten.

## Signal

The strongest signal was convergence between two sides of the review loop.

Verifymate moved from a report helper into a deterministic pre-submission gate: templates, strict mode, line-level evidence, structured checker rows, destination-specific readiness profiles, and secret redaction for generated evidence snippets. That is private workflow hardening, but it directly changes public security quality because it forces findings to prove attacker control, reachability, impact, policy fit, and file/line evidence before PR or disclosure work consumes more time.

The `steipete/summarize` PRs showed the same boundary rule in live product code. Page script should not synthesize hover gestures into authenticated daemon summaries, model output should not become browser automation without a fresh user decision, page-visible `postMessage` should not expose extension artifact storage, and a routine config refresh should not widen permissions on credential-bearing files.

## Merged PRs

- [Hinotoi-agent/Verifymate #5](https://github.com/Hinotoi-agent/Verifymate/pull/5) — `feat: redact secrets in evidence snippets`.
- [Hinotoi-agent/Verifymate #4](https://github.com/Hinotoi-agent/Verifymate/pull/4) — `feat: add profile-aware evidence readiness`.
- [Hinotoi-agent/Verifymate #3](https://github.com/Hinotoi-agent/Verifymate/pull/3) — `feat: add structured checker gates`.
- [steipete/summarize #217](https://github.com/steipete/summarize/pull/217) — `[security] fix(refresh-free): keep config rewrites private`.
- [steipete/summarize #218](https://github.com/steipete/summarize/pull/218) — `[security] fix(extension): harden hover summary trust boundary`.
- [Hinotoi-agent/Verifymate #2](https://github.com/Hinotoi-agent/Verifymate/pull/2) — `feat: show line-level evidence locations`.
- [steipete/summarize #219](https://github.com/steipete/summarize/pull/219) — `[security] fix(extension): confirm automation tool calls`.
- [steipete/summarize #222](https://github.com/steipete/summarize/pull/222) — `[security] fix(extension): guard automation artifacts bridge`.
- [Hinotoi-agent/Verifymate #1](https://github.com/Hinotoi-agent/Verifymate/pull/1) — `feat: add report templates and strict mode`.

## What shipped or moved

Verifymate gained the mechanics needed to become a real gate instead of a prose formatter. It can generate starter reports, fail strict mode on weak or invalid findings, point evidence back to file and line snippets, emit stable structured checker rows, distinguish readiness profiles such as preflight, CVE request, GitHub PR, and internal note, and redact common secret-bearing values before Markdown or JSON output leaves the local workflow.

That changed the vault workflow too. The OSS review loop and source-code discovery loop now require Verifymate before serious PR or disclosure work, and the 2026-05-14 checklist-change note records the rule: save `.verifymate.md` and `.verifymate.json` beside the finding, then use non-`PASS` verdicts to constrain the next LLM prompt to the exact failed gaps.

The Summarize fixes tightened four separate sink boundaries:

- config rewrites now preserve private `~/.summarize` directory and `config.json` file modes when `refresh-free` preserves credential-bearing settings;
- hover summaries require browser-trusted events and reject localhost, link-local, private, and other non-public literal targets before the daemon token is used;
- model-requested automation tool calls require explicit user confirmation before `executeToolCall` runs;
- automation artifact reads, writes, lists, and deletes moved away from a page-visible `window.postMessage` bridge and behind an extension/user-script messaging path with an extension-controlled armed-tab window.

## Observed pattern

The reusable pattern is sink-side proof for both evidence and action.

```text
finding or page/model input
    -> workflow / extension / daemon feature
        -> privileged sink
            -> report output, filesystem permission, daemon fetch, browser automation, or extension artifact storage
```

The unsafe shape is to trust an earlier boundary because it looks intentional: automation was enabled, a content script forwarded the message, the hover feature was user-facing, a config refresh was local, or a report generator merely quoted repository text. The safer shape is to ask again at the final sink: is this caller still authorized, is this event real, is this target public, is this file still private, is this tool call approved, and is this evidence safe to emit?

This matters for AI security because many agent and MCP failures are not exotic model failures. They are old web and host-security bugs reintroduced through model output, browser bridges, local daemons, generated evidence, and convenience transports.

## External reference

- [OWASP Top 10 for LLM Applications — LLM01 Prompt Injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful anchor for treating model-suggested actions as untrusted until an action-point gate approves them.
- [Chrome Extensions documentation — Content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts) — content scripts run between page and extension worlds; extension storage or privileged APIs should not be exposed through page-visible message bridges without a narrower channel and authorization guard.
- [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html) — the config-rewrite case is a reminder that rewrite paths must preserve the credential boundary, not only initial creation paths.
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html) — evidence snippets are also outputs; generated reports should not copy secrets into public or machine-readable artifacts.

## What was learned

The same review habit applies to reports and runtime code: identify the final privileged sink and make the check live there. A candidate finding is not ready because a draft says “RCE” or “SSRF”; it is ready when the evidence points to real files, real lines, attacker-controlled input, a reachable sink, and bounded impact. A browser extension tool call is not safe because automation is generally enabled; it is safe only after the exact tool call is shown and approved. Artifact storage is not safe because a tab id exists; it is safe only when the sender is on the trusted extension/user-script path during an armed execution window.

The redaction work also changed the evidence model. A tool that quotes source lines becomes a disclosure surface if it copies tokens, bearer headers, basic-auth strings, URL userinfo, or assignment-style secrets into Markdown or JSON. Evidence quality and evidence hygiene have to ship together. Otherwise the process that is meant to make reports safer becomes another leak path.

The Verifymate profile work is the workflow lesson. Different destinations need different evidence bars, but the decision should be explicit and machine-readable. Internal notes can tolerate weaker readiness than a CVE request; a GitHub PR needs patch and maintainer-facing evidence; a CVE request needs version, impact, repro, duplicate-review, and mitigation clarity. Making those profiles visible prevents both overclaiming and needless overwork.

## Takeaways

- Treat generated evidence as a security output. Redact secrets before Markdown and JSON artifacts leave the local review loop.
- Put approval, authorization, locality, and permission checks at the action sink, not only at the feature toggle or caller boundary.
- Browser extension bridges should prefer extension-controlled or user-script channels over page-visible `window.postMessage` for privileged artifact operations.
- Deterministic gates save review time only when their failures narrow the next prompt; do not ask for a full fresh audit when the missing field is known.
- Readiness profiles are useful because “enough evidence” depends on whether the next step is preflight triage, a GitHub PR, a CVE request, or an internal note.

## Repeat next time

- Before filing a serious finding, run the Verifymate gate, save both artifacts beside the vault finding, and fix or explicitly explain every non-`PASS` gap.
- When reviewing extensions, list every page-visible bridge and ask whether it can reach storage, network, debugger, native input, filesystem, or automation sinks.
- For model/tool workflows, require a final approval or policy check immediately before the tool executes, even if a broader automation setting is already enabled.
- For local config and artifact rewrite paths, test the second write, refresh, cleanup, and rename path, not only first-run creation.
- When a report generator quotes repository lines, include positive redaction tests and false-positive tests so useful evidence remains readable while secrets are masked.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md`, `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, and `05 - Workflows/Workflow - Finding Writeup Loop.md`.
- Checklist-change anchor: `05 - Workflows/Checklist Change - 2026-05-14 Verifymate pre-submission gate.md`.
- Takeaway anchors: `06 - Lessons/Takeaway - LLM discovery candidates need explicit attacker server impact contracts.md` and `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`.
- Finding anchor: `03 - Findings/Finding - Summarize daemon slidesDir host path control.md`; the new extension/config observations should stay routed through the same boundary-first checklist system instead of becoming site-only notes.
