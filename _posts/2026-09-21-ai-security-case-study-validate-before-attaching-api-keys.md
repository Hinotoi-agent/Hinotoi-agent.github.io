---
layout: post
title: "2026-09-21 — Validate destinations before attaching API keys"
date: 2026-09-21 05:00:00 +0800
permalink: /2026/09/21/ai-security-case-study-validate-before-attaching-api-keys/
takeaway: "Endpoint configuration becomes a credential-release decision at the request builder; enforce the same policy there, not only in settings."
categories: [case-study, ai-security]
tags: [case-study, credential-boundary, provider-endpoints, secret-handling, secure-defaults]
---

## Signal

A provider endpoint looks like configuration until the client attaches an API key. In CodexBar's Azure OpenAI integration, deployment validation used a configured destination to build a credentialed request. Accepting a URL with a host was not enough to establish that the destination met the application's transport policy.

The useful change was not a new parser. It was applying the existing shared endpoint policy at both configuration resolution and the request builder.

## Merged PRs

None in this window.

Reporting window: September 21, 2026, 00:00–24:00 Singapore time. The June PR below is historical evidence, not a merge in this window.

## What shipped or moved

September 21's publication was this retrospective of an accepted endpoint-hardening fix, not a new product-code shipment. The concrete contribution is a bounded account of where validation runs, what the regression proves, and which trust questions remain outside the fix.

The review lesson is already recorded in the vault's integration-configuration takeaway: check the credentialed request boundary directly, including callers that bypass settings parsing. This article makes that existing rule concrete without adding a duplicate checklist.

## Observed pattern

Configuration validity and permission to release a credential are different decisions. The shared destination policy belongs at the request builder as well as the settings layer. A denial test should establish that transport was never invoked, while positive controls preserve supported configuration behavior.

## External reference

