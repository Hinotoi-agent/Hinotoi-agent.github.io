---
layout: page
title: Reading List
permalink: /reading-list/
---

External sources are used as anchors, not as copy. The point is to extract durable review behavior: new bug classes, proof shapes, defensive patterns, and checklist changes.

<div class="source-list">
{% for source in site.data.reading_sources %}
  <article class="source-card">
    <div class="pr-card-meta">{{ source.category }}</div>
    <h3><a href="{{ source.url }}">{{ source.title }}</a></h3>
    <p>{{ source.use }}</p>
  </article>
{% endfor %}
</div>

## Reading rule

A source is high-signal when it does at least one of these:

- changes a checklist,
- introduces a reusable proof shape,
- clarifies a trust boundary,
- maps to an active AI/OSS target,
- explains a maintainer or advisory outcome,
- or improves how future findings should be written.

Everything else can be bookmarked, but it should not distort the research queue.
