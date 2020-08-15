---
title: Connecting
type: docs
weight: 4
---

## Why do I need a dedicated subsystem for connecting?

WebRTC will go to great lengths to achieve direct bi-directional communication between two WebRTC Agents. These agents may even be in different networks with no direct communication between agents, by using NAT Traversal WebRTC can make communication happen. NAT Traversal is a networking technique that enables communication between two peers that can't directly connect.

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

## NAT Mapping
NAT(Network Address Translation) Mapping is the magic that makes the connectivity of WebRTC possible, even when the peers can't access each other on their own. With this you can have two peers in completely different networks communicating directly.

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

The document that describes these behaviors is [RFC 4787](https://tools.ietf.org/html/rfc4787)

### Creating a Mapping
Creating a mapping is the easiest part. When you send a packet to an address outside your network, a mapping is created! If the server then responds to your request the response will be delivered back to the host that sent it.
The server can respond with multiple packets back to your single message.

The details around mappings is where it gets complicated.

### Mapping Creation Behaviors
These are the rules for when a new mapping is created. They fall into three different categories.

#### Endpoint Independent Mapping
One mapping is created for each sender inside the NAT. If you send two packets to different remote addresses the NAT Mapping will be re-used. Both remote hosts could then respond and it would be sent back to the same local listener.

This is the best case scenario. For a call to work at least one side MUST be of this type.

#### Address Dependent Mapping
A new mapping is created every time you send to a new address. If you send two packets to different hosts two mappings will be created. If you send two packets to the same remote host, but different destination ports a new mapping will NOT be created.

#### Address and Port Dependent Mapping
A new mapping is created if the remote IP or Port is different. If you send two packets to the same remote host, but different destination ports a new mapping will be created.

### Mapping Filtering Behaviors
Mapping filtering are the rules around who is allowed to use the mapping. They fall into three similar classifications.

#### Endpoint Independent Filtering
Anyone can use the mapping. After you create the mapping by sending a packet that mapping can be used by anyone on the internet.

#### Address Dependent Filtering
Only the host the mapping was created for can use the mapping. If you send a packet to host `A` it can respond back with as many packets as it wants. If host `B` attempts to send a packet to that mapping it will be ignored.

#### Address and Port Dependent Filtering
Only the host and port the mapping was created for can use the mapping. If you send a packet to host `A:5000` it can respond back with as many packets as it wants. If host `A:5001` attempts to send a packet to that mapping it will be ignored.

### Mapping Refresh
It is recommended that if a mapping is unused for 5 minutes it should be destroyed. This is entirely up to the ISP or hardware manufacturer.

## STUN
STUN(Session Traversal Utilities for NAT) is a protocol that was created just for working with NATs. This is another technology pre-dates WebRTC (and ICE!). It is defined by [RFC 5389](https://tools.ietf.org/html/rfc5389) STUN defines the structure of packets we send over UDP. The STUN protocol is also used by ICE/TURN.

STUN is useful because it gives us all the details about our NAT Mappings. We are able to create them, but we have no idea what the address is! STUN not only gives you the ability to create a mapping, but then you get the details so you can share it with others so they can send traffic to you via the mapping you created.

Lets start with a basic description of STUN. Later it will be extended later for TURN and ICE usage. For now we are just going to describe the Request/Response flow to create a mapping and then how we get the details of it to share with others. This is what actually happens when you have a `stun:` server in your ICE urls.

### Protocol Structure
Every STUN packets begins with a STUN header, with the following structure

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
Each STUN packet has a type. For now we only care about the following. We make a request to a STUN server, and it responds with a different type.

* Binding Request - `0x0001`
* Binding Response - `0x0101`

#### Message Length
This is how long the `Data` section is. This section contains arbitrary data that is defined by the `Message Type`

#### Magic Cookie
The fixed value `0x2112A442`, it helps distinguish STUN traffic from other protocols.

#### Transaction ID
96-bit identifier that uniquely identifies a request/response. This helps you pair up your requests and responses.

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

The `STUN Binding Request` uses no attributes.

The `STUN Binding Response` uses a `XOR-MAPPED-ADDRESS (0x0020)`. This attribute contains an IP/Port. This is the IP/Port of the NAT Mapping that is created!

### Create a NAT Mapping
Creating a NAT Mapping using STUN just takes sending one request! You send a `STUN Binding Request` to the STUN Server. The STUN Server then responds with a `STUN Binding Response`.
This `STUN Binding Response` will contain the `Mapped Address`. This `Mapped Address` is what you would share if someone wanted to send packets to you.

This how a `Server Reflexive Candidate` is generated also known as your `Public IP`.

### Determining NAT Type
Unfortunately the `Mapped Address` might not be useful in all cases. If it is `Address Dependent` only the STUN server can send traffic back to you, making it useless for communicating with others.

[RFC5780](https://tools.ietf.org/html/rfc5780) defines a method for running a test to determine your NAT Type. This would be useful because you would know ahead of time if direct connectivity was possible, or if you need to use a TURN Server.

## TURN
TURN (Traversal Using Relays around NAT) is defined in [RFC5766](https://tools.ietf.org/html/rfc5766) is the solution when direct connectivity isn't possible. It could be because you have two NAT Types that are incompatible, or maybe can't speak the same protocol! TURN is also important for privacy purposes. By running all your communication through TURN you obscure the clients actual address.

TURN uses a dedicated server. This server acts as a proxy for a client. The client connects to a TURN Server and creates an `Allocation`. By creating a `Allocation` a client gets a temporary IP/Port/Protocol that can send into to get traffic back to the client. This new listener is known as the `Relayed Transport Address`.
Think of it like a forwarding address! Anything you send into this is forwarded to the client. Also the client then sends packets via the `Relayed Transport Address`.

### TURN Lifecycle
The following is everything that a client who wishes to create a TURN allocation has to do. Communicating with someone who is using TURN requires no changes though, you get a IP/Port and communicate with it like any other host.

#### Allocations
Allocations are at the core of TURN. A Allocation is basically a 'TURN Session'. To create a TURN allocation you communicate with the TURN control port (usually 3478)

When creating an allocation you need to provide/decide a few things
* Username/Password - Creating TURN allocations require authentication
* Allocation Transport - The `Relayed Transport Address` can be UDP or TCP

#### Permissions

#### Send Indication/ChannelData

### TURN Usage
#### One TURN Allocations for Communication
#### Two TURN Allocations for Communication

## ICE
ICE (Interactive Connectivity Establishment)

### Candidate Gathering
#### Host
#### Host (mDNS)
#### Server Reflexive
#### Relay

### Connectivity Checks
#### Peer Reflexive Candidates
### Candidate Selection
