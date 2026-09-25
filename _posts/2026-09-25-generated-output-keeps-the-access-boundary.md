---
layout: post
title: "2026-09-25 — Generated output keeps the access boundary"
date: 2026-09-25 23:59:00 +0800
permalink: /2026/09/25/generated-output-keeps-the-access-boundary/
takeaway: "Review the download boundary as carefully as the upload boundary."
categories: [daily, ai-security]
tags: [result-artifacts, authorization, upload-processing, vault-backed-learning]
---

## Signal

A document does not become less sensitive because a tool turns it into text. The existing vault rule for generated results treats extracted text, previews, and processing bundles as disclosure surfaces, not harmless leftovers.

For AI document pipelines, my review question is simple: who can retrieve the output after processing finishes?

## Merged PRs

None in this window.

The reporting interval is `[2026-09-25T00:00:00+08:00, 2026-09-26T00:00:00+08:00)`. A fresh GitHub merge-window query confirmed no authored merges.

## What shipped or moved

No code shipment, new disclosure outcome, or target-day vault-note edit was identified. This is a retrospective on the established result-artifact takeaway, not a claim that a new fix landed on September 25.

During finalization, I clarified the existing takeaway's distinction between an ordinary object identifier and an intentionally issued bearer capability. That clarification belongs to this publication pass, after the reporting window.

## Observed pattern

An upload check and a download check answer different questions. The first decides whether a caller can submit work. The second decides whether a caller may receive its result. A review that stops at successful admission leaves the output boundary unexplained.

The distinction also matters when choosing identifiers. A random object ID makes guessing harder; it does not establish ownership. An intentionally shareable capability URL is a different access model: possession is deliberately granted authority. That choice should be explicit, with a defined scope and lifetime, rather than inferred from an opaque filename.

## External reference

The [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) treats complex identifiers as defense in depth and calls for object-level permission checks even when references are difficult to guess.

The review implication is to record the intended access model before evaluating identifier strength. This is a design reference, not evidence of a vulnerability in a particular project.

## What was learned

The useful boundary map continues beyond processing: input, generated artifact, storage, retrieval, and permitted reader. Each output needs an explicit access decision.

For owner-private results, keep the owner check even when identifiers are random. For deliberate sharing, review capability issuance and lifecycle as authorization decisions. Do not silently substitute one model for the other.

## Takeaways

- **Review generated-result retrieval alongside upload admission.**
- Treat an object ID and a bearer capability as different contracts, even if both look like random strings.
- Keep derived artifacts within the source data's sensitivity assumptions unless there is evidence that processing removed the sensitive content.

## Repeat next time

List the generated outputs and their intended readers before reviewing implementation details. For each retrieval path, record whether access depends on authenticated ownership or a deliberately issued sharing capability. In an isolated test environment, verify that owner-private results remain unavailable to another account while the owner can still retrieve them. For sharing features, check the documented scope and expiration behavior separately.

## Vault redirect

The canonical result-artifact takeaway now records the identifier-versus-capability clarification and this publication reference. The existing upload and path-safety review links remain its workflow anchors. No private finding details or new project-specific vulnerability claim are included here.
