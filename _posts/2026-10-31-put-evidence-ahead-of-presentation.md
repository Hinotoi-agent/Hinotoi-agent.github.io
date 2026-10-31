---
layout: post
title: "2026-10-31 — Put evidence ahead of presentation"
date: 2026-10-31 23:59:00 +0800
permalink: /2026/10/31/put-evidence-ahead-of-presentation/
takeaway: "A security profile can have a strong visual identity, but its claims should lead quickly to independently navigable public evidence."
categories: [daily, ai-security]
tags: [evidence, security-communication, provenance, accessibility, vault-backed-learning]
---

## Signal

The closed Singapore-time window contained no authored PR merge and no target-window Markdown movement in the canonical research vault. The public site did move: its profile was reorganized so open evidence appears before the longer career narrative, while decorative motion was moved onto a route that does not cross readable content.

This is publication architecture, not a new finding, disclosure, or security shipment.

## Merged PRs

None in this window.

Window: `[2026-10-31T00:00:00+08:00, 2026-11-01T00:00:00+08:00)`.

## What shipped or moved

The profile now puts verifiable work near the start of the page:

- merged-PR and security/hardening counts are derived from the site's maintained data rather than copied into prose;
- the evidence section links to the merged-PR archive, selected work, four public CVE records, and one product advisory;
- the AI-assisted testing claim is explicitly bounded to selected internal trials and keeps human validation in the statement;
- canonical, social, and `ProfilePage` metadata make the page identity clearer outside the visual layout;
- mobile navigation, collapsible secondary material, and reduced-motion behavior keep the primary evidence path usable across presentation modes;
- the travelling decorative element now has a dedicated track instead of competing with profile content.

`_data/merged_prs.yml` remains unchanged because no new merge belongs to the target window.

## Observed pattern

Visual identity can attract attention, but it cannot establish a security claim:

```text
security claim -> public evidence link -> independently inspectable record
visual persona  -> context and attention, not proof
```

The same separation matters in AI-assisted security work. A polished model summary, severity label, dashboard card, or profile statistic is a presentation layer. Authority still comes from the underlying PR, advisory, CVE record, reproduction, or regression proof. The interface should shorten the path to that evidence rather than asking readers to trust the interface itself.

## External reference

The OWASP [Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html) recommends enough detail for a vulnerability to be understood and reproduced, supporting evidence, impact, and appropriate references. That guidance is written for disclosure reports, not personal profiles, but its evidence-ordering principle transfers cleanly: security communication should let another person inspect the basis of a claim.

## What was learned

A distinctive profile and an evidence-first profile are compatible. The useful boundary is structural: public records and bounded claims come first; biography, metaphor, and motion remain supporting context. When a decorative layer can obscure text or controls, it has crossed from presentation into interference and should be isolated or removed.

This also keeps activity accounting honest. A profile redesign can improve how existing security work is inspected without becoming a new merge, finding, or disclosure event.

## Takeaways

- **Put inspectable evidence before persona.** A security-facing profile should lead quickly to PRs, advisories, CVEs, and selected work.
- Derive public counts from maintained data, and link the numbers to the records they summarize.
- Bound AI-assisted performance claims to the measured context and retain the human-validation condition.
- Treat presentation improvements as publication movement, not as new security research events.

## Repeat next time

1. Separate target-window research events from changes to the public presentation shell.
2. For each prominent security claim, provide a direct path to an independently inspectable record.
3. Derive counts from the canonical data file instead of duplicating them in page copy.
4. Keep trial metrics scoped by task, comparison, and validation conditions.
5. Test mobile navigation, reduced-motion behavior, and decorative layers against the primary evidence path.

## Vault redirect

The reusable rule routes to **Takeaway — Public observations should route back into the vault** under a new public-evidence-before-presentation update. It changes how the public synthesis layer should order and label claims; it does not add a vulnerability-review checklist item or turn the profile refinement into a security event.