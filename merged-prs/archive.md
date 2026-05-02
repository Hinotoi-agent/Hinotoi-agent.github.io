---
layout: page
title: Merged PR Archive
permalink: /merged-prs/archive/
---

{% assign prs_by_date = site.data.merged_prs | group_by: "date" %}

This is the complete merged PR archive. The main merged PR page stays short; this page preserves the full record.

<p><a class="archive-link" href="{{ '/merged-prs/' | relative_url }}">← Back to compact PR index</a></p>

{% for day in prs_by_date %}
## {{ day.name }}
{% for pr in day.items %}
- [{{ pr.repo }} #{{ pr.number }}]({{ pr.url }}) — {{ pr.title }} _({{ pr.category | replace: '-', ' ' }})_
{% endfor %}
{% endfor %}
