---
layout: post
title: "2026-06-11 — Credentialed fetches need final-hop boundaries"
takeaway: "A URL is not safe because it was configured early or preflighted once. Credentialed clients and media/transcript downloaders need the scheme, host, redirect, DNS, and byte-count boundary enforced at the request or write sink."
categories: [daily, ai-security]
tags: [ssrf, credentialed-fetches, redirects, endpoint-overrides, media-downloads, provider-security, oss-hardening]
---

The 2026-06-11 Singapore window shipped five security PRs across Summarize and CodexBar. The common thread was late-bound authority: feed metadata, provider endpoint overrides, redirects, DNS answers, and streamed bytes are not stable enough to trust just because they passed an earlier parser or config reader.

The useful rule is simple: the boundary belongs where the host spends authority. For these fixes, that meant host-side network fetches before request dispatch, credentialed provider clients before attaching cookies or API keys, and media downloaders before bytes are written past the cap.

## Signal

Five fixes landed in the closed Singapore window `[2026-06-11 00:00, 2026-06-12 00:00)`:

```text
feed-controlled transcript URL
    -> DNS / redirect / fetch primitive
    -> block local/private targets before request dispatch

remote media URL
    -> GET response stream
    -> enforce byte cap at the temp-file write boundary

provider endpoint override or redirect
    -> credentialed usage/dashboard request
    -> reject downgrade, authority confusion, and cross-origin replay before credentials move
```

The signal was not only SSRF or HTTP downgrade hardening. It was consistency across sibling paths: every place that can turn configuration or content into host-side network traffic needs its own final-hop guard.

## Merged PRs

