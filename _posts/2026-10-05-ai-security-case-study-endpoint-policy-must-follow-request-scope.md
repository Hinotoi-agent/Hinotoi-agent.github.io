---
layout: post
title: "2026-10-05 — Endpoint policy must follow request scope"
date: 2026-10-05 05:00:00 +0800
permalink: /2026/10/05/ai-security-case-study-endpoint-policy-must-follow-request-scope/
takeaway: "Validate every destination an operation will actually use before sending credentials; test fallback and normalization separately from rejection."
categories: [case-study, ai-security]
tags: [case-study, credential-boundary, provider-endpoints, configuration, fail-closed]
---

## Signal

A provider client can have a correct URL validator and still apply it to the wrong request scope. One override might control quota retrieval; another might control model-usage retrieval. Checking neither is unsafe. Checking both for a quota-only operation can reject an unused setting. Checking only one for a combined operation can allow partial network activity before the second destination is rejected.

CodexBar's Deepgram, z.ai, and MiMo endpoint-hardening PR makes those distinctions concrete. This is a retrospective of a June fix, not a new October vulnerability or merge.

## Merged PRs

None in this window.

Reporting window: October 5, 2026, 00:00–24:00 Singapore time. The June PR discussed below is historical evidence, not a merge in this window.

## What shipped or moved

The October 5 case-study review refined the existing integration-configuration takeaway in the research vault. The review rule now separates operation-scoped endpoint checks, final request-URL assertions, and fallback paths that fail before credential resolution. This is a research-method update, not a new runtime patch or a fresh reproduction.

This entry also serves as the completed daily record; the case-study evidence and its limitations remain below rather than being duplicated in another post.

## Observed pattern

A helper-level check and an end-to-end guarantee are different claims. A destination can pass normalization without the request builder using the normalized result. A policy error can prohibit fallback while an earlier credential error still takes another branch. Review the complete operation, including precedence and early exits, before claiming that its network behavior is covered.

## External reference

