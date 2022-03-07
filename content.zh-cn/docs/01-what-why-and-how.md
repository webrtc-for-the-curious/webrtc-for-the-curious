---
title: 是什么，为什么，如何使用
type: docs
weight: 2
---

# 是什么，为什么，如何使用

## WebRTC是什么？

WebRTC是Web实时通信（Real-Time Communication）的缩写，它既是API也是协议。WebRTC协议是两个WebRTC Agent协商双向安全实时通信的一组规则。开发人员可以通过WebRTC API使用WebRTC协议。目前WebRTC API仅有JavaScript版本。

可以用HTTP和Fetch API之间的关系作为类比。WebRTC协议就是HTTP，而WebRTC API就是Fetch API。

除了JavaScript语言，WebRTC协议也可以在其他API和语言中使用。你还可以找到WebRTC的服务器和特定领域的工具。所有这些实现都使用WebRTC协议，以便它们可以彼此交互。

WebRTC协议由IETF工作组在[rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/)中维护。WebRTC API的W3C文档在[webrtc](https://www.w3.org/TR/webrtc/)。

## 为什么我应该学习WebRTC？

下面这些是WebRTC可以带给你的东西。这并不是一份详尽的清单，只是列举一些你在学习中可能感兴趣的点。如果你还不了解所有这些术语，请不要担心，本书将陆续将这些概念教给你。

* 开放标准
* 多种实现
* 在浏览器中可用
* 强制加密
* NAT穿透
* 复用现有技术
* 拥塞控制
* 亚秒级延迟

## WebRTC协议是一组其他技术的集合体

这个主题需要整本书来解释。但是，首先，我们将其分为四个步骤。

* 信令（Signaling）
* 连接（Connecting）
* 安全加密（Securing）
* 通信（Communicating）

这四个步骤依次发生。上一个步骤必须100％成功，随后的步骤才能开始。

关于WebRTC的一个特殊事实是，每个步骤实际上都是由许多其他协议组成的！为了让WebRTC工作起来，我们将许多现有技术结合在一起。从这个意义上讲，WebRTC更像是2000年代早期以来就已经存在的一些易于理解的技术的组合和配置。

每个步骤都有专门的章节，但是首先从较高的层次上理解它们会有所帮助。由于它们彼此依赖，因此理解这些在进一步解释每个步骤的目的时会有所帮助。

### 信令：peer如何在WebRTC中找到彼此

当WebRTC Agent启动时，它不知道与谁通信以及他们将要通信的内容。信令解决了这个问题！信令用于引导呼叫，以便两个WebRTC Agent可以开始通信。

信令使用现有的协议SDP（会话描述协议）。SDP是一种纯文本协议。每个SDP消息均由键/值对组成，并包含“media sections（媒体部分）”列表。两个WebRTC Agent交换的SDP所包含一些详细信息，如：

* Agent可供外部访问的（候选的）IP和端口。
* Agent希望发送多少路音频和视频流。
* Agent支持哪些音频和视频编解码器。
* 连接时需要用到的值（`uFrag`/`uPwd`）。
* 加密传输时需要用到的值（证书指纹）。

注意，信令通常发生在“out-of-band”。也就是说，应用通常不使用WebRTC本身来交换信令消息。在连接的peer中，任何适合发送消息的架构均可被用于传递SDP信息，许多应用程序都使用其现有的基础设施（例如REST端点，WebSocket连接或身份验证代理）来解决适当客户端之间的SDP传递问题。

### 使用STUN/TURN进行连接和NAT穿透

现在，两个WebRTC Agent知道足够的详细信息以尝试相互连接。接下来，WebRTC将使用另一种成熟的技术，称为ICE。

ICE（交互式连接建立）是WebRTC之前的协议。ICE允许在两个Agent之间建立连接。这些Agent可以在同一网络上，也可以在世界的另一端。ICE是无需中央服务器即可建立直接连接的解决方案。

这里真正的魔法是“ NAT穿透”和STUN/TURN服务器。这两个概念是与另一个子网中的ICE Agent进行通信所需的全部。稍后我们将深入探讨这些主题。

ICE成功连接后，WebRTC继续建立加密的传输。此传输用于音频，视频和数据。

### 使用DTLS和SRTP加密传输层

现在我们有了双向通信（通过ICE），我们需要建立安全的通信。这是通过WebRTC之前的两种协议完成的。第一个协议是DTLS（数据报传输层安全性），它只是基于UDP的TLS。TLS是用于保护通过HTTPS进行通信的加密协议。第二种协议是SRTP（安全实时传输协议）。

首先，WebRTC通过在ICE建立的连接上进行DTLS握手来进行连接。与HTTPS不同，WebRTC不使用中央授权来颁发证书。相反，WebRTC只是判断通过DTLS交换的证书是否与通过信令共享的签名相符。然后，此DTLS连接可以被用于传输DataChannel消息。

接下来，WebRTC使用RTP协议进行音频/视频的传输。我们使用SRTP来保护我们的RTP数据包。我们从协商的DTLS会话中提取密钥，用来初始化SRTP会话。在后续章节中，我们会讨论为什么媒体传输需要有它自己的协议。

现在我们完成了！你现在可以进行安全的双向通信。如果你的WebRTC Agent之间具有稳定的连接，上面这就是你可能需要解决的所有复杂问题。不幸的是，现实世界中存在数据包丢失和带宽限制等问题，在后续章节中，我们会介绍如何处理这些问题。

### 通过RTP和SCTP进行点对点通信

现在，我们有了两个具有安全的双向通信功能的WebRTC Agent。让我们开始通信！跟前面一样，我们使用两个预先存在的协议：RTP（实时传输协议）和SCTP（流控制传输协议）。我们使用RTP来交换用SRTP加密过的媒体数据，使用SCTP发送和接收那些用DTLS加密过的DataChannel消息。

RTP很小，但是提供了实现实时流式传输所需的功能。重要的是，RTP为开发人员提供了灵活性，因此他们可以根据需要处理延迟，丢失和拥塞。我们将在媒体章节中对此进行进一步讨论。

协议栈中的最后一个协议是SCTP。SCTP支持许多不同的消息传送选项。你可以选择不可靠的无序交付，以便获得实时系统所需的低延迟。

## WebRTC是一系列协议的集合

WebRTC解决了许多问题。初看起来，这似乎是过度设计的。实际上，WebRTC非常克制。它并未认为它可以更好的解决所有问题。相反，它采纳了许多现有的解决特定领域问题的技术，然后将它们有机地结合起来。

这使得我们可以独立的检查和学习每个部分，而不会毫无头绪。实际上，从另一个角度去看“ WebRTC Agent”，它只是许多不同协议的协调器。

![WebRTC Agent](../../images/01-webrtc-agent.png "WebRTC Agent图示")

## WebRTC（API）如何工作

本部分显示JavaScript API是如何跟协议相对应的。这不是WebRTC API的详细演示，而更像是创建了一个思维模型，将各个模块串联起来。如果你对各个模块都不熟悉，那也不要紧。当你了解更多信息时，再回头看看这一部分，可能会很有趣！

### `new RTCPeerConnection`

`RTCPeerConnection`是最顶层的"WebRTC会话"。它包含上述所有协议。调用后，所有子系统都会被创建，但是此时什么都还没有发生。

### `addTrack`

`addTrack`创建一个新的RTP流。并将为这个流生成一个随机的SSRC（Synchronization Source/同步源）。然后，`createOffer`将生成会话描述，这个RTP流会被放入一个media section。每次调用`addTrack`都会创建一个新的SSRC和一个对应的media section。

在建立SRTP会话后，这些媒体数据包将被SRTP加密，然后立即通过ICE开始发送。

### `createDataChannel`

如果没有SCTP关联存在，`createDataChannel`将创建一个新的SCTP流。默认情况下，SCTP是不启用的，只有在一方请求数据通道时才启动。

在DTLS会话建立之后，SCTP关联将立即通过ICE发送数据包，并使用DTLS加密。

### `createOffer`

`createOffer`生成本地状态的会话描述，以与远端Peer共享。

调用`createOffer`的行为对于本地Peer没有任何改变。

### `setLocalDescription`

`setLocalDescription`提交所有请求的更改。 在此调用之前，`addTrack`，`createDataChannel`和其他类似的调用都是临时的(未生效的)。 调用`setLocalDescription`时，使用由`createOffer`生成的值。

通常，在此调用之后，你会将offer发送给远端Peer，他们将调用`setRemoteDescription`，将此offer设入。

### `setRemoteDescription`

收到远端Peer发来的offer之后，我们通过`setRemoteDescription`通知本地Agent。这就是使用JavaScript API传递“信令”的方式。

双方都调用过`setRemoteDescription`后，WebRTC Agent现在拥有足够的信息来开始进行点对点（P2P）通信！

### `addIceCandidate`

`addIceCandidate`允许WebRTC Agent随时添加更多的远程ICE候选对象。该API将ICE候选对象发送到ICE子系统，并且对更大的WebRTC连接没有其他影响。

### `ontrack`

`ontrack`是收到远端Peer的RTP数据包时触发的回调。传入的RTP数据包的格式应该已在传递给`setRemoteDescription`的会话描述中声明。

WebRTC使用SSRC并查找关联的`MediaStream`和`MediaStreamTrack`，并使用`MediaStream`和`MediaStreamTrack`中的详细信息来触发此回调。

### `oniceconnectionstatechange`

`oniceconnectionstatechange`是ICE Agent的状态变化时触发的回调。当网络连接或断开时，你将得到此通知。

### `onconnectionstatechange`

`onconnectionstatechange`是ICE Agent和DTLS Agent状态的组合。当ICE和DTLS都成功完成时，你将得到此通知。
