---
layout: page
title: AI Security Patterns
permalink: /ai-security-patterns/
---

This is the evergreen map behind the daily notes: recurring ways AI products, agent frameworks, MCP-style tool systems, and OSS automation cross from data into authority.

The core thesis is simple:

> AI security issues become real when untrusted content crosses into tools, memory, files, credentials, browsers, network calls, or human approval paths.

{% assign themes = site.data.research_themes %}

<div class="pattern-grid">
{% for theme in themes %}
  <article class="pattern-card">
    <div class="pr-card-meta">Pattern</div>
    <h3 id="{{ theme.slug }}">{{ theme.name }}</h3>
    <p>{{ theme.summary }}</p>
    <div class="tag-row">
      {% for tag in theme.tags %}<span class="tag-pill">{{ tag }}</span>{% endfor %}
    </div>
  </article>
{% endfor %}
</div>

## Review questions

- What untrusted object enters the system: prompt, document, URL, path, repo, webhook, model output, memory, or tool response?
- Which component later treats that object as authority?
- Where is the damaging sink: file I/O, HTTP fetch, browser automation, command execution, upload, approval, or stored state mutation?
- Does validation happen at the sink, or only at an earlier caller/config layer?
- Is there a compatibility escape hatch, and is it explicit, narrow, and regression-tested?

## Related daily notes

<div class="post-list">
{% for post in site.posts limit:8 %}
  <a class="post-card" href="{{ post.url | relative_url }}">
    <div class="post-card-date">{{ post.date | date: "%b %-d, %Y" }}</div>
    <div class="post-card-title">{{ post.title }}</div>
    <p class="post-card-summary">{{ post.excerpt | strip_html | strip_newlines | truncate: 180 }}</p>
  </a>
{% endfor %}
</div>
