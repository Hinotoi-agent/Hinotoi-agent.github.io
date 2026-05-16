---
layout: page
title: Singapore AI Jobs
permalink: /ai-jobs/
---

{% assign job_feed = site.data.ai_jobs %}
{% assign jobs = job_feed.jobs %}

<p class="page-lede">Weekly Singapore-focused scan for AI, LLM, AI-security, product-security, trust/safety, and adjacent engineering roles.</p>

<div class="jobs-meta-card">
  <div>
    <strong>Location filter:</strong> {{ job_feed.location_filter | default: "Singapore" }}
  </div>
  <div>
    <strong>Last refreshed:</strong> {{ job_feed.updated_at | default: "pending first refresh" }}
  </div>
  <p>{{ job_feed.source_note }}</p>
</div>

{% if jobs and jobs.size > 0 %}
  <div class="jobs-list">
    {% for job in jobs %}
      <article class="job-card">
        <div class="job-card-topline">
          <span>{{ job.source }}</span>
          {% if job.published_at %}<time>{{ job.published_at }}</time>{% endif %}
        </div>
        <h2><a href="{{ job.url }}">{{ job.title }}</a></h2>
        <div class="job-company">{{ job.company }} · {{ job.location }}</div>
        <p>{{ job.summary }}</p>
        {% if job.tags and job.tags.size > 0 %}
          <div class="job-tags">
            {% for tag in job.tags limit:6 %}
              <span>{{ tag }}</span>
            {% endfor %}
          </div>
        {% endif %}
      </article>
    {% endfor %}
  </div>
{% else %}
  <div class="jobs-empty">
    <h2>No Singapore AI/security roles found in this refresh.</h2>
    <p>The weekly scanner will try again next Monday. The feed is intentionally strict: roles must match Singapore / Remote-Singapore plus AI, LLM, security, trust/safety, or related engineering signals.</p>
  </div>
{% endif %}
