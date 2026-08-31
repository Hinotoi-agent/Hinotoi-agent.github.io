---
layout: post
title: "2026-08-31 — Credentials must be private before publication"
date: 2026-08-31 05:01:41 +0800
permalink: /2026/08/31/ai-security-case-study-private-before-publication/
takeaway: "A credential writer must enforce owner-only permissions on the staged file before it writes secrets or atomically publishes the final path; process umask is not a security policy."
categories: [case-study, ai-security]
tags: [case-study, credential-security, oauth, file-permissions, atomic-write, local-security]
---

## Signal

Atomic replacement protects file integrity, but it does not automatically protect confidentiality. If a credential store lets the replacement file inherit permissions from a permissive process umask, a routine token refresh can publish a readable secret file.

The invariant belongs in the writer: secret-bearing bytes must enter a private file, and the final path must remain private after publication.

## Merged PRs

None in this window.

The case below is grounded in a previously merged fix, not presented as a new merge in the closed Singapore-time window from 2026-08-31 00:00 to 2026-09-01 00:00.

## What shipped or moved

The public case study was published and the corresponding private review rule was tightened from “check the final credential-file mode” to “make the staged file private before writing secret bytes, preserve that mode through publication, and prove failure cleanup.” The merged-PR archive did not need a new record.

## Observed pattern

Security properties can arrive too late. A final `chmod` can repair the published file while still leaving a secret-bearing staged object exposed during the write. The stronger invariant is temporal as well as structural: confidentiality must hold when the object first receives authority-bearing data, through rename, and after the final path becomes visible.

For credential persistence, the useful chain is `secret source -> serializer -> staged object creation -> permission decision -> write -> atomic publication -> final object`. “Atomic” protects completeness; it does not establish confidentiality.

## External reference

- [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html) anchors the confidentiality risk when credentials or configuration data are readable through incorrect resource permissions.
- The Open Group [`open()` specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/open.html) makes the creation semantics explicit: the requested mode is modified by the process file-creation mask, while `O_CREAT | O_EXCL` provides exclusive creation. The review lesson is to request the restrictive mode at creation rather than inherit a general process default and repair it later.

## Threat model

The victim runs CodexBar on a shared Unix-like machine. Another local user can traverse the victim's Codex home path and read files permitted to group or other users.

The attacker does not control the OAuth tokens or need remote access. The relevant event is a normal CodexBar save, refresh, or account-selection rewrite of `auth.json` under a permissive umask such as `022`. The file contains reusable access and refresh tokens, an optional ID token, and account metadata.

## Finding and PR

