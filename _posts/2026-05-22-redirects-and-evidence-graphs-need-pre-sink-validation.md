---
layout: post
title: "2026-05-22 — Redirects and evidence graphs need pre-sink validation"
takeaway: "Network, workflow, and evidence boundaries become reliable only when validation sits immediately before the sink and the proof chain is preserved as structured review data."
categories: [daily, ai-security]
tags: [ssrf, redirects, vulnweave, evidence-graphs, source-to-sink, oss-hardening]
---

The 2026-05-22 Singapore window had three merged PRs: one SSRF hardening fix in `HKUDS/nanobot` and two public workflow/tooling updates in `Hinotoi-agent/vulnweave`.

## Signal

The useful signal was boundary placement.

`web_fetch` already had URL validation, but redirect handling meant the actual outbound request primitive could still move to a private target before the guard saw the final URL. VulnWeave moved the same idea into the review workflow: the candidate is not useful until the chain from source to sink, evidence, exported finding, and vault insight stays intact.

The shared lesson is not “add more checks.” It is place the check where the side effect happens, then preserve the proof path so future reviews can see why that placement was necessary.

## Merged PRs

- [HKUDS/nanobot #3928](https://github.com/HKUDS/nanobot/pull/3928) — [security] fix(web): validate redirect targets before fetching
- [Hinotoi-agent/vulnweave #3](https://github.com/Hinotoi-agent/vulnweave/pull/3) — feat: complete VulnWeave workflow loop
- [Hinotoi-agent/vulnweave #1](https://github.com/Hinotoi-agent/vulnweave/pull/1) — ci: add validation workflow and install docs

## What shipped or moved

`nanobot` switched `web_fetch` redirect handling away from automatic follow behavior and into an explicit manual redirect loop. Each `Location` is resolved and validated before the next request is made, and both the image prefetch path and readability fetch path use the same redirect boundary. The regression tests assert the property that matters for SSRF: a blocked loopback/private redirect target is not requested at all.

`vulnweave` gained the end-to-end workflow loop:

```text
repo -> map -> candidates -> export-finding -> vault-graph -> vault-insights
```

The public tool now exports candidate findings into a vault-shaped record, enriches source graphs with file/function/call/handler/scope/route/webhook evidence edges, and includes focused detector patterns for list-filter/direct-load drift, bearer-handle ownership gaps, upload/write path risk, prompt-content-to-host-tool risk, and public route/webhook auth drift.

The earlier CI/install PR made that workflow easier to validate and repeat: tests, Ruff, compile checks, editable install docs, and examples now line up with the packaged CLI.

## Observed pattern

Pre-sink validation and graph-shaped evidence are the same discipline at different layers.

```text
attacker-controlled input
    -> transformation / redirect / resolver / detector
        -> request, file, tool, route, or workflow sink
            -> proof that the unsafe sink was not reached
                -> vault record that keeps the chain reusable
```

For SSRF, the weak pattern validates the starting URL and inspects the final response after the client has already followed redirects. The stronger pattern validates every candidate target before network I/O.

For vulnerability discovery, the weak pattern records a promising candidate as prose and loses the exact boundary map. The stronger pattern keeps the source-to-sink chain, sibling checks, fix strategy, and checklist learning as structured review data that can feed the vault instead of becoming an isolated note.

## External reference

- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html) — public anchor for cases where user-controlled URLs can make the server reach unintended internal or private network targets.
- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — useful for treating URL parsing, redirects, DNS/IP resolution, and outbound request controls as one fetch-path boundary.
- [OWASP Top 10 for LLM Applications: LLM06 Sensitive Information Disclosure](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — a category-level anchor for agent/tool cases where model-driven or user-driven fetches can expose data reachable from the host environment.

## What was learned

Redirect security is ordering-sensitive. If the HTTP client sends the redirected request before validation runs, the later block is still useful for the user-visible result but too late for the network boundary. The test must prove absence of the internal request, not only a final blocked error.

The same ordering rule applies to review infrastructure. A source-code candidate should not jump directly from “interesting pattern” to “PR text.” It needs a graph pass that records attacker control, entry surface, trust boundary, primitive, impact, evidence, sibling review, prior-art search, fix strategy, and checklist learning. Otherwise the public fix may ship, but the private research system learns less than it should.

## Takeaways

- SSRF fixes should validate every redirect hop before the next outbound request, not after the HTTP client has already followed it.
- Regression tests for fetch guards should assert negative side effects: the private, loopback, link-local, or metadata target receives no request.
- Discovery tooling is most useful when it carries candidates into vault-ready source-to-sink records instead of leaving them as detached scanner output.
- CI and install documentation are part of security tooling quality when they make the evidence loop repeatable for maintainers and future reviews.

## Repeat next time

- For every URL-fetch finding, write the chain as `input URL -> parser/resolver -> redirect/retry/client primitive -> outbound request`, then place validation immediately before the request primitive.
- Test both visible denial and sink absence: blocked result, no internal request, capped redirects, and safe public redirects still working where compatibility matters.
- For every strong candidate, export or record a graph-shaped finding before PR work: source, boundary, sink, evidence, sibling variants, prior art, fix, and checklist learning.
- Route public observations back into the vault takeaway/workflow layer before treating the daily post as complete.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md`, `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, and `05 - Workflows/Workflow - Finding Knowledge Graph Loop.md`.
- Checklist/change anchors: `05 - Workflows/Checklist Change - 2026-05-22 finding knowledge graph workflow.md` and the URL-fetch / SSRF review checklist path.
- Takeaway anchor: `06 - Lessons/Takeaway - Transport redirect validation must live in the actual fetch path.md`, refreshed with the `nanobot` redirect-order reinforcement.
- PR anchors: `HKUDS/nanobot#3928`, `Hinotoi-agent/vulnweave#3`, and `Hinotoi-agent/vulnweave#1`, merged during the 2026-05-22 Singapore window.
