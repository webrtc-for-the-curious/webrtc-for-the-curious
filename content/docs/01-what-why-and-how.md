---
title: What, Why and How
type: docs
weight: 2
---



# What is WebRTC?
WebRTC, short for Web Real-Time Communication, is both an API and a Protocol. The WebRTC protocol is a set of rules for two WebRTC agents to negotiate bi-directional secure real-time communication. The WebRTC API then allows developers to use the WebRTC protocol. The WebRTC API is specified only for JavaScript.

A similar relationship would be HTTP and the fetch API. WebRTC the protocol would be HTTP, and WebRTC the API would be the fetch API.

The WebRTC protocol is available in other APIs/languages besides JavaScript. You can find servers and domain-specific tools as well for WebRTC. All of these implementations use the WebRTC protocol so they can interact with each other.

## Why should I learn WebRTC?

These are the things that WebRTC will give you. This list is not exhaustive but is some of the things you may appreciate during your journey. Don't worry if you don't know some of these terms yet, this book will teach them to you along the way.

* Open Standard
* Multiple Implementations
* Available in Browsers
* Mandatory Encryption
* NAT Traversal
* Repurposed existing technology
* Congestion Control
* Sub-second Latency

## WebRTC Protocol is a collection of other technologies

This is a topic that takes an entire book to explain. However, to start off we break it into four steps.

* Signaling
* Connecting
* Securing
* Communicating

These four steps happen sequentially. The prior step must be 100% successful for the subsequent one to even begin.

One peculiar fact about WebRTC is that each step is actually made up of many other protocols! To make WebRTC we stitch together many existing technologies. In that sense, WebRTC is more a combination and configuration of well-understood tech that has been around since the early 2000s.

Each of these steps has dedicated chapters, but it is helpful to understand them at a high level first. Since they depend on each other, it will help when explaining further the purpose of each of these steps.

### Signaling: How peers find each other in WebRTC

When a WebRTC Agent starts it has no idea who it is going to communicate with and what they are going to communicate about. Signaling solves this issue! Signaling is used to bootstrap the call so that two WebRTC agents can start communicating.

Signaling uses an existing protocol SDP (Session Description Protocol). SDP is a plain-text protocol. Each SDP message is made up of key/value pairs and contains a list of 'media sections'. The SDP that the two WebRTC Agents exchange contains details like.

* IPs and Ports that the agent is reachable on (candidates)
* How many audio and video tracks the agent wishes to send
* What audio and video codecs each agent supports
* Values used while connecting (uFrag/uPwd)
* Values used while securing (certificate fingerprint)

Note that signaling typically happens "out-of-band"; that is, applications generally don't use WebRTC itself to trade signaling messages. Any architecture suitable for sending messages can be used to relay the SDPs between the connecting peers, and many applications will use their existing infrastructure (like REST endpoints, WebSocket connections, or authentication proxies) to facilitate easy trading of SDPs between the proper clients.

### Connecting and NAT Traversal with STUN/TURN

The two WebRTC Agents now know enough details to attempt to connect to each other. WebRTC then uses another established technology called ICE.

ICE (Interactive Connectivity Establishment) is a protocol that pre-dates WebRTC. ICE allows the establishment of a connection between two Agents. These Agents could be on the same network, or on the other side of the world. ICE is the solution to establishing a direct connection without a central server.

The real magic here is 'NAT Traversal' and STUN/TURN Servers. These two concepts are all you need to communicate with an ICE Agent in another subnet. We will explore these topics in depth later.

Once ICE successfully connects, WebRTC then moves on to establishing an encrypted transport. This transport is used for audio, video, and data.


### Securing the transport layer with DTLS and SRTP

Now that we have bi-directional communication (via ICE) we need to establish secure communication. This is done through two protocols that pre-date WebRTC. The first protocol is DTLS (Datagram Transport Layer Security) which is just TLS over UDP. TLS is the cryptographic protocol used to secure communication over HTTPS. The second protocol is SRTP (Secure Real-time Transport Protocol).

First, WebRTC connects by doing a DTLS handshake over the connection established by ICE. Unlike HTTPS, WebRTC doesn't use a central authority for certificates. Instead, WebRTC just asserts that the certificate exchanged via DTLS matches the fingerprint shared via signaling. This DTLS connection is then used for DataChannel messages.

WebRTC then uses a different protocol for audio/video transmission called RTP. We secure our RTP packets using SRTP. We initialize our SRTP session by extracting the keys from the negotiated DTLS session. In a later chapter, we discuss why media transmission has its own protocol.

