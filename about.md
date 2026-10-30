---
layout: default
title: Lennon Chia — Security Across the Long Journey
permalink: /about/
body_class: portfolio-anime frieren-portfolio
excerpt: Lennon Chia is a Singapore-based cybersecurity manager working across offensive security, AI-assisted penetration testing, agentic controls, and open-source vulnerability research.
---

{% assign merged_prs = site.data.merged_prs %}
{% assign security_prs = merged_prs | where: "category", "security" %}
{% assign repos = merged_prs | group_by: "repo" %}

<a class="anime-skip" href="#profile-main">Skip to profile</a>

<div class="anime-portfolio">
  <nav class="anime-nav" aria-label="Profile navigation">
    <a class="anime-wordmark" href="{{ '/' | relative_url }}" aria-label="Hinotoi home">
      <span class="anime-wordmark-sigil" aria-hidden="true">H</span>
      <span><strong>LENNON CHIA</strong><small>Hinotoi · Security across the long journey</small></span>
    </a>
    <div class="anime-nav-links">
      <a href="#about">About</a>
      <a href="#experience">Journey</a>
      <a href="#operations">Craft</a>
      <a href="#proof">Archive</a>
      <a class="anime-nav-cta" href="https://github.com/Hinotoi-agent" rel="me">GitHub ↗</a>
    </div>
  </nav>

  <main id="profile-main">
    <section class="anime-hero" aria-labelledby="anime-hero-title">
      <div class="anime-grid-glow" aria-hidden="true"></div>
      <div class="anime-memory-motes" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="anime-hero-copy">
        <div class="anime-status"><span aria-hidden="true"></span> A long journey, still in progress · Singapore</div>
        <p class="anime-overline">Security craft · human judgment · responsible AI</p>
        <h1 id="anime-hero-title">Security,<br><em>remembered.</em><br>Judgment, retained.</h1>
        <p class="anime-hero-lede">I lead AI innovation and penetration-testing teams, build human-validated security workflows, and research the trust boundaries where software gains authority.</p>
        <div class="anime-hero-actions">
          <a class="anime-button anime-button-primary" href="#operations">Open the spellbook <span aria-hidden="true">↘</span></a>
          <a class="anime-button anime-button-secondary" href="https://www.linkedin.com/in/lennon-chia/" rel="me">LinkedIn <span aria-hidden="true">↗</span></a>
        </div>
        <div class="anime-tag-row" aria-label="Specialisms">
          <span>AI security</span><span>Penetration testing</span><span>Agentic controls</span><span>OSS research</span>
        </div>
      </div>

      <figure class="anime-portrait-frame">
        <div class="anime-portrait-halo" aria-hidden="true"></div>
        <div class="anime-portrait-panel">
          <img src="{{ '/assets/img/moonlit-elf-portrait.svg' | relative_url }}" alt="Original moonlit portrait of a silver-haired elven archivist with luminous green eyes">
          <div class="anime-scan-line" aria-hidden="true"></div>
          <span class="anime-corner anime-corner-one" aria-hidden="true"></span>
          <span class="anime-corner anime-corner-two" aria-hidden="true"></span>
        </div>
        <figcaption>
          <span>Moonlit archivist · 01</span>
          <strong>LENNON CHIA</strong>
          <small>Every finding needs human judgment</small>
        </figcaption>
      </figure>
    </section>

    <section class="anime-evidence" aria-label="Career and public-work highlights">
      <div><strong>11+</strong><span>Years on the security journey</span></div>
      <div><strong>02</strong><span>Teams guided across AI and penetration testing</span></div>
      <div><strong>≈50%</strong><span>Lower effort in selected AI-assisted trials</span></div>
      <a href="{{ '/merged-prs/' | relative_url }}"><strong>{{ merged_prs | size }}</strong><span>Merged PRs indexed <b aria-hidden="true">↗</b></span></a>
    </section>

    <section id="about" class="anime-section anime-about">
      <header class="anime-section-heading">
        <span>Scroll I · Profile</span>
        <h2>Lessons that outlast the moment.</h2>
      </header>
      <div class="anime-about-grid">
        <div class="anime-about-copy">
          <p class="anime-drop-lede">I’m a Singapore-based cybersecurity professional working where offensive security, practical AI, and secure engineering meet.</p>
          <p>As a Cybersecurity Manager at EY, I lead an AI innovation team and a penetration-testing delivery team across government and multinational environments. My role combines technical direction, methodology, finding validation, delivery quality, demonstrations, workshops, and client engagement.</p>
          <p>I treat AI as a force multiplier—not a substitute for experienced security practitioners. The systems I build keep human review at the decision boundary, especially when a model can influence testing, triage, exploitation, or remediation advice.</p>
        </div>
        <aside class="anime-identity-card" aria-label="Profile summary">
          <div class="anime-identity-label">Adventurer record · LC-01</div>
          <dl>
            <div><dt>Base</dt><dd>Singapore</dd></div>
            <div><dt>Current role</dt><dd>Cybersecurity Manager, EY</dd></div>
            <div><dt>Primary lens</dt><dd>Offensive security + AI</dd></div>
            <div><dt>Research mode</dt><dd>Evidence → patch → regression proof</dd></div>
          </dl>
          <blockquote>“The useful question is not whether AI can act. It is where its output gains authority—and how a human stays in control.”</blockquote>
        </aside>
      </div>
      <figure class="anime-cinematic anime-cinematic-path">
        <img src="{{ '/assets/img/long-journey-landscape.svg' | relative_url }}" alt="An original fantasy landscape with a winding road, distant ruins, mountains, and blue flowers">
        <figcaption><span>The road continues</span><strong>Small lessons accumulate into lasting judgment.</strong></figcaption>
      </figure>
    </section>

    <section id="experience" class="anime-section anime-experience">
      <header class="anime-section-heading">
        <span>Scroll II · Journey</span>
        <h2>A career measured in what endures.</h2>
      </header>
      <div class="anime-timeline">
        <article class="anime-role anime-role-featured">
          <div class="anime-role-meta">
            <span>OCT 2021 — PRESENT</span>
            <b>EY · SINGAPORE</b>
          </div>
          <div class="anime-role-body">
            <p class="anime-role-index">Journey · 01</p>
            <h3>Cybersecurity Manager</h3>
            <ul>
              <li>Lead an AI innovation team and a penetration-testing delivery team.</li>
              <li>Own the architecture and ground-up development of an AI-assisted penetration-testing accelerator built on locally hosted language models.</li>
              <li>Integrate AI into attack-path analysis, cyber risk assessment, secure code review, web testing, vulnerability triage, exploit validation, and remediation guidance.</li>
              <li>Engineer agentic controls around least privilege, approval gates, auditability, rollback, and human oversight.</li>
              <li>Set technical direction, validate findings, and assure delivery quality across the penetration-testing lifecycle.</li>
            </ul>
            <div class="anime-trial-note"><strong>Selected trial signal</strong><span>Approximately 50% lower analyst effort and triage time for selected AI-assisted activities, with findings and conclusions still human-validated.</span></div>
          </div>
        </article>

        <article class="anime-role">
          <div class="anime-role-meta">
            <span>APR 2015 — OCT 2021</span>
            <b>EY · SINGAPORE</b>
          </div>
          <div class="anime-role-body">
            <p class="anime-role-index">Journey · 02</p>
            <h3>Senior Information Security Consultant</h3>
            <p>Built the technical foundation for more than six years of penetration testing, vulnerability assessment, offensive security delivery, and client-facing security work before moving into management.</p>
          </div>
        </article>

        <article class="anime-role anime-role-education">
          <div class="anime-role-meta">
            <span>2013 — 2015</span>
            <b>EDUCATION</b>
          </div>
          <div class="anime-role-body">
            <p class="anime-role-index">Foundation · 01</p>
            <h3>University of Wollongong</h3>
            <p>Academic foundation supporting a career in information security, technical delivery, and systems thinking.</p>
          </div>
        </article>
      </div>
    </section>

    <section id="operations" class="anime-section anime-operations">
      <header class="anime-section-heading">
        <span>Scroll III · Practice</span>
        <h2>A grimoire for practical security.</h2>
      </header>
      <div class="anime-operation-grid">
        <article class="anime-operation-card anime-operation-wide">
          <span class="anime-operation-number">01</span>
          <p class="anime-operation-kicker">Augmentation · AI-assisted offensive security</p>
          <h3>Local models. Deliberate control. Human decisions.</h3>
          <p>I’m building a locally hosted penetration-testing accelerator using high-performance model serving with SGLang and speculative decoding. It supports practitioners across analysis, review, testing, triage, validation, and remediation without treating model output as ground truth.</p>
          <div class="anime-flow" aria-label="AI-assisted security workflow">
            <span>CONTEXT</span><i aria-hidden="true"></i><span>MODEL</span><i aria-hidden="true"></i><span>CONTROL</span><i aria-hidden="true"></i><span>HUMAN</span>
          </div>
        </article>

        <article class="anime-operation-card">
          <span class="anime-operation-number">02</span>
          <p class="anime-operation-kicker">The five-ward control model</p>
          <h3>Authority is designed, not assumed.</h3>
          <p>Least privilege, explicit approvals, traceable audit records, safe rollback, and continuous human oversight define the operating boundary.</p>
        </article>

        <article class="anime-operation-card">
          <span class="anime-operation-number">03</span>
          <p class="anime-operation-kicker">Field practice · Penetration testing</p>
          <h3>Methodology through quality assurance.</h3>
          <p>I lead technical delivery, set methodology and direction, validate findings, and translate technical evidence into decisions.</p>
        </article>

        <article class="anime-operation-card">
          <span class="anime-operation-number">04</span>
          <p class="anime-operation-kicker">Open-source research grimoire</p>
          <h3>Trace the boundary. Ship the fix.</h3>
          <p>I reproduce source-to-sink paths, check for duplicates, contribute focused patches with regression tests, and turn shipped work into reusable research patterns.</p>
          <div class="anime-project-links">
            <a href="https://github.com/Hinotoi-agent/vulnweave">VulnWeave ↗</a>
            <a href="https://github.com/Hinotoi-agent/Verifymate">Verifymate ↗</a>
            <a href="{{ '/selected-work/' | relative_url }}">Selected work →</a>
          </div>
        </article>
      </div>
      <figure class="anime-cinematic anime-cinematic-companions">
        <img src="{{ '/assets/img/companions-campfire.svg' | relative_url }}" alt="An original twilight illustration of four travelers sharing a quiet meal beside a fire">
        <figcaption><span>Companions of the craft</span><strong>The strongest security work is learned, reviewed, and delivered together.</strong></figcaption>
      </figure>
    </section>

    <section class="anime-section anime-controls">
      <header class="anime-section-heading anime-section-heading-compact">
        <span>Five wards · Human in the loop</span>
        <h2>Guardrails before autonomy.</h2>
      </header>
      <ol class="anime-control-sequence">
        <li><b>01</b><strong>Least privilege</strong><span>Give each model and tool only the authority the task requires.</span></li>
        <li><b>02</b><strong>Approval gates</strong><span>Pause before sensitive, irreversible, or externally visible actions.</span></li>
        <li><b>03</b><strong>Audit trails</strong><span>Preserve what was requested, decided, executed, and returned.</span></li>
        <li><b>04</b><strong>Rollback paths</strong><span>Design recovery before granting an agent the ability to change state.</span></li>
        <li><b>05</b><strong>Human oversight</strong><span>Keep findings and conclusions accountable to an experienced reviewer.</span></li>
      </ol>
    </section>

    <section id="proof" class="anime-section anime-proof">
      <header class="anime-section-heading">
        <span>Scroll IV · Open archive</span>
        <h2>Evidence, preserved in the open.</h2>
      </header>
      <div class="anime-proof-stats">
        <a href="{{ '/merged-prs/' | relative_url }}"><strong>{{ merged_prs | size }}</strong><span>Merged upstream PRs</span></a>
        <a href="{{ '/merged-prs/' | relative_url }}"><strong>{{ security_prs | size }}</strong><span>Security / hardening PRs</span></a>
        <a href="{{ '/selected-work/' | relative_url }}"><strong>{{ repos | size }}</strong><span>Repositories touched</span></a>
      </div>

      <div class="anime-disclosure-grid">
        <a class="anime-disclosure" href="https://osv.dev/vulnerability/CVE-2026-22207">
          <span>CVE-2026-22207</span><strong>OpenViking broken access control</strong><small>Missing root API key allowed anonymous ROOT access.</small>
        </a>
        <a class="anime-disclosure" href="https://nvd.nist.gov/vuln/detail/CVE-2026-25858">
          <span>CVE-2026-25858</span><strong>macrozheng mall account takeover</strong><small>Password-reset OTP exposure enabled unauthenticated resets.</small>
        </a>
        <a class="anime-disclosure" href="https://nvd.nist.gov/vuln/detail/CVE-2026-25870">
          <span>CVE-2026-25870</span><strong>DoraCMS server-side request forgery</strong><small>Remote-image fetching lacked destination restrictions.</small>
        </a>
        <a class="anime-disclosure" href="https://nvd.nist.gov/vuln/detail/CVE-2026-26218">
          <span>CVE-2026-26218</span><strong>newbee-mall default administrator credentials</strong><small>Predictable pre-seeded credentials exposed administrative access.</small>
        </a>
        <a class="anime-disclosure anime-disclosure-wide" href="https://www.yalehome.com/global/legal-and-privacy/product-advisory/Yale-PA-2023-01.pdf">
          <span>Product advisory · Yale</span><strong>MIFARE Classic cloning research</strong><small>Responsible disclosure and collaboration on affected smart-lock RFID implementations.</small>
        </a>
      </div>
    </section>

    <section class="anime-section anime-background">
      <article class="anime-speaking">
        <p class="anime-operation-kicker">Gathering · Milipol TechX 2026</p>
        <h2>Using AI as a Force Multiplier to Augment Offensive Security</h2>
        <p>A lightning talk on applying AI to offensive-security workflows while retaining practitioner control, verification, and accountability.</p>
        <a href="https://www.linkedin.com/posts/lennon-chia_happy-to-share-that-at-milipol-techx-2026-activity-7457275024522121216-IF5F">View the talk post on LinkedIn ↗</a>
      </article>
      <article class="anime-certifications">
        <p class="anime-operation-kicker">Grimoire · Selected credentials</p>
        <h2>Technical foundations</h2>
        <div class="anime-cert-grid" aria-label="Selected certifications earned">
          <span><b>CRTO</b>Certified Red Team Operator</span>
          <span><b>CRTP</b>Certified Red Team Professional</span>
          <span><b>OSWE</b>Offensive Security Web Expert</span>
          <span><b>OSWP</b>Offensive Security Wireless Professional</span>
          <span><b>OSCP</b>Offensive Security Certified Professional</span>
          <span><b>AZ-500</b>Azure Security Engineer Associate</span>
        </div>
        <small>Credentials listed as earned; current status is maintained on LinkedIn.</small>
      </article>
    </section>

    <section class="anime-section anime-notes">
      <header class="anime-section-heading anime-section-heading-compact">
        <span>Field journal · Latest notes</span>
        <h2>Knowledge gathered along the way.</h2>
      </header>
      <div class="anime-note-list">
        {% for post in site.posts limit: 3 %}
          <a href="{{ post.url | relative_url }}">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y.%m.%d" }}</time>
            <strong>{{ post.title }}</strong>
            <span>{{ post.excerpt | strip_html | strip_newlines | truncate: 135 }}</span>
          </a>
        {% endfor %}
      </div>
    </section>

    <figure class="anime-cinematic anime-cinematic-meteors">
      <img src="{{ '/assets/img/era-meteors.svg' | relative_url }}" alt="An original night landscape with travelers watching meteors above distant mountains and ruins">
      <figcaption><span>What remains</span><strong>The work passes. The lessons become part of the next journey.</strong></figcaption>
    </figure>

    <section class="anime-contact" aria-labelledby="anime-contact-title">
      <p class="anime-overline">Campfire · Open channel</p>
      <h2 id="anime-contact-title">What boundary lies ahead?</h2>
      <p>Explore my public work, follow the field notes, or connect with me professionally.</p>
      <div class="anime-hero-actions anime-contact-actions">
        <a class="anime-button anime-button-primary" href="https://www.linkedin.com/in/lennon-chia/" rel="me">Connect on LinkedIn <span aria-hidden="true">↗</span></a>
        <a class="anime-button anime-button-secondary" href="https://github.com/Hinotoi-agent" rel="me">Explore GitHub <span aria-hidden="true">↗</span></a>
        <a class="anime-button anime-button-secondary" href="{{ '/feed.xml' | relative_url }}">Follow RSS <span aria-hidden="true">↗</span></a>
      </div>
      <small>Independent research and opinions published here are my own. No private client information or uncoordinated findings are included.</small>
    </section>
  </main>

  <footer class="anime-footer">
    <a href="{{ '/' | relative_url }}">Hinotoi · Arcane security notes</a>
    <span>Quiet craft, long memory, and fixes that endure.</span>
    <a href="#profile-main">Back to top ↑</a>
  </footer>
</div>
