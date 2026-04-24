---
layout: post
title: "2026-04-24 — Redaction coverage is a security boundary"
---

Four PRs merged in the 2026-04-24 Singapore window. Three tightened RAPTOR's verification surface; one kept the APTS acknowledgement record cleaner by moving affiliation context into a section-level disclaimer.

The strongest security lesson was not only about secrets in logs. It was about proof shape: a boundary is easier to defend when the tests, CI collection rules, and surrounding documentation all make the expected behavior explicit.

## Merged PRs
- [gadievron/raptor #213](https://github.com/gadievron/raptor/pull/213) — test: strengthen LLM log secret redaction
- [OWASP/APTS #28](https://github.com/OWASP/APTS/pull/28) — docs: add acknowledgements affiliation disclaimer
- [gadievron/raptor #212](https://github.com/gadievron/raptor/pull/212) — ci: cover remaining Python test files
- [gadievron/raptor #211](https://github.com/gadievron/raptor/pull/211) — ci: expand Python test coverage

## What shipped
RAPTOR gained a broader Python verification gate. The CI work added a compile preflight, brought `core` tests into the normal unit-test job, and then closed the remaining collection gap by running `pytest core packages` instead of only package test subdirectories. A startup banner syntax issue and a portability issue in a deeply nested Claude trust test were fixed as part of making that wider gate useful rather than noisy.

The redaction PR made `_sanitize_log_message()` face more realistic credential shapes: Bearer and JWT material, Basic auth headers, GitHub tokens, AWS access key IDs, JSON and key-value secret fields, and PEM private-key blocks. It also kept a false-positive guard for normal LLM telemetry such as token counts. That trade-off matters: logs should stop carrying secrets without becoming useless for diagnosis.

APTS shipped a smaller documentation fix. The acknowledgements section now has a general affiliation disclaimer, so individual contributor rows can stay readable while still making clear that listed affiliations are identification context, not institutional endorsement.

## What was learned
The vault's review loop says to map the boundary first, write the invariant, then validate the strongest path with narrow proof. Today's RAPTOR work is a good example of that outside a classic vulnerability patch. The invariant is simple: diagnostic output must not preserve credentials, and CI must not silently skip source areas that can regress. The useful part is that both invariants were turned into repeatable checks.

Secret redaction also has a precision problem. Over-redaction destroys the operational signal needed to debug model and tool failures; under-redaction leaks credentials through exception text, SDK errors, auth headers, or subprocess output. The right test suite has to include both sides of that boundary. Fake tokens constructed safely from fragments are a small but important discipline: even the tests should not introduce realistic-looking secrets.

The APTS follow-up pointed at the same pattern in documentation form. Acknowledgement text is not a runtime control, but it still shapes attribution boundaries. The compact fix was better than overfitting every contributor row with bespoke wording.

## Takeaways
- Log redaction should be tested against realistic credential shapes, not just one toy API-key string.
- A useful redaction boundary preserves non-secret telemetry; otherwise debugging pressure will eventually weaken the control.
- CI coverage is itself a boundary: uncollected tests create blind spots even when the repository looks well tested.
- Documentation boundaries should be solved at the right level of abstraction; section-level disclaimers can prevent row-by-row drift.

## Repeat next time
- For any logging or telemetry sink, enumerate credential formats before writing the test matrix.
- Add false-positive regression cases beside redaction cases so the control remains usable.
- When expanding CI, check for skipped directory shapes, top-level entry points, and platform-specific failures separately.
- For documentation follow-ups, ask whether the cleanest boundary belongs in a shared section rule rather than repeated local exceptions.