We are done! You now have bi-directional and secure communication. If you have a stable connection between your WebRTC Agents this is all the complexity you may need. Unfortunately, the real world has packet loss and bandwidth limits, and the next section is about how we deal with them.

### Communicating with peers via RTP and SCTP

We now have two WebRTC Agents with secure bi-directional communication. Let's start communicating! Again, we use two pre-existing protocols: RTP (Real-time Transport Protocol), and SCTP (Stream Control Transmission Protocol). SRTP is used to encrypt media exchanged over RTP, and SCTP is used to send DataChannel messages encrypted with DTLS.

RTP is quite minimal but provides what is needed to implement real-time streaming. The important thing is that RTP gives flexibility to the developer so they can handle latency, loss, and congestion as they please. We will discuss this further in the media chapter.

The final protocol in the stack is SCTP. SCTP allows many different delivery options for messages. You can optionally choose to have unreliable, out of order delivery so you can get the latency needed for real-time systems.


## WebRTC, a collection of protocols
WebRTC solves a lot of problems. At first, this may even seem over-engineered. The genius of WebRTC is really the humility. It didn't assume it could solve everything better. Instead, it embraced many existing single purpose technologies and bundled them together.

This allows us to examine and learn each part individually without being overwhelmed. A good way to visualize it is a 'WebRTC Agent' is really just an orchestrator of many different protocols.

{{<mermaid>}}
graph TB

webrtc{WebRTC Agent}

sctp{SCTP Agent}
dtls{DTLS Agent}
ice{ICE Agent}
stun{STUN Protocol}
turn{TURN Agent}
srtp{SRTP Agent}
sctp{SDP}
rtp{RTP}
rtcp{RTCP}

webrtc --> ice
webrtc --> dtls
webrtc --> sctp
webrtc --> srtp

ice --> turn
ice --> stun

srtp --> rtcp
srtp --> rtp
{{</mermaid>}}


## How does WebRTC (the API) work

This section shows how the JavaScript API maps to the protocol. This isn't meant as an extensive demo of the WebRTC API, but more to create a mental model of how it all ties together.
If you aren't familiar with either, it is ok. This could be a fun section to return to as you learn more!

#### `new RTCPeerConnection`
The `RTCPeerConnection` is the top-level 'WebRTC Session'. It contains all the protocols mentioned above. The subsystems are all allocated but nothing happens yet.

#### `addTrack`

`addTrack` creates a new RTP stream. A random SSRC will be generated for this stream. This stream will then be inside the Session Description generated by `createOffer` inside a media section. Each call to `addTrack` will create a new SSRC and media section.

Immediately after a SRTP Session is established these media packets will start being sent via ICE after being encrypted using SRTP.

#### `createDataChannel`

`createDataChannel` creates a new SCTP stream if no SCTP association exists. By default, SCTP is not enabled but is only started when one side requests a data channel.

Immediately after a DTLS Session is established, the SCTP association will start sending packets via ICE and encrypted with DTLS.

#### `createOffer`

`createOffer` generates a Session Description of the local state to be shared with the remote peer.

The act of calling `createOffer` doesn't change anything for the local peer.

#### `setLocalDescription`

`setLocalDescription` commits any requested changes. `addTrack`, `createDataChannel` and similar calls are all temporary until this call. `setLocalDescription` is called with the value generated by `createOffer`.

Usually, after this call, you will send the offer to the remote peer, and they will call `setRemoteDescription` with it.

#### `setRemoteDescription`

`setRemoteDescription` is how we inform the local agent about the remote candidates' state. This is how the act of 'Signaling' is done with the JavaScript API.

When `setRemoteDescription` has been called on both sides, the WebRTC Agents now have enough info to start communicating P2P!

#### `addIceCandidate`

`addIceCandidate` allows a WebRTC agent to add more remote ICE Candidates whenever they want. This API sends the ICE Candidate right into the ICE subsystem and has no other effect on the greater WebRTC connection.

#### `ontrack`

`ontrack` is a callback that is fired when a RTP packet is received from the remote peer. The incoming packets would have been declared in the Session Description that was passed to `setRemoteDescription`

WebRTC uses the SSRC and looks up the associated `MediaStream` and `MediaStreamTrack` and fires this callback with these details populated.

#### `oniceconnectionstatechange`

`oniceconnectionstatechange` is a callback that is fired that reflects the state of the ICE Agent. When you have network connectivity or when you become disconnected this is how you are notified.

#### `onstatechange`

`onstatechange` is a combination of ICE Agent and DTLS Agent state. You can watch this to be notified when ICE and DTLS have both completed successfully.
