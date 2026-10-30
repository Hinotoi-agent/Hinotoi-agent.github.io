---
layout: page
title: About
permalink: /about/
excerpt: Lennon Chia is a Singapore-based defensive security researcher working on AI security, open-source vulnerability research, and fixes that ship.
---

{% assign merged_prs = site.data.merged_prs %}
{% assign security_prs = merged_prs | where: "category", "security" %}
{% assign repos = merged_prs | group_by: "repo" %}

<section class="about-hero">
  <div class="about-hero-copy">
    <div class="about-kicker">Lennon Chia · Singapore</div>
    <h2>Security research that turns small signals into fixes.</h2>
    <p class="about-lede">I’m a defensive security researcher and open-source contributor focused on AI systems, agent tooling, and the trust boundaries where untrusted content can reach files, credentials, browsers, network calls, or host actions.</p>
    <p>My work sits between vulnerability research and secure engineering: trace the real source-to-sink path, reproduce the issue, check for duplicates, build the smallest safe patch, add regression coverage, and leave maintainers with evidence they can act on.</p>
    <div class="about-actions">
      <a class="button button-primary" href="{{ '/merged-prs/' | relative_url }}">View merged PRs</a>
      <a class="button button-secondary" href="{{ '/selected-work/' | relative_url }}">Selected work</a>
    </div>
  </div>
  <div class="about-portrait-wrap">
    <img class="about-portrait" src="https://avatars.githubusercontent.com/u/275430060?v=4" alt="Lennon Chia’s GitHub avatar">
    <span>Hinotoi-agent</span>
  </div>
</section>

<div class="about-stat-grid" aria-label="Public work indexed on this site">
  <div class="about-stat">
    <strong>{{ merged_prs | size }}</strong>
    <span>Merged PRs indexed</span>
  </div>
  <div class="about-stat">
    <strong>{{ security_prs | size }}</strong>
    <span>Security and hardening PRs</span>
  </div>
  <div class="about-stat">
    <strong>{{ repos | size }}</strong>
    <span>Open-source repositories</span>
  </div>
</div>

## What I do

<div class="about-grid">
  <article class="about-card">
    <div class="about-card-number">01</div>
    <h3>AI and agent security</h3>
    <p>I review AI agents, MCP-style integrations, local control planes, approval flows, memory, uploads, and tool execution—especially when model-controlled or retrieved content can trigger a privileged action.</p>
  </article>
  <article class="about-card">
    <div class="about-card-number">02</div>
    <h3>Open-source vulnerability research</h3>
    <p>I trace attacker-controlled input to consequential sinks, validate the issue in isolation, check advisories and project history for duplicates, and contribute focused fixes with regression tests.</p>
  </article>
  <article class="about-card">
    <div class="about-card-number">03</div>
    <h3>Security tooling and workflows</h3>
    <p>I build repeatable research workflows and public tools such as <a href="https://github.com/Hinotoi-agent/vulnweave">VulnWeave</a>, <a href="https://github.com/Hinotoi-agent/huntpack">Huntpack</a>, and <a href="https://github.com/Hinotoi-agent/Verifymate">Verifymate</a> to structure evidence and reduce review drift.</p>
  </article>
  <article class="about-card">
    <div class="about-card-number">04</div>
    <h3>Field notes that compound</h3>
    <p>I turn shipped fixes, maintainer feedback, and external research into concise public patterns. The goal is not to publish more—it is to make the next review more precise.</p>
  </article>
</div>

## How I work

<div class="about-principles">
  <div><strong>Boundary first</strong><span>Define the actor, controlled input, transformation path, authority, and sink before making an impact claim.</span></div>
  <div><strong>Evidence over drama</strong><span>Prefer a reproducible path and scoped severity over a broad claim the evidence cannot support.</span></div>
  <div><strong>Small patches</strong><span>Preserve compatibility where possible and change only the invariant that is actually broken.</span></div>
  <div><strong>Ship the lesson</strong><span>A useful result includes tests, maintainer-ready context, and a reusable review pattern—not just a report.</span></div>
</div>

## Current focus

- AI-agent and MCP trust boundaries
- prompt and content injection that crosses into tools or host actions
- upload, document-parser, URL-fetch, SSRF, path, and symlink safety
- browser-to-local-service authorization and control-plane hardening
- evidence quality for AI-assisted vulnerability discovery

## Find my work

<div class="about-links">
  <a class="button button-primary" href="https://github.com/Hinotoi-agent" rel="me">GitHub</a>
  <a class="button button-secondary" href="https://www.linkedin.com/in/lennon-chia/" rel="me">LinkedIn</a>
  <a class="button button-secondary" href="{{ '/ai-security-patterns/' | relative_url }}">Security patterns</a>
  <a class="button button-secondary" href="{{ '/research-method/' | relative_url }}">Research method</a>
</div>

This site is my public notebook for work that is ready to share. It records merged contributions and reusable lessons without publishing private research notes, uncoordinated findings, or unsupported claims.
