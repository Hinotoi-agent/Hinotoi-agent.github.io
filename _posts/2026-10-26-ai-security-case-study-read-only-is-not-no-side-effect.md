---
layout: post
title: "2026-10-26 — Read-only is not a no-side-effect proof"
date: 2026-10-26 05:00:00 +0800
permalink: /2026/10/26/ai-security-case-study-read-only-is-not-no-side-effect/
takeaway: "Treat semantic tool labels as policy inputs: derive the permission class from the strongest reachable side effect."
categories: [case-study, ai-security]
tags: [case-study, agent-tools, authorization, side-effects, permission-boundary]
---

## Signal

An agent framework can make a correct permission decision from incorrect metadata. If a tool says it is `read-only`, policy may auto-allow it before reaching the branch that writes a file, persists memory, starts a process, performs network I/O, or mutates control state.

The useful review unit is therefore not the label. It is the complete classifier-to-sink chain.

## Threat model

Untrusted or model-visible content can influence tool selection and arguments. The host trusts semantic metadata such as `read-only`, `safe`, or `non-mutating` when deciding whether to prompt, deny execution in a restricted mode, or dispatch automatically.

The boundary fails when a tool carrying a low-risk label has any reachable mutating branch. The concrete impact depends on that branch; this case study does not turn the pattern into a claim about a specific private target or imply code execution without sink-level proof.

## Finding and PR

[Hinotoi-agent/huntpack #9 — detect tool side-effect classification mismatches](https://github.com/Hinotoi-agent/huntpack/pull/9) merged on August 11, 2026.

Merge commit: [`3c9ad7cc6e77f0d8177b80c2acad81f775ed1f5b`](https://github.com/Hinotoi-agent/huntpack/commit/3c9ad7cc6e77f0d8177b80c2acad81f775ed1f5b).

Changed files:

- `huntpack/huntpack.py`
- `tests/test_candidate_contract.py`
- `README.md`

The PR added the `tool-semantic-side-effect-mismatch` hunt family. It correlates four signal kinds that are weak in isolation but useful together: a semantic classifier, a permission decision, a tool-dispatch path, and a concrete side-effect sink.

This PR is a review-method improvement, not a remediation for a vulnerability in Huntpack. Its finding is the recurring policy mismatch that Huntpack should rank for targeted validation.

## Exploit path

```text
untrusted or model-visible input
  -> agent selects a tool and supplies arguments
  -> semantic classifier reports read-only / safe / non-mutating
  -> permission policy auto-allows or bypasses restricted-mode denial
  -> dispatcher invokes the implementation
  -> a reachable branch writes, deletes, persists, fetches, spawns, or mutates
```

The classification becomes security-relevant only because policy consumes it. A mutating function elsewhere in the repository is not enough; review must prove that the labeled tool can reach that function through the real dispatch path and under the affected permission mode.

## Mitigation

Classify a tool by its strongest reachable side effect, not its common path or display name. A tool that sometimes mutates should enter the mutating permission lane for the arguments that enable that branch. If argument-sensitive classification is too fragile, use the stricter class for the whole tool.

Keep enforcement in the canonical permission primitive and preserve intentional compatibility explicitly. Restricted or plan modes should deny before the sink. A genuinely read-only operation should remain usable as a positive control.

Huntpack's mitigation is narrower: it raises this source-to-sink shape as a candidate family and emits a proof recipe. It does not decide that every regex match is a vulnerability.

## Verification

The merged regression `test_tool_semantic_family_connects_classifier_policy_and_mutation_sink` constructs a synthetic line containing:

```text
tool.is_read_only(args) -> permission.allow() -> execute_tool(tool_call) -> memory.save()
```

It verifies that the family recognizes all four signal kinds, includes `is_read_only` in duplicate-search terms, records the strongest reachable side effect as the invariant, and asks for both a restricted/plan-mode denial proof and a genuinely read-only success control.

For this publication, the merge commit was checked out and validated directly:

```sh
python3 -m py_compile huntpack/huntpack.py
python3 -m pytest -q tests/test_candidate_contract.py
python3 huntpack/huntpack.py --help
```

Result: `5 passed in 0.02s`; compilation and CLI help also completed successfully.

That regression proves detector construction and output semantics. It does not prove a vulnerable product path. A target-level proof must still invoke the real registry, classifier, permission decision, dispatcher, and harmless sink; then assert both denial and absence of file, memory, network, process, or control-state side effects. The positive control must show that intended read-only behavior still works.

## What was learned

Metadata becomes authority when policy acts on it. Reviewing the policy function without reviewing how the label is produced misses one side of the boundary; reviewing the tool implementation without tracing the real permission consumer misses the other.

Detection should preserve uncertainty. Correlating classifier, policy, dispatch, and sink is a candidate-generation technique. Promotion requires a real source-to-sink path, a lower-trust actor, and sink-shaped evidence.

## Repeat next time

- Inventory semantic labels consumed by agent, MCP, plugin, and workflow permission systems.
- Trace each label through the real registry and dispatcher to every reachable branch.
- Derive the permission class from the strongest side effect.
- In restricted modes, assert denial before the sink and absence of all side effects.
- Add a genuinely read-only success control so hardening does not disable intended behavior.
- Keep candidates private until duplicate, actor-boundary, runtime, and evidence gates pass.

## Vault redirect

The durable rule already lives in the vault takeaway **Boundary claims must be enforced at the action sink**: map `model-visible input -> tool selection -> semantic classifier -> permission decision -> action sink`. This public post adds no target-specific claim; it routes the detector's evidence limits and positive-control requirement back to that existing review rule.