---
title: Applied WebRTC
type: docs
weight: 8
---


# Applied WebRTC

This section is under construction, and needs your help! *Applied WebRTC* is a chapter about how applications get built "in the real world", so it wouldn't be complete without extensive input from the community. If you know something about WebRTC application architecture that isn't covered in this chapter, we want to know about it!

## By Use Case

The technologies behind WebRTC aren't just for video chatting -- since WebRTC is a generic real-time framework, applications are limitless. Some of the most common categories include:

__Each category will begin with a paragraph about how WebRTC solves the problem, notable benefits (or drawbacks) to solving this problem with WebRTC. Avoid just listing links to outside projects__

### Conferencing (audio/video)

Audio/Video Conferencing is one of the most popular use cases for WebRTC technology. The low-latency nature of WebRTC protocol is great for calls, and it's common to see conferences arranged in p2p mesh configuration (for low latency), or peering through an SFU (Selective Forwarding Unit) to improve call quality. Since codec support varies by browser, many conferencing servers allow browsers to broadcast using proprietary or non-free codecs like h264, and then re-encode to an open standard like VP8 at the server level; when the SFU performs an encoding task beyond just forwarding packets, it is now called an MCU (Multi-point Conferencing Unit). While SFU are notoriously fast and efficient and great for conferences, MCU can be very resource intensive! Some conferencing servers even perform heavy tasks like compositing (combining together) A/V streams, customized for each caller, to minimize client bandwidth use by sending only a single stream of all the other callers.

### Broadcasting

WebRTC can also be used to broadcast video streams in a one-to-many configuration. Typically, on the server side, this is accomplished very much like conferencing with an SFU (or MCU to encode additional profiles), though there are some modern attempts at using peer-to-peer mesh networks to relay video streams (see Distributed CDN below). Using WebRTC for broadcasting live video content is a great choice, and WebRTC typically has much lower latency than RTMP or HLS; however other protocols like HLS have better out-of-the-box support for streaming Video on Demand content.

### Remote Control 
### File-Transfer
### Distributed CDN
### IoT


## By Peering Patterns

Regardless of whether you use WebRTC for voice, video or DataChannel capabilities, everything starts with a `PeerConnection`. How peers connect to one another is a key design consideration in any WebRTC application, and there are many established approaches.

__Each of these sections should be expanded with a graphical representation of the peering pattern, a description of typical or notable use-cases, and a list of pros/cons or strengths/weaknesses, or "when to use".__

### Client-Server
#### SFU (Selective Forwarding Unit)
#### MCU (Multi-point Conferencing Unit)

### Peer-To-Peer
#### One-To-One
#### P2P Mesh
