---
title: 连接
type: docs
weight: 4
---

# 为什么WebRTC需要专用的子系统进行连接？

目前，大多数部署的应用程序都通过客户端/服务器方式进行连接。对于客户端/服务器连接，它要求服务器具有稳定且公开可用的传输地址。客户端与服务器联系，然后服务器做出响应。

WebRTC不使用客户端/服务器，它建立点对点（P2P）连接。 在P2P连接中，创建连接的任务被平均分配给两个对等方。这是因为无法猜测WebRTC中的传输地址（IP和端口），而且，在会话过程中，传输地址甚至可能会变更。WebRTC将收集所有可能收集的信息，并将尽力实现两个WebRTC代理之间的双向通信。

听起来简单，建立点对点连接实际上可能会非常困难。这些代理可能位于没有直接连接的不同网络中。即使在两个代理可以直接连接的情况下，您可能还会遇到其他问题。比如在某些情况下，两个客户端使用不同的网络协议（UDP <-> TCP）或使用不同的IP版本（IPv4 <-> IPv6）。

尽管在建立点对点连接方面存在一些困难，在WebRTC提供的下面这些属性的帮助下，您仍然可以获得相对于传统客户端/服务器技术的一些优势。

### 降低带宽成本

由于媒体通信直接发生在Peer之间，因此您无需为传输它而付费（无需经过第三方服务器并为此付费）。

### 更低延迟

直接通信时速度更快！当用户必须通过您的服务器运行所有内容时，这会使事情变慢。

### 安全的端到端通信

直接通信更安全。由于用户数据根本没有通过服务器，因此用户不需要考虑服务端会不会解密。

## 它是如何工作的？

