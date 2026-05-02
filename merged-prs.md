---
layout: page
title: Merged PRs
permalink: /merged-prs/
---

{% assign prs = site.data.merged_prs %}
{% assign total_prs = prs | size %}
{% assign security_prs = prs | where: "category", "security" %}
{% assign docs_prs = prs | where: "category", "docs-standards" %}
{% assign test_prs = prs | where: "category", "tests-ci" %}
{% assign repos = prs | group_by: "repo" | sort: "name" %}
{% assign categories = prs | group_by: "category" %}
{% assign months = prs | group_by: "month" %}

This page is now an archive, not an endless flat list. The latest work stays visible here; older entries are grouped into monthly, repository, and category paths so the signal does not get buried under volume.

<div class="stat-grid">
  <div class="stat-card"><span>Total merged PRs</span><strong>{{ total_prs }}</strong></div>
  <div class="stat-card"><span>Security / hardening</span><strong>{{ security_prs | size }}</strong></div>
  <div class="stat-card"><span>Docs / standards</span><strong>{{ docs_prs | size }}</strong></div>
  <div class="stat-card"><span>Tests / CI</span><strong>{{ test_prs | size }}</strong></div>
</div>

## Browse

<div class="chip-row">
  <a class="chip" href="{{ '/merged-prs/archive/' | relative_url }}">Full archive</a>
  <a class="chip" href="{{ '/selected-work/' | relative_url }}">Selected work</a>
  {% for month in months %}<a class="chip" href="{{ '/merged-prs/' | append: month.name | append: '/' | relative_url }}">{{ month.name }}</a>{% endfor %}
  {% for group in repos %}<a class="chip" href="#repo-{{ group.name | slugify }}">{{ group.name }}</a>{% endfor %}
</div>

## Latest merged PRs

<div class="pr-list">
{% for pr in prs limit:20 %}
  <article class="pr-card">
    <div class="pr-card-meta">{{ pr.date }} · {{ pr.category | replace: '-', ' ' }}</div>
    <h3><a href="{{ pr.url }}">{{ pr.repo }} #{{ pr.number }}</a></h3>
    <p>{{ pr.title }}</p>
  </article>
{% endfor %}
</div>

<p><a class="archive-link" href="{{ '/merged-prs/archive/' | relative_url }}">Open the full archive →</a></p>

## By repository

{% for group in repos %}
### <span id="repo-{{ group.name | slugify }}">{{ group.name }}</span>
{% assign repo_prs = group.items %}
{% for pr in repo_prs limit:8 %}
- {{ pr.date }} — [#{{ pr.number }}]({{ pr.url }}) — {{ pr.title }}
{% endfor %}
{% if repo_prs.size > 8 %}- _{{ repo_prs.size | minus: 8 }} more in the full archive._{% endif %}
{% endfor %}

## By category

{% for group in categories %}
### {{ group.name | replace: '-', ' ' | capitalize }}
{% for pr in group.items limit:10 %}
- {{ pr.date }} — [{{ pr.repo }} #{{ pr.number }}]({{ pr.url }}) — {{ pr.title }}
{% endfor %}
{% endfor %}
