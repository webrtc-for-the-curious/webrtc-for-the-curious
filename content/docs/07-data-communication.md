---
title: Data Communication
type: docs
weight: 8
---

# What do I get from WebRTC's data communication?
WebRTC provides data channels for data communication. Between two peers you can open 65,534 data channels.
A data channel is datagram based, and each has its own durability settings. By default each data
channel has guaranteed ordered delivery.

If you are approaching WebRTC from a media background data channels might seem wasteful. Why do
I need this whole subsystem when I could just use HTTP or WebSockets?

The real power with data channels is that you can configure them to behave like UDP with unordered/lossy delivery.
This is necessary for low latency and high performance situations. You can measure the back pressure and ensure you
are only sending as much as your network supports.

## How does it work
WebRTC uses SCTP, defined in [RFC 2960](https://tools.ietf.org/html/rfc2960). SCTP (Stream Control Transmission Protocol) is a
transport layer protocol and was intended as an alternative to TCP or UDP. For WebRTC we use it as an application layer protocol
which runs over our DTLS connection.

SCTP gives you streams and each stream can be configured. WebRTC data channels are just a thin abstraction around them. The settings
around durability/ordering are just passed right into the SCTP Agent.

Data channels have some features that SCTP can't express like channel labels. To solve that WebRTC uses the DCEP (Data Channel Establishment Protocol)
which is defined in [RFC 8832](https://tools.ietf.org/html/rfc8832). DCEP defines a messages to communicate the channel label and protocol

## DCEP
DCEP only has two messages `DATA_CHANNEL_OPEN` and `DATA_CHANNEL_ACK`. For each data channel that is opened the remote must respond with an ack.

### DATA_CHANNEL_OPEN
This message is sent by the WebRTC Agent that wishes to open a channel

#### Packet Format
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

#### Message Type
Message Type is a static value of `0x03`

#### Channel Type
Channel Type controls durability/ordering attributes of the channel. It may have the following values.

* **DATA_CHANNEL_RELIABLE (0x00)** - No messages are lost and will arrive in order
* **DATA_CHANNEL_RELIABLE_UNORDERED (0x80)** - No messages are lost and may arrive out of order
* **DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT (0x01)** - Messages may be lost after trying the requested amount of times and will arrive in order
* **DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED (0x81)** - Messages may be lost after trying the requested amount of times and may arrive out of order
* **DATA_CHANNEL_PARTIAL_RELIABLE_TIMED (0x02)** - Messages may be lost if they don't arrive in the requested amount of time and will arrive in order
* **DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED (0x82)** - Messages may be lost if they don't arrive in the requested amount of time and may arrive out of order

#### Priority
The priority of the data channel. Data channels having a higher priority will be scheduled first. Large lower-priority user
messages will not delay the sending of higher-priority user messages.

#### Reliability Parameter
If a data channel is `DATA_CHANNEL_PARTIAL_RELIABLE` this configures the behavior.

If it is a `REXMIT` this parameter controls how many times the sender will re-send the message before giving up.

If it is a `TIMED` this parameter controls how long the sender will re-send the message before giving up.

#### Label
The name of the data channel as a UTF-8-encoded string.  This may be an empty string.

#### Protocol
If this is an empty string, the protocol is unspecified.  If it is
a non-empty string, it specifies a protocol registered in the
"WebSocket Subprotocol Name Registry"

### DATA_CHANNEL_ACK
This message is sent by the WebRTC Agent to acknowledge that this data channel has been opened.

#### Packet Format
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
```

## SCTP
SCTP is the real power behind WebRTC data channels. It provides all these features of the data channel.

* Multiplexing
* Reliable delivery using a TCP-like retransmission mechanism
* Partial-reliability options
* Congestion Avoidance
* Flow Control

To understand SCTP we explore it in 3 parts. The goal is to have info to debug and learn the
deep details of SCTP on your own after this chapter.

## Concepts
SCTP is a feature rich protocol. This section is only going to cover the parts of SCTP that are used by WebRTC.
SCTP has some things that aren't used by WebRTC like multi-homing and path selection.

With over twenty years of development SCTP can be hard to fully grasp.

### Association
Association is the term used of a SCTP Session. It is the state that is shared
between two SCTP Agents while they communicate.

### Streams
A stream is one bi-directional sequence of user data. When you create a data channel you are actually just creating a
SCTP stream.  Each SCTP Association contains a list of streams.  Each stream can be configured with differently reliability types.

WebRTC only allows you to configure on stream creation, but SCTP actually allows configuration at anytime.

### Datagram Based
SCTP frames data as datagrams and not as a byte stream. Sending and receiving data feels like UDP instead of TCP. So you don't need
to add extra code to transfer multiple files over one stream.

SCTP messages don't have size limits like UDP. A single SCTP message can be multiple gigabytes in size.

### Chunks
The SCTP protocol is made up of chunks. There are many different types of chunks. These chunks are used for all communication.
User data, connection initialized, congestion control and more is all done via chunks.

Each SCTP packet contains a list of chunks. So in one UDP packet you can have multiple chunks carrying messages from different streams.

### Transmission sequence number
The TSN (Transmission sequence number) is a global unique identifier for DATA chunks. A DATA chunk is what carries all the messages
a user wishes to send. The TNS is important because it helps a receiver determine if packets are lost or out of order.

If the receiver sees it is missing a TSN it doesn't give the data to the user until it is fulfilled.

### Stream identifier
Each stream has a unique identifier. When you create a data channel with an explicit ID it actually is just passed right into SCTP
as the stream identifier. If you don't pass an id the stream identifier is chosen for you.

### Payload protocol identifier
Each DATA chunk also a PPID (Payload protocol identifier). This is used to uniquely identify what type of Data is being exchanged.
SCTP has many PPIDs, but WebRTC only uses the following 5.

* **WebRTC DCEP (50)** - DCEP messages
* **WebRTC String (51)** - Datachannel string messages
* **WebRTC Binary (53)** - Datachannel binary messages
* **WebRTC String Empty (56)** - Datachannel string messages with 0 length
* **WebRTC Binary Empty (57)** - Datachannel binary messages with 0 length

## Protocol
### Abort Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 6    |Reserved     |T|           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\               Zero or more Error Causes                       \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

An ABORT chunk abruptly shuts down the the assocation. Used when
one side enters an error state. Gracefully ending the connection uses
the SHUTDOWN chunk.

### Cookie Echo Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 10   |Chunk  Flags   |         Length                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                     Cookie                                    /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Data Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 0    | Reserved|U|B|E|    Length                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              TSN                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Stream Identifier S      |   Stream Sequence Number n    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Payload Protocol Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                 User Data (seq n of Stream S)                 /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Error Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 9    | Chunk  Flags  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                    one or more Error Causes                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Forward TSN Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 192  |  Flags = 0x00 |        Length = Variable      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      New Cumulative TSN                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-1              |       Stream Sequence-1       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               /
/                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-N              |       Stream Sequence-N       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Heartbeat Request Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 4    | Chunk  Flags  |      Heartbeat Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/            Heartbeat Information TLV (Variable-Length)        /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Init Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 1    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Initiate Tag                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Advertised Receiver Window Credit (a_rwnd)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Number of Outbound Streams   |  Number of Inbound Streams    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Initial TSN                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/              Optional/Variable-Length Parameters              /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Selective Acknowledgment Chunk

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 3    |Chunk  Flags   |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Advertised Receiver Window Credit (a_rwnd)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Number of Gap Ack Blocks = N  |  Number of Duplicate TSNs = X |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Gap Ack Block #1 Start       |   Gap Ack Block #1 End        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Gap Ack Block #N Start      |  Gap Ack Block #N End         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN 1                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN X                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Shutdown Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 7    | Chunk  Flags  |      Length = 8               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Reconfig Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Type = 130    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                  Re-configuration Parameter                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/             Re-configuration Parameter (optional)             /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## State Machine
### Connection establishment flow
### Connection teardown flow
### Keep-alive mechanism
### How does a user message get sent?
### TSN and retransmission
### Congestion avoidance
### Selective ACK
### Fast retransmission/recovery
### Partial Reliability
