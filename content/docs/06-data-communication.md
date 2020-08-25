---
title: Data Communication
type: docs
weight: 7
---

## What is Data Channel?

### Questions From The Curious 

* What’s the difference with TCP?
* How many channels can we have?
* Why do we need data channels?
* Any limit in data size? (max size, 0 byte data?)
* Any limit in bandwidth?
* Can we send binary data? JSON?
* What’s good about data channels?
* Difference from WebSocket?
* How about congestion control?
* How about latency?
* What technologies are used in data channels? (protocol stack)
* How do I know I am sending too much?
* How can I automate the flow control?
* How about unordered traffic like UDP?
* How about unreliable transfers like UDP?
* Would unreliable transfer help to yield low latency?
* Can we send video via data channel?

### What does data channels solve?
* Application examples
  - Real-time network games
  - Game player action events
  - Asset exchange
  - Text chat
  - Collaborative file transfer (distributed storage p2p file sharing)
  - Monitoring IoT devices

### Fundamental features
### Reliability
### Congestion avoidance
### Flow control

## Data Channel API
### Connection / Teardown
### Data channel options (label, ID, partial reliability)
### Flow control API (bufferedAmount, threshold event, etc)

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

### DCEP
#### Open/ACK handshake
#### PPID
#### Parameter exchange

## Reference to RFCs

