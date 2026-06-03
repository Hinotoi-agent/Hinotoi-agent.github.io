---
layout: page
title: AI job search
permalink: /ai-jobs/
---

{% assign job_feed = site.data.ai_jobs %}
{% assign jobs = job_feed.jobs %}
{% assign alerts = job_feed.alerts %}

<p class="page-lede">Singapore-focused AI job search for security-adjacent roles: AI-security, LLM-security, penetration testing, red-team, AppSec, application-security management, product-security, trust/safety, vulnerability research, and adjacent security engineering. The weekly refresh now tracks new/still-open roles, checks more ATS sources, and lets you filter the ranked list directly on this page.</p>

<div class="jobs-meta-card">
  <div class="jobs-meta-grid">
    <div><strong>Location filter:</strong> {{ job_feed.location_filter | default: "Singapore" }}</div>
    <div><strong>Last refreshed:</strong> {{ job_feed.updated_at | default: "pending first refresh" }}</div>
    {% if job_feed.stats %}
      <div><strong>Candidates scored:</strong> {{ job_feed.stats.candidates_scored }}</div>
      <div><strong>Published:</strong> top {{ job_feed.stats.published_count }}</div>
    {% endif %}
  </div>
  <p>{{ job_feed.source_note }}</p>
  {% if job_feed.search_behavior %}<p><strong>Search behavior:</strong> {{ job_feed.search_behavior }}</p>{% endif %}
  {% if job_feed.minimum_score %}<p><strong>Publishing threshold:</strong> final score {{ job_feed.minimum_score }}+ before top-10 ranking.</p>{% endif %}
</div>

{% if alerts and alerts.size > 0 %}
  <section class="jobs-alert-panel" aria-label="High priority alerts">
    <h2>Apply-now alerts</h2>
    <p>New or very high-signal roles from the wider candidate pool, not just the final top 10.</p>
    <div class="jobs-alert-grid">
      {% for job in alerts limit:6 %}
        <a class="job-alert-card" href="{{ job.url }}">
          <span>{{ job.alert_reason | default: "high-signal match" }}</span>
          <strong>{{ job.title }}</strong>
          <small>{{ job.company }} · {{ job.score }}/100 · {{ job.status }}</small>
        </a>
      {% endfor %}
    </div>
  </section>
{% endif %}

