---
layout: post
title: "2026-05-10 — Common AI security issues mapped to OWASP"
takeaway: "Across the current vault findings, the recurring failure is not one exotic LLM bug. It is old web security boundaries reappearing around agent tools, local control planes, file systems, and model-mediated actions."
categories: [ai-security, field-notes]
tags: [ai-security, owasp, llm-top-10, web-top-10, agents, vulnerability-research]
---

This is a compact map of the security issues in the OSS vulnerability vault so far. I grouped the findings by the failure mode that matters most during review, then mapped each group to the closest OWASP Web Top 10 and OWASP Top 10 for LLM Applications categories.

The short version: most of the issues are not mysterious. They are familiar web and systems bugs placed next to agent autonomy, tool execution, local files, model output, MCP/plugin surfaces, and browser-reachable control planes.

## Category chart

<div class="chart-panel" role="img" aria-label="Finding counts by category">
  <div class="chart-row"><span class="chart-label">Unsafe tool/code execution</span><span class="chart-bar" style="--w: 100%">8</span></div>
  <div class="chart-row"><span class="chart-label">Missing auth / exposed control planes</span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">File read / secret disclosure</span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">File write / delete / workspace escape</span><span class="chart-bar" style="--w: 87.5%">7</span></div>
  <div class="chart-row"><span class="chart-label">Authorization / identity bypass</span><span class="chart-bar" style="--w: 75%">6</span></div>
  <div class="chart-row"><span class="chart-label">SSRF / unsafe fetching</span><span class="chart-bar" style="--w: 62.5%">5</span></div>
  <div class="chart-row"><span class="chart-label">Browser, OAuth, webhook trust</span><span class="chart-bar" style="--w: 50%">4</span></div>
  <div class="chart-row"><span class="chart-label">Network exposure / local defaults</span><span class="chart-bar" style="--w: 25%">2</span></div>
  <div class="chart-row"><span class="chart-label">Package / archive supply chain</span><span class="chart-bar" style="--w: 12.5%">1</span></div>
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

## 1. Unsafe tool/code execution

**Pattern:** an API, agent tool, MCP server, sandbox, or helper path reaches shell, Python, subprocess, or command execution without a strong boundary.

**OWASP map:** Web **A03 Injection**, **A01 Broken Access Control**, **A05 Security Misconfiguration**. LLM **LLM06 Excessive Agency**, **LLM05 Improper Output Handling**, **LLM03 Supply Chain**.

Findings:

- `heymrun/heym` — Python tool sandbox escape.
- `HKUDS/AutoAgent` — unauthenticated FastAPI tool RCE.
- `HKUDS/AutoAgent` — unauthenticated Docker TCP command server RCE.
- `berabuddies/agentflow` — unauthenticated inline shell/python pipeline RCE.
- `0xSero/vllm-studio` — unauthenticated runtime job command execution.
- `HKUDS/OpenHarness` PR 61 — GitTool read-only diff external-diff execution.
- `NousResearch/hermes-agent` — ACP stdio MCP command execution.
- `NousResearch/hermes-agent` — process stdin approval bypass.

**Thought:** this is the sharpest AI-agent risk class. When a product exposes tools, agents, pipelines, MCP servers, or sandboxes, the real question is not whether the UI calls it a tool. The question is whether untrusted input can reach a host capability.

## 2. Missing authentication / exposed control planes

**Pattern:** a server intended for local use, admin use, or agent orchestration is reachable without authentication.

**OWASP map:** Web **A01 Broken Access Control**, **A07 Identification and Authentication Failures**, **A05 Security Misconfiguration**. LLM **LLM06 Excessive Agency**, **LLM02 Sensitive Information Disclosure**, **LLM01 Prompt Injection**.

Findings:

- `HKUDS/nanobot` — browser-reachable unauthenticated API control plane.
- `HKUDS/OpenHarness` PR 87 — unauthenticated web control plane.
- `NousResearch/hermes-agent` — dashboard plugin API unauthenticated Kanban dispatch.
- `MLT-OSS/open-assistant-api` — file routes missing token auth.
- `bytedance/deer-flow` — unauthenticated custom agent `SOUL` / `USER` prompt management.
- `lupantech/AgentFlow` — unauthenticated training control plane.
- `NousResearch/hermes-agent` — unauthenticated detailed health diagnostics.

**Thought:** local-first software often treats `localhost` or a dashboard as a trust boundary. That only works if bind address, Host/Origin handling, auth, and browser behavior all enforce the same assumption.

## 3. Authorization / identity boundary bypass

**Pattern:** the caller is authenticated, but the system trusts the wrong identity, skips object-level authorization, or grants a lower role an owner-level capability.

**OWASP map:** Web **A01 Broken Access Control**, **A07 Identification and Authentication Failures**. LLM **LLM06 Excessive Agency**, **LLM02 Sensitive Information Disclosure**.

Findings:

- `heymrun/heym` — cross-workflow subworkflow authorization bypass.
- `heymrun/heym` — shared users can re-share workflows.
- `openclaw/crabbox` — shared token owner/org impersonation.
- `openclaw/crabbox` — use-role bridge ticket minting.
- `OpenClaw` — trusted-proxy requests default to full operator scopes.
- `NousResearch/hermes-agent` — Telegram model picker callback authorization gap.

**Thought:** agent systems amplify IDOR-style bugs because “view,” “use,” “run,” “manage,” and “bridge into a workspace” are different privileges. The review has to split those verbs apart.

## 4. File read / secret disclosure

**Pattern:** attacker-controlled paths, model-controlled media, or unauthenticated file APIs expose local files, prompts, credentials, artifacts, or secret-bearing config.

**OWASP map:** Web **A01 Broken Access Control**, **A02 Cryptographic Failures**, **A05 Security Misconfiguration**. LLM **LLM02 Sensitive Information Disclosure**, **LLM05 Improper Output Handling**.

Findings:

- `0xSero/vllm-studio` — frontend agent filesystem read.
- `HKUDS/AutoAgent` — File Surfer workspace path traversal.
- `berabuddies/agentflow` — artifact API path traversal file disclosure.
- `HKUDS/nanobot` — message tool outbound media arbitrary file read.
- `NousResearch/hermes-agent` — `MEDIA:` directive arbitrary local file exfiltration.
- `NousResearch/hermes-agent` — ACP resource link arbitrary local file read.
- `steipete/summarize` — daemon config credential disclosure.

**Thought:** file read bugs become more serious around agents because files often contain prompts, credentials, session state, workspace data, and provider tokens. “Just a file read” is rarely just a file read in an agent runtime.

## 5. Arbitrary file write / delete / workspace escape

**Pattern:** upload filenames, plugin names, symlinks, repo-local configs, or container-writable paths escape the intended directory and affect host files.

**OWASP map:** Web **A01 Broken Access Control**, **A05 Security Misconfiguration**, **A08 Software and Data Integrity Failures**. LLM **LLM03 Supply Chain**, **LLM06 Excessive Agency**.

Findings:

- `heymrun/heym` — upload filename traversal arbitrary file write.
- `bytedance/deer-flow` — symlinked upload destination write.
- `HKUDS/OpenHarness` — Feishu/Lark attachment filename traversal.
- `HKUDS/OpenHarness` — plugin uninstall path traversal.
- `nesquena/hermes-webui` — profile path traversal.
- `qwibitai/nanoclaw` — container-writable Claude fragments symlink host file deletion.
- `openclaw/crabbox` — Islo workdir workspace escape.

**Thought:** path safety should be enforced at the sink with resolved containment checks. It should not depend on a caller convention, a UI label, or the absence of `..` in one parser layer.

## 6. SSRF / unsafe server-side fetching

**Pattern:** model/tool/user-controlled URLs reach backend HTTP clients, media fetchers, MCP clients, OpenAPI action runners, or browser-control discovery paths.

