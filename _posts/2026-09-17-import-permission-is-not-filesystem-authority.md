---
layout: post
title: "2026-09-17 — Import permission is not filesystem authority"
date: 2026-09-17 23:59:00 +0800
permalink: /2026/09/17/import-permission-is-not-filesystem-authority/
takeaway: "Permission to import a bundle does not grant authority over every destination named inside it."
categories: [daily, ai-security]
tags: [path-safety, imports, trust-boundaries, oss-hardening, vault-backed-learning]
---

## Signal

An import permission answers who may submit a bundle. It does not answer where the bundle may write. Those decisions need separate enforcement, even when the uploader has an owner role within the application.

## Merged PRs

None in this window.

The reporting interval is `[2026-09-17T00:00:00+08:00, 2026-09-18T00:00:00+08:00)`. A fresh GitHub search confirmed the empty merge window.

## What shipped or moved

No new code shipment or target-day vault update was identified. This entry revisits an existing archive-import case and path-safety checklist, rather than presenting an older advisory as a new finding. The recent merged history is already indexed; no archive update is needed.

The review focus is the distinction between application ownership and filesystem authority. An account allowed to manage one collection is not necessarily trusted to modify the server or another collection.

## Observed pattern

Importers translate structured content into filesystem operations. The outer request may be authorized while destinations carried inside the bundle still require containment checks.

For agent workspaces, memory imports, and tool-generated bundles, the same defensive question applies: what root is this operation allowed to affect, and which component enforces that limit before creating directories or writing files? A trusted import route must not make every embedded path trusted by inheritance.

## External reference

The public [gramps-webapi media-import advisory](https://github.com/advisories/GHSA-m5gr-86j6-99jp) distinguishes tree-owner privileges from server administration and describes deployment-dependent impact. It records resolved-root validation before extraction as the remediation.

This is an older reference already captured in the vault, not a new disclosure. The useful anchor here is its permission and deployment distinction. This post does not independently reproduce the advisory, validate its library-level explanation, or assess a current release.

## What was learned

A role name is not a complete trust model. “Owner” needs an object: owner of a collection, a workspace, or the deployment itself. The boundary claim should name that object before discussing impact.

Containment evidence also needs to describe state, not just an error response. A rejected import should not leave files outside its permitted root. Compatibility belongs beside that negative check: a valid bundle should still import within the intended destination.

## Takeaways

- **Separate admission from destination authority.** Import access does not authorize arbitrary filesystem writes.
- Name what the actor owns; do not equate application ownership with server administration.
- Keep impact tied to the deployment's actual storage and isolation boundaries rather than its most dramatic possible configuration.

## Repeat next time

Before evaluating an importer, record the permitted root and the actor's scope. Check that destination validation precedes filesystem mutation. In an isolated regression fixture, verify rejection and absence of outside-root writes, then verify that a valid import still succeeds. Do not treat these proposed checks as execution evidence until they have actually run.

## Vault redirect

The existing media-import advisory case and Path Safety Review checklist remain the canonical records. Their rules already cover resolved containment, validation before I/O, and absence-of-side-effect checks. The discovery workflow supplies the actor and deployment boundary contract. This post applies those existing rules; it adds no new finding or checklist policy requiring a duplicate vault note.
