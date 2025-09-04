---
title: 데이터 통신
type: docs
weight: 8
---

# 데이터 통신

## WebRTC 데이터 통신으로 무엇을 할 수 있나요?

WebRTC는 데이터 채널을 제공합니다. 두 피어 사이에 최대 65,534개의 채널을 열 수 있습니다. 데이터 채널은 데이터그램 기반이며,
채널마다 내구성(재전송/시간 제한/순서 보장)을 독립적으로 설정할 수 있습니다. 기본은 보장된 순서 전달입니다.

미디어 관점에서 보면 데이터 채널은 과해 보일 수 있습니다. HTTP/WebSocket으로도 보낼 수 있지 않나? 하지만 데이터 채널의 힘은
무질서/손실 허용(UDP 유사) 동작으로 구성할 수 있다는 데 있습니다. 낮은 지연/고성능에 필수적이며, 백프레셔를 측정해 네트워크 용량을
넘지 않도록 보낼 수 있습니다.

## 어떻게 동작하나요?
WebRTC는 [RFC 4960](https://tools.ietf.org/html/rfc4960)의 SCTP(Stream Control Transmission Protocol)를 사용합니다. 원래 전송 계층용이지만,
WebRTC에서는 DTLS 위의 응용 계층 프로토콜로 사용합니다. SCTP는 ‘스트림’을 제공하며 각 스트림을 독립적으로 구성할 수 있습니다. 데이터 채널은
이에 대한 얇은 추상화로, 내구성/순서 옵션은 SCTP 에이전트에 그대로 전달됩니다.

또한 채널 라벨처럼 SCTP가 직접 표현하지 못하는 정보는 [RFC 8832](https://tools.ietf.org/html/rfc8832)의 DCEP(Data Channel Establishment Protocol)로
교환합니다.

## DCEP
DCEP에는 `DATA_CHANNEL_OPEN`과 `DATA_CHANNEL_ACK` 두 메시지만 있습니다. 채널을 열면 상대는 ACK로 응답해야 합니다.

### DATA_CHANNEL_OPEN
채널을 열고자 하는 에이전트가 전송합니다. 필드는 다음 의미를 갖습니다.

* Message Type: `0x03`
* Channel Type: 내구성/순서 속성
  - `RELIABLE`(`0x00`): 손실 없음, 순서 보장
  - `RELIABLE_UNORDERED`(`0x80`): 손실 없음, 무질서 허용
  - `PARTIAL_RELIABLE_REXMIT`(`0x01`): 제한 횟수 재전송 후 손실 허용, 순서 보장
  - `PARTIAL_RELIABLE_REXMIT_UNORDERED`(`0x81`): 위와 동일, 무질서 허용
  - `PARTIAL_RELIABLE_TIMED`(`0x02`): 제한 시간 내 도착하지 않으면 손실 허용, 순서 보장
  - `PARTIAL_RELIABLE_TIMED_UNORDERED`(`0x82`): 위와 동일, 무질서 허용
* Priority: 높은 우선순위가 먼저 스케줄됨
* Reliability Parameter: `REXMIT`(재전송 횟수) 또는 `TIMED`(재전송 시간, ms)
* Label: 채널 이름(UTF-8)
* Protocol: 비어 있지 않다면 [RFC 6455]의 WebSocket 서브프로토콜 레지스트리 값을 권장

### DATA_CHANNEL_ACK
원격이 채널 오픈을 수락했음을 알립니다.

## SCTP 핵심 개념

### 전송 시퀀스 번호(TSN)
모든 DATA 청크의 전역 고유 번호입니다. 손실/무질서 판단에 사용합니다.

### 스트림 식별자/시퀀스 번호
각 스트림에는 ID가 있고, 메시지 단위의 시퀀스 번호가 있습니다(`U=0`일 때 순서 판단에 사용).

### PPID(Payload Protocol Identifier)
전송 데이터의 타입을 나타냅니다. WebRTC는 `DCEP(50)`, `String(51)`, `Binary(53)`, `String Empty(56)`, `Binary Empty(57)`를 사용합니다.

## 주요 청크

### DATA
사용자 데이터 전달에 사용합니다. `U`(무질서), `B/E`(분할 메시지의 시작/끝), `TSN`, `Stream ID`, `Stream Seq`, `PPID` 등을 포함합니다.

### INIT
연결(Association) 생성 시작. 쿠키용 Initiate Tag, 수신 윈도 크기(a_rwnd), 송/수신 스트림 수, 초기 TSN, 선택 매개변수 등을 담습니다.

### SACK
수신 확인(Selective ACK). 누적 TSN ACK, 수신 윈도 크기, 갭 ACK 블록, 중복 TSN 등을 보고합니다.

### HEARTBEAT / ABORT / SHUTDOWN / ERROR
연결 상태 확인, 비정상 종료, 정상 종료, 비치명적 오류 보고 등에 사용됩니다.

### FORWARD TSN
더 이상 필요 없는 오래된 데이터 구간을 건너뛰도록 누적 TSN을 앞으로 당깁니다(실시간 무용 데이터 스킵).

## 상태 머신

### 연결 수립 흐름
`INIT`/`INIT ACK`로 능력/설정을 교환합니다. SCTP는 핸드셰이크 중 쿠키를 사용해 상대를 검증하고(DOS/MITM 방지), `COOKIE ECHO`/`COOKIE ACK`로
완료합니다. 이후 DATA 교환이 시작됩니다.

![Connection establishment](../images/07-connection-establishment.png "Connection establishment")

### 연결 종료 흐름
`SHUTDOWN`으로 우아한 종료를 시작합니다. 각 측은 마지막 전송 TSN을 공유해 데이터 손실 없이 종료합니다.

### Keep-Alive
`HEARTBEAT REQUEST/ACK`를 주기적으로 교환해 연결을 유지하고, 왕복 시간을 추정합니다.

