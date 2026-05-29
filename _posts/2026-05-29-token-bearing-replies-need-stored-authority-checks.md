---
layout: post
title: "2026-05-29 — Token-bearing replies need stored authority checks"
takeaway: "A reply URL or conversation reference becomes security authority once a later client attaches credentials to it."
categories: [daily, ai-security]
tags: [bot-framework, ssrf, token-disclosure, stored-authority, webhook-security, oss-hardening]
---

The 2026-05-29 Singapore window had one merged security PR in `HKUDS/nanobot`. The useful signal was not only that a URL was checked; it was that a stored conversation reference was treated as authority before a later bearer-authenticated reply could use it.

## Signal

The important boundary was a delayed one.

An inbound chat activity can carry routing metadata for a later reply. That metadata looks passive while it is being stored, but it becomes active authority when a Bot Framework client later builds an outbound request from it and attaches an access token. The safe pattern is to validate the authority when it enters durable reply state and again immediately before the token-bearing request.

## Merged PRs

- [HKUDS/nanobot #4047](https://github.com/HKUDS/nanobot/pull/4047) — [security] fix(msteams): trust service URLs before replies

## What shipped or moved

`nanobot` hardened the Microsoft Teams channel around Bot Framework service URLs. Conversation references are now accepted only when the service URL is HTTPS and matches trusted Bot Framework / Teams host patterns. The send path also performs a final trust check before requesting or sending a bearer-authenticated reply.

The patch covers both sides of the stored-authority problem:

```text
inbound activity
    -> conversation reference storage
        -> later reply construction
            -> token-bearing outbound request
```

New regression coverage exercises the forged/untrusted inbound service URL case and the legacy poisoned-reference case. That second test matters: a storage-time check protects new state, but use-time denial protects old persisted state and future paths that might populate the reference table differently.

## Observed pattern

Stored reply metadata is a capability when a later component consumes it with credentials.

For webhooks, chat connectors, bot frameworks, MCP callbacks, and agent gateways, the dangerous value may not be used at the same time it is received. A URL, conversation ID, callback base, route handle, or delivery target can sit quietly in state until another subsystem turns it into a network request, file write, tool call, or credential-bearing action.

The review question should therefore be:

```text
What stored value will the trusted host later consume with ambient authority?
```

If the answer includes bearer tokens, provider credentials, internal network reachability, workspace files, approval state, or durable routing tables, the stored value needs both admission validation and sink-side revalidation.

## External reference

- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html) — public anchor for cases where attacker-influenced URLs make a server issue unintended outbound requests.
- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — useful for treating URL parsing, allowlists, redirects, and request-time enforcement as one outbound boundary.
- [Microsoft Bot Framework authentication documentation](https://learn.microsoft.com/en-us/azure/bot-service/bot-builder-concept-authentication) — a reminder that bot replies are not just messages; they can be authenticated service calls and should inherit the same trust-boundary discipline as other credentialed clients.

## What was learned

The stronger framing is “stored authority,” not only “URL validation.” A user-controlled or integration-controlled field becomes security-sensitive when the host later combines it with credentials or privileged network position. The fix belongs at the point where the authority is admitted into state, and at the point where the authority is consumed by the sensitive client.

This also keeps severity claims bounded. The default inbound Bot Framework validation remains an important prerequisite boundary. The merged fix hardens the conditional path where that boundary is disabled, bypassed, or misconfigured, and it prevents the stored value from becoming unrestricted bearer-token egress.

## Takeaways

- Treat service URLs, callback bases, conversation references, and delivery targets as authority carriers when later clients attach tokens or credentials to them.
- Validate stored reply authority at admission time, but still re-check it at the send/fetch/mutation sink.
- Regression tests should prove absence of the sensitive side effect: no token fetch, no token-bearing outbound HTTP request, and no use of legacy poisoned state.
- Bound the public claim to the real deployment preconditions instead of turning a defense-in-depth hardening issue into a default-exploitable story.

## Repeat next time

- For every webhook/chat/bot connector, map `inbound activity -> stored reference -> reply/client construction -> credentialed sink` before judging impact.
- Ask whether any stored URL, callback, channel, or route handle can be populated under weaker auth than the later sink assumes.
- Test both fresh poisoning attempts and previously persisted unsafe references.
- Keep compatibility explicit: allow known trusted service hosts, support intentional configuration where needed, and deny unknown authorities before credentials are requested.

## Vault redirect

- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md` was updated with the stored reply-authority rule from `HKUDS/nanobot#4047`.
- Checklist anchor: `05 - Workflows/Checklist - URL Fetch and SSRF Review.md` remains the cross-check for token-bearing callback/reply URLs that can become SSRF plus credential disclosure.
- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` remain the canonical place to start similar reviews.
- PR anchor: `HKUDS/nanobot#4047`, merged during the 2026-05-29 Singapore window.
