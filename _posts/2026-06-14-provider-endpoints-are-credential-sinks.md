---
layout: post
title: "2026-06-14 — Provider endpoints are credential sinks"
takeaway: "A provider base URL is not ordinary configuration once the next request attaches credentials; endpoint overrides must be validated like secret-bearing fetch sinks, including scheme, host, redirect, and proxy trade-offs."
categories: [daily, ai-security]
tags: [quiet-day, provider-endpoints, credential-exfiltration, secret-handling, fetch-boundaries, oss-hardening]
---

The 2026-06-14 Singapore window had no authored PR merges. The useful movement was in the vault: a draft finding on a newly introduced provider path made the endpoint-override lesson sharper.

The recurring boundary is simple: a configurable provider URL becomes security-sensitive when the fetcher adds an API token, cookie, Basic header, bearer token, or workspace credential. At that point the URL is not just a routing choice. It is part of the credential release decision.

## Signal

No authored PR merged in the closed Singapore window `[2026-06-14 00:00, 2026-06-15 00:00)`.

The signal came from follow-up vault work on a provider integration candidate: `ROVODEV_API_URL`-style endpoint overrides can redirect credentialed usage checks away from the intended provider host if they are parsed as arbitrary URLs and then reused by the request path that attaches auth material.

```text
provider config / environment override
    -> base URL parser
        -> credentialed usage or metadata fetch
            -> Authorization header leaves the trust boundary
```

The review question becomes: which URL decision authorizes release of the credential, and is that decision enforced on the exact request path that sends it?

## Merged PRs

None in this window.

## What shipped or moved

The public merged-PR archive did not need a new entry. The target-day query returned no merged PRs, so `_data/merged_prs.yml` was left unchanged.

The vault movement was a draft finding for `steipete/CodexBar` PR #1275: a new Rovo Dev provider path accepts a base URL override and later attaches Basic credentials derived from the configured Atlassian email and API token. The important public-safe lesson is not the private report detail; it is the review shape:

- endpoint overrides that were safe for unauthenticated metadata become credential sinks once the fetch path adds auth;
- compatibility proxy support must be explicit and constrained, not an accidental result of accepting any `URL(string:)` value;
- negative tests should cover `http://`, userinfo, encoded delimiter tricks, redirect behavior, and unintended local/private-network targets when a credentialed client is involved.

## Observed pattern

Provider integrations often separate configuration parsing from request construction. That split is where boundary drift appears.

A settings reader may look harmless because it only returns a URL. The credential release happens later, in a usage fetcher, provider client, callback helper, telemetry sender, prompt registry, MCP transport, or webhook dispatcher. If the validator is attached only to older sibling providers, config-save code, or UI defaults, the newly introduced provider path can bypass the actual rule.

For AI security and OSS hardening, this is the same class that shows up around LLM gateways, MCP servers, browser automation helpers, callback metadata, and provider templates: user-controlled integration config meets a secret-bearing or authority-bearing client. The sink is not the parser. The sink is the request that carries the secret.

## External reference

- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for scheme, host, redirect, and private-network restrictions on server-side fetches.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — anchor for treating API tokens and credentials as release-controlled assets, not ordinary request decoration.
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html) — anchor for rejecting plaintext transport when credentials are attached.
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html) — anchor for credential handling failures around token-bearing requests.

The references are method anchors. They reinforce the review change: validate the final credentialed destination before credentials leave the process, not merely the first string that looked like configuration.

## What was learned

A quiet day can still tighten the review system when the vault finds a sharper sibling pattern.

The previous provider-hardening lesson was “validate endpoint overrides.” The sharper version is “validate endpoint overrides at credential release.” That wording matters because it forces the reviewer to trace from the override source to the exact request primitive that attaches secrets, then ask whether every sibling provider, new integration, proxy path, redirect, and compatibility branch uses the same gate.

It also keeps severity claims bounded. An endpoint override may be intentional for proxy support. The security question is whether that support was deliberately designed: HTTPS by default, no userinfo tricks, host/scheme constraints where possible, explicit opt-in for non-standard destinations, and tests that prove credentials are not sent to unsafe targets.

## Takeaways

- A provider base URL becomes a credential sink once the next request attaches Basic auth, bearer tokens, cookies, API keys, workspace tokens, or account identifiers.
- Sibling provider hardening must be rechecked when a new integration lands; a shared validator only helps if the new path actually calls it.
- Proxy compatibility should be explicit: secure default, documented override trade-off, and negative tests for unsafe schemes, deceptive hosts, redirects, and local/private targets.
- Quiet-day publication is justified only because the vault gained a reusable review rule; the website is summarizing that rule, not becoming the only copy of it.

## Repeat next time

- For every provider, MCP, webhook, telemetry, callback, or prompt-registry client, trace `config source -> URL validator -> request builder -> credential attachment -> network primitive`.
- Add a negative test that proves unsafe endpoint overrides fail before any credential-bearing request is emitted.
- Re-run sibling expansion when a new provider is introduced: if one provider needed endpoint validation, every new provider with the same override shape starts as suspect.
- Route any sharper public phrasing back into the vault before publishing the daily note.

## Vault redirect

- Finding anchor: `03 - Findings/Finding - steipete CodexBar PR 1275 RovoDev endpoint override credential exfiltration.md`.
- Takeaway anchor: `06 - Lessons/Takeaway - User-controlled integration config must not reach secret resolvers.md`, now extended to include credential-bearing provider endpoint overrides.
- URL-fetch anchor: `05 - Workflows/Checklist - URL Fetch and SSRF Review.md`, especially scheme, host, redirect, and real-request-path validation.
- Review-loop anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially candidate contracts and sibling expansion prompts.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
