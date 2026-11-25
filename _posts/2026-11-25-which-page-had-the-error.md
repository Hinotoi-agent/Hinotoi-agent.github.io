---
layout: post
title: "Which page had the error?"
date: 2026-11-25 12:00:00 +0800
permalink: /2026/11/25/which-page-had-the-error/
takeaway: "Look for secrets across the whole log. Look for the page ID and error type together on the record that describes the failure."
categories: [daily-security]
tags: [logging, redaction, regression-tests]
---

## Signal

Suppose one log entry says page A failed. Another says page B raised `RuntimeError`. Searching the combined text for both `page A` and `RuntimeError` succeeds. It still doesn’t tell the operator what happened to page A.

## Merged PRs

None in this window.

## What shipped or moved

On 25 November I added [the previous day’s crawler example](/2026/11/24/what-a-redacted-error-still-needs-to-say/) to my redaction review notes. It pairs two checks: the log must omit the sensitive value and still identify the failure. The change was to the review notes, not to the crawler.

## Observed pattern

Those checks need different scopes. A secret in *any* captured message is a failure, even if the error entry itself is clean. But the page ID and exception type are useful together: a type logged for a different page can’t explain this one.

## External reference

The [regression in RAPTOR #336](https://github.com/gadievron/raptor/blob/e29283b5e094277451b9e4d5f332d0b46103dd99/packages/web/tests/test_secret_redaction.py#L107-L130) drives one crawler failure, joins the captured messages, and checks the resulting text. The two-page example above is a reason to tighten the assertion when adapting that test for multiple failures, not a report that RAPTOR mislabels errors.

## What was learned

In a small synthetic check, searching the combined messages accepted the split example above. Requiring the expected ID and type on the same error entry rejected it. Conversely, checking only that entry missed a synthetic secret in a separate diagnostic message.

## Takeaways

Search every captured record for the synthetic secret. Then select the error record for the expected page and check its exception type there.

## Repeat next time

Give page B the exception type expected for page A, and leave the type off A’s entry. The test should fail. Restore the type to A, then put the fake secret in a different message: the test should fail for that reason too.

## Vault redirect

I kept the two-page example beside the original crawler regression in the redaction takeaway, so the next logging review has both checks in one place.
