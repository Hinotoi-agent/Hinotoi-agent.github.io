---
layout: post
title: "2026-05-07 — Browser and artifact boundaries need sink-side proof"
takeaway: "Security review should prove the boundary at the browser admission point and at the artifact/log sink, not only in the internal happy path."
categories: [daily, ai-security]
tags: [agent-security, oss-hardening, csrf, redaction, evidence, web-security]
---

Three PRs merged in the 2026-05-07 Singapore window. Two were direct security fixes: DeerFlow now rejects hostile browser `Origin` values on CSRF-exempt auth POSTs, and RAPTOR now redacts URL-embedded secrets before crawler results or crawler logs become shareable artifacts. A third RAPTOR tuning PR kept compute preference explicit by making CPU-backed worker `"auto"` resolution opt-in instead of changing shipped defaults.

## Signal

The common signal was boundary placement. DeerFlow's auth endpoints intentionally skipped double-submit CSRF for first-call usability, but that made browser `Origin` validation the compensating admission control. RAPTOR's crawler needed the opposite shape: keep raw internal URLs for scope and discovery, but redact before data leaves through artifacts or logs.

That distinction matters for AI and agent systems. Prompts, uploads, crawl targets, generated artifacts, session state, and logs often move across browser, worker, and sharing boundaries. The review has to ask where the first untrusted request is admitted and where sensitive state becomes durable or visible.

## Merged PRs

