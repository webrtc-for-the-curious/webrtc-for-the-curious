---
title: ¿Qué, Por qué y Cómo?
type: docs
weight: 2
---

# ¿Qué, Por qué y Cómo?

## ¿Qué es WebRTC?

WebRTC, es la abreviatura de Web Real-Time Communication, es una API como un Protocolo. El protocolo WebRTC es un conjunto de reglas para que dos Agentes WebRTC
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
3. Seguridad (Securing)
4. Comunicación (Communication)

Estos pasos son secuenciales, lo que significa que el paso anterior debe haber sido entendido al 100% para dar comienzo con el siguiente paso.

Un hecho peculiar de WebRTC es que cada uno de los pasos ¡está hecho de muchos otros protocolos! Para crear WebRTC, nosotros juntamos varias tecnologías ya existentes.
En ese sentido, puedes pensar en WebRTC como una combinación y configuración de tecnología bien entendida, que se remonta a principios de la década del 2000
que como un proceso completamente nuevo por derecho propio.

Cada uno de estos pasos tiene un capítulo dedicado, pero ayuda mucho el primero entenderlos a un alto nivel. Ya que dependen del uno al otro, ayudará cuando se explique más el propósito
de cada uno de estos pasos.

### Señalización: ¿Cómo se encuentran los puntos de conexión entre ellos en WebRTC?

Cuando un agente de WebRTC es iniciado, no tiene ni idea de con quién se va a comunicar o que es lo que van a comunicar. ¡La *Señalización* resuelve este problema!
La señalización es usada para arrancar la llamada, permitiendo dos Agentes independientes de WebRTC empezar a comunicarse.

La señalización usa un protocolo de texto plano, llamado SDP (Protocolo de descripción de Sesión). Cada mensaje SDP está hecho de una llave y un valor,
y contiene una lista de "sección de medios". El SDP que intercambian los dos Agentes WebRTC contiene detalles como:

* Las IPs y Puertos que el agente es accesible (es candidato).
* El número de pistas de audio y vídeo que el agente desea mandar.
* Los códecs de audio y vídeo que cada agente soporta.
* Los valores usados mientras se conectaban (`uFrag`/`uPwd`).
* Los valores usados mientras se aseguraban (certificado de huella digital).

Es importante tener en cuenta que, la señalización típicamente pasa "fuera de banda", lo que significa, aplicaciones que generalmente no usan
WebRTC por si mismos para intercambiar mensajes de señalización. Cualquier arquitectura apropiada para mandar mensajes puede transmitir los SDPs
entre los puntos de conexión, y muchas aplicaciones simplemente usarán infraestructura existente (ej. REST API, conexiones WebSocket, o servidores proxy de autenticación)
para facilitar el comercio de SDPs entre los clientes apropiados.

### Conexión y NAT Transversal con STUN/TURN

Una vez, dos Agentes WebRTC han intercambiado SDPs, tendrán la información suficiente para intentar conectarse entre ellos. Para que esto pase,
WebRTC usa otra tecnología establecida llamada ICE (Establecimiento de Conectividad Interactiva).

ICE es un protocolo que es más antiguo que WebRTC y permite el establecimiento de una conexión directa entre dos Agentes sin un servidor central.
Estos dos Agentes podrían estar en la misma red o en la otra parte del mundo.

ICE permite conexiones directas, pero lo realmente mágico del proceso de conexión, implica un concepto llamado 'NAT Transversal' y el uso de servidores STUN/TURN.
Estos dos conceptos, los cuales los exploraremos con más detalle luego, son todo lo que se necesita para comunicarse con un Agente ICE en otra Subred.

Una vez, los dos Agentes han establecido una conexión ICE satisfactoriamente, WebRTC se mueve al siguiente paso: establecer un transporte cifrado para compartir
audio, vídeo y datos entre ellos.

### Asegurando la capa de transporte con DTLS y SRTP

Ahora que tenemos una comunicación bidireccional (vía ICE), ¡necesitamos hacer nuestra comunicación segura! Esto se hace mediante dos o más protocolos que
también son más antiguos que WebRTC; DTLS (Seguridad de la capa de transporte de datagramas) y SRTP (Protocolo de Transporte Seguro en Tiempo Real).
El primer protocolo, DTLS, es simplemente TSL sobre UDP (TLS es el protocolo de cifrado que se usa para asegurar una comunicación segura vía HTTP).
El segundo protocolo, SRTP, se utiliza para garantizar el cifrado de paquetes de datos RTP (Protocolo en Tiempo Real)

Primero, WebRTC se conecta haciendo uso de DTLS sobre la conexión establecida por ICE. Diferente a HTTPS, WebRTC no usa una autoridad central para certificados.
Simplemente afirma que el certificado intercambiado vía DTLS coincide con la huella digital, compartida por medio de la señalización. Esta conexión DTLS
se usa luego para los mensajes de DataChannel.

Después, WebRTC usa el protocolo RTP, asegurado usando SRTP, para la transmisión de audio/vídeo. Nosotros inicializamos nuestra sesión SRTP, extrayendo la llave
desde la sesión DTLS negociada.

Discutiremos por qué los medios y la transmisión de datos tienen sus propios protocolos en los siguientes capítulos, pero por ahora es suficiente para saber que se manejan
por separado.

¡Todo listo! Hemos establecido una comunicación bidireccional y segura exitosamente. Si tienes una conexión estable entre tus agentes WebRTC, esta es toda la complejidad que necesitas.
En la siguiente sección, hablaremos sobre como WebRTC trata con los desafortunados problemas del mundo real: la perdida de paquetes y los límites de banda ancha.

