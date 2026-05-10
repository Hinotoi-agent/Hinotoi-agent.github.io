---
layout: post
title: "2026-05-10 — Common AI security patterns mapped to OWASP"
takeaway: "The recurring AI security issue is boundary drift: familiar web weaknesses reappear around agent tools, local control planes, files, browser paths, and model-mediated actions."
categories: [ai-security, field-notes]
tags: [ai-security, owasp, llm-top-10, web-top-10, agents, vulnerability-research]
---

This is a higher-level summary of the security patterns I keep seeing while reviewing open-source AI and agent systems. I am intentionally keeping it generic: the value is not in naming every repository, but in noticing where the same boundary keeps failing.

The short version: most findings are not exotic LLM-only problems. They are familiar web and systems bugs placed next to agent autonomy, tool execution, local files, model output, MCP/plugin surfaces, and browser-reachable control planes.

## Pattern chart

<div class="chart-panel" role="img" aria-label="Approximate finding counts by pattern">
  <div class="chart-row"><span class="chart-label">Unsafe tool/code execution <small>LLM06 / LLM05</small></span><span class="chart-bar" style="--w: 100%">8</span></div>
  <div class="chart-row"><span class="chart-label">Missing auth / exposed control planes <small>LLM06 / LLM01</small></span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">File read / secret disclosure <small>LLM02 / LLM05</small></span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">File write / workspace escape <small>LLM03 / LLM06</small></span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">Authorization / identity bypass <small>LLM06 / LLM02</small></span><span class="chart-bar" style="--w: 75%">6</span></div>
  <div class="chart-row"><span class="chart-label">SSRF / unsafe fetching <small>LLM06 / LLM03</small></span><span class="chart-bar" style="--w: 62.5%">5</span></div>
  <div class="chart-row"><span class="chart-label">Browser, OAuth, webhook trust <small>LLM06</small></span><span class="chart-bar" style="--w: 50%">4</span></div>
  <div class="chart-row"><span class="chart-label">Network exposure / local defaults <small>LLM06</small></span><span class="chart-bar" style="--w: 25%">2</span></div>
  <div class="chart-row"><span class="chart-label">Package / archive supply chain <small>LLM03</small></span><span class="chart-bar" style="--w: 12.5%">1</span></div>
</div>

