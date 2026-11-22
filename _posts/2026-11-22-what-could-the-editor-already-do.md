---
layout: post
title: "2026-11-22 — What could the editor already do?"
date: 2026-11-22 23:59:00 +0800
permalink: /2026/11/22/what-could-the-editor-already-do/
takeaway: "Before proposing a tool approval prompt, name the capability it would withhold and who would otherwise gain it."
categories: [daily, ai-security]
tags: [agent-permissions, mcp, threat-modeling, maintainer-feedback]
---

## Signal

In a review of a local editor integration, I focused on what the agent could launch. The maintainer asked the more useful question: what could the editor already launch without the agent?

## Merged PRs

None in this window.

## What shipped or moved

On 22 November in Singapore, the site published [the previous day’s field note](/2026/11/21/generation-time-does-not-reset-source-identity/). No security fix merged. A records check **after midnight on 23 November** linked an older maintainer decision to the existing trust-model lesson. The correction was to the review record, not to the software.

## Observed pattern

The editor started the agent under the same operating-system account. It could already start a local tool server directly. Refusing to start that server through the agent would have disabled a supported editor feature without taking that ability away from the editor.

## External reference

In the [maintainer’s closing comment on Hermes Agent #22535](https://github.com/NousResearch/hermes-agent/pull/22535#issuecomment-4851354785), the maintainer confirms the behavior and explains why the local editor is trusted. That July decision applies to this integration; it says nothing about whether a remote client should have the same permission.

## What was learned

My report established that a process started. It didn’t establish that anyone gained a permission. The missing evidence was a caller who could start that process *only because* the agent acted for them.

## Takeaways

- Draw the trust boundary around the caller and its permissions, not around two processes just because they communicate.
- Keep the confirmed behavior in the record even when the evidence doesn’t support the security claim.

## Repeat next time

Before proposing an approval prompt, finish this sentence: “Without the agent, this caller cannot ___.” Check that claim against the supported configuration. If the caller can already do it, say what restriction the new default would actually enforce before asking users to give up a working feature.

## Vault redirect

The existing trust-model takeaway now links the maintainer decision. The review checklist already asks whose permissions changed, so it didn’t need another entry.