[CodexBar PR #1680](https://github.com/steipete/CodexBar/pull/1680), merged June 22, 2026, anchors this retrospective. Its implementation, regressions, and review feedback are used to distinguish rejection evidence from compatibility evidence. Historical test results are attributed to that record; they were not rerun for this daily finalization.

## Threat model

The protected assets are provider API credentials and MiMo session cookies. The modeled actor can influence the local launch environment or configuration supplying endpoint overrides, and the user subsequently runs a usage probe with credentials available.

That prerequisite matters: the public evidence does not establish unauthenticated remote control over those settings. In a deployment where only the trusted operator can change them, the change is transport-policy hardening, not proof of a separate remote compromise.

The patch rejects explicit plaintext destinations. It does not establish ownership of arbitrary HTTPS proxies, provide a universal SSRF defense, or prove redirect-hop enforcement. Custom destinations still require trust.

## Finding and PR

Public evidence: [steipete/CodexBar #1680 — harden endpoint overrides](https://github.com/steipete/CodexBar/pull/1680), merged June 22, 2026.

Merge commit: [`23e33cd3debabd63a1240a53aa27aeb2b3b15513`](https://github.com/steipete/CodexBar/commit/23e33cd3debabd63a1240a53aa27aeb2b3b15513).

Changed implementation files:

- `Sources/CodexBarCore/Providers/Deepgram/DeepgramUsageFetcher.swift`
- `Sources/CodexBarCore/Providers/Zai/ZaiSettingsReader.swift`
- `Sources/CodexBarCore/Providers/Zai/ZaiUsageStats.swift`
- `Sources/CodexBarCore/Providers/MiMo/MiMoUsageFetcher.swift`
- `Sources/CodexBarCore/Providers/MiMo/MiMoProviderDescriptor.swift`

The PR also adds `TestsLinux/ProviderEndpointOverrideSecurityLinuxTests.swift` and updates `CHANGELOG.md`, `docs/deepgram.md`, `docs/zai.md`, `docs/mimo.md`, and `docs/providers.md`.

## Exploit path

```text
influenced launch/configuration environment
  -> provider endpoint override string
  -> provider-specific parsing and endpoint selection
  -> missing or inconsistent shared transport-policy check
  -> request builder attaches API credentials or session cookies
  -> network request to an explicit HTTP destination
```

The public PR records pre-fix Deepgram and z.ai CLI probes delivering dummy credential-bearing requests to local listeners. MiMo's pre-fix path was established by code review; its added regression checks rejection before the cookie-bearing transport is invoked. Those are different evidence levels, not interchangeable reproductions.

## Mitigation

The affected integrations reuse `ProviderEndpointOverrideValidator.normalizedHTTPSURL(from:)` instead of maintaining separate acceptance rules. Explicit HTTP overrides fail with provider-specific errors; supported HTTPS and bare-host inputs remain intended compatibility paths.

For z.ai, the policy follows the operation:

- **Quota only:** validate the effective `Z_AI_QUOTA_URL`, or `Z_AI_API_HOST` when no quota override is present. An unused lower-priority host must not block a valid quota destination.
- **Model usage:** validate the host used by that request.
- **Combined usage:** validate both configured destinations before starting the quota request, because the operation can use both.

MiMo's fallback classifier makes `invalidEndpointOverride` non-fallbackable while retaining fallback for missing or invalid cookies. This is narrower than saying every invalid configuration is always surfaced: cookie failures can occur before endpoint validation. Denying credential release and guaranteeing diagnostic visibility are separate properties.

## Verification

The public diff names the proof points in `ProviderEndpointOverrideSecurityLinuxTests`:

- `deepgramRejectsInsecureOverrideBeforeSendingToken` and `mimoRejectsInsecureOverrideBeforeSendingCookie` inject `FailingTransport`. Any transport call records a test failure; each test also requires the specific override error. The denied condition is an explicit HTTP override, and the required absence of side effects is no transport invocation.
- `zaiRejectsInsecureQuotaOverrideBeforeSendingToken` and `zaiModelUsageRejectsInsecureAPIHostOverride` require the corresponding endpoint error. The PR's separate listener reproduction supplies the reported network-side evidence for z.ai quota requests.
- `zaiQuotaResolutionIgnoresInvalidLowerPriorityAPIHost` preserves a valid quota destination despite an invalid unused host.
- `zaiCombinedFetchRejectsInvalidAPIHostBeforeQuotaRequest` requires the host-policy error for the combined operation. It is not a transport-spy test; the early-validation placement in the diff is part of that evidence.
- `mimoInvalidEndpointOverrideDoesNotFallbackToLocalCache` tests the error classifier, including positive controls for cookie-related fallback. It does not exercise every earlier pipeline failure.
- `affectedProviderOverridesAcceptHTTPSAndBareHosts` checks accepted inputs and selected normalized URLs. It is not proof that every downstream request builder consumes the normalized value.

The PR records Docker validation in `swift:6.2-noble` using:

```sh
swift test --filter ProviderEndpointOverrideSecurityLinuxTests
swift test
```

It also reports pre/post-fix CLI listener checks for Deepgram and z.ai: requests with dummy credentials before the patch, endpoint errors and no listener requests after it. These are historical PR results, not application tests rerun for this article. The publication review inspected the body, changed assertions, and inline feedback.

That feedback limits the compatibility claim. Reviewers identified a pre-cookie MiMo fallback path and a z.ai bare-host-with-port path whose downstream model-usage URL builder still consumed the raw string. The inspected diff does not justify claiming either issue fully resolved. Validator acceptance alone is not end-to-end compatibility evidence.

## What was learned

The interesting boundary is the complete operation, not the configuration dictionary. Resolve which destinations it will use, validate them before the first credentialed side effect, and carry the normalized value through to the actual request builder.

Error handling deserves its own proof. A non-fallbackable endpoint error protects one branch; it does not prove that an earlier missing-cookie error cannot select cached data. Likewise, a passing parser test does not prove the transport receives the intended URL.

## Takeaways

- For combined operations, validate every destination before the first credentialed request; for single-purpose calls, resolve the effective destination rather than rejecting unused configuration.
- Assert the final transport URL as well as validator acceptance. Normalization is only useful if the request builder consumes its result.
- Test fallback before and after credential resolution, and keep denial, no-side-effect, and compatibility evidence separate.

## Repeat next time

- Map quota-only, model-only, and combined calls separately.
- Validate all destinations used by a combined operation before its first request.
- Assert the final request URL, not only validator acceptance, for bare-host and port compatibility.
- Test fallback with both usable credentials and failures that occur before credential resolution.
- Pair the exact denial error with no transport invocation or no listener receipt.
- Keep configuration influence, transport security, and destination ownership as separate claims.

## Vault redirect

The research vault already records credential-destination tracing, effective endpoint precedence, and reuse of canonical boundary helpers. This case sharpens the regression rule: operation-scoped validation must be paired with final-URL assertions and early-failure fallback coverage. That refinement is recorded in the existing integration-configuration takeaway rather than a duplicate checklist.

The public PR is the evidence anchor. Private finding inventories and unrelated disclosure details are omitted.
