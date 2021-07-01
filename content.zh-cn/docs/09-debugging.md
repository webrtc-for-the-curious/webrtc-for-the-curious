---
title: 调试
type: docs
weight: 10
---

# 调试
调试WebRTC可能是一项艰巨的任务。有很多部分都处于运行状态，每一个部分都可能出现问题。如果您不够细心，可能会浪费数周的时间来查看错误的模块。当您最终找到出错的部分时，您还需要学习一些知识才能理解问题的根源。

本章将带您学习WebRTC的调试。它将向您展示如何分析并定位相关问题。确定问题后，我们将快速介绍一下流行的调试工具。

### 分解问题
开始调试时，您需要先分解问题的源头。从以下题目开始：

#### 信令故障
#### 网络故障

使用netcat测试您的STUN服务器：

1. 准备**20字节**的绑定请求数据包：

    ```
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    ```

    解释：

    - `00 01` 是消息类型

    - `00 00` 是数据段的长度

    - `21 12 a4 42` 是magic cookie

    - `54 45 53 54 54 45 53 54 54 45 53 54` （解码成ASCII就是`TESTTESTTEST`） 是12字节的transaction ID

2. 发送请求并等待**32字节**的响应：

    ```
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    ```

    解释：

    - `01 01` 是消息类型

    - `00 0c` 是数据段的长度，解码后是十进制的12

    - `21 12 a4 42` 是magic cookie

    - `54 45 53 54 54 45 53 54 54 45 53 54` （解码成ASCII就是`TESTTESTTEST`）是12字节的transaction ID

    - `00 20 00 08 00 01 6f 32 7f 36 de 89` 是12字节的数据，解释：

        - `00 20` 是类型：`XOR-MAPPED-ADDRESS`

        - `00 08` 是value段的长度，以十进制解码就是8

        - `00 01 6f 32 7f 36 de 89` 是数据值，解释：

            - `00 01` 是地址类型（IPv4）

            - `6f 32` 是经过XOR映射的端口

            - `7f 36 de 89` 是经过XOR映射的IP地址

解码XOR映射的部分很麻烦，但是我们可以通过提供设置为`00 00 00 00`的（无效）伪magic cookie来诱骗stun服务器执行伪XOR映射：

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

对伪magic cookie的XOR运算是幂等的，因此响应中的端口和地址将是清楚的（这并非在所有情况下都有效，因为某些路由器会操纵传递的数据包，伪装IP地址）； 如果我们查看返回的数据值（最后八个字节）：

  - `00 01 4e 20 5e 24 7a cb` 是数据值，解释：

    - `00 01` 是地址类型（IPv4）

    - `4e 20` 是映射的端口，解码成十进制就是20000

    - `5e 24 7a cb` 是IP地址，解码成点分十进制表示法就是`94.36.122.203`

#### 安全故障
#### 媒体故障
#### 数据故障

### 用到的工具

#### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) 是用于使用TCP或UDP读取和写入网络连接的命令行网络实用程序。通常它可以用`nc`命令来调用。

#### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump)是一个命令行数据网络数据包分析器。

常用命令：

- 捕获与端口19302之间的UDP数据包，并打印数据包内容的十六进制转储：

    `sudo tcpdump 'udp port 19302' -xx`

- 与上一条相同，但将数据包保存在PCAP（数据包捕获）文件中以供以后检查

    `sudo tcpdump 'udp port 19302' -w stun.pcap`

  可以使用wireshark GUI打开PCAP文件：`wireshark stun.pcap`

#### wireshark
#### webrtc-internals

