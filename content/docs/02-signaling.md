---
title: Signaling
type: docs
weight: 3
---

## Why do I need signaling?
When you create a WebRTC agent it knows nothing about the other peer. It has no idea who it is going to connect with or what they are going to send! Signaling is the inital bootstrapping that makes the call possible. After these values are exhanged the WebRTC agents then can communicate directly with each other.

Signaling messages are just text. The WebRTC agents don't care how they are transported. They are commonly shared via Websockets, but not a requirement.


## How does it work?

WebRTC uses an existing protcol called the Session Description Protocol for signaling. WebRTC also adds one more concept, Offers and Answers.



The WebRTC API generates these messages by calling createOffer and createAnswer. 



## Session Description Protocol

### Protocol Format

### Values that matter for WebRTC



Signaling is the act of exchanging attributes and capabilities of the two WebRTC clients. When you start a WebRTC call these