上面描述的连接过程是通过Interactive Connectivity Establishment（[交互式连接建立/ICE](https://tools.ietf.org/html/rfc8445)） 实现的。这是另一个在WebRTC之前就已经出现的协议。

ICE是一种用来寻找两个ICE代理之间通信的最佳方式的协议。每个ICE代理都会发布如何访问自己的方式，这些路径被称为候选地址（candidates）。候选地址本质上是一个传输地址，ICE代理认为这个传输地址可能可以被对端访问到。接下来ICE将确定候选地址的最佳搭配。

本章稍后将详细介绍实际的ICE过程。要了解ICE为什么存在，最好先了解我们要面临的网络特性。

## 现实世界的网络限制

ICE就是克服现实世界网络限制的方法。在我们开始讨论ICE如何解决问题之前，先讨论一下有哪些实际问题。

### 不在同一个网络中

在大多数情况下，两个WebRTC代理不在同一个网络中。典型的呼叫通常是在没有直接连接的不同网络中的两个WebRTC代理之间进行的。

下面是通过公共互联网连接的两个不同网络的示意图。在每个网络中，您拥有两个主机。

{{<mermaid>}}
graph TB
subgraph netb ["Network B (IP Address 5.0.0.2)"]
  b3["Agent 3 (IP 192.168.0.1)"]
  b4["Agent 4 (IP 192.168.0.2)"]
  routerb["Router B"]
  end

subgraph neta ["Network A (IP Address 5.0.0.1)"]
  routera["Router A"]
  a1["Agent 1 (IP 192.168.0.1)"]
  a2["Agent 2 (IP 192.168.0.2)"]
  end

pub{Public Internet}
routera-->pub
routerb-->pub

{{</mermaid>}}

对于同一网络中的主机来说，互相连接非常容易。例如在`192.168.0.1 -> 192.168.0.2`之间通讯就很容易！这两个主机无需任何外部帮助即可相互连接。

但是，使用`Router B`的主机无法直接访问`Router A`背后的任何主机。您如何区分`Router A`后面的`191.168.0.1`主机和`Router B`后面相同IP的主机之间的区别呢？它们都使用内网IP！使用`Router B`的主机可以将数据直接发送到`Router A`，但是请求在那里就结束了。`Router A`怎么知道它应该将消息转发给哪台主机呢？

### 协议限制

有些网络不允许UDP通信，或者也有可能不允许TCP。有些网络的MTU（Maximum Transmission Unit/最大传输单元）可能非常低。网络管理员可以更改许多变量，这些修改可能会使通信变得困难。

### 防火墙/IDS规则

另一个问题是`深度数据包检查`和其他智能过滤方式。某些网络管理员将运行一些软件，这些软件会试图处理每个数据包。很多时候，这些软件无法识别WebRTC的数据包，由于它们不知道如何处理，它们可能会阻拦这些数据包，例如，它们可能将WebRTC数据包视为不在端口白名单上的可疑UDP数据包。

## NAT映射

NAT（网络地址转换）映射是使得WebRTC连接成为可能的魔法。WebRTC就是使用NAT让处于完全不同的子网中的两个peer进行通信，从而解决了上述"不在同一网络中"的问题，这同时也带来了新的挑战。首先，让我们解释一下NAT映射是如何工作的。

NAT映射不使用中继，代理或服务器。跟上一个例子一样，我们有`Agent 1`和`Agent 2`，它们位于不同的网络中。然而，流量穿透了路由器。看起来就像这样：

{{<mermaid>}}
graph TB
subgraph netb ["Network B (IP Address 5.0.0.2)"]
  b2["Agent 2 (IP 192.168.0.1)"]
  routerb["Router B"]
  end

subgraph neta ["Network A (IP Address 5.0.0.1)"]
  routera["Router A"]
  a1["Agent 1 (IP 192.168.0.1)"]
  end

pub{Public Internet}

a1-.->routera;
routera-.->pub;
pub-.->routerb;
routerb-.->b2;
{{</mermaid>}}

想要这样通信的话，您需要创建一个NAT映射。Agent 1使用端口7000与Agent 2建立WebRTC连接。这将创建一个`192.168.0.1:7000`到`5.0.0.1:7000`的绑定。然后，Agent 2将数据包发送到`5.0.0.1:7000`时，数据包会被转发给Agent 1。在这个例子中，创建一个NAT映射，就像是在路由器中做了一次自动化的端口转发。

NAT映射的缺点是：映射的形式不止一种（例如静态端口转发），并且映射的实现方式在不同的网络中也是不一样的。ISP和硬件制造商可能会以不同的方式来实现NAT映射。在某些情况下，网络管理员甚至可能禁用它。

好消息是，NAT映射的所有行为都是可以理解和观察到的，因此ICE代理能够确认其创建了NAT映射，并确认该映射的属性。

描述这些行为的文档是 [RFC 4787](https://tools.ietf.org/html/rfc4787)。

### 创建映射

创建映射是最简单的部分。当您将数据包发送到网络外部的地址时，一个映射就被创建出来了！NAT映射只是由NAT分配的一个临时的公共IP/端口。出站的消息将被重写，使得其源地址变为新创建的映射地址。如果有消息被成功发到映射地址，消息会被自动路由返回给NAT网络中创建这个映射地址的主机。

说到映射相关的细节，这就开始变得复杂了。

### 映射创建的行为

映射创建分为三类：

#### 端点无关的映射

这种创建方式为NAT网络中的所有发送者只创建一个映射。如果您将两个数据包发送到两个不同的远程地址，这个NAT映射将被重用。两个远程主机将看到相同的源IP/端口。如果远程主机响应，它将被发送回相同的本地侦听器。

这是最好的情况。要使得呼叫能够建立起来，至少一侧必须是这种类型。

#### 地址相关的映射

每次将数据包发送到新地址时，都会创建一个新的映射。如果您将两个数据包发送到不同的主机，则会创建两个映射。如果将两个数据包发送到同一远程主机，但目标端口不同，则不会创建新的映射。

#### 地址和端口相关的映射

如果远程IP或端口不同，则会创建一个新的映射。如果将两个数据包发送到同一远程主机，但目标端口不同，则将创建一个新的映射。

### 映射过滤行为

映射过滤是关于允许谁使用映射的规则。它们分为三个类似的类别：

#### 端点无关的过滤

任何人都可以使用该映射。您可以与其他多个peer共享该映射，他们都可以向该映射发送流量。

#### 地址相关的过滤

只有为其创建映射的主机才能使用该映射。如果您将数据包发送到主机`A`，则它可以根据需要返回任意数量的数据包。如果主机`B`尝试将数据包发送到该映射，将被忽略。

#### 地址和端口相关的过滤

仅有创建映射的主机和端口可以使用该映射。如果您将数据包发送到主机`A:5000`，则它可以根据需要返回任意数量的数据包。如果主机`A：5001`尝试将数据包发送到该映射，将被忽略。

### 映射的刷新

通常的建议是，如果5分钟未使用映射，则应将其销毁。但这完全取决于ISP或硬件制造商。

{{< hint info >}}
译注：换个说法，NAT映射的创建即是NAT网络中的主机`发送`数据时，路由器的处理方式；而过滤即是`接收`数据时，路由器的处理方式。映射的刷新即是路由器`释放`映射的处理方式。不同网络情况不同，因此某些特定的搭配会导致两个网络间无法建立P2P连接。在穿透相关的技术中，将不同的情况称为不同的`锥形`。
{{< /hint >}}

## STUN

STUN（NAT会话传输实用程序）是一种用来配合NAT使用的协议。这是WebRTC（和ICE！）之前的另一项技术。它由[RFC 5389](https://tools.ietf.org/html/rfc5389)定义，该文件还定义了STUN数据包结构。STUN协议也在ICE/TURN中被使用。

STUN很有用，因为它允许以编程方式创建NAT映射。在STUN之前，我们能够创建NAT映射，但是我们不知道映射的IP/端口是什么！STUN不仅使您能够创建映射，还可以获取映射的详细信息，用来与他人共享，这样他们便可以通过您创建的映射向您传送数据。

让我们从对STUN的基本描述开始。稍后，我们再将话题扩展到TURN和ICE的用法。现在，我们只打算描述请求/响应流程来创建映射。然后，我们将讨论如何获取该映射的详细信息以便与他人共享。当您在ICE URLs中有一个用于WebRTC PeerConnection的`stun:`服务器时，此过程就会发生。简而言之，STUN向NAT外部的STUN服务器发送请求，服务器返回其在请求中观察到的内容，STUN根据这些内容来帮助NAT后面的端点找出已创建的映射。

### 协议结构

每个STUN数据包都具有以下结构：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|0 0|     STUN Message Type     |         Message Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Magic Cookie                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     Transaction ID (96 bits)                  |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### STUN 消息类型

每个STUN数据包都有一个类型。目前，我们仅关心以下几种：

* Binding Request - `0x0001`
* Binding Response - `0x0101`

为了创建一个NAT映射，我们发出一个`Binding Request`。然后服务器回应一个`Binding Response`。

#### 消息长度

这就是`Data`段的长度。这一段中包含由`消息类型`所定义的任意数据。

#### Magic Cookie

指的是固定值`0x2112A442`，以网络字节顺序发送。这个值有助于将STUN流量与其他协议区分开。

#### 交互（Transaction）ID

一个96-bit的标识符，用于唯一标识一个请求/响应对。这可以帮助您配对请求和响应。

#### 数据

数据将包含一个STUN属性的列表。一个STUN属性具有以下结构。

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 ```

`STUN Binding Request`不使用任何属性。这意味着一个`STUN Binding Request`仅包含header。

`STUN Binding Response`使用一个`XOR-MAPPED-ADDRESS (0x0020)`。此属性包含一个IP/端口对。这正是所创建的NAT映射的IP/端口对！

### 创建NAT映射

使用STUN创建NAT映射只需要发送一个请求！您向STUN服务器发送一个`STUN Binding Request`。然后，STUN服务器回应一个`STUN Binding Response`。
该`STUN Binding Response`将包含`映射地址`。`映射地址`是STUN服务器看到您的方式，也是您的`NAT映射`。
如果您希望某人向您发送数据包，那么您应该共享该`映射地址`。

人们还会将`映射地址`称为`公网IP`或`Server Reflexive Candidate`。

### 确定NAT类型

不幸的是，`映射地址`可能并非在所有情况下都可用。如果是`地址相关的映射`，则只有STUN服务器才能将流量发送回给您。如果您共享它，那么另一个peer尝试向该地址发送的消息将被丢弃。这使得该peer无法与别的peer交流。如果STUN服务器还可以为您将数据包转发给对端peer，您可能会发现`地址相关的映射`问题实际上是可以解决的！这也就是下面将要说到的TURN解决方案。

[RFC 5780](https://tools.ietf.org/html/rfc5780)定义了一种方法，可以运行一个测试来确定您的NAT类型。 这很有用，因为您可能会提前知道是否可以进行直接连接。

## TURN

在无法建立直接连接的情况下，[RFC 5766](https://tools.ietf.org/html/rfc5766)中定义了TURN（使用中继穿透NAT）。当您的两个peer的NAT类型不兼容，或者双方使用不同协议时，就需要使用TURN！TURN也可以被用于保护隐私的目的。如果通过TURN运行所有通讯，客户的真实地址在对端是被隐藏的。

TURN使用专用服务器。该服务器充当客户端的代理。客户端连接到TURN服务器并创建一个对应的`Allocation`。通过创建该`Allocation`，客户端将获得一个临时`IP/端口/协议`三元组，其他peer可以使用该`IP/端口/协议`将数据发送给该客户端。这个新的监听地址被称为`中继传输地址`。您可将其视为转发地址并分享给他人，以便其他人可以通过TURN向您发送流量！对于每个将获得该`中继传输地址`的peer，您必须为其创建一个新的`Permission`，以允许它与您进行通信。

当您通过TURN发送出站流量时，它会通过`中继传输地址`发送。当远程peer获得该出站流量时，他们会看到数据来自TURN服务器。

### TURN生命周期

下面就是一个客户端创建TURN `allocation`时必须做的所有事情。对于其他peer而言，与使用TURN服务器的客户端进行通信和其他客户端没有任何区别，先获得IP/端口，然后像跟其他任何主机一样通信。

#### Allocations

Allocations是TURN的核心。本质上，一个`allocation`就是一个`TURN会话`。要创建一个TURN allocation，您需要与TURN `Server Transport Address`（服务器传输地址，通常在3478端口）进行通信。

创建allocation时，您需要提供/确定以下内容
* 用户名/密码 - 创建TURN allocation时需要身份验证
* Allocation传输方式 - `中继传输地址`可以是UDP或TCP方式
* 连续端口 - 您可以为多个allocation请求顺序排列的一系列端口，这点与WebRTC无关

如果请求成功，您将在TURN服务器上获得响应，在响应的数据部分，包含以下的STUN属性。
* `XOR-MAPPED-ADDRESS` - `TURN Client`的`Mapped Address`。当有人将数据发送到`中继传输地址`时，数据将被转发到该地址。
* `RELAYED-ADDRESS` - 这是您提供给其他客户端的地址。如果有人将数据包发送到该地址，则会将其转发到TURN客户端。
* `LIFETIME` - Allocation被销毁的时间。您可以通过发送`Refresh`请求来延长这一时间。

{{< hint info >}}
译注：上面两个地址很拗口，但实际上理解起来并不复杂。`Mapped Address`是Turn Client的实际地址，也就是Turn Server收到数据包时的`目标地址`。而`Relayed Address`时Turn Client的名义地址，也就是其他WebRTC Agent要发送数据给这个Turn Client时，所使用的地址。
{{< /hint >}}

#### 权限

在您为远程主机创建权限之前，远程主机是无法通过您的`中继传输地址`发送数据的。所谓创建权限，即是告知TURN服务器一个"可以用来发送入站流量"的IP/端口。

远程主机需要先为您提供TURN服务器上使用的IP/端口。这意味着它应该先向TURN服务器发送一个`STUN绑定请求`。 有时会发生这样一个常见的错误情况，即是远程主机发送`STUN绑定请求`到另外一台服务器，然后再要求TURN服务器为此IP创建权限。

对于上面那种错误情况，假设您要为一个使用`地址相关的映射`的NAT网络的主机创建权限，如果您从其他TURN服务器生成`映射地址`，则所有入站流量都将被丢弃。因为每次他们与其他主机通信时，它都会生成一个新的映射。如果未被刷新，权限将在5分钟后过期。

{{< hint info >}}
译注：对于这个常见的错误情况，实际指的是被连接的主机从TURN服务器以外的STUN/TURN服务器获取本机IP，再告知发起连接的主机这样的情况。当被连接的主机使用`地址相关的映射`类型的NAT时，它获取的IP在当前的TURN服务器上是无效的。
{{< /hint >}}

#### SendIndication/ChannelData

这是TURN客户端将消息发送到远端peer时所使用的两个消息。

SendIndication是一个自包含的消息。它包含您希望发送的数据，以及您希望发送的目标。如果您要向远端peer发送大量消息的话，这种方式很昂贵。因为如果要发送1,000条消息，目标IP地址就被重复了1,000次！

ChannelData允许您发送数据，但不需要重复IP地址。您需要先创建一个具有IP/端口的通道（Channel）。然后使用ChannelId发送，IP/端口将在服务器端被填充进去。如果您要发送大量消息，这是更好的选择。

#### 刷新

Allocations将自动销毁。要避免其过早销毁，TURN客户端必须在创建allocation时指定的`LIFETIME`到来之前，及时刷新它们。

### TURN 使用方法

TURN有两种用法。通常情况下，一个peer会作为'TURN客户端'连接，而另一方则直接进行通信。在某些情况下，您可能在两侧都需要使用TURN服务。举例来说，当两个客户端都位于在禁用UDP的网络中时，只能通过TCP连接到各自的TURN服务器来建立连接。

下面这些图有助于说明TURN的用法。

#### 单个 TURN Allocation 通信
{{<mermaid>}}
graph TB

subgraph turn ["TURN Allocation"]
  serverport["Server Transport Address"]
  relayport["Relayed Transport Address" ]
  end

turnclient{TURN Client}
peer{UDP Client}

turnclient-->|"ChannelData (To UDP Client)"|serverport
serverport-->|"ChannelData (From UDP Client)"|turnclient

peer-->|"Raw Network Traffic (To TURN Client)"|relayport
relayport-->|"Raw Network Traffic (To UDP Client)"|peer
{{</mermaid>}}

#### 双重 TURN Allocation 通信
{{<mermaid>}}
graph TB

subgraph turna["TURN Allocation A"]
  serverportA["Server Transport Address"]
  relayportA["Relayed Transport Address" ]
  end

subgraph turnb["TURN Allocation B"]
  serverportB["Server Transport Address"]
  relayportB["Relayed Transport Address" ]
  end


turnclientA{TURN Client A}
turnclientB{TURN Client B}

turnclientA-->|"ChannelData"|serverportA
serverportA-->|"ChannelData"|turnclientA

turnclientB-->|"ChannelData"|serverportB
serverportB-->|"ChannelData"|turnclientB

relayportA-->|"Raw Network Traffic"|relayportB
relayportB-->|"Raw Network Traffic"|relayportA
{{</mermaid>}}

{{< hint info >}}
译注：单个TURN Allocation的情况，指的是一个TURN Client和另一个可访问的UDP Client的通信。双重TURN Allocation的情况，指的是两个TURN Client之间通信。
{{< /hint >}}

## ICE

ICE（交互式连接建立）是WebRTC连接两个代理的方式。这也是WebRTC之前的一项技术，在[RFC 8445](https://tools.ietf.org/html/rfc8445)中定义！ICE是用于建立连接的协议。它会确定两个peer之间所有可能的路由，然后确保您保持连接状态。

这些路由被称为`Candidate Pair（候选地址对）`，也就是本地地址和远程地址的配对。这就是STUN和TURN在ICE中发挥作用的地方。这些地址可以是您的本地IP地址，`NAT映射`或`中继传输地址`。通信双方需要收集它们要使用的所有地址，交换这些地址，然后尝试连接！

两个ICE代理使用ICE ping数据包（正式名称为连通性检查）进行通信。一旦建立连接后，他们就可以发送任何信息。感觉就像使用普通socket一样。连通性检查使用STUN协议。

### 创建ICE代理

ICE代理要么处于`控制中`，要么处于`受控中`。`控制中`的代理是决定选择`候选对`的代理。通常来说，发送offer的peer是`控制中`的一方。

每一方都必须有一个`用户片段`和一个`密码`。必须先交换这两个值，才能进行连接检查。`用户片段`以纯文本形式发送，用于多个ICE会话的解复用（demux）。
`密码`用于生成`MESSAGE-INTEGRITY`属性。在每个STUN数据包的末尾，都有这个属性，该属性是使用`密码`作为密钥的整个数据包的哈希值。这用于验证数据包并确保它未被篡改。

对于WebRTC，所有这些值都通过上一章中所述的`会话描述`进行分发。

### 候选地址收集

现在，我们需要收集所有可能联通的地址。这些地址被称为候选地址。这些候选地址也通过`会话描述`来分发。

#### 主机

主机候选地址直接在本地接口上侦听。可以是UDP或TCP方式。

#### mDNS

mDNS候选地址类似于主机候选地址，但是其IP地址是隐藏的。您不必给对方提供您的IP地址，只需要给他们提供一个UUID作为主机名。然后设置一个多播监听器，并在有人请求您发布的UUID时进行响应。

如果您与代理位于同一网络中，则可以通过多播找到彼此。如果不在同一网络中，则将无法连接（除非网络管理员明确配置网络以允许多播数据包通过）。

这对于保护隐私很有用。以前，用户可以通过WebRTC使用主机候选地址（甚至无需尝试与您连接）来找出您的本地IP地址。而使用mDNS候选地址的话，他们只能获得随机的UUID。

#### 服务器自反（Server Reflextive）

服务器自反候选地址是通过对STUN服务器执行`STUN绑定请求`时生成的。

当您收到`STUN绑定响应`时，`XOR-MAPPED-ADDRESS`就是您的服务器自反候选地址。

#### Peer自反

Peer自反候选地址是指，当您从您不知道的地址收到入站请求时，由于ICE是经过身份验证的协议，因此您知道这些传输是合法的，这只是意味着远端Peer是通过它也不知道的地址与您通信。

这通常会发生在这样的情况下，当`主机候选地址`与`服务器自反候选地址`进行通信时，由于您是在子网外部进行通信，因此创建了一个新的`NAT映射`。还记得我们说过的连通性检查实际上是STUN数据包吗？STUN响应的格式自然允许peer报告Peer自反地址。

#### 中继

中继候选地址是通过使用TURN服务器生成的。

在与TURN服务器进行初始握手之后，您将获得`RELAYED-ADDRESS`，这就是您的中继候选地址。

### 连通性检查

现在我们知道了远程代理的`用户片段`，`密码`和候选地址。我们可以尝试连接了！ 候选地址可以相互配对。因此，如果每边有3个候选地址，那么现在就有9个候选地址对。

看起来像这样
{{<mermaid>}}
graph LR

subgraph agentA["ICE Agent A"]
  hostA{Host Candidate}
  serverreflexiveA{Server Reflexive Candidate}
  relayA{Relay Candidate}
  end

style hostA fill:#ECECFF,stroke:red
style serverreflexiveA fill:#ECECFF,stroke:green
style relayA fill:#ECECFF,stroke:blue

subgraph agentB["ICE Agent B"]
  hostB{Host Candidate}
  serverreflexiveB{Server Reflexive Candidate}
  relayB{Relay Candidate}
  end

hostA --- hostB
hostA --- serverreflexiveB
hostA --- relayB
linkStyle 0,1,2 stroke-width:2px,fill:none,stroke:red;

serverreflexiveA --- hostB
serverreflexiveA --- serverreflexiveB
serverreflexiveA --- relayB
linkStyle 3,4,5 stroke-width:2px,fill:none,stroke:green;

relayA --- hostB
relayA --- serverreflexiveB
relayA --- relayB
linkStyle 6,7,8 stroke-width:2px,fill:none,stroke:blue;
{{</mermaid>}}

### 候选地址选择

`控制中`的代理和`受控中`的代理都开始在每个候选地址对上发送流量数据。这样是必须的，因为如果一个代理位于一个`地址相关映射`的网络中，这样会创建`Peer自反候选地址`。

每个收到流量数据的`候选地址对`，会被提升为`有效候选地址`对。接下来，`控制中`的代理将指定一个`有效候选地址`对。这就是`提名候选地址对`。然后，`控制中`的代理和`受控中`的代理再尝试进行一轮双向通信。如果成功，则`提名候选地址对`将成为`选定的候选地址对`！它将被用于后面的会话中。

### 重新启动

如果`选定的候选地址对`由于任何原因停止工作（如：NAT映射到期，TURN服务器崩溃等），则ICE代理将进入`失败`状态。此时可以重新启动两个代理，然后重新完整执行整个过程。