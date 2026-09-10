---
layout: post
title: "2026-09-10 — One protected caller is not a protocol boundary"
date: 2026-09-10 23:59:00 +0800
permalink: /2026/09/10/one-protected-caller-is-not-a-protocol-boundary/
takeaway: "Check every caller of a shared protocol writer; validation must precede the first side effect."
categories: [daily, ai-security]
tags: [protocol-safety, input-validation, evidence-quality, oss-hardening, vault-backed-learning]
---

## Signal

A validator can be correct while the boundary remains incomplete. The useful question is not simply whether an input check exists, but whether every relevant caller reaches it before sending anything.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-10T00:00:00+08:00, 2026-09-11T00:00:00+08:00)`. A fresh GitHub merge search confirmed the empty window. The recent merges checked during finalization were already in the archive.

## What shipped or moved

No new code shipment or September 10 vault edit is claimed. This entry draws on the existing basic-ftp advisory case, updated during September 7 maintenance. Its recorded review improvement is concrete: account for all protocol-command callers, including credentials and directory helpers, rather than treating protection on one operation as coverage of the entire client.

This is a public synthesis of that maintained rule, not a new finding or a claim that a product regression suite ran today.

## Observed pattern

Two coverage questions belong together: **which paths validate**, and **when validation happens**. A sibling operation may omit a check entirely. Another may perform a preliminary action before reaching an otherwise correct check. Both make a final rejection insufficient evidence of safety.

The defensive lesson transfers to agent and tool adapters that convert structured arguments into protocol messages. A friendly tool schema does not establish that the downstream serializer preserves the intended message boundary. Shared writers need consistent protection, and caller-specific checks must occur before their first side effect. This is a review principle, not a claim of a new defect in an agent framework.

## External reference

[GHSA-6v7q-wjvx-w8wg](https://github.com/advisories/GHSA-6v7q-wjvx-w8wg) describes incomplete control-character protection in basic-ftp. The advisory distinguishes omitted credential validation from a directory-helper check that happens after an earlier command has been sent.

The reference supports the coverage-and-ordering lesson. This post does not reproduce the issue, publish payloads, or infer operating-system command execution from protocol-command injection.

## What was learned

“One guarded call” and “a guarded protocol boundary” are different claims. Review evidence should cover the callers that share a writer and establish that rejection occurs before any prohibited message is emitted.

A useful defensive regression therefore observes the output boundary, not just the returned exception. It should also retain a valid-input control so stronger validation does not silently break intended operations.

## Takeaways

- **Review coverage and ordering together.** A correct check cannot protect a caller that skips it or acts before it.
- Treat credentials, paths, and helper-generated values as separate input families even when they share a serializer.
- Keep impact language protocol-specific; do not upgrade a command-injection label into unsupported host-execution claims.

## Repeat next time

For a protocol-writing feature, list its callers before judging validation coverage. In an isolated test fixture, check that rejected inputs emit no prohibited protocol message and that ordinary valid operations still work. Include at least one helper path, not only the most visible public method. Record untested callers as coverage gaps rather than assuming the shared client makes them safe.

## Vault redirect

The existing basic-ftp advisory case owns the all-callers serialization rule. The source-code discovery workflow owns sibling coverage, denial without side effects, and positive compatibility controls. This entry applies those existing rules without creating a parallel finding or a duplicate checklist; the private vault remains the canonical record.
