---
layout: page
title: Field Notes
permalink: /field-notes/
---

Short observations that should survive beyond a single PR. These are public-safe summaries of what the vault, merged work, maintainer feedback, and external references keep teaching.

<div class="note-grid">
  <article class="note-card"><strong>The sink owns the boundary.</strong><p>Caller intent is context, not enforcement. File reads, HTTP fetches, browser actions, process launches, uploads, and approvals must prove their own invariants.</p></article>
  <article class="note-card"><strong>Prompt injection matters when it gains a bridge.</strong><p>The interesting question is not whether text can influence a model. It is whether that influence reaches tools, files, memory, credentials, network access, or approval bypass.</p></article>
  <article class="note-card"><strong>Redirects are part of SSRF.</strong><p>A URL that starts safe can become unsafe when a downstream client follows redirects, falls back to another transport, or retries through a different code path.</p></article>
  <article class="note-card"><strong>Uploads are parser exposure.</strong><p>Extension checks are weak if privileged services still parse attacker-controlled Office, PDF, archive, image, or markdown content in a rich execution context.</p></article>
  <article class="note-card"><strong>Agent memory is persistence.</strong><p>If untrusted content can become future context, it can become delayed influence. Review storage, retrieval, summarization, and deletion paths as part of the security model.</p></article>
  <article class="note-card"><strong>Maintainer feedback is training data.</strong><p>Closed, downgraded, or re-scoped findings should update the vault, not disappear into a comment thread.</p></article>
</div>

## How a field note becomes useful

A note is worth keeping when it changes one of these:

- the next duplicate-check query,
- the next proof shape,
- the next regression test,
- the next checklist item,
- the next disclosure boundary,
- or the next public explanation.

If it does not change future behavior, it stays as context rather than becoming a lesson.
