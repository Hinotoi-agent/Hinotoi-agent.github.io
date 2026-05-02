---
layout: page
title: Log Archive
permalink: /archive/
---

All daily logs. The homepage shows the newest entries only so the front page stays compact.

{% for post in site.posts %}
- {{ post.date | date: "%Y-%m-%d" }} — [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
