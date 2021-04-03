---
title: Media Communication
type: docs
weight: 7
---

# What do I get from WebRTC's media communication?
WebRTC allows you to send and receive an unlimited amount of audio and video streams. You can add and remove these streams at anytime during a call. These streams could all be independent, or they could be bundled together! You could send a video feed of your desktop, and then include audio/video from your webcam.

The WebRTC protocol is codec agnostic. The underlying transport supports everything, even things that don't exist yet! However, the WebRTC Agent you are communicating with may not have the necessary tools to accept it.

WebRTC is also designed to handle dynamic network conditions. During a call your bandwidth might increase, or decrease. Maybe you suddenly experience lots of packet loss. The protocol is designed to handle all of this. WebRTC responds to network conditions and tries to give you the best experience possible with the resources available.

## How does it work?
WebRTC uses two pre-existing protocols RTP and RTCP, both defined in [RFC 1889](https://tools.ietf.org/html/rfc1889)

RTP (Real-time Transport Protocol) is the protocol that carries the media. It was designed to allow for real-time delivery of video. It does not stipulate any rules around latency or reliability, but gives you the tools to implement them. RTP gives you streams, so you can run multiple media feeds over one connection. It also gives you the timing and ordering information you need to feed a media pipeline.

RTCP (RTP Control Protocol) is the protocol that communicates metadata about the call. The format is very flexible and allows you to add any metadata you want. This is used to communicate statistics about the call. It is also used to handle packet loss and to implement congestion control. It gives you the bi-directional communication necessary to respond to changing network conditions.

## Latency vs Quality
Real-time media is about making trade-offs between latency and quality. The more latency you are willing to tolerate, the higher quality video you can expect.

### Real World Limitations
These constraints are all caused by the limitations of the real world. They are all characteristics of your network that you will need to overcome.

### Video is Complex
Transporting video isn't easy. To store 30 minutes of uncompressed 720 8-bit video you need ~110Gb. With those numbers a 4 person conference call isn't going to happen. We need a way to make it smaller, and the answer is video compression. That doesn't come without downsides though.

## Video 101
We aren't going to cover video compression in depth, but just enough to understand why RTP is designed the way it is. Video compression encodes video into a new format that requires fewer bits to represent the same video, usually with a slight loss in quality.

### Lossy and Lossless compression
It can be lossless (no information is lost) or lossy (information may be lost). RTP typically uses lossy compression. It is better to have some details lost in the picture, then have it not arrive at all.

### Intra and Inter frame compression
Video compression comes in two types. The first is intra-frame. Intra-frame compression reduces the bits used to describe a single video frame. The same techniques are used to compress still pictures, like the JPEG compression method.

The second type is inter-frame compression. Since video is made up of many pictures we look for ways to not send the same information twice.

### Inter-frame types
You then have three frame types

* **I-Frame** - A complete picture, can be decoded without anything else
* **P-Frame** - A partial picture, is a modification of previous pictures
* **B-Frame** - A partial picture, is a modification of previous and future pictures

The following is visualization of the three frame types.

{{< figure src="/images/05-frame-types.svg">}}

### Video is delicate
Video compression is incredibly stateful, making it difficult to transfer over the internet. What happens If you lose part of a I-Frame? How does a P-Frame know what to modify? As video compression gets more complex this is becoming even more of a problem. Luckily RTP and RTCP have the solution.

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
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
`Version` is always `2`

#### Padding (P)
`Padding` is a bool that controls if the payload has padding.

The last byte of the payload contains a count of how many padding bytes were added.

#### Extension (X)
If set, the RTP header will have extensions. This is described in greater detail below.

#### CSRC count (CC)
The amount of `CSRC` identifiers that follow after the `SSRC`, and before the payload.

#### Marker (M)
The marker bit has no pre-set meaning, and can be used however the user likes.

In some cases it is set when a user is speaking. It is also commonly used to mark a keyframe.

#### Payload Type (PT)
`Payload Type` is a unique identifier for what codec is being carried by this packet.

For WebRTC the `Payload Type` is dynamic. VP8 in one call may be different then another. The Offerer in the call determines the mapping of `Payload Types` to codecs in the `Session Description`.

#### Sequence Number
`Sequence Number` is used for ordering packets in a stream. Every time a packet is sent the `Sequence Number` is incremented by one.

RTP is designed to be useful over lossy networks. This gives the receiver a way to detect when packets have been lost.

#### Timestamp
The sampling instant for this packet. This is not a global clock, but how much time has passed in the media stream.

#### Synchronization Source (SSRC)
A `SSRC` is the unique identifier for this stream. This allows you to run multiple streams of media over a single stream.

#### Contributing Source (CSRC)
A list that communicates what `SSRC`es contributed to this packet.

This is commonly used for talking indicators. Lets say server side you combined multiple audio feeds into a single RTP stream. You could then use this field to say 'Input stream A and C were talking at this moment'

#### Payload
The actual payload data. Might end with the count of how many padding bytes were added, if the padding flag is set.

### Extensions

## RTCP

### Packet Format
Every RTCP packet has the following structure:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|    RC   |       PT      |             length            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
`Version` is always `2`

#### Padding (P)
`Padding` is a bool that controls if the payload has padding.

The last byte of the payload contains a count of how many padding bytes
were added.

#### Reception Report Count (RC)
The number of reports in this packet. A single RTCP Packet can contain multiple events.

#### Packet Type (PT)
Unique Identifier for what type of RTCP Packet this is. A WebRTC Agent doesn't need to support all these types, and support between Agents can be different. These are the ones you may commonly see though.

* Full INTRA-frame Request (FIR) - `192`
* Negative ACKnowledgements (NACK) - `193`
* Sender Report - `200`
* Receiver Report - `201`
* Generic RTP Feedback - `205`

The significance of these packet types will be described in greater detail below.

### Full INTRA-frame Request
This RTCP message notifies the sender that it needs to send a full image. This is for when the encoder is giving you partial frames, but you aren't able to decode them.

This could happen because you had lots of packet loss, or maybe the decoder crashed.

### Negative ACKnowledgements
A NACK requests that a sender re-transmits a single RTP Packet. This is usually caused when a RTP Packet is lost, but could also happen because it is late.

NACKs are much more bandwidth efficent than requesting that the whole frame get sent again. Since RTP breaks up packets into very small chunks, you are really just requesting one small missing piece.

### Sender/Receiver Reports
These reports are used to send statistics between agents. This communicates the amount of packets actually received and jitter.

The reports can be used for diagnostics and Congestion Control.

## How RTP/RTCP solve problems together
RTP and RTCP then work together to solve all the problems caused by networks. These techniques are still constantly changing!

### Negative Acknowledgment
Also known as a NACK. This is one method of dealing with packet loss with RTP.

A NACK is a RTCP message sent back to a sender to request re-transmission. The receiver crafts a RTCP message with the SSRC and Sequence Number. If the sender does not have this RTP packet available to re-send, it just ignores the message.

### Forward Error Correction
Also known as FEC. Another method of dealing with packet loss. FEC is when you send the same data multiple times, without it even being requested. This is done at the RTP level, or even lower with the codec.

If the packet loss for a call is steady then FEC is a much lower latency solution than NACK. The round trip time of having to request, and then re-transmit the packet can be significant for NACKs.

### Adaptive Bitrate and Bandwidth Estimation
As discussed in [Real-time networking](05-real-time-networking.md) networks are unpredictable and unreliable. Bandwidth availability can change multiple times throughout a session.
It is not uncommon to see available bandwidth change dramatically (orders of magnitude) within a second.

The main idea is to adjust encoding bitrate based on predicted, current, and future available network bandwidth.
This ensures that video/audio signal of the best possible quality is transmitted and the connection does not get dropped because of network congestion.
Heuristics that model the network behavior and tries to predict it is known as Bandwidth estimation.

There is a lot of nuance to this, so lets explore in greater detail.

## Communicating Network Status
The first road block with implementing Congestion Control is that UDP and RTP don't communicate network status. As a sender I have no idea when my packets are arriving or if they are arriving at all!

RTP/RTCP has 3 different solutions to this problem. They all have their pros and cons. What you use will depend on what clients you are working with. What is the topology you are working with. Or even just how many development time you have available.

### Receiver Reports
Receiver Reports are RTCP messages, the original way to communicate network status. You can find them in [RFC 1889](https://tools.ietf.org/html/rfc1889). They are sent on a schedule for each SSRC and contain the following fields:

* **Fraction Lost** -- What percentage of packets have been lost since the last Receiver Report.
* **Cumulative Number of Packets Lost** -- How many packets have been lost during the entire call.
* **Extended Highest Sequence Number Received** -- What was the last Sequence Number received, and how many times has it rolled over.
* **Interarrival Jitter** -- The rolling Jitter for the entire call.

### TMMBR, TMMBN and REMB
The next generation of Network Status messages all involve receivers messaging senders via RTCP with explicit bitrate requests.

* **Temporary Maximum Media Stream Bit Rate Request** - A mantissa/exponent of a requested bitrate for a single SSRC.
* **Temporary Maximum Media Stream Bit Rate Notification** - A message to notify that a TMMBR has been received.
* **Receiver Estimated Maximum Bitrate** - A mantissa/exponent of a requested bitrate for the entire session.

TMMBR and TMMBN came first and are defined in [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB came later, there was a draft submitted in [draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), but it was never standardized.

A session that uses REMB would look like the following {{< figure src="/images/05-remb.png">}}

### Transport Wide Congestion Control
Transport Wide Congestion Control is the latest development in RTCP network status communication.

TWCC uses a quite simple principle:

{{< figure src="/images/05-twcc-idea.png">}}

Unlike in REMB, a TWCC receiver doesn't try to estimate it's own incoming bitrate. It just lets the sender know which packets were received and when. Based on these reports, the sender has a very up-to-date idea of what is happening in the network.

- The sender creates an RTP packet with a special TWCC header extension, containing a list of packet sequence numbers.
- The receiver responds with a special RTCP feedback message letting the sender know if and when each packet was received.

The sender keeps track of sent packets, their sequence numbers, sizes and timestamps.
When the sender receives RTCP messages from the receiver, it compares the send inter-packet delays with receive delays.
If the receive delays increase, it means network congestion is happenning and the sender must act on it.

In the diagram below, the median interpacket delay increase is +20 msec, a clear indicator of network congestion happening.

{{< figure src="/images/05-twcc.png">}}

TWCC provides the raw data and an excellent view into real time network conditions:
- Almost instant packet loss statistics, not only the percentage lost, but the exact packets that were lost.
- Accurate send bitrate.
- Accurate receive bitrate.
- A jitter estimate.
- Differences between send and receive packet delays.

A trivial congestion control algrorithm to estimate the incoming bitrate on the receiver from the sender is to sum up packet sizes received, and divide it by the remote time elapsed.


## Generating a Bandwidth Estimate
Now that we have information around the state of the network we can make estimates around the bandwidth available. In 2012 the IETF started the RMCAT (RTP Media Congestion Avoidance Techniques) working group.
This working group contains multiple submitted standards for congestion control algorithms. Before then Congestion Controllers algorithms were proprietary.

The most deployed implementation is 'A Google Congestion Control Algorithm for Real-Time Communication' defined in [draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).
In can run in two passes. First a 'loss based' pass that just uses Receiver Reports. If TWCC is available it will also take that additional data into consideration.
It predicts the current and future network bandwidth by using a [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter).

There are several alternatives to GCC, for example [NADA: A Unified Congestion Control Scheme for Real-Time Media](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) and [SCReAM - Self-Clocked Rate Adaptation for Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