**OWASP map:** Web **A10 Server-Side Request Forgery**. LLM **LLM06 Excessive Agency**, **LLM03 Supply Chain**.

Findings:

- `MLT-OSS/open-assistant-api` — unauthenticated action SSRF.
- `HKUDS/nanobot` — DingTalk outbound media SSRF.
- `labring/FastGPT` — stored MCP tool URLs bypass internal-address validation.
- `NousResearch/hermes-agent` — vision media download helper SSRF guard.
- `NousResearch/hermes-agent` — unsafe explicit CDP override endpoint validation.

**Thought:** the safest SSRF review question is: where does the actual redirect-following transport run? Validating a stored URL, a preview URL, or a helper path is not enough if another client performs the real network I/O later.

## 7. Browser, OAuth, webhook, and request-origin trust

**Pattern:** the system trusts browser requests, OAuth state, Host headers, callbacks, or webhook notifications without a strong origin/secret/state boundary.

**OWASP map:** Web **A07 Identification and Authentication Failures**, **A01 Broken Access Control**, **A05 Security Misconfiguration**. LLM: usually secondary, often **LLM06 Excessive Agency** when the request can drive agent behavior.

Findings:

- `bytedance/deer-flow` — login CSRF session fixation.
- `BasedHardware/omi` — MCP OAuth callback forgeable state.
- `NousResearch/hermes-agent` — API server Host header rebinding.
- `NousResearch/hermes-agent` — MS Graph webhook missing `clientState` fail-open.

**Thought:** callback and browser-adjacent endpoints need boring invariants: signed state, single-use nonces, Origin/Host checks where appropriate, and fail-closed secrets. Agent products do not get to skip old web rules.

## 8. Network exposure / insecure local defaults

**Pattern:** local or sandbox services bind too broadly, publish Docker ports on all interfaces, or perform side effects before local/remote admission checks.

**OWASP map:** Web **A05 Security Misconfiguration**, **A01 Broken Access Control**. LLM **LLM06 Excessive Agency**.

Findings:

- `bytedance/deer-flow` — local Docker sandbox broad port bind.
- `HKUDS/OpenHarness` — pre-allowlist channel media side effects.

**Thought:** if the design says “local only,” the primitive has to say local only too. Documentation is not a bind address.

## 9. Package / archive supply chain

**Pattern:** install or compatibility scripts trust downloaded archives and extract them without containment.

**OWASP map:** Web **A08 Software and Data Integrity Failures**, **A06 Vulnerable and Outdated Components**. LLM **LLM03 Supply Chain**.

Findings:

- `NousResearch/hermes-agent` — Android psutil sdist unsafe tar extraction.

**Thought:** package-install helper scripts are part of the attack surface. If they download and extract code, they need the same path traversal, symlink, hardlink, and special-file checks as any other archive handler.

## Cross-cutting lesson

The common issue is boundary drift.

The product says one thing:

```text
local only
read only
shared use
safe tool
trusted callback
workspace confined
internal URL rejected
```

But the sink does another thing:

```text
binds to 0.0.0.0
launches a command
trusts a header
reads an arbitrary file
follows a symlink
fetches through a different client
accepts model-controlled output as an action
```

For AI security review, OWASP LLM categories explain why the impact is amplified: tools, prompts, model output, MCP, files, and agent autonomy turn old classes of web bugs into host-side action. OWASP Web categories still explain the root cause: access control, injection, misconfiguration, SSRF, auth failures, and integrity failures.

## Repeat next time

- Start with the old web boundary: auth, object auth, path containment, SSRF, origin/state, and command injection.
- Then ask what the LLM/agent layer amplifies: tool use, prompt control, file upload, file read, MCP/plugin loading, browser reachability, and unattended execution.
- Prove the bug at the sink, not at the helper.
- Prefer small patches that encode the invariant where the dangerous action actually happens.
