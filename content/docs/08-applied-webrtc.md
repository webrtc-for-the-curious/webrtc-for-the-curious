---
title: Applied WebRTC
type: docs
weight: 9
---


# Applied WebRTC

Now that you know how WebRTC works it is time to build with it. This chapter explores what people are building with WebRTC, and how they are building it. You will learn all the interesting things that are happening with WebRTC. The power of WebRTC comes as a cost. Building production grade WebRTC services is challenging. This chapter will try and explain those challenges before you hit them.

## By Use Case

The technologies behind WebRTC aren't just for video chatting -- since WebRTC is a generic real-time framework, applications are limitless. Some of the most common categories include:

### Conferencing

Conferencing was the use case that WebRTC was originally designed for. You can have two users directly connect to each other. Once they are connected they can share their webcams, or maybe their desktop. Participants can send and receive as many streams as they want. They can also add and remove those streams at any time.

Going beyond just media DataChannels are very useful for building a conferencing experience. Users can send metadata or share documents. You can create multiple streams and have multiple conversations going at once.

Conferencing becomes more difficult as more users join the call. How you scale is entirely up to you. The WebRTC topologies section covers this further.

### Broadcasting

WebRTC can also be used to broadcast video streams one-to-many.

### Remote Control
### File-Transfer

A desktop application could be created to capture a screenshot. Once the screenshot is captured on the clipboard of Device A, it could generate a temporary link for another device to access. Once Device B opens the link, a PeerConnection could be created back to Device A, the data could be streamed using the `DataChannel` part of WebRTC and once the transmission is successful the connection could tear down. This would effectively create a peer-to-peer secure way to transfer files over the internet.

### Distributed CDN
### IoT

When a video doorbell detects movement, it could supply the cameras RTP stream and initiated a new `PeerConnection` with a central server for recording or send a push notification to a mobile device to ask it to connect as a peer. This would establish a real-time communication between the front door and the mobile app. The mobile app could send real time audio back to the doorbell or it could initiate secure remote controls over WebRTC.

### Protocol Bridging


## WebRTC Topologies

Regardless of whether you use WebRTC for voice, video or DataChannel capabilities, everything starts with a `PeerConnection`. How peers connect to one another is a key design consideration in any WebRTC application, and there are many established approaches.

### Client-Server

The low-latency nature of WebRTC protocol is great for calls, and it's common to see conferences arranged in p2p mesh configuration (for low latency), or peering through an SFU (Selective Forwarding Unit) to improve call quality. Since codec support varies by browser, many conferencing servers allow browsers to broadcast using proprietary or non-free codecs like h264, and then re-encode to an open standard like VP8 at the server level; when the SFU performs an encoding task beyond just forwarding packets, it is now called an MCU (Multi-point Conferencing Unit). While SFU are notoriously fast and efficient and great for conferences, MCU can be very resource intensive! Some conferencing servers even perform heavy tasks like compositing (combining together) A/V streams, customized for each caller, to minimize client bandwidth use by sending only a single stream of all the other callers.


#### SFU (Selective Forwarding Unit)
#### MCU (Multi-point Conferencing Unit)

### Peer-To-Peer
#### One-To-One
#### P2P Mesh
