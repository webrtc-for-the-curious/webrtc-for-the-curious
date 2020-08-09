---
title: Connecting
type: docs
weight: 4
---

## Why do I need a dedicated subsystem for connecting?

WwbRTC will go to great lengths to acheive bi-directional communication between two agents. These agents can be in different networks with no direct communication. But by using NAT traversal WebRTC makes it happen. The packets aren't even routed through a relay, it is a direct connection.

In situations where direct connectivity isn't possible WebRTC has other techniques all well. You can use a TURN server to communicate across protocols (UDP <-> TCP) and versions (IPv4 <-> IPv6) and in places where NAT Traversal can't do the job.

Because WebRTC does this you get

* No Bandwidth Costs from running servers

Since all the communication happens directly during peers you don't have to pay for transporting that data!

* Lower Latency

Communication is much faster when it is direct! If a user has to run everything through you server it makes things a lot slower.

* Secure E2E Communication

Direct Communication is also more secure. Since users aren't routing your data through your server they don't even need to trust you won't decrypt it.


## How does it work?

Everything described above is done by [ICE](https://tools.ietf.org/html/rfc8445). Another protocol that pre-dates WebRTC.


## Networking real world constraints
### Not in the same network
### Protocol Restrictions
### Firewall Rules

## Network Address Translation

### Port Mapping
### Filtering

## STUN ()
## TURN ()

## ICE ()
### Candidate Gathering
### Connectivity Checks
### Candidate Selection


