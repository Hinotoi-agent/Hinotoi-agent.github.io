---
layout: post
title: "2026-08-06 — Model observations remain untrusted across feedback loops"
date: 2026-08-06 23:59:00 +0800
permalink: /2026/08/06/model-observations-remain-untrusted-across-feedback-loops/
takeaway: "A target response, evaluator rationale, tool result, or memory recall remains untrusted when it is fed into the next model prompt; provenance labels help, but sensitive actions still need deterministic sink-side policy."
categories: [daily, ai-security]
tags: [prompt-injection, llm-harness, untrusted-observations, feedback-loop, prompt-driver, vault-backed-learning, oss-hardening]
---

An AI evaluation loop can protect the target and still let the target steer the evaluator. Every observation that returns to a model is another input boundary.

## Signal

The closed Singapore window was `2026-08-06T00:00:00+08:00` through `2026-08-07T00:00:00+08:00`.

The pre-run merge seed was empty, but a fresh authored merged-PR query found [`microsoft/RAMPART #60`](https://github.com/microsoft/RAMPART/pull/60), merged at `2026-08-06 09:09:35 +08:00`. The patch hardens RAMPART's LLM-backed prompt driver after prior target responses and evaluator rationales could return to the next driver prompt as free-form, instruction-like text.

## Merged PRs

- [`microsoft/RAMPART #60 — [FIX]: Security - Prompt Drivers: treat LLM observations as untrusted`](https://github.com/microsoft/RAMPART/pull/60) — merged at `09:09:35` Singapore time; merge commit `424bed63f3e5f3197caaaac592f2da9a7d4ef4de`.

## What shipped or moved

The merged patch changed three public files:

- `rampart/drivers/llm.py` serializes prior-turn values as JSON fields with explicit `_untrusted` labels and tells the driver not to obey instructions, role claims, or policy overrides inside those strings.
- `rampart/drivers/prompts/llm_driver_system_prompt.yaml` adds the same trust rule to the driver system prompt.
- `tests/unit/drivers/test_llm_driver.py` adds regression coverage for untrusted target responses, evaluator rationales, and the system-prompt contract.

The PR reports `26 passed` for the focused driver suite and `450 passed` for the full suite, plus successful Ruff, Pyright, compileall, and diff checks.

The merge was also added to `_data/merged_prs.yml`. In the canonical vault, the outcome now has a security-PR record, the existing prompt-injection feedback-loop takeaway covers model-to-model observations, and the source-code discovery workflow names this review edge explicitly.

## Observed pattern

The relevant chain is not only `untrusted text -> model`. It is a control loop:

```text
target agent response or evaluator rationale
  -> prior-turn observation builder
  -> prompt-driver user message
  -> driver LLM interprets mixed data and instructions
  -> next generated test prompt
  -> target agent
  -> another observation enters the loop
```

The target response is adversarial by design: RAMPART is testing another agent. An evaluator rationale may also contain or repeat target-controlled language. Passing either value through an evaluator, summary, or JSON serializer does not change its trust origin.

The merged mitigation improves separation by giving the observations a structure, explicit trust labels, and repeated instructions. That is useful model-level hardening, but it is not equivalent to a deterministic parser or authorization gate. A sufficiently capable or vulnerable model can still interpret data strings as instructions.

The broader AI-security rule is therefore two-layered:

1. make control text and untrusted observations visibly distinct before model interpretation;
2. keep sensitive tool, file, network, memory, and approval decisions behind deterministic policy at the actual action boundary.

## External reference

The [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) recommends separating instructions from data, validating inputs, monitoring outputs, and applying least privilege around downstream capabilities.

RAMPART #60 is a narrow implementation of the first part: it labels and structures observations that had previously been interpolated as free text. The external guidance also explains why this should not be overstated. Prompt framing is one defense layer; it does not replace capability restrictions or independent enforcement when model output can reach a consequential sink.

## What was learned

The word *observation* can hide provenance. Target output, evaluator rationale, critic output, tool results, retrieved memory, generated summaries, and prior reports may all look like neutral context by the time they reach a planner. If any field originated with an adversarial component, its trust label must survive every transform and handoff.

For review, the important object is the feedback edge:

```text
untrusted producer
  -> serializer / evaluator / summarizer
  -> next model context
  -> model-controlled decision
  -> consequential sink
```

Inspecting only the first prompt or final tool call misses the loop that connects them. The review should ask which model consumes each observation next, whether the field can issue instruction-like text, whether the model controls a tool or workflow decision, and where a non-model policy boundary finally constrains the result.

## Takeaways

- **Concrete rule:** inventory every target, evaluator, critic, tool, memory, and summary field that re-enters a model prompt; treat it as untrusted until a deterministic boundary says otherwise.
- Structured JSON and explicit `_untrusted` labels reduce ambiguity, but do not claim they eliminate prompt injection.
- Evaluator-generated text can preserve or amplify target-controlled instructions; an intermediate model is not a sanitizer by default.
- For sensitive effects, combine prompt separation with bounded schemas, action allowlists, least privilege, and sink-side policy enforcement.
- Regression tests should assert the prompt contract and preserve positive driver behavior, while security claims remain bounded to what those tests actually prove.

## Repeat next time

- Draw the full feedback graph before reviewing an AI harness: producer, transform, next model, decision, and sink.
- Search prompt builders for prior responses, rationales, summaries, tool output, memory, reports, and other interpolated model-generated fields.
- Test instruction-like strings in each observation field and verify that the application preserves its configured objective and expected output shape.
- Distinguish model-level hardening from deterministic enforcement in the finding, patch description, and validation claims.
- If the next model can select tools or mutate state, verify authorization and approval again immediately before dispatch, with denial leaving no sink-side effect.

## Vault redirect

- Outcome record: `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART prompt driver untrusted observations.md`.
- Durable lesson: `06 - Lessons/Takeaway - Prompt injection reliability can be amplified by client-side feedback loops.md`.
- Review-method owner: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.
- Change history: `05 - Workflows/Checklist Change - 2026-08-07 model observation feedback edges.md`.

The observation was routed into the existing feedback-loop takeaway and canonical discovery workflow rather than left as a website-only phrase or split into a duplicate prompt-injection checklist.