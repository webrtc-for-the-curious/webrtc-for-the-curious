---
title: Signaling
type: docs
weight: 3
---

## Why do I need signaling?
When you create a WebRTC agent it knows nothing about the other peer. It has no idea who it is going to connect with or what they are going to send! Signaling is the inital bootstrapping that makes the call possible. After these values are exhanged the WebRTC agents then can communicate directly with each other.

Signaling messages are just text. The WebRTC agents don't care how they are transported. They are commonly shared via Websockets, but not a requirement.

## How does it work?

WebRTC uses an existing protcol called the Session Description Protocol. Via this protocol the two WebRTC Agents will share all the state required to establish a connection. The protocol itself is simple to read and understand. The complexity comes from understanding all the values that WebRTC
populates it with.

This protocol is not specific to WebRTC, so we can learn the Session Description Protocol first without even talking about WebRTC. WebRTC only really takes advantage of a subset of the protcol so we are only going to cover that.  After we understand the protocol we will move on to its applied usage in WebRTC.

## Session Description Protocol
The Session Description Protocol is defined in [RFC 4566](https://tools.ietf.org/html/rfc4566). It is a key/value protocol with a newline after each value. It will feel similar to an ini file.

The protocol is used to communicate a list of Media Descriptions. A Media Description usually maps to a single stream of media. So if you wanted to describe a call with three video streams and two audio tracks you would beed five Media Descriptions.

### What does Key/Value mean
Every line in a Session Description will start with a single character, this is your key. It will then be followed by an equal sign. Everything after that equal sign is the value. After the value is complete you will have a newline.

The Session Description Protocol defines all the keys that are valid. You can only use letters for keys as defined bt the protocol. These keys all have significant meaning, which will be explained later. 

Take this example Session Description. 

```
a=my-sdp-value
a=second-value
```

You have two lines. Each with the key `a`. The first line has the value `my-sdp-value`, the second line has the value `second-value`.

### WebRTC only uses some keys
Not all key values defined by the Session Description Protocol are used by WebRTC. The following are the only keys you need to understand. Don't worry about fully understanding yet, but this will be a handy reference in the future.

* `v` - Version, should be equal to '0'
* `o` - Origin, contains a unique ID useful for renegotiations
* `s` - Session Name, should be equal to '-'
* `t` - Timing, should be equal to '0 0'
* `m` - Meda Description, described in detail below
* `a` - Attribute, free text field this is the most common line in WebRTC
* `c` - Connection Data, should be equal to 'IN IP4 0.0.0.0' 

### Media Descriptions

The Media Description key is unlike any other. It is not just a value, but is the start if a block. 



### Full Example

```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 127.0.0.1
t=0 0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4002 RTP/AVP 96
a=rtpmap:96 VP8/90000
```

## Session Description Protocol and WebRTC

### Offers and Answers
### Transceivers
### Renegotiation
### Values used by WebRTC
### Simulcast
### Examples

```
v=0
o=- 3546004397921447048 1596742744 IN IP4 0.0.0.0
s=-
t=0 0
a=fingerprint:sha-256 0F:74:31:25:CB:A2:13:EC:28:6F:6D:2C:61:FF:5D:C2:BC:B9:DB:3D:98:14:8D:1A:BB:EA:33:0C:A4:60:A8:8E
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=setup:active
a=mid:0
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ssrc:350842737 cname:yvKPspsHcYcwGFTw
a=ssrc:350842737 msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=ssrc:350842737 mslabel:yvKPspsHcYcwGFTw
a=ssrc:350842737 label:DfQnKjQQuwceLFdV
a=msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=setup:active
a=mid:1
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=ssrc:2180035812 cname:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=ssrc:2180035812 mslabel:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 label:JgtwEhBWNEiOnhuW
a=msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
```
