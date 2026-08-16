---
layout: post
title: "2026-08-17 — Deserialized artifacts need containment at load time"
date: 2026-08-17 05:00:30 +0800
permalink: /2026/08/17/ai-security-case-study-deserialized-artifacts-need-containment/
takeaway: "Persisted path metadata is active input: validate its namespace and type, resolve filesystem objects, and prove containment before a loader returns them to the application."
categories: [case-study, ai-security]
tags: [case-study, path-traversal, symlink, deserialization, artifact-security, file-boundary]
---

AI security tooling often persists payloads, attachments, or evaluation artifacts for later reuse. The dangerous boundary is not only the initial upload. A serialized reference becomes active input when a loader turns it back into a filesystem object.

## Signal

A payload collection can look passive on disk while still carrying authority over later file access. In RAMPART, each JSONL record could include an artifact path that the loader reconstructed as a `Path`. That makes a shared or otherwise untrusted collection a file-boundary input, not merely stored metadata.

The public fix is deliberately narrow defense-in-depth. It contains deserialized artifact references without claiming that every persisted collection is attacker-controlled or that the separate payload-ID and collection-name questions were fixed by the same patch.

## Threat model

The bounded threat model is a user or process that can supply or modify a persisted payload collection before a more trusted RAMPART process loads it. The actor controls the serialized `artifact` value and may also control filesystem objects under the collection, including symlinks.

The security objective is simple: loading that collection must not return an artifact outside the collection's own `artifacts/` directory. Legitimate in-directory artifacts must continue to round-trip normally.

## Finding and PR

Public PR: [`microsoft/RAMPART #106 — [FIX]: contain deserialized payload artifacts`](https://github.com/microsoft/RAMPART/pull/106).

Merge commit: [`b00cfb57c027e8d718282cd6596ed00d23b57bb6`](https://github.com/microsoft/RAMPART/commit/b00cfb57c027e8d718282cd6596ed00d23b57bb6).

Changed files:

- `rampart/payloads/_store.py` — adds serialized-reference validation, resolved containment checks, and an explicit `artifacts/` load boundary.
- `tests/unit/payloads/test_payload_store_security.py` — covers traversal, absolute and non-artifact paths, malformed types, artifact symlink escapes, and an `artifacts/` directory symlink escape.

Before the patch, deserialization joined the collection directory with the stored artifact value and accepted the result when it existed. Absolute paths, `..` traversal, or a symlink could therefore make the reconstructed payload point outside the intended artifact root.

## Exploit path

The public source-to-sink chain was:

```text
attacker-influenced artifact value in payloads.jsonl
  -> json.loads()
  -> PayloadStore._deserialize()
  -> collection directory joined with the stored path
  -> existence check on the resulting filesystem object
  -> Payload returned with an out-of-root artifact Path
  -> later artifact consumer can read the referenced file
```

Examples covered by the regression suite include `../outside.pdf`, `artifacts/../outside.pdf`, an absolute `/tmp/outside.pdf` reference, and `artifacts/linked.pdf` where `linked.pdf` resolves through a symlink to an outside file. A second case replaces the collection's entire `artifacts/` directory with a symlink to an outside directory.

The relevant policy decision is not whether the string starts with a plausible prefix. It is whether the final filesystem object, after normalization and symlink resolution, remains beneath the intended root.

## Mitigation

The merged patch separates the boundary into explicit checks:

1. `_validate_artifact_reference()` requires a string, rejects absolute paths and any `..` component, requires the `artifacts/` namespace, and returns only the path relative to that namespace.
2. `_resolve_artifact_path()` joins that relative path beneath the expected artifact directory and checks the resolved result against the resolved root.
3. `load()` separately proves that the `artifacts/` directory itself resolves inside the collection directory, preventing a directory-level symlink escape.
4. Missing but otherwise valid artifacts retain the existing `FileNotFoundError` contract; malformed or escaping references fail with a bounded `ValueError`.

This combines lexical rejection with filesystem-object containment. Either check alone is incomplete: lexical checks do not settle symlinks, while resolution without a clear namespace contract can preserve ambiguous serialized input.

## Verification

The security regression file names the negative proof directly:

- `test_payload_store_rejects_deserialized_artifact_escape`
- `test_payload_store_rejects_non_string_deserialized_artifact`
- `test_payload_store_rejects_deserialized_artifact_symlink_escape`
- `test_payload_store_rejects_deserialized_artifacts_directory_symlink_escape`
- `test_payload_store_rejects_missing_deserialized_artifact`

The denial condition is a `ValueError` before an escaping reference is returned as a payload artifact. The positive compatibility control remains in `tests/unit/payloads/test_store.py`: `test_load_roundtrip_binary` and `test_path_based_payload_roundtrip` save legitimate artifacts, load them, and confirm their original bytes remain readable.

The PR recorded these commands and results:

```sh
uv run pytest tests/unit/payloads/test_payload_store_security.py -q
# 5 passed

uv run pytest tests/unit/payloads/test_store.py tests/unit/payloads/test_payload_store_security.py -q
# 18 passed

uv run pytest -q
# 617 passed, 5 skipped

uv run ruff check rampart/payloads/_store.py tests/unit/payloads/test_payload_store_security.py
uv run ruff format --check rampart/payloads/_store.py tests/unit/payloads/test_payload_store_security.py
uv run ty check rampart/payloads/_store.py tests/unit/payloads/test_payload_store_security.py
python -m compileall -q rampart tests
git diff --check
```

Ruff, formatting, type checking, compileall, and the diff check passed. A Python 3.12 container run of the combined 18-test payload-store lane plus Ruff, ty, and the whitespace check also passed.

## What was learned

Persisted metadata is not inert when deserialization gives it filesystem meaning. The review unit should be the complete reconstruction chain:

```text
serialized reference
  -> type and namespace gate
  -> path construction
  -> normalization and symlink resolution
  -> root-containment decision
  -> file-bearing object returned to downstream code
```

This also shows why path hardening has multiple contracts. Serialized-input semantics need deliberate errors for malformed values. Identifier or namespace semantics need compatibility-aware lexical rules. Filesystem-object semantics need containment after resolution. A fix can handle traversal text and still miss a symlink, or stop a symlink while accidentally narrowing valid persisted data.

## Repeat next time

- Treat archive manifests, JSONL records, checkpoints, caches, and database path fields as active input when they are rehydrated.
- Test absolute paths, `..` at multiple positions, malformed types, empty/root-only references, file symlinks, and directory symlinks.
- Prove containment on resolved paths; do not rely on string prefixes.
- Assert both sides of the contract: escaping references fail before a file-bearing object is returned, while a legitimate artifact still round-trips and remains readable.
- Keep the patch scoped to the demonstrated load boundary and state separately which adjacent identifier or storage questions remain out of scope.

## Vault redirect

The canonical research record remains in the private OSS Vulnerability Research Vault. The existing RAMPART security-PR note owns the maintainer outcome, split-patch history, validation record, and durable closure rule.

No new vault checklist was created for this publication. The reusable rule already belongs to the Path Safety Review: trace `serialized reference -> namespace/type gate -> resolution -> root containment -> read sink`, then prove rejection and the valid compatibility path. This post is the public-safe synthesis of that existing record, not a parallel source of truth.
