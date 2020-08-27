---
title: Connecting
type: docs
weight: 4
---

## Why do I need a dedicated subsystem for connecting?

WebRTC will go to great lengths to achieve direct bi-directional communication between two WebRTC Agents. This connection style is also known as peer-to-peer. Establishing peer-to-peer connectivity can be difficult though. These agents could be in different networks with no direct connectivity!

In situations where direct connectivity does exist you can have other issues.  In some cases, your clients don't speak the same network protocols (UDP <-> TCP) or maybe IP Versions (IPv4 <-> IPv6).

Because WebRTC has these attributes you get these advantages over traditional Client/Server technology.

### Reduced Bandwidth Costs

Since media communication happens directly between peers you don't have to pay for transporting it.

###  Lower Latency

Communication is faster when it is direct! When a user has to run everything through your server it makes things slower.

###  Secure E2E Communication

Direct Communication is more secure. Since users aren't routing your data through your server they don't even need to trust you won't decrypt it.

## How does it work?

The process described above is [ICE](https://tools.ietf.org/html/rfc8445). Another protocol that pre-dates WebRTC.

ICE is a protocol that tries to find the best way to communicate between two ICE Agents. Each ICE Agent publishes the ways it is reachable, these are known as candidates. ICE then determines the best pairing of candidates.

The actual ICE process is described in greater detail later in this chapter. To understand why ICE exists, it is useful to understand what network behaviors we are overcoming.

## Networking real-world constraints
ICE is all about overcoming the constraints of real-world networks. Before we even explore the solution lets talk about the actual problems.

### Not in the same network
Most of the time the other WebRTC Agent will not even be in the same network. A typical call is usually between two WebRTC Agents in different networks with no direct connectivity.

Below is a graph of two distinct networks, connected by the public internet. Then in each network, you have two hosts.

{{<mermaid>}}
graph TB
subgraph netb ["Network B (IP Address 5.0.0.2)"]
  b3["Agent 3 (IP 192.168.0.1)"]
  b4["Agent 4 (IP 192.168.0.2)"]
  routerb["Router B"]
  end

subgraph neta ["Network A (IP Address 5.0.0.1)"]
  routera["Router A"]
  a1["Agent 1 (IP 192.168.0.1)"]
  a2["Agent 2 (IP 192.168.0.2)"]
  end

pub{Public Internet}
routera-->pub
routerb-->pub

{{< /mermaid >}}

For the hosts in the same network, it is very easy to connect. Communication between `192.168.0.1 -> 192.168.0.2` is easy to do! These two hosts can connect to each other without any outside help.

However, a host using `Router B` has no way to directly access anything behind `Router A`. A host using `Router B` could send traffic directly to `Router A`, but the request would end there. How does `Router A` know which host it should deliver the message too?

### Protocol Restrictions

Some networks don't allow UDP traffic at all, or maybe they don't allow TCP. Some networks have very low MTU. There are lots of variables that network administrators can change that can make communication difficult.

### Firewall/IDS Rules

Another is 'Deep Packet Inspection' and other intelligent filterings. Some network administrators will run software that tries to process every packet. Many times this software doesn't understand WebRTC, so it blocks because it doesn't know what to do

## NAT Mapping
NAT(Network Address Translation) Mapping is the magic that makes the connectivity of WebRTC possible. This is how WebRTC allows two peers in completely different subnets to communicate. It doesn't use a relay, proxy, or server.

Again we have  `Agent 1` and `Agent 2` and they are in different networks. However, traffic is flowing completely through. Visualized that looks like.

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

To make this communication happen you establish a NAT Mapping. Creating a NAT mapping will feel like an automated/config-less version of doing port forwarding in your router.

The downside to NAT Mapping is that that network behavior is inconsistent between networks. ISPs and hardware manufacturers may do it in different ways. In some cases, network administrators may even disable it.
The full range of behaviors is understood and observable, so an ICE Agent is able to confirm it created a NAT Mapping, and the attributes of the mapping.

The document that describes these behaviors is [RFC 4787](https://tools.ietf.org/html/rfc4787)

### Creating a Mapping
Creating a mapping is the easiest part. When you send a packet to an address outside your network, a mapping is created! A NAT Mapping is just a temporary public IP/Port that is allocated by your NAT. The outbound message will be rewritten to have
its source address be the newly created mapping.  If a message isn't sent, it will be automatically routed back to the host inside the NAT.

The details around mappings are where it gets complicated.

### Mapping Creation Behaviors
Mapping creation falls into three different categories:

#### Endpoint-Independent Mapping
One mapping is created for each sender inside the NAT. If you send two packets to two different remote addresses the NAT Mapping will be re-used. Both remote hosts would see the same source IP/Port. If the remote hosts respond, it would be sent back to the same local listener.

This is the best-case scenario. For a call to work, at least one side MUST be of this type.

#### Address Dependent Mapping
A new mapping is created every time you send a packet to a new address. If you send two packets to different hosts two mappings will be created. If you send two packets to the same remote host, but different destination ports a new mapping will NOT be created.

#### Address and Port Dependent Mapping
A new mapping is created if the remote IP or port is different. If you send two packets to the same remote host, but different destination ports, a new mapping will be created.

### Mapping Filtering Behaviors
Mapping filtering is the rules around who is allowed to use the mapping. They fall into three similar classifications:

#### Endpoint-Independent Filtering
Anyone can use the mapping. You can share the mapping with multiple other peers and they could all send traffic to it.

#### Address Dependent Filtering
Only the host the mapping was created for can use the mapping. If you send a packet to host `A` it can respond back with as many packets as it wants. If host `B` attempts to send a packet to that mapping, it will be ignored.

#### Address and Port Dependent Filtering
Only the host and port for which the mapping was created for can use that mapping. If you send a packet to host `A:5000` it can respond back with as many packets as it wants. If host `A:5001` attempts to send a packet to that mapping, it will be ignored.

### Mapping Refresh
It is recommended that if a mapping is unused for 5 minutes it should be destroyed. This is entirely up to the ISP or hardware manufacturer.

## STUN
STUN(Session Traversal Utilities for NAT) is a protocol that was created just for working with NATs. This is another technology that pre-dates WebRTC (and ICE!). It is defined by [RFC 5389](https://tools.ietf.org/html/rfc5389) which also defines the STUN packet structure. The STUN protocol is also used by ICE/TURN.

STUN is useful because it allows the programmatic creation of NAT Mappings. Before STUN, we were able to create NAT Mappings, but we had no idea what the IP/Port of it was! STUN not only gives you the ability to create a mapping, but you also get the details so you can share it with others so they can send traffic to you via the mapping you created.

Let's start with a basic description of STUN. Later, we will expand on TURN and ICE usage. For now, we are just going to describe the Request/Response flow to create a mapping. Then we talk about how we get the details of it to share with others. This is the process that happens when you have a `stun:` server in your ICE urls for a WebRTC PeerConnection.

### Protocol Structure
Every STUN packet begins with a STUN header with the following structure:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|0 0|     STUN Message Type     |         Message Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Magic Cookie                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     Transaction ID (96 bits)                  |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### STUN Message Type
Each STUN packet has a type. For now, we only care about the following:

* Binding Request - `0x0001`
* Binding Response - `0x0101`

To create a NAT Mapping we make a `Binding Request`. Then the server responds with a `Binding Response`.

#### Message Length
This is how long the `Data` section is. This section contains arbitrary data that is defined by the `Message Type`

#### Magic Cookie
The fixed value `0x2112A442` in network byte order, it helps distinguish STUN traffic from other protocols.

#### Transaction ID
A 96-bit identifier that uniquely identifies a request/response. This helps you pair up your requests and responses.

#### Data
Data will contain a list of STUN attributes. A STUN Attribute has the following structure.

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 ```

The `STUN Binding Request` uses no attributes. This means a `STUN Binding Request` contains only the header.

The `STUN Binding Response` uses a `XOR-MAPPED-ADDRESS (0x0020)`. This attribute contains an IP/Port. This is the IP/Port of the NAT Mapping that is created!

### Create a NAT Mapping
Creating a NAT Mapping using STUN just takes sending one request! You send a `STUN Binding Request` to the STUN Server. The STUN Server then responds with a `STUN Binding Response`.
This `STUN Binding Response` will contain the `Mapped Address`. The `Mapped Address` is how the STUN Server sees you and is your `NAT Mapping`.
The `Mapped Address` is what you would share if you wanted someone to send packets to you.

People will also call the `Mapped Address` your `Public IP` or `Server Reflexive Candidate`.

### Determining NAT Type
Unfortunately, the `Mapped Address` might not be useful in all cases. If it is `Address Dependent` only the STUN server can send traffic back to you. If you shared it and another peer tried to send messages in they will be dropped. This makes it useless for communicating with others.

[RFC5780](https://tools.ietf.org/html/rfc5780) defines a method for running a test to determine your NAT Type. This would be useful because you would know ahead of time if direct connectivity was possible.

## TURN
TURN (Traversal Using Relays around NAT) is defined in [RFC5766](https://tools.ietf.org/html/rfc5766) is the solution when direct connectivity isn't possible. It could be because you have two NAT Types that are incompatible, or maybe can't speak the same protocol! TURN is also important for privacy purposes. By running all your communication through TURN you obscure the client's actual address.

TURN uses a dedicated server. This server acts as a proxy for a client. The client connects to a TURN Server and creates an Allocation. By creating an Allocation a client gets a temporary IP/Port/Protocol that can send into to get traffic back to the client. This new listener is known as the `Relayed Transport Address`. Think of it as a forwarding address, you give this out so others can send you traffic via TURN! For each peer you give the `Relay Transport Address` to, you must create a `Permission` to allow communication with you.

When you send outbound traffic via TURN it is sent via the `Relayed Transport Address`. When a remote peer gets traffic they see it coming from the TURN Server.

### TURN Lifecycle
The following is everything that a client who wishes to create a TURN allocation has to do. Communicating with someone who is using TURN requires no changes. The other peer gets an IP/Port and they communicate with it like any other host.

#### Allocations
`Allocations` are at the core of TURN. An `allocation` is basically a 'TURN Session'. To create a TURN allocation you communicate with the TURN `Server Transport Address` (usually port 3478)

When creating an allocation, you need to provide/decide the following
* Username/Password - Creating TURN allocations require authentication
* Allocation Transport - The `Relayed Transport Address` can be UDP or TCP
* Even-Port - You can request sequential ports for multiple allocations, not relevant for WebRTC

If the request succeeded, you get a response with the TURN Server with the follow STUN Attributes in the Data section.
* `XOR-MAPPED-ADDRESS` - `Mapped Address` of the `TURN Client`. When someone sends data to the `Relayed Transport Address` this is where it is forwarded too.
* `RELAYED-ADDRESS` - This is the address that you give out to other clients. If someone sends a packet to this address it is relayed to the TURN client.
* `LIFETIME` - How long until this TURN Allocation is destroyed. You can extend the lifetime by sending a `Refresh` request.

#### Permissions
A remote host can't send into your `Relayed Transport Address` until you create a permission for them. When you create a permission you are telling the TURN server that this IP/Port is allowed to send inbound traffic.

The remote host needs to give you the IP/Port as it appears to the TURN server. This means it should send a `STUN Binding Request` to the TURN Server. A common error case is that a remote host will
send a `STUN Binding Request` to a different server. They will then ask you to create a permission for this IP.

Let's say you want to create a permission for a host behind a `Address Dependent Mapping`. If you generate the `Mapped Address` from a different TURN server all inbound traffic will be dropped. Every time they communicate with a different host it generates a new mapping.

#### SendIndication/ChannelData
These two messages are for the TURN Client to send messages to a remote peer.

SendIndication is a self-contained message. Inside it is the data you wish to send, and who you wish to send it too. This is wasteful if you are sending a lot of messages to a remote peer. If you send 1,000 messages you will repeat their IP Address 1,000 times!

ChannelData allows you to send data, but not repeat an IP Address. You create a Channel with an IP/Port. You then send with the ChannelId, and the IP/Port is populated server side. This is the better choice if you are sending lots of messages.

#### Refreshing
Allocations will destroy themselves automatically. The TURN Client must refresh them sooner than the `LIFETIME` given when creating the allocation.

### TURN Usage
TURN Usage exists in two forms. Usually, you have one peer acting as a 'TURN Client' and the other side communicating directly. In bad cases, you might have TURN Usage on both sides because of improper setup.

These diagrams help illustrate what that would look like.

#### One TURN Allocations for Communication
{{<mermaid>}}
graph TB

subgraph turn ["TURN Allocation"]
  serverport["Server Transport Address"]
  relayport["Relayed Transport Address" ]
  end

turnclient{TURN Client}
peer{UDP Client}

turnclient-->|"ChannelData (To UDP Client)"|serverport
serverport-->|"ChannelData (From UDP Client)"|turnclient

peer-->|"Raw Network Traffic (To TURN Client)"|relayport
relayport-->|"Raw Network Traffic (To UDP Client)"|peer
{{< /mermaid >}}

#### Two TURN Allocations for Communication
{{<mermaid>}}
graph TB

subgraph turna["TURN Allocation A"]
  serverportA["Server Transport Address"]
  relayportA["Relayed Transport Address" ]
  end

subgraph turnb["TURN Allocation B"]
  serverportB["Server Transport Address"]
  relayportB["Relayed Transport Address" ]
  end


turnclientA{TURN Client A}
turnclientB{TURN Client B}

turnclientA-->|"ChannelData"|serverportA
serverportA-->|"ChannelData"|turnclientA

turnclientB-->|"ChannelData"|serverportB
serverportB-->|"ChannelData"|turnclientB

relayportA-->|"Raw Network Traffic"|relayportB
relayportB-->|"Raw Network Traffic"|relayportA
{{< /mermaid >}}

## ICE
ICE (Interactive Connectivity Establishment) is how WebRTC connects two Agents. Defined in [RFC8445](https://tools.ietf.org/html/rfc8445), this is another technology that pre-dates WebRTC! ICE is a protocol for establishing connectivity. It determines all the possible routes between the two peers and then ensures you stay connected.

These routes are known as `Candidate Pairs`, which is a pairing of a local and remote address. This where STUN and TURN come into play with ICE. These addresses can be your local IP Address, `NAT Mapping`, or `Relayed Transport Address`. Each side gathers all the addresses they want to use, exchange them, and then attempt to connect!

Two ICE Agents communicate using the STUN Protocol. They send STUN packets to each other to establish connectivity. After connectivity is established they can send whatever they want. It will feel like using a normal socket.

### Creating an ICE Agent
An ICE Agent is either `Controlling` or `Controlled`. The `Controlling` Agent is the one that decides the selected `Candidate Pair`. Usually, the peer sending the offer is the controlling side.

Each side must have a `user fragment` and `password`. These two values must be exchanged before connectivity checks to even begin. The `user fragment` is sent in plain text and is useful for demuxing multiple ICE Sessions.
The `password` is used to generate a `MESSAGE-INTEGRITY` attribute. At the end of each STUN packet, there is an attribute that is a hash of the entire packet using the `password` as a key. This is used to authenticate the packet and ensure it hasn't been tampered with.

For WebRTC, all these values are distributed via the `Session Description` as described in the previous chapter.

### Candidate Gathering
We now need to gather all the possible addresses we are reachable at. These addresses are known as candidates. These candidates are also distributed via the `Session Description`.

#### Host
A Host candidate is listening directly on a local interface. This can either be UDP or TCP.

#### mDNS
A mDNS candidate is similar to a host candidate, but the IP address is obscured. Instead of informing the other side about your IP address, you give them a UUID. You then set-up a multicast listener, and respond if anyone requests the UUID you published.

If you are in the same network as the agent, you can find each other via Multicast. If you aren't in the same network you will be unable to connect.

This is useful for privacy purposes. Before, a user could find out your local IP address via WebRTC, now they only get a random UUID.

#### Server Reflexive
A Server Reflexive candidate is generated by doing a `STUN Binding Request` to a STUN Server.

When you get the `STUN Binding Response`, the `XOR-MAPPED-ADDRESS` is your Server Reflexive Candidate.

#### Peer Reflexive
A Peer Reflexive candidate is when you get an inbound request from an address that isn't known to you. Since ICE is an authenticated protocol you know the traffic is valid. This just means the remote peer is
communicating with you from an address it didn't know about.

This commonly happens when a `Host Candidate` communicates with a `Server Reflexive Candidate`. A new `NAT Mapping` was created because you are communicating outside your subnet.

#### Relay
A Relay Candidate is generated by using a TURN Server.

After the initial handshake with the TURN Server you are given a  `RELAYED-ADDRESS`, this is your Relay Candidate.

### Connectivity Checks
We now know the remote agent's `user fragment`, `password`, and candidates. We can now attempt to connect! Every candidate is paired with each other. So if you have 3 candidates on each side, you now have 9 candidate pairs.

Visually it looks like this
{{<mermaid>}}
graph LR

subgraph agentA["ICE Agent A"]
  hostA{Host Candidate}
  serverreflexiveA{Server Reflexive Candidate}
  relayA{Relay Candidate}
  end

style hostA fill:#ECECFF,stroke:red
style serverreflexiveA fill:#ECECFF,stroke:green
style relayA fill:#ECECFF,stroke:blue

subgraph agentB["ICE Agent B"]
  hostB{Host Candidate}
  serverreflexiveB{Server Reflexive Candidate}
  relayB{Relay Candidate}
  end

hostA --- hostB
hostA --- serverreflexiveB
hostA --- relayB
linkStyle 0,1,2 stroke-width:2px,fill:none,stroke:red;

serverreflexiveA --- hostB
serverreflexiveA --- serverreflexiveB
serverreflexiveA --- relayB
linkStyle 3,4,5 stroke-width:2px,fill:none,stroke:green;

relayA --- hostB
relayA --- serverreflexiveB
relayA --- relayB
linkStyle 6,7,8 stroke-width:2px,fill:none,stroke:blue;
{{< /mermaid >}}

### Candidate Selection
The Controlling and Controlled Agent both start sending traffic on each pair. This is needed if one Agent is behind a `Address Dependent Mapping`, this will cause a `Peer Reflexive Candidate` to be created.

Each `Candidate Pair` that saw network traffic is then promoted to a `Valid Candidate` pair. The Controlling Agent then takes one `Valid Candidate` pair and nominates it. This becomes the `Nominated Pair`. The Controlling
and Controlled Agent then attempt one more round of bi-directional communication. If that succeeds, the `Nominated Pair` becomes the `Selected Candidate Pair`! This is used for the rest of the session.

### Restarts
If the `Selected Candidate Pair` stops working for any reason (NAT Mapping Expires, TURN Server crashes) the ICE Agent will go to `Failed` state. Both agents can be restarted and do the whole process over again.
