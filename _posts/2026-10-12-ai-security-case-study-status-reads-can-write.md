---
layout: post
title: "2026-10-12 — Status reads can write"
date: 2026-10-12 05:00:00 +0800
permalink: /2026/10/12/ai-security-case-study-status-reads-can-write/
takeaway: "Trace status and result tools through reconciliation: a read-shaped interface can still reach a filesystem write sink."
categories: [case-study, ai-security]
tags: [case-study, mcp, path-traversal, state-reconciliation, agent-security]
---

## Signal

A tool called `get_run_result` sounds observational. That name says nothing about whether loading a result repairs and persists the underlying state.

This retrospective examines Vibe-Trading's June MCP swarm fix. It is not a new October vulnerability or a claim about the current release. The useful distinction from a conventional path lookup is the write hidden behind a status read.

## Threat model

The public report assumes a caller with access to the configured MCP swarm tools. The caller controls a run identifier. Exploitation also requires an outside directory containing a parseable swarm `run.json`, with the relevant artifact destinations writable by the application.

Those conditions matter: the proof does not establish unauthenticated access, arbitrary-byte file writes, or how an attacker independently plants the outside run document. The protected boundary is the designated swarm run store, not admission to the MCP server itself.

## Finding and PR

[HKUDS/Vibe-Trading #258 — contain swarm run identifiers](https://github.com/HKUDS/Vibe-Trading/pull/258) merged on June 18, 2026.

Merge commit: [`f45fd85392f07b5e404e41d4fcb0ef0d6c2f87ab`](https://github.com/HKUDS/Vibe-Trading/commit/f45fd85392f07b5e404e41d4fcb0ef0d6c2f87ab).

Changed files:

- `agent/mcp_server.py`
- `agent/src/swarm/store.py`
- `agent/tests/test_swarm_retry.py`
- `agent/tests/test_swarm_status_hydration.py`

HTTP-side traversal checks did not cover the sibling MCP path. The storage helper still interpreted the caller's run selector as a path component without enforcing a bare-name contract.

## Exploit path

```text
caller-controlled MCP run identifier
  -> status/result/retry wrapper
  -> SwarmStore.run_dir joins an unchecked selector
  -> outside run.json is accepted as run state
  -> reconciliation runs with write=True
  -> task, event, and run-state persistence outside the intended store
```

The missing policy decision was whether the selector was a valid run-directory name before loading state. Successful parsing was not evidence that the selected state belonged to the store. Reconciliation then converted the lookup error into an out-of-store mutation.

## Mitigation

The patch places the identifier guard in `SwarmStore.run_dir()`, before the filesystem lookup. It rejects blank, absolute, multipart, dot-component, slash-containing, and backslash-containing values. MCP status, result, and retry wrappers turn the resulting `ValueError` into structured JSON errors.

This keeps ordinary bare run names usable while applying the same rule to storage callers. It is a lexical identifier guard; the diff does not establish symlink containment, ownership enforcement, or race resistance. Those need separate evidence rather than broader claims about this patch.

## Verification

The added result regression, `test_mcp_run_result_rejects_path_shaped_run_id_without_outside_write`, uses pytest temporary directories and the actual MCP wrapper. A crafted outside run is available to load. The assertions require an error identifying `run_id` and confirm that neither an outside `tasks/` directory nor `events.jsonl` is created.

`test_retry_run_rejects_path_shaped_run_id` separately checks the retry wrapper's structured denial. It does not contain the same filesystem-absence assertions; do not silently give both tests the stronger proof claim.

Existing compatibility coverage at the merge commit includes:

- `test_get_swarm_status_surfaces_live_progress`: a valid stored run still returns running/in-progress state.
- `test_get_swarm_status_auto_recovers_zombie`: a valid stale run still reaches the intended recovery path and persists failed state inside its store.

The public PR records this focused command:

```sh
python3 -m pytest -q agent/tests/test_swarm_status_hydration.py::test_mcp_run_result_rejects_path_shaped_run_id_without_outside_write agent/tests/test_swarm_retry.py::test_retry_run_rejects_path_shaped_run_id
```

It reports **2 passed, 1 warning** in Docker and **103 passed, 2 warnings** for the broader local swarm/path/auth suite. These are historical PR results. This publication reviewed the public body, diff, and merge-commit test source; it did not rerun application tests or Docker.

The negative result test proves absence of the named task/event artifacts, not byte-for-byte preservation of every outside file. A future stronger regression could also compare the original run document before and after denial.

## What was learned

Classify an operation by its strongest reachable side effect, not its verb. Status hydration, recovery, reconciliation, and lazy repair deserve the same sink tracing as explicit writes.

Interface parity also matters. An HTTP route's validation cannot protect an MCP wrapper that reaches the same helper independently. The shared storage contract is the useful place to stop that drift.

## Repeat next time

- Follow read-style tools through recovery and persistence before calling them read-only.
- Compare HTTP, MCP, CLI, and background callers of the same storage helper.
- Reject invalid identifiers before loading state that may trigger reconciliation.
- Assert denial and absence of the concrete write artifacts; preserve a valid recovery control.
- Keep lexical validation, resolved-path containment, and ownership as separate review questions.

## Vault redirect

The canonical finding already captures the MCP-to-storage-to-reconciliation chain. This publication's proof limits and repeat-next-time rule are routed back there: distinguish an error response from demonstrated absence of writes, and record exactly which artifacts each regression observes. No private finding inventory or unrelated disclosure material is published.