### Comunicándose con los puntos de conexión vía RTP y SCTP

Ahora que tenemos dos Agentes WebRTC conectados y asegurados y con una comunicación bidireccional establecida, ¡Vamos a comenzar a comunicarnos! Para esto, WebRTC usará dos protocolos
ya existentes: RTP (Protocolo de Transport de Tiempo Real), y SCTP (Protocolo de Transmisión de Control de Flujo). Usamos RTP para intercambiar multimedia cifrada con SRTP, y usamos
SCTP para mandar y recibir mensajes de DataChannel cifrados con DTLS.

RTP es casi un protocolo pequeño, pero provee las herramientas necesarias para implementar transmisión en tiempo real. Lo más importante acerca de RTP es que le da flexibilidad a el
desarrollador, permitiéndoles manejar la latencia, la perdida de paquetes, y la congestión como ellos gusten. Discutiremos acerca de esto en el capítulo de multimedia.

El protocolo final en el conjunto es SCTP. Lo importante acerca de este, es que permite la entrega de mensajes no confiables y fuera de servicio (entre muchas diferentes opciones). Esto
permite a los desarrolladores asegurar la latencia necesaria para sistemas de tiempo real.

## WebRTC, una colección de protocolos
WebRTC resuelve muchos problemas. A primera vista, la tecnología puede parecer sobre-diseñada, pero la genialidad de WebRTC es su humildad. No fue creado bajo la suposición de que podría
resolver todo mejor. En cambio, abarcó muchas tecnologías existentes de un solo propósito y las reunió en un paquete simplificado y ampliamente aplicable.

Esto nos permite examinar y aprender cada parte individualmente sin abrumarse. Una buena manera de visualizarlo es que un 'Agente WebRTC' es solamente un intermediario de muchos
protocolos diferentes.

![Agente WebRTC](../images/01-webrtc-agent.png "Diagrama de Agente WebRTC")

## ¿Cómo funciona WebRTC (la API)?

Esta sección describe como la API JavaScript de WebRTC se asigna al protocolo WebRTC descrito anteriormente. No pretende ser una demostración extensa de la API de WebRTC, pero si
crear un modelo mental de como todo se une.
Si no estás familiarizado con ningún protocolo o la API, no te preocupes. ¡Esta podría ser una sección divertida a la que regresar cuando aprendas más!

### `new RTCPeerConnection`

La `RTCPeerConnection` es la "Sesión WebRTC" de nivel superior. Esta contiene todos los protocolos mencionados anteriormente. Los subsistemas están asignados pero todavía no pasa nada.

### `addTrack`

`addTrack` crea un nuevo secuencia RTP. Una Fuente de Sincronización Aleatoria (SSRC) será generada para esta secuencia. Esta secuencia estará dentro de la Descripción de la Sesión,
generada por `createOffer` dentro de la sección de multimedia. Cada llamada a `addTrack` creará una nueva sección multimedia y SSRC.

Inmediatamente después de que una sesión SRTP es establecida, estos paquetes multimedia comenzarán a ser cifrados usando SRTP y enviados vía ICE.

### `createDataChannel`

`createDataChannel` crea una nueva secuencia SCTP si no existe ninguna asociación SCTP. SCTP no está activado por defecto. Solo se inicia cuando un lado solicita un canal de datos.

Inmediatamente después de que una sesión DTLS es establecida, la asociación SCTP comenzará a enviar paquetes cifrados con DTLS vía ICE.

### `createOffer`

`createOffer` genera una Descripción de la Sesión del estado local para ser compartido con el punto de conexión remoto.

El acto de llamar `createOffer` no cambia nada para el punto de conexión local.

### `setLocalDescription`

`setLocalDescription` confirma cualquier cambio de solicitud. Las llamadas a `addTrack`, `createDataChannel`, y similares, son temporales hasta esta convocatoria. `setLocalDescription`
es llamada con el valor generado por `createOffer`.

Usualmente, después de esta convocatoria, tu enviarás la oferta a el punto de conexión remoto, el cual lo usará para llamar a `setRemoteDescription`.

### `setRemoteDescription`

`setRemoteDescription` es la forma con la que informamos al agente local acerca del estado del candidato remoto. Asi es como se hace el acto de 'Señalización' con la API de JavaScript.

Cuando `setRemoteDescription` fue llamado en ambos lados, ¡los Agentes WebRTC ahora tienen la suficiente información para comenzar una comunicación Peer-To-Peer (P2P)!

### `addIceCandidate`

`addIceCandidate` permite a el agente WebRTC añadir más Candidatos remotos ICE en cualquier momento. Esta API envía el Candidato ICE directamente al subsistema ICE y no tiene ningún
otro efecto en la conexión WebRTC mayor.

### `ontrack`

`ontrack` es una llamada que se activa cuando se recibe un paquete RTP del punto de conexión remoto. Los paquetes entrantes habría sido declarado en la descripción de la sesión que se
pasó a `setRemoteDescription`.

WebRTC usa el SSRC y busca `MediaStream` y `MediaStreamTrack` asociados y activa esta llamada con estos detalles completados.

### `oniceconnectionstatechange`

`oniceconnectionstatechange` es una llamada que refleja un cambio en el estado de un agente ICE. Cuando tiene un cambio en la conectividad de la red, así es como se le notifica.

### `onconnectionstatechange`

`onconnectionstatechange` es una combinación de los estados de los agentes ICE y DTLS. Puedes ver esto para recibir una notificación cuando ICE y DTLS se hayan completado con éxito.
