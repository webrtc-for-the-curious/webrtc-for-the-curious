---
title: ¿Qué, Por qué y Cómo?
type: docs
weight: 2
---

# ¿Qué, Por qué y Cómo?

## ¿Qué es WebRTC?

WebRTC, es la abreviatura de Web Real-Time Communication, es una API como un Protocolo. El protocolo WebRTC es un conjunto de reglas para que dos agentes WebRTC
negocien una comunicación bidireccional segura en tiempo real. Mientras que la WebRTC API permite a los desarrolladores usar el protocolo WebRTC.
La WebRTC API es solo para JavaScript.

Una relación similar sería entre HTTP y la Fetch API. El protocolo WebRTC sería HTTP, y la WebRTC API sería la Fetch API.

El protocolo WebRTC está disponible en otros lenguajes además de JavaScript. Puedes encontrar servidores y herramientas de dominio específico para WebRTC.
Todas estas implementaciones usan el protocolo WebRTC, así que pueden interactuar entre ellos.

El protocolo WebRTC es mantenido en el IETF (Grupo de Trabajo de Ingeniería de Internet) en el grupo de trabajo [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents).
La WebRTC API es documentada en [W3C](https://www.w3.org/TR/webrtc).

## ¿Por qué debería aprender WebRTC?

Estas son algunas cosas que WebRTC te proporcionará:

* Estándar abierto
* Implementaciones Múltiples
* Disponibilidad en navegadores web
* Cifrado obligatorio
* NAT transversal
* Reuso de tecnología existente
* Control de congestión
* Latencia de menos de un segundo

Esta lista no es exhaustiva, solo un ejemplo de algunas de las cosas que podrás apreciar durante el recorrido. No te preocupes si no sabes todos estos términos aún,
este libro te enseñará su significado con el tiempo.

## El protocolo WebRTC es una colección de otras tecnologías

El protocolo WebRTC es un tema inmenso que tomaría un libro entero para explicarlo. Sin embargo, para empezar lo dividiremos en cuatro pasos.

1. Señalización (Signaling)
2. Conexión (Connecting)
3. Asegurar (Securing)
4. Comunicando (Communication)

Estos pasos son secuenciales, lo que significa que el paso anterior debe haber sido entendido al 100% para dar comienzo con el siguiente paso.

Un hecho peculiar de WebRTC es que cada uno de los pasos ¡está hecho de muchos otros protocolos! Para crear WebRTC, nosotros juntamos varias tecnologías ya existentes.
En ese sentido, puedes pensar en WebRTC como una combinación y configuración de tecnología bien entendida, que se remonta a principios de la década del 2000
que como un proceso completamente nuevo por derecho propio.

Cada uno de estos pasos tiene un capítulo dedicado, pero ayuda mucho el primero entenderlos a un alto nivel. Ya que dependen del uno al otro, ayudará cuando se explique más el propósito
de cada uno de estos pasos.

### Señalización: ¿Cómo se encuentran los usuarios entre ellos en WebRTC?

Cuando un agente de WebRTC es iniciado, no tiene ni idea de con quién se va a comunicar o que es lo que van a comunicar. ¡La *Señalización* resuelve este problema!
La señalización es usada para arrancar la llamada, permitiendo dos agentes independientes de WebRTC empezar a comunicarse.

Signaling uses an existing, plain-text protocol called SDP (Session Description Protocol). Each SDP message is made up of key/value pairs and contains a list of "media sections". The SDP that the two WebRTC Agents exchange contains details like:

* The IPs and Ports that the agent is reachable on (candidates).
* The number of audio and video tracks the agent wishes to send.
* The audio and video codecs each agent supports.
* The values used while connecting (`uFrag`/`uPwd`).
* The values used while securing (certificate fingerprint).

It is important to note that signaling typically happens "out-of-band", which means applications generally don't use WebRTC itself to exchange signaling messages. Any architecture suitable for sending messages can relay the SDPs between the connecting peers, and many applications will simply use their existing infrastructure (e.g. REST endpoints, WebSocket connections, or authentication proxies) to facilitate trading of SDPs between the proper clients.

### Connecting and NAT Traversal with STUN/TURN

Once two WebRTC Agents have exchanged SDPs, they have enough information to attempt to connect to each other. To make this connection happen, WebRTC uses another established technology called ICE (Interactive Connectivity Establishment).

ICE is a protocol that pre-dates WebRTC and allows the establishment of a direct connection between two Agents without a central server. These two Agents could be on the same network or on the other side of the world.

ICE enables direct connection, but the real magic of the connecting process involves a concept called 'NAT Traversal' and the use of STUN/TURN Servers. These two concepts, which we will explore in more depth later, are all you need to communicate with an ICE Agent in another subnet.

Once two Agents have successfully established an ICE connection, WebRTC moves on to the next step: establishing an encrypted transport for sharing audio, video, and data between them.

### Securing the transport layer with DTLS and SRTP

Now that we have bi-directional communication (via ICE), we need to make our communication secure! This is done through two more protocols that also pre-date WebRTC; DTLS (Datagram Transport Layer Security) and SRTP (Secure Real-Time Transport Protocol). The first protocol, DTLS, is simply TLS over UDP (TLS is the cryptographic protocol used to secure communication over HTTPS). The second protocol, SRTP (Secure Real-time Transport Protocol), is used to ensure encryption of RTP (Real-time Protocol) data packets.

First, WebRTC connects by doing a DTLS handshake over the connection established by ICE. Unlike HTTPS, WebRTC doesn't use a central authority for certificates. It simply asserts that the certificate exchanged via DTLS matches the fingerprint shared via signaling. This DTLS connection is then used for DataChannel messages.

Next, WebRTC uses the RTP protocol, secured using SRTP, for audio/video transmission. We initialize our SRTP session by extracting the keys from the negotiated DTLS session.

We will discuss why media and data transmission have their own protocols in a later chapter, but for now it is enough to know that they are handled separately.

Now we are done! We have successfully established bi-directional and secure communication. If you have a stable connection between your WebRTC Agents, this is all the complexity you need. In the next section, we will discuss how WebRTC deals with the unfortunate real world problems of packet loss and bandwidth limits.

### Communicating with peers via RTP and SCTP

Now that we have two WebRTC Agents connected and secure, bi-directional communication established, let's start communicating! Again, WebRTC will use two pre-existing protocols: RTP (Real-time Transport Protocol), and SCTP (Stream Control Transmission Protocol). We use RTP to exchange media encrypted with SRTP, and we use SCTP to send and receive DataChannel messages encrypted with DTLS.

RTP is quite a minimal protocol, but it provides the necessary tools to implement real-time streaming. The most important thing about RTP is that it gives flexibility to the developer, allowing them to handle latency, package loss, and congestion as they please. We will discuss this further in the media chapter.

The final protocol in the stack is SCTP. The important thing about SCTP is that it allows for unreliable, out of order message delivery (among many different options). This allows developers to ensure the necessary latency for real-time systems.

## WebRTC, a collection of protocols
WebRTC solves a lot of problems. At first glance the technology may seem over-engineered, but the genius of WebRTC is its humility. It wasn't created under the assumption that it could solve everything better. Instead, it embraced many existing single purpose technologies and brought them together into a streamlined, widely applicable bundle.

This allows us to examine and learn each part individually without being overwhelmed. A good way to visualize it is a 'WebRTC Agent' is really just an orchestrator of many different protocols.

![WebRTC Agent](../images/01-webrtc-agent.png "WebRTC Agent Diagram")

## How does WebRTC (the API) work?

This section outlines how the WebRTC JavaScript API maps to the WebRTC protocol described above. It isn't meant as an extensive demo of the WebRTC API, but more to create a mental model of how everything ties together.
If you aren't familiar with either the protocol or the API, don't worry. This could be a fun section to return to as you learn more!

### `new RTCPeerConnection`

The `RTCPeerConnection` is the top-level "WebRTC Session". It contains all the protocols mentioned above. The subsystems are all allocated but nothing happens yet.

### `addTrack`

`addTrack` creates a new RTP stream. A random Synchronization Source (SSRC) will be generated for this stream. This stream will then be inside the Session Description generated by `createOffer` inside a media section. Each call to `addTrack` will create a new SSRC and media section.

Immediately after an SRTP Session is established, these media packets will start being encrpyted using SRTP and sent via ICE.

### `createDataChannel`

`createDataChannel` creates a new SCTP stream if no SCTP association exists. SCTP is not enabled by default.  It is only started when one side requests a data channel.

Immediately after a DTLS Session is established, the SCTP association will start sending packets encrypted with DTLS via ICE.

### `createOffer`

`createOffer` generates a Session Description of the local state to be shared with the remote peer.

The act of calling `createOffer` doesn't change anything for the local peer.

### `setLocalDescription`

`setLocalDescription` commits any requested changes. The calls `addTrack`, `createDataChannel`, and similar calls are temporary until this call. `setLocalDescription` is called with the value generated by `createOffer`.

Usually, after this call, you will send the offer to the remote peer, who will use it to call `setRemoteDescription`.

### `setRemoteDescription`

`setRemoteDescription` is how we inform the local agent about the state of the remote candidates'. This is how the act of 'Signaling' is done with the JavaScript API.

When `setRemoteDescription` has been called on both sides, the WebRTC Agents now have enough info to start communicating Peer-To-Peer (P2P)!

### `addIceCandidate`

`addIceCandidate` allows a WebRTC agent to add more remote ICE Candidates at any time. This API sends the ICE Candidate right into the ICE subsystem and has no other effect on the greater WebRTC connection.

### `ontrack`

`ontrack` is a callback fired when an RTP packet is received from the remote peer. The incoming packets would have been declared in the Session Description that was passed to `setRemoteDescription`.

WebRTC uses the SSRC and looks up the associated `MediaStream` and `MediaStreamTrack`, and fires this callback with these details populated.

### `oniceconnectionstatechange`

`oniceconnectionstatechange` is a callback that is fired which reflects a change in the state of an ICE Agent. When you have a change in network connectivity this is how you are notified.
### `onconnectionstatechange`

`onconnectionstatechange` is a combination of ICE Agent and DTLS Agent state. You can watch this to be notified when ICE and DTLS have both completed successfully.