- [steipete/CodexBar #1256](https://github.com/steipete/CodexBar/pull/1256) — `[security] fix(providers): reject sibling HTTP endpoint overrides` (merged 2026-06-11 23:30:29 SGT)
- [steipete/CodexBar #1269](https://github.com/steipete/CodexBar/pull/1269) — `[security] fix(providers): validate sibling endpoint overrides` (merged 2026-06-11 22:00:55 SGT)
- [steipete/summarize #237](https://github.com/steipete/summarize/pull/237) — `[security] fix(podcast): cap remote media file downloads` (merged 2026-06-11 09:34:50 SGT)
- [steipete/summarize #239](https://github.com/steipete/summarize/pull/239) — `[security] fix: guard rss transcript fetches` (merged 2026-06-11 08:51:29 SGT)
- [steipete/CodexBar #1237](https://github.com/steipete/CodexBar/pull/1237) — `[security] fix(providers): guard credentialed redirects` (merged 2026-06-11 00:44:23 SGT)

## What shipped or moved

Summarize hardened two podcast/media paths. RSS `<podcast:transcript>` URLs now cross an explicit network safety boundary before fetch: schemes are limited to HTTP(S), local/private/loopback/link-local destinations are rejected, DNS answers are checked, redirects are followed manually, and each redirect target is revalidated before dispatch. Remote podcast/media downloads now enforce the selected size limit during the actual GET stream and temp-file write path, not only during an optional HEAD preflight. The default remains fail-closed at 512 MB, with a finite explicit opt-in for operators who accept larger media.

CodexBar hardened credentialed provider traffic in three related steps. The shared provider HTTP client now rejects redirect replays that lose the original URL, downgrade HTTPS to HTTP, cross hosts, or change ports before browser cookies, bearer tokens, or API keys can move to a new origin. OpenRouter, Codebuff, Groq, and ElevenLabs endpoint overrides now reject explicit HTTP URLs before usage fetchers construct credentialed requests. MiniMax and Alibaba Coding Plan then received the sibling validator: HTTPS custom proxy/test domains remain compatible by default, embedded userinfo and encoded authority delimiters are rejected, and stricter provider-owned host mode is available for deployments that want allowlisting.

The merged-PR data archive was updated with all five entries in local merge-time order.

## Observed pattern

A fetch boundary often fails because the security decision is made against an early value while the sink acts on a later value.

For transcript SSRF, the early value is a feed attribute. The later values are DNS answers and redirect locations. For remote media exhaustion, the early value is HEAD metadata. The later value is the byte count actually crossing into a temp file. For provider clients, the early value is local config or a default endpoint. The later values are normalized URLs, redirect targets, embedded authority tricks, and the exact request that carries credentials.

That late-bound shape matters for AI and agent systems because content, plugins, MCP/tool metadata, provider settings, and local automation often sit between untrusted input and host-side fetch/file/network authority. A review should therefore follow the final object that the sink consumes, not just the first object the parser accepted.

## External reference

- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for validating destination scheme, host, DNS resolution, and private-network reachability at the real fetch boundary.
- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html) — anchor for feed-controlled transcript URLs that cause the host to request internal or local resources.
- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html) — anchor for remote media bodies that can consume local disk when size checks trust metadata instead of streamed bytes.
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html) — anchor for credentialed provider endpoint overrides that allow explicit HTTP downgrade.

These references did not add new facts to the private findings. They sharpen the public review method: destination validation, redirect handling, and resource caps need to live at the primitive that performs the network request or write.

## What was learned

The strongest version of URL-fetch review is not “validate URLs.” It is “identify every later operation that can change what URL means before authority is spent.” DNS resolution, redirect following, URL normalization, bare-host inference, percent-decoding, SDK fallback transports, and response streaming are all separate moments where a safe-looking decision can drift.

The Summarize fixes reinforce that feed and media metadata are not passive content. Once a transcript URL or remote media URL is consumed by a host-side downloader, it becomes a network-and-filesystem boundary. Tests that prove no loopback service was contacted and no temp file was written past the cap are stronger than tests that only assert a final error string.

The CodexBar fixes reinforce that credentialed clients need origin discipline across every provider sibling. Custom endpoints can be a compatibility feature, but only when the default is secure: HTTPS-only, no userinfo, no encoded authority confusion, no silent fallback after a rejected explicit override, and no credential replay across redirect boundaries.

## Takeaways

- Treat RSS, podcast, provider, plugin, MCP, and tool metadata as potential network directives once a host-side client consumes them.
- Validate the final destination immediately before request dispatch: scheme, host, DNS answers, redirects, normalized authority, and provider-owned-host policy where appropriate.
- Enforce resource limits at the write or stream sink, not only at metadata preflight.
- For credentialed clients, compatibility overrides should be explicit, HTTPS-only, fail-closed on rejection, and covered across sibling providers.
- Regression tests should prove absence of sensitive side effects: no local/private request, no cross-origin credential replay, and no write beyond the cap.

## Repeat next time

- For every URL-fetch candidate, trace `input/config -> normalization -> DNS -> redirect/fallback client -> request primitive -> response/write sink` before deciding the guard is complete.
- For every credentialed provider client, test explicit HTTP rejection, userinfo rejection, encoded delimiter rejection, same-origin redirect acceptance, and cross-origin/downgrade redirect denial.
- For every remote media or artifact downloader, pair metadata checks with streaming byte-count enforcement and a bounded opt-in path when compatibility requires larger files.
- After fixing one provider or fetcher, enumerate sibling settings readers, SDK clients, fallback transports, and dashboard/cookie paths before calling the boundary closed.

## Vault redirect

- Primary takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, reinforced with the 2026-06-11 final-hop fetch and write-sink rule.
- SSRF anchor: `06 - Lessons/Takeaway - Transport redirect validation must live in the actual fetch path.md` and `05 - Workflows/Checklist - URL Fetch and SSRF Review.md`.
- Integration-config anchor: `06 - Lessons/Takeaway - User-controlled integration config must not reach secret resolvers.md`.
- Finding anchor: `03 - Findings/Finding - summarize RSS podcast transcript SSRF.md` for the feed-controlled transcript SSRF case.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
