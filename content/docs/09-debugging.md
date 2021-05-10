---
title: Debugging
type: docs
weight: 10
---


# Debugging
Debugging WebRTC can be a daunting task. There are a lot of moving parts, and they all can break independently. If you aren't careful, you can lose weeks of time looking at the wrong things. When you do finally find the part that is broken, you will need to learn a bit to understand why.

This chapter will get you in the mindset to debug WebRTC. It will show you how to break down the problem. After we know the problem, we will give a quick tour of the popular debugging tools.

### Isolate The Problem
When debugging, you need to isolate where the issue is coming from. Start from the beginning of the...

#### Signaling Failure
#### Networking Failure

Test your STUN server using netcat:

1. prepare the **20-byte** binding request packet:

    ```
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    ```

    interpretation:

    - `00 01` is the message type

    - `00 00` is the length of the data section

    - `21 12 a4 42` is the magic cookie

    - and `54 45 53 54 54 45 53 54 54 45 53 54` (which decodes to ASCII `TESTTESTTEST`) is the 12-byte transaction ID

2. send the request and wait for the **32 byte** response:

    ```
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    ```

    interpretation:

    - `01 01` is the message type

    - `00 0c` is the length of the data section which decodes to 12 in decimal

    - `21 12 a4 42` is the magic cookie

    - and `54 45 53 54 54 45 53 54 54 45 53 54` (which decodes to ASCII `TESTTESTTEST`) is the 12-byte transaction ID

    - `00 20 00 08 00 01 6f 32 7f 36 de 89` is the 12-byte data, interpretation:

        - `00 20` is the type: `XOR-MAPPED-ADDRESS`

        - `00 08` is the length of the value section which decodes to 8 in decimal

        - `00 01 6f 32 7f 36 de 89` is the data value, interpretation:

            - `00 01` is the address type (IPv4)

            - `6f 32` is the XOR-mapped port

            - `7f 36 de 89` is the XOR-mapped IP address

Decoding the XOR-mapped section is cumbersome, but we can trick the stun server to perform a dummy XOR-mapping, by supplying an (invalid) dummy magic cookie set to `00 00 00 00`:

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

XOR-ing against the dummy magic cookie is idempotent, so the port and address will be in clear in the response (this will not work in all situations, because some routers manipulate the passing packets, cheating on the IP address); if we look at the returned data value (last eight bytes):

  - `00 01 4e 20 5e 24 7a cb` is the data value, interpretation:

    - `00 01` is the address type (IPv4)

    - `4e 20` is the mapped port, which decodes to 20000 in decimal

    - `5e 24 7a cb` is the IP address, which decodes to `94.36.122.203` in dotted-decimal notation.

#### Security Failure
#### Media Failure
#### Data Failure

### Tools of the trade

#### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) is command-line networking utility for reading from and writing to network connections using TCP or UDP. It is tipically available as the `nc` command.

#### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) is a command-line data-network packet analyzer.

Common commands:

- capture UDP packets to and from port 19302, print hexdump of the packet content:

    `sudo tcpdump 'udp port 19302' -xx`

- same but save packets in PCAP (packet capture) file for later inspection

    `sudo tcpdump 'udp port 19302' -w stun.pcap`

  the PCAP file can be opened with the wireshark GUI: `wireshark stun.pcap`

#### wireshark
#### webrtc-internals

Chrome comes with a built-in WebRTC statistics page available at [chrome://webrtc-internals](chrome://webrtc-internals).

## Latency

How do you know you have high latency? 

You may have noticed that your video is lagging, but do you know precisely how much it is lagging? 
To be able to reduce this latency, you have to start by measuring it first.

True latency is supposed to be measured end-to-end. 

That means not just the latency of the network path between the sender and the receiver, but the combined latency of camera capture, frame encoding, transmission, receiving, decoding and displaying, as well as possible queueing between any of these steps.

End-to-end latency is not a simple sum of latencies of each component.

While you could theoretically measure the latency of the components of a live video transmission pipeline separately and then add them together, in practice, at least some components will be either inaccessible for instrumentation, or produce significantly different results when measured outside of the pipeline.
Variable queue depths between pipeline stages, network topology and camera exposure changes are just a few examples of components affecting end-to-end latency.

The intrinsic latency of each component in your live streaming system can change and affect downstream components.
Even the content of captured video affects latency. 
For example, many more bits are required for high frequency features such as tree branches, compared to a low frequency clear blue sky.
A camera with auto exposure turned on may take _much_ longer than the expected 33 milliseconds to capture a frame, even if when the capture rate is set to 30 frames per second.
Transmission over the network, especially so cellular, is also very dynamic due to changing demand. 
More users introduce more chatter on the air. 
Your physical location (notorious low signal zones) and multiple other factors increase packet loss and latency.
What happens when you send a packet to a network interface, say wifi adapter or an LTE modem for delivery?
If it can not be immediately delivered it is queued on the interface, the larger the queue the more latency such network interface introduces.

### Manual end-to-end latency measurement
When we talk about end-to-end latency, we mean the time between an event happening and it being observed - video frames appearing on the screen.
```
EndToEndLatency = T(observe) - T(happen)
```
A naive approach is to record time at event happening and subtract it from the time at observation.
However as precision goes down to milliseconds time synchronization becomes an issue.
Trying to synchronize clocks across distributed systems is mostly futile, even a small error in time sync produces unreliable latency measurement.

A simple workaround for clock sync issues is to use the same clock.
Put sender and receiver in the same frame of reference.

Imagine you have a ticking millisecond clock or any other event source really.
You want to measure latency in a system that live streams the clock to a remote screen by pointing a camera at it.
An obvious way to measure time between the millisecond timer ticking (T<sub>`happen`</sub>) and video frames of the clock appear on screen (T<sub>`observe`</sub>) is the following:
- Point your camera at the millisecond clock.
- Send video frames to a receiver that is in the same physical location.
- Take a picture (use your phone) of the millisecond timer and the received video on screen.
- Subtract two times.
That is the most true-to-yourself end-to-end latency measurement.
It accounts for all components latencies (camera, encoder, network, decoder) and does not rely on any clock synchronization.

![DIY Latency](../images/09-diy-latency.png "DIY Latency Measurement").
![DIY Latency Example](../images/09-diy-latency-happen-observe.png "DIY Latency Measurement Example")
In the photo above measured end-to-end latency is 101 msec. Event happening right now is 10:16:02.862 but live streaming system observer sees 10:16:02.761. 

### Automatic end-to-end latency measurement
#### Example latency estimation
#### Actual video time in browser
### Latency Debugging Tips
#### Camera latency
#### Encoder latency
#### Network latency
#### Receiver side latency
