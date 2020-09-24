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
该层提供了API。

#### 数据通道建立协议层
该层负责与对端peer建立数据通道握手。它使用SCTP流作为控制通道来协商诸如有序交付，maxRetransmits（最大重传）/ maxPacketLifeTime（最大包生命周期）（也就是"部分可靠性"选项）之类的功能。

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

### DCEP
#### Open/ACK handshake
#### PPID
#### Parameter exchange

## Reference to RFCs

