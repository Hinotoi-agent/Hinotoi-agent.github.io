---
layout: post
title: "2026-08-14 — Persisted paths are active input at load time"
date: 2026-08-14 23:59:00 +0800
permalink: /2026/08/14/persisted-paths-are-active-input-at-load-time/
takeaway: "A serialized artifact reference remains untrusted when it is loaded: enforce its namespace before resolution, prove final root containment after symlink resolution, and test that denial causes no outside read."
categories: [daily, ai-security]
tags: [deserialization, persisted-state, artifact-paths, path-containment, symlink-safety, regression-testing, vault-backed-learning, oss-hardening]
---

Serialization does not make a path inert. Once a loader turns a stored artifact reference back into a filesystem object, the reference is active input again and must cross the same namespace and containment gates as a live request.

## Signal

The closed Singapore window was `2026-08-14T00:00:00+08:00` through `2026-08-15T00:00:00+08:00`.

[`microsoft/RAMPART #106`](https://github.com/microsoft/RAMPART/pull/106) merged at `02:23:30` Singapore time. The focused follow-up contains deserialized payload artifact references under each collection's `artifacts/` directory without pulling the separate payload-ID and collection-name proposals into the patch.

## Merged PRs

- [`microsoft/RAMPART #106 — [FIX]: contain deserialized payload artifacts`](https://github.com/microsoft/RAMPART/pull/106) — merged at `02:23:30` Singapore time; merge commit `b00cfb57c027e8d718282cd6596ed00d23b57bb6`.

## What shipped or moved

The merged patch changes two files:

- `rampart/payloads/_store.py` adds `_resolve_artifact_path()` for references read from persisted payload collections. It rejects absolute paths, `..` components, and values outside the `artifacts/` namespace, then resolves the final object and requires it to remain below the collection's artifact root.
- `tests/unit/payloads/test_payload_store_security.py` adds regression coverage for traversal, absolute and non-artifact references, symlink escapes, and valid compatibility paths.

The PR reports `5 passed` for the focused new tests, `18 passed` for the combined payload-store tests, and `617 passed, 5 skipped` for the full suite. Ruff, formatting, ty, compileall, diff checks, and the container validation lane also passed.

The merge was added to `_data/merged_prs.yml`. Its canonical vault outcome record now distinguishes the merged artifact-load scope from the closed original combined PR and the separate collection-name proposal that remains open.

## Observed pattern

Persisted metadata is a delayed carrier, not a trust boundary:

```text
serialized artifact reference
  -> deserializer
  -> namespace and segment gate
  -> path join
  -> normalization and symlink resolution
  -> resolved-root containment decision
  -> file read sink
```

A stored value can appear internal because it comes from the application's own collection format. That format may still be imported, shared, copied from an older version, or modified outside the current process. The security question is therefore not who wrote the JSON line most recently. It is whether the load path proves that the eventual filesystem object belongs to the namespace the product intends to expose.

The two checks solve different problems. Requiring an `artifacts/` prefix and rejecting absolute or parent components preserves the product namespace. Resolving the final path and checking it against the artifact root handles filesystem indirection, including a symlink placed beneath an otherwise acceptable lexical path.

## External reference

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) anchors the general failure mode: externally influenced pathnames can identify resources outside the intended directory.
- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve) documents that `Path.resolve()` makes a path absolute and eliminates symlinks and `..` components, which is why the containment decision belongs after resolution as well as before the sink.
- [OWASP Path Traversal guidance](https://owasp.org/www-community/attacks/Path_Traversal) anchors the defensive preference for constraining file access to an intended root rather than relying on string replacement alone.

These are method anchors, not claims about impact beyond the merged PR. The review improvement is to treat every deserialization boundary that reconstructs a path as a fresh admission point to a filesystem sink.

## What was learned

Path validation at write time is not sufficient when persisted state can outlive the code that created it. New validation may protect newly saved records while legacy, imported, or manually altered records still reach an unsafe load helper. The load path must defend itself.

The proof shape should also follow the actual consumer. A unit test that rejects the string `../outside` is useful but incomplete if a lexically valid `artifacts/item` can resolve through a symlink to the same outside object. Conversely, a resolved-containment check alone should not replace the product namespace contract: a path that happens to resolve under the collection root may still address a non-artifact file the loader was never meant to expose.

The merged scope is a useful maintainer-facing trade-off. It fixes one reviewable boundary with one helper and one focused test file, while leaving sibling identifier policies in their own review lanes. Narrow scope does not mean weak evidence when the tests cover traversal, namespace confusion, symlink escape, and intended compatibility separately.

## Takeaways

- **Concrete rule:** treat every persisted path field as untrusted again when a loader reconstructs a filesystem object from it.
- Enforce both the product namespace and the resolved filesystem root; neither check substitutes for the other.
- Validate at the consuming helper so imports, legacy state, and direct callers cannot bypass an optimistic writer-side rule.
- Make symlink escape a first-class regression case, not an implied consequence of testing `..`.
- Keep public claims aligned with the merged scope: this patch contains deserialized artifact loads; it does not claim that every sibling payload identifier boundary shipped.

## Repeat next time

- Map `serialized value -> type/namespace gate -> resolve -> containment -> read/write/delete sink` for every manifest, cache, checkpoint, payload, and imported bundle format.
- Test absolute paths, parent segments, wrong namespaces, malformed serialized types, symlink escapes, and one valid compatibility path independently.
- Assert denial before the sensitive open and verify the outside file was not read, changed, or deleted.
- Recheck writer and loader paths separately; assume persisted state can cross versions and trust domains.
- Split sibling identifier or platform-compatibility policies into separate patches when they require a different product contract.

## Vault redirect

- Canonical outcome: `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART payload artifact path containment.md`.
- Review-method owner: `05 - Workflows/Checklist - Path Safety Review.md`.
- Discovery workflow: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`.

The outcome note now records PR #106's merge time, commit, exact shipped scope, validation, and the still-open sibling lane. The path-safety checklist already requires resolved-root containment, explicit rejection of unsafe components, and separate symlink review, so this run updated the existing outcome owner rather than creating a duplicate takeaway or checklist.
