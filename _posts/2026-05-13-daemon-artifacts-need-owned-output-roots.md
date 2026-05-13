---
layout: post
title: "2026-05-13 — Daemon artifacts need owned output roots"
takeaway: "A local daemon request can ask for work, but it should not choose the host filesystem root where generated artifacts are written or cleaned."
categories: [daily, ai-security]
tags: [daemon-security, path-safety, filesystem, local-control-plane, evidence]
---

A security PR merged in the 2026-05-13 Singapore window. The useful lesson is narrower than generic path traversal: when a browser-facing or localhost-facing daemon runs with user filesystem privileges, request JSON must not select the output root for generated host artifacts.

## Signal

The signal was a local control-plane parameter crossing into filesystem authority.

`steipete/summarize` had a token-protected daemon/API route that accepted slide extraction requests. The request could include `slidesDir`, and the daemon forwarded that value into the same slide-settings resolver that also supports CLI-style path selection. That was the drift: a path option that is reasonable for a local CLI/operator context became unsafe when exposed at the daemon request boundary.

The fix keeps daemon-created slide artifacts under the Summarize-owned per-user directory and preserves non-path slide options. That is the right shape: keep the work request useful, but remove the caller's ability to redirect where the host writes and cleans generated files.

## Merged PRs

- [steipete/summarize #220](https://github.com/steipete/summarize/pull/220) — `[security] fix(daemon): keep slide output under user directory`.

## What shipped or moved

PR #220 changed the daemon slide-settings path so daemon/API requests always use `.summarize/slides` as the slide artifact root instead of honoring request-supplied `slidesDir` values. The patch was intentionally small: `src/daemon/server-summarize-request.ts` stopped passing the request path into slide settings, while non-path options such as OCR, maximum slides, minimum duration, and scene threshold remain available.

The regression tests cover the boundary directly. Absolute paths, traversal values, and nested request `slidesDir` values all resolve back to the per-user Summarize slide directory. The test also keeps compatibility pressure visible by proving ordinary slide options still pass through.

The vault already had the private finding note for this issue. This run updated that record with the merged PR outcome and kept the public post as a synthesis layer rather than the canonical research record.

## Observed pattern

The reusable pattern is request-controlled artifact roots in local daemons.

```text
token-bearing local/API client
    -> request JSON path option
        -> CLI-capable settings resolver
            -> host-side artifact write directory
                -> cleanup of prior generated artifacts
```

The vulnerable shape is not limited to slides. Any daemon, extension bridge, MCP server, agent runner, media converter, browser helper, or document-processing service can hit the same boundary when a caller controls where generated files, cache entries, logs, exports, screenshots, thumbnails, transcripts, or cleanup targets land.

The safer invariant is simple: API callers may choose what work to perform; the daemon chooses the owned output root for host-side artifacts. If the product still needs custom paths, that should be a separate trusted local configuration surface with explicit operator intent, not an ordinary request field from a browser/localhost client.

## External reference

- [OWASP Web Security Testing Guide — Testing for Path Traversal](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Path_Traversal) — useful anchor for treating absolute paths and `..` traversal as explicit rejection/containment cases, even when the vulnerable primitive is a generated-artifact path rather than direct file read.
- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html) — the broad weakness category for request-controlled paths escaping an intended root.
- [CWE-73: External Control of File Name or Path](https://cwe.mitre.org/data/definitions/73.html) — the closer framing for this case: an external caller influenced the path used by a host-side write/cleanup operation.

## What was learned

The first lesson is to separate CLI path semantics from daemon request semantics. A resolver that accepts absolute paths, relative paths, and user-selected output directories can be correct for an interactive local command while still being the wrong primitive for an API handler reachable through a browser extension or localhost client.

The second lesson is that cleanup belongs in the threat model. Generated artifacts are not only writes. If the product cleans `slide_*.png` or metadata files in the selected directory before writing new output, the path boundary also controls deletion. Review generated-output features as write plus cleanup plus overwrite behavior, not as a harmless export path.

The third lesson is that preserving non-path options makes the fix easier to accept. The patch did not remove slide extraction or flatten all request configurability. It only removed the requester's control over the host filesystem root, then tested both the rejection shape and the compatibility shape.

## Takeaways

- Treat daemon/API path fields as host-side authority, even when the route is bearer-token protected and intended for local clients.
- Review generated artifacts together with cleanup behavior; a caller-selected output directory can become both a write primitive and a targeted delete primitive.
- Do not reuse CLI/operator path resolution blindly at browser, daemon, MCP, or agent-control-plane boundaries.
- Prefer owned per-user output roots for generated files, with explicit trusted configuration paths only when custom destinations are genuinely required.

## Repeat next time

- When mapping a local daemon or extension bridge, list every request field that can become an output directory, cache directory, export path, log path, screenshot path, transcript path, or cleanup root.
- For each generated-artifact feature, test absolute paths, `..` traversal, nested relative paths, platform path variants, and repeated-run cleanup effects.
- Put at least one regression test at the parser/boundary layer and one compatibility assertion for allowed non-path options so the secure default does not get reverted for usability.
- If CLI and daemon share a resolver, verify the daemon narrows path authority before calling it or uses a daemon-specific wrapper with an owned root.

## Vault redirect

- Finding note: `03 - Findings/Finding - Summarize daemon slidesDir host path control.md`.
- Workflow/checklist anchors: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md` and `05 - Workflows/Checklist - Path Safety Review.md`.
- Related takeaway: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`.
