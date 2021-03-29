---
title: Applied WebRTC
type: docs
weight: 9
---

# Applied WebRTC

Now that you know how WebRTC works it is time to build with it. This chapter explores what people are
building with WebRTC, and how they are building it. You will learn all the interesting things that are
happening with WebRTC. The power of WebRTC comes as a cost. Building production grade WebRTC services is
challenging. This chapter will try and explain those challenges before you hit them.

## By Use Case

Many think WebRTC is just the technology conferencing in the web browser. It is so much more then that though!
WebRTC is used for a wide range of use cases. New use cases showing up all the time. These are some of the common ones
and how WebRTC is revolutionizing them.

### Conferencing

Conferencing is the original use case for WebRTC. The protocol contains a few necessary features that no other protocol offers
in the browser. You could build a conferencing system with WebSockets and it may work in optimal conditions. If you want
something that can be deployed in real world network conditions WebRTC is the best choice.

WebRTC provides congestion control and adaptive bitrate for media. As the conditions of the network change users will still get the
best experience possible. Developers don't have to write any additional code to measure these conditions either.

Participants can send and receive multiple streams. They can also add and remove those streams at any time. Codecs are negotiated
as well. All of this functionality is provided by the browser, no custom code is required to be written by the developer.

Conferencing also benefits from data channels. Users can send metadata or share documents. You can create multiple streams
and configure them if you need performance more then reliability.

### Broadcasting

Lots of new projects are starting to appear in the broadcast space that use WebRTC. The protocol has a lot to offer for both the publisher
and consumer of media.

WebRTC being in the browser makes for it easy for users to publish video. It removes the requirement for users to download a new client.
Any platform that has a web browser can publish video. Publishers can then send multiple tracks and modify/remove them at anytime. This is
a huge improvement over legacy protocols that only allowed one audio/one video track per connection.

WebRTC gives developers greater control over the latency/quality trade-offs. It could be more important that latency never exceeds a
certain threshold, and you are willing to tolerate some decoding artifacts. You can configure the viewer to play media as soon as it
arrives. With other protocols that run over TCP that isn't as easy. In the browser you can request data and that is it.

### Remote Access

Remote Access is when you remotely access another computer via WebRTC. You could have complete control of the remote host, or maybe just a
single application.  This is great for running computationally tasks when the local hardware can't do it. Like running a new video game, or
CAD software. WebRTC was able to revolutionize the space in three ways.

WebRTC can be used to remotely access a host that isn't world routable. With NAT Traversal you can access a computer that is only available
via STUN. This is great for security and privacy. Your users don't have to route video through a ingest or 'jump box'. NAT Traversal also
makes deployments easier. You don't have to worry about port forwarding or setting up a static IP ahead of time.

Data channels are really powerful as well in this scenario. They can be configured so that only the latest data is accepted. With TCP run the
risk of encountering Head-of-line blocking. A old mouse click or keypress could arrive late, and block the subsequent ones from being accepted.
WebRTC's data channels are designed to handle this and can be configured to not retry on lost packets. You can also measure the backpressure and
make sure that you aren't sending more data then your network supports.

WebRTC being available in the browser has been a huge quality of life improvement. You don't have to download a proprietary client to start the
session. More and more clients are coming with WebRTC bundled, smart TVs are getting full web browsers now.

### File Sharing and Censorship Circumvention

File Sharing and Censorship Circumvention are dramatically different problems. However, WebRTC solves the same problems for them both. It makes
them both easily available and harder to block.

The first problem that WebRTC solves is getting the client. If you want to join a file sharing network you need to download the client. Even if
the network is distributed, you still need to get the client first.  In a restricted network the download will often be blocked. Even if you
can download it the user may not be able to install/run the client. WebRTC is available in every web browser already making it readily available.

The second problem that WebRTC solves is your traffic being blocked. If you use a protocol that is just for file sharing or censorship circumvention
it is much easier to block it.  Since WebRTC is a general purpose protocol blocking it would impact everyone. Blocking WebRTC might prevent other
users of the network from joining conference calls.

### IoT

When a video doorbell detects movement, it could supply the cameras RTP stream and initiated a new `PeerConnection` with a central server
for recording or send a push notification to a mobile device to ask it to connect as a peer. This would establish a real-time communication
between the front door and the mobile app. The mobile app could send real time audio back to the doorbell or it could initiate secure remote
controls over WebRTC.

### Media Protocol Bridging

### Data Protocol Bridging

### Robotics

### Distributed CDN

## WebRTC Topologies

WebRTC is a protocol for connecting two agents, so how are developers connecting hundreds of people at once? There are a few different
ways you can do it and they all have pros and cons.

### Peer-To-Peer
#### One-To-One
#### P2P Mesh

### Client-Server
The low-latency nature of WebRTC protocol is great for calls, and it's common to see conferences arranged in p2p mesh configuration
(for low latency), or peering through an SFU (Selective Forwarding Unit) to improve call quality. Since codec support varies by browser,
many conferencing servers allow browsers to broadcast using proprietary or non-free codecs like h264, and then re-encode to an open standard
like VP8 at the server level; when the SFU performs an encoding task beyond just forwarding packets, it is now called an MCU (Multi-point Conferencing Unit).
While SFU are notoriously fast and efficient and great for conferences, MCU can be very resource intensive! Some conferencing servers even
perform heavy tasks like compositing (combining together) A/V streams, customized for each caller, to minimize client bandwidth use by
sending only a single stream of all the other callers.

#### SFU (Selective Forwarding Unit)
#### MCU (Multi-point Conferencing Unit)
