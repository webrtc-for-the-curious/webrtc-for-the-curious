---
title: Applied WebRTC
type: docs
weight: 99
---


# Applied WebRTC

This section is under construction, and needs your help! *Applied WebRTC* is a chapter about how applications get built "in the real world", so it wouldn't be complete without extensive input from the community. If you know something about WebRTC application architecture that isn't covered in this chapter, we want to know about it!

## By Use Case

The technologies behind WebRTC aren't just for video chatting -- since WebRTC is a generic real-time framework, applications are limitless. Some of the most common categories include:

__Each category will begin with a paragraph about how WebRTC solves the problem, notable benefits (or drawbacks) to solving this problem with WebRTC. Avoid just listing links to outside projects__

### Conferencing (audio/video)
### Broadcasting
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