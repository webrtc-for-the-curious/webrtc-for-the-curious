---
title: Data Communication
type: docs
weight: 8
---

# What is Data


## Functional Overview
A data channel can deliver any type of data. If you wish, you can send audio or video data over the data channel too. But if you need to playback media in real-time, using media channels (see [Media Communication]({{< ref "06-media-communication.md" >}})) that use RTP/RTCP protocols is a better option.

### What are the applications of data channel?
Applicability of the data channel is unlimited! The data channel solves packet loss,
congestion problems, and many other things for you. It provides you with a very simple
API to deliver your data to your peer in real-time. You just need to focus on what
your application wants to achieve.

Here are some example applications using the data channel:
  - Real-time network games
  - Serverless remote home automation
  - Text chat
  - Animation (series of still images)
  - P2P CDN (Content Delivery Network)
  - Monitoring data from IoT
  - Continuous ingestion of time-series data from sensor devices
  - Real-time image recognition with AI from cameras

### Protocol Stack Overview
The data channel is comprised of the following 3 layers:
* Data Channel Layer
* DCEP (Data Channel Establishment Protocol) Layer
* SCTP (Stream Control Transmission Protocol) Layer

{{< figure src="/images/06-datachan-proto-stack.png">}}

#### Data Channel Layer
This layer provides the API.
The API largely mimics that of WebSockets, making it relatively easy for web developers
to repurpose existing client-server WebSocket based code to work over the P2P data channel.
A single peer connection can have many data channels, saving you the bother of
multiplexing and demultiplexing different data sources and sinks. Just create one data channel per
class of data you need to exchange, and the peer connection does the rest.
Unlike WebSockets data channels have lables which are assigned by the creator and can be used by
recipient to figure out which data channel is which.

#### Data Channel Establishment Protocol Layer
This layer is responsible for the data channel handshake with the peer. It uses a
SCTP stream as a control channel to negotiate capabilities such as ordered delivery,
`maxRetransmits`/`maxPacketLifeTime` (a.k.a. "Partial-reliability"), set the channel's label and so on.

#### SCTP Protocol Layer
This is the heart of the data channel. What it does includes:

* Channel multiplexing (In SCTP, channels are called "streams")
* Reliable delivery using a TCP-like retransmission mechanism
* Partial-reliability options
* Congestion Avoidance
* Flow Control

## Data Channel API
### Connection / Teardown
### Data Channel Options
### Flow Control API

## Data Channel in Depth
### SCTP
#### Connection establishment flow
#### Connection teardown flow
#### Keep-alive mechanism
#### How does a user message get sent?
#### TSN and retransmission
#### Congestion avoidance
#### Selective ACK
#### Fast retransmission/recovery
#### Partial Reliability

### DCEP
DCEP is a simple 2 packet protocol which describes the behaviour of a given data channel.
It does not require a network round trip, so subsequent data for the channel can be included in the same packet.
This makes establishing data channels fast and cheap.

#### Open/ACK handshake
```
0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |  Message Type |  Channel Type |            Priority           |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                    Reliability Parameter                      |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |         Label Length          |       Protocol Length         |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \                                                               /
     |                             Label                             |
     /                                                               \
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \                                                               /
     |                            Protocol                           |
     /                                                               \
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
Here is a list of chanel types and the associated reliability parameter
that will be applied when packets are lost or received in the wrong order.
```
DATA_CHANNEL_OPEN
Message Type: 0x03
     +================================================+=============+
     | Channel Type                                   | Reliability |
     |                                                |  Parameter  |
     +================================================+=============+
     | DATA_CHANNEL_RELIABLE                          |   Ignored   |
     +------------------------------------------------+-------------+
     | DATA_CHANNEL_RELIABLE_UNORDERED                |   Ignored   |
     +------------------------------------------------+-------------+
     | DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT           |  Number of  |
     |                                                |     RTX     |
     +------------------------------------------------+-------------+
     | DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED |  Number of  |
     |                                                |     RTX     |
     +------------------------------------------------+-------------+
     | DATA_CHANNEL_PARTIAL_RELIABLE_TIMED            | Lifetime in |
     |                                                |      ms     |
     +------------------------------------------------+-------------+
     | DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED  | Lifetime in |
     |                                                |      ms     |
     +------------------------------------------------+-------------+
```
Reliable is largely equivelent to TCP.

Reliable_Unordered requires a special mention. It means that when a packet is dropped by the network, only the message that the packet is part of will be delayed until it is resent. Other messages which were sent later may be delivered earlier. You can use this mode when the sequence that messages are received is less important than the speed of their arrival. In this mode message delivery still enforced, but the ordering is not. This mode can be thought of as a halfway house between TCP and UDP.

The remaining modes are equivelent to a UDP based protocols with differing retry/failure rules.

```
DATA_CHANNEL_ACK
Message Type: 0x02

      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |  Message Type |
     +-+-+-+-+-+-+-+-+

```
There is no DCEP NACK.
DataChannel opens always succeed, because they are carried on the same SCTP stream as the data, which has already suceeded!

#### PPID
The SCTP PPID for WebRTC DCEP is 50. DCEP messages are processed apart from the rest of the data in the SCTP stream and not passed back up to the web application or service.

#### Parameter exchange
In theory it is possible to create a datachannel using out-of-band non-DCEP negotiation in SDP. Don't.

## Reference to RFCs
https://datatracker.ietf.org/doc/rfc8832/?include_text=1
