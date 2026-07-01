---
layout: post
title: "2026-07-01 — Case study: loopback CSRF on a local upload API"
takeaway: "A local API is still browser-reachable; unsafe loopback requests need origin-aware denial before the handler can spend local authority."
categories: [case-study, ai-security]
tags: [case-study, loopback, csrf, browser-origin, local-api, upload, control-plane, oss-hardening]
---

This case study uses [HKUDS/Vibe-Trading #293](https://github.com/HKUDS/Vibe-Trading/pull/293), a small merged hardening PR with a useful AI-security lesson: local developer APIs are not protected by loopback alone when a browser can be used as the request carrier.

The concrete chain is simple:

```text
remote page
    -> victim browser
        -> POST http://127.0.0.1:<local-api>/upload
            -> loopback dev-mode trust
                -> upload handler writes a file
```

CORS can hide the response from the remote page. It does not prove the upload, shutdown, runner, settings, or other side effect was blocked.

## Signal

Vibe-Trading keeps local API behavior convenient for CLI and local UI workflows. That is a common trade-off in AI tools, notebooks, local web UIs, agent runners, and MCP-style control planes: the service listens locally and treats loopback traffic as operator-adjacent.

The security signal was the ordering of checks. The server already had a cross-site browser request guard, and it already had loopback trust. The risky path appeared when loopback trust could be honored before the server rejected unsafe browser-originated requests.

That makes the bug class broader than one upload endpoint. Any local API that accepts unsafe browser-sendable methods can accidentally let a remote page spend local authority.

## Threat model

Attacker capability:

- host a web page under an attacker-controlled origin;
- convince a developer/operator to visit it in a browser on the same machine or network context as the local API;
- trigger a browser request to `127.0.0.1` / `localhost` with browser headers such as `Origin` and `Sec-Fetch-Site`.

Defender assumption that failed:

- "the request is from loopback, so it is local and trusted."

The missing distinction is actor versus carrier. The TCP peer can be loopback while the initiating actor is an untrusted remote web page using the victim browser as the carrier.

For AI systems, this matters because local APIs often expose actions with host-side effects: upload files, change settings, start jobs, invoke tools, write memory, stop services, attach provider credentials, or mutate workflow state.

## Finding and PR

- Finding class: browser-mediated loopback CSRF against unsafe local API methods.
- Public PR: [HKUDS/Vibe-Trading #293 — `fix: reject cross-site unsafe local API requests`](https://github.com/HKUDS/Vibe-Trading/pull/293).
- Merged: `2026-06-23T10:49:42Z`.
- Merge commit: `5414a59e221730f2b758f5dd02378a119e2fa575`.
- Files changed:
  - `agent/api_server.py`
  - `agent/tests/test_upload_api.py`

The PR summary states the boundary directly: reject unsafe cross-site browser requests before applying loopback dev-mode auth trust.

## Exploit path

The relevant pre-fix path was:

```text
attacker-controlled page
    -> browser sends cross-site POST /upload to local API
        -> request appears to come from loopback
            -> auth validation treats loopback as trusted
                -> upload route processes multipart file
                    -> filesystem side effect
```

The important point is not whether the attacker can read the response. A blind side effect is enough. If the handler writes a file, starts a job, changes a setting, or shuts down a process, CORS response blocking has not protected the local service.

The regression added in the PR models the attacker shape with browser-origin headers:

```python
headers={
    "Host": "127.0.0.1:8899",
    "Origin": "https://evil.example",
    "Sec-Fetch-Site": "cross-site",
}
```

The payload is sent to `POST /upload`. That is a good proof shape because it reaches a concrete sink: the upload directory. The denial can be checked by status code and by absence of a created file.

## Mitigation

The fix adds a safe-method split and moves the browser-origin denial before loopback trust is honored for unsafe methods:

```python
_SAFE_BROWSER_METHODS = {"GET", "HEAD", "OPTIONS"}

if request.method.upper() not in _SAFE_BROWSER_METHODS:
    _reject_cross_site_browser_request(request)

# Loopback clients are always trusted...
if _is_local_client(request):
    return
```

The mitigation has two useful properties:

1. **Deny before authority is spent.** Unsafe browser-originated cross-site requests hit the cross-site guard before local dev-mode trust can bypass token validation.
2. **Preserve intentional local workflows.** The patch does not delete loopback support. It keeps non-browser local upload behavior working and covers that compatibility path with a positive regression.

This is the right shape for local AI tooling. Secure defaults should block browser-mediated unsafe requests, but the fix should still name and test the intended local CLI or same-origin workflow instead of leaving compatibility pressure to weaken the guard later.

## Verification

The PR includes two focused regression tests.

Negative test:

- `test_cross_site_browser_upload_is_rejected_even_from_loopback`
- sends `POST /upload` with `Origin: https://evil.example` and `Sec-Fetch-Site: cross-site`;
- expects `403`;
- expects response detail `Cross-site request denied`;
- asserts the upload directory remains empty.

Positive control:

- `test_loopback_upload_without_browser_origin_still_allowed_when_key_configured`
- sends `POST /upload` from loopback without browser-origin headers;
- expects `200`;
- asserts one uploaded file exists.

The PR test plan records both targeted host tests and a container run:

```text
python3 -m pytest -q agent/tests/test_upload_api.py agent/tests/test_security_auth_api.py agent/tests/test_settings_api.py
```

Container proof from the PR:

```text
70 passed, 5 warnings in 0.54s
cross-site upload returned 403 with no created files
local non-browser upload returned 200
```

That verification is stronger than checking the response alone. It proves the denial happened before the file-write sink, and it proves the intended local path still works.

## What was learned

Loopback is a location fact, not a complete authorization decision. For local AI and automation systems, the review needs a second question: who caused the loopback request?

A useful review trace is:

```text
browser page
    -> Origin / Fetch Metadata classification
        -> loopback trust branch
            -> auth decision
                -> handler sink
                    -> file/job/tool/settings side effect
```

The invariant belongs before the sink. If the sink is upload, the test should prove no file was created. If the sink is runner start, the test should prove no job was queued. If the sink is settings, the test should prove no mutation occurred. A blocked response body is not enough.

The follow-up lesson is compatibility discipline. After adding a browser-origin guard, define the allowed lane as explicitly as the denied lane: same-origin UI, authenticated remote UI, local non-browser CLI, or another intentional path. Otherwise the next bug may be a hardening patch that is technically safe but operationally too broad.

## Repeat next time

- Enumerate unsafe local API methods separately from Host-header or DNS-rebinding checks.
- Treat `Origin` and Fetch Metadata as authorization inputs before loopback shortcuts on `POST`, `PUT`, `PATCH`, and `DELETE`.
- For each candidate route, name the sink: file write, job start, shutdown, settings mutation, credential attachment, tool call, or approval change.
- Write one negative regression that asserts both denial and absence of the sink-side effect.
- Write one positive control for the legitimate local or same-origin path so compatibility is preserved deliberately.
- When reviewing AI agents, MCP bridges, notebooks, IDEs, and local web UIs, assume a browser can reach the local control plane until the server proves otherwise.

## Vault redirect

- Finding anchor: `03 - Findings/HKUDS Vibe-Trading - Loopback CSRF shutdown.md` records the same browser-to-loopback trust boundary on an adjacent unsafe route family.
- Takeaway anchor: `06 - Lessons/Takeaway - Loopback browser unsafe methods need pre-sink origin gates.md` captures the reusable proof contract.
- Checklist anchor: `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md` now separates loopback/browser unsafe-method review from Host and DNS-rebinding review.
- Follow-up compatibility rule: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, especially the 2026-06-23 and 2026-06-25 updates.
- Public role: this post is the public-safe case study. The durable review rule stays in the vault checklist and takeaway notes.