{% if jobs and jobs.size > 0 %}
  <section class="jobs-score-model" aria-label="Ranking model">
    <h2>How the top 10 is ranked</h2>
    <div class="score-model-grid">
      <div><strong>43%</strong><span>CV fit</span></div>
      <div><strong>27%</strong><span>AI/security relevance</span></div>
      <div><strong>14%</strong><span>Seniority/upside</span></div>
      <div><strong>10%</strong><span>Singapore/location fit</span></div>
      <div><strong>6%</strong><span>Freshness</span></div>
    </div>
    <p>Sales, junior-only, compliance-heavy, SOC-only, or non-technical matches are penalized before the top 10 is selected. The page now exposes score breakdowns so poor matches can be tuned in future refreshes.</p>
  </section>

  <section class="jobs-category-panel" aria-label="Best matches by role type">
    <h2>Best matches by category</h2>
    <div class="jobs-category-grid">
      {% assign category_labels = "Best AI-security role|Best pentest/red-team role|Best product/AppSec role|Best research role|Best incident-response role|Best leadership role" | split: "|" %}
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

  <section class="jobs-controls" aria-label="Job filters">
    <div>
      <label for="job-search-input">Search</label>
      <input id="job-search-input" type="search" placeholder="title, company, AI, AppSec…" data-job-search>
    </div>
    <div>
      <label for="job-category-filter">Category</label>
      <select id="job-category-filter" data-job-category>
        <option value="all">All categories</option>
        <option value="Best AI-security role">AI security</option>
        <option value="Best pentest/red-team role">Pentest / red team</option>
        <option value="Best product/AppSec role">Product / AppSec</option>
        <option value="Best research role">Research</option>
        <option value="Best incident-response role">Incident response</option>
        <option value="Best leadership role">Leadership</option>
      </select>
    </div>
    <div>
      <label for="job-priority-filter">Priority</label>
      <select id="job-priority-filter" data-job-priority>
        <option value="all">All priorities</option>
        <option value="High">High</option>
        <option value="Medium-high">Medium-high</option>
        <option value="Medium">Medium</option>
        <option value="Watchlist">Watchlist</option>
      </select>
    </div>
    <div>
      <label for="job-source-filter">Source</label>
      <select id="job-source-filter" data-job-source>
        <option value="all">All sources</option>
        <option value="Ashby">Ashby</option>
        <option value="Greenhouse">Greenhouse</option>
        <option value="Lever">Lever</option>
        <option value="MyCareersFuture">MyCareersFuture</option>
        <option value="RemoteOK">RemoteOK</option>
        <option value="Remotive">Remotive</option>
      </select>
    </div>
    <div>
      <label for="job-sort-select">Sort</label>
      <select id="job-sort-select" data-job-sort>
        <option value="rank">Ranked fit</option>
        <option value="freshness">Freshness</option>
        <option value="company">Company</option>
        <option value="score">Score</option>
      </select>
    </div>
    <div class="jobs-filter-count" data-job-count>{{ jobs.size }} shown</div>
  </section>

  <div class="jobs-list" data-jobs-list>
    {% for job in jobs %}
      <article class="job-card" data-job-card data-rank="{{ forloop.index }}" data-score="{{ job.score }}" data-freshness="{{ job.score_breakdown.freshness | default: 0 }}" data-company="{{ job.company | escape }}" data-source="{{ job.source | escape }}" data-priority="{{ job.priority | escape }}" data-category="{{ job.categories | join: '|' | escape }}" data-status="{{ job.status | escape }}" data-search="{{ job.title | append: ' ' | append: job.company | append: ' ' | append: job.location | append: ' ' | append: job.summary | append: ' ' | append: job.tags | join: ' ' | downcase | escape }}">
        <div class="job-card-topline">
          <span>{{ job.source }}</span>
          {% if job.published_at %}<time>{{ job.published_at }}</time>{% endif %}
          {% if job.status_badge %}<span class="job-status job-status-{{ job.status_badge | downcase | replace: ' ', '-' }}">{{ job.status_badge }}</span>{% elsif job.status %}<span class="job-status job-status-{{ job.status | downcase | replace: ' ', '-' }}">{{ job.status }}</span>{% endif %}
        </div>
        <div class="job-rank-row">
          <span class="job-rank">#{{ forloop.index }}</span>
          <span class="job-score">Fit score {{ job.score }}/100</span>
          {% if job.priority %}<span class="job-priority job-priority-{{ job.priority | downcase | replace: ' ', '-' }}">{{ job.priority }} priority</span>{% endif %}
          {% if job.seniority %}<span class="job-seniority">{{ job.seniority }}</span>{% endif %}
        </div>
        <h2><a href="{{ job.url }}">{{ job.title }}</a></h2>
        <div class="job-company">{{ job.company }} · {{ job.location }}</div>
        {% if job.salary_estimate %}<div class="job-salary"><strong>Salary:</strong> {{ job.salary_estimate }}</div>{% endif %}

        {% if job.categories and job.categories.size > 0 %}
          <div class="job-category-badges">
            {% for category in job.categories %}<span>{{ category }}</span>{% endfor %}
          </div>
        {% endif %}

        {% if job.fit and job.fit.size > 0 %}<div class="job-fit"><strong>CV fit:</strong> {{ job.fit | join: ", " }}</div>{% endif %}
        {% if job.why_match %}<p class="job-why"><strong>Why this matches:</strong> {{ job.why_match }}</p>{% endif %}

        {% if job.next_action or job.apply_angle %}
          <div class="job-action-plan">
            <div class="job-action-plan-heading">
              <span>Action plan</span>
              {% if job.status_badge %}<strong>{{ job.status_badge }}</strong>{% endif %}
            </div>
            {% if job.next_action %}<p><strong>Next action:</strong> {{ job.next_action }}</p>{% endif %}
            {% if job.apply_angle %}<p><strong>Best application angle:</strong> {{ job.apply_angle }}</p>{% endif %}
          </div>
        {% elsif job.apply_angle %}
          <p class="job-angle"><strong>Best application angle:</strong> {{ job.apply_angle }}</p>
        {% endif %}
        {% if job.possible_gap %}<p class="job-gap"><strong>Possible gap to check:</strong> {{ job.possible_gap }}</p>{% endif %}

        {% if job.skillsets_to_build or job.learning_gaps or job.certifications_to_consider %}
          <div class="job-learning-plan">
            <div class="job-learning-heading">Relevance plan</div>
            {% if job.skillsets_to_build and job.skillsets_to_build.size > 0 %}
              <div>
                <strong>Skillsets to build:</strong>
                <ul>{% for skill in job.skillsets_to_build %}<li>{{ skill }}</li>{% endfor %}</ul>
              </div>
            {% endif %}
            {% if job.certifications_to_consider and job.certifications_to_consider.size > 0 %}
              <div>
                <strong>Certs / courses to consider:</strong>
                <ul>{% for cert in job.certifications_to_consider %}<li>{{ cert }}</li>{% endfor %}</ul>
              </div>
            {% endif %}
            {% if job.learning_gaps and job.learning_gaps.size > 0 %}
              <div>
                <strong>Learning gaps to close:</strong>
                <ul>{% for gap in job.learning_gaps %}<li>{{ gap }}</li>{% endfor %}</ul>
              </div>
            {% endif %}
          </div>
        {% endif %}

        {% if job.score_breakdown %}
          <details class="job-score-breakdown">
            <summary>Score breakdown</summary>
            <div>
              <span>CV {{ job.score_breakdown.cv_fit }}</span>
              <span>AI/sec {{ job.score_breakdown.ai_security }}</span>
              <span>Upside {{ job.score_breakdown.career_upside }}</span>
              <span>Location {{ job.score_breakdown.location_fit }}</span>
              <span>Fresh {{ job.score_breakdown.freshness }}</span>
              <span>Noise -{{ job.score_breakdown.noise_penalty }}</span>
            </div>
          </details>
        {% endif %}

        <p>{{ job.summary }}</p>
        {% if job.tags and job.tags.size > 0 %}
          <div class="job-tags">{% for tag in job.tags limit:7 %}<span>{{ tag }}</span>{% endfor %}</div>
        {% endif %}
      </article>
    {% endfor %}
  </div>
{% else %}
  <div class="jobs-empty">
    <h2>No Singapore AI job search matches found in this refresh.</h2>
    <p>The weekly scanner will try again next Monday. The feed is intentionally strict: roles must match Singapore / Remote-Singapore / APAC-eligible location metadata plus AI-security, LLM-security, penetration testing, red-team, AppSec, product-security, trust/safety, or related security-engineering signals.</p>
  </div>
{% endif %}

