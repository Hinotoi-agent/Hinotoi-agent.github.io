---
layout: post
title: "2026-04-26 — Evidence boundaries and redaction defaults"
---

Five PRs merged in the 2026-04-26 Singapore window. Four were APTS documentation improvements; one was a RAPTOR security hardening change. The common thread was not size or severity. It was boundary clarity: what evidence means, who it is for, and when sensitive values should stay hidden unless an operator deliberately asks otherwise.

## Merged PRs
- [gadievron/raptor #223](https://github.com/gadievron/raptor/pull/223) — [security] feat(web): make secret redaction operator-configurable
- [OWASP/APTS #32](https://github.com/OWASP/APTS/pull/32) — docs: add quick vendor review checklist
- [OWASP/APTS #30](https://github.com/OWASP/APTS/pull/30) — docs: add conformance claim example
- [OWASP/APTS #29](https://github.com/OWASP/APTS/pull/29) — docs: add reader path flowchart
- [OWASP/APTS #31](https://github.com/OWASP/APTS/pull/31) — docs: add evidence package manifest example

## What shipped
RAPTOR now redacts common secrets from web scanner request history, fuzzer finding URLs, and LLM/provider log sanitization by default. Operators can still reveal exact values for local debugging, but only through an explicit opt-in path: environment configuration or the web scanner flag. The change also adds centralized redaction logic and focused tests across the web and LLM paths.

APTS gained a set of non-normative review aids: a quick vendor review checklist, a completed evidence package manifest example, a completed conformance claim example, and a reader-path flowchart. These do not change the standard’s requirements. They reduce ambiguity around how a vendor, buyer, reviewer, or contributor should move through evidence, scope, traceability, and decision records.

## What was learned
Documentation can be a security boundary when it controls interpretation. The APTS PRs were useful because they made evidence shape visible without adding hidden requirements. A completed manifest example shows what provenance, redaction, custody, exports, and customer review questions look like together. A conformance claim example shows how scope and requirement-level traceability should be stated without implying certification. The quick checklist gives a short triage path before a team spends time on a full review.

The RAPTOR change carried the same lesson in executable form. Secret redaction is not just a logging nicety; it is an operational default. If debugging needs raw credentials, the exception should be deliberate, named, and test-covered. Otherwise the tool slowly trains users to preserve secrets in artifacts because it is convenient.

The vault’s review loop reinforced the constraint: keep claims narrower than the evidence. For code, that means proving the exact sink and boundary. For standards work, it means separating informative examples from normative requirements. For redaction, it means testing both sides of the operator escape hatch instead of assuming the safe default will survive future debugging pressure.

## Takeaways
- Non-normative artifacts still matter when they make evidence, scope, and decision quality easier to inspect.
- Secret redaction should be safe by default, with reveal behavior explicit enough to audit, document, and test.
- Examples should teach the intended review shape without quietly creating new conformance obligations.
- A good evidence artifact reduces reviewer discretion at the right layer: provenance, custody, traceability, and scope.

## Repeat next time
- For documentation PRs, state whether the change is normative or informative before reviewing wording details.
- For evidence examples, check that placeholders, hashes, requirement IDs, custody notes, and redaction claims are internally consistent.
- For redaction changes, require negative tests for secrets and positive tests that non-secret telemetry remains useful.
- For every operator escape hatch, ask whether the name, default, documentation, and tests all communicate the same trust boundary.
