---
title: 调试
type: docs
weight: 10
---

# 调试
调试WebRTC可能是一项艰巨的任务。有很多部分都处于运行状态，每一个部分都可能出现问题。如果您不够细心，可能会浪费数周的时间来查看错误的模块。当您最终找到出错的部分时，您还需要学习一些知识才能理解它。

本章将带您学习WebRTC的调试。它将向您展示如何分析并定位相关问题。确定问题后，我们将快速介绍一下流行的调试工具。

### 分解问题
开始调试时，您需要先分析问题的根源。

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

    sudo tcpdump 'udp port 19302' -xx

- 与上一条相同，但将数据包保存在PCAP（数据包捕获）文件中以供以后检查

    sudo tcpdump 'udp port 19302' -w stun.pcap

  可以使用wireshark GUI打开PCAP文件：`wireshark stun.pcap`

#### wireshark
#### webrtc-internals