<script>
(function () {
  var list = document.querySelector('[data-jobs-list]');
  if (!list) return;
  var cards = Array.prototype.slice.call(list.querySelectorAll('[data-job-card]'));
  var search = document.querySelector('[data-job-search]');
  var category = document.querySelector('[data-job-category]');
  var priority = document.querySelector('[data-job-priority]');
  var source = document.querySelector('[data-job-source]');
  var sort = document.querySelector('[data-job-sort]');
  var count = document.querySelector('[data-job-count]');

  function value(el, fallback) { return el ? el.value : fallback; }
  function matches(card) {
    var text = value(search, '').toLowerCase().trim();
    var cat = value(category, 'all');
    var pri = value(priority, 'all');
    var src = value(source, 'all');
    if (text && card.dataset.search.indexOf(text) === -1) return false;
    if (cat !== 'all' && card.dataset.category.indexOf(cat) === -1) return false;
    if (pri !== 'all' && card.dataset.priority !== pri) return false;
    if (src !== 'all' && card.dataset.source !== src) return false;
    return true;
  }
  function compare(a, b) {
    var mode = value(sort, 'rank');
    if (mode === 'freshness') return Number(b.dataset.freshness) - Number(a.dataset.freshness) || Number(a.dataset.rank) - Number(b.dataset.rank);
    if (mode === 'company') return a.dataset.company.localeCompare(b.dataset.company) || Number(a.dataset.rank) - Number(b.dataset.rank);
    if (mode === 'score') return Number(b.dataset.score) - Number(a.dataset.score) || Number(a.dataset.rank) - Number(b.dataset.rank);
    return Number(a.dataset.rank) - Number(b.dataset.rank);
  }
  function update() {
    var shown = 0;
    cards.sort(compare).forEach(function (card) {
      var ok = matches(card);
      card.hidden = !ok;
      if (ok) shown += 1;
      list.appendChild(card);
    });
    if (count) count.textContent = shown + ' shown';
  }
  [search, category, priority, source, sort].forEach(function (el) {
    if (el) el.addEventListener('input', update);
    if (el) el.addEventListener('change', update);
  });
  update;
  update();
}());
</script>
