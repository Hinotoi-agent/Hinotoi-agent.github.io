---
layout: post
title: "2026-05-16 — Remote trust boundaries need sink-level denial"
takeaway: "Remote-channel and test-only hardening both matter when they prove the dangerous handler, session, crawler, or terminal sink cannot be reached by the wrong input."
categories: [daily, ai-security]
tags: [remote-control-plane, slack, autopilot, regression-tests, crawler-limits, terminal-safety, ai-agents]
---

The 2026-05-16 Singapore window combined OpenHarness remote-command hardening with RAPTOR regression and crawl-limit work. The common thread was not only "make the flag false" or "add a test." The useful boundary is the point where the remote message, session key, crawler queue, terminal output, or Git/autopilot handler would actually create side effects.

## Signal

The strongest signal was the separation between admission metadata and sink behavior.

OpenHarness landed three security PRs around remote channel handling: Slack thread sessions now remain sender-scoped, `/commit` stays local-only unless an operator intentionally opts it into remote administration, and `/autopilot` stays local-only by default so remote messages cannot start autonomous local agent runs. RAPTOR landed two test/evidence PRs: terminal-control sanitisation regressions now cover OSC 8 hyperlinks, OSC 52 clipboard writes, DCS/PM/APC controls, partial escape sequences, and long hostile strings; scanner-level crawl limits now flow into the actual `WebCrawler` used by `WebScanner`.

The pattern is direct: a boundary is not proven by a route label, CLI option, or sanitizer name. It is proven when the dangerous sink is unreachable or bounded on the real path.

## Merged PRs

- [HKUDS/OpenHarness #255](https://github.com/HKUDS/OpenHarness/pull/255) — `[security] fix(ohmo): scope Slack thread sessions by sender`.
- [HKUDS/OpenHarness #258](https://github.com/HKUDS/OpenHarness/pull/258) — `[security] fix(commands): keep autopilot local-only by default`.
- [HKUDS/OpenHarness #261](https://github.com/HKUDS/OpenHarness/pull/261) — `[security] fix(commands): keep /commit local-only over remote channels`.
- [gadievron/raptor #498](https://github.com/gadievron/raptor/pull/498) — `test(web): honor scanner crawl limits`.
- [gadievron/raptor #487](https://github.com/gadievron/raptor/pull/487) — `test: harden log sanitisation regressions`.

## What shipped or moved

OpenHarness tightened three remote-channel boundaries.

Slack thread routing stopped using a senderless session-key override for threaded channel messages. Thread metadata is still preserved for replies, but the central gateway now derives sender-scoped session keys so another allowed participant in the same Slack thread cannot reuse the same runtime/session key and retrieve retained conversation text through `/summary`.

`/autopilot` became local-only by default unless an operator explicitly opts it into the remote-admin command allowlist. The regression path matters: a remote `/autopilot run-next` message is denied before it reaches the autopilot agent runner, so attacker-controlled task-card content does not start a local autonomous OpenHarness run through the remote channel.

`/commit` received the same local-only treatment for Git side effects. Remote channel messages cannot stage workspace changes, create commits, or trigger local Git hooks by default. The compatibility path is explicit: trusted deployments can use `remote_admin_opt_in=True`, but the default remote boundary now denies before the Git handler runs.

RAPTOR moved two proof surfaces forward. The crawler test now proves `WebScanner(max_depth=0, max_pages=1)` passes those scanner-level controls into `WebCrawler` and only requests the seed page. The log-sanitisation tests lock in terminal-control handling for OSC hyperlinks, clipboard writes, other control families, partial escapes, and long hostile strings without claiming a new runtime fix where the sanitizer already behaved correctly.

## Observed pattern

Remote and model-adjacent systems need sink-level denial, not just entry-point intention.

```text
remote message / tool output / scan target output
    -> gateway, scanner, parser, sanitizer, or registry
        -> session, agent runner, Git handler, crawler, terminal/log sink
            -> prove denial, scoping, bound, or neutralization there
```

The OpenHarness fixes show the control-plane version: command metadata must travel all the way to the registry and gateway path that decides whether a remote sender can reach a local action. Session identity must include the actor at the point where retained memory is selected, not merely in the surrounding channel context.

The RAPTOR PRs show the evidence version: a CLI option is not a resource boundary until the concrete crawler uses it, and a sanitizer is not a terminal boundary until regressions cover the control sequences that create side effects in real terminals.

## External reference

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM06 Excessive Agency is the useful anchor for remote messages that can reach agent runners, Git actions, or other host-side capabilities.
- [CWE-862: Missing Authorization](https://cwe.mitre.org/data/definitions/862.html) — remote slash-command and session-routing checks need actor/context enforcement before protected actions or retained state are reached.
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html) — shared thread/session state and terminal/log artifacts are disclosure sinks when identity or sanitisation is incomplete.
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html) — crawler limits only matter when the actual crawler queue and request loop consume them.

## What was learned

Local-only has to be tested as a property of the command sink. For `/autopilot`, the important fact is not only that the command registry says remote invocation is disabled; it is that a remote gateway message cannot invoke the runner. For `/commit`, the denial must happen before staging, commit creation, or local Git hooks can run. That shape is much stronger than a route-level assertion because it proves absence of side effects.

Identity scoping is similar. Slack thread metadata is useful for reply continuity, but it cannot become the whole session key in a shared channel. The actor has to remain part of the retained-state lookup, otherwise a convenience feature becomes a cross-user memory boundary failure.

The RAPTOR work is a reminder not to dismiss test-only PRs. Regression coverage is part of the security boundary when it preserves the exploit or failure shape that mattered: terminal-control output should stay inert at the logging sink, and advertised crawl limits should bound the crawler that performs the requests.

## Takeaways

- Treat remote slash commands that touch Git, autonomous agents, credentials, config, or workspace state as local-only by default unless a deployment makes a deliberate remote-admin choice.
- Regression tests should prove both user-visible denial and absence of sink-side effects: no runner call, no commit, no hook, no retained-session crossover, no unexpected crawl expansion.
- Session keys for shared chat/thread surfaces need actor identity at the retained-state lookup, not only in outer channel metadata.
- Test-only hardening is valuable when it locks the real path: parser/output -> sanitizer -> terminal/log sink, or scanner option -> crawler queue -> request loop.

## Repeat next time

- For every remote command, map `remote message -> parser/router -> registry -> handler -> side-effect sink`, then add at least one regression that asserts the handler was not called.
- For every shared chat thread or channel session, compare the session key against sender identity and retained-memory lookup, not just reply-thread continuity.
- For scanner and crawler knobs, test the smallest nonzero/zero bounds against a local fake target and count actual requests plus persisted artifacts.
- For terminal/log sanitizers, keep hostile control-sequence fixtures in regression coverage even when no runtime code changes were needed.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchor: `05 - Workflows/Checklist - Authz Coverage Review.md`.
- Finding anchors: `03 - Findings/Finding - OpenHarness remote autopilot full-auto agent execution.md` and `03 - Findings/Finding - OpenHarness Slack thread summary session leak.md`.
- Disclosure anchor: `10 - Disclosure/Pending CVE Requests/Pending CVE Request - HKUDS - OpenHarness - sensitive control-plane commands remained remotely invocable by default.md`.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`; the May 16 observation was routed back there as a remote-command/session/test-proof variant rather than left only on the public site.
