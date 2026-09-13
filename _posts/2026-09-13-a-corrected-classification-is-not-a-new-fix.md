---
layout: post
title: "2026-09-13 — A corrected classification is not a new fix"
date: 2026-09-13 23:59:00 +0800
permalink: /2026/09/13/a-corrected-classification-is-not-a-new-fix/
takeaway: "Keep the date a research record changed separate from the date code shipped. A classification correction improves the next review without becoming another finding."
categories: [daily, ai-security]
tags: [research-method, evidence-quality, oss-hardening, vault-backed-learning]
---

## Signal

The useful movement in this window was a correction to the research record, not another security fix. That distinction matters when daily notes become inputs to later summaries: a better explanation must not inflate the count of findings or shipments.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-13T00:00:00+08:00, 2026-09-14T00:00:00+08:00)`. A fresh GitHub merge search confirmed the empty window.

## What shipped or moved

On September 13, while finalizing the previous day's post, the existing file-ACL advisory case in the research vault was corrected against its public source. A misleading path-traversal classification was removed. The case now distinguishes filesystem containment from permission to mutate a protected object.

[The September 12 note](/2026/09/12/contained-paths-still-need-authorization/) covers that technical distinction. Today's record closes the bookkeeping: the correction belongs to September 13; it is not a new vulnerability, reproduction, or runtime shipment.

## Observed pattern

Research has at least two relevant dates: when the underlying event occurred and when the maintained record became more accurate. Collapsing them can make one advisory look like repeated new work—or make a later correction disappear from the audit trail.

This applies equally to agent and MCP security notes. A revised boundary label should change the next review question, not silently become evidence that another product is affected.

## External reference

[GHSA-wvhv-qcqf-f3cx](https://github.com/advisories/GHSA-wvhv-qcqf-f3cx) explicitly distinguishes its authorization failure from path traversal. It remains the public evidence anchor for the classification correction. No exploit was run and no patched release was independently validated for this post.

## What was learned

A useful correction needs an owner and a bounded claim. Here the owner is the existing advisory case, and the claim is that its classification now matches the source. The technical lesson already has a checklist destination; there is no reason to create another finding or duplicate checklist.

## Takeaways

- **Separate event time from record time.** Date the correction without relabeling the underlying advisory as a new shipment.
- Update the canonical case before reusing its category in another review or summary.
- Stop expanding the narrative when the evidence has not changed.

## Repeat next time

Before turning a vault delta into a daily shipment claim, identify the changed artifact, the source supporting the change, and whether it represents code, evidence, or classification. For a correction, amend the existing owner and preserve the distinction in the public summary.

## Vault redirect

The corrected advisory case already records the September 13 clarification, its source, and the authorization-review takeaway. The existing public-observation takeaway also requires event time to remain separate from record time. This post applies those rules; no new private finding, checklist, or duplicate lesson was created.
