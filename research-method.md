---
layout: page
title: Research Method
permalink: /research-method/
---

This site is the public synthesis layer. The working system is the OSS Vulnerability Research Vault, where sources, cases, takeaways, workflows, and checklist changes compound over time.

## The loop

```text
external source / OSS target / maintainer feedback
  -> vault source note
  -> case or finding note
  -> takeaway
  -> checklist or workflow change
  -> public observation
  -> reverse-routed vault lesson if the public post creates a new reusable rule
```

## Operating sequence

1. **Select a signal.** Start from a target, advisory, merged PR, maintainer comment, external article, or repeated failure pattern.
2. **Bound the claim.** Identify the trust boundary, attacker-controlled input, transformation path, and damaging sink.
3. **Check for duplicates.** Search vault notes, open/closed GitHub PRs/issues, advisories, changelogs, and recent commits.
4. **Confirm reproducibility.** Prefer a local repro, regression test, code-path proof, detached worktree, or static validation when runtime is unavailable.
5. **Run improvement loops.** Expand siblings/variants, harden proof shape, and refine the smallest safe patch.
6. **Ship or disclose.** Use the maintainer-friendly evidence shape: affected code, root cause, impact, safe repro, fix rationale, and tests.
7. **Learn back into the vault.** Update lessons, takeaways, checklists, source notes, disclosure trackers, or target notes.
8. **Publish clean synthesis.** The blog post should explain the reusable observation, not dump private notes or unready claims.

## Evidence standard

Good evidence separates:

- what input is attacker-controlled,
- what privilege or authority the sink has,
- what default behavior is unsafe,
- what compatibility path remains,
- what regression proves the fix,
- and what changed in the review method.

## What not to publish

- secrets, tokens, private reports, or uncoordinated exploit details,
- speculative severity beyond the evidence,
- vendor text copied verbatim,
- raw vault dumps,
- or ambiguous claims that have not passed duplicate and repro checks.
