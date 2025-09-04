---
title: 무엇, 왜, 어떻게?
type: docs
weight: 2
---

# 무엇, 왜, 어떻게?

## WebRTC란 무엇인가?

WebRTC(Web Real-Time Communication)는 API이자 프로토콜입니다. WebRTC 프로토콜은 두 WebRTC 에이전트가
실시간 양방향 안전 통신을 협상하기 위한 규칙 집합입니다. WebRTC API는 개발자가 이 WebRTC 프로토콜을 사용할 수 있게 합니다.
WebRTC API는 JavaScript를 대상으로 합니다.

HTTP와 Fetch API의 관계에 비유할 수 있습니다. WebRTC 프로토콜이 HTTP라면, WebRTC API는 Fetch API에 해당합니다.

WebRTC 프로토콜은 JavaScript 외의 언어로도 구현되어 있습니다. 서버와 도메인 특화 도구들도 존재합니다.
이 모든 구현은 WebRTC 프로토콜을 사용하므로 상호 운용이 가능합니다.

WebRTC 프로토콜은 IETF(Internet Engineering Task Force)의 [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents) 작업 그룹에서 관리되며,
WebRTC API는 [W3C](https://www.w3.org/TR/webrtc)에 문서화되어 있습니다.

## 왜 WebRTC를 배워야 하나요?

WebRTC는 다음과 같은 이점을 제공합니다.

* 개방형 표준
* 다중 구현체
* 웹 브라우저 지원
* 의무적 암호화
* NAT 우회
* 기존 기술 재사용
* 혼잡 제어
* 1초 미만 지연

이 목록은 전부가 아니라 예시에 불과합니다. 아직 익숙하지 않은 용어가 있더라도 걱정하지 마세요.
이 책을 읽는 동안 자연스럽게 의미를 배우게 됩니다.

## WebRTC 프로토콜은 여러 기술의 집합

WebRTC 프로토콜은 방대하여 책 한 권이 필요할 주제입니다. 시작을 위해 네 단계로 나누어 보겠습니다.

1. 시그널링(Signaling)
2. 연결(Connecting)
3. 보안(Securing)
4. 통신(Communication)

이 단계들은 순차적입니다. 앞 단계를 충분히 이해해야 다음 단계로 넘어갈 수 있습니다.

WebRTC의 흥미로운 점은 각 단계가 다시 많은 프로토콜로 이루어져 있다는 것입니다! WebRTC는 이미 존재하는 다양한 기술을 조합해 만듭니다.
즉, WebRTC는 완전히 새로운 발명이라기보다 2000년대 초반부터 잘 이해된 기술들의 조합과 구성으로 볼 수 있습니다.

각 단계는 별도 장에서 자세히 다루지만, 먼저 높은 수준에서 개념을 잡아두면 도움이 됩니다. 단계들이 서로 의존하므로,
각 단계의 목적을 염두에 두면 세부 설명을 이해하기 쉬워집니다.

### 시그널링: WebRTC에서 단말들은 어떻게 서로를 찾을까?

WebRTC 에이전트는 시작 시점에 누구와 무엇을 통신할지 알지 못합니다. 바로 이 문제를 시그널링이 해결합니다!
시그널링은 두 독립적인 WebRTC 에이전트가 통신을 시작할 수 있도록 호출을 개시합니다.

시그널링에는 SDP(Session Description Protocol)라는 평문 텍스트 프로토콜을 사용합니다. 각 SDP 메시지는 키-값으로 이뤄지며,
여러 개의 “미디어 섹션”을 포함합니다. 두 WebRTC 에이전트가 교환하는 SDP에는 다음과 같은 정보가 들어갑니다.

* 에이전트가 접근 가능한 IP와 포트(ICE 후보)
* 전송하려는 오디오/비디오 트랙의 개수
* 각 에이전트가 지원하는 오디오/비디오 코덱
* 연결 과정에서 사용하는 값들(`uFrag`/`uPwd`)
* 보안 설정에 사용하는 값(인증서 지문)

중요한 점은, 시그널링은 대개 “대역 외(out-of-band)”로 이뤄진다는 것입니다. 즉, 애플리케이션은 보통 WebRTC 자체가 아닌
적절한 메시징 수단을 사용해 시그널링 메시지를 교환합니다. SDPs를 주고받기 위해 적합한 어떤 아키텍처도 사용할 수 있으며
많은 애플리케이션은 기존 인프라(예: REST API, WebSocket 연결, 인증 프록시 서버 등)를 그대로 활용합니다.

### 연결과 NAT 우회: STUN/TURN

두 WebRTC 에이전트가 SDP를 교환하면 서로 연결을 시도할 수 있을 만큼의 정보를 갖추게 됩니다. 이를 위해 WebRTC는
ICE(Interactive Connectivity Establishment)라는 확립된 기술을 사용합니다.

ICE는 WebRTC보다 오래된 프로토콜로, 중앙 서버 없이 두 에이전트 간 직접 연결을 수립할 수 있게 해 줍니다.
두 에이전트는 같은 네트워크에 있을 수도, 지구 반대편에 있을 수도 있습니다.

ICE는 직접 연결을 가능하게 하지만, 진정한 마법은 ‘NAT 우회’와 STUN/TURN 서버의 사용에 있습니다.
이 두 개념은 다른 서브넷에 있는 ICE 에이전트와 통신하기 위해 필요한 모든 것입니다. 자세한 내용은 뒤에서 다룹니다.

연결이 성립되면 두 에이전트는 미디어와 데이터 전송을 위한 기반을 얻게 됩니다. 이 과정 전반은 연결성 검사, 후보 수집과 우선순위화,
그리고 최종 후보 쌍 선정 등으로 구성됩니다.

### 보안: 어떻게 안전하게 만들까?

연결이 수립된 뒤에는 보안이 중요합니다. WebRTC는 DTLS를 통해 키 교환과 상호 인증을 수행하고, SRTP로 미디어를 암호화합니다.
데이터 채널은 DTLS 위의 SCTP를 통해 보호됩니다. 이렇게 해서 전송 중 콘텐츠가 도청되거나 변조되는 것을 방지합니다.

### 통신: 무엇을 어떻게 주고받을까?

보안 채널이 준비되면 실제 통신이 시작됩니다. 미디어는 RTP/SRTP로, 데이터는 SCTP(DataChannel)로 전송됩니다.
코덱, 전송률 제어, 패킷 손실 대응, 지터 버퍼 등 실시간 전송 품질을 좌우하는 요소들이 여기에 포함됩니다.

![WebRTC 에이전트](../images/01-webrtc-agent.png "Diagrama de Agente WebRTC")

## WebRTC API는 어떻게 동작하나?

이 절은 앞서 설명한 WebRTC 프로토콜이 JavaScript API와 어떻게 대응되는지 설명합니다. API의 모든 기능을 다루는
광범위한 데모가 아니라, 전체를 묶어 이해할 수 있는 사고 모델을 제시합니다.
프로토콜이나 API가 익숙하지 않다면 걱정하지 마세요. 더 배우고 돌아와도 좋습니다!

### `new RTCPeerConnection`

`RTCPeerConnection`은 최상위 수준의 ‘WebRTC 세션’입니다. 앞서 언급한 모든 하위 시스템을 포함하지만,
아직 이 시점에는 구체적인 동작이 일어나지 않습니다.

### `addTrack`

`addTrack`은 새로운 RTP 스트림을 만듭니다. 이 스트림에는 무작위 동기화 소스(SSRC)가 할당됩니다.
이 스트림은 `createOffer`가 생성하는 세션 설명의 미디어 섹션에 포함됩니다. `addTrack`을 호출할 때마다
새 미디어 섹션과 SSRC가 추가됩니다.

SRTP 세션이 성립되는 즉시, 이 미디어 패킷들은 SRTP로 암호화되어 ICE를 통해 전송됩니다.

### `createDataChannel`

`createDataChannel`은 기존에 SCTP 연결이 없다면 새로운 SCTP 연결을 만듭니다. SCTP는 기본적으로 활성화되어 있지 않으며,
한쪽에서 데이터 채널을 요청할 때 시작됩니다.

DTLS 세션이 수립되면, SCTP 연결은 DTLS로 암호화된 패킷을 ICE를 통해 전송하기 시작합니다.

### `createOffer`

`createOffer`는 원격 단말과 공유할 로컬 상태의 세션 설명을 생성합니다.

`createOffer` 자체는 로컬 단말의 상태를 바꾸지 않습니다.

### `setLocalDescription`

`setLocalDescription`은 요청된 변경을 확정합니다. `addTrack`, `createDataChannel` 등은 이 호출 전까지는 일시적인 상태이며,
보통 `createOffer`가 만든 값을 `setLocalDescription`에 전달합니다.

대개 이 다음 단계로, 생성된 오퍼를 원격 단말에 전송하고, 원격 단말은 이를 받아 `setRemoteDescription`을 호출합니다.

### `setRemoteDescription`

`setRemoteDescription`은 원격 후보의 상태를 로컬 에이전트에 알립니다. JavaScript API 관점에서 시그널링을 수행하는 단계입니다.

양쪽에서 `setRemoteDescription` 호출이 끝나면, 이제 WebRTC 에이전트들은 P2P 통신을 시작하기에 충분한 정보를 갖춘 것입니다!

### `addIceCandidate`

`addIceCandidate`는 언제든지 원격 ICE 후보를 추가할 수 있게 합니다. 이 API는 후보를 ICE 하위 시스템에 직접 전달하며,
그 외 WebRTC 연결 전반에는 영향을 주지 않습니다.

### `ontrack`

`ontrack`은 원격 단말에서 RTP 패킷을 수신했을 때 발생합니다. 들어오는 패킷은 `setRemoteDescription`에 전달된 세션 설명에
기재되어 있습니다.

WebRTC는 SSRC를 바탕으로 연결된 `MediaStream`과 `MediaStreamTrack`을 찾아, 이 정보를 담아 콜백을 호출합니다.

### `oniceconnectionstatechange`

`oniceconnectionstatechange`는 ICE 에이전트의 상태 변화가 있을 때 반영됩니다. 네트워크 연결성에 변화가 생기면 이를 통해 알림을 받습니다.

### `onconnectionstatechange`

`onconnectionstatechange`는 ICE와 DTLS 상태를 조합해 보여줍니다. ICE와 DTLS가 성공적으로 완료되었을 때 등을 확인할 수 있습니다.

