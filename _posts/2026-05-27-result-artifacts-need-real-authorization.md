---
layout: post
title: "2026-05-27 — Result artifacts need real authorization"
takeaway: "Generated result URLs are authorization boundaries when they expose user-derived files."
categories: [daily, ai-security]
tags: [quiet-day, result-artifacts, capability-urls, upload-processing, evidence-gates, oss-hardening]
---

The 2026-05-27 Singapore window had no merged PRs. The useful movement was in the private research system: a file-processing finding was written with local proof, then pushed through the VulnWeave gate and routed back into a reusable takeaway.

## Signal

The signal was not a new public patch. It was a sharper review rule for generated artifacts.

File-processing systems often protect the upload path but leave the output path softer: OCR text, converted markdown, result archives, extracted bundles, logs, and previews get served later through a small identifier. If that identifier is predictable and the route has no owner check, the download URL becomes the authorization boundary.

## Merged PRs

None in this window.

## What shipped or moved

A private vault finding moved from hypothesis to locally validated candidate. The evidence record captured the affected repository/commit, the boundary, a bounded impact claim, duplicate-search terms, a suggested fix shape, and a safe local proof that exercised the real download routes without publishing exploit details.

VulnWeave also ran against the finding and target checkout with an `OK` gate result. The important interpretation stayed explicit: graph/candidate output is workflow evidence, not standalone proof. Reachability, attacker control, duplicate status, impact, and severity still have to be confirmed separately.

The reusable lesson was reverse-routed into the vault as `Takeaway - Result download URLs need capability-grade identifiers`, so the public observation does not become a separate website-only note.

## Observed pattern

Generated artifacts inherit the sensitivity of the input that produced them.

```text
user document / prompt / file
    -> server-side processing
        -> generated text, archive, preview, log, or bundle
            -> download URL
                -> identifier is either a real capability or a weak guessable pointer
```

For AI and agent systems, this pattern appears around OCR, document conversion, tool output bundles, prompt/debug traces, code-review exports, sandbox artifacts, and upload preprocessing. The dangerous mistake is to review only the initial upload control and ignore the later retrieval path.

## External reference

- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html) — useful public anchor for object identifiers that become access-control decisions when the server trusts the key alone.
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html) — broad anchor for generated outputs that disclose private document, prompt, or processing content.
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — review anchor for testing direct object access, authorization checks, and predictable resource identifiers.

## What was learned

A result URL should be treated like a capability if it is the only thing standing between a user-derived artifact and another client. Timestamps, counters, filenames, path-derived names, and other guessable identifiers are operationally convenient, but they are not authorization.

The proof shape also matters. For this class, a good test does not need to publish private exploit detail. It needs to show that a second unauthenticated or unauthorized client can retrieve a planted victim artifact with only the result identifier, and that the artifact contains sensitive output derived from the victim's input.

## Takeaways

- Review generated-result downloads as first-class authorization surfaces, not as harmless static-file helpers.
- Treat OCR text, markdown conversions, archives, previews, logs, and debug bundles as sensitive outputs when they derive from user-controlled documents or prompts.
- If a download route has no owner/session check, its identifier must be unguessable, scoped, and ideally expiring.
- Evidence gates like VulnWeave are useful when their role is kept narrow: they support workflow correlation; they do not replace route-level proof.

## Repeat next time

- Map both sides of every file-processing feature: upload/submit path and result retrieval path.
- Check whether result identifiers are random capability tokens or only timestamps, counters, filenames, or path-derived strings.
- Test with a planted victim output and a second client that knows only the identifier.
- Record graph/evidence-gate output separately from the proof so correlation does not get mistaken for confirmed reachability.

## Vault redirect

- Finding anchor: a private vault finding for predictable unauthenticated result downloads was updated on 2026-05-27 with local proof and bounded impact.
- Gate anchor: the same finding received a VulnWeave `OK` artifact; the post keeps the gate in its proper role as workflow evidence.
- Takeaway anchor: `06 - Lessons/Takeaway - Result download URLs need capability-grade identifiers.md` now records the durable review rule.
- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` remain the canonical path for turning candidates into validated, non-duplicate, bounded findings.
