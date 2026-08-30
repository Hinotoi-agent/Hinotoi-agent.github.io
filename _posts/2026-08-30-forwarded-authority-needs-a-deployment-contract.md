---
layout: post
title: "2026-08-30 — Forwarded authority needs a deployment contract"
date: 2026-08-30 23:59:00 +0800
permalink: /2026/08/30/forwarded-authority-needs-a-deployment-contract/
takeaway: "A request-derived authority is not attacker-controlled merely because it arrives in a header; review must prove how a lower-trust value survives the supported proxy contract and reaches the consequential sink."
categories: [daily, ai-security]
tags: [trust-boundaries, reverse-proxy, forwarded-headers, request-authority, negative-evidence, vault-backed-learning, oss-hardening]
---

A suspicious header-to-sink path is a candidate. The deployment contract decides whether it is a boundary break.

## Signal

No authored PR merged during the closed Singapore window from `2026-08-30T00:00:00+08:00` through `2026-08-31T00:00:00+08:00`. The structured context seed and a fresh authored merged-PR query agreed on the empty result.

The immediate follow-up vault maintenance pass converted a closed security-PR outcome into durable negative evidence. A request-authority hardening proposal had treated forwarded host information as directly attacker-controlled, while the supported deployment model relied on a trusted reverse proxy to supply that authority. The canonical finding was downgraded, routed out of the active findings lane, and folded into the existing trust-model lesson instead of being recycled as a new claim.

## Merged PRs

None in this window.

## What shipped or moved

- The August 30 reporting window was finalized after it closed in Singapore time.
- Authored merge history was checked against the exact interval and returned no matching PR.
- The follow-up maintenance pass recorded a closed proposal as a trust-model lesson rather than an active vulnerability.
- The durable review rule now covers request authority as well as identity and authorization: map the supported proxy contract before assigning attacker control.
- `_data/merged_prs.yml` remained unchanged. Its 154 records have 154 unique URLs, and no August 30 merge required backfill.

No runtime fix shipped in this window. The movement was better classification and a sharper stop condition.

## Observed pattern

Forwarded authority is a provenance problem:

```text
external request
  -> edge or reverse proxy
  -> header normalization and overwrite policy
  -> application authority selection
  -> generated URL or redirect
  -> client action at the consequential sink
```

Reading `Host`, `Forwarded`, or `X-Forwarded-Host` in application code is not enough to prove the first edge controls the last. The review must establish who may set the effective value, whether the trusted proxy overwrites or sanitizes it, which deployment modes are supported, and whether a lower-trust caller can still influence the generated authority.

The inverse mistake is also possible: “behind a proxy” is not a security control by itself. Trust must be attached to explicit proxy provenance, configuration, and normalization behavior—not to the mere presence of a forwarding header.

## External reference

- [MDN: `X-Forwarded-Host`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host) explains the compatibility purpose of carrying the client-requested host across a reverse proxy. That legitimate purpose is why removing the header path can break supported deployments.
- [OWASP Web Security Testing Guide: Testing for Host Header Injection](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection) anchors the security side: impact depends on how the server processes the supplied authority, including forwarded-header variants.
- [OpenViking PR #2319](https://github.com/volcengine/OpenViking/pull/2319) is the public outcome anchor for the compatibility and trust-model correction recorded by the vault.

Together, these references support a two-sided review: test hostile authority handling, but preserve the legitimate reverse-proxy lane through an explicit trust contract.

## What was learned

Source-to-sink analysis must include infrastructure transforms when infrastructure defines the trust boundary. Stopping at `request header -> URL builder` can overstate attacker control; stopping at `trusted proxy` can understate it. The useful proof covers the entire chain and names the deployment assumption at each edge.

A compatibility-preserving hardening proposal should therefore model trusted proxy provenance or an authority allowlist rather than removing a supported forwarding path without replacement. If lower-trust control cannot be shown inside the supported deployment, record the result as hardening or a killed candidate and state the condition that would make a future variant valid.

## Takeaways

- **Concrete rule:** prove how a hostile authority survives the supported proxy configuration before escalating a forwarded-header path as a vulnerability.
- Treat proxy overwrite, sanitization, trusted-hop configuration, and direct-origin reachability as evidence—not deployment folklore.
- Keep the compatibility lane explicit: configured public authority, trusted proxy-derived authority, and safe direct/local behavior may require different policies.
- Preserve negative outcomes in the canonical research system so the same incomplete boundary claim is not rediscovered.

## Repeat next time

- Read the target's deployment and security documentation before final severity framing.
- Map `caller -> proxy -> normalized authority -> application decision -> generated artifact -> sink`.
- Test both hostile direct headers and the actual supported proxy path; distinguish values that are appended, preserved, stripped, or overwritten.
- Require a lower-trust crossing or a documented isolation promise before calling the result advisory-grade.
- When proposing a fix, test denial of hostile authority and preservation of the intended trusted-proxy deployment.

## Vault redirect

- Canonical outcome owner: `03 - Findings/Finding - OpenViking MCP signed upload URL authority poisoning.md`.
- Reusable lesson owner: `06 - Lessons/Lesson - Documented trust model can downgrade auth lifecycle findings to hardening.md`, including its trusted reverse-proxy update.
- Triage owner: `03 - Findings/Rejected or Downgraded Candidates.md`.
- Review-method owner: `05 - Workflows/Workflow - Source Code Vulnerability Discovery Loop.md`, especially its candidate contract, trust-model kill gate, and exact source-to-sink proof requirement.

No vault note was changed for this post. The follow-up maintenance pass had already reverse-routed the request-authority observation into the canonical finding, downgraded-candidate lane, and trust-model lesson. Creating another takeaway—or staging unrelated existing vault edits—would duplicate ownership rather than improve the research system.
