---
layout: post
title: "2026-07-23 — Path hardening has three contracts"
date: 2026-07-23 23:59:00 +0800
permalink: /2026/07/23/path-hardening-has-three-contracts/
takeaway: "A path validator must preserve identifier compatibility, reject platform aliases, and normalize malformed serialized values before the filesystem sink."
categories: [daily, ai-security]
tags: [path-safety, deserialization, compatibility, windows-paths, maintainer-feedback, regression-testing, vault-backed-learning, oss-hardening]
---

The strongest security review is often the second pass. Closing a traversal is not enough if the validator strands valid names, misses platform aliases, or lets malformed serialized values fail through accidental exceptions.

## Signal

No authored PR merged during the closed Singapore window from `2026-07-23T00:00:00+08:00` through `2026-07-24T00:00:00+08:00`.

The meaningful movement was maintainer feedback on three open RAMPART hardening PRs. One LLM-observation boundary was approved, while two payload-store patches were refined to preserve compatibility, cover Windows filename aliases, and normalize malformed deserialized artifact references.

## Merged PRs

None in this window.

## What shipped or moved

- [`microsoft/RAMPART #60`](https://github.com/microsoft/RAMPART/pull/60) received approval for treating prior target responses and evaluator rationales as untrusted observations rather than driver instructions.
- [`microsoft/RAMPART #59`](https://github.com/microsoft/RAMPART/pull/59) was revised after review to reject traversal and Windows alias cases without replacing the existing collection-name contract with a narrower ASCII-only grammar.
- [`microsoft/RAMPART #106`](https://github.com/microsoft/RAMPART/pull/106) fixed its build and made non-string artifact references fail through one explicit validation contract before path resolution.
- `_data/merged_prs.yml` remained unchanged because a fresh merged-PR query confirmed that none of these open PRs merged in the target window.

This was review and validation movement, not a claim that the fixes have shipped upstream.

## Observed pattern

Path safety is not one check. It is three connected contracts:

```text
external identifier or serialized value
  -> type contract
  -> product identifier contract
  -> platform path semantics
  -> normalized and resolved object
  -> containment decision
  -> read, write, or delete sink
```

The type contract decides whether the value is even a valid path-bearing field. The identifier contract distinguishes names from paths without breaking names the public API already supports. Platform semantics then account for aliases that string-level checks can miss, such as trailing periods or reserved device names on Windows. Only after those gates should normalization, symlink resolution, containment, and filesystem access occur.

The same structure appears in AI systems. A target-agent response or evaluator rationale begins as external content. Labelling or serializing it as data helps preserve its type at the next model boundary; it does not grant authority. For paths, JSON shape and string type are similarly only the first gate before product policy and the sink.

## External reference

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) anchors the core containment failure: externally influenced pathnames can escape the intended directory.
- [Microsoft: Naming Files, Paths, and Namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) documents Windows naming rules and reserved names that portable validators must consider.
- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html) anchors lexical path operations and resolved-path handling as distinct steps.

These references are not a replacement for the product contract. The method change is to test type validity, identifier compatibility, platform aliases, and resolved containment separately instead of treating one regex or one `resolve()` call as the whole boundary.

## What was learned

A positive allowlist can look secure while introducing a compatibility bug. If an existing API allowed spaces, Unicode, or long collection names, replacing that contract with a narrow ASCII grammar may strand stored data or make `list()` return names that `load()` and `delete()` reject.

The better rule is to reject values for a security reason tied to the sink: separators, dot entries, platform aliases, reserved basenames, containment escape, symlink escape, or the wrong serialized type. Preserve other names unless the product deliberately adopts a migration plan.

Malformed persisted values deserve the same discipline. `null`, arrays, objects, and numbers should not reach path operations and produce whichever `TypeError` happens to emerge. Reject them at the deserialization boundary with a stable error contract, then prove that no file read, write, or deletion occurred.

Maintainer review therefore tests more than whether the exploit is denied. It tests whether the patch encodes the actual public abstraction and remains portable across the platforms that abstraction claims to support.

## Takeaways

- Separate type validation, identifier policy, platform alias handling, and resolved containment in both code and tests.
- Preserve the existing public name contract unless a narrower grammar is intentional, documented, and migration-safe.
- Treat Windows trailing-dot/space aliases and reserved device basenames as collision cases, not cosmetic edge cases.
- Normalize malformed serialized path fields into one deliberate validation failure before filesystem access.
- Report open-PR movement as review progress, not as a shipped fix.

## Repeat next time

- Map `serialized value -> type gate -> identifier gate -> platform semantics -> resolve -> containment -> sink` before proposing a path fix.
- Add negative cases for `.` / `..`, separators, absolute paths, symlinks, trailing dots/spaces, reserved device names, and non-string JSON values.
- Add positive controls for every previously supported identifier class and verify `list`, `exists`, `save`, `load`, `manifest`, and `delete` agree on the same contract.
- Assert denial before the filesystem operation and absence of outside reads, writes, or deletion.
- Re-run focused tests, the full suite, formatting, type checks, documentation builds, and a container lane after maintainer-requested changes.

## Vault redirect

- Canonical outcome owner: `10 - Disclosure/Security PRs/Security PR - microsoft - RAMPART payload artifact path containment.md`.
- Workflow anchor: `05 - Workflows/Checklist - Path Safety Review.md`.
- The vault outcome note now records the split PRs, exact reviewed heads, validation state, and the three-contract rule. This public post keeps only the generic review lesson and public PR evidence; it does not create a parallel private record.