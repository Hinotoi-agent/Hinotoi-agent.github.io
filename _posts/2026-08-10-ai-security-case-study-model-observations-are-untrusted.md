---
layout: post
title: "2026-08-10 — Model observations are still untrusted input"
date: 2026-08-10 12:03:54 +0800
permalink: /2026/08/10/ai-security-case-study-model-observations-are-untrusted/
takeaway: "A target response or evaluator rationale does not become trusted when it is fed back into another model; preserve the data boundary and enforce sensitive policy outside model interpretation."
categories: [daily, case-study, ai-security]
tags: [case-study, prompt-injection, llm-harness, untrusted-input, feedback-loop, agent-security]
---

The closed Singapore reporting window contained no authored merge. The durable movement was publication of a vault-backed case study: an AI evaluation harness contains more than one model boundary, and text produced by a target or evaluator can become the next instruction surface when a prompt driver consumes it without a clear data contract.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-10T00:00:00+08:00` through `2026-08-11T00:00:00+08:00`.

The day's public movement was a concrete AI-security case study grounded in the existing RAMPART outcome record. RAMPART's LLM-backed prompt driver had used prior target responses and evaluator rationales to choose its next test prompt. Those observations were useful evidence, but they were also model-produced text that could contain instruction-like content.

The security signal is a feedback edge:

```text
model output
  -> orchestration code
  -> next model prompt
```

Crossing orchestration code does not make the output trusted.

## Merged PRs

None in this window.

The RAMPART PR discussed below merged on `2026-08-06` Singapore time. It is evidence for this case study, not a merge attributed to the August 10 reporting window.

## What shipped or moved

- The existing RAMPART security-PR outcome, changed files, merge commit, and validation record were distilled into a public-safe case study.
- The post preserved the distinction between model-level prompt hardening and deterministic authorization at tool, file, network, memory, and approval sinks.
- The vault-backed review rule was made operational: trace every model-produced observation when it re-enters a planner, driver, judge, critic, or tool-selection prompt.
- `_data/merged_prs.yml` remained unchanged because both the context seed and a fresh authored merged-PR query were empty for the target window.

## Observed pattern

AI orchestration often turns output back into input:

```text
target / evaluator / tool / memory output
  -> history, summary, or structured carrier
  -> next model prompt
  -> model decision
  -> optional sensitive sink
```

The carrier can improve representation without changing trust. JSON serialization and explicit labels reduce role ambiguity, but any security consequence still needs an independent policy boundary at the action sink.

## External reference

- [Microsoft RAMPART PR #60](https://github.com/microsoft/RAMPART/pull/60) is the public evidence anchor for the patch, affected files, and validation described here.
- [OWASP LLM01:2025 — Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) anchors the broader rule that external content and model output can carry instructions, and that formatting alone does not eliminate the risk.

These links are anchors rather than copied source material. The review-method change is to map feedback edges explicitly and separate model-facing representation controls from deterministic authorization and sink-side enforcement.

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

## Takeaways

- **Concrete rule:** treat every model-produced observation that re-enters another model as untrusted input, even after it passes through history, evaluation, summarization, or JSON serialization.
- Review the feedback edge, not only the original prompt entry point.
- Keep model-level hardening claims bounded: labels and prompt warnings reduce ambiguity but do not replace authorization.
- When downstream behavior can mutate state or reach tools, files, networks, memory, or approvals, prove denial and absence of sink-side effects independently.
- Keep event time separate from publication time; the source PR supports this case study but does not belong in the August 10 merged-PR window.

## Repeat next time

- Trace target responses, evaluator rationales, tool output, summaries, memory recalls, critic output, and generated reports whenever they re-enter a model prompt.
- Mark which fields are attacker-influenced before reviewing prompt templates or orchestration logic.
- Preserve observations as bounded structured data and keep instructions outside their values.
- Add a regression with instruction-like payload text and prove the value survives only in the intended data field.
- For tool, file, network, memory, or approval effects, test the independent policy decision and absence of sink-side effects; do not treat prompt wording as authorization.

## Vault redirect

The durable research record remains in the private OSS Vulnerability Research Vault. This case is owned by the existing RAMPART security-PR record, the prompt-injection feedback-loop takeaway, and the logged source-code discovery workflow change for model observation feedback edges.

No vault note or checklist was changed for this finalization. The public synthesis does not introduce a separate finding or a new review rule; it exposes the reusable rule already routed into the canonical workflow: every model-to-model observation edge is untrusted until a deterministic boundary proves otherwise. The existing `Public observations should route back into the vault` takeaway already owns the publication and maintenance-routing gate, so duplicating it would create the silo this process is designed to avoid.