<style>
.chart-panel {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px solid var(--border, #d0d7de);
  border-radius: 14px;
  background: var(--surface, #f6f8fa);
}
.chart-row {
  display: grid;
  grid-template-columns: minmax(12rem, 18rem) 1fr;
  align-items: center;
  gap: .75rem;
  margin: .55rem 0;
  font-size: .95rem;
}
.chart-label { color: var(--muted, #57606a); }
.chart-label small {
  display: block;
  margin-top: .2rem;
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .02em;
  color: var(--accent, #d9480f);
}
.chart-bar {
  display: block;
  width: var(--w);
  min-width: 2.25rem;
  padding: .35rem .65rem;
  border-radius: 999px;
  color: #fff;
  font-weight: 700;
  line-height: 1;
  background: linear-gradient(90deg, #d9480f, #f59f00);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.25);
}
@media (max-width: 720px) {
  .chart-row { grid-template-columns: 1fr; gap: .25rem; }
}
</style>

## 1. Unsafe tool and code execution

The highest-risk pattern is simple: untrusted input reaches a tool, shell, Python runner, subprocess, MCP server, or sandbox escape path.

- OWASP Web: **A03 Injection**, **A01 Broken Access Control**
- OWASP LLM: **LLM06 Excessive Agency**, **LLM05 Improper Output Handling**

My view: once an AI product exposes tools, the review should treat every tool call as a capability boundary. The important question is whether the caller can make the host do something the product did not mean to delegate.

## 2. Exposed control planes

Many AI systems ship with local dashboards, training servers, agent APIs, plugin routes, or admin-like endpoints. These often start as development conveniences and become real attack surfaces.

- OWASP Web: **A01 Broken Access Control**, **A07 Identification and Authentication Failures**, **A05 Security Misconfiguration**
- OWASP LLM: **LLM06 Excessive Agency**, **LLM01 Prompt Injection**

My view: “local” is not a security control unless the bind address, browser behavior, Host/Origin handling, and authentication all agree.

## 3. Broken authorization and identity trust

Another common pattern is not missing login, but missing object-level or role-level checks. A user can access another workflow, act as another owner, mint a stronger ticket, or turn a low-privilege role into a management role.

- OWASP Web: **A01 Broken Access Control**, **A07 Identification and Authentication Failures**
- OWASP LLM: **LLM06 Excessive Agency**, **LLM02 Sensitive Information Disclosure**

My view: agent products need precise verbs. “View,” “use,” “run,” “manage,” and “bridge into the workspace” are different permissions.

## 4. File and secret exposure

Agents sit close to prompts, credentials, workspaces, logs, attachments, and provider tokens. That makes file-read bugs more sensitive than they first appear.

- OWASP Web: **A01 Broken Access Control**, **A05 Security Misconfiguration**, sometimes **A02 Cryptographic Failures**
- OWASP LLM: **LLM02 Sensitive Information Disclosure**, **LLM05 Improper Output Handling**

My view: in an agent runtime, local files often contain the real trust material: API keys, prompts, state, task history, and user data.

## 5. File write, delete, and workspace escape

Uploads, symlinks, archive extraction, plugin names, repo-local config, and container-mounted folders keep producing path-boundary failures.

- OWASP Web: **A05 Security Misconfiguration**, **A01 Broken Access Control**, **A08 Software and Data Integrity Failures**
- OWASP LLM: **LLM03 Supply Chain**, **LLM06 Excessive Agency**

My view: path safety belongs at the sink. Normalize, resolve, and verify containment where the read/write/delete actually happens.

## 6. SSRF and unsafe fetching

AI products frequently fetch URLs for tools, media, OpenAPI actions, browser control, MCP integrations, or document ingestion. This creates repeated SSRF risk.

- OWASP Web: **A10 Server-Side Request Forgery**
- OWASP LLM: **LLM06 Excessive Agency**, **LLM03 Supply Chain**

My view: validate the actual network client that follows redirects and performs the request. A pre-check in a different helper is not enough.

## 7. Browser, OAuth, webhook, and callback trust

Old web rules still matter: signed state, single-use nonces, Host/Origin checks, webhook shared secrets, and fail-closed validation.

- OWASP Web: **A07 Identification and Authentication Failures**, **A01 Broken Access Control**, **A05 Security Misconfiguration**
- OWASP LLM: usually secondary, but often **LLM06 Excessive Agency** when the callback drives an agent action

My view: AI systems do not get to skip ordinary web authentication rules just because the interesting part happens after the callback.

## 8. Insecure local defaults and supply chain helpers

Some risk comes from defaults: broad network binds, published Docker ports, unsafe archive extraction, trusted repo-local files, and plugin/package helper scripts.

- OWASP Web: **A05 Security Misconfiguration**, **A08 Software and Data Integrity Failures**, **A06 Vulnerable and Outdated Components**
- OWASP LLM: **LLM03 Supply Chain**, **LLM06 Excessive Agency**

My view: defaults are part of the threat model. If the product claims a safe local or sandbox boundary, the primitive must enforce it by default.

## The common thread

The recurring issue is boundary drift.

A product says:

```text
local only
read only
safe tool
shared use
workspace confined
trusted callback
internal URL blocked
```

But the dangerous sink says:

```text
bind broadly
launch command
trust header
read file
follow symlink
fetch anyway
upload model-chosen path
```

OWASP Web explains the root cause: access control, injection, SSRF, authentication failure, misconfiguration, and integrity failure. OWASP LLM explains the amplification: tools, prompts, model output, plugins, MCP, files, and unattended agent actions make those old weaknesses more consequential.

## Repeat next time

- Start with the ordinary web boundary.
- Then ask what the agent layer amplifies.
- Prove the issue at the sink, not the helper.
- Patch the invariant where the dangerous action actually happens.
