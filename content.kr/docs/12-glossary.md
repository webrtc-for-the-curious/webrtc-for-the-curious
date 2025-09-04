---
title: 용어집
type: docs
weight: 13
---

# 용어집

* ACK: Acknowledgment(확인 응답)
* AVP: Audio and Video profile
* B-Frame: [양방향 예측 프레임](../06-media-communication/#intra-and-inter-frame-compression). 이전/이후 그림을 참고해 부분만 담는 프레임
* DCEP: [Data Channel Establishment Protocol](../07-data-communication/#dcep), [RFC 8832](https://datatracker.ietf.org/doc/html/rfc8832)
* DeMux: Demultiplexer(역다중화)
* DLSR: Delay since last sender report
* DTLS: [Datagram Transport Layer Security](../04-securing/#dtls), [RFC 6347](https://datatracker.ietf.org/doc/html/rfc6347)
* E2E: End-to-End(종단 간)
* FEC: [Forward Error Correction](../06-media-communication/#forward-error-correction)
* FIR: [Full INTRA-frame Request](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)
* G.711: 협대역 오디오 코덱
* GCC: [Google Congestion Control](../06-media-communication/#google-congestion-control-gcc), [draft-ietf-rmcat-gcc-02](https://datatracker.ietf.org/doc/html/draft-ietf-rmcat-gcc-02)
* H.264: 범용 오디오비주얼 인코딩 규격
* H.265: ITU-T H.265 고효율 비디오 코딩 적합성 규격
* HEVC: High Efficiency Video Coding
* HTTP: Hypertext Transfer Protocol
* HTTPS: TLS 위의 HTTP, [RFC 2818](https://datatracker.ietf.org/doc/html/rfc2818)
* I-Frame: [인트라 프레임](../06-media-communication/#intra-and-inter-frame-compression). 완전한 그림으로 단독 디코딩 가능
* ICE: [Interactive Connectivity Establishment](../03-connecting/#ice), [RFC 8445](https://datatracker.ietf.org/doc/html/rfc8445)
* INIT: Initiate
* IoT: Internet of Things(사물인터넷)
* IPv4: Internet Protocol, Version 4
* IPv6: Internet Protocol, Version 6
* ITU-T: International Telecommunication Union Telecommunication Standardization Sector
* JSEP: [JavaScript Session Establishment Protocol](../02-signaling/#what-is-the-session-description-protocol-sdp), [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829)
* MCU: [Multi-point Conferencing Unit](../08-applied-webrtc/#mcu)
* mDNS: [Multicast DNS](../03-connecting/#mdns), [RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762)
* MITM: Man-In-The-Middle(중간자)
* MTU: Maximum Transmission Unit, 패킷 최대 크기
* MUX: Multiplexing(다중화)
* NACK: Negative Acknowledgment
* NADA: [network-assisted dynamic adaptation](../06-media-communication/#bandwidth-estimation-alternatives), [draft-zhu-rmcat-nada-04](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04)
* NAT: [Network Address Translation](../03-connecting/#nat-mapping), [RFC 4787](https://datatracker.ietf.org/doc/html/rfc4787)
* Opus: 완전 개방형, 로열티 프리, 다목적 오디오 코덱
* P-Frame: [예측 프레임](../06-media-communication/#intra-and-inter-frame-compression). 이전 그림 대비 변경분만 포함
* P2P: Peer-to-Peer
* PLI: [Picture Loss Indication](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)
* PPID: [Payload Protocol Identifier](../07-data-communication/#payload-protocol-identifier)
* REMB: [Receiver Estimated Maximum Bitrate](../06-media-communication/#tmmbr-tmmbn-and-remb)
* RFC: Request for Comments
* RMCAT: [RTP Media Congestion Avoidance Techniques](../06-media-communication/#generating-a-bandwidth-estimate)
* RR: Receiver Report
* RTCP: [RTP Control Protocol](../10-history-of-webrtc/#rtp), [RFC 3550](https://datatracker.ietf.org/doc/html/rfc3550)
* RTP: [Real-time transport protocol](../10-history-of-webrtc/#rtp), [RFC 3550](https://datatracker.ietf.org/doc/html/rfc3550)
* RTT: Round-Trip Time(왕복 시간)
* SACK: Selective Acknowledgment
* SCReAM: [Self-Clocked Rate Adaptation for Multimedia](../06-media-communication/#bandwidth-estimation-alternatives), [draft-johansson-rmcat-scream-cc-05](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05)
* SCTP: [Stream Control Transmission Protocol](../07-data-communication/#stream-control-transmission-protocol), [RFC 4960](https://datatracker.ietf.org/doc/html/rfc4960)
* SDP: [Session Description Protocol](../02-signaling/#what-is-the-session-description-protocol-sdp), [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866)
* SFU: [Selective Forwarding Unit](../08-applied-webrtc/#selective-forwarding-unit)
* SR: Sender Report
* SRTP: [Secure Real-time Transport Protocol](../04-securing/#srtp), [RFC 3711](https://datatracker.ietf.org/doc/html/rfc3711)
* SSRC: Synchronization Source
* STUN: [Session Traversal Utilities for NAT](../03-connecting/#stun), [RFC 8489](https://datatracker.ietf.org/doc/html/rfc8489)
* TCP: Transmission Control Protocol
* TLS: Transport Layer Security, [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446)
* TMMBN: [Temporary Maximum Media Stream Bit Rate Notification](../06-media-communication/#tmmbr-tmmbn-and-remb)
* TMMBR: [Temporary Maximum Media Stream Bit Rate Request](../06-media-communication/#tmmbr-tmmbn-and-remb)
* TSN: [Transmission Sequence Number](../07-data-communication/#transmission-sequence-number)
* TURN: [Traversal Using Relays around NAT](../03-connecting/#turn), [RFC 8656](https://datatracker.ietf.org/doc/html/rfc8656)
* TWCC: [Transport Wide Congestion Control](../06-media-communication/#transport-wide-congestion-control)
* UDP: User Datagram Protocol
* VP8, VP9: WebM 프로젝트에서 개발한 고효율 비디오 코덱. 누구나 로열티 없이 사용 가능
* WebM: 웹을 위한 개방형 미디어 파일 포맷
* WebRTC: Web Real-Time Communications. [W3C WebRTC 1.0: Real-Time Communication Between Browsers](https://www.w3.org/TR/webrtc/)

