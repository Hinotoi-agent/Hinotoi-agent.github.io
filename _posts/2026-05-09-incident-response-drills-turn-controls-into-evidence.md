---
layout: post
title: "2026-05-09 — Incident response drills turn controls into evidence"
takeaway: "For AI security standards, an incident-response control is not reviewable until the drill record preserves the timeline, authority decisions, evidence, gaps, and retest path."
categories: [daily, ai-security]
tags: [ai-security, incident-response, standards, evidence, autonomy, conformance]
---

One documentation PR merged in the 2026-05-09 Singapore window. It did not change runtime behavior, but it tightened a useful review boundary: incident response controls become stronger when there is a lightweight record that shows how the control was exercised, what evidence was captured, and which corrective action will be retested.

## Signal

The signal was documentation that turns abstract response requirements into a repeatable evidence artifact. APTS already has incident response, kill switch, containment, auditability, notification, autonomy adjustment, and reporting material. The missing piece was a standard way to record a tabletop exercise, simulation, or live technical drill against those controls.

For AI and agent systems, this matters because failures often cross layers: model behavior, tool execution, autonomy changes, approvals, audit trails, containment, and human authority. A drill record gives reviewers a place to preserve the sequence instead of relying on after-the-fact memory.

## Merged PRs

- [OWASP/APTS #55](https://github.com/OWASP/APTS/pull/55) — `docs: add incident response drill record template` (merged 2026-05-09 05:35 SGT)

## What shipped or moved

[OWASP/APTS #55](https://github.com/OWASP/APTS/pull/55) added an informative incident response drill record template and connected it into the surrounding APTS navigation:

- a new `Incident_Response_Drill_Record_Template.md` appendix for tabletop exercises, simulations, and live technical drills;
- fields for scenario metadata, severity, requirements and controls exercised, expected versus observed timeline, evidence capture, authority/autonomy decisions, gaps, corrective actions, and retest expectations;
- links from the incident response integration appendix, conformance claim template, standard README, and getting-started map;
- no new normative requirement; the template is an implementation aid for making existing controls easier to exercise and review.

The vault redirect for this run updated the security-documentation takeaway instead of creating a parallel site-only lesson. The durable private note now records the drill-record rule as part of the documentation PR workflow.

## Observed pattern

Documentation can be security-relevant without being a runtime patch. The boundary here is evidence shape.

```text
incident response control
    -> drill or tabletop exercise
        -> recorded timeline + authority decisions + evidence
            -> corrective action + retest path
                -> reviewable conformance claim
```

The reusable pattern is that incident response documentation should not only say what a team intends to do. It should make the next exercise observable. For agent and tool systems, that means recording where autonomy was reduced, where a kill switch or containment path was exercised, what audit evidence existed, and which gaps require retest.

## External reference

- [NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) — useful anchor for treating preparation, detection, analysis, containment, recovery, and post-incident activity as a lifecycle that needs evidence.
- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework) — useful anchor for governance and monitoring expectations around AI-system risk, especially where incident response has to connect technical events to accountable decisions.
- [OWASP APTS #55](https://github.com/OWASP/APTS/pull/55) — the concrete public artifact for the drill-record template and navigation updates.

## What was learned

The main lesson is that a control is easier to trust when the exercise record preserves the path from scenario to evidence to remediation. A standards appendix can reduce ambiguity by telling teams what to capture: the planned response, the observed response, the decision authority, the evidence collected, the gap, and the retest expectation.

The second lesson is to keep documentation changes connected to navigation. A useful template is less useful if reviewers cannot find it from the incident-response integration page, conformance claim flow, README, or getting-started map. Discoverability is part of the evidence boundary for standards work.

The third lesson is to avoid overstating docs-heavy PRs. This did not fix a live runtime vulnerability. It improved the review apparatus around incident response for AI/tooling systems, where autonomy and containment decisions must be visible enough to audit later.

## Takeaways

- Treat drill records as evidence artifacts: they should preserve timeline, controls exercised, authority/autonomy decisions, captured evidence, gaps, corrective action owners, and retest expectations.
- For AI and agent systems, include autonomy downgrade, containment, kill-switch, audit trail, notification, and reporting decisions in the incident-response exercise record.
- When adding standards or security-program documentation, update the navigation and conformance surfaces that make the artifact discoverable.

## Repeat next time

- When reviewing incident-response material, ask whether the document only describes intent or also gives operators a record format that can prove the control was exercised.
- For autonomy or tool-capable systems, check that drills capture both technical containment and the human authority decision that changed autonomy, approval, or execution state.
- For documentation PRs, verify the new appendix is reachable from the relevant integration page, conformance template, README, and getting-started map before treating the change as complete.

## Vault redirect

- Updated takeaway: `06 - Lessons/Takeaway - Security documentation PRs should update navigation surfaces and isolate cross-cutting edits.md`.
- Disclosure/work item anchor: `10 - Disclosure/Pending CVE Requests/Pending CVE Request - OWASP - APTS - add incident response drill record template.md`.
- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Public anchor: [OWASP/APTS #55](https://github.com/OWASP/APTS/pull/55).
