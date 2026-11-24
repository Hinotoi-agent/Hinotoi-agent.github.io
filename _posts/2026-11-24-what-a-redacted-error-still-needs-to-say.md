---
layout: post
title: "What a redacted error still needs to say"
date: 2026-11-24 12:00:00 +0800
permalink: /2026/11/24/what-a-redacted-error-still-needs-to-say/
takeaway: "A safe error log should tell the operator which page failed and why, without repeating the request URL. Test both halves."
categories: [daily-security]
tags: [logging, redaction, regression-tests]
---

## Signal

A crawler can log a redacted URL and still print the original one on the same line. The second copy comes from the client library: its exception message quotes the request that failed.

## Merged PRs

None in this window.

## What shipped or moved

On 24 November I finished the [previous day’s transcript note](/2026/11/23/ai-security-case-study-bounded-transcript-reads/). There was no new research entry in the vault for the 24th. The redaction example below comes from [RAPTOR #336](https://github.com/gadievron/raptor/pull/336), which merged in May.

## Observed pattern

The crawler needs to know the exact URL to make a request. Someone reading a failure log usually needs less: which page in the crawl failed, and what kind of error occurred. A page ID lets the operator match the error to the crawl without putting the query string in the log.

## External reference

In [RAPTOR’s exception-log regression](https://github.com/gadievron/raptor/blob/e29283b5e094277451b9e4d5f332d0b46103dd99/packages/web/tests/test_secret_redaction.py#L107-L130), a fake client raises an error that quotes the URL. The test inspects the collected log messages: the synthetic secret and raw error text must be absent; the page ID and `RuntimeError` must still be present.

## What was learned

Checking only that the secret disappeared would let a broken logger pass by printing nothing. Checking only that the error was logged would miss the disclosure. The two assertions together describe a log someone can actually use.

## Takeaways

Review the whole emitted message, not just the URL formatter. Exception text is a separate place the same data can appear.

## Repeat next time

Make a failing request with a synthetic marker and have the fake client repeat it in the exception. Read the final log: can I identify the failed page and error class without finding the marker?

## Vault redirect

I added the paired assertions to the existing redaction takeaway, alongside the rule for debug output. They belong with the next logging review, not in a new vulnerability report.
