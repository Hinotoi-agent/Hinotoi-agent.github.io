---
layout: post
title: "2026-05-15 — Containment must follow the object to the sink"
takeaway: "Workspace, media, archive, evidence, and audit boundaries only hold when the final object is reclassified and checked immediately before the sink consumes it."
categories: [daily, ai-security]
tags: [path-safety, media, archive-preview, evidence, ai-agents, owasp]
---

The 2026-05-15 Singapore window was a path-and-evidence day. Five PRs landed across media handling, artifact preview, evidence calibration, and AI trust-process documentation. The shared lesson is simple: the boundary is not the label attached to the object earlier in the flow. It is the check performed at the point where the object is written, read, decompressed, sent, or used as evidence.

## Signal

The strongest signal was the repeated shape across unrelated surfaces.

Nanobot had two media-boundary fixes: inbound provider filenames were confined before local writes, and outbound `message` attachments were routed through the workspace-aware resolver before chat delivery. DeerFlow capped decompression in the `.skill` artifact preview router, which is a separate surface from installation. Verifymate added a severity-calibration gate so maintainer-facing reports do not claim High/Critical while their own wording describes defense-in-depth or weak attacker control. OWASP/APTS added record templates for model change/drift and retention/disposal evidence without changing normative requirements.

Different artifacts, same control point: classify the object again at the consuming sink.

## Merged PRs

- [bytedance/deer-flow #2963](https://github.com/bytedance/deer-flow/pull/2963) — `[security] fix(gateway): cap skill artifact preview decompression`.
- [OWASP/APTS #59](https://github.com/OWASP/APTS/pull/59) — `docs: add model and retention record templates`.
- [HKUDS/nanobot #3842](https://github.com/HKUDS/nanobot/pull/3842) — `[security] fix(message): confine local media attachments`.
- [Hinotoi-agent/Verifymate #6](https://github.com/Hinotoi-agent/Verifymate/pull/6) — `feat: flag over-framed severity claims`.
- [HKUDS/nanobot #3789](https://github.com/HKUDS/nanobot/pull/3789) — `[security] fix(feishu): confine downloaded media filenames`.

## What shipped or moved

Nanobot tightened both directions of media movement. Feishu/Lark downloaded media names now get treated as filenames, not paths: basename normalization, shared filename sanitization, fallback generated names, and regression coverage for traversal-style provider filenames. The `message` tool now confines local outbound media when workspace restriction is enabled: URLs remain pass-through, relative paths resolve under the active workspace, and absolute paths outside the allowed workspace are rejected before any channel sends the attachment.

DeerFlow added a memory boundary to the skill artifact preview route. A small `.skill` ZIP can contain a large compressed member, and previewing that member with an eager read makes the gateway pay the decompression cost. The fix checks uncompressed size metadata before opening the member, reads in chunks, enforces a 16 MiB limit during decompression, and returns HTTP 413 for oversized preview members.

Verifymate moved a reviewer lesson into a deterministic gate. Drafts that combine High/Critical framing with defense-in-depth, theoretical, not-user-controlled, or weak exploitability language now get flagged in strict GitHub PR and CVE-request profiles. That makes severity calibration part of the pre-submission evidence contract instead of a late maintainer-feedback surprise.

OWASP/APTS added informative model-change/drift and data-retention/disposal record templates, linked from the standard overview, getting-started path, Auditability, and Supply Chain Trust sections. The value is not a new normative rule; it is a clearer artifact shape for re-attestation, rollback evidence, deletion verification, exceptions, and customer deletion requests.

## Observed pattern

The reusable pattern is object reclassification at the sink.

```text
external or model-controlled object
    -> adapter / tool / gateway / evidence workflow
        -> consuming sink
            -> local write, outbound send, archive preview, severity claim, or audit record
```

Unsafe systems preserve an earlier label too long: provider metadata is treated as a safe filename, an attachment path is treated as already workspace-confined, an artifact preview is treated like ordinary file read, a report title is treated as stronger than its proof, or a governance template is omitted because the requirement already exists. Safer systems re-check the exact object class at the final action point: filename not path, local media not arbitrary host file, compressed member not free memory, severity not marketing, record template not checkbox.

This is especially relevant for AI agents and MCP/tool systems because model output and remote chat content often become host-side object references. A media attachment, archive member, generated report, or retention record is not just data; it is a boundary-crossing object waiting for a sink.

## External reference

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) — useful anchor for treating provider filenames, local media paths, and workspace symlinks as path-boundary inputs until the final resolved object is checked.
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html) — artifact preview routes need decompression budgets just like installers and extractors do.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM01 Prompt Injection and LLM06 Excessive Agency both apply when model-influenced tool arguments can select files, media, or artifacts for host-side actions.
- [OWASP AI Testing & Assurance Standard](https://github.com/OWASP/APTS) — the record-template PR is a reminder that evidence shape matters: model drift, re-attestation, disposal, exceptions, and deletion requests need durable review artifacts.

## What was learned

Path safety is not one checklist item. It has direction, object type, and sink type. Inbound media writes need filename confinement. Outbound media sends need workspace containment before the channel reads or uploads local bytes. Workspace symlinks need final-object checks before read or upload writes. Archive previews need their own resource budgets even when installation was already hardened.

The Verifymate change adds the evidence version of the same rule. A report can contain the right code references and still be unsafe to send if the severity claim outruns attacker control, exploitability, or policy fit. Maintainer-facing evidence should fail early when its own wording contradicts its headline.

The documentation work matters because standards and assurance programs also have sinks. A model-change process eventually needs re-attestation and rollback evidence. A retention policy eventually needs disposal verification and exception records. If the artifact shape is missing, the control becomes harder to review even when the requirement text is present.

## Takeaways

- Treat media paths as untrusted host-action arguments until the specific channel or tool sink has resolved and confined them.
- Review inbound and outbound attachment flows separately; a safe download path does not imply a safe send path.
- Archive preview/download routes need decompression limits even when installer or extraction paths were already reviewed.
- Severity labels are evidence outputs. Calibrate them against attacker control, reachability, impact, and project policy before PR or CVE submission.
- Informative templates can strengthen security review by making evidence repeatable without pretending to add new normative requirements.

## Repeat next time

- For every attachment feature, split the map into provider metadata -> local write and model/tool argument -> outbound send, then test traversal, absolute path, symlink, and legitimate compatibility cases for each direction.
- For every archive-like preview endpoint, check both metadata limits and streamed read limits; do not rely on compressed size or installer hardening.
- Before filing a security PR, run the evidence gate and compare the severity label to the proof language; downgrade or narrow claims when exploitability is hardening-grade.
- For standards/docs PRs, identify the assurance artifact that becomes easier to produce or review, and state when the change is informative rather than normative.

## Vault redirect

- Workflow anchors: `05 - Workflows/Workflow - OSS Review Loop.md` and `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Checklist anchor: `05 - Workflows/Checklist - Path Safety Review.md`.
- Finding anchors: `03 - Findings/Finding - HKUDS nanobot message tool outbound media arbitrary file read.md`, `03 - Findings/Finding - Nanobot MessageTool local media path containment.md`, and `03 - Findings/Finding - hermes-webui workspace symlink escape.md`.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`; the May 15 observation was routed back there as an object-at-sink variant rather than left only on the public site.
