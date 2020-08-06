---
title: Signaling
type: docs
weight: 3
---

## Why do I need signaling?
When you create a WebRTC agent it knows nothing about the other peer. It has no idea who it is going to connect with or what they are going to send! Signaling is the inital bootstrapping that makes the call possible. After these values are exhanged the WebRTC agents then can communicate directly with each other.

Signaling messages are just text. The WebRTC agents don't care how they are transported. They are commonly shared via Websockets, but not a requirement.


## How does it work?

WebRTC uses an existing protcol called the Session Description Protocol. The protocol is simple, but the 

## Session Description Protocol
The Session Description Protocol is defined in [RFC 4566](https://tools.ietf.org/html/rfc4566). It is a key/value protocol with a newline after each value. It will feel similar to an ini file. They will be easy to read, but the complexity comes from understanding the values and what they mean.

WebRTC only really takes advantage of a subset of the protcol so we are only going to cover that. After we understand tbe protocol we will move on to its applied usage in WebRTC.

### Keys used by WebRTC
### Media Sections
### Examples

## Session Description Protocol and WebRTC

### Offers and Answers
### Transceivers
### Renegotiation
### Values that matter for WebRTC
### Simulcast
### Examples


