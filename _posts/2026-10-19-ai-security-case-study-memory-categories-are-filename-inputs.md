---
layout: post
title: "2026-10-19 — Memory categories are filename inputs"
date: 2026-10-19 05:00:00 +0800
permalink: /2026/10/19/ai-security-case-study-memory-categories-are-filename-inputs/
takeaway: "A tool-schema enum is not a storage boundary: validate every caller-controlled filename component before writing."
categories: [case-study, ai-security]
tags: [case-study, agent-memory, path-traversal, tool-schema, filesystem-boundary]
---

## Signal

The title was sanitized. The category was not. Both became part of the same memory filename.

This retrospective examines a June fix in Vibe-Trading, not a newly discovered October issue. Its useful lesson is about composition: hardening one input does not make a filename safe when a second input can still supply path separators.

## Merged PRs

None in this window.

Daily record finalized for October 19, 2026, 00:00–24:00 Singapore time. The June merge below is historical context, not work merged in this reporting window.

## What shipped or moved

The day's publication revisited the persistent-memory fix and recorded a more precise evidence boundary in the canonical finding: wrapper denial, direct-storage rejection, outside-file absence, and valid-category compatibility are separate claims. No new runtime fix shipped in this window, and application tests were not rerun for publication.

## Observed pattern

A filename can remain unsafe after its most obvious input is sanitized. Review category prefixes and other semantic labels as filesystem inputs whenever they participate in destination construction. The enforcement point matters more than the schema's description of allowed values.

## External reference

The public evidence anchor is [Vibe-Trading PR #257](https://github.com/HKUDS/Vibe-Trading/pull/257). Read its storage guard and regression diff together: the review-method change is to distinguish what a test actually asserts from what its name appears to promise.

## Threat model

The public report assumes an already-admitted caller that can invoke the `remember` tool with crafted arguments. The caller controls `memory_type`, title, and content. The destination outside the configured memory directory must already exist and be writable by the application.

The demonstrated impact is an out-of-root Markdown write with application-generated frontmatter and a `.md` suffix. It is not evidence of unauthenticated access, arbitrary-byte writes, credential exposure, or code execution. Admission to a tool and permission to choose its filesystem destination are different boundaries.

## Finding and PR

[HKUDS/Vibe-Trading #257 — validate persistent memory types](https://github.com/HKUDS/Vibe-Trading/pull/257) merged on June 18, 2026.

Merge commit: [`2e78f1402d7eda5ef466f294543f964f2950b603`](https://github.com/HKUDS/Vibe-Trading/commit/2e78f1402d7eda5ef466f294543f964f2950b603).

Changed files:

- `agent/src/memory/persistent.py`
- `agent/src/tools/remember_tool.py`
- `agent/tests/test_remember_tool_security.py`

The tool schema described an enum, but the storage implementation did not enforce it. Earlier memory hardening covered title/body handling; this patch addresses the separate category prefix.

## Exploit path

```text
admitted caller supplies a path-shaped memory_type
  -> RememberTool save dispatch passes the category to storage
  -> PersistentMemory.add sanitizes the title-derived slug only
  -> unchecked category is prepended to that slug and a .md suffix
  -> the joined destination escapes the intended memory directory
  -> the application writes a Markdown memory document outside its root
```

The public temporary-directory proof used `../outside/proof` with the title `Traversal Proof`. Vulnerable code created `outside/proof_traversal_proof.md`. The missing policy decision was category membership before filename construction—not whether the supplied title could be converted into a slug.

## Mitigation

`PersistentMemory.add()` now checks the existing `MEMORY_TYPES` allowlist before constructing the filename. The permitted categories remain `user`, `feedback`, `project`, and `reference`. `RememberTool._save()` catches the resulting `ValueError` and returns a structured error.

Putting the rule in storage protects direct callers as well as the tool wrapper. This is a category-validation fix, not proof of general symlink containment or race resistance.

## Verification

The added `test_remember_rejects_memory_type_path_traversal` exercises the real `RememberTool` with a pytest temporary memory directory and an existing sibling directory. It asserts both a structured error naming `memory_type` and the absence of `outside/proof_traversal_proof.md`.

The separate `test_persistent_memory_rejects_unknown_memory_type` calls storage directly and requires `ValueError`. Despite its broad name, its supplied value is traversal-shaped; it does not independently test a harmless-looking unknown category such as `custom`.

Existing positive controls at the merge commit include `TestAdd.test_creates_file_and_index`, which checks a valid project memory and its index, and `TestAdd.test_multiple_adds`, which saves project, user, and reference entries. `TestAdd.test_frontmatter_structure` covers a feedback entry.

The public PR records focused local and Docker validation using:

```sh
python3 -m pytest -q agent/tests/test_remember_tool_security.py agent/tests/test_persistent_memory.py
```

It also records Docker Ruff validation, and explicitly excludes a full-suite claim. These are historical PR results. This publication reviewed the PR body, diff, and merge-commit compatibility tests; it did not rerun application tests or Docker.

The negative wrapper test proves that the named outside file is not created. It does not assert byte-for-byte preservation of a pre-existing outside file or exercise the full registry/MCP transport.

## What was learned

A schema can describe allowed arguments without making every execution path enforce them. The component that turns those arguments into a write destination needs its own invariant.

Review the whole filename expression. Prefixes, category labels, identifiers, and extensions deserve the same scrutiny as the obvious title or path field. A narrow semantic allowlist can preserve the intended feature without accepting arbitrary path syntax.

## Takeaways

- Validate every caller-controlled filename component at the storage boundary; sanitizing the title alone does not constrain a category prefix.
- Keep rejection, absence of a new outside file, and preservation of an existing file as distinct proof obligations. Report only the assertions the tests actually make.

## Repeat next time

- Enumerate every caller-controlled component of a constructed filename.
- Compare schema declarations with the checks actually reached by direct and wrapper callers.
- Enforce category membership before path construction or writes.
- Pair denial with an explicit sink-side absence assertion and valid-category controls.
- Test an unknown plain category separately from traversal, and pre-existing destinations separately from new files.

## Vault redirect

The canonical research finding retains the source-to-sink chain. This publication routes back the sharper verification rule: distinguish wrapper denial, direct-storage rejection, outside-file absence, and valid-category compatibility. Historical test evidence remains labeled as historical; private research artifacts are not required to follow the public PR.
