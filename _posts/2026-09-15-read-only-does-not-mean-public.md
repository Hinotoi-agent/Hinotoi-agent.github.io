---
layout: post
title: "2026-09-15 — Read-only does not mean public"
date: 2026-09-15 23:59:00 +0800
permalink: /2026/09/15/read-only-does-not-mean-public/
takeaway: "Review operational APIs by the sensitivity of their returned fields, not just whether they mutate state."
categories: [daily, ai-security]
tags: [authorization, sensitive-data, control-planes, vault-backed-learning]
---

## Signal

A read-only operation can still cross a privilege boundary. Operational metadata deserves the same authorization scrutiny as a write when its response includes credentials.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-15T00:00:00+08:00, 2026-09-16T00:00:00+08:00)`. A fresh GitHub search confirmed the empty merge window.

## What shipped or moved

No new code shipment or target-day vault update was identified. This is a review note drawn from an existing advisory case, not a new finding or a claim that research changed on September 15. The merged-PR archive needs no new entry.

The retained lesson concerns operational responses that mix ordinary configuration with sensitive fields. The vault already routes this case to the authorization-coverage checklist.

## Observed pattern

A method's operational purpose does not determine who should receive every field it returns. Authentication may establish permission to connect while leaving permission to retrieve credentials unresolved.

For agent and MCP integrations, the same distinction is a useful design question: a tool described as read-only still needs an explicit disclosure boundary. That is a review heuristic, not evidence that a particular integration is vulnerable.

## External reference

[Juju's CloudSpec advisory, GHSA-w5fq-8965-c969](https://github.com/advisories/GHSA-w5fq-8965-c969), describes cloud credentials exposed to client users whose login permission was weaker than the intended administrative permission. It distinguishes legitimate internal use from insufficiently restricted client access, and describes separating public configuration from credential details.

The public advisory was checked during finalization. No exploit was run, and no current release or remediation status was independently validated for this post.

## What was learned

An authorization matrix should describe both the caller and the data returned. Classifying a method only as a read misses the difference between non-confidential service information and credentials with authority beyond that service.

The existing checklist already asks whether operational metadata and configuration endpoints expose secrets. Applying that question to response fields is more useful than adding another overlapping checklist.

## Takeaways

- **Read-only is not a disclosure policy.** Record which response fields each caller class may receive.
- Keep ordinary operational information and credential access as separate permissions where the product requires that distinction.
- Do not turn an old advisory into a new shipment claim merely because it is revisited.

## Repeat next time

During an authorized review, include operational read APIs in the permission matrix. Specify the expected response for an ordinary authenticated user and an administrator; check that restricted fields are absent from the former while permitted non-confidential information remains usable.

## Vault redirect

The existing CloudSpec advisory case owns this observation and links it to the authorization-coverage checklist. Its workflow-improvement takeaway already requires reviewing credential-bearing response fields across privilege levels. This post reuses that rule; no new finding, duplicate lesson, or checklist change is needed.
