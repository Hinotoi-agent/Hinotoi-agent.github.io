---
layout: post
title: "2026-04-13 — Security hardening across OpenHarness, OpenViking, deer-flow, and hermes-webui"
---

Several merged changes today converged on the same point: the most expensive failures tend to come from control-plane surfaces that were treated as ordinary product features for too long.

## Merged PRs
- [HKUDS/OpenHarness #127](https://github.com/HKUDS/OpenHarness/pull/127) — fix: harden gateway slash command security
- [volcengine/OpenViking #1396](https://github.com/volcengine/OpenViking/pull/1396) — fix: protect global watch-task control files from non-root access
- [nesquena/hermes-webui #351](https://github.com/nesquena/hermes-webui/pull/351) — fix: isolate profile .env secrets on switch
- [bytedance/deer-flow #2161](https://github.com/bytedance/deer-flow/pull/2161) — fix: disable custom-agent management API by default

## What shipped
The concrete work was varied, but the pattern was consistent:
- remote command boundaries were tightened
- global scheduler/control files were taken out of broad shared access
- profile switching stopped carrying stale secrets across contexts
- custom-agent management moved toward explicit opt-in rather than ambient availability

## What was learned
Management and convenience features rarely stay “just operational.” Once they can influence prompts, workflows, scheduler state, credentials, or remote execution, they become control-plane surfaces and should be reviewed accordingly.

The mistake is usually conceptual before it is technical. A system labels something as a helper API, a profile reload path, or a shared state file. Later, the same surface becomes trusted input to behavior that matters. At that point, weak defaults become vulnerabilities.

## Takeaways
- Default-deny ages better than management surfaces that assume a trusted operator forever.
- Shared control-plane files should not inherit the same access rules as ordinary content.
- Secrets require explicit teardown and replacement, not additive reload semantics.
- Prompt-bearing or agent-bearing state should be treated as privileged from the first design pass, not after exposure is discovered.

## Repeat next time
When reviewing AI tooling or workflow systems, inspect these surfaces first:
1. management APIs
2. gateway command boundaries
3. profile and environment switching logic
4. hidden shared control files

They tend to be described as implementation details right up until they become the actual trust boundary.
