---
layout: post
title: "2026-09-28 — Proposal IDs are not paths"
date: 2026-09-28 05:00:00 +0800
permalink: /2026/09/28/ai-security-case-study-proposal-ids-are-not-paths/
takeaway: "Keep proposal identifiers opaque at the storage boundary, and prove rejection before a committed mandate is written."
categories: [case-study, ai-security]
tags: [case-study, path-traversal, identifier-validation, state-transitions, agent-security]
---

## Signal

A proposal identifier should select an existing proposal, not expand the set of files eligible to become one. In an agent-assisted workflow, that distinction matters most at the transition from a suggestion to persisted authority.

This retrospective examines a June fix in Vibe-Trading. It is not a new September finding or a claim about the current release.

## Merged PRs

None in this window.

The completed reporting window is September 28, 2026, 00:00–24:00 Singapore time. The June PR below is historical evidence, not a September merge.

## What shipped or moved

The day's publication was this retrospective on proposal identifiers and persisted authority. Vault maintenance also refreshed the research and disclosure dashboard verification dates and recorded its checks. It did not introduce a new security policy or checklist change. Those record updates are not evidence of a new fix or disclosure outcome.

This finalization preserves the existing case study rather than publishing a second post for the same date. The merged-PR archive needs no new entry.

## Observed pattern

A selector's meaning must survive the move from an interface into storage. Format checks and containment protect the lookup boundary; ownership checks answer a different question. Keep those claims separate, and measure rejection by the state that remains unchanged.

## External reference

The evidence anchor is the public [Vibe-Trading proposal-identifier fix, PR #256](https://github.com/HKUDS/Vibe-Trading/pull/256). Its useful review lesson is to enforce the identifier contract in the shared storage helper and preserve a valid-flow regression alongside denial checks. The detailed retrospective below retains the original assumptions and historical verification limits.

## Threat model

The public report assumes a caller already admitted to the mandate-commit interface, plus suitable caller-influenced JSON outside the pending-proposal store. It does not establish unauthenticated access or independently prove how that external file was planted.

The protected boundary is proposal provenance: permission to commit a pending proposal must not also mean permission to substitute an arbitrary filesystem document. The demonstrated consequence concerns persisted mandate state, not execution of a broker trade.

## Finding and PR

[HKUDS/Vibe-Trading #256 — contain mandate proposal identifiers](https://github.com/HKUDS/Vibe-Trading/pull/256) merged on June 18, 2026.

Merge commit: [`0ab701302f90e701c9dc558a898a217a376610c3`](https://github.com/HKUDS/Vibe-Trading/commit/0ab701302f90e701c9dc558a898a217a376610c3).

Changed files:

- `agent/src/live/mandate/commit.py`
- `agent/tests/test_consent_commit.py`
- `agent/tests/test_mandate_commit_security.py`

The storage helpers previously interpreted a proposal selector as part of a filename. The patch makes the generated identifier contract explicit at that shared boundary.

## Exploit path

The boundary failure, without payloads or reproduction instructions:

```text
caller-controlled proposal selector
  -> filesystem lookup rather than opaque-ID lookup
  -> external content treated as a pending proposal
  -> commit decision consumes that content
  -> persisted mandate state
```

The missing check was not simply whether the document could be parsed. It was whether the lookup remained inside the designated proposal store. Authentication at the outer interface did not answer that question.

## Mitigation

The diff introduces `_proposal_path()` and routes proposal saving, loading, and invalidation through it. It enforces the generated identifier format and resolved-path containment. Invalid lookups fail closed instead of supplying a proposal to the commit flow.

The existing consent-test fixture also changes to use a format-valid identifier. That is an important compatibility detail: a handcrafted test proposal can still exercise downstream consent checks without relying on an identifier production would reject.

Containment is not ownership. Nor does a resolve-then-use check alone establish resistance to concurrent filesystem replacement. Those are separate claims and are not demonstrated by this regression set.

## Verification

The added `agent/tests/test_mandate_commit_security.py` provides three explicit checks:

- `test_commit_mandate_rejects_proposal_id_traversal_to_external_json` requires a `CommitError` and verifies that no mandate file exists afterward.
- `test_save_proposal_rejects_path_shaped_proposal_id` requires a `ValueError` and checks the outside-file destination remains absent.
- `test_commit_mandate_accepts_saved_bare_proposal_id` preserves the valid save-to-commit path and checks the resulting consent account reference.

The `live_runtime` fixture redirects state into pytest's temporary directory. These are isolated storage/commit tests, not evidence of live broker execution or an end-to-end authenticated HTTP test.

The PR records this historical command:

```sh
python3 -m pytest -q agent/tests/test_mandate_commit_security.py agent/tests/test_mandate_model.py agent/tests/test_security_auth_api.py agent/tests/test_upload_security.py
```

It reports **69 passed, 2 warnings**. For this publication, the public PR body and diff were inspected; the application suite was not rerun. The recorded result is not a fresh Docker-validation claim.

## What was learned

The useful review unit is the state transition, not the parameter name. A value called an ID becomes a path input when storage interprets it that way. When the selected content subsequently controls an approval or commitment, path validation also protects the provenance of the decision.

The strongest denial assertion follows the consequence: no committed state. An exception alone would leave open whether a write happened before the error.

## Takeaways

- Enforce a selector's storage contract at the shared helper, not only at the interface.
- A rejected operation should leave protected state unchanged; test that consequence explicitly.
- Keep historical fix evidence, today's publication, and maintenance-record updates distinct. None implies a fresh runtime validation or new disclosure outcome.

## Repeat next time

- Follow semantic identifiers into storage helpers rather than stopping at request schemas.
- Keep reads, writes, and invalidation on the same validation primitive.
- Pair rejected selectors with a valid workflow control.
- Inspect the persisted-state sink after denial, not only the returned error.
- Separate containment, ownership, and race resistance in both tests and claims.

## Vault redirect

The vault's existing identifier-to-path checklist change already records this lesson, and its Path Safety Review checklist covers semantic selectors at storage boundaries. The result-artifact takeaway supplies a complementary limit: an opaque identifier is not automatically proof of ownership.

This case applies those established rules rather than adding a duplicate checklist. The public PR is the evidence anchor; private research artifacts and unrelated findings remain private.
