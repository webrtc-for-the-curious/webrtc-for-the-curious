---
title: What, Why and How
type: docs
weight: 2
---

# What, Why and How

## What is WebRTC?

WebRTC, short for Web Real-Time Communication, is both an API and a Protocol. The WebRTC protocol is a set of rules for two WebRTC agents to negotiate bi-directional secure real-time communication. The WebRTC API then allows developers to use the WebRTC protocol. The WebRTC API is specified only for JavaScript.

A similar relationship would be the one between HTTP and the Fetch API. WebRTC the protocol would be HTTP, and WebRTC the API would be the Fetch API.

The WebRTC protocol is available in other APIs and languages besides JavaScript. You can find servers and domain-specific tools as well for WebRTC. All of these implementations use the WebRTC protocol so that they can interact with each other.

The WebRTC protocol is maintained in the IETF in the [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/) working group. The WebRTC API is documented in the W3C as [webrtc](https://www.w3.org/TR/webrtc/).

## Why should I learn WebRTC?

These are some of the things that WebRTC will give you:

* Open standard
* Multiple implementations
* Available in browsers
* Mandatory encryption
* NAT Traversal
* Repurposed existing technology
* Congestion control
* Sub-second latency

This list is not meant to be exhaustive, but rather a range of things you may appreciate during your journey. If you don't know all these terms yet, don't worry: this book will teach them to you along the way.

## The WebRTC Protocol is a collection of other technologies

The WebRTC Protocol is an immense topic that would take an entire book of its own to explain in full. We can, however, begin an explanation by breaking it into four steps:

1. Signaling
2. Connecting
3. Securing
4. Communicating

These steps are sequential, which means the prior step must be 100% successful for the subsequent step to begin.

One peculiar fact about WebRTC is that each step is actually made up of many other protocols; to make WebRTC, we stitch together many existing technologies. In that sense, you can think of WebRTC as being more a combination and configuration of well-understood tech dating back to the early 2000s than as a brand-new process in its own right.

Each of these steps has its own dedicated chapter but, since each step depends on the one before it, it is helpful to understand them at a high level first. A basic understand of all the steps will help when explaining further the purpose of each individually.

### Signaling: How peers find each other in WebRTC

When a WebRTC Agent starts, it has no idea who it is going to communicate with or what they are going to communicate about. The *Signaling* step solves this issue! Signaling is used to bootstrap the call, allowing two independant WebRTC agents to start communicating.

Signaling uses an existing, plain-text protocol called SDP (Session Description Protocol). Each SDP message is made up of key/value pairs and contains a list of "media sections". The SDP that the two signaling WebRTC Agents exchange contains details like:

* The IPs and Ports that the agent is reachable on (candidates)
* The number of audio and video tracks the agent wishes to send
* The audio and video codecs each agent supports
* The values used while connecting (`uFrag`/`uPwd`)
* The values used while securing (certificate fingerprint)

It is important to note that signaling typically happens "out-of-band," which means applications generally don't use WebRTC itself to trade signaling messages. Any architecture suitable for sending messages can relay the SDPs between the connecting peers, and many applications will simply use their existing infrastructure (e.g. REST endpoints, WebSocket connections, or authentication proxies) to facilitate trading of SDPs between the proper clients.

### Connecting:  Using STUN/TURN to Navigate Connaction and NAT Traversal

After trading SDPs, the two WebRTC Agents now have enough information to attempt to connect to each other. To make this happen, WebRTC uses another established technology called ICE (Interactive Connectivity Establishment).

ICE is a protocol that pre-dates WebRTC which allows the establishment of a connection between two Agents. These Agents could be on the same network or on the other side of the world. ICE is the solution to establishing a direct connection without a central server.

The real magic here is 'NAT Traversal' and STUN/TURN Servers. These two concepts are all you need to communicate with an ICE Agent in another subnet. We will explore these topics in depth later.

Once ICE successfully connects, WebRTC then moves on to establishing an encrypted transport. This transport is used for audio, video, and data.

### Securing the transport layer with DTLS and SRTP

Now that we have bi-directional communication (via ICE) we need to establish secure communication. This is done through two protocols that pre-date WebRTC. The first protocol is DTLS (Datagram Transport Layer Security) which is just TLS over UDP. TLS is the cryptographic protocol used to secure communication over HTTPS. The second protocol is SRTP (Secure Real-time Transport Protocol).

First, WebRTC connects by doing a DTLS handshake over the connection established by ICE. Unlike HTTPS, WebRTC doesn't use a central authority for certificates. Instead, WebRTC just asserts that the certificate exchanged via DTLS matches the fingerprint shared via signaling. This DTLS connection is then used for DataChannel messages.

WebRTC then uses a different protocol for audio/video transmission called RTP. We secure our RTP packets using SRTP. We initialize our SRTP session by extracting the keys from the negotiated DTLS session. In a later chapter, we discuss why media transmission has its own protocol.

Now we are done! You now have bi-directional and secure communication. If you have a stable connection between your WebRTC Agents, this is all the complexity you may need. Unfortunately, the real world has packet loss and bandwidth limits, and the next section is about how we deal with them.

### Communicating with peers via RTP and SCTP

We now have two WebRTC Agents with secure bi-directional communication. Let's start communicating! Again, we use two pre-existing protocols: RTP (Real-time Transport Protocol), and SCTP (Stream Control Transmission Protocol). Use RTP to exchange media encrypted with SRTP, and use SCTP to send and receive DataChannel messages encrypted with DTLS.

RTP is quite minimal but provides what is needed to implement real-time streaming. The important thing is that RTP gives flexibility to the developer, so they can handle latency, loss, and congestion as they please. We will discuss this further in the media chapter.

The final protocol in the stack is SCTP. SCTP allows many delivery options for messages. You can optionally choose to have unreliable, out of order delivery, so you can get the latency needed for real-time systems.

## WebRTC, a collection of protocols
WebRTC solves a lot of problems. At first, this may even seem over-engineered. The genius of WebRTC is really the humility. It didn't assume it could solve everything better. Instead, it embraced many existing single purpose technologies and bundled them together.

This allows us to examine and learn each part individually without being overwhelmed. A good way to visualize it is a 'WebRTC Agent' is really just an orchestrator of many different protocols.

![WebRTC Agent](../images/01-webrtc-agent.png "WebRTC Agent Diagram")

## How does WebRTC (the API) work

This section shows how the JavaScript API maps to the protocol. This isn't meant as an extensive demo of the WebRTC API, but more to create a mental model of how it all ties together.
If you aren't familiar with either, it is ok. This could be a fun section to return to as you learn more!

### `new RTCPeerConnection`

The `RTCPeerConnection` is the top-level "WebRTC Session". It contains all the protocols mentioned above. The subsystems are all allocated but nothing happens yet.

### `addTrack`

`addTrack` creates a new RTP stream. A random Synchronization Source (SSRC) will be generated for this stream. This stream will then be inside the Session Description generated by `createOffer` inside a media section. Each call to `addTrack` will create a new SSRC and media section.

Immediately after a SRTP Session is established these media packets will start being sent via ICE after being encrypted using SRTP.

### `createDataChannel`

`createDataChannel` creates a new SCTP stream if no SCTP association exists. By default, SCTP is not enabled but is only started when one side requests a data channel.

Immediately after a DTLS Session is established, the SCTP association will start sending packets via ICE and encrypted with DTLS.

### `createOffer`

`createOffer` generates a Session Description of the local state to be shared with the remote peer.

The act of calling `createOffer` doesn't change anything for the local peer.

### `setLocalDescription`

`setLocalDescription` commits any requested changes. `addTrack`, `createDataChannel` and similar calls are all temporary until this call. `setLocalDescription` is called with the value generated by `createOffer`.

Usually, after this call, you will send the offer to the remote peer, and they will call `setRemoteDescription` with it.

### `setRemoteDescription`

`setRemoteDescription` is how we inform the local agent about the remote candidates' state. This is how the act of 'Signaling' is done with the JavaScript API.

When `setRemoteDescription` has been called on both sides, the WebRTC Agents now have enough info to start communicating Peer-To-Peer (P2P)!

### `addIceCandidate`

`addIceCandidate` allows a WebRTC agent to add more remote ICE Candidates whenever they want. This API sends the ICE Candidate right into the ICE subsystem and has no other effect on the greater WebRTC connection.

### `ontrack`

`ontrack` is a callback that is fired when an RTP packet is received from the remote peer. The incoming packets would have been declared in the Session Description that was passed to `setRemoteDescription`.

WebRTC uses the SSRC and looks up the associated `MediaStream` and `MediaStreamTrack`, and fires this callback with these details populated.

### `oniceconnectionstatechange`

`oniceconnectionstatechange` is a callback that is fired that reflects the state of the ICE Agent. When you have network connectivity or when you become disconnected this is how you are notified.

### `onconnectionstatechange`

`onconnectionstatechange` is a combination of ICE Agent and DTLS Agent state. You can watch this to be notified when ICE and DTLS have both completed successfully.
