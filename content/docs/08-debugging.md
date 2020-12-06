---
title: Debugging
type: docs
weight: 9
---


# Debugging
Debugging WebRTC can be a daunting task. There are a lot of moving parts, and they all can break independently. If you aren't careful you can lose weeks of time looking at the wrong things. When you do finally find the part that is broken you will need to learn a bit to understand it.

This chapter will get you in the mindset to debug WebRTC. It will show you how to break down the problem. After we know the problem we will give a quick tour of the popular debugging tools.


### Isolate The Problem
When debugging you need to isolate where the issue is coming from. Start from the begining of t

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

    sudo tcpdump 'udp port 19302' -xx

- same but save packets in PCAP (packet capture) file for later inspection

    sudo tcpdump 'udp port 19302' -w stun.pcap

  the PCAP file can be opened with the wireshark GUI: `wireshark stun.pcap`

#### wireshark
#### webrtc-internals
