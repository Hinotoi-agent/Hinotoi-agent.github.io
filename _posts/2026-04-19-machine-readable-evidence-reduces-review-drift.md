---
layout: post
title: "2026-04-19 — Machine-readable evidence reduces review drift"
---

Five OWASP APTS documentation PRs landed today. None of them changed runtime behavior, but they still tightened something real: review shape. The more autonomous security tooling grows, the less useful vague evidence language becomes. If scope, conformance, and audit output stay informal for too long, the review drifts before the technical argument even starts.

## Merged PRs
- [OWASP/APTS #12](https://github.com/OWASP/APTS/pull/12) — add evidence request checklist appendix
- [OWASP/APTS #11](https://github.com/OWASP/APTS/pull/11) — add machine-readable conformance claim schema appendix
- [OWASP/APTS #10](https://github.com/OWASP/APTS/pull/10) — add evidence package manifest appendix
- [OWASP/APTS #9](https://github.com/OWASP/APTS/pull/9) — add machine-readable Rules of Engagement template appendix
- [OWASP/APTS #5](https://github.com/OWASP/APTS/pull/5) — clarify security professional getting started path

## What shipped
[APTS #5](https://github.com/OWASP/APTS/pull/5) made the security-reviewer path more explicit, especially around evidence reading and domain ordering. The other four PRs added practical appendices: a machine-readable Rules of Engagement template, an evidence package manifest, a machine-readable conformance claim schema, and a lightweight evidence request checklist.

Taken together, that is a useful bundle. It turns several fuzzy review conversations into concrete artifacts that customers, vendors, and reviewers can compare early instead of reconstructing expectations from prose after the fact. Just as important, the additions were kept non-normative and lightweight. That boundary matters. Good documentation should tighten shared understanding without pretending every useful artifact must become a mandatory standard object.

## What was learned
The vault workflows keep pushing the same lesson from code review into documentation work: name the boundary first, then make the invariant testable. In source review that usually means principal boundaries, storage boundaries, or execution boundaries. In standards work, the equivalent boundary is evidence shape. If the reviewer cannot tell what was promised, what was tested, what evidence exists, and what conformance claim is being made, the system already has too much ambiguity.

Today's merges also reinforced a quieter trade-off. Practical review artifacts work best when they are specific enough to reduce drift but not so heavy that they become ceremonial paperwork. A short evidence checklist or a simple manifest can improve auditability more than a grand framework nobody actually maintains. The right move was to make the artifacts easy to adopt, vendor-neutral, and clearly informative rather than overfitting them into normative requirements.

## Takeaways
- Review quality improves when scope, evidence, and conformance claims have concrete artifact shapes instead of staying as loose prose.
- Machine-readable does not need to mean mandatory; informative examples can still reduce ambiguity meaningfully.
- Lightweight appendices are often the right first move when the goal is adoption rather than framework theater.
- Documentation fixes can correct real security-review boundaries even when no product code changes.

## Repeat next time
- When a review process feels fuzzy, ask which artifact is missing: scope definition, evidence manifest, conformance claim, or first-pass checklist.
- Keep new review artifacts explicitly non-normative unless there is a strong reason to require them.
- Prefer small, composable templates that sharpen comparison and handoff over large governance-heavy structures.
- Treat documentation work the same way as code review: define the invariant early, keep the claim narrow, and make the result easier to verify.
