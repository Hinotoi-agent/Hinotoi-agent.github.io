---
layout: post
title: "2026-05-30 — Media download limits are admission boundaries"
takeaway: "A configured byte limit is only a real resource boundary when unknown-size media is denied or capped before the host materializes it."
categories: [daily, ai-security]
tags: [matrix, media-downloads, resource-exhaustion, dos, streaming-limits, concurrency-caps, oss-hardening]
---

The 2026-05-30 Singapore window had one merged security PR in `HKUDS/nanobot`. The useful signal was a resource boundary: `max_media_bytes` was already present, but Matrix media with missing size metadata could still reach the download path before the limit became effective.

## Signal

Resource limits are admission controls, not after-the-fact labels.

For inbound chat, Matrix, Discord, Slack, bot, and agent media paths, the dangerous operation often starts before parsing or summarization. A remote attachment has already become host resource pressure when the process opens the network stream, buffers bytes, decrypts the payload, writes it to disk, or lets many downloads run at once. The review should therefore ask whether the configured limit controls the pre-sink path, not only whether the final in-memory object is rejected later.

## Merged PRs

- [HKUDS/nanobot #4106](https://github.com/HKUDS/nanobot/pull/4106) — [security] fix(matrix): bound inbound media downloads

## What shipped or moved

`nanobot` hardened Matrix inbound media handling around the configured media-size boundary.

The merged fix rejects Matrix media when the event does not provide trusted `content.info.size`, streams Matrix media through `aiohttp` with a hard byte cap, aborts once the configured `max_media_bytes` limit is exceeded, and adds a Matrix media download semaphore so multiple media events cannot fan out into unbounded simultaneous downloads.

The patch moved the effective boundary earlier in the chain:

```text
Matrix sender allowed by channel policy
    -> media event with mxc:// content
        -> declared-size admission gate
            -> capped streaming download
                -> small concurrent-download semaphore
                    -> optional processing/storage
```

Regression coverage was added for bounded downloads, declared-size rejection, unknown-size rejection, encrypted media handling, and download failure behavior.

## Observed pattern

Media metadata is not proof of safety; it is an input to an admission decision.

A size field, filename, MIME type, provider media object, or encrypted-media wrapper can be missing, stale, forged, or simply unavailable. If the host treats unknown metadata as safe, the first real boundary becomes the host's memory, bandwidth, CPU, or disk budget. That is too late.

The reusable review question is:

```text
Can untrusted media consume host resources before the configured cap is enforced?
```

If the answer includes full-body buffering, decrypt-before-size-check, concurrent download fan-out, near-limit file accumulation, parser expansion, archive preview, or background worker queues, the cap needs to move to the earliest concrete resource sink and remain present as defense in depth later.

## External reference

- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html) — public anchor for denial-of-service cases where the system lets an attacker consume memory, bandwidth, CPU, or storage without a strong bound.
- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html) — useful framing for concurrent download fan-out and missing semaphore/rate boundaries.
- [OWASP API4:2023 — Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) — practical anchor for treating file uploads/downloads, request sizes, concurrency, and expensive processing as explicit API security limits.
- [Matrix Client-Server API media repository](https://spec.matrix.org/latest/client-server-api/#media-repository) — protocol context for `mxc://` media flows; the security lesson is to bind application-side bot downloads even when the media object comes through a standard channel.

## What was learned

The stronger frame is “bounded materialization,” not just “file too large.” A file-size policy protects the process only if it controls all materialization steps: metadata admission, network read, response buffering, decryption, parser handoff, disk write, and concurrency. A final `len(data) > limit` check is still useful, but it is defense in depth after the resource has already been spent.

This also keeps the public claim narrow. The merged issue is a Medium availability hardening fix for Matrix-enabled deployments where a sender can message a room or chat processed by the bot. It is not unauthenticated reachability, code execution, or credential disclosure. The important review upgrade is that media channels should prove resource bounds before work begins, especially when AI/bot systems turn inbound attachments into downstream parsing, summarization, tool context, or durable files.

## Takeaways

- Treat unknown-size media as unsafe by default unless a streaming cap is already active before bytes are materialized.
- Enforce media budgets at every expensive transition: declared metadata, network read, decrypt/transform step, parser handoff, disk write, and concurrent worker queue.
- Concurrency limits are part of the security boundary for attachment handling; one safe single download can still become unsafe under fan-out.
- Keep severity bounded to the real admission path and deployment preconditions, especially when the impact is availability rather than data access or execution.

## Repeat next time

- For every bot, Matrix, Slack, Discord, MCP, upload, or agent media path, map `remote media reference -> download primitive -> buffer/decrypt/parse -> storage/tool sink` before judging the fix.
- Test missing, invalid, oversized, encrypted, and near-limit media separately; each can cross a different resource boundary.
- Assert both denial and absence of expensive side effects: no unbounded body materialization, no decrypt-before-cap path, no uncontrolled concurrent downloads, and no unbounded file accumulation.
- Prefer bounded streaming helpers and small semaphores over post-download checks as the primary control; keep post-download checks as backup.

## Vault redirect

- Finding anchor: `03 - Findings/Finding - HKUDS nanobot Matrix media oversized download DoS.md` records the Matrix media resource-exhaustion chain, validation, merged PR, and bounded-impact framing.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md` was reverse-routed with the bounded-materialization rule from `HKUDS/nanobot#4106`.
- Checklist anchors: `05 - Workflows/Checklist - URL Fetch and SSRF Review.md` remains relevant for media fetch sinks, and the source-code discovery loop remains the place to map resource sinks before relying on configured limits.
- PR anchor: `HKUDS/nanobot#4106`, merged during the 2026-05-30 Singapore window.
