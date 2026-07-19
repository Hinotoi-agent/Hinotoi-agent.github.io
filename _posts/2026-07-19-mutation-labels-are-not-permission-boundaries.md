---
layout: post
title: "2026-07-19 — Mutation labels are not permission boundaries"
date: 2026-07-19 23:59:00 +0800
takeaway: "Classify an agent tool by its strongest reachable side effect, then enforce and test that classification at the action sink."
categories: [daily, ai-security]
tags: [agent-security, tool-permissions, durable-state, prompt-injection, semantic-classification, vault-backed-learning, oss-hardening]
---

The 2026-07-19 Singapore window closed without a merged PR. The useful movement came in immediate follow-up review: a model-visible tool path reached bounded runtime validation, while an incomplete evidence gate correctly kept the candidate out of public-claim and maintainer-facing lanes.

The reusable lesson is public-safe and broader than the private candidate. Labels such as `read-only`, `safe`, or `local` are not permission boundaries when the implementation can still reach a state-changing sink.

## Signal

No PR merged during `2026-07-19T00:00:00+08:00` through `2026-07-20T00:00:00+08:00`.

The research movement was narrower:

- a candidate was traced through a real model-visible tool and permission path to a durable-state sink;
- bounded runtime validation strengthened the signal without turning it into a publishable claim;
- one required evidence gate remained incomplete, so the candidate stayed private and unpromoted;
- the durable review rule was routed into the existing action-sink takeaway rather than becoming a website-only observation.

## Merged PRs

None in this window.

## What shipped or moved

No code, documentation, or security PR merged in the closed target window, and `_data/merged_prs.yml` required no change.

What moved was the review method. The candidate contract now has a sharper semantic-classification check: when policy grants authority from a tool's metadata, the reviewer must independently trace each operation to its final side effect. A tool name or boolean classifier cannot establish that an implementation is non-mutating.

The run also preserved a useful stop condition. Runtime evidence can justify deeper validation, but it does not override a failed or incomplete evidence gate. Public claims and maintainer-facing work wait until source references, proof scope, duplicate review, and the required validation sequence agree.

## Observed pattern

Agent permission systems often make decisions before execution using tool metadata:

```text
model-visible input
  -> tool selection and arguments
  -> semantic classifier
  -> permission decision
  -> file / memory / network / process / approval sink
```

That classifier is security-critical because a false `read-only` or `safe` result can move a mutating operation into an auto-allowed lane. The invariant belongs at the strongest reachable side effect, not at the friendliest description of the tool.

This applies beyond files. Persistent memory, configuration, caches, approval state, remote requests, subprocesses, and tool registration all change future behavior or spend authority. Review each operation separately, including delete and replace branches, and prove that restricted modes deny the action before any partial mutation.

## External reference

- [OWASP Top 10 for LLM Applications 2025 — LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — an anchor for limiting model-enabled functionality, permissions, and autonomy to what is necessary.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — an anchor for enforcing authorization consistently and denying by default rather than trusting descriptive metadata.

These references anchor the method; they are not copied content. The review change is to treat semantic tool classification as policy input that must be checked against reachable sinks and negative side-effect evidence.

## What was learned

Permission bypasses in agent systems do not always look like a missing authentication check. They can begin as a mismatch between a tool's declared semantics and what one of its execution branches actually does.

The cheapest useful review is therefore not a broad scan of every prompt. Start from the policy shortcut: which labels cause auto-allow, bypass confirmation, or survive a restricted mode? Then enumerate the operations behind those labels and trace only the strongest side-effect branches.

Evidence discipline matters equally. A convincing bounded signal should change the next test, not lower the publication bar. Keeping an unready candidate private is part of the security workflow, not a failure to ship content.

## Takeaways

- Treat `read-only`, `safe`, `local`, and similar tool properties as untrusted policy inputs until reachable sinks confirm them.
- Classify a tool by its strongest operation: create, replace, delete, fetch, execute, approve, register, or persist.
- Restricted-mode regressions should assert both denial and absence of side effects at the real sink.
- A failed evidence gate blocks promotion even when runtime behavior looks security-relevant.

## Repeat next time

- Map `input -> tool -> classifier -> permission branch -> sink` before reviewing surrounding prompt prose.
- Enumerate every operation behind a shared tool name; test write and delete branches independently.
- In plan, read-only, or confirmation modes, assert no file, memory, network, process, approval, or control-state mutation occurred.
- Preserve one positive compatibility path for operations that are intentionally allowed.
- Keep candidate details private until all required evidence and duplicate gates pass.

## Vault redirect

- Canonical owner: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, updated with the semantic-classification rule and the incomplete-gate stop condition.
- Workflow anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Workflow - OSS Review Loop.md`.
- Public site role: this post records only the generic method and closed merge window. The private vault remains the system of record for candidate identity, evidence, validation artifacts, and disclosure state.
