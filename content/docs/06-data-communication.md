---
title: Data Communication
type: docs
weight: 7
---

# What is Data Channel?

### Questions From The Curious 
I know many of you have a bunch of questions similar to the ones shown below.
Let's get them quickly answered first! (Click on the questions to expand for the answer.)

{{<expand "Question: What’s the difference from TCP?">}}
*Short Answer:*

Peer-to-peer connection (NAT traversal) is possible.
While it provides "guaranteed delivery" like TCP, it also provides none-reliable delivery like UDP.

*Related sections for more details:*
* [SCTP](#sctp)
{{</expand>}}

{{<expand "Question: How many channels can we have?">}}
*Short Answer:*

Unlimited (theoretically 65536 channels as stream identifier has 16 bits)

*Related sections for more details:*
* [SCTP](#sctp)
{{</expand>}}

{{<expand "Question: What are data channels good for?">}}
*Short Answer:*

Any data transfer other than audio and video.
As it has various delivery options (partial reliability), it has broader applications than TCP.

*Related sections for more details:*
* [Functional Overview](#functional-overview)
{{</expand>}}

{{<expand "Question: Any limit in bandwidth?">}}
*Short Answer:*

As much as the underlying network allows.
The underlying SCTP protocol is designed so that you cannot overwhelm the network.
{{</expand>}}

{{<expand "Question: Can we send binary data?">}}
*Short Answer:*

Yes, you can send both text and binary data.

*Related sections for more details:*
* [Data Channel API](#data-channel-api)
{{</expand>}}

{{<expand "Question: How about congestion control?">}}
*Short Answer:*
* Yes it has congestion control.

*Related sections for more details:*
* [SCTP](#sctp)
{{</expand>}}

{{<expand "Question: How is the latency compared to that of TCP?">}}
*Short Answer:*
Even though the WebRTC's SCTP lives in "user space", performance is comparable to that of TCP.
Data channels support "Partial-reliability" option which can reduce latency caused by
data retransmissions over a lossy connection.
*Related sections for more details:*
* [Partial Reliability](#partial-reliability)
{{</expand>}}

{{<expand "Question: What technologies are used in data channels?">}}
*Short Answer:*
WebRTC (primarily) uses UDP. On top of UDP, there's SCTP, then DCEP which
controls establishment of data channels.

*Related sections for more details:*
* [Protocol Stack](#protocol-stack)
{{</expand>}}

{{<expand "Question: How do I know if I am sending too much?">}}
*Short Answer:*

Calls on the send method on a data channel always return immediately. It does not mean the data was sent on the wire.
It will first be written to a buffer... When you call send() faster than your network can process, the buffered size will grow.
[RTCDataChannel.bufferedAmount](https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel/bufferedAmount) is your friend.


*Related sections for more details:*
* [Flow Control API](#flow-control-api)
{{</expand>}}

{{<expand "Question: Do messages arrive in the order they were sent?">}}
*Short Answer:*

By default, Yes. Optionally, you could disable it to receive messages as it
arrives.

*Related sections for more details:*
* [Data Channel API](#data-channel-api)
* [SCTP](#sctp)
{{</expand>}}

{{<expand "Question: When do you use unordered delivery option?">}}
*Short Answer:*

When newer information obsoletes the old such as positional information of an
object, or each message is independent from the others and need to avoid
head-of-line blocking delay.

*Related sections for more details:*
* [Data Channel Options](#data-channel-options)
* [SCTP](#sctp)
{{</expand>}}

{{<expand "Question: Can we send audio or video via data channel?">}}
*Short Answer:*

You could send any data over data channel. In a browser case, it is your
responsibility to decode the data and pass it to a media player for rendering,
where it is automatically done when you use media channels.

*Related sections for more details:*
* [Audio and Video Communication](/docs/05-media-communication)
{{</expand>}}

## Functional Overview
Data channel can deliver any types of data. If you wish, you send send audio or video
data over the data channel too, but if you need to playback the media in real-time,
using media channels (See [Media Communication]({{< ref "05-media-communication.md" >}})) that uses RTP/RTCP protocols are the better options.

### What are the applications of data channel?
Applicability of the data channel is unlimited! The data channel solves packet loss,
congestion problems and many other stuff for you and provide you with very simple
API to deliver you your data to your peer in real-time. You just need to focus on what
your application wants to achieve, and be creative.

Here are some example applications using the data channel:
  - Real-time network games
  - Serverless home automation from remote
  - Text chat
  - Animation (series of still images)
  - P2P CDN (Content Delivery Network)
  - Monitoring data from IoT
  - Continuous ingestion of time-series data from sensor devices
  - Real-time image recognition with AI from cameras

### Protocol Stack Overview
The data channel is comprised of the following 3 layers:
* Data Channel Layer
* DCEP (Data channel Establishment Protocol) Layer
* SCTP (Stream Control Transmission Protocol) Layer

{{< figure src="/images/06-datachan-proto-stack.png">}}

#### Data Channel Layer
This layer provides API.

#### Data channel Establishment Protocol Layer
This layer is responsible for the data channel handshake with the peer. It uses a
SCTP stream as a control channel to negotiate capabilities such as ordered delivery,
maxRetransmits/maxPacketLifeTime (a.k.a. "Partial-reliability"), etc.

#### SCTP Protocol Layer
This is the heart of the data channel. What it does includes:

* Channel multiplexing (In SCTP, channels are called "streams")
* Reliable delivery with TCP-like retransmission mechanism
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
#### Open/ACK handshake
#### PPID
#### Parameter exchange

## Reference to RFCs

