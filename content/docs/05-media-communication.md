---
title: Media Communication
type: docs
weight: 6
---

## What do I get from WebRTC's media communication?
WebRTC allows you to send and receive an unlimited amount of audio and video streams. You can add and remove these streams at anytime during a call. These streams could all be independent, or they could be bundled together! You could send a video feed of your desktop, and then include audio/video from your webcam.

The WebRTC protocol is codec agnostic. The underlying transport supports everything, even things that don't exist yet! However, the WebRTC Agent you are communicating with may not have the necessary tools to accept it.

WebRTC is also designed to handle dynamic network conditions. During a call your bandwidth might increase, or decrease. Maybe you all the sudden experience lots of packet loss. The protocol is designed to handle all of this. WebRTC responds to network conditions and tries to give you the best experience possible with the resources available.

## How does it work?
WebRTC uses two pre-existing protocols RTP and RTCP, both defined in [RFC 1889](https://tools.ietf.org/html/rfc1889)

RTP is the protocol that carries the media. It was designed to allow real-time delivery of video. It doesn't stipulate any rules around latency or reliability, but gives you the tools to implement them. RTP gives you streams, so you can run multiple media feeds over one connection. It also gives you the timing and ordering information you need to feed a media pipeline.

RTCP is the protocol that communicates metadata about the call. The format is flexible enough so you can add whatever you want. This is used to communicate statistics about the call. It is also necessary to handle packet loss and to implement congestion control. It gives you the bi-directional communication necessary to respond to network conditions changing.

## RTP
### Packet Format
Every RTP packet has the following structure:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       Sequence Number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           Timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Synchronization Source (SSRC) identifier            |
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
|            Contributing Source (CSRC) identifiers             |
|                             ....                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
Version is always 2

#### Padding (P)
Padding is a bool that controls if the payload has padding.

The last byte of the payload contains a count of how many padding bytes
were added.

#### Extension (X)


#### CSRC count (CC)

#### Marker (M)

#### Payload Type (PT)

#### Sequence Number

#### Timestamp

#### Synchronization Source (SSRC)

#### Contributing Source (CSRC)

### Extensions
### Mapping Payload Types to Codecs

## RTCP
### Packet Format

## Latency vs Quality
### Packet Loss
### Jitter
### Congestion
### Round Trip Time
### Maximum transmission unit

## How does RTP/RTCP Handle This
### NACK
### FEC
### JitterBuffer
### Post-Decode Audio/Video Improvements
