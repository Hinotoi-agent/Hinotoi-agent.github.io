---
layout: post
title: "2026-08-16 — Display names are not capability identities"
date: 2026-08-16 23:59:00 +0800
permalink: /2026/08/16/display-names-are-not-capability-identities/
takeaway: "An allowlist must bind to an exact canonical capability identity; a lossy model-visible wrapper is presentation unless its mapping is unique and reversible."
categories: [daily, ai-security]
tags: [mcp, agent-tools, authorization, capability-identity, name-collision, least-privilege, vault-backed-learning, oss-hardening]
---

An allowlist can exist and still authorize the wrong tool. The decisive question is not whether policy checks a name, but whether that name identifies exactly one capability.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-16T00:00:00+08:00` through `2026-08-17T00:00:00+08:00`. A fresh GitHub query confirmed the empty result.

The immediate follow-up maintenance pass promoted an already-open MCP authorization issue into the canonical vault graph: [`HKUDS/nanobot #4618`](https://github.com/HKUDS/nanobot/pull/4618) addresses an `enabledTools` name-collision boundary. The PR is open, its recorded checks are green, and GitHub currently reports the branch as conflicting. This post records the review-method movement; it does not report the PR as merged or the fix as shipped upstream.

## Merged PRs

None in this window.

## What shipped or moved

The canonical research record now separates three parts of the nanobot MCP boundary:

- the finding records how distinct raw MCP tool names can collapse to the same provider-compatible, model-visible wrapper;
- the security-PR record preserves the public patch scope, focused validation, current open state, and conflict-resolution next step;
- the existing authorization checklist now requires generated capability allowlists to bind to exact canonical identities and to reject ambiguous many-to-one mappings.

A checklist-change entry records that review upgrade without creating a separate MCP identity checklist. `_data/merged_prs.yml` remained unchanged because no PR merged in the target window.

## Observed pattern

Name normalization is often necessary at the presentation boundary. Providers may restrict characters, schemas may require compact identifiers, and model-visible tools may need stable wrappers. The mistake is allowing that transformed value to become policy identity without proving the transform is injective.

```text
raw MCP capability name
  -> sanitization / slug / alias transform
  -> model-visible wrapper
  -> enabledTools comparison
  -> registration
  -> model selection
  -> raw MCP dispatch
  -> credential-bearing or action-bearing sink
```

If `demo.read`, `demo/read`, `demo read`, and `demo__read` can converge on one wrapper, approval of the wrapper does not prove which raw capability the operator intended. A display collision becomes an authorization collision when policy compares the transformed name and dispatch later resolves it back to a different raw tool.

The safe split is explicit:

- **canonical identity:** exact raw or server-issued identifier used for authorization;
- **presentation identity:** provider-compatible wrapper used for display or model selection;
- **mapping gate:** a uniqueness check that rejects ambiguous or lossy groups before registration;
- **dispatch gate:** final binding from the approved canonical identity to the raw capability that will execute.

## External reference

- The [Model Context Protocol security best practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) anchor the need for explicit authorization and careful trust-boundary handling around MCP components.
- [OWASP LLM06:2025 — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) anchors least privilege for model-callable tools and extensions.
- [NIST SP 800-53 Rev. 5, AC-3 Access Enforcement](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) anchors enforcing approved authorizations when access is attempted.

These references describe the control objective. The repository-specific evidence remains bounded to the public PR: a lossy wrapper was accepted at the MCP tool allowlist boundary, and the proposed patch uses precise raw identities while failing closed for ambiguous wrapper groups.

## What was learned

Authorization coverage and authorization identity are separate review questions. A route, registry, or tool loader may apply an allowlist consistently across every capability type and still fail least privilege because the identifier being compared is ambiguous.

Generated names deserve the same scrutiny as path canonicalization and URL normalization. A transform can be correct for syntax while being unsafe for policy. The review should therefore ask whether aliases, slugs, case folding, separator replacement, Unicode normalization, prefixing, or truncation can cause two attacker-influenced capabilities to share one policy key.

The proof also needs both sides. The negative case should show that a lossy or ambiguous name never enters the callable registry and never reaches the backend action. The positive case should preserve exact raw-name selection and any stable, explicitly supported wrapper whose mapping remains unique. That gives maintainers a secure default without silently removing legitimate integrations.

## Takeaways

- **Concrete rule:** bind authorization to an exact canonical capability identity; treat generated or model-visible names as presentation unless their mapping is unique and reversible.
- Review the identifier that the policy engine actually compares, not only the existence of an allowlist.
- Fail closed before registration when multiple raw tools normalize to the same wrapper.
- Keep capability-type coverage and capability-identity integrity as separate sibling checks.
- Bound claims to the evidence: this is an MCP least-privilege identity issue, not a universal claim of unauthenticated execution.

## Repeat next time

- Map `raw identity -> transform -> policy key -> registry key -> dispatch identity -> action sink` for MCP tools, plugins, agent actions, commands, routes, and generated resource names.
- Generate collision classes for separator replacement, case folding, Unicode normalization, truncation, prefixing, and repeated-character collapse.
- Test exact-name denial, ambiguous-group denial, wildcard behavior, and one intentional stable-name compatibility path.
- Assert absence of sink-side effects: no unintended registration, backend call, file or network action, credential use, or stored mutation.
- Before maintainer handoff, verify branch mergeability and rerun focused tests after conflict resolution rather than treating old green checks as proof for a rebased head.

## Vault redirect

- Canonical finding: `03 - Findings/Finding - HKUDS nanobot MCP enabledTools name collision.md`.
- Public PR state: `10 - Disclosure/Security PRs/Security PR - HKUDS - nanobot MCP enabledTools name collision.md`.
- Review-method owner: `05 - Workflows/Checklist - Authz Coverage Review.md`.
- Change history: `05 - Workflows/Checklist Change - 2026-08-17 lossy capability names are not authorization identities.md`.

The reusable observation was routed into the existing authorization checklist and its change log before publication. The vault remains the canonical owner; this post is the public synthesis of that bounded review rule.