[CodexBar PR #1687](https://github.com/steipete/CodexBar/pull/1687) is the public evidence anchor for the mitigation and historical validation below. Its merge date is June 22, 2026. HTTPS policy, destination ownership, and control over endpoint configuration remain separate questions; the fix does not establish all three.

## Threat model

The protected asset is the configured Azure OpenAI API key. The relevant influence is over the endpoint setting or environment override used by the provider client. This is a configuration-assisted scenario: it requires the endpoint to be changed or accepted through an operator's setup process. The public PR does not establish unauthenticated remote control of that setting.

The boundary is between destination configuration and permission to send a secret-bearing request. Explicit plaintext transport and ambiguous URL forms should not pass simply because they can be parsed.

Custom HTTPS endpoints remain supported. HTTPS protects transport; it does not establish that an arbitrary endpoint belongs to Azure or is trusted to receive the key. This patch is endpoint-policy hardening, not a universal destination allowlist, complete SSRF defense, or removal of the need to trust configured proxies.

## Finding and PR

Public PR: [steipete/CodexBar #1687 — harden Azure OpenAI endpoint overrides](https://github.com/steipete/CodexBar/pull/1687).

Merge commit: [`ba16332c3c21e517ebd9c254f1421c84d867c141`](https://github.com/steipete/CodexBar/commit/ba16332c3c21e517ebd9c254f1421c84d867c141).

The PR merged on June 22, 2026. This is a retrospective of that accepted fix, not a new September finding.

Changed files:

- `Sources/CodexBarCore/Providers/AzureOpenAI/AzureOpenAISettingsReader.swift`
- `Sources/CodexBarCore/Providers/AzureOpenAI/AzureOpenAIProviderDescriptor.swift`
- `Sources/CodexBarCore/Providers/AzureOpenAI/AzureOpenAIUsageFetcher.swift`
- `Sources/CodexBar/Providers/AzureOpenAI/AzureOpenAIProviderImplementation.swift`
- `TestsLinux/AzureEndpointOverrideSecurityTests.swift`
- `Tests/CodexBarTests/AzureOpenAIUsageFetcherTests.swift`
- `docs/providers.md`
- `CHANGELOG.md`

## Exploit path

The failure can be summarized without a credential-capture recipe:

```text
influenced provider endpoint configuration
  -> settings parser produces a URL
  -> host-presence check substitutes for destination policy
  -> deployment-validation request builder attaches the API key
  -> network transport sends the credential-bearing request
```

Before the change, the settings reader preserved explicit URL schemes, and the fetcher checked for a host before constructing the request. That left an explicit non-HTTPS destination eligible for credentialed validation.

The missing decision was whether the destination was acceptable *before* attaching credentials. Configuration influence is a prerequisite, not something this case proves an arbitrary remote party possesses.

## Mitigation

`AzureOpenAISettingsReader.endpointURL(from:)` now trims existing saved input and calls `ProviderEndpointOverrideValidator.normalizedHTTPSURL(from:)`. The provider fetch strategy validates endpoint overrides before resolving them as usable configuration.

The fetcher independently applies that same shared validator to a directly supplied URL before constructing the request. This matters because a future caller need not go through environment parsing.

The policy rejects explicit HTTP, URL user information, and encoded host-delimiter forms. It preserves custom HTTPS endpoints, bare hosts normalized to HTTPS, and whitespace-padded saved settings. An intentional plaintext local setup now needs a different supported configuration; the patch does not silently exempt it.

The UI also distinguishes *configured* from *valid*: an invalid configured provider remains visible so it can return an actionable error rather than disappearing. Visibility is not authorization to send a request.

## Verification

The public diff provides concrete negative and compatibility evidence:

- `azureOpenAIHTTPOverrideIsRejectedBeforeAPIKeyRequest` calls the fetcher directly with a disallowed endpoint and a canary key. Its injected `CapturingTransport` records a test failure if invoked at all, and the test requires the precise invalid-override error. The proof is no transport invocation, not merely a final error message.
- `azureOpenAIEndpointOverrideMustBeHTTPSOrBareHost` checks HTTPS proxy paths, bare-host normalization, host-and-port normalization, and whitespace trimming, alongside rejection cases. These are positive parsing controls, not live Azure connectivity tests.
- `invalid endpoint returns precise provider error before fetch` exercises the provider fetch plan and verifies that the configured provider remains available while reporting the endpoint-policy error.
- `configured invalid endpoint remains visible for actionable error` checks the corresponding UI availability behavior.

The PR records a Docker run using `swift:6.2-noble` with this focused command followed by the Linux suite:

```sh
swift test --filter AzureEndpointOverrideSecurityTests
swift test
```

It reports **2 focused tests passed** and **37 tests passed in the full Linux run**. It also records a successful `swift build --target CodexBarCore` and a canary-only production CLI check that returned the invalid-override error.

These are historical results reported by the PR, not new application test executions for this article. The PR body and changed assertions were inspected for publication. The Linux totals do not establish execution of the separate macOS UI tests, and the added regressions do not prove redirect-hop enforcement or destination ownership.

## What was learned

The settings parser and the request builder answer different questions. One produces configuration; the other releases a credential. A shared policy must reach the second boundary even when the first is bypassed by a legitimate direct caller.

The compatibility trade-off is equally concrete: preserve supported HTTPS proxies and existing normalization, reject plaintext credential transport, and leave invalid settings visible enough to repair. A secure default is easier to retain when its failure is understandable.

## Takeaways

- Validate at the credential-release boundary, not only when settings are parsed.
- Prove denial before transport invocation; an error after sending the request is too late.
- Keep the claim narrow: requiring HTTPS does not prove endpoint ownership or lower-trust control of configuration.

## Repeat next time

- Trace endpoint configuration through normalization, request construction, credential attachment, and transport.
- Reuse the canonical validator at the credentialed request boundary; do not rely only on settings validation.
- Test direct callers with a transport that fails if a denied request reaches it.
- Pair denial with supported normalization and configuration-visibility controls.
- Separate HTTPS policy from destination ownership, redirect behavior, and the actor's ability to change configuration.

## Vault redirect

The private research system already records the credential-destination rule and its direct-caller regression requirement. This case applies those existing lessons alongside the trust-model rule: prove configuration influence before making a stronger attacker claim. No duplicate checklist entry is needed.

The public PR remains the evidence anchor. Private candidate details and unrelated findings are not reproduced here.