Public PR: [`steipete/CodexBar #1702 — [security] fix(codex): keep OAuth auth.json private`](https://github.com/steipete/CodexBar/pull/1702).

Merge commit: [`ca31ab2a8045039b3d611ecdb2d003f064d17ef1`](https://github.com/steipete/CodexBar/commit/ca31ab2a8045039b3d611ecdb2d003f064d17ef1).

Changed files:

- `Sources/CodexBarCore/Providers/Codex/CodexOAuth/CodexOAuthCredentials.swift` — replaces the umask-dependent atomic save with an explicitly private staged write and rename.
- `Tests/CodexBarTests/CodexOAuthCredentialsStorePermissionsTests.swift` — checks the final mode and the pre-publication staging invariant.
- `TestsLinux/CodexOAuthCredentialsStoreLinuxTests.swift` — exercises the final permission invariant in Linux/container CI.
- `CHANGELOG.md` — records the credential-persistence hardening.

Before the fix, `CodexOAuthCredentialsStore.save` used an atomic data write without restoring owner-only POSIX permissions. Under `umask 022`, the rewritten `auth.json` could become `0644`.

## Exploit path

The bounded public source-to-sink chain was:

```text
normal CodexBar OAuth save or refresh
  -> access, refresh, and optional ID tokens are serialized
  -> atomic replacement inherits process umask policy
  -> auth.json can be published as mode 0644
  -> another local user reads the credential file
  -> reusable OAuth token material crosses the user boundary
```

The dangerous assumption was not atomicity itself. It was treating process-wide creation defaults as sufficient policy for a specific secret-bearing artifact. Atomic replacement can preserve consistency while still replacing a private file with a more permissive one.

## Mitigation

The merged writer creates a unique staged file beside `auth.json` with `open(..., O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600)`. It then applies `fchmod(..., 0600)`, writes and synchronizes the data, closes the descriptor, and renames the staged file over the destination.

This ordering makes privacy true before secret bytes are written and before the file is published:

```text
create exclusive staged file as 0600
  -> reinforce mode on the open descriptor
  -> write and synchronize credentials
  -> close
  -> atomically rename to auth.json
```

On failure, the staged file is removed. Token format, parsing, refresh behavior, and account selection remain unchanged.

## Verification

The macOS/Linux regression `saving O auth credentials keeps auth json private` calls the real `CodexOAuthCredentialsStore.save` API with placeholder tokens and a temporary `CODEX_HOME`, then asserts that `auth.json` has mode `0600`.

A second test, `auth json is private before atomic publication`, inspects the staged file immediately before rename. It asserts `0600`, confirms the old destination still contains its original data, forces publication to stop, and then proves the old file remains intact with no staged-file residue. This verifies both confidentiality before publication and cleanup on failure.

The Linux suite provides the focused control `CodexOAuthCredentialsStoreLinuxTests/saveKeepsAuthJSONPrivate`. The PR records this container-backed command:

```sh
docker run --rm -v "$PWD:/work" -w /work swift:6.2-noble bash -lc '
  set -e
  apt-get update >/dev/null
  apt-get install -y libsqlite3-dev >/dev/null
  swift test --filter CodexOAuthCredentialsStoreLinuxTests/saveKeepsAuthJSONPrivate
'
```

The PR also records a macOS runtime proof using the real save API under `umask 022`; the resulting `auth.json` mode was `600`. Placeholder values were used, and no production tokens were exposed.

## What was learned

A final `chmod` is better than relying on umask, but the stronger primitive is to create the staged object privately before writing sensitive data. That closes both the persistent final-mode failure and any interval in which a temporary file could carry secrets under weak permissions.

The reusable review boundary is `secret source -> serializer -> staging primitive -> permission decision -> atomic publication -> final filesystem object`. Check every step. “Atomic” answers whether readers see a complete version; it does not answer who may read it.

The private research system already generalizes this as a destination-boundary rule: controls should sit at the primitive that sends, stores, or executes authority. For credential stores, the regression contract is owner-only staging plus owner-only final state, not merely a successful save.

## Takeaways

- Make a secret-bearing staged file owner-only before the first credential byte is written.
- Test both the staged state and the published state; a final-mode assertion alone cannot prove there was no exposure interval.
- Treat process umask as an ambient default, not as the application-specific policy for OAuth tokens, API keys, cookies, sessions, or private keys.
- Verify failure paths preserve the old destination and remove every staged artifact.

## Repeat next time

- Inventory token, API-key, cookie, session, and private-key writers, including refresh and migration paths.
- Trace atomic saves through their temporary or staged files instead of checking only the final filename.
- Test under a permissive umask and assert the exact final mode.
- Add a pre-publication hook or equivalent test seam that can inspect staged permissions before rename.
- Force a publication failure and assert that the old file remains intact and no secret-bearing temporary file remains.
- Keep a positive control for normal save/load behavior so permission hardening does not break credential refresh.

## Vault redirect

The canonical reusable rule remains in the private OSS Vulnerability Research Vault, in `Takeaway - User-controlled integration config must not reach secret resolvers`: credential writers must make staged objects owner-only before writing secrets, preserve owner-only permissions through atomic replacement, and enforce destination policy in the storage primitive rather than infer it from caller intent or process defaults.

This post is the public-safe synthesis of the merged PR and that maintained review rule. It does not reproduce private finding artifacts or extend the public claim beyond the demonstrated local credential-confidentiality boundary.
