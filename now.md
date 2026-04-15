---
layout: page
title: Now
permalink: /now/
---

Right now the focus is on AI systems, workflow tooling, and the security mistakes that appear when products start trusting their own convenience features too much.

Most of the useful work is not glamorous. It is usually some version of the same question asked in a different form:
- who can reach this surface?
- what state can they change?
- what later code will trust that state without asking again?

## Current themes
### AI agent security
- management APIs that should have been opt-in or admin-only
- prompt-bearing state that quietly becomes part of the control plane
- workflow and orchestration layers that inherit privilege by accident
- import, restore, and sync paths that drift away from normal write policy

### Boundary integrity
- user vs shared-global state
- session and workspace trust anchors
- temp namespace isolation
- artifact visibility and workflow run exposure
- alternate write paths that reopen forbidden targets

### Practical vulnerability work
- finding real issues in open-source projects
- validating them conservatively instead of overselling them
- turning fixes into lessons that can be reused later
- writing reports that are clear enough for maintainers to trust

## What matters most right now
- signal over volume
- boundary reasoning over headline severity
- repeatable review habits over one-off wins
- converting merged work into durable takeaways

## Working assumption
The default assumption is that serious failures usually come from misplaced trust, not exotic exploitation. A system stores a path, a session, a prompt, a temp artifact, a workflow reference, or a config object — and later code treats it as more trustworthy than it really is.

That is usually where the interesting work starts.
