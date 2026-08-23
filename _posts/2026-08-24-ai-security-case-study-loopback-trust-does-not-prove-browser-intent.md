---
layout: post
title: "2026-08-24 — Loopback trust does not prove browser intent"
date: 2026-08-24 05:00:07 +0800
permalink: /2026/08/24/ai-security-case-study-loopback-trust-does-not-prove-browser-intent/
takeaway: "A loopback peer address proves where the final socket came from, not who caused the request; reject cross-site unsafe browser methods before local trust can authorize a side effect."
categories: [case-study, ai-security]
tags: [case-study, browser-origin, csrf, loopback, local-api, control-plane, upload-security]
---

Local AI products often trust loopback traffic so their UI, CLI, and agent tooling can work without repeated credentials. That trust becomes unsafe when it is treated as proof of browser intent.

## Signal

A browser can send a request to a service on `127.0.0.1` from a remote web page. The TCP peer is local because the browser opens the connection, but the initiating principal is still the remote page.

CORS normally prevents the page from reading a cross-origin response. It does not reliably prevent a browser-simple unsafe request from reaching a local upload, settings, runner, tool, or shutdown sink. The authorization decision must therefore happen before loopback trust and before the side effect.

## Threat model

The victim runs Vibe-Trading's API locally and visits an attacker-controlled page. The page causes the victim browser to issue a cross-site unsafe request to the loopback API.

The attacker does not need to read the response. Success is the blind side effect itself. The bounded public regression uses `POST /upload`: an unauthorized file appearing in the local upload directory is sufficient proof.

The compatibility requirement is equally important. A legitimate non-browser loopback client must continue to upload while the API key is configured.

## Finding and PR

Public PR: [`HKUDS/Vibe-Trading #293 — fix: reject cross-site unsafe local API requests`](https://github.com/HKUDS/Vibe-Trading/pull/293).

Merge commit: [`5414a59e221730f2b758f5dd02378a119e2fa575`](https://github.com/HKUDS/Vibe-Trading/commit/5414a59e221730f2b758f5dd02378a119e2fa575).

Changed files:

- `agent/api_server.py` — applies the existing cross-site browser-request guard to unsafe methods before loopback dev-mode trust is honored.
- `agent/tests/test_upload_api.py` — adds a cross-site negative regression and a local non-browser compatibility control.

The vulnerable ordering was the issue: `_validate_api_auth()` could accept a request because its peer was loopback before establishing whether an unsafe browser request came from a foreign origin.

## Exploit path

The public source-to-sink chain was:

```text
attacker-controlled remote page
  -> victim browser sends cross-site POST to 127.0.0.1
  -> local API sees a loopback network peer
  -> loopback dev-mode trust bypasses configured API-key validation
  -> POST /upload processes attacker-selected content
  -> file is created in the local upload directory
```

The carrier and the actor are different. The browser is the loopback carrier; the remote origin is the actor influencing the request. Treating the carrier's socket address as authorization collapses that distinction.

This is separate from DNS rebinding and Host-header validation. A direct request to `127.0.0.1` can already cross the browser-to-local-service boundary without rebinding a hostname.

## Mitigation

The patch defines `GET`, `HEAD`, and `OPTIONS` as safe browser methods. For every other method, `_validate_api_auth()` now calls `_reject_cross_site_browser_request(request)` before checking whether the client is local.

That ordering encodes the invariant at the shared authorization boundary:

```text
unsafe browser-shaped request
  -> origin/fetch-metadata decision
  -> local or remote authentication policy
  -> route handler
  -> side effect
```

A request carrying a foreign `Origin` and `Sec-Fetch-Site: cross-site` is denied before the local-client shortcut. Safe methods retain their existing behavior, and a local non-browser client without browser-origin headers retains the intended dev-mode path.

## Verification

The negative regression is `test_cross_site_browser_upload_is_rejected_even_from_loopback`. It sends `POST /upload` with:

- `Host: 127.0.0.1:8899`
- `Origin: https://evil.example`
- `Sec-Fetch-Site: cross-site`
- a concrete multipart file payload

The test asserts `403`, the bounded error `Cross-site request denied`, and an empty upload directory. The last assertion is the sink-shaped proof: denial alone is insufficient if a file was partially created.

The positive control is `test_loopback_upload_without_browser_origin_still_allowed_when_key_configured`. It sends the same class of upload from a local non-browser path, asserts `200`, and confirms that exactly one file exists.

The PR records this targeted command:

```sh
python3 -m pytest -q \
  agent/tests/test_upload_api.py \
  agent/tests/test_security_auth_api.py \
  agent/tests/test_settings_api.py
```

The container result was `70 passed, 5 warnings in 0.54s`. The manual after-fix proof matched the tests: the cross-site upload returned `403` with no created file, while the local non-browser upload returned `200`.

## What was learned

Network locality is a transport fact, not actor identity. Local AI control planes often expose high-impact operations—uploads, tool calls, settings changes, runner controls, memory mutation, and process shutdown—behind a loopback convenience assumption. A browser can bridge a remote origin into that local transport.

The durable review rule is to classify browser-origin admission separately from Host/DNS-rebinding defenses and from API authentication. Then place the denial before any shortcut that trusts locality and before any side-effect sink.

The proof should be two-sided: a foreign-origin unsafe method is rejected with no mutation, while the intended local client still works. Without the positive control, a security patch can quietly replace a trust-boundary bug with a compatibility regression.

## Repeat next time

- Enumerate unsafe methods on loopback, MCP, notebook, IDE, runner, and local agent APIs before broad source review.
- Trace each method to upload, file, settings, memory, tool-call, job-control, subprocess, or shutdown sinks.
- Ask whether peer IP, local-owner context, or dev mode bypasses the browser-origin decision.
- Keep browser CSRF, DNS rebinding, Host validation, and bearer/session authentication as separate review questions.
- Assert both denial and absence of side effects; then preserve a same-origin or local non-browser compatibility path.

## Vault redirect

The canonical research record remains in the private OSS Vulnerability Research Vault. The finding note preserves the broader loopback-control-plane evidence, while `Takeaway - Loopback browser unsafe methods need pre-sink origin gates` owns the reusable proof contract.

No new vault checklist was needed for this publication. The existing source-code quick pass already requires `foreign-origin unsafe request -> pre-sink denial -> no mutation -> legitimate local control`. This post is the public-safe synthesis of that rule and the merged public regression, not a parallel research record.
