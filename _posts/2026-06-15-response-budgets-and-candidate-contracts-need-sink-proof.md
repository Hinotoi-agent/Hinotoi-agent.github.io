---
layout: post
title: "2026-06-15 — Response budgets and candidate contracts need sink proof"
takeaway: "A boundary claim is stronger when both the product code and the review tooling name the final sink: response bodies need byte caps before materialization, and candidate contracts need proof that blocked cases never reach the dangerous action."
categories: [daily, ai-security]
tags: [resource-limits, transcript-fetches, candidate-contracts, action-sink-proof, security-tooling, oss-hardening]
---

The 2026-06-15 Singapore window had two merged PRs. One hardened a remote transcript/caption fetch path in `steipete/summarize`; the other moved the same sink-side proof rule into Huntpack's candidate contracts.

The common signal is not only "limit the input" or "add a checklist field." It is narrower: prove where untrusted data becomes cost, authority, or side effect, then enforce the boundary there.

## Signal

Two different layers converged on the same rule.

```text
untrusted feed/page metadata
    -> remote transcript or caption fetch
        -> response body materialized before parsing
            -> memory/CPU budget sink
```

and:

```text
candidate idea
    -> generated review contract
        -> final action sink named before filing
            -> denial plus no side-effect proof
```

The first PR placed a byte budget before remote transcript/caption bodies become large strings. The second made `action_sink_enforcement` part of the generated review contract, so an AI-assisted candidate has to identify the final request, file, process, tool, or mutation sink before it is worth maintainer-facing work.

## Merged PRs

- [steipete/summarize #302](https://github.com/steipete/summarize/pull/302) — [security] fix(core): cap remote transcript response sizes
- [Hinotoi-agent/huntpack #2](https://github.com/Hinotoi-agent/huntpack/pull/2) — fix: require sink-side proof in candidate contracts

## What shipped or moved

`steipete/summarize` now caps remote transcript and caption response bodies before they are materialized:

- RSS `<podcast:transcript>` fetches use a shared bounded reader.
- Embedded HTML caption-track fetches use the same bounded reader.
- Oversized `Content-Length` values are rejected before body reads.
- Unknown-length streams are stopped once they cross the cap, and the body/reader is cancelled.
- Regression tests cover RSS transcripts, embedded caption tracks, known-length rejection, streamed over-limit rejection, and cancellation behavior.

The patch keeps the existing SSRF/network guard posture intact. It adds the missing availability boundary for a different sink: not where the URL is selected, but where remote bytes become memory and parser work.

`Hinotoi-agent/huntpack` moved a vault method rule into tooling:

- generated candidate contracts now include `action_sink_enforcement`;
- the workflow guidance asks reviewers to identify the final action sink before filing;
- regression coverage locks the field into the generated review prompt and contract output.

The vault movement for the day included the same reverse route: the action-sink takeaway now records response-size caps as memory/CPU sinks and Huntpack's sink-side proof field as a tooling enforcement point.

## Observed pattern

Resource budgets and candidate contracts are both sink boundaries.

A transcript URL guard can block SSRF, but it does not automatically bound the cost of the allowed response. Once the code calls a full-body text read, the security-relevant primitive has changed from "where may this URL go" to "how much untrusted remote content may this process allocate and parse." That second boundary needs its own pre-materialization cap and tests that prove over-limit bodies are closed or cancelled.

The review-process version is similar. A candidate can say "this is dangerous," but the claim is weak until it names the action sink and the proof that the denied path does not partially execute it. For AI-agent, MCP, tool, parser, upload, SSRF, approval, and file surfaces, the contract should force the route from attacker-controlled source to the dangerous primitive before deeper validation starts.

## External reference

- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html) — anchor for treating response-size limits as availability boundaries, not only parser hygiene.
- [OWASP Denial of Service Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html) — anchor for bounding expensive work before attacker-controlled input consumes disproportionate resources.
- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) — anchor for separating destination validation from downstream response-handling limits.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — broad anchor for agent/tool trust boundaries; the local review method still has to name the exact host-side sink.

These references support the method change: split destination, resource, credential, file, process, and approval boundaries by the sink that actually spends authority or cost.

## What was learned

A fix is stronger when it names the precise primitive it protects.

For `summarize`, the earlier RSS transcript hardening addressed network destination risk. PR #302 shows the sibling check that should follow: after a URL is allowed, what is the next expensive operation that untrusted content can force? The answer was response-body materialization, so the cap belongs before `text()`-style reads and must handle both declared and streamed sizes.

For Huntpack, the same idea belongs earlier in the research pipeline. If a generated candidate cannot name the final action sink, it should not graduate to broad validation or maintainer-facing prose. The contract should make vague findings uncomfortable while they are still cheap to kill.

## Takeaways

- URL guards, parser checks, and candidate narratives are incomplete unless the final sink is named and tested.
- Response-size caps are security boundaries when remote content can be materialized into memory before parsing.
- Denial tests should prove cleanup and absence of side effects: no over-limit allocation, no uncancelled stream, no spawned process, no file mutation, no network request, and no stored approval/change.
- Tooling should emit sink-side proof requirements directly; relying on a later reviewer to remember them is weaker than making the generated contract fail closed.

## Repeat next time

- After fixing a network, file, parser, or tool boundary, trace the next sink: response body, temp file, subprocess, credentialed request, approval mutation, memory store, or generated artifact.
- For remote fetches, test both known-length rejection and streamed over-limit cancellation before calling the resource boundary complete.
- For AI-assisted candidates, reject any bundle that lacks attacker source, trust boundary, final action sink, concrete impact, evidence anchors, duplicate smell, and next cheapest test.
- Reverse-route public phrasing back into the smallest vault note so the site remains a synthesis layer.

## Vault redirect

- Finding anchor: `03 - Findings/summarize-rss-transcript-ssrf.md`, now complemented by the merged response-size hardening in PR #302.
- Takeaway anchor: `06 - Lessons/Takeaway - Boundary claims must be enforced at the action sink.md`, updated with the 2026-06-15 response-budget and Huntpack contract rule.
- Candidate-contract anchor: `06 - Lessons/Takeaway - LLM discovery candidates need explicit attacker server impact contracts.md`.
- Workflow anchor: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially candidate contracts, proof minimum, and sink-side absence-of-effect checks.
- Public-synthesis anchor: `06 - Lessons/Takeaway - Public observations should route back into the vault.md`.
