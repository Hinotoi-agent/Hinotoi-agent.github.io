---
layout: post
title: "2026-04-13 — Security hardening shipped across OpenHarness, OpenViking, deer-flow, and hermes-webui"
---

Today’s merged work concentrated on tightening control-plane boundaries and reducing surprising privilege exposure.

## Merged PRs
- [HKUDS/OpenHarness #127](https://github.com/HKUDS/OpenHarness/pull/127) — fix: harden gateway slash command security
- [volcengine/OpenViking #1396](https://github.com/volcengine/OpenViking/pull/1396) — fix: protect global watch-task control files from non-root access
- [nesquena/hermes-webui #351](https://github.com/nesquena/hermes-webui/pull/351) — fix: isolate profile .env secrets on switch
- [bytedance/deer-flow #2161](https://github.com/bytedance/deer-flow/pull/2161) — fix: disable custom-agent management API by default

## What was learned
A lot of dangerous product behavior hides behind “management” and “convenience” surfaces. Gateway commands, profile switching, shared scheduler files, and custom-agent controls all become security-relevant the moment they cross from private operator intent into shared or remotely reachable state.

## Takeaways
- Default-deny is healthier than feature-rich management APIs that assume trusted deployment.
- Shared control-plane files should not live behind the same access rules as ordinary content.
- Secrets and identity-bearing environment data need explicit lifecycle cleanup, not additive reload behavior.
- If a route changes prompt-bearing or agent-bearing state, treat it like a privileged admin surface from day one.

## Repeat next time
When reviewing AI tooling and automation products, look first at:
1. management APIs
2. gateway command boundaries
3. profile/env switching logic
4. shared hidden control files
