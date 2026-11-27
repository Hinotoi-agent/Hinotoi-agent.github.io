---
layout: post
title: "Which log received the event?"
date: 2026-11-27 12:00:00 +0800
permalink: /2026/11/27/which-log-received-the-event/
takeaway: "A clean console can mean the debug record never reached it. Check each log destination against the events it should receive."
categories: [daily-security]
tags: [logging, redaction, regression-tests]
---

## Signal

`WARNING job-17 timed out` was the entire console output in both runs. To tell which run logged a synthetic secret, I had to look at the diagnostic stream.

## Merged PRs

None in this window.

## What shipped or moved

On 27 November I filed [the previous day’s formatter check](/2026/11/26/read-past-the-first-log-line/) in my review notes. No product change came with it. While finalizing this entry, I tested a question that example left open: what if the console and the diagnostic log receive different events?

## Observed pattern

I set up two in-memory Python log handlers. The console accepted `INFO` and above; the diagnostic stream also accepted `DEBUG`. Both received the timeout warning. Only the diagnostic stream received the retry detail.

## External reference

The [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations) shows why this setup is useful: an operator can keep detailed records in a file without putting every debug message on the console.

## What was learned

In the first run the retry detail contained `TEST-MARKER`. In the second it contained `timeout` instead. The diagnostic stream showed the difference; the console was identical. A console-only test would have passed both runs. Its level filter worked, but it told me nothing about redaction.

## Takeaways

Give each destination its own expectation. For this fixture the console should show the warning, and the diagnostic stream should identify the retry without revealing the marker. Turning off debug logging altogether would hide the marker but lose the retry detail too.

## Repeat next time

Send a marked debug event first and confirm the test catches it in the diagnostic output. Then replace the marker with a safe reason and require the retry detail to remain. Keep the two captures separate so a line in one cannot satisfy an assertion about the other.

## Vault redirect

I added the two-destination check to the existing redaction takeaway, alongside the formatter example. It’s a test for logging configurations, not a finding against a project.
