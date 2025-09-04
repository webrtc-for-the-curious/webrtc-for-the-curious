---
title: 시그널링
type: docs
weight: 3
---

# 시그널링

## WebRTC 시그널링이란?

WebRTC 에이전트를 생성했을 때, 상대 피어에 대해 아는 것은 없습니다. 누구와 연결할지, 무엇을 보낼지 전혀 모릅니다!
시그널링은 통화를 가능하게 만드는 초기 부트스트랩 단계입니다. 이 값들을 교환한 뒤에는 WebRTC 에이전트끼리 직접 통신할 수 있습니다.

시그널링 메시지는 단지 텍스트일 뿐입니다. WebRTC 에이전트는 어떤 전송 수단을 쓰는지 신경 쓰지 않습니다. 보통 WebSocket으로 주고받지만, 필수는 아닙니다.

## WebRTC 시그널링은 어떻게 동작하나?

WebRTC는 Session Description Protocol(SDP)이라는 기존 프로토콜을 사용합니다. 이 프로토콜을 통해 두 WebRTC 에이전트는
연결 수립에 필요한 모든 상태를 공유합니다. 프로토콜 자체는 읽고 이해하기 쉽습니다. 복잡함은 WebRTC가 채워 넣는 값들을 이해하는 데서 옵니다.

이 프로토콜은 WebRTC 전용이 아닙니다. 먼저 WebRTC와 무관하게 SDP를 학습합니다. WebRTC는 이 프로토콜의 일부만 사용하므로 필요한 부분만 다룹니다.
프로토콜을 이해한 다음, WebRTC에서의 실제 사용 방법을 살펴보겠습니다.

