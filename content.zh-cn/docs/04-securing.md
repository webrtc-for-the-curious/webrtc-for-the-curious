---
title: 安全性
type: docs
weight: 5
---

# WebRTC具有哪些安全性保障？

每个WebRTC连接都经过身份验证和加密。您可以确信第三方看不到您发送的内容，也无法插入虚假消息。您还可以确保与您进行通信的WebRTC代理正是生成会话描述的代理。

没有人能够篡改消息这一点非常重要。如果第三方在传输中读取了会话描述，这不会产生什么影响。然而，WebRTC无法防止会话描述被修改。攻击者可以通过更改ICE候选地址和证书指纹来对您进行MITM（Man-in-the-middle）攻击。

{{< hint info >}}
译注：这里指的是，P2P连接建立之后，双方之间的通信安全是有保障的。但在连接建立的过程中，攻击者可以通过MITM方式伪装中间人同时与通信双方建立连接并通信。
{{< /hint >}}

## 它是如何做到的？

WebRTC使用两个预先存在的协议[DTLS](https://tools.ietf.org/html/rfc6347)和[SRTP](https://tools.ietf.org/html/rfc3711)。

DTLS使您可以协商会话，然后在两个peer之间安全地交换数据。它是TLS的同类产品，而TLS是HTTPS使用的技术。DTLS是通过UDP而不是TCP进行的，因此协议必须处理不可靠的数据传输。SRTP是专为交换媒体数据而设计的。相对于DTLS而言，我们可以使用SRTP对传输进行一些优化。

DTLS先被使用。它通过ICE提供的连接进行一次握手。DTLS是一种客户端/服务器协议，因此其中一侧需要开始握手。客户端/服务器的角色是在信令中被确定的。在DTLS握手期间，双方都会提供证书。
握手完成后，需要将收到的证书与`会话描述`中的证书哈希进行比较。这是为了确定握手的目标就是您所期望的WebRTC代理。接下来，可以将DTLS连接用于DataChannel通信。

要创建SRTP会话，我们使用DTLS生成的密钥对其进行初始化。SRTP没有握手机制，因此必须使用外部密钥进行引导。完成此操作后，媒体数据即可以通过SRTP加密并进行交换！

## 安全性101

要了解本章介绍的技术，您首先需要了解这些术语。密码学是一个棘手的主题，因此其他资源也是值得参考的！

#### Cipher

Cipher是将明文转换为密文的一系列步骤。Cipher可以反过来运行，因此您可以将密文恢复为明文。一个Cipher通常拥有一个更改其行为的密钥。还有一个术语是加密和解密。

举例来说，一个简单的cipher是ROT13。也就是每个字母向前移动13个字符。要解密这个cipher，需要每个字母向后移动13个字符。明文`HELLO`将成为密文`URYYB`。 在这种情况下，Cipher是ROT，密钥是13。

#### 明文/密文

明文是cipher的输入。密文是cipher的输出。

#### 哈希

哈希是一种生成摘要的单向过程。给定一个输入，它每次都会生成相同的输出。其重要特点是输出不可逆。也就是说，根据输出的摘要，无法确定其输入。当您要确认消息未被篡改时，哈希很有用。

举例来说，一个简单的哈希将是仅将所有其他字母`HELLO`变成`HLO`。您不能认为`HELLO`就是输入，但可以确认如果输入的是`HELLO`，那么结果是匹配的。

#### 公钥/私钥加密

公钥/私钥加密描述了DTLS和SRTP使用的cipher类型。在此系统中，您有两个密钥，即公钥和私钥。公钥用于加密消息，可以安全共享。
私钥用于解密消息，不应共享。当解密那些使用对应的公钥加密的消息时，它是唯一的密钥。

#### Diffie-Hellman交换

Diffie-Hellman交换允许两个以前从未见过的用户通过Internet安全的交换信息。 用户`A`可以将信息发送给用户`B`，而不必担心被窃听。破解该信息依赖于破解离散对数问题的难度。
您不必完全理解这一点，但这可以帮助您了解DTLS握手是如何变得可行的。

Wikipedia在[此处](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation)中有一个实际的例子。

#### 伪随机函数（PRF）

伪随机函数是一个预定义函数，用于生成随机出现的值。它可能需要多个输入并生成一个输出。

#### 密钥派生（KDF）

密钥派生是一类伪随机函数。是一种用于增强密钥的安全性的方法。一种常见的模式是密钥扩展。

假设您获得的密钥为8字节。您可以使用KDF使其更坚固。

#### Nonce

Nonce是cipher的附加输入。这样，即使您多次加密同一条消息，也可以从cipher中获得不同的输出。

如果将同一条消息加密10次，cipher将为您提供10次相同的密文。通过使用nonce，在使用同一个密钥的情况下，您将得到不同的输入。需要注意的是，每条消息都要使用不同的nonce！ 否则就没有什么意义了。

#### 消息身份验证代码（Message Authentication Code）

消息身份验证代码（MAC）是放在消息末尾的哈希值。MAC能证明该消息来自您期望的用户。

如果您不使用MAC，攻击者可能会插入无效的消息。因为他们不知道密钥，所以这些消息解密后是无意义的垃圾内容。

#### 密钥轮换

密钥轮换是一种间隔一段时间便更改密钥的做法。这种做法会使得被窃取的密钥影响较小。如果密钥被窃取或泄漏，那么只有很少的数据可以被解密。

## DTLS

DTLS（数据报传输层安全协议）允许两个peer在没有预先存在的配置的情况下建立安全的通信。即使有人窃听了通信，他们也将无法解密消息。

为了使DTLS客户端和服务器进行通信，他们需要就cipher和密钥达成一致。他们通过进行DTLS握手来确定这些值。在握手期间，消息为纯文本格式。
当DTLS客户端/服务器交换了足够的详细信息以开始加密时，它会发送`Change Cipher Spec`（更改Cipher规格）。在此消息之后，后续的每个消息都将被加密！

### 数据包格式
每个DTLS数据包开头都包含一个头部信息

#### 内容类型

您可以看到包括以下类型

* Change Cipher Spec（更改Cipher规格） - `20`
* Handshake（握手） - `22`
* Application Data（应用程序数据） - `23`

`握手`用于交换详细信息以开始会话。 `更改Cipher规格`用于通知另一端所有内容都将被加密。`应用程序数据`是加密的消息。

#### 版本
版本可以是`0x0000feff`（DTLS v1.0）或`0x0000fefd`（DTLS v1.2），没有v1.1。

#### Epoch（时段）
时段从`0`开始，但在`更改Cipher规格`之后变为`1`。在非零时段的任何消息都将被加密。

#### 序列号
序列号用于保持消息顺序。每条消息都会增加序列号。当时段增加时，序列号重新开始。

#### 长度和有效载荷
有效载荷是特定于`内容类型`的。 对于`应用程序数据`，`有效载荷`是加密的数据。 对于`握手`，它会根据消息而有所不同。

长度是指有效载荷的大小。

### `握手`状态机
在握手期间，客户端/服务器交换一系列消息。这些消息被分为多个Flight。每个Flight中可能有多个消息（或只有一个）。
直到收到Flight中的所有消息，该Flight才算完成。我们将在下面更详细地描述每条消息的目的，

{{<mermaid>}}
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: ClientHello
    Note over C,S: Flight 1

    S->>C: HelloVerifyRequest
    Note over C,S: Flight 2

    C->>S: ClientHello
    Note over C,S: Flight 3

    S->>C: ServerHello
    S->>C: Certificate
    S->>C: ServerKeyExchange
    S->>C: CertificateRequest
    S->>C: ServerHelloDone
    Note over C,S: Flight 4

    C->>S: Certificate
    C->>S: ClientKeyExchange
    C->>S: CertificateVerify
    C->>S: ChangeCipherSpec
    C->>S: Finished
    Note over C,S: Flight 5

    S->>C: ChangeCipherSpec
    S->>C: Finished
    Note over C,S: Flight 6
{{</mermaid>}}

#### ClientHello
ClientHello是客户端发送的初始消息。它包含一个属性列表。这些属性告诉服务器客户端支持的cipher和功能。对于WebRTC，这也是我们选择SRTP cipher方式的原因。它还包含将用于生成会话密钥的随机数据。

#### HelloVerifyRequest
服务器将HelloVerifyRequest发送到客户端。这是为了确认客户端准备继续发送请求。然后，客户端重新发送ClientHello，但这一次需要携带HelloVerifyRequest中提供的令牌。

#### ServerHello
ServerHello是服务器响应消息，是此次会话的配置信息。它包含此会话直到结束时将使用的cipher。它还包含服务器端的随机数据。

#### Certificate
Certificate包含客户端或服务器的证书。它被用来唯一识别我们与之通信的对方。握手结束后，我们将确保这个证书的哈希与`SessionDescription`中的指纹相匹配。

#### ServerKeyExchange/ClientKeyExchange
这些消息用于传输公共密钥。在启动时，客户端和服务器都会生成密钥对。握手后，这些值将被用来生成 **Pre-Master Secret**

#### CertificateRequest
CertificateRequest由服务端发送，用来通知客户端需要一个证书。服务端既可以请求一个证书，也可以要求必须提供证书。

#### ServerHelloDone
ServerHelloDone通知客户端此时服务器已完成握手动作。

#### CertificateVerify
发送者用CertificateVerify消息来证明他已经获得了Certificate消息中发送的私钥。

#### ChangeCipherSpec
ChangeCipherSpec通知接收者在此消息之后发送的所有内容都将被加密。

#### Finished
Finished消息是加密的，它包含所有消息的哈希。用来断言握手过程未被篡改。

### 密钥的生成
握手完成后，您可以开始发送加密数据。Cipher是由服务器选择的，位于ServerHello消息中。但接下来如何生成密钥呢？

首先，我们需要生成`Pre-Master Secret`。为了获得该值，我们通过`ServerKeyExchange`和`ClientKeyExchange`消息，使用Diffie-Hellman算法来交换密钥。细节因选定的Cipher而异。

接下来，生成`Master Secret`。每个版本的DTLS都有一个定义的`Pseudorandom function`（伪随机函数）。对于DTLS 1.2，PRF（伪随机函数）会在`ClientHello`和`ServerHello`中获取`Pre-Master Secret`和随机值。
运行`Pseudorandom function`后，获得的输出是`Master Secret`。`Master Secret`是用于Cipher的密钥。

### 交换ApplicationData
DTLS的主要内容是`ApplicationData`。现在我们有了一个初始化好的Cipher，我们可以开始加密和发送数据了。

如前所述，`ApplicationData`消息使用DTLS标头。`Payload`中填充了密文。您现在可以正常使用DTLS会话，并且可以安全地进行通信。

DTLS具有更多有趣的功能，例如重新协商等。WebRTC中不使用此功能，因此此处不作介绍。

## SRTP
SRTP是仅用于加密RTP数据包的协议。要启动SRTP会话，需要指定密钥和cipher。与DTLS不同，它没有握手机制。因此，所有的配置和密钥都是在DTLS握手期间配置的。

DTLS提供了专用的API，用来导出密钥以供另一个进程使用。这是在[RFC 5705](https://tools.ietf.org/html/rfc5705)中定义的

### 会话创建
SRTP定义了一个密钥派生函数，用于处理输入。在创建SRTP会话时，密钥派生函数将被执行，用输入数据生成SRTP Cipher的密钥。之后，您可以继续处理媒体。

### 交换媒体数据
每个RTP数据包都有一个16位的SequenceNumber（序列号）。这些序列号用于使数据包保持顺序，就像主键一样。在通话期间，这些序列号将滚动累加。SRTP会对其进行跟踪，并将其称为滚动计数器。

加密数据包时，SRTP使用滚动计数器和序列号作为nonce。这是为了确保即使两次发送相同的数据，密文也会有所不同。这很重要，否则攻击者可以识别模式或尝试重播攻击。