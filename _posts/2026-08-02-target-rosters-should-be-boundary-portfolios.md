---
layout: post
title: "2026-08-02 — Target rosters should be boundary portfolios"
date: 2026-08-02 23:59:00 +0800
permalink: /2026/08/02/target-rosters-should-be-boundary-portfolios/
takeaway: "A target earns scarce review time by exposing a distinct, testable trust boundary with a cheap next proof—not by ranking highly on popularity or keyword density alone."
categories: [daily, ai-security]
tags: [target-selection, agent-security, mcp-security, trust-boundaries, research-operations, vault-backed-learning, oss-hardening]
---

A compact research roster should be a portfolio of testable boundaries. A ranking can find candidates, but it cannot decide which repository deserves the next unit of review time.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-02T00:00:00+08:00` through `2026-08-03T00:00:00+08:00`.

The immediate post-window maintenance pass did produce durable research movement: it refreshed the five-target AI-product roster, promoted three repositories into first-class target notes, and moved three superseded targets into the archive without deleting their reusable scope notes.

## Merged PRs

None in this window.

## What shipped or moved

- The active roster remained capped at five repositories rather than expanding with every high-scoring discovery result.
- Three promoted targets gained explicit maps for agent, MCP, memory, file, network, workflow, tenant, and credential boundaries.
- Each promoted target now has a next-cheapest validation step and an exit condition before broad review begins.
- Public advisory history and repository security-policy fit became first-pass inputs for duplicate risk and disclosure planning.
- Three superseded targets moved to an archive lane; their reusable scope notes were preserved instead of deleted.
- `_data/merged_prs.yml` remained unchanged because both the context seed and a fresh local-window query found no authored merge.

No upstream runtime fix, test change, advisory publication, or new vulnerability claim is represented here.

## Observed pattern

Target discovery and target admission are different decisions:

```text
broad discovery signals
  -> disclosure-policy and prior-art filter
  -> distinct trust-boundary map
  -> bounded candidate contract
  -> next-cheapest proof
  -> active roster or archive
```

Keyword density, stars, recent activity, and product descriptions are useful discovery signals. They do not prove an attacker-controlled source, a reachable sink, a violated invariant, or a practical disclosure path.

The better portfolio question is whether a candidate adds a distinct review surface. For agentic systems that may mean tool-call authorization, MCP exposure, memory namespaces, workspace and symlink containment, model-provider credentials, outbound URL fetches, background jobs, or cross-tenant artifacts. A roster filled with near-identical surfaces creates the appearance of coverage while concentrating the same blind spots.

## External reference

- [OWASP GenAI Security Project](https://genai.owasp.org/) provides public threat-class anchors for LLM and agentic systems. Its value here is not a checklist to copy, but a vocabulary for testing whether a target adds a distinct model, tool, memory, identity, or action boundary.
- [GitHub Docs: Adding a security policy to your repository](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository) anchors the disclosure-policy check. A repository's reporting instructions are part of review planning, not metadata to inspect only after a finding exists.

These references change the method in two places: classify the boundary portfolio before deep review, and confirm the maintainer's reporting route before investing in a proof that cannot be handled safely.

## What was learned

A target score should open a question, not settle it. Before a repository enters the active set, the review record should state:

1. which trust surfaces differ from the current portfolio;
2. which attacker and deployment conditions make them reachable;
3. which public advisories or prior fixes raise duplicate risk;
4. which reporting policy constrains testing and disclosure;
5. which narrow test can kill or strengthen the first candidate cheaply; and
6. which condition will move the target back out of the active set.

This turns target rotation into evidence-budget management. It also reduces broad AI-assisted reading: the agent receives a bounded surface and stop condition instead of an open-ended instruction to “audit the repository.”

## Takeaways

- **Concrete rule:** admit a target only when it adds a distinct, attacker-relevant boundary and has a named next-cheapest test.
- Treat discovery scores as triage signals, never as evidence of vulnerability value.
- Check security-policy fit and advisory history before expensive validation, not after drafting a report.
- Cap the active portfolio so every target retains an explicit hypothesis, proof path, and exit criterion.
- Archive cleanly when the remaining paths are duplicate-covered, trust-model-bounded, or too broad to validate honestly.

## Repeat next time

- Map routes, auth helpers, tool/MCP dispatch, storage roots, network clients, background jobs, and tests before delegating deep review.
- Write one candidate contract with attacker source, boundary, sink, invariant, impact, evidence anchors, duplicate terms, and next-cheapest test.
- Compare the new target's surfaces with the current roster; reject redundant breadth unless a concrete sibling variant justifies it.
- Read `SECURITY.md` and public advisories before runtime testing so scope and disclosure constraints shape the proof.
- Remove a target from the active set when no bounded non-duplicate candidate or maintainer action remains; preserve the reusable map in the archive.

## Vault redirect

- Canonical roster and movement record: `02 - Targets/Roster/AI Target Roster.md`, the three promoted target notes, and `98 - System/Vault Maintenance.md`.
- Canonical review method: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially family-first ranking, candidate contracts, and next-cheapest tests.
- Reverse-routed observation: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`, under the `2026-08-02 boundary-portfolio target selection update`.
- The vault owns target identities, private research state, and validation decisions. This post publishes only the generic portfolio rule.
