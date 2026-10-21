---
layout: post
title: "2026-10-21 — Approval is not an identity upgrade"
date: 2026-10-21 23:59:00 +0800
permalink: /2026/10/21/approval-is-not-an-identity-upgrade/
takeaway: "An approval marker may suppress another prompt; it must not erase the original caller's scope."
categories: [daily, ai-security]
tags: [approval, caller-context, agent-security, trust-boundaries, vault-backed-learning]
---

## Signal

The useful question after an approval click is not only whether execution resumed. It is which actor the resumed action represents.

This quiet-day entry revisits the existing vault rule for approval replay: authorize the requested action without silently upgrading its caller. It is a review-method recap, not a new finding.

## Merged PRs

None in this window.

Window: `[2026-10-21T00:00:00+08:00, 2026-10-22T00:00:00+08:00)`.

## What shipped or moved

No new code shipment or same-day vault change was established for this window. This publication is a compact synthesis of retained approval-review guidance, not a claim that a new fix or validation run occurred. The recent merged-PR check found no missing entries in the archive, so its data stays unchanged.

## Observed pattern

Map the handoff as request → pending approval record → serialization → replay dispatcher → scope check → action sink.

The command text can survive that chain while caller, session, group, or tenant context disappears. A review should inspect those fields separately. An internal `approved` marker may prevent a prompt loop; it should not stand in for the identity evidence that downstream policy needs.

This is a candidate shape, not proof of a vulnerability. Establish the lower-trust requester, the documented authority model, and the actual change in effective scope before making an impact claim.

## External reference

The [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) calls for server-side enforcement, controlled transaction state transitions, and an authorization check at execution. Those are useful design anchors for reviewing an approval handoff.

The application to agent replay here is the vault's review heuristic: trace the original caller through the handoff rather than treating approval as blanket authority.

## What was learned

Review the pending-work record as identity-bearing state, not just a saved command. Compare what the initial dispatcher knows with what the replay dispatcher receives. Missing context deserves an explicit explanation, especially when a compatibility fallback assumes a host-originated request.

The test should observe the policy decision and the sensitive operation. A resumed command returning an error does not establish that it retained the right identity or avoided earlier side effects.

## Takeaways

- **Approval is not an identity upgrade.** Preserve the original caller and relevant scope across serialization and replay.
- Keep loop prevention separate from authorization. A replay marker should skip redundant prompting, not ordinary scope checks.
- Judge compatibility branches against the documented trust model; do not label every host-originated fallback an exploit without a lower-trust path to it.

## Repeat next time

1. List the identity and scope fields consumed by the action's policy checks.
2. Follow each field through the pending-approval schema and replay entry point.
3. In an isolated regression harness, approve a lower-trust request and verify that an out-of-scope action remains denied without sink-side mutation.
4. Pair it with an allowed request under the same preserved context, plus the intended host-originated compatibility case where applicable.

These are next-review checks, not tests executed during this daily finalization.

## Vault redirect

The canonical rule remains in **Takeaway — Approval replay must preserve original caller context**, including its replay-chain checklist and actor/scope proof contract. The **Source Code Vulnerability Discovery Loop** supplies the denial, side-effect, and positive-control requirements. This post restates those maintained rules; no new finding or duplicate lesson note is needed.
