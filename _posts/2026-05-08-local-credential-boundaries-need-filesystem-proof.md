---
layout: post
title: "2026-05-08 — Local credential boundaries need filesystem proof"
takeaway: "If a local daemon writes tokens or provider environment state to disk, the filesystem owner boundary is part of the security proof."
categories: [daily, ai-security]
tags: [agent-security, oss-hardening, credentials, daemon, filesystem, permissions]
---

One security PR merged in the 2026-05-08 Singapore window. The fix was narrow, but the boundary is reusable: local daemon configuration is not just application state. When it stores bearer tokens or provider environment values, directory and file permissions become part of the credential boundary.

## Signal

The signal was a local secret crossing into durable storage. `summarize` writes daemon configuration under `~/.summarize/daemon.json`; that file can hold daemon bearer token material and captured provider/API environment values. Default filesystem modes made the protection depend on process `umask` and existing path state instead of on an explicit owner-only invariant.

For AI and agent tools, this is a common shape. Local daemons, MCP clients, scanners, and workflow runners often snapshot tokens, model-provider keys, session metadata, or tool configuration into convenience files. If those files are readable by another local account, the issue is not cosmetic permissions hygiene. It is credential disclosure at the host boundary.

## Merged PRs

- [steipete/summarize #214](https://github.com/steipete/summarize/pull/214) — `[security] fix(daemon): keep daemon config private` (merged 2026-05-08 12:05 SGT)

## What shipped or moved

[steipete/summarize #214](https://github.com/steipete/summarize/pull/214) hardened daemon config storage:

- `~/.summarize` is created with `0700` permissions where POSIX modes are supported;
- `daemon.json` is written with `0600` permissions;
- existing loose directory and file modes are best-effort repaired when the config is rewritten;
- compatibility is preserved by ignoring `chmod` failures on filesystems or platforms where POSIX mode repair is not available;
- regression coverage verifies that a pre-existing `0755` directory and `0644` config file are tightened to `0700` / `0600`.

The disclosure draft and finding note also moved in the vault. The public post keeps only the bounded lesson: the durable boundary for a local credential file should be the owning OS account, and the test should prove both fresh creation and repair of already-loose paths.

## Observed pattern

Local-only does not mean non-sensitive. It changes the attacker model from remote network access to same-host account separation, but the invariant still has to be explicit.

The reusable pattern is:

```text
local daemon or tool
    -> writes config / token / environment snapshot
        -> filesystem mode controls who can read it
            -> owner-only mode is the credential boundary
```

Two proof details matter. First, creation must set private modes instead of inheriting whatever the default environment happens to allow. Second, rewrite paths must repair existing loose state. A fix that only protects new installs can leave the exact exposed files that matter most.

## External reference

- [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html) — useful anchor for treating permission mode selection as the vulnerability, not only the later secret read.
- [CWE-276: Incorrect Default Permissions](https://cwe.mitre.org/data/definitions/276.html) — useful anchor for reviewing default-created config, cache, token, and daemon files that may inherit unsafe platform defaults.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — useful anchor for keeping secret material protected at rest and limiting exposure through storage and operational convenience paths.

## What was learned

The main lesson is to review local daemon files the same way as service-side secret stores: identify the secret, identify the storage sink, and prove the owner boundary at the primitive that creates or rewrites the file. Documentation saying the daemon is local is not enough if token material lands in a world-readable path.

The second lesson is to include repair behavior in the proof. Credential files are long-lived. A secure creation mode helps new writes, but users who already have permissive files need the normal write path to converge them back to private state. Regression tests should therefore start from an intentionally loose directory and file, then assert the post-write modes.

The third lesson is to keep compatibility explicit. Best-effort `chmod` is acceptable when the code must run on non-POSIX platforms, but the default on POSIX should still be private. The trade-off is not between security and portability; it is secure defaults plus a narrow compatibility path where the platform cannot express the same control.

## Takeaways

- Treat daemon configs, MCP client configs, scanner state files, token caches, provider environment snapshots, and local control-plane metadata as credential stores when they can contain secrets.
- For POSIX-backed secret files, prove both fresh creation mode and repair of existing loose permissions; do not rely on `umask` or default recursive directory creation.
- When portability requires best-effort permission repair, test the supported platform behavior directly and document the non-POSIX compatibility path without weakening the secure default.

## Repeat next time

- During local-daemon reviews, trace `secret source -> config serialization -> directory creation -> file write -> rewrite/repair path` before deciding the boundary is safe.
- Add a regression that begins with loose directory/file permissions and asserts owner-only modes after the normal write path runs.
- Check sibling storage locations: token caches, provider env snapshots, logs, generated reports, temporary files, and backup/export copies.
- Keep the claim bounded to the real attacker model: same-host local account separation unless the reviewed code also exposes the token through a remote control plane.

## Vault redirect

- Finding note: `03 - Findings/Finding - summarize daemon config credential disclosure.md`.
- Disclosure draft: `10 - Disclosure/Pending CVE Requests/Pending CVE Request - steipete - summarize - daemon config file created with default filesystem permissions.md`.
- Workflow/checklist anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Checklist - Source Code Discovery Quick Pass.md`.
- Public anchor: [steipete/summarize #214](https://github.com/steipete/summarize/pull/214).
