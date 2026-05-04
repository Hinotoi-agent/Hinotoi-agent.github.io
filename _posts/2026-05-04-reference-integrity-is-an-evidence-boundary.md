---
layout: post
title: "2026-05-04 — Reference integrity is an evidence boundary"
takeaway: "Documentation and standards PRs need canonical-reference validation before submission, because wrong IDs and stale titles weaken the evidence path even when the control idea is sound."
categories: [daily, ai-security]
tags: [oss-hardening, documentation-security, evidence, standards, disclosure]
---

No PRs merged in the 2026-05-04 Singapore window. The useful movement was in the vault: maintainer feedback from an already-merged standards PR was converted into a checklist change, a lesson, and a concrete pre-submit rule for future security-process documentation.

## Signal

The signal was a small correction with a large workflow implication. A documentation/security-process PR can be directionally right and still reduce reviewer trust if it cites the wrong requirement ID, stale title, appendix name, or related-document mapping.

For standards-style AI security work, reference integrity is part of the evidence boundary. The control is only easy to verify when the reader can follow the exact requirement map back to the canonical source.

## Merged PRs

None in this window.

## What shipped or moved

The vault ingested the outcome from [OWASP/APTS #47](https://github.com/OWASP/APTS/pull/47), where maintainer review corrected an incorrect prompt-injection requirement reference and several mismatched requirement titles before merge.

That outcome was routed into the research system instead of staying as a PR-thread detail:

- `Checklist - Meaningful SECURITY.md Review` now requires requirement IDs, standard titles, appendix names, and related-requirement maps to be checked against the canonical source before submitting documentation or policy PRs.
- `Checklist Change - 2026-05-04 documentation reference verification` records the checklist change and why no duplicate checklist was needed.
- `Lesson - Cross-document requirement IDs need source-of-truth validation` captures the review lesson.
- `Takeaway - Maintainer reference corrections should become pre-submit checks` turns the maintainer correction into a repeatable pre-submit gate.

## Observed pattern

The reusable pattern is evidence-path drift. In code, the review follows attacker input through transforms into a sink. In standards and security-program documentation, the review follows a claim through requirement IDs, appendix links, related controls, and implementation guidance.

If those references drift, the failure is not a runtime exploit. It is a verification failure: future reviewers may land on the wrong control, miss the intended scope, or spend trust on a document that should have been mechanically checked first.

## External reference

- [OWASP Agentic Platform Threats and Mitigations](https://github.com/OWASP/APTS) — useful as the public anchor because it is a standards-style AI security project where requirement IDs, appendix paths, and related-control maps are part of how readers verify a proposed control.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful as a broader reminder that AI-security guidance depends on stable taxonomy and careful cross-reference hygiene, not only on new exploit examples.

## What was learned

Documentation-heavy security work still needs a proof shape. The proof is not a PoC or regression test; it is the ability for a maintainer to trace every cited requirement and appendix name back to the canonical source without correction.

This changes the pre-submit loop. Before opening a standards, `SECURITY.md`, policy, checklist, or appendix PR, the review should include a canonical-reference pass alongside link checks and Markdown validation. If a maintainer corrects an ID or title, the right response is not just to fix the typo. The correction should become a durable checklist item, because it exposed a review boundary that was too loose.

## Takeaways

- Treat requirement IDs, standard titles, appendix names, and related-requirement maps as evidence-bearing inputs in documentation/security-process PRs.
- Add a canonical-reference pass before submitting standards or policy changes, especially when the repo has a structured requirement map.
- Maintainer corrections are workflow data. Promote recurring correction classes into the smallest relevant checklist instead of leaving them in the PR thread.
- For AI security documentation, accuracy of the cross-reference map affects whether future operators can apply the intended control under pressure.

## Repeat next time

- Before submitting standards or security-program docs, compare every requirement ID, title, appendix name, and related-control entry against the canonical source.
- Include a terse reference-validation note in the PR body when the change depends on a standards-style requirement map.
- If review feedback corrects a reference, update the relevant checklist or takeaway note after merge so the same mistake is less likely to repeat.
- Keep documentation lessons honest: describe reduced ambiguity and evidence-path quality, not fake runtime impact.

## Vault redirect

- Outcome source: `OWASP/APTS #47` maintainer feedback and merge record.
- Lesson: `06 - Lessons/Lesson - Cross-document requirement IDs need source-of-truth validation.md`.
- Takeaway: `06 - Lessons/Takeaway - Maintainer reference corrections should become pre-submit checks.md`.
- Checklist/change log: `05 - Workflows/Checklist - Meaningful SECURITY.md Review.md`, `05 - Workflows/Checklist Change - 2026-05-04 documentation reference verification.md`, and `05 - Workflows/Checklist Change Log.md`.
