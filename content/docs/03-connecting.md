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

The process described above is [ICE](https://tools.ietf.org/html/rfc8445). Another protocol that pre-dates WebRTC.

ICE is a protocol that tries to find the best way to communicate between two ICE Agents. Each ICE Agenta publishes the ways it is reachable, these are known as candidatea. ICE then determines the best candidate pair.

The actual ICE Process is described in greater detail later in this chapter. To understand why ICE exists it is useful to understand what network behaviors it is taking advantage of.

## Networking real world constraints
ICE is all about overcoming the constraints of real world networks. Before we even explore the solution lets talk about the actual problems.


### Not in the same network
Most of the time the other WebRTC Agent will not even be in the same network! A typical call will usually have two WebRTC Agents in different networks with no direct connectivity.

Visually it looks something like.

*TODO Two peers inside different NATs*


### Protocol Restrictions

### Firewall/IDS Rules


## Network Address Translation Address and Port Mapping
NAT Mapping is the magic that makes the direct connectivity of WebRTC possible. With this you can have two peers in completely different networks communicating directly. This behavior allows traffic to an external address be forwarded to an internal host.

*TODO port forwarding diagram*

NAR mapping essentially is a automated/config-less version of doing port forwarding in your router.

The downside to NAT Mapping is that it has been implemented in many different ways. In some cases network administrators may even disable it entirely.

### Creating a Mapping
### Mapping Creation Behaviors
### Mapping Filtering Behaviors
### Mapping Lifetimes

## STUN ()
## TURN ()

## ICE ()

### Candidate Gathering
#### Host
#### Host (mDNS)
#### Server Reflexive
#### Relay

### Connectivity Checks
#### Peer Reflexive Candidates
### Candidate Selection
