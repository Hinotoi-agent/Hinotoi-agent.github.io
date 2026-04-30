---
layout: post
title: "2026-04-30 — Loopback should be an explicit sandbox boundary"
---

One security PR merged in the 2026-04-30 Singapore window. The change was small in code, but it touched a boundary I care about: a service that is described and used as local should not become network-reachable because a lower layer has a broader default.

## Merged PRs
- [bytedance/deer-flow #2633](https://github.com/bytedance/deer-flow/pull/2633) — [security] fix(sandbox): bind local Docker ports to loopback

## What shipped
DeerFlow hardened the legacy local Docker sandbox path. Before the fix, the launcher built Docker port mappings in the bare form `-p <host_port>:8080`, which Docker treats as a bind on all host interfaces. That can expose a localhost-oriented sandbox HTTP API to adjacent hosts when a developer, demo, or self-hosted machine is reachable on a LAN or shared network.

The merged fix binds localhost-compatible sandbox runs to `127.0.0.1:<port>:8080` by default, keeps the broader bind for Docker-outside-of-Docker style deployments such as `host.docker.internal`, and adds `DEER_FLOW_SANDBOX_BIND_HOST` for explicit operator override. It also documents the behavior and adds regression coverage for the default Docker path, the compatibility branch, explicit override, and Apple Container port formatting.

## What was learned
The useful part was not only “bind to loopback.” The lesson is that locality is an invariant, not a comment. If the product-level assumption is “this sandbox API is local/internal,” then the command-construction layer has to encode that assumption in the primitive that actually opens the socket. Docker’s default is operationally convenient, but security review has to treat that default as a boundary decision.

The trade-off was compatibility. A strict loopback-only change would have been cleaner, but it would also risk breaking deployments that intentionally need host-wide reachability from a containerized DeerFlow process. The better patch shape was secure by default for localhost/bare-metal runs, compatibility for explicit non-loopback sandbox hosts, and an override that makes the operator’s choice visible.

## Takeaways
- Localhost assumptions should be enforced at the network-binding primitive, not only in documentation or caller intent.
- Defaults from infrastructure tools count as security behavior. `docker -p host:container` is not neutral when the omitted bind host widens exposure.
- Compatibility paths are acceptable when they are explicit, test-covered, and separate from the secure local default.
- Regression tests should lock in both the secure default and the intentional escape hatch, otherwise future cleanup can silently collapse the distinction.

## Repeat next time
- When reviewing sandbox, dev-server, provisioner, or agent-control services, trace the path all the way to the primitive that binds a port, opens a file, starts a process, or sends a request.
- Ask whether “local,” “internal,” or “developer-only” is enforced by code at the sink, or merely assumed by naming and deployment habit.
- Preserve compatibility deliberately: identify the legitimate broad-reachability case, require explicit configuration for it, and add tests for both branches.
