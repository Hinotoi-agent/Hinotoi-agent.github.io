---
layout: page
title: Now
permalink: /now/
---

## Current focus
Right now the focus is on AI and security, specifically where workflow systems, agent tooling, and control-plane design create silent trust-boundary failures.

## Active themes
### 1. AI agent security
- management APIs that should be opt-in or admin-only
- prompt-bearing control-plane state
- workflow and orchestration surfaces that quietly become privileged
- import, restore, and sync paths that bypass normal write policy

### 2. Boundary integrity
- user vs shared-global state
- session and workspace trust anchors
- temp namespace isolation
- artifact exposure and workflow run visibility
- configuration drift between direct-write and alternate-write paths

### 3. Practical vulnerability work
- finding issues in real open-source projects
- validating them conservatively
- turning fixes into reusable lessons and checklists
- writing reports that are precise, reproducible, and not overstated

## What I am optimizing for
- high-signal findings over inflated severity
- repeatable review heuristics over one-off wins
- tighter reasoning about trust boundaries
- converting merged work into durable takeaways

## Current research posture
The working assumption is simple: most serious failures come from systems trusting something they should only have tolerated conditionally.

So the review focus stays on:
- who can reach a surface
- what state it can read or change
- what later code trusts that state
- whether an alternate path quietly reopens a forbidden target
