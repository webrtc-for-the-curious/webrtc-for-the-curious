---
title: 信令
type: docs
weight: 3
---

# 信令

## 什么是 WebRTC 信令？

当一个 WebRTC Agent 被创建时，它对其他 peer 一无所知。它不知道它将与谁联系，也不知道它们将发送些什么！
信令是使呼叫成为可能的初始引导程序。交换信令消息后，WebRTC Agent 才可以直接相互通信。

信令消息只是文本。WebRTC Agent 并不关心它们的传递方式。信令通常使用 Websockets 分享，但这不是必需的。

## WebRTC 信令如何工作？

WebRTC 使用到一种现有的协议，称为会话描述协议（Session Description Protocol，简称 SDP）。两个 WebRTC Agent 会将建立连接所需的所有状态通过此协议来分享。该协议本身亦易于阅读和理解。
但要理解 WebRTC 填充于协议中的所有值，是有些复杂的。

SDP 并不是 WebRTC 特有的。我们将首先学习会话描述协议，这里甚至不用提到 WebRTC。WebRTC 实际上仅是利用了 SDP 协议的子集，因此我们将仅介绍我们所需的内容。
理解协议后，我们将继续结合 WebRTC 来说明其在实际中的应用方法。

## 什么是 *会话描述协议*（SDP）？

