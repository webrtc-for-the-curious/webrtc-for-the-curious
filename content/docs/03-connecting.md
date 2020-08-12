---
title: Connecting
type: docs
weight: 4
---

## Why do I need a dedicated subsystem for connecting?

WwbRTC will go to great lengths to achieve direct bi-directional communication between two WebRTC Agents. These agents may even be in different networks with no direct communication between agents, by using NAT Traversal WebRTC can make communication happen. NAT Traversal is a networking technique that enables communication between two peers that can't directly connect.

In situations where direct connectivity doesn't exist and NAT Traversal fails WebRTC has other techniques. You can then use a TURN server to communicate across protocols (UDP <-> TCP) and versions (IPv4 <-> IPv6).

Because WebRTC has these attributes you get these advantages over traditional Client/Server technology.

### Reduced Bandwidth Costs

Since media communication happens directly during peers you don't have to pay for transporting it.

###  Lower Latency

Communication is faster when it is direct! When a user had to run everything through you server it makes things slower.

###  Secure E2E Communication

Direct Communication is more secure. Since users aren't routing your data through your server they don't even need to trust you won't decrypt it.

## How does it work?

The process described above is [ICE](https://tools.ietf.org/html/rfc8445). Another protocol that pre-dates WebRTC.

ICE is a protocol that tries to find the best way to communicate between two ICE Agents. Each ICE Agents publishes the ways it is reachable, these are known as candidates. ICE then determines the best candidate pairing of candidates.

The actual ICE Process is described in greater detail later in this chapter. To understand why ICE exists it is useful to understand what network behaviors were are overcoming.

## Networking real world constraints
ICE is all about overcoming the constraints of real world networks. Before we even explore the solution lets talk about the actual problems.

### Not in the same network
Most of the time the other WebRTC Agent will not even be in the same network. A typical call is usually between two WebRTC Agents in different networks with no direct connectivity.

Below is a graph of two distinct networks, connected by the public internet. Then in each network you have two hosts.

{{<mermaid>}}
graph TB
subgraph netb ["Network B (IP Address 5.0.0.2)"]
  b3["Agent 3 (IP 192.168.0.1)"]
  b4["Agent 4 (IP 192.168.0.1)"]
  routerb["Router B"]
  end

subgraph neta ["Network A (IP Address 5.0.0.1)"]
  routera["Router A"]
  a1["Agent 1 (IP 192.168.0.1)"]
  a2["Agent 2 (IP 192.168.0.1)"]
  end

pub{Public Internet}
routera-->pub
routerb-->pub

{{< /mermaid >}}

For the hosts in the same network it is very easy to connect. `192.168.0.1 -> 192.168.0.2` is easy to do! However a host using `Router B` has no way to directly access anything using `Router A`. A host using `Router B` could send traffic directly to `Router A`, but the request would end there.

### Protocol Restrictions

Some networks don't allow UDP traffic at all, or maybe they don't allow TCP. Some networks have a very low MTU. There are lots of variables that network administrators can change that can make communication difficult.

### Firewall/IDS Rules

Another is 'Deep Packet Inspection' and other intelligent filtering. Some network administrators will run software that tries to process every packet. Many times this software doesn't understand WebRTC, so blocks because it doesn't know what to do

## Network Address Translation and Address/Port Mapping
NAT Mapping is the magic that makes the connectivity of WebRTC possible, even when the peers can't access each other on their own. With this you can have two peers in completely different networks communicating directly.

Again we have a `Agent 1` and `Agent 2` and they are in different networks. However traffic is flowing completely through. Visualized that looks like.

{{<mermaid>}}
graph TB
subgraph netb ["Network B (IP Address 5.0.0.2)"]
  b2["Agent 2 (IP 192.168.0.1)"]
  routerb["Router B"]
  end

subgraph neta ["Network A (IP Address 5.0.0.1)"]
  routera["Router A"]
  a1["Agent 1 (IP 192.168.0.1)"]
  end

pub{Public Internet}

a1-.->routera;
routera-.->pub;
pub-.->routerb;
routerb-.->b2;
{{< /mermaid >}}

To makes this possible you need to establish a NAT Mapping first. NAT mapping will feel like an automated/config-less version of doing port forwarding in your router.

The downside to NAT Mapping is that that network behavior is inconsistent between networks. ISPs and hardware manufacturers do it in different ways for their own reasons. In some cases network administrators may even disable it.
The full range of behaviors is understood and observable, so a ICE Agent is able to confirm it created a NAT Mapping, and the attributes of the mapping.

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
