---
title: 数据通信
type: docs
weight: 7
---

# 什么是数据


## 功能概述
数据通道可以传送任何类型的数据。您也可以通过数据通道发送音频或视频数据，但是如果需要实时播放媒体（请参阅[媒体通信]({{< ref "05-media-communication.md" >}})），使用基于RTP/RTCP协议的媒体通道是更好的选择。

### 数据通道有哪些应用？

数据通道的适用性是无限的！数据通道为您解决了数据包丢失，拥塞问题和许多其他问题，并为您提供了非常简单的API，让您将数据实时交付给对端peer。您只需要关注应用程序想要实现的目标并发挥创造力即可。

以下是一些使用数据通道的示例应用：
  - 实时网络游戏
  - 远程无服务器家庭自动化
  - 文字聊天
  - 动画（一系列静止图像）
  - P2P CDN（内容交付网络）
  - 监控物联网数据
  - 从传感器设备持续提取时间序列数据
  - 从相机获取实时图像并利用AI进行图像识别

### 协议栈概述
数据通道由以下3层组成：
* 数据通道层
* DCEP（数据通道建立协议）层
* SCTP（流控制传输协议）层

{{< figure src="/images/06-datachan-proto-stack.png">}}

#### 数据通道层
该层提供了API。该API大体上是对WebSocket的模拟，从而使Web开发人员能相对容易的将现有的基于Websocket的客户端-服务器的代码修改为使用P2P数据通道实现。单个peerconnection可以包含peer之间的多条数据通道，从而省去了从多个数据源和接收器复用和解复用的麻烦。只需要为交换的每一类数据创建一个数据通道，其余的工作都交给peerconnection完成。与websockets不同的一点是，数据通道具有创建者分配的标签，接收者可以使用标签来确定数据通道的身份。

#### 数据通道建立协议层
该层负责与对端peer建立数据通道握手。它使用SCTP流作为控制通道来协商诸如有序交付，maxRetransmits（最大重传）/ maxPacketLifeTime（最大包生命周期）（也就是"部分可靠性"选项），发送频道的标签等等。

#### SCTP协议层
这是数据通道的核心。它包括：

* 通道复用（在SCTP中，通道称为"流"）
* 通过类似TCP的重传机制进行可靠传递
* 部分可靠性选项
* 避免拥塞
* 流量控制

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

### DCEP（Data Channel Establishment Protocol/数据通道建立协议）
DCEP是一个简单到只有两个数据包的协议，它描述了建立数据通道的行为。它不需要等待握手完成，因此该通道的后续数据可以包含在同一数据包中。这使得建立数据通道更加快速，而且成本更低。

#### Open/ACK handshake（握手）
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
这里是通道类型的列表以及相关的可靠性参数的含义，这些可靠性参数将在数据包丢失或乱序时被使用。
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
数据通道的可靠性大体上等同于TCP。

需要特别提一下Reliable_Unordered。这种模式意味着，如果一个数据包因为网络原因丢失时，只有包含这个数据包的消息会被延后，直到重新发送为止。在这个消息之后发送的其他消息可能会更早到达。当接收消息的顺序不如消息到达的速度重要时，就可以使用这种模式。在这种模式下，仍然强制执行消息传递，但传递顺序不是强制的。可以将这种模式视为TCP和UDP之间的折衷方案。

其他的模式等价于基于UDP，但具有不同的重试/失败规则的协议。

```
DATA_CHANNEL_ACK
Message Type: 0x02

      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |  Message Type |
     +-+-+-+-+-+-+-+-+

```
没有DCEP NACK（译注：即数据通道建立失败）。
数据通道的打开始终会成功，因为它们的传输是在已经成功建立的SCTP流上进行！

#### PPID（Payload Protocol Identifier/有效载荷协议标识符）
WebRTC DCEP的SCTP PPID为50。DCEP消息与SCTP流中的其余数据分开处理，并且不会传递回Web应用程序或服务。

#### 参数交换
理论上讲，可以使用out-of-band的SDP中非DCEP协商的方式来创建数据通道。不要这样。

## RFC链接
https://datatracker.ietf.org/doc/rfc8832/?include_text=1