会话描述协议定义于 [RFC 8866](https://tools.ietf.org/html/rfc8866) 中。它是一个 key/value 协议，每一行是一个值。看起来类似于 INI 文件。
一个会话描述包含零个或多个媒体描述。对此模型，可以理解为会话描述包含了一个媒体描述的数组。

一个媒体描述通常映射到单个媒体流。因此，如果你想描述一个包含三个视频流和两个音轨的呼叫，需要五个媒体描述。

### 如何阅读 SDP 信息

会话描述中的每一行都将以一个单字符开始，这是你的 key。单字符后面将跟随一个等号。等号后的所有内容都是 value。value 结束的地方将有一个换行符。

会话描述协议定义了所有有效的 key。对于协议中定义的 key，你只能使用字母。这些 key 都有重要的意义，稍后将对此进行解释。

作为参考，下面是一个会话描述的部分内容：

```
a=my-sdp-value
a=second-value
```

这里有两行。每行的 key 都是 `a`。第一行的 value 为 `my-sdp-value`，第二行的 value 为 `second-value`。

### WebRTC 仅使用了部分 SDP 的 key

WebRTC 并未使用会话描述协议定义的所有 key，只有那些在 JavaScript Session Establishment Protocol (JSEP，协议定义在[RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829)) 中被使用到的 key 是重要的。你当前只需要理解下面的 7 个 key。

* `v` - Version，版本，版本，应等于 `0`。
* `o` - Origin，源，包含一个唯一 ID，用于重新协商。
* `s` - Session Name，会话名称，应等于`-`。
* `t` - Timing，时间，应等于 `0 0`。
* `m` - Media Description(`m=<media> <port> <proto> <fmt> ...`)，媒体描述，下面有详细说明。
* `a` - Attribute，属性，一个自由文本字段，这是 WebRTC 中最常见的行。
* `c` - Connection Data，连接数据，应等于 `IN IP4 0.0.0.0`。

### 会话描述中的媒体描述

一个会话描述中，可以包含无限数量的媒体描述。

一个媒体描述定义中，包含一个格式列表。这些格式映射到 RTP 有效负载类型。然后，实际的编解码器由媒体描述中的 `rtpmap` 属性定义。
RTP 和 RTP 有效负载类型的重要性将在后面的媒体章节中讨论。每个媒体描述可以包含无限数量的属性。

作为参考例子，下面是一个会话描述的部分内容：

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

这里面有两个媒体描述，第一个是音频，格式为 `111`，另一个是视频，格式为 `96`。第一个媒体描述只有一个属性。该属性将有效载荷类型 `111` 映射到 Opus 编解码器。
第二个媒体描述具有两个属性。第一个属性将有效负载类型 `96` 映射到 VP8 编解码器，第二个属性只是 `my-sdp-value`。

{{< hint info >}}
译注：参照前面 key 的定义，第 1 行的 v=0 表示版本为 0，第 2/3 行是第一个媒体描述，第 4/5/6 行是第二个媒体描述
{{< /hint >}}

### 完整示例

以下内容将我们讨论过的所有概念整合在一起。这些是 WebRTC 所使用的会话描述协议的所有特性。
如果你可以读懂这个例子，那么你可以读懂任何 WebRTC 会话描述！

```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 127.0.0.1
t=0 0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4002 RTP/AVP 96
a=rtpmap:96 VP8/90000
```

* `v`, `o`, `s`, `c`, `t` 虽然被定义，但他们不对 WebRTC 会话产生影响。
* 这里有两个媒体描述。一个是 `audio` 即音频类型，一个是 `video` 即视频类型。
* 每个媒体描述都有一个属性。这个属性配置了 RTP 管道的详细信息，这部分将在 " 媒体通信 " 章节详细讨论

## *会话描述协议* 和 WebRTC 如何协同工作

下一块拼图是理解 WebRTC _ 如何 _ 使用会话描述协议。

### 什么是 Offer 和 Answer？

WebRTC 使用 Offer/Answer 模型。这指的是，一个 WebRTC Agent 发出 "Offer" 以开始呼叫，如果另一个 WebRTC Agent 愿意接受 "Offer" 的内容，它会响应 "Answer"。

这使得应答者有机会拒绝媒体描述中的某些不支持的编解码器，也是两个 peer 互相理解他们希望交换何种格式的方式。

### 用于发送和接收的收发器（Transceivers）

收发器是 WebRTC 中特有的概念，你将在看到它。它的作用是将 " 媒体描述 " 暴露给 JavaScript API。每个媒体描述都将成为一个收发器。每次创建收发器时，都会将新的媒体描述添加到本地会话描述中。

WebRTC 中的每个媒体描述都包含一个 direction 属性。这样，WebRTC Agent 可以声明 " 我将向你发送此编解码器，但我不打算接受任何返回的内容 "。direction 属性有四个有效值：

* `send`
* `recv`
* `sendrecv`
* `inactive`

### WebRTC 用到的 SDP 值

这个列表包含了你将在 WebRTC Agent 的会话描述中看到的一些常见属性。这些值控制着我们尚未讨论到的子系统。

#### `group:BUNDLE`

BUNDLE 是一种在单个连接上传输多种类型流量的行为。一些 WebRTC 实现对每个媒体流会使用专用的连接。但 BUNDLE 方式应该是首选。

#### `fingerprint:sha-256`

该属性是 peer 用于 DTLS 证书的哈希值。DTLS 握手完成后，你可以将其与实际证书进行比较，以确认你正在与预期的对象进行通信。

{{< hint info >}}
译注：下面是[RFC 4572](https://tools.ietf.org/html/rfc4572)中的一个例子
```
a=fingerprint:SHA-1 \
          4A:AD:B9:B1:3F:82:18:3B:54:02:12:DF:3E:5D:49:6B:19:E5:7C:AB
```
{{< /hint >}}

#### `setup:`

该属性控制了 DTLS Agent 的行为。在 ICE 连接后，该属性将确定 DTLS Agent 是作为客户端还是服务器来运行。有以下几个可能的值：

* `setup:active` - 作为 DTLS 客户端运行。
* `setup:passive` - 作为 DTLS 服务器运行。
* `setup:actpass` - 要求另一个 WebRTC Agent 选择。

#### `mid`

该属性是每个 Media Description 的唯一 ID。用于标识媒体。

#### `ice-ufrag`

该属性是 ICE Agent 的用户片段值。用于 ICE 流量的身份验证。

#### `ice-pwd`

该属性是 ICE Agent 的密码。用于 ICE 流量的身份验证。

#### `rtpmap`

该属性用于将特定的编解码器映射到 RTP 有效负载类型。有效负载类型不是静态的，因此对于每次呼叫，发起者都需要确定每个编解码器的有效负载类型。

#### `fmtp`

该属性为一种有效负载类型定义附加的值。要传递特定的视频配置文件或编码器设置时，这很有用。

#### `candidate`

该属性是来自 ICE Agent 的 ICE 候选地址。这是一个可能被 WebRTC Agent 使用的地址。这些将在下一章中详细说明。

#### `ssrc`

一个同步源（SSRC）定义了一个单独的媒体流。

`label` 是此媒体流的 ID。`mslabel` 是容器的 ID，该容器中可以有多个流。

### WebRTC 会话描述示例

下面是一个 WebRTC 客户端生成的一套完整会话描述：

```
v=0
o=- 3546004397921447048 1596742744 IN IP4 0.0.0.0
s=-
t=0 0
a=fingerprint:sha-256 0F:74:31:25:CB:A2:13:EC:28:6F:6D:2C:61:FF:5D:C2:BC:B9:DB:3D:98:14:8D:1A:BB:EA:33:0C:A4:60:A8:8E
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=setup:active
a=mid:0
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ssrc:350842737 cname:yvKPspsHcYcwGFTw
a=ssrc:350842737 msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=ssrc:350842737 mslabel:yvKPspsHcYcwGFTw
a=ssrc:350842737 label:DfQnKjQQuwceLFdV
a=msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=setup:active
a=mid:1
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=ssrc:2180035812 cname:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=ssrc:2180035812 mslabel:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 label:JgtwEhBWNEiOnhuW
a=msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=sendrecv
```

从这个会话描述中，我们可以知道以下内容：

* 我们有两个媒体描述，一个是音频，一个是视频
* 这两个媒体描述都是 `sendrecv` 收发器。我们将得到两个流，也可以发送两个流回去。
* 我们有 ICE 候选地址和身份验证的详细信息，因此我们可以尝试连接
* 我们有一个证书指纹，因此我们可以进行安全的呼叫

{{< hint info >}}
译注：对照以上 4 点
* 两个媒体描述即是两个 `m=` 段
* 两个 m 段中都有 `a=sendrecv`，即是说可以收也可以发
* ICE 候选地址对应 `a=candidate:foundation` 到 `a=end-of-candidates` 之间的部分，身份验证信息参考前面的 `ice-ufrag` 和 `ice-pwd` 等
* 指的是 `fingerprint:sha-256` 属性
{{< /hint >}}

### 进一步的话题

在本书的后续版本中，还将讨论以下主题：

* 重新协商（Renegotiation）
* 同步广播（Simulcast）
