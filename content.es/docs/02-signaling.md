---
title: Señalización
type: docs
weight: 3
---

# Señalización

## ¿Qué es la Señalización de WebRTC?

Cuando creas un agente WebRTC, no sabe nada sobre el otro par. ¡No tiene idea de con quién se va a conectar o qué van a enviar!
La señalización es el proceso inicial de arranque que hace posible una llamada. Después de que estos valores se intercambian, los agentes WebRTC pueden comunicarse directamente entre sí.

Los mensajes de señalización son simplemente texto. A los agentes WebRTC no les importa cómo se transportan. Comúnmente se comparten a través de Websockets, pero eso no es un requisito.

## ¿Cómo funciona la señalización de WebRTC?

WebRTC utiliza un protocolo existente llamado Protocolo de Descripción de Sesión (Session Description Protocol). A través de este protocolo, los dos agentes WebRTC compartirán todo el estado requerido para establecer una conexión. El protocolo en sí es simple de leer y entender.
La complejidad proviene de comprender todos los valores con los que WebRTC lo completa.

Este protocolo no es específico de WebRTC. Primero aprenderemos el Protocolo de Descripción de Sesión sin siquiera hablar de WebRTC. WebRTC realmente solo aprovecha un subconjunto del protocolo, por lo que solo vamos a cubrir lo que necesitamos.
Después de que entendamos el protocolo, pasaremos a su uso aplicado en WebRTC.

