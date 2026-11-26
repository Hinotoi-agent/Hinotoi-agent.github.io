---
layout: post
title: "Read past the first log line"
date: 2026-11-26 12:00:00 +0800
permalink: /2026/11/26/read-past-the-first-log-line/
takeaway: "Test redaction against what the log handler writes. A clean message can still have a traceback attached."
categories: [daily-security]
tags: [logging, redaction, regression-tests]
---

## Signal

`page-17 failed: RuntimeError` was the message in both runs of a small Python logging test. Only one run printed the synthetic secret. The difference was in the traceback *below* that line.

## Merged PRs

None in this window.

## What shipped or moved

On 26 November I recorded [the previous day’s two-page logging example](/2026/11/25/which-page-had-the-error/) in my review notes. That was a write-up, not a crawler change. While finalizing this entry I checked a question it left open: does reading every message show everything the handler writes?

## Observed pattern

A Python log record can carry the exception separately from the message. Even if the caller logs only a page ID and an error class, the formatter can append the original exception text.

## External reference

Python’s [`logging.Formatter.format` documentation](https://docs.python.org/3/library/logging.html#logging.Formatter.format) identifies where this happens: the formatter builds the message first, then appends exception information if the record carries it.

## What was learned

I raised a `RuntimeError` containing a harmless marker and captured a `StreamHandler`’s output. With `exc_info=False`, the output identified the page and error class without the marker. With `exc_info=True`, `getMessage()` returned the same clean text, but the traceback included the marker. This checks standard-library behavior, not a defect in the crawler.

## Takeaways

Use the error record to check *which page failed and how*. Use the formatted output to check *what a reader could see*. A search across every `getMessage()` can still miss the exception text.

## Repeat next time

Start with a plain formatter and attach the marked exception: the redaction test should fail. Then capture the handler and formatter the application actually uses. The test should pass only if the marker is absent and the page ID and error class stay together.

## Vault redirect

I added the formatter check to the existing redaction takeaway, beside the two-page example.
