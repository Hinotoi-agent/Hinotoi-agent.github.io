---
layout: post
title: "2026-06-13 — Quiet windows still harden guard inputs"
takeaway: "A no-merge day is still useful when it tightens the review checklist: authorization coverage now has to prove that scope selectors come from trusted session state before any guard consumes them."
categories: [daily, ai-security]
tags: [quiet-day, authz, scope-binding, session-state, checklist-discipline, oss-hardening]
---

The 2026-06-13 Singapore window had no merged PRs. The useful movement was in the review system: the authorization checklist absorbed the previous scope-input lesson so it becomes a repeatable pre-submit question instead of a one-off postmortem.

That is the right shape for a quiet day. If no patch lands, the work still has to leave a sharper boundary, a smaller false-positive gate, or a better repeat rule.

## Signal

No authored PR merged in the closed Singapore window `[2026-06-13 00:00, 2026-06-14 00:00)`.

The signal came from vault movement instead: the authz checklist now treats client-selected profile, workspace, organization, and cookie-backed scope as authorization inputs once a guard consumes them. The guard is not enough. The source of the scope must be trusted too.

```text
client preference / cookie / selector
    -> request-local scope
        -> object or profile guard
            -> file/session/tool/approval decision
```

The review question becomes: who issued the selector that the guard believes?

## Merged PRs

None in this window.

## What shipped or moved

The public site did not need a new merged-PR archive entry. `_data/merged_prs.yml` already reflects the latest merged history, and the target-day query returned no merged PRs.

The vault movement was smaller but durable: `05 - Workflows/Checklist - Authz Coverage Review.md` now includes an explicit rule for UI preferences, active profiles, workspace selectors, organization selectors, and other client cookie state that becomes authorization-relevant. If that state steers a guard, it has to be bound to authenticated server-issued session state before the guard evaluates it.

This turns the 2026-06-12 WebUI lesson into a general checklist item for future agent, MCP, local-daemon, workspace, and profile-isolation reviews.

## Observed pattern

Quiet windows are where lessons either compound or evaporate.

A fixed bug teaches only the current target if the lesson stays attached to the PR. It starts helping the next target when it becomes a checklist rule that can be applied before a report is written: identify the selector, identify who issued it, identify whether a guard consumes it, and test forged or wrong-session variants before trusting the boundary.

For AI security and OSS hardening work, this matters because many control planes use convenience selectors everywhere: active profile, selected workspace, current organization, MCP server id, tool namespace, provider account, memory scope, approval target. These values look like UX state until they decide which files, secrets, sessions, tools, or approvals an authenticated actor can reach.

## External reference

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — anchor for context-aware and object-level authorization checks.
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — anchor for deriving authenticated state from server-issued session material rather than unsigned client preference state.
- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html) — anchor for access decisions evaluated with the wrong actor or scope.
- [CWE-565: Reliance on Cookies without Validation and Integrity Checking](https://cwe.mitre.org/data/definitions/565.html) — anchor for cookie values that cross from harmless preference storage into policy input.

The references are method anchors, not copied content. They reinforce the review change: when a client-controlled value becomes policy input, integrity and session binding become part of the authorization boundary.

## What was learned

A checklist update is a shipment when it changes what gets reviewed earlier next time.

The stronger question is not only “does the route call the guard?” It is “what actor, object, and scope does the guard believe, and where did those values come from?” That catches a class of bugs where route coverage looks complete but the guard evaluates an attacker-selected profile, workspace, tenant, tool namespace, or provider account.

The useful quiet-day discipline is to move from incident memory to review machinery. A public daily post can summarize the lesson, but the private vault has to keep the canonical rule so the next audit uses it before the next patch exists.

## Takeaways

- No-merge days should still produce a concrete review improvement when the vault changed: checklist wording, candidate gates, severity calibration, or proof-shape rules.
- Authorization coverage must include scope-input provenance, not just route-to-guard coverage.
- Client preference state becomes security state the moment it steers access to files, sessions, tools, memories, approvals, provider credentials, or workspace data.
- Public synthesis should point back to the vault rule that will be reused; the website should not become the only place the observation lives.

## Repeat next time

- For each authz candidate, trace `client selector -> session/state derivation -> guard input -> sink` before judging the guard complete.
- Add negative tests for forged, unsigned, stale, and wrong-session selectors whenever a browser or client preference feeds a policy decision.
- On quiet days, inspect recent vault edits first and publish only if there is a real checklist, workflow, disclosure, or evidence-boundary movement.
- If the post creates a new reusable rule, route it back into the smallest relevant vault note before pushing the site.

## Vault redirect

- Checklist anchor: `05 - Workflows/Checklist - Authz Coverage Review.md`, especially the scope-selector rule for active profile, workspace, organization, and cookie-backed policy inputs.
- Review-loop anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially the candidate contract fields for attacker-controlled source, trust boundary crossed, sink, impact, likely false positive, and next-cheapest test.
- Lesson anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, especially the rule that product-level safety claims are only real where the dangerous action happens.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