## Session Description Protocol(SDP)이란?
SDP는 [RFC 8866](https://tools.ietf.org/html/rfc8866)에 정의되어 있습니다. 각 줄이 키/값 형태이며, 값 뒤에 개행이 옵니다. INI 파일과 비슷한 느낌입니다.
세션 설명(Session Description)은 0개 이상의 미디어 설명(Media Description)을 포함합니다. 즉, 세션 설명은 미디어 설명의 배열로 모델링할 수 있습니다.

하나의 미디어 설명은 보통 하나의 미디어 스트림에 대응합니다. 예를 들어 비디오 3개와 오디오 2개로 이루어진 통화를 설명하려면 5개의 미디어 설명이 필요합니다.

### SDP 읽는 법
세션 설명의 모든 줄은 한 글자의 키로 시작합니다. 그 뒤에 등호가 오며, 등호 뒤가 값입니다. 값이 끝나면 개행으로 마무리합니다.

SDP는 사용할 수 있는 키를 정의합니다. 키는 알파벳 문자만 사용할 수 있으며 각 키는 중요한 의미를 갖습니다(뒤에서 설명).

다음은 SDP 일부 예시입니다.

```
a=my-sdp-value
a=second-value
```

두 줄이 있으며, 둘 다 키는 `a`입니다. 첫 줄의 값은 `my-sdp-value`, 둘째 줄의 값은 `second-value`입니다.

### WebRTC가 사용하는 SDP 키
SDP에 정의된 모든 키를 WebRTC가 사용하는 것은 아닙니다. [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829)에 정의된 JSEP(JavaScript Session Establishment Protocol)에서 사용하는 키만 중요합니다.
지금 이해해야 할 핵심 키는 다음 일곱 가지입니다.

* `v` - 버전, 항상 `0`이어야 합니다.
* `o` - 오리진, 재협상 시 유용한 고유 ID를 담습니다.
* `s` - 세션 이름, `-` 여야 합니다.
* `t` - 타이밍, `0 0` 여야 합니다.
* `m` - 미디어 설명(`m=<media> <port> <proto> <fmt> ...`), 아래에서 자세히 설명합니다.
* `a` - 속성(Attribute), 자유 텍스트 필드. WebRTC에서 가장 흔한 줄입니다.
* `c` - 연결 정보, `IN IP4 0.0.0.0`이어야 합니다.

### 세션 설명의 미디어 설명

하나의 세션 설명은 제한 없이 많은 미디어 설명을 담을 수 있습니다.

미디어 설명은 여러 포맷 목록을 포함하며, 각 포맷은 RTP Payload Type에 매핑됩니다. 실제 코덱은 미디어 설명 내부의 `rtpmap` 속성으로 정의합니다.
RTP와 Payload Type의 중요성은 미디어 장에서 자세히 다룹니다. 각 미디어 설명에는 제한 없이 많은 속성을 가질 수 있습니다.

다음 예시를 봅시다.

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

두 개의 미디어 설명이 있습니다. 오디오 타입의 `111` 포맷 하나, 비디오 타입의 `96` 포맷 하나입니다. 첫 번째 미디어 설명에는 하나의 속성이 있으며,
Payload Type `111`을 Opus에 매핑합니다. 두 번째 미디어 설명에는 두 개의 속성이 있으며, 첫 번째는 `96`을 VP8에 매핑하고 두 번째는 단순 속성 `my-sdp-value`입니다.

### 전체 예시

앞서 설명한 개념을 모두 합친 예시입니다. WebRTC가 사용하는 SDP의 모든 요소가 들어 있습니다. 이 예시를 읽을 수 있다면 어떤 WebRTC SDP든 읽을 수 있습니다!

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

* `v`, `o`, `s`, `c`, `t`는 정의되지만 WebRTC 세션 자체에는 영향을 주지 않습니다.
* `audio`와 `video` 두 개의 미디어 설명이 있습니다.
* 각 미디어 설명에는 하나의 속성이 있으며, 이는 RTP 파이프라인의 세부를 구성합니다(“미디어 통신” 장에서 설명).

## SDP와 WebRTC의 결합 방식

다음으로 WebRTC가 SDP를 ‘어떻게’ 사용하는지 이해해야 합니다.

### 오퍼와 앤서

WebRTC는 Offer/Answer 모델을 사용합니다. 한쪽 WebRTC 에이전트가 통화를 시작하겠다는 “오퍼(Offer)”를 제안하고, 상대 에이전트가 이를 수락하면 “앤서(Answer)”를 반환합니다.

이 과정에서 응답자는 미디어 설명에서 지원하지 않는 코덱을 거부할 수 있습니다. 이렇게 두 피어는 서로 교환 가능한 포맷을 합의합니다.

### 트랜시버: 송수신의 단위

트랜시버(Transceiver)는 API에서 보게 되는 WebRTC 고유 개념으로, 본질적으로 미디어 설명을 JavaScript API로 노출한 것입니다. 트랜시버를 만들 때마다
로컬 SDP에 새 미디어 설명이 추가됩니다.

WebRTC의 각 미디어 설명에는 방향 속성이 있습니다. 예를 들어 “나는 이 코덱을 보낼 수 있지만, 받지는 않겠다”와 같이 선언할 수 있습니다. 가능한 값은 다음 네 가지입니다.

* `send`
* `recv`
* `sendrecv`
* `inactive`

### WebRTC가 쓰는 SDP 값들

다음은 WebRTC 에이전트의 SDP에서 자주 보게 되는 속성들입니다. 많은 값은 아직 다루지 않은 하위 시스템을 제어합니다.

#### `group:BUNDLE`
번들은 여러 종류의 트래픽을 하나의 연결로 다루는 방식입니다. 일부 구현은 미디어 스트림마다 전용 연결을 사용하지만, 번들을 사용하는 것이 바람직합니다.

#### `fingerprint:sha-256`
DTLS에 사용하는 인증서의 해시입니다. DTLS 핸드셰이크가 끝나면 실제 인증서와 비교해 예상한 피어와 통신 중인지 확인합니다.

#### `setup:`
ICE 연결 이후 DTLS 에이전트의 동작(클라이언트/서버 역할)을 제어합니다. 가능한 값은 다음과 같습니다.

* `setup:active` - DTLS 클라이언트로 동작
* `setup:passive` - DTLS 서버로 동작
* `setup:actpass` - 상대 에이전트가 선택하도록 요청

#### `mid`
세션 설명 내에서 미디어 스트림을 식별하는 데 사용하는 값입니다.

#### `ice-ufrag`
ICE 에이전트의 user fragment 값으로, ICE 트래픽 인증에 사용됩니다.

#### `ice-pwd`
ICE 에이전트의 비밀번호로, ICE 트래픽 인증에 사용됩니다.

#### `rtpmap`
특정 코덱을 RTP Payload Type에 매핑합니다. Payload Type은 고정이 아니므로, 오퍼 측이 통화마다 코덱별 타입을 정합니다.

#### `fmtp`
특정 Payload Type의 추가 매개변수를 정의합니다. 예를 들어 특정 비디오 프로파일이나 인코더 설정을 전달할 때 유용합니다.

#### `candidate`
ICE 에이전트가 제공하는 ICE 후보입니다. WebRTC 에이전트가 사용 가능한 하나의 주소를 나타냅니다. 자세한 내용은 다음 장에서 다룹니다.

#### `ssrc`
SSRC(Synchronization Source)는 하나의 미디어 스트림 트랙을 정의합니다.

`label`은 개별 스트림의 ID이고, `mslabel`은 여러 스트림을 담을 수 있는 컨테이너 ID입니다.

### WebRTC 세션 설명 예시
다음은 WebRTC 클라이언트가 생성한 완전한 SDP입니다.

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

이 메시지로부터 알 수 있는 점은 다음과 같습니다.

* 오디오와 비디오, 두 개의 미디어 섹션이 있습니다.
* 둘 다 `sendrecv` 트랜시버입니다. 두 스트림을 받고, 두 스트림을 보낼 수 있습니다.
* ICE 후보와 인증 세부 정보가 있어 연결을 시도할 수 있습니다.
* 인증서 지문이 있어 안전한 통화를 설정할 수 있습니다.

### 추가 주제
이후 버전에서 다음 주제도 다룰 예정입니다.

* 재협상(Renegotiation)
* 시뮬캐스트(Simulcast)

