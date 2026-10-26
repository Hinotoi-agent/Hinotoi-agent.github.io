---
layout: post
title: "2026-10-26 — Read-only is not a no-side-effect proof"
date: 2026-10-26 05:00:00 +0800
permalink: /2026/10/26/ai-security-case-study-read-only-is-not-no-side-effect/
takeaway: "Treat semantic tool labels as policy inputs: derive the permission class from the strongest reachable side effect."
categories: [field-notes, ai-security]
tags: [agent-tools, authorization, side-effects, permission-boundary]
---

## Signal

An agent framework can make a correct permission decision from incorrect metadata. A tool labeled `read-only` may still have a branch that writes a file, persists memory, starts a process, or changes control state. The review unit is the classifier-to-sink chain, not the label.

This note finalizes October 26, 2026, in Singapore time: midnight inclusive to October 27 midnight exclusive. It is a review-method synthesis, not a newly disclosed vulnerability.

## Merged PRs

None in this window.

## What shipped or moved

The day's vault maintenance refreshed the active research and disclosure dashboards. The existing action-sink takeaway remains the owner of the semantic-classification rule; no new runtime fix is claimed here.

This finalization also narrows the earlier post to a public-safe field note. Private repository references and internal test results are not public evidence anchors. The merged-PR archive needs no new entry for this window.

## Observed pattern

Metadata becomes authority when policy acts on it:

```text
model-visible input -> tool selection -> semantic classifier
  -> permission decision -> dispatcher -> action sink
```

A mutating function somewhere in a repository is not sufficient evidence. Review must establish that the labeled tool reaches that function through the actual dispatch path under the affected permission mode. Network access also needs its own analysis: an operation can avoid local writes while still crossing an egress or credential boundary.

## External reference

The [MCP tool annotation schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-06-18/schema.ts) explicitly treats annotations as hints, not guaranteed descriptions of behavior, and warns clients against making tool-use decisions from annotations supplied by untrusted servers.

The practical consequence is narrow: a `readOnlyHint` is an input to inspect, not independent authorization evidence. Trace who supplies the label and which host decision consumes it.

## What was learned

Reviewing only the permission function misses how its inputs were produced. Reviewing only the tool implementation misses which policy relied on its description. Both ends must be connected before calling the mismatch a security issue.

A detector regression can prove that a candidate pattern is recognized. It cannot prove a vulnerable product path. Target-level validation still needs a lower-trust actor, the real permission and dispatch route, and a harmless observable sink. This post reports no new target-level reproduction or test run.

## Takeaways

- Derive the permission class from the strongest reachable side effect, not the common path or display name.
- If argument-sensitive classification is fragile, use the stricter class for the whole tool.
- Denial evidence must include absence of side effects; an error message alone is insufficient.
- Keep public references independently accessible. Authenticated access to a private repository does not make it a public source.

## Repeat next time

1. Inventory semantic labels consumed by agent, MCP, plugin, and workflow permission systems.
2. Trace each label through the real registry, classifier, permission consumer, and dispatcher.
3. Exercise a harmless mutating branch in the restricted mode and verify denial before file, memory, network, process, or control-state effects.
4. Include a genuinely read-only success control so enforcement preserves intended behavior.
5. Check source visibility before publication; retain private proof details in the research record.

## Vault redirect

The canonical rule remains **Boundary claims must be enforced at the action sink**. The publication check routes to **Public observations should route back into the vault**: verify source visibility separately from authenticated access, and do not promote internal validation into public proof. No private target details are needed to preserve either lesson.
