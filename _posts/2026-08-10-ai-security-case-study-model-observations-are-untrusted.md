---
layout: post
title: "2026-08-10 — Model observations are still untrusted input"
date: 2026-08-10 12:03:54 +0800
permalink: /2026/08/10/ai-security-case-study-model-observations-are-untrusted/
takeaway: "A target response or evaluator rationale does not become trusted when it is fed back into another model; preserve the data boundary and enforce sensitive policy outside model interpretation."
categories: [case-study, ai-security]
tags: [case-study, prompt-injection, llm-harness, untrusted-input, feedback-loop, agent-security]
---

An AI evaluation harness contains more than one model boundary. Text produced by the target or evaluator can become the next instruction surface when a prompt driver consumes it without a clear data contract.

## Signal

RAMPART's LLM-backed prompt driver used prior target responses and evaluator rationales to choose its next test prompt. Those observations were useful evidence, but they were also model-produced text that could contain instruction-like content.

The security signal is a feedback edge:

```text
model output
  -> orchestration code
  -> next model prompt
```

Crossing orchestration code does not make the output trusted.

## Threat model

The bounded threat model is an AI evaluation run in which the target agent can influence its response text. That text is returned to a separate driver model responsible for generating the next user prompt. Evaluator rationale is another model-produced input on the same path.

The target does not need direct access to the driver's system prompt. It only needs its response to contain instruction-like text that the harness later places into the driver's user message. The consequence is steering of the evaluation process: the driver may depart from the configured objective or strategy.

This is prompt-injection hardening inside an evaluation harness, not a deterministic authorization bypass. The merged evidence supports a clearer trust contract and reduced role ambiguity; it does not prove that every model will ignore every adversarial string.

## Finding and PR

Public PR: [`microsoft/RAMPART #60 — [FIX]: Security - Prompt Drivers: treat LLM observations as untrusted`](https://github.com/microsoft/RAMPART/pull/60).

Merge commit: `424bed63f3e5f3197caaaac592f2da9a7d4ef4de`.

Security-relevant files:

- `rampart/drivers/llm.py` — changes `_build_user_message()` from free-form concatenation to labeled JSON observations with an explicit warning.
- `rampart/drivers/prompts/llm_driver_system_prompt.yaml` — adds the trust rule to the driver system prompt.
- `tests/unit/drivers/test_llm_driver.py` — verifies the JSON representation and system-prompt contract.

Before the patch, the driver message directly concatenated `Agent response`, `Evaluator outcome`, and `Evaluator rationale`. A target response such as an instruction to ignore previous directions therefore arrived as ordinary prose in the same driver-side message used to select the next prompt.

## Exploit path

The public source-to-sink chain was:

```text
instruction-like text in a target-agent response
  -> latest turn stored in evaluation history
  -> LLMDriver._build_user_message()
  -> free-form driver-side user message
  -> driver model interprets the mixed observation/control text
  -> next generated test prompt departs from the configured objective
```

Evaluator rationale followed the same feedback path and could carry similar instruction-like text. The security boundary was not the history object itself; it was the point where untrusted observations were transformed into a new model prompt without an explicit distinction between evidence and control text.

## Mitigation

The merged patch makes that distinction explicit at two layers:

- prior-turn values are serialized as JSON rather than concatenated as prose;
- attacker-influenced fields are named `agent_response_untrusted` and `evaluator_rationale_untrusted`;
- each driver-side message warns against following instructions, role claims, or policy overrides inside JSON string values;
- the driver system prompt repeats the same rule and limits those observations to evidence for selecting the next user prompt.

This is an appropriate narrow fix for the demonstrated prompt contract. It is still model-level hardening, not a complete security boundary. If a downstream choice can invoke tools, write files, reach networks, mutate memory, or approve actions, deterministic schemas, allowlists, independent policy checks, and sink-side enforcement remain necessary.

## Verification

The focused regression tests added in `tests/unit/drivers/test_llm_driver.py` are:

- `test_non_empty_history_labels_agent_response_as_untrusted_data` — injects instruction-like target text and evaluator rationale, then proves both remain exact JSON string values under explicit `_untrusted` keys and that the warning is present;
- `test_system_prompt_treats_observations_as_untrusted` — proves the system prompt names target-agent responses as untrusted and tells the driver never to follow instructions inside them.

The PR recorded these commands and results:

```sh
uv run pytest tests/unit/drivers/test_llm_driver.py -q
# 26 passed

uv run pytest -q
# 450 passed

uv run ruff check rampart/drivers/llm.py tests/unit/drivers/test_llm_driver.py
uv run ruff format --check rampart/drivers/llm.py tests/unit/drivers/test_llm_driver.py
uv run pyright rampart/drivers/llm.py tests/unit/drivers/test_llm_driver.py
# 0 errors, 0 warnings, 0 informations
```

`compileall` and `git diff --check` also passed. The negative proof is representation-shaped: adversarial text remains labeled observation data instead of being emitted as unlabeled prose. The positive control is preserved: the driver still receives the target response, evaluator outcome, and rationale as evidence for choosing its next prompt.

## What was learned

Model output remains untrusted when another model produced, evaluated, summarized, or stored it. The useful review unit is the feedback edge, not only the original prompt entry point.

For planners, drivers, judges, critics, memory systems, and tool selectors, map:

```text
producer
  -> observation carrier or transform
  -> prompt construction
  -> model decision
  -> sensitive downstream sink
```

Then separate two questions. First, can observation text be mistaken for control text? Second, what deterministic boundary limits the consequences if the model still follows it? Structured serialization and trust labels address the first question. Authorization and sink-side controls address the second.

## Repeat next time

- Trace target responses, evaluator rationales, tool output, summaries, memory recalls, critic output, and generated reports whenever they re-enter a model prompt.
- Mark which fields are attacker-influenced before reviewing prompt templates or orchestration logic.
- Preserve observations as bounded structured data and keep instructions outside their values.
- Add a regression with instruction-like payload text and prove the value survives only in the intended data field.
- For tool, file, network, memory, or approval effects, test the independent policy decision and absence of sink-side effects; do not treat prompt wording as authorization.

## Vault redirect

The durable research record remains in the private OSS Vulnerability Research Vault. This case is owned by the existing RAMPART security-PR record, the prompt-injection feedback-loop takeaway, and the logged source-code discovery workflow change for model observation feedback edges.

No new checklist was created for this publication. The public synthesis does not introduce a separate finding; it exposes the reusable review rule already routed into the canonical workflow: every model-to-model observation edge is untrusted until a deterministic boundary proves otherwise.
