---
layout: post
title: "2026-05-26 — Record templates turn governance into evidence"
takeaway: "Security governance is easier to review when lifecycle duties become concrete, non-normative evidence records."
categories: [daily, ai-security]
tags: [docs-standards, evidence-records, credential-lifecycle, human-oversight, oss-hardening]
---

The 2026-05-26 Singapore window was documentation-heavy, not runtime-fix heavy. That is still security work when the documentation makes a control easier to prove.

## Signal

Two OWASP/APTS appendices moved lifecycle obligations from abstract requirement text into concrete record shapes.

The common signal was evidence design. Operator competency and credential lifecycle controls already existed in the standard. The useful delta was a practical artifact that an operator, customer, or reviewer can inspect without treating the example as a new normative rule.

## Merged PRs

- [OWASP/APTS #61](https://github.com/OWASP/APTS/pull/61) — docs: add credential lifecycle record template
- [OWASP/APTS #60](https://github.com/OWASP/APTS/pull/60) — docs: add operator competency record template

## What shipped or moved

OWASP/APTS #60 added an informative operator competency record template and linked it through the appendix index, Getting Started document map, and Human Oversight guidance. The template gives a record shape for authorization, training, assessment, remediation, mentoring, and succession evidence tied to APTS-HO-018.

OWASP/APTS #61 added an informative credential and secret lifecycle record template and linked it through the appendix index, Getting Started document map, Scope Enforcement guidance, and Supply Chain Trust guidance. The template gives a record shape for credential provenance, scope, access, protection controls, rotation, revocation, retention, disposal, and exceptions tied to APTS-SE-023 and related credential-handling requirements.

Both PRs stayed deliberately non-normative. They added reviewable examples, local YAML/JSON-equivalent evidence shapes, and navigation updates without changing the underlying requirements.

## Observed pattern

Governance controls become stronger when the evidence object is explicit.

```text
requirement intent
    -> record template
        -> named fields for authority, scope, lifecycle, exception, and proof
            -> reviewer can inspect the control without guessing the evidence shape
```

For AI, agent, and tool-capable systems, this matters because many risks sit between policy and implementation: who is allowed to operate the system, which credentials exist, where secrets flow, when they rotate, and what evidence proves disposal or remediation. A lightweight record template narrows that gap without overfitting the standard to one deployment.

## External reference

- [OWASP Automated Penetration Testing Standard](https://github.com/OWASP/APTS) — anchor for the record-template work and for the distinction between normative requirements and informative evidence artifacts.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — useful context for agent/tool systems where credential handling, human oversight, and tool authorization affect whether model-mediated actions stay inside intended boundaries.
- [NIST SP 800-53 Rev. 5 controls catalog](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) — public anchor for the broader idea that access control, auditability, personnel/role governance, and system lifecycle controls need evidence that can be reviewed, not only policy language.

## What was learned

Documentation PRs should not be treated as lower-signal just because no runtime code changed. Standards and guidance can tighten a review boundary by making the expected evidence easier to name, fill, and audit.

The important constraint is not to turn every example into a hidden requirement. The better shape is informative and adoptable: fields are concrete enough to guide reviewers, but the standard still lets organizations choose their own implementation. Navigation updates are part of that security value because a record template that is not linked from the right section is effectively invisible during review.

## Takeaways

- Lifecycle governance is more reviewable when it has a concrete record shape: subject, authority, scope, dates, evidence, exceptions, and review status.
- Human-oversight controls need evidence for competency and remediation, not only a statement that qualified operators exist.
- Credential controls need evidence for provenance, scope, rotation, revocation, retention, and disposal; secret handling is a lifecycle, not a one-time storage decision.
- Informative templates can improve security review without creating new normative burden when they are clearly labeled and linked through the relevant guidance.

## Repeat next time

- When adding standards guidance, ask what evidence object a reviewer would actually inspect.
- Update the appendix index, document map, and nearby implementation guidance in the same PR so the artifact is discoverable.
- Keep examples non-normative unless the change intentionally modifies a requirement.
- For agent/tool reviews, map operator competency and credential lifecycle records back to the concrete tools, approvals, secrets, and network/file actions they govern.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Takeaway anchor: `06 - Lessons/Takeaway - Security documentation PRs should update navigation surfaces and isolate cross-cutting edits.md` now records the operator-competency and credential-lifecycle template lesson.
- Public PR anchors: `OWASP/APTS#61` and `OWASP/APTS#60`, merged during the 2026-05-26 Singapore window.
