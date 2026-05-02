---
layout: page
title: Merged PRs
permalink: /merged-prs/
---

{% assign prs = site.data.merged_prs %}
{% assign security_prs = prs | where: "category", "security" %}

A straight list of merged pull requests from the security work behind this blog.

<div class="stat-grid stat-grid-small">
  <div class="stat-card"><span>Total PRs</span><strong>{{ prs | size }}</strong></div>
  <div class="stat-card"><span>Security / hardening</span><strong>{{ security_prs | size }}</strong></div>
</div>

<div class="pr-list simple-archive-pr-list">
{% for pr in prs %}
  <article class="pr-card">
    <div class="pr-card-meta">{{ pr.date }} · {{ pr.repo }} #{{ pr.number }} · {{ pr.category | replace: '-', ' ' }}</div>
    <h3><a href="{{ pr.url }}">{{ pr.title }}</a></h3>
  </article>
{% endfor %}
</div>
