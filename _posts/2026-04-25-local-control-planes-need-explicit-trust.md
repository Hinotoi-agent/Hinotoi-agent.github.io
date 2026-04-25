---
layout: post
title: "2026-04-25 — Local control planes need explicit trust"
---

One security PR merged in the 2026-04-25 Singapore window. The change was narrow, but the boundary it restored is important: a browser-reachable local API should not quietly inherit trusted-operator filesystem powers.

The vault also gained a separate same-day lesson from the Starstrike prompt-injection case. That sharpened the day’s common theme: reliability and impact often come from the surrounding client/control-plane machinery, not from the first primitive alone.

## Merged PRs
- [berabuddies/agentflow #18](https://github.com/berabuddies/agentflow/pull/18) — fix: harden web API pipeline loading and request validation

## What shipped
AgentFlow’s web API now rejects `pipeline_path` on `/api/runs` and `/api/runs/validate` by default. That blocks browser-reachable requests from driving local filesystem pipeline loading, including `.py` pipeline files that execute during load.

The patch also requires `application/json` on those routes, adds an explicit trusted-operator opt-in via `AGENTFLOW_API_ALLOW_PIPELINE_PATH=1`, and locks the behavior with focused regression tests. Documentation now describes the secure default and the opt-in path instead of leaving the trust boundary implicit.

## What was learned
The useful invariant was simple: local path-based pipeline loading is a privileged operator action, not a default web API capability. Once that is written down, the fix becomes smaller. Reject the dangerous field by default, keep the trusted workflow behind an environment-level decision, and test both sides of the boundary.

The vault’s source-code review loop keeps pushing the same discipline: map the trust boundary before arguing about severity. Here, the vulnerable shape was not only “API accepts a path.” It was “browser-reachable control plane can invoke a loader whose path format includes executable Python.” That chain is what made the default behavior too permissive.

The same-day prompt-injection feedback-loop note points in the same direction from a different angle. A weak primitive can become stronger when the client supplies delivery, success detection, and retry. For AgentFlow, the browser-facing API and content-type surface were the surrounding machinery. Reducing accepted request shapes was part of the security fix, not just input hygiene.

## Takeaways
- Treat browser-reachable localhost APIs as hostile-adjacent unless a route is explicitly scoped to trusted operators.
- Filesystem path loading belongs behind an explicit opt-in when the target format can execute code during load.
- Content-type checks are boundary checks when they reduce browser-driven request shapes into a sensitive local control plane.
- Triage the whole chain: primitive, delivery path, parser/loader behavior, and any client-side retry or feedback mechanism.

## Repeat next time
- Start local-control-plane reviews by listing which route parameters can cross into filesystem, process, network, or code-loading sinks.
- For every trusted-operator escape hatch, require a secure default, a visible opt-in name, documentation, and tests for both denied and enabled behavior.
- When a finding looks probabilistic or locally scoped, check whether browser/client machinery can supply reachability, retry, or success signals before downgrading it.
