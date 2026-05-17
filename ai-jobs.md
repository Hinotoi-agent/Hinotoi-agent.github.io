---
layout: page
title: AI job search
permalink: /ai-jobs/
---

{% assign job_feed = site.data.ai_jobs %}
{% assign jobs = job_feed.jobs %}

<p class="page-lede">Singapore-focused AI job search for security-adjacent roles: AI-security, LLM-security, penetration testing, red-team, AppSec, product-security, trust/safety, and adjacent security engineering. The weekly refresh keeps only the top 10 matches after location checks, relevance scoring, CV-fit weighting, and noise filtering.</p>

<div class="jobs-meta-card">
  <div>
    <strong>Location filter:</strong> {{ job_feed.location_filter | default: "Singapore" }}
  </div>
  <div>
    <strong>Last refreshed:</strong> {{ job_feed.updated_at | default: "pending first refresh" }}
  </div>
  <p>{{ job_feed.source_note }}</p>
  {% if job_feed.search_behavior %}
    <p><strong>Search behavior:</strong> {{ job_feed.search_behavior }}</p>
  {% endif %}
  {% if job_feed.minimum_score %}
    <p><strong>Publishing threshold:</strong> final score {{ job_feed.minimum_score }}+ before top-10 ranking.</p>
  {% endif %}
</div>

{% if jobs and jobs.size > 0 %}
  <section class="jobs-score-model" aria-label="Ranking model">
    <h2>How the top 10 is ranked</h2>
    <div class="score-model-grid">
      <div><strong>45%</strong><span>CV fit</span></div>
      <div><strong>25%</strong><span>AI/security relevance</span></div>
      <div><strong>15%</strong><span>Seniority/upside</span></div>
      <div><strong>10%</strong><span>Singapore/location fit</span></div>
      <div><strong>5%</strong><span>Freshness</span></div>
    </div>
    <p>Generic sales, junior-only, compliance-heavy, or non-technical matches are penalized before the top 10 is selected. The search intentionally prefers Singapore or remote-Singapore roles where AI/LLM/security terms appear in the title, description, or structured job metadata.</p>
  </section>

  <section class="jobs-category-panel" aria-label="Best matches by role type">
    <h2>Best matches by category</h2>
    <div class="jobs-category-grid">
      {% assign category_labels = "Best AI-security role|Best pentest/red-team role|Best product/AppSec role|Best research role|Best leadership role" | split: "|" %}
      {% for category in category_labels %}
        {% assign selected_job = nil %}
        {% for job in jobs %}
          {% if selected_job == nil and job.categories contains category %}
            {% assign selected_job = job %}
          {% endif %}
        {% endfor %}
        {% if selected_job %}
          <a class="job-category-card" href="{{ selected_job.url }}">
            <span>{{ category }}</span>
            <strong>{{ selected_job.title }}</strong>
            <small>{{ selected_job.company }}</small>
          </a>
        {% endif %}
      {% endfor %}
    </div>
  </section>

  <div class="jobs-list">
    {% for job in jobs %}
      <article class="job-card">
        <div class="job-card-topline">
          <span>{{ job.source }}</span>
          {% if job.published_at %}<time>{{ job.published_at }}</time>{% endif %}
        </div>
        <div class="job-rank-row">
          <span class="job-rank">#{{ forloop.index }}</span>
          <span class="job-score">Fit score {{ job.score }}/100</span>
          {% if job.priority %}<span class="job-priority job-priority-{{ job.priority | downcase | replace: ' ', '-' }}">{{ job.priority }} priority</span>{% endif %}
        </div>
        <h2><a href="{{ job.url }}">{{ job.title }}</a></h2>
        <div class="job-company">{{ job.company }} · {{ job.location }}</div>

        {% if job.categories and job.categories.size > 0 %}
          <div class="job-category-badges">
            {% for category in job.categories %}
              <span>{{ category }}</span>
            {% endfor %}
          </div>
        {% endif %}

        {% if job.fit and job.fit.size > 0 %}
          <div class="job-fit"><strong>CV fit:</strong> {{ job.fit | join: ", " }}</div>
        {% endif %}

        {% if job.why_match %}
          <p class="job-why"><strong>Why this matches:</strong> {{ job.why_match }}</p>
        {% endif %}

        {% if job.possible_gap %}
          <p class="job-gap"><strong>Possible gap to check:</strong> {{ job.possible_gap }}</p>
        {% endif %}

        {% if job.score_breakdown %}
          <div class="job-score-breakdown" aria-label="Score breakdown">
            <span>CV {{ job.score_breakdown.cv_fit }}</span>
            <span>AI/sec {{ job.score_breakdown.ai_security }}</span>
            <span>Upside {{ job.score_breakdown.career_upside }}</span>
            <span>Fresh {{ job.score_breakdown.freshness }}</span>
          </div>
        {% endif %}

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
    <h2>No Singapore AI job search matches found in this refresh.</h2>
    <p>The weekly scanner will try again next Monday. The feed is intentionally strict: roles must match Singapore / Remote-Singapore plus AI-security, LLM-security, penetration testing, red-team, AppSec, product-security, trust/safety, or related security-engineering signals.</p>
  </div>
{% endif %}
