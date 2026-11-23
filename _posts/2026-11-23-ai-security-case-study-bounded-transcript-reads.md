---
layout: post
title: "A transcript URL can be safe to fetch and too large to read"
date: 2026-11-23 05:00:00 +0800
permalink: /2026/11/23/ai-security-case-study-bounded-transcript-reads/
takeaway: "A missing transcript tells you what the parser received. To verify a download limit, also check that the reader stopped."
categories: [daily-security, case-study, ai-security]
tags: [case-study, resource-limits, streaming, transcripts, availability]
---

## Signal

In `summarize`, the RSS reader checked where a transcript URL led before connecting. That protected the destination, not the reader’s memory. The most useful evidence in the eventual fix came from the other end of the connection: the server saw the client stop reading.

## Merged PRs

None in this window.

## What shipped or moved

On 23 November, I published this case study of a fix that merged in June. I also corrected stale entries in the security PR tracker. One proposal was still listed as open even though its author had redirected review to a different patch. I marked the original as superseded. Its replacement was still open, so neither counted as a shipped fix.

## Observed pattern

A parser returning no text and a downloader stopping work are two different outcomes. Only the second tells us the size limit protected the reader while the response was arriving.

### Threat model

A user asks for a summary. The publisher supplies the transcript or caption reference; the summarizer spends memory and CPU reading it. The concern was the availability of that job, not access to private data.

### Finding and PR

[steipete/summarize #302](https://github.com/steipete/summarize/pull/302) merged on 15 June 2026 ([`e691487`](https://github.com/steipete/summarize/commit/e69148716fd35b755259b4ea2ef0488d0ea2c431)). The RSS reader (`podcast/rss-transcript.ts`) and embedded caption reader (`generic-embedded.ts`) switched to a shared helper, `response-size-limit.ts`. The patch also added three regression files and a changelog entry.

### Exploit path

Both readers could turn a remote response into a string before the parser saw it. The PR documented a transcript larger than the eventual limit being read in full. It did not demonstrate a process crash.

### Mitigation

Both readers now enforce a 5 MiB limit. An oversized `Content-Length` lets the helper cancel without reading the body. When the length is unknown, the helper counts bytes as they arrive and cancels before decoding the chunk that crosses the limit. A legitimate transcript above the cap is skipped too.

### Verification

The PR reports 21 tests passing across four files in Docker. The RSS and caption tests checked that an oversized declaration left the body unread and that small responses still returned the expected text. The shared-reader test checked cancellation and lock release when a stream crossed the limit. In a separate local HTTP check, the serving side observed the connection close. The existing RSS destination tests still passed; they did not test the byte limit.

## External reference

The [stream-cancellation regression at the merge commit](https://github.com/steipete/summarize/blob/e69148716fd35b755259b4ea2ef0488d0ea2c431/tests/security.transcript-response-size-limit.test.ts) is worth reading alongside the PR’s HTTP check. One observes the reader’s cleanup; the other observes what happened to the connection.

## What was learned

If the only assertion is “no transcript returned,” an implementation that downloads everything and then discards it could pass. Watching cancellation makes the test distinguish that implementation from one that actually stops the download.

## Takeaways

- Give the URL policy and the response-size limit separate tests. A permitted destination can serve a response of any size.
- Keep a small, valid caption in the regression suite. Rejecting every response would protect the budget while breaking the feature.

## Repeat next time

For each remote reader, check three cases: a declared oversize body that stays unread, an unknown-length stream that gets cancelled at the cap, and a small valid response whose text reaches the parser unchanged.

## Vault redirect

The existing resource-limit takeaway already calls for cancellation before the full response is held in memory. The corrected PR outcomes belong in the tracker; neither the case study nor the tracker correction needed a new finding.
