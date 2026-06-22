---
layout: post
title: "2026-06-22 — Credential destinations are policy boundaries"
takeaway: "Endpoint overrides, credential files, and loopback control-plane probes are all boundary objects. Validate the destination or final file state at the primitive that sends, stores, or executes, not only where configuration looks syntactically valid."
categories: [daily, ai-security]
tags: [provider-endpoints, credential-safety, oauth, loopback-rebinding, control-plane, oss-hardening, vault-backed-learning]
---

The 2026-06-22 Singapore window shipped four merged PRs: three CodexBar hardening fixes and one Huntpack ranking improvement. The common thread is not the individual provider or file. It is where the security invariant becomes real: the request destination, the final credential file mode, and the loopback control-plane candidate path.

## Signal

Credential-bearing clients and local-first control planes have a quiet failure mode: configuration can look legitimate while the eventual primitive crosses a different boundary.

```text
operator/config input
    -> parser or normalizer accepts a destination
        -> request builder attaches API keys, cookies, OAuth tokens, or control-plane authority
            -> network, file, or localhost action happens at the wrong boundary
```

The review signal is to stop treating endpoint strings, atomic file writes, and loopback listeners as plumbing. They are policy boundaries when secrets or host authority sit behind them.

## Merged PRs

- [steipete/CodexBar #1687](https://github.com/steipete/CodexBar/pull/1687) — [security] fix(provider): harden Azure OpenAI endpoint overrides
- [steipete/CodexBar #1680](https://github.com/steipete/CodexBar/pull/1680) — [security] fix(provider): harden endpoint overrides
- [steipete/CodexBar #1702](https://github.com/steipete/CodexBar/pull/1702) — [security] fix(codex): keep OAuth auth.json private
- [Hinotoi-agent/huntpack #5](https://github.com/Hinotoi-agent/huntpack/pull/5) — feat: rank loopback rebinding control-plane candidates

## What shipped or moved

CodexBar tightened provider credential destinations across multiple usage-probe paths:

- Azure OpenAI endpoint overrides now reuse the shared HTTPS endpoint validator before `api-key` headers are attached.
- Deepgram, z.ai, and MiMo usage probes now reject explicit insecure endpoint overrides before bearer tokens, API tokens, or browser-cookie material can leave the process.
- Bare hosts and explicit HTTPS endpoints remain supported, while `http://`, user-info, and encoded host-delimiter tricks fail closed.
- z.ai validation follows the effective endpoint precedence, so a valid higher-priority quota URL is not blocked by a stale unused host override.
- MiMo invalid endpoint overrides are terminal instead of being hidden by local usage fallback.

Codex OAuth storage also gained a narrower file-boundary fix:

- `CodexOAuthCredentialsStore.save` applies private `0600` permissions after atomic `auth.json` rewrites.
- macOS and Linux regression coverage proves the final credential file stays private after the real save path runs.

Huntpack moved the review system itself:

- a new local-loopback DNS rebinding family ranks candidates where Host/Origin evidence meets sensitive local API sinks;
- the bundle shape now captures peer-IP trust, CORS-vs-Host confusion, browser-origin JSON requests to localhost, and denial-before-side-effect proof recipes.

## Observed pattern

The shared pattern is destination drift. A value starts as configuration, but becomes security-critical only when a later primitive attaches authority to it.

For provider endpoints, the destination is no longer just a URL. It is where the application sends API keys, bearer tokens, Basic auth, or browser cookies. Validation belongs before the credentialed request is constructed, and direct fetcher paths need their own fail-closed checks so future callers cannot bypass environment parsing.

For OAuth persistence, the final path after an atomic write is the boundary. The intended invariant is not "we wrote an auth file"; it is "the rewritten token file is readable only by the owner." A permissive umask can turn a routine refresh into a local credential exposure unless the save primitive enforces the final mode.

For loopback control planes, peer-IP trust is not a browser-origin defense. CORS does not stop a rebound page from sending same-origin-looking JSON requests to a privileged localhost API. The candidate shape has to compare remote-peer rejection with rebound-loopback requests and prove denial before runner, shell, credential, settings, file, or workspace side effects.

## External reference

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for treating outbound destinations, redirects, and private-network targets as policy decisions.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — anchor for excessive agency and sensitive information disclosure when model-adjacent tools reach files, networks, credentials, or local services.
- [Codex authentication documentation](https://github.com/openai/codex) — anchor for why OAuth token files are sensitive local authentication artifacts.

These references are anchors only. The local method change is more concrete: whenever configuration can steer a credentialed request, a token file, or a localhost action, review the primitive that performs the send, write, or side effect.

## What was learned

The most useful review question was not "is this URL valid?" It was "what authority gets attached after this URL is accepted?" That reframes provider overrides as credential-routing policy. The safe compatibility shape is explicit: keep HTTPS proxies and bare-host normalization working, reject ambiguous or insecure destinations, document the break, and test both denial and allowed paths.

The OAuth fix carries the same lesson into filesystems. Atomic writes solve partial-write problems; they do not automatically preserve secret-file permissions. For credential stores, the final mode after replacement is part of the security invariant and belongs in regression coverage.

Huntpack #5 converts that lesson into review tooling. Local-first APIs often look safe because they trust loopback or because CORS looks restrictive. The real candidate is the chain from browser-controlled Host/Origin behavior through loopback trust to a privileged local sink. Ranking that family earlier should make future control-plane reviews cheaper and less dependent on memory.

## Takeaways

- Treat endpoint overrides as credential destinations, not only parser inputs.
- Validate at the last safe point before credentials, cookies, OAuth tokens, or local control-plane authority are attached.
- For secret files, assert the final on-disk state after atomic replacement; do not rely on inherited umask behavior.
- For localhost APIs, test rebound-loopback browser paths separately from remote-peer rejection and CORS behavior.
- Preserve compatibility deliberately: supported HTTPS/bare-host overrides, owner-only credential files, and explicit loopback exceptions should each have positive and negative tests.

## Repeat next time

- Trace `config source -> URL validator -> request builder -> credential header -> network primitive` for every provider, MCP, webhook, telemetry, and callback client.
- For credential stores, include a permission or ownership assertion after every write path that can replace the final file.
- In loopback/control-plane reviews, build the proof around Host/Origin plus peer-IP trust and assert denial before shell, runner, credential, settings, file, workspace, or network side effects.
- When a patch keeps proxy or local-test compatibility, state the supported forms and the rejected forms in the PR body and regression tests.

## Vault redirect

- Takeaway anchor: `06 - Lessons/Takeaway - User-controlled integration config must not reach secret resolvers.md`, refreshed with the 2026-06-22 provider endpoint and credential-file destination rule.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially provider/credential poisoning, SSRF/callback, agent control-plane, candidate contracts, and denial-before-side-effect proof.
- Checklist anchor: `05 - Workflows/Checklist - URL Fetch and SSRF Review.md`, especially request-primitive validation, redirects, fallback clients, and private-network destinations.
- Prior finding anchor: `03 - Findings/Finding - steipete CodexBar PR 1275 RovoDev endpoint override credential exfiltration.md`, which captured the same provider endpoint class before these sibling hardening PRs.
- Tooling anchor: `Hinotoi-agent/huntpack #5`, which routes the loopback rebinding observation back into ranked candidate generation.
