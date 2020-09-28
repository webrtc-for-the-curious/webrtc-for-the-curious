---
title: Data Communication
type: docs
weight: 7
---

## What is Data Channel?

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

WebRTC (primarily) uses UDP. On top of UDP, there's SCTP, then DCEP which
controls establishment of data channels.

*Related sections for more details:*
* [Flow Control API](#flow-control-api)
{{</expand>}}

{{<expand "Question: How can I automate the flow control?">}}
*Short Answer:*

Yes, you can. WebRTC provides a set of methods and an event for it.

*Related sections for more details:*
* [Flow Control API](#flow-control-api)
{{</expand>}}

{{<expand "Question: Do messages arrive in the sequential order they were sent?">}}
*Short Answer:*

Yes. Optionally, you could tell the data channel to deliver message as it
they arrive even those messages reordered over the network.

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

You can send any data over data channel. In a browser case, it is your
responsibility to decode the data and pass it to a media player for rendering,
while it is automatically done when you use media channels.

*Related sections for more details:*
* [Audio and Video Communication](/docs/05-media-communication)
{{</expand>}}


## Functional Overview
### What does data channels solve?
* Application examples
  - Real-time network games
  - Game player action events
  - Asset exchange
  - Text chat
  - Collaborative file transfer (distributed storage p2p file sharing)
  - Monitoring IoT devices

### Protocol Stack
(TODO)

### Basic Features
* Reliability
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