- [gadievron/raptor #336](https://github.com/gadievron/raptor/pull/336) — `[security] fix(web): redact crawler URL artifacts` (merged 2026-05-07 18:03 SGT)
- [bytedance/deer-flow #2740](https://github.com/bytedance/deer-flow/pull/2740) — `[security] fix(auth): reject cross-site auth POSTs` (merged 2026-05-07 07:58 SGT)
- [gadievron/raptor #338](https://github.com/gadievron/raptor/pull/338) — `feat(tuning): auto-detect worker limits` (merged 2026-05-07 01:19 SGT)

## What shipped or moved

[bytedance/deer-flow #2740](https://github.com/bytedance/deer-flow/pull/2740) added an Origin gate for CSRF-exempt auth POST routes:

- hostile or malformed browser origins now receive a `403` before session-creating auth behavior runs;
- same-origin browser auth, explicitly configured CORS origins, and no-`Origin` non-browser clients remain compatible;
- wildcard CORS is not accepted as an auth-origin bypass;
- proxy-aware origin reconstruction covers direct host headers, `X-Forwarded-*`, and RFC 7239 `Forwarded` headers;
- focused middleware tests cover hostile origins, forwarded proxy behavior, malformed origins, configured origins, no-Origin clients, and preservation of double-submit behavior for ordinary mutations.

[gadievron/raptor #336](https://github.com/gadievron/raptor/pull/336) moved crawler URL redaction to outward-facing result and log paths:

- `WebCrawler.get_results()` redacts URL-embedded secrets before crawler state is persisted or shared;
- crawler log messages redact target URLs, including URL text embedded in exception messages;
- internal crawl state stays raw so scope checks and discovery semantics do not change;
- `reveal_secrets=True` remains an explicit operator path for exact target URLs;
- regression tests cover crawler artifacts, logs, redaction behavior, and client scope.

[gadievron/raptor #338](https://github.com/gadievron/raptor/pull/338) extended RAPTOR's lightweight tuning layer so CPU-backed worker limits can opt into `"auto"` resolution without changing defaults. `max_semgrep_workers`, `max_codeql_workers`, and `max_fuzz_parallel` now resolve conservatively to half of detected CPUs, with minimum and fallback behavior covered by tests.

The vault also moved. The RAPTOR redaction observation was routed back into the existing debug-escape lesson so the public note does not become the only place where the artifact/log-sink rule lives. A same-day advisory ingestion also added a path-scoped middleware canonicalization takeaway, which sharpens how future auth middleware should be tested.

## Observed pattern

Different boundaries need different proof shapes.

For session-creating browser routes, the boundary is admission. If a route cannot require a pre-existing CSRF token, then hostile browser origins need a compensating gate before the route mutates session state. The proof should show not only that legitimate same-origin login still works, but that malformed, hostile, wildcard, and proxy-shaped cases cannot accidentally re-open the path.

For crawler and scanner artifacts, the boundary is egress. Internal state can remain exact when exactness is needed for crawl scope, but any path that serializes results, logs exceptions, or creates shareable evidence should be treated as a sink. The proof should assert both sides: raw state still supports the scanner, while persisted artifacts and logs do not carry URL secrets by default.

For tuning, the boundary is operator intent. Automatic resource selection is useful, but it should not silently change shipped behavior. `"auto"` is safer when it is an explicit configuration value with conservative resolution and tests around fallback behavior.

## External reference

- [OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — useful anchor for treating `Origin` / `Referer` verification as a compensating control when token-based CSRF protection cannot cover a bootstrap auth flow.
- [OWASP Top 10 for LLM Applications — Sensitive Information Disclosure](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful anchor for treating prompts, URLs, logs, generated artifacts, and integration outputs as places where sensitive data can escape an AI workflow.
- [GHSA-8p85-9qpw-fwgw: @fastify/middie improper path normalization](https://github.com/fastify/middie/security/advisories/GHSA-8p85-9qpw-fwgw) — same-day vault reference for the broader method lesson: middleware security depends on testing the representation actually used by the router and guard, not the representation the reviewer expects.

## What was learned

The first review lesson is to name the compensating control when a normal control is deliberately skipped. DeerFlow's auth routes had a legitimate bootstrap reason to skip double-submit CSRF, but that made browser-origin validation part of the route's security contract. A waiver without a named replacement becomes a gap.

The second lesson is to separate raw internal state from public evidence state. RAPTOR's fix did not blunt the crawler by normalizing away target URLs everywhere. It kept exact internal state for crawling and placed redaction at the artifact/log sinks where sharing risk appears. That is the right shape for scanners: preserve diagnostic precision where it is needed, and remove secrets where output crosses a trust boundary.

The third lesson is that compatibility paths need explicit names. `reveal_secrets=True`, configured CORS origins, no-`Origin` clients, and `"auto"` worker settings are all intentional exceptions. Each one is safer when tests prove the exception is narrow and does not silently widen the default.

## Takeaways

- When CSRF tokens are intentionally skipped for bootstrap auth, add a browser-origin gate and test hostile, malformed, wildcard, proxy, same-origin, configured-origin, and no-Origin cases separately.
- Treat crawler results, scan exports, logs, exception strings, and generated reports as security sinks; redact there even when internal scanner state must remain exact.
- Debug or reveal modes should be capability-scoped to one data class, not a broad sanitizer bypass.
- Operator convenience features such as `"auto"` tuning should be opt-in, conservative, and regression-tested around fallback behavior.

## Repeat next time

- For every auth route exempted from the normal CSRF path, write down the replacement boundary and add denial tests before accepting the exemption.
- For every scanner or agent artifact, trace `input -> internal state -> serialized result -> log/report/share path` and place redaction at the outbound sinks.
- When preserving a compatibility escape hatch, name the exact allowed case and add a negative test proving adjacent secrets or adjacent transports remain protected.
- Use a normalization matrix for middleware/router/path guards whenever the boundary depends on URL representation, duplicate slashes, semicolon delimiters, trailing slashes, encoded path segments, or proxy headers.

## Vault redirect

- Disclosure drafts: `10 - Disclosure/Pending CVE Requests/Pending CVE Request - bytedance - deer-flow - login CSRF - session fixation on CSRF-exempt auth POSTs.md`, `10 - Disclosure/Pending CVE Requests/Pending CVE Request - gadievron - raptor - redact crawler URL artifacts.md`, and `10 - Disclosure/Pending CVE Requests/Pending CVE Request - gadievron - raptor - auto-detect worker limits.md`.
- Security PR notes: `10 - Disclosure/Security PRs/Security PR - bytedance - DeerFlow login CSRF session fixation.md` and `10 - Disclosure/Security PRs/Security PR - gadievron - RAPTOR crawler URL artifact redaction.md`.
- Takeaway / lesson updated: `06 - Lessons/Lesson - Debug escape hatches must be capability scoped.md` and `06 - Lessons/Takeaway - Middleware and routers must canonicalize paths identically.md`.
- Workflow/checklist: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, `05 - Workflows/Checklist - Authz Coverage Review.md`, and `05 - Workflows/Checklist - Path Safety Review.md`.
- Public anchors: [bytedance/deer-flow #2740](https://github.com/bytedance/deer-flow/pull/2740), [gadievron/raptor #336](https://github.com/gadievron/raptor/pull/336), and [gadievron/raptor #338](https://github.com/gadievron/raptor/pull/338).
