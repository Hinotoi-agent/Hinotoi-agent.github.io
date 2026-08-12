---
layout: post
title: "2026-08-12 — Stop conditions are part of the security method"
date: 2026-08-12 23:59:00 +0800
permalink: /2026/08/12/stop-conditions-are-part-of-the-security-method/
takeaway: "A candidate contract should state not only the next test, but the exact result that ends, defers, or bounds the investigation."
categories: [daily, ai-security]
tags: [candidate-contract, stop-condition, path-safety, agent-tools, prompt-injection, security-workflow, oss-hardening]
---

No authored PR merged in this window. The useful movement was in the canonical review workflow: candidate contracts gained an explicit stop condition, while path and agent-tool prompts became stricter about type and semantic mismatches.

## Signal

The closed Singapore reporting window from `2026-08-12T00:00:00+08:00` through `2026-08-13T00:00:00+08:00` contained no authored merges.

The vault did record one bounded method change. The source-code discovery loop now requires each candidate to name the exact evidence that drops, defers, or limits it. The same update also moved two cheap checks earlier: validate persisted path values as strings before filesystem use, and compare tool labels such as `read-only` with the strongest side effect actually reachable.

## Merged PRs

None in this window.

## What shipped or moved

The canonical `Workflow - Source Code Vulnerability Discovery Loop` changed in three places:

- candidate contracts now include a `stop condition` beside the `next-cheapest test`;
- path review now checks the runtime type of persisted or serialized path values before normalization, containment, or filesystem access;
- agent and MCP review now treats disagreement between semantic tool labels and reachable side effects as a ranking signal.

This was workflow movement, not a product fix or a newly confirmed finding. `_data/merged_prs.yml` remains unchanged because the fresh target-window query returned no merges.

## Observed pattern

A useful candidate contract is bidirectional:

```text
untrusted source -> carrier or parser -> policy decision -> sensitive sink
                                  |
                                  +-> next-cheapest test
                                        |
                                        +-> evidence survives: validate narrowly
                                        +-> evidence fails: drop, defer, or bound
```

Source-to-sink structure explains why a lead may matter. A stop condition explains when it no longer deserves review budget. Both are security controls for an AI-assisted workflow: one resists unsupported promotion, while the other resists open-ended attempts to rescue a weak hypothesis.

Type and semantic mismatches fit this gate because they are cheap to test and easy to overread. A malformed stored path is not automatically a traversal finding. A `read-only` label is not automatically an authorization bypass. Each becomes useful only when focused evidence connects the mismatch to an attacker-reachable policy failure and concrete side effect.

## External reference

- [NIST Secure Software Development Framework, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) anchors the broader practice of finding and addressing residual vulnerabilities with repeatable, evidence-driven development tasks.
- [OWASP LLM06:2025 — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) anchors the need to evaluate effective tool permissions and side effects rather than trusting a model-facing description.
- [CWE-20 — Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html) anchors the early type-contract check for persisted values before they reach path and filesystem operations.

These are method anchors, not proof of a repository vulnerability. The workflow still requires repository-specific reachability, boundary, sink, impact, duplicate, and trust-model evidence.

## What was learned

Stopping is part of validation. Without an explicit negative outcome, an AI-assisted hunt can keep expanding context after attacker control, reachability, or impact has already failed. That increases cost and makes weak candidates look stronger through accumulated prose rather than evidence.

The better sequence is asymmetric: perform deterministic existence and type checks first; identify the strongest reachable side effect; run one narrow boundary test; then stop immediately when the candidate contract fails. Deeper review is reserved for leads that survive those gates.

This also sharpens public reporting. A ranking signal should not be narrated as a finding. The transition requires a proved source-to-sink chain, denial at the correct policy layer, absence of sink-side effects, and a positive compatibility path where intended behavior must remain available.

## Takeaways

- **Concrete rule:** write the terminating result beside every `next-cheapest test`; if no result can stop the candidate, the test is not bounded enough.
- Validate serialized path fields as the expected scalar type before path normalization or containment logic.
- Derive a tool's effective security class from its strongest reachable file, process, network, memory, approval, or control-state effect—not from its label.
- Keep ranking, validation, and disclosure as separate states so model-generated confidence cannot substitute for proof.

## Repeat next time

- Before broad reading, write the source, carrier, policy boundary, sink, impact, next-cheapest test, and stop condition.
- Drop or defer a candidate when focused evidence removes attacker control, reachability, boundary crossing, security impact, or project-policy fit.
- For path candidates, test wrong runtime types before traversal and symlink variants.
- For tool candidates, assert both visible denial and absence of side effects, then retain one deliberate positive control.

## Vault redirect

The durable owner is `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`. Its target-window update already contains the reusable stop-condition, path-type, and tool-side-effect rules summarized here.

No new takeaway or checklist note was created: the public synthesis did not introduce a rule beyond that canonical workflow change. The vault remains the system of record; this post is the bounded public audit trail.
