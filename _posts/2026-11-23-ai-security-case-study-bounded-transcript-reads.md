---
layout: post
title: "A transcript URL can be safe to fetch and too large to read"
date: 2026-11-23 05:00:00 +0800
permalink: /2026/11/23/ai-security-case-study-bounded-transcript-reads/
takeaway: "Check where a transcript comes from before connecting. Count bytes while reading it, and verify that crossing the limit stops the stream."
categories: [case-study, ai-security]
tags: [case-study, resource-limits, streaming, transcripts, availability]
---

## Signal

In `summarize`, an RSS transcript URL could pass the network check and still return more text than the process should hold. The parser only saw the transcript after the fetcher had read it in full.

## Threat model

A user or scheduled job asks for a summary. The feed or page publisher supplies the transcript or caption reference; the summarizer supplies the memory and CPU to process the response. The concern is availability during that job. It doesn't require access to a private network or imply data disclosure.

## Finding and PR

[steipete/summarize #302](https://github.com/steipete/summarize/pull/302) merged on June 15, 2026 ([`e691487`](https://github.com/steipete/summarize/commit/e69148716fd35b755259b4ea2ef0488d0ea2c431)). The RSS reader (`podcast/rss-transcript.ts`) and the caption reader (`generic-embedded.ts`) switched to a shared helper, `response-size-limit.ts`. The patch also added three regression files and a changelog entry.

## Exploit path

Feed metadata and embedded captions led to the same operation: a reader turned a remote response into a string without a byte limit. On the RSS path, the destination check answered *may we connect?* Nothing yet answered *how much may we read?* The PR records an 8 MiB transcript accepted before the fix. That demonstrates the missing bound, not a process crash.

## Mitigation

Both readers now use a 5 MiB transcript limit. If `Content-Length` already exceeds it, the helper cancels the body without reading it. For a streaming body, it counts actual bytes and cancels before decoding the chunk that crosses the limit. An unusually large legitimate transcript is skipped too; the existing RSS destination policy is unchanged.

## Verification

The PR reports 21 passing tests across four files in Docker. The checks separate early rejection, stream cleanup, and compatibility:

- **Before reading:** `security.rss-transcript-size-limit.test.ts` and `security.embedded-caption-size-limit.test.ts` both check that an oversized declaration yields no transcript and the body-read flag stays false. Small fixtures still return the expected transcript and caption text.
- **During reading:** `security.transcript-response-size-limit.test.ts` checks that the over-limit reader is cancelled and its lock released. In a separate local HTTP check recorded in the PR, the serving side observed the connection close.
- **Existing protection:** the fourth file, `security.rss-transcript-ssrf.test.ts`, covered the RSS destination checks. Those tests passing would not, on their own, say anything about response size.

## What was learned

The server observing the close is the useful detail. “No transcript returned” tells us what the parser received. It doesn't tell us whether the download stopped.

## Repeat next time

For a remote reader, keep three fixtures: an oversized declaration whose body must not be read, an unknown-length stream whose cancellation is observable, and a small valid response whose parsed text must not change.

## Vault redirect

This case belongs with the existing review rule on resource limits: verify the limit where bytes become retained text. Keep destination checks as a separate item with separate evidence.
