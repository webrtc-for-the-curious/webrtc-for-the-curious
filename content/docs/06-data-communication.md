---
title: Data Communication
type: docs
weight: 7
---

# What is Data 


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

