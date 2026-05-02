---
layout: page
title: Selected Work
permalink: /selected-work/
---

Not every merged PR should carry the same visual weight. This page highlights work that best represents the current cybersecurity AI posture: boundary-first, evidence-driven, and biased toward fixes that actually ship.

{% assign security_prs = site.data.merged_prs | where: "category", "security" %}

## Representative security and hardening PRs

<div class="pr-list">
{% for pr in security_prs limit:12 %}
  <article class="pr-card">
    <div class="pr-card-meta">{{ pr.date }} · {{ pr.repo }}</div>
    <h3><a href="{{ pr.url }}">#{{ pr.number }} — {{ pr.title }}</a></h3>
    <p>Boundary class: {% if pr.tags and pr.tags.size > 0 %}{{ pr.tags | join: ', ' }}{% else %}security hardening{% endif %}.</p>
  </article>
{% endfor %}
</div>

## Why these matter

The shared pattern is AI/security boundary work: paths, URLs, local services, control-plane routes, uploads, logs, and tool outputs become dangerous when later code trusts them more than the original boundary allowed.

## Repeat next time

- Check the sink, not just the caller intent.
- Keep disclosure units aligned to the broken invariant.
- Add regression coverage on the route that actually carried the risk.
- Prefer small patches that preserve compatibility while tightening the default boundary.