Chrome 内置了一个 WebRtc 指标数据页面 [chrome://webrtc-internals](chrome://webrtc-internals) 。

## 延迟(Latency)

我们该如何感知高延迟？你会注意到视频出现延迟了，但你知道它具体延迟了多少吗？

想要降低延迟，你首先必须知道如何测量延迟。

真正的延迟应该是端到端测量的。这不仅仅是指发送方和接收方之间网络路径的延迟，还包括相机拍摄、帧编码、传输、接收、解码和视频播放等一系列步骤延迟的综合，以及这些步骤之间可能存在的队列。
端到端延迟不是各个组件延迟的简单叠加。

虽然在理论上，你可以单独测量整个视频传输管线中各个模块的延迟，然后累加到一起；但是在实践中，至少有些组件没有方法去测量延迟，或者在外部测量延迟的结果存在明显的偏差。

各个步骤之间的队列大小，网络拓扑，甚至是相机的曝光变化，都可能会对分步骤的测量结果产生影响，进而影响 端到端延迟。

直播系统中每个组件内部的延迟都会改变并影响下游组件。甚至拍摄的内容也会影响延迟。例如，与晴朗的蓝天这种低频图像相比，树枝等高频特征需要更多的比特数。(*译者注：编码的本质是压缩，压缩的本质是减少数据冗余，复杂的图像编码后需要更多的空间*)
开启自动曝光的相机拍摄一帧图像可能比预期的需要花更多的时间，即使你设置了固定的拍摄速率。
网络传输的效率也是动态变化的，尤其是蜂窝网络，受网络上的传输需求的明显影响。
用户越多，网络负载就越大。
地理位置（特别是某些臭名昭著的低信号区）等其他因素也会增加丢包和延迟。当你把数据包发送到网络接口，比如请求 WIFT适配器或者LTE 进行分发，当网络接口有队列时，你的数据包将不会被立即发送，队列越大，网络接口引入的延迟就越大。

### 端到端延迟——手动测量

当我们谈论 端到端延迟时，指的是从 事件发生 到 事件被看到(即视频帧播放在屏幕上) 的时间间隔。

```
EndToEndLatency = T(observe) - T(happen)
```

一个想当然的方法是，记录事件发生的时间，再与事件被看到的时间相减即可得到。
但是，当精确度为毫秒级时，时间同步就成了难题。
想要在分布式系统中同步时钟基本是徒劳的，即使是时钟同步的一个小错误，也会让 延迟测量 不再可信。

绕开时间同步的一种简单方式，就是使用相同的时钟。
将 sender 和 receiver 放在 同一个参考系。

想象一下你有一个 正常运行的毫秒时钟 （或者其他真实的可以表示时间的物体）。
你要测量一个系统的延迟，这个系统中，摄像头对准 时钟，采集的直播流显示到同一个地方的另一个屏幕上。
有一个直接的测量方式来 测量  时钟当前时间 (T<sub>`happen`</sub>) 和这个时钟视频出现在屏幕上的时间 (T<sub>`observe`</sub>) 。步骤如下：

- 将你的摄像头对准这个时钟
- 将视频帧发送给同一个地方的接收端，接收端在屏幕上进行播放
- 拍一张照片（用你的手机），将时钟和屏幕视频画面 拍进同一个画面内
- 将照片中的两个时间相减（时钟上的时间，和 屏幕视频画面里 时钟的时间）

这是最真实的端到端延迟测量。
它考虑了所有组件的延迟（相机、编码器、网络、解码器）并且不依赖任何时钟同步。

![DIY Latency](../images/09-diy-latency.png "DIY Latency Measurement").
![DIY Latency Example](../images/09-diy-latency-happen-observe.png "DIY Latency Measurement Example")
在上面的照片中，测得的端到端延迟为 101 msec。事件发生的时间是 10:16:02.862 , 而 直播观看者看到的时间是 10:16:02.761。

### 端到端延迟——自动测量

本文写作时(2021年5月)，WebRtc 标准 关于 端到端延迟的话题正在被积极 [讨论](https://github.com/w3c/webrtc-stats/issues/537)。
Firefox 实现了 一套 APIs ，来允许用户在标准WebRTCAPIs之上，创建对延迟的自动测量。
不过在本章节，我们将讨论端到端延迟自动测量的最通用的方法。

![NTP Style Latency Measurement](../images/09-ntp-latency.png "NTP Style Latency Measurement")

Roundtrip ，即往返时间，简而言之就是： 我向你发送我的时间 `tR1`, 当我接收到 `tR1` 回来时，时间是 `tR2` ，可得 round trip time 是 `tR2 - tR1` 。

这里假设在发送者和 接收者 之间有一个 通信channel（比如， [DataChannel](https://webrtc.org/getting-started/data-channels) ，接收者 可以 通过 以下步骤来模拟 发送者 的单调时钟： 

1. 在时间`tR1` ，Receiver 发送一个消息，携带它的本地时钟时间戳 `tR1`。
2. 在 Sender 端的时间 `tS1` ，Sender 收到该消息，Sender 进行消息响应，消息中携带三个时间： `tR1` 和 `tS1`，以及 Sender的 视频轨道时间 `tSV1` 
3. 在Receiver 端的时间 `tR2`  ，Receiver 收到消息，则往返时间 即 消息的接收时间减去发送时间： `RTT = tR2 - tR1`
4. 有了 往返时间 `RTT` 和 Sender 本地时间戳 `tS1` ，就可以 估算 Sender的单调时钟了。Sender的当前时间 `tR2` , 近似等于 `tS1` 加上 往返时间 `RTT` 的一半
5. 有了 Sender 本地时钟时间戳 `tS1` ， video track 时间戳 `tSV1`  和 往返时间 `RTT` ，就可以 将 Receiver 端 的 video track time 同步 到 Sender端的 video track 

现在我们知道  Sender 发出了最后一个 视频帧时间 `tSV1` 之后，过去了多长时间，我们可以 用 期待的视频时间 减去 当前播放的视频时间 来 近似  时间延迟：

```
expected_video_time = tSV1 + time_since(tSV1)
latency = expected_video_time - actual_video_time
```

*译者注：期待的视频时间指的是 没有时延的情况下应该播放到哪个时间，在Sender端，tSV1时间采集tSV1,之后，过了 time_since(tSV1)时间，Sender端当前应该采集的是 tSV1 + time_since(tSV1)，无延迟情况下，期待的视频时间也就是Sender当前应该采集的时间。*

这种方法的缺陷是没有包含相机内部的延迟。
大多数视频系统一般以 相机的帧传送到内存的时间, 作为这一帧的拍摄时间戳，
这一帧所记录的事件，它实际发生的时间 会比 这一帧传送到内存的时间的略早

#### 延迟测量示例

一个简单实现是在Receiver端开启一个 `latency` data channel，并定期地发送 Receiver单调时钟时间戳 到 Sender端。Sender端 响应一个 JSON 消息（消息中包含上面提到的三个时间）然后，Receiver 根据 这个 消息 来计算延迟。

```json
{
    "received_time": 64714,       // Timestamp sent by receiver, sender reflects the timestamp. 
    "delay_since_received": 46,   // Time elapsed since last `received_time` received on sender.
    "local_clock": 1597366470336, // The sender's current monotonic clock time.
    "track_times_msec": {
        "myvideo_track1": [
            13100,        // Video frame RTP timestamp (in milliseconds).
            1597366470289 // Video frame monotonic clock timestamp.
        ]
    }
}
```

在Receiver端开启 这个 `latency` data channel :

```javascript
dataChannel = peerConnection.createDataChannel('latency');
```

定期发送Receiver端的时间 `tR1` ，示例中使用的周期是2秒 ：

```javascript
setInterval(() => {
    let tR1 = Math.trunc(performance.now());
    dataChannel.send("" + tR1);
}, 2000);
```

Sender端处理来自 Receiver 的消息：

```javascript
// Assuming event.data is a string like "1234567".
tR1 = event.data
now = Math.trunc(performance.now());
tSV1 = 42000; // Current frame RTP timestamp converted to millisecond timescale.
tS1 = 1597366470289; // Current frame monotonic clock timestamp.
msg = {
  "received_time": tR1,
  "delay_since_received": 0,
  "local_clock": now,
  "track_times_msec": {
    "myvideo_track1": [tSV1, tS1]
  }
}
dataChannel.send(JSON.stringify(msg));
```

Receiver端，处理来自 Sender的消息，并在console上 打印估算的时延：

```javascript
let tR2 = performance.now();
let fromSender = JSON.parse(event.data);
let tR1 = fromSender['received_time'];
let delay = fromSender['delay_since_received']; // How much time that has passed between the sender receiving and sending the response.
let senderTimeFromResponse = fromSender['local_clock'];
let rtt = tR2 - delay - tR1;
let networkLatency = rtt / 2;
let senderTime = (senderTimeFromResponse + delay + networkLatency);
VIDEO.requestVideoFrameCallback((now, framemeta) => {
    // Estimate current time of the sender.
    let delaySinceVideoCallbackRequested = now - tR2;
    senderTime += delaySinceVideoCallbackRequested;
    let [tSV1, tS1] = Object.entries(fromSender['track_times_msec'])[0][1]
    let timeSinceLastKnownFrame = senderTime - tS1;
    let expectedVideoTimeMsec = tSV1 + timeSinceLastKnownFrame;
    let actualVideoTimeMsec = Math.trunc(framemeta.rtpTimestamp / 90); // Convert RTP timebase (90000) to millisecond timebase.
    let latency = expectedVideoTimeMsec - actualVideoTimeMsec;
    console.log('latency', latency, 'msec');
});
```

#### 浏览器上确切的视频时间

> `<video>.requestVideoFrameCallback()` 允许web开发者在 视频帧可以被合成图像时收到通知。

直到现在(2020年5月)，我们还无法在在浏览器上获取 视频当前播放帧 的 确切时间戳 。
虽然存在一个基于`video.currentTime` 的变通方法，但得到的结果也不是特别精确。

Chrome 和 Mozilla 的浏览器开发者都[支持](https://github.com/mozilla/standards-positions/issues/250) 引入 新的 W3C 标准，[`HTMLVideoElement.requestVideoFrameCallback()`](https://wicg.github.io/video-rvfc/) ，该标准添加了一个API回调来访问 当前视频帧的时间。
这个添加听起来微不足道，但是它目前已经赋能了多个Web上的高级的媒体应用，赋予了它们在Web上进行 音视频同步的能力。
对于 WebRTC 而言， 回调中将包含 `rtpTimestamp` 字段，该 RTP 时间戳 关联 当前视频帧的时间。
这个接口理应出现在WebRTC， 可惜目前还没有。

### 延迟的调试技巧

由于调试很可能会影响测量到的延迟值，所以大体原则是：将你的环境简化到能复现问题的最小环境。
移除越多的组件，就越容易找到造成延迟问题的组件。

#### 相机延迟

根据相机设置，相机延迟可能会有所不同。
检查 自动曝光、自动对焦和自动白平衡 等设置。
网络摄像头的所有自动功能都需要一些额外的时间来分析捕获的图像，然后才能将其提供给 WebRTC 。

如果环境是 Linux ，你可以使用 `v4l2-ctl` 命令行工具 来控制相机设置：

```bash
# Disable autofocus:
v4l2-ctl -d /dev/video0 -c focus_auto=0
# Set focus to infinity:
v4l2-ctl -d /dev/video0 -c focus_absolute=0
```

你也可以使用UI工具  `guvcview`  ，快速检测和调整 相机设置。

#### 编码延迟

大多数现代编码器会在输出 已编码数据 之前，先缓存一些帧。
编译器的首要目标是 维持 输出图像质量 与 比特率 之间的平衡。
多通道编码器就是编码器 忽略 输出时延 的一个极端例子。
只有当第一通道编码器获取到完整视频数据后，才会开始输出 视频帧。

不过，通过适当的调整，我们可以减少 sub-frame latencies (*译者注：这里应该是指 subsequent-frame,避免对后续帧的依赖 * ) 。
请确保您的编码器不使用过多的参考帧或 B帧。
每个编解码器的延迟调整设置都不同，但对于 x264，我们建议使用 `tune=zerolatency` 和 `profile=baseline` 以获得最低的帧输出延迟。

#### 网络延迟

对于网络延迟，我们能做的不多，最好的方法就是升级到更好的网络连接。
网络延迟很像天气——你不能阻止下雨，但你可以查看天气预报然后打把雨伞。
WebRTC 以 毫秒级 的精度 测量 网络状态。
重要的指标有：

- 往返时间
- 丢包与包重传

**往返时间**

WebRTC 有内建的 网络往返时间(round trip time, RRT) [测量机制](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats-roundtriptime) 。
延迟的一个很不错的近似 是 `RTT/2` 。这种近似 假设 发包 与 收包 花费同样的时间，实际很多情况下都是不一样的。
RTT 界定了 端到端的最低时延。
视频帧无法在比 `RTT/2` 还短的时间 送达 接收端，不管相机到编码的链路怎样优化。

内建的RTT 机制，基于特殊的RTCP包，即 sender/receiver reports。
Sender 发送自己的时间戳 给 Receiver, Receiver 将这个时间戳回传给Sender。
这样，Sender就知道 这个 数据包 去往 Receiver 再 返回 一共花了多长时间。
RTT测量的更多内容，请参阅  [Sender/Receiver Reports](../06-media-communication/#senderreceiver-reports)  章节。

**丢包与包重传**

RTP 和 RTCP 都是基于 UDP ，UDP 不对  顺序传输、成功送达、数据不重复 等提供任何保障。
所有的这些在实际的WebRTC应用中 都会发生，也总是在发生。
一个简单的解码器实现会期望一个视频帧的所有数据包都完整送达，以便解码器能重新生成图像。
出现丢包会造成各种问题， [P-帧](../06-media-communication/#inter-frame-types) 丢包时，可能会出现解码出错误图像；
I-帧 丢包时，则所有依赖于这个 I-帧 的 一系列视频帧都将出现 错误图像，甚至无法被解码。这种情况很可能会造成 视频 卡住一段时间 。

为了避免视频 (当然只是尽量避免)卡住或者解码错误，WebRTC 使用 negative acknowledgement ([NACK](../06-media-communication/#negative-acknowledgment))。
当 Receiver 没有 收到 一个 期待的RTP包时，将 返回 NACK 消息 给 Sender, 告知 Sender 重传这个丢失的包。
这样的重传会引入额外的延迟。
NACK 包的发送数量和接收数量会被记录在 WebRTC 内建的 统计数据字段  [outbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-nackcount) 和 [inbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-nackcount)  。

你可以在 [webrtc internals page](#webrtc-internals) 中看到  `nackCount`   发送数和接收数的图表。
如果你看到 `nackCount` 增加，这意味着网络正处于 高丢包状态，而WebRTC 内部将尽力创建一个流畅的 音视频 体验，即使在糟糕的网络环境下。

当丢包率高到解码器无法解码出图像时，或者 被依赖的帧丢失（如I-帧完整丢失），所有后续相关的 P-帧 都将无法解码。
这种情况下，接收者将通过发送 Picture Loss Indication ([PLI](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)) 消息来尝试缓解。
一旦Sender 接收到一个 `PLI` 消息，它将生成一个新的 I-帧来帮助Receiver端 解码器。
I-帧 一般比P-帧大，这也增加了需要传输的数据包数量。
和 NACK 消息一样，Receiver 需要等待新的I-帧，这也引入了额外的延迟。

关注 [webrtc internals page](#webrtc-internals) 的 `pliCount` 指标，如果它增加了，
需要 调整编码器 以 输出 较少的 数据包；
或者开启 更高容错 的通信模式。

#### 接收端延迟

接收端延迟会受乱序到达的数据包影响。
如果一个图像，下半部分的数据包比上半部分的数据包先到达，则必须等待上半部分的数据包到达，才能开始解码。
关于这个问题的更详细内容在  [Solving Jitter](05-real-time-networking/#solving-jitter) 章节。

你也可以参考内建的  [jitterBufferDelay](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) 指标，看看一个视频帧 在等待所有 数据包到达前， 在 Receiver 缓存中 被 保留了多久 。只有所有的相关的数据包都到达了，视频帧才会推给 解码器。

