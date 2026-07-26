---
layout: post
title: "2026-07-27 — Prove the owner before resuming agent work"
date: 2026-07-27 05:00:13 +0800
permalink: /2026/07/27/ai-security-case-study-owner-proof-before-session-resume/
takeaway: "A resume key identifies work; it does not prove who may inherit that work's agent authority."
categories: [case-study, ai-security]
tags: [case-study, authorization, identity-binding, agent-session, token-rotation, control-plane, github-actions]
---

Resuming agent work is an authorization event, not only a lifecycle operation. A durable work identifier can locate a session, but it must not replace proof of the actor allowed to rotate that session's credentials.

## Signal

[`openclaw/crabfleet #68`](https://github.com/openclaw/crabfleet/pull/68) fixed a GitHub Actions session-resume path where an existing `workKey` allowed registration to continue without the stable owner proof required for new work.

The high-signal chain was:

```text
service-authenticated registration
  -> existing workKey lookup
  -> omitted owner skips mismatch check
  -> session reset and agent-token rotation
  -> fresh session-agent credential returned
```

The service token admitted the caller to the registration API. It did not prove that the caller owned the existing action session selected by `workKey`.

## Threat model

`POST /api/openclaw/action-sessions` accepts registrations from GitHub Actions automation. Deployments may share the OpenClaw automation token across rooms, tenants, automation contexts, or less-trusted service components.

Within that deployment model, a caller possessing the service token and a known or guessed existing `workKey` could attempt to resume work belonging to another stable owner. The issue did not require bypassing service authentication. It crossed the narrower owner boundary inside an already authenticated control plane.

The security claim is correspondingly bounded: this was a session-owner binding failure in configurations where multiple trust contexts share registration authority, not an unauthenticated Internet-wide takeover.

## Finding and PR

Public PR: [`openclaw/crabfleet #68 — [security] fix(openclaw): require owner proof to resume action work`](https://github.com/openclaw/crabfleet/pull/68).

Merge commit: `06de74cc6a9f022bb5ed62912d6b3f3b8d4d173b`.

Security-relevant files:

- `src/worker/github-actions-session-registration.ts` — requires a resolved owner for every registration and preserves the stable-owner comparison on resume.
- `tests/github-actions-session-registration.test.ts` — covers missing, matching, and mismatched owner cases plus token-rotation side effects.
- `README.md`, `docs/api.md`, and `docs/github-actions-sessions.md` — make owner proof part of the public registration and resume contract.

Before the fix, missing owner proof was rejected only when no existing row was found. The later mismatch guard also ran only when an owner had been supplied. An ownerless request for existing work therefore skipped both checks and reached the update path.

## Exploit path

The source-to-sink chain was:

```text
shared automation context or service component
  -> service-authenticated POST /api/openclaw/action-sessions
  -> caller-supplied existing workKey
  -> database session lookup
  -> missing owner accepted on resume
  -> session update and agent_token_hash rotation
  -> fresh plaintext agentToken returned
  -> authority as the existing session agent
```

`workKey` was a carrier and lookup handle. Treating possession of that handle as enough to resume work detached session authority from the stable owner subject established at registration.

The sensitive sink was token rotation. Once the request reached that mutation, the caller received a new credential for the selected session. The relevant invariant therefore had to be enforced before changing `agent_token_hash`, not inferred from the fact that the caller knew the work identifier.

## Mitigation

The patch requires `owner` to resolve successfully for both new registrations and resumes. For existing work, the resolved stable owner subject must match the session's stored `owner_subject` before any reset or token rotation occurs.

This creates two explicit paths:

- **deny:** missing or mismatched owner proof fails before session mutation;
- **compatibility:** a matching owner can resume the same session and rotate its session-scoped token.

The fix also aligned the documentation with the implementation. That matters for authorization boundaries: an optional field in API prose tends to become an optional security assumption in clients and future refactors.

## Verification

The focused regression named in the PR was:

```sh
pnpm exec node --test --experimental-strip-types tests/github-actions-session-registration.test.ts
```

It reported 12 passing tests. The same file passed in a read-only Node 22 Docker run. Full validation reported 731 passing tests with no failures, plus clean checks and formatting.

The PR also recorded a sanitized runtime proof against a local Wrangler Worker with local D1 state:

```text
new registration with owner: 201
ownerless resume: 400, token_rotated=False
matching-owner resume: 201, token_rotated=True
DB proof: ownerless_reject_preserved_hash=True
```

This is sink-shaped verification. The negative case proves both visible denial and absence of the sensitive side effect: the stored token hash does not change. The positive control proves that intended matching-owner resume behavior remains available.

## What was learned

Authenticated does not mean authorized for every object selected inside the request. In agent and workflow control planes, a service token may establish the calling service while a separate durable owner, tenant, room, session, or workspace fact governs the object-level action.

Resume paths deserve the same scrutiny as create paths. They often inherit identifiers, cached state, approvals, or tokens and then perform a privileged mutation under the assumption that earlier checks still bind the current actor.

The reusable review chain is:

```text
request credential -> object handle -> server-derived owner -> policy decision -> token or action sink
```

A carrier such as `workKey`, resume token, approval payload, idempotency key, local address, or request header can locate or constrain work. It is not actor proof by itself. The proof must bind the current request to the principal whose authority is used at the sink.

## Repeat next time

- Review create, retry, resume, reconnect, replay, and restore paths as separate authorization entry points.
- Map every caller-supplied object handle to a server-derived owner, tenant, session, workspace, or capability before mutation.
- Treat shared service authentication as admission to the control plane, not automatic ownership of every object behind it.
- Put the owner/scope check immediately before token rotation, dispatch, file mutation, network action, or other sensitive sink.
- Test missing proof, wrong proof, and matching proof.
- For denials, assert absence of side effects: no token rotation, session reset, dispatch, file write, network call, or stored mutation.

## Vault redirect

The durable private owner is the OSS Vulnerability Research Vault's authorization and action-sink review workflow. The public lesson is intentionally narrow: an existing work handle did not prove ownership, the fix restored stable owner binding before credential rotation, and verification proved denial without mutation plus a working matching-owner control.

Future reviews should preserve the complete boundary map—request credential, object handle, server-derived principal, policy decision, and action sink—without publishing private target notes or uncoordinated research artifacts.