## ¿Qué es el *Protocolo de Descripción de Sesión* (SDP)?
El Protocolo de Descripción de Sesión está definido en [RFC 8866](https://tools.ietf.org/html/rfc8866). Es un protocolo de clave/valor con una nueva línea después de cada valor. Se sentirá similar a un archivo INI.
Una Descripción de Sesión contiene cero o más Descripciones de Medios. Mentalmente puedes modelarlo como una Descripción de Sesión que contiene un array de Descripciones de Medios.

Una Descripción de Medios generalmente se mapea a un solo flujo de medios. Así que si quisieras describir una llamada con tres flujos de video y dos pistas de audio tendrías cinco Descripciones de Medios.

### Cómo leer el SDP
Cada línea en una Descripción de Sesión comenzará con un solo carácter, esta es tu clave. Luego será seguida por un signo igual. Todo después de ese signo igual es el valor. Después de que el valor esté completo, tendrás una nueva línea.

El Protocolo de Descripción de Sesión define todas las claves que son válidas. Solo puedes usar letras para claves como se define en el protocolo. Estas claves tienen un significado importante, que se explicará más adelante.

Toma este extracto de Descripción de Sesión:

```
a=my-sdp-value
a=second-value
```

Tienes dos líneas. Cada una con la clave `a`. La primera línea tiene el valor `my-sdp-value`, la segunda línea tiene el valor `second-value`.

### WebRTC solo usa algunas claves SDP
No todos los valores de clave definidos por el Protocolo de Descripción de Sesión son utilizados por WebRTC. Solo las claves usadas en el Protocolo de Establecimiento de Sesión de JavaScript (JSEP), definido en [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829), son importantes. Las siguientes siete claves son las únicas que necesitas entender ahora mismo:

* `v` - Versión, debería ser igual a `0`.
* `o` - Origen, contiene un ID único útil para renegociaciones.
* `s` - Nombre de Sesión, debería ser igual a `-`.
* `t` - Temporización, debería ser igual a `0 0`.
* `m` - Descripción de Medios (`m=<media> <port> <proto> <fmt> ...`), descrito en detalle más abajo.
* `a` - Atributo, un campo de texto libre. Esta es la línea más común en WebRTC.
* `c` - Datos de Conexión, debería ser igual a `IN IP4 0.0.0.0`.

### Descripciones de Medios en una Descripción de Sesión

Una Descripción de Sesión puede contener un número ilimitado de Descripciones de Medios.

Una definición de Descripción de Medios contiene una lista de formatos. Estos formatos se mapean a Tipos de Carga Útil RTP. El códec real se define luego por un Atributo con el valor `rtpmap` en la Descripción de Medios.
La importancia de RTP y los Tipos de Carga Útil RTP se discute más adelante en el capítulo de Medios. Cada Descripción de Medios puede contener un número ilimitado de atributos.

Toma este extracto de Descripción de Sesión como ejemplo:

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

Tienes dos Descripciones de Medios, una de tipo audio con fmt `111` y una de tipo video con el formato `96`. La primera Descripción de Medios tiene solo un atributo. Este atributo mapea el Tipo de Carga Útil `111` a Opus.
La segunda Descripción de Medios tiene dos atributos. El primer atributo mapea el Tipo de Carga Útil `96` a VP8, y el segundo atributo es solo `my-sdp-value`.

### Ejemplo Completo

Lo siguiente reúne todos los conceptos de los que hemos hablado. Estas son todas las características del Protocolo de Descripción de Sesión que WebRTC utiliza.
¡Si puedes leer esto, puedes leer cualquier Descripción de Sesión de WebRTC!

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

* `v`, `o`, `s`, `c`, `t` están definidos, pero no afectan la sesión WebRTC.
* Tienes dos Descripciones de Medios. Una de tipo `audio` y una de tipo `video`.
* Cada una de esas tiene un atributo. Este atributo configura detalles del pipeline RTP, que se discute en el capítulo "Comunicación de Medios".

## Cómo funcionan juntos el *Protocolo de Descripción de Sesión* y WebRTC

La siguiente pieza del rompecabezas es entender _cómo_ WebRTC usa el Protocolo de Descripción de Sesión.

### ¿Qué son las Ofertas y Respuestas?

WebRTC usa un modelo de oferta/respuesta. Todo esto significa que un agente WebRTC hace una "Oferta" para iniciar una llamada, y el otro agente WebRTC "Responde" si está dispuesto a aceptar lo que se ha ofrecido.

Esto le da al que responde la oportunidad de rechazar códecs no soportados en las Descripciones de Medios. Así es como dos pares pueden entender qué formatos están dispuestos a intercambiar.

### Los Transceivers son para enviar y recibir

Transceivers es un concepto específico de WebRTC que verás en la API. Lo que está haciendo es exponer la "Descripción de Medios" a la API de JavaScript. Cada Descripción de Medios se convierte en un Transceiver.
Cada vez que creas un Transceiver se agrega una nueva Descripción de Medios a la Descripción de Sesión local.

Cada Descripción de Medios en WebRTC tendrá un atributo de dirección. Esto permite que un agente WebRTC declare "Voy a enviarte este códec, pero no estoy dispuesto a aceptar nada de vuelta". Hay cuatro valores válidos:

* `send`
* `recv`
* `sendrecv`
* `inactive`

### Valores SDP utilizados por WebRTC

Esta es una lista de algunos atributos comunes que verás en una Descripción de Sesión de un agente WebRTC. Muchos de estos valores controlan los subsistemas que aún no hemos discutido.

#### `group:BUNDLE`
El empaquetamiento (Bundling) es el acto de ejecutar múltiples tipos de tráfico sobre una conexión. Algunas implementaciones de WebRTC usan una conexión dedicada por flujo de medios. El empaquetamiento debería ser preferido.

#### `fingerprint:sha-256`
Este es un hash del certificado que un par está usando para DTLS. Después de que se completa el handshake DTLS, comparas esto con el certificado real para confirmar que te estás comunicando con quien esperas.

#### `setup:`
Esto controla el comportamiento del agente DTLS. Esto determina si se ejecuta como un cliente o servidor después de que ICE se haya conectado. Los valores posibles son:

* `setup:active` - Ejecutar como Cliente DTLS.
* `setup:passive` - Ejecutar como Servidor DTLS.
* `setup:actpass` - Pedir al otro agente WebRTC que elija.

#### `mid`
El atributo "mid" se usa para identificar flujos de medios dentro de una descripción de sesión.

#### `ice-ufrag`
Este es el valor de fragmento de usuario para el agente ICE. Usado para la autenticación del tráfico ICE.

#### `ice-pwd`
Esta es la contraseña para el agente ICE. Usado para la autenticación del tráfico ICE.

#### `rtpmap`
Este valor se usa para mapear un códec específico a un Tipo de Carga Útil RTP. Los tipos de carga útil no son estáticos, así que para cada llamada el oferente decide los tipos de carga útil para cada códec.

#### `fmtp`
Define valores adicionales para un Tipo de Carga Útil. Esto es útil para comunicar un perfil de video específico o configuración de codificador.

#### `candidate`
Este es un Candidato ICE que proviene del agente ICE. Esta es una posible dirección en la que el agente WebRTC está disponible. Estos se explican completamente en el siguiente capítulo.

#### `ssrc`
Una Fuente de Sincronización (SSRC) define una única pista de flujo de medios.

`label` es el ID para este flujo individual. `mslabel` es el ID para un contenedor que puede tener múltiples flujos dentro de él.

### Ejemplo de una Descripción de Sesión de WebRTC
Lo siguiente es una Descripción de Sesión completa generada por un cliente WebRTC:

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

Esto es lo que sabemos de este mensaje:

* Tenemos dos secciones de medios, una de audio y una de video.
* Ambas son transceivers `sendrecv`. Estamos recibiendo dos flujos, y podemos enviar dos de vuelta.
* Tenemos Candidatos ICE y detalles de Autenticación, así que podemos intentar conectarnos.
* Tenemos una huella digital de certificado, así que podemos tener una llamada segura.

### Temas Adicionales
En versiones posteriores de este libro, también se abordarán los siguientes temas:

* Renegociación
* Simulcast
