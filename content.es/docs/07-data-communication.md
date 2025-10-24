---
title: Comunicación de Datos
type: docs
weight: 8
---

# Comunicación de Datos

## ¿Qué obtengo de la comunicación de datos de WebRTC?

WebRTC proporciona canales de datos para la comunicación de datos. Entre dos pares puedes abrir 65,534 canales de datos.
Un canal de datos está basado en datagramas, y cada uno tiene su propia configuración de durabilidad. Por defecto, cada canal de datos tiene entrega ordenada garantizada.

Si te acercas a WebRTC desde un trasfondo de medios, los canales de datos pueden parecer derro chadores. ¿Por qué necesito todo este subsistema cuando podría simplemente usar HTTP o WebSockets?

El verdadero poder de los canales de datos es que puedes configurarlos para que se comporten como UDP con entrega desordenada/con pérdida.
Esto es necesario para situaciones de baja latencia y alto rendimiento. Puedes medir la contrapresión y asegurarte de que solo estás enviando tanto como tu red soporta.

## ¿Cómo funciona?
WebRTC usa el Protocolo de Transmisión de Control de Flujo (SCTP), definido en [RFC 4960](https://tools.ietf.org/html/rfc4960). SCTP es un
protocolo de capa de transporte que fue concebido como una alternativa a TCP o UDP. Para WebRTC lo usamos como un protocolo de capa de aplicación que se ejecuta sobre nuestra conexión DTLS.

SCTP te da flujos y cada flujo puede ser configurado independientemente. Los canales de datos de WebRTC son solo abstracciones delgadas sobre ellos. Las configuraciones
sobre durabilidad y ordenamiento se pasan directamente al Agente SCTP.

Los canales de datos tienen algunas características que SCTP no puede expresar, como etiquetas de canal. Para resolver eso, WebRTC usa el Protocolo de Establecimiento de Canal de Datos (DCEP)
que está definido en [RFC 8832](https://tools.ietf.org/html/rfc8832). DCEP define un mensaje para comunicar la etiqueta del canal y el protocolo.

## DCEP
DCEP solo tiene dos mensajes `DATA_CHANNEL_OPEN` y `DATA_CHANNEL_ACK`. Para cada canal de datos que se abre, el remoto debe responder con un acuse de recibo.

### DATA_CHANNEL_OPEN
Este mensaje es enviado por el Agente WebRTC que desea abrir un canal.

#### Formato de Paquete
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |  Channel Type |            Priority           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Reliability Parameter                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Label Length          |       Protocol Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                             Label                             /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            Protocol                           /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

#### Tipo de Mensaje
El Tipo de Mensaje es un valor estático de \`0x03\`.

#### Tipo de Canal
El Tipo de Canal controla los atributos de durabilidad/ordenamiento del canal. Puede tener los siguientes valores:

* \`DATA_CHANNEL_RELIABLE\` (\`0x00\`) - No se pierden mensajes y llegarán en orden
* \`DATA_CHANNEL_RELIABLE_UNORDERED\` (\`0x80\`) - No se pierden mensajes, pero pueden llegar fuera de orden.
* \`DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT\` (\`0x01\`) - Los mensajes pueden perderse después de intentar la cantidad de veces solicitada, pero llegarán en orden.
* \`DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED\` (\`0x81\`) - Los mensajes pueden perderse después de intentar la cantidad de veces solicitada y pueden llegar fuera de orden.
* \`DATA_CHANNEL_PARTIAL_RELIABLE_TIMED\` (\`0x02\`) - Los mensajes pueden perderse si no llegan en la cantidad de tiempo solicitada, pero llegarán en orden.
* \`DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED\` (\`0x82\`) - Los mensajes pueden perderse si no llegan en la cantidad de tiempo solicitada y pueden llegar fuera de orden.

#### Prioridad
La prioridad del canal de datos. Los canales de datos con mayor prioridad se programarán primero. Los mensajes de usuario de prioridad más baja y de gran tamaño no retrasarán el envío de mensajes de usuario de mayor prioridad.

#### Parámetro de Confiabilidad
Si el tipo de canal de datos es \`DATA_CHANNEL_PARTIAL_RELIABLE\`, los sufijos configuran el comportamiento:

* \`REXMIT\` - Define cuántas veces el remitente reintentará enviar el mensaje antes de rendirse.
* \`TIMED\` - Define durante cuánto tiempo (en ms) el remitente reintentará enviar el mensaje antes de rendirse.

#### Etiqueta
Una cadena codificada en UTF-8 que contiene el nombre del canal de datos. Esta cadena puede estar vacía.

#### Protocolo
Si es una cadena vacía, el protocolo no está especificado. Si es una cadena no vacía, debe especificar un protocolo registrado en el "WebSocket Subprotocol Name Registry", definido en [RFC 6455](https://tools.ietf.org/html/rfc6455#page-61).

### DATA_CHANNEL_ACK
Este mensaje es enviado por el Agente WebRTC para reconocer que este canal de datos ha sido abierto.

#### Formato de Paquete
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
\`\`\`

## Protocolo de Transmisión de Control de Flujo
SCTP es el verdadero poder detrás de los canales de datos de WebRTC. Proporciona todas estas características del canal de datos:

* Multiplexación
* Entrega confiable usando un mecanismo de retransmisión similar a TCP
* Opciones de confiabilidad parcial
* Evitación de Congestión
* Control de Flujo

Para entender SCTP lo exploraremos en tres partes. El objetivo es que sepas lo suficiente para depurar y aprender los detalles profundos de SCTP por tu cuenta después de este capítulo.

## Conceptos
SCTP es un protocolo rico en características. Esta sección solo va a cubrir las partes de SCTP que son usadas por WebRTC.
Las características en SCTP que no son usadas por WebRTC incluyen multi-homing y selección de ruta.

Con más de veinte años de desarrollo, SCTP puede ser difícil de comprender completamente.

### Asociación
Asociación es el término usado para una Sesión SCTP. Es el estado que se comparte
entre dos Agentes SCTP mientras se comunican.

### Flujos
Un flujo es una secuencia bidireccional de datos de usuario. Cuando creas un canal de datos en realidad solo estás creando un flujo SCTP. Cada Asociación SCTP contiene una lista de flujos. Cada flujo puede ser configurado con diferentes tipos de confiabilidad.

WebRTC solo te permite configurar en la creación del flujo, pero SCTP en realidad permite cambiar la configuración en cualquier momento.

### Basado en Datagramas
SCTP enmarca datos como datagramas y no como un flujo de bytes. Enviar y recibir datos se siente como usar UDP en lugar de TCP.
No necesitas agregar ningún código extra para transferir múltiples archivos sobre un flujo.

Los mensajes SCTP no tienen límites de tamaño como UDP. Un solo mensaje SCTP puede ser de múltiples gigabytes de tamaño.

### Fragmentos
El protocolo SCTP está compuesto de fragmentos. Hay muchos tipos diferentes de fragmentos. Estos fragmentos se usan para toda la comunicación.
Datos de usuario, inicialización de conexión, control de congestión y más se hacen a través de fragmentos.

Cada paquete SCTP contiene una lista de fragmentos. Así que en un paquete UDP puedes tener múltiples fragmentos transportando mensajes de diferentes flujos.

### Número de Secuencia de Transmisión
El Número de Secuencia de Transmisión (TSN) es un identificador único global para fragmentos DATA. Un fragmento DATA es lo que transporta todos los mensajes que un usuario desea enviar. El TSN es importante porque ayuda a un receptor a determinar si los paquetes se perdieron o están fuera de orden.

Si el receptor nota un TSN faltante, no entrega los datos al usuario hasta que se cumpla.

### Identificador de Flujo
Cada flujo tiene un identificador único. Cuando creas un canal de datos con un ID explícito, en realidad solo se pasa directamente a SCTP como el identificador de flujo. Si no pasas un ID, el identificador de flujo se elige por ti.

### Identificador de Protocolo de Carga Útil
Cada fragmento DATA también tiene un Identificador de Protocolo de Carga Útil (PPID). Esto se usa para identificar de manera única qué tipo de datos se está intercambiando.
SCTP tiene muchos PPIDs, pero WebRTC solo está usando los siguientes cinco:

* \`WebRTC DCEP\` (\`50\`) - Mensajes DCEP.
* \`WebRTC String\` (\`51\`) - Mensajes de cadena de DataChannel.
* \`WebRTC Binary\` (\`53\`) - Mensajes binarios de DataChannel.
* \`WebRTC String Empty\` (\`56\`) - Mensajes de cadena de DataChannel con longitud 0.
* \`WebRTC Binary Empty\` (\`57\`) - Mensajes binarios de DataChannel con longitud 0.

## Protocolo
Los siguientes son algunos de los fragmentos utilizados por el protocolo SCTP. Esta no es
una demostración exhaustiva. Esto proporciona suficientes estructuras para que la
máquina de estados tenga sentido.

Cada Fragmento comienza con un campo \`tipo\`. Antes de una lista de fragmentos, también
tendrás un encabezado.

### Fragmento DATA
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 0    | Reserved|U|B|E|    Length                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              TSN                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Stream Identifier        |   Stream Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Payload Protocol Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            User Data                          /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`
El fragmento DATA es cómo se intercambian todos los datos de usuario. Cuando envías
cualquier cosa sobre el canal de datos, así es como se intercambia.

El bit \`U\` se establece si este es un paquete desordenado. Podemos ignorar el
Número de Secuencia de Flujo.

\`B\` y \`E\` son los bits de inicio y fin. Si quieres enviar un
mensaje que es demasiado grande para un fragmento DATA, necesita fragmentarse en múltiples fragmentos DATA enviados en paquetes separados.
Con el bit \`B\` y \`E\` y Números de Secuencia, SCTP es capaz de expresar
esto.

* \`B=1\`, \`E=0\` - Primera pieza de un mensaje de usuario fragmentado.
* \`B=0\`, \`E=0\` - Pieza intermedia de un mensaje de usuario fragmentado.
* \`B=0\`, \`E=1\` - Última pieza de un mensaje de usuario fragmentado.
* \`B=1\`, \`E=1\` - Mensaje sin fragmentar.

\`TSN\` es el Número de Secuencia de Transmisión. Es el identificador
único global para este fragmento DATA. Después de 4,294,967,295 fragmentos esto se reiniciará a 0.
El TSN se incrementa para cada fragmento en un mensaje de usuario fragmentado para que el receptor sepa cómo ordenar los fragmentos recibidos para reconstruir el mensaje original.

\`Identificador de Flujo\` es el identificador único para el flujo al que pertenecen estos datos.

\`Número de Secuencia de Flujo\` es un número de 16 bits incrementado cada mensaje de usuario e incluido en el encabezado del fragmento del mensaje DATA. Después de 65535 mensajes esto se reiniciará a 0. Este número se usa para decidir el orden de entrega de mensajes al receptor si \`U\` está establecido en 0. Similar al TSN, excepto que el Número de Secuencia de Flujo solo se incrementa para cada mensaje en su conjunto y no para cada fragmento DATA individual.

\`Identificador de Protocolo de Carga Útil\` es el tipo de datos que fluye a través
de este flujo. Para WebRTC, será DCEP, String o Binary.

\`Datos de Usuario\` es lo que estás enviando. Todos los datos que envías a través de un canal de datos de WebRTC
se transmiten a través de un fragmento DATA.

### Fragmento INIT
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 1    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Initiate Tag                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Advertised Receiver Window Credit (a_rwnd)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Number of Outbound Streams   |  Number of Inbound Streams    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Initial TSN                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/              Optional/Variable-Length Parameters              /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

El fragmento INIT inicia el proceso de creación de una asociación.

\`Etiqueta de Inicio\` se usa para la generación de cookies. Las cookies se usan para la protección contra
Man-In-The-Middle y Denegación de Servicio. Se describen con mayor detalle en la sección de
máquina de estados.

\`Crédito de Ventana de Receptor Anunciado\` se usa para el Control de Congestión de SCTP. Esto
comunica qué tan grande es el búfer que el receptor ha asignado para esta asociación.

\`Número de Flujos de Salida/Entrada\` notifica al remoto cuántos flujos este
agente soporta.

\`TSN Inicial\` es un \`uint32\` aleatorio para comenzar el TSN local.

\`Parámetros Opcionales\` permite a SCTP introducir nuevas características al protocolo.


### Fragmento SACK

\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 3    |Chunk  Flags   |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Advertised Receiver Window Credit (a_rwnd)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Number of Gap Ack Blocks = N  |  Number of Duplicate TSNs = X |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Gap Ack Block #1 Start       |   Gap Ack Block #1 End        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Gap Ack Block #N Start      |  Gap Ack Block #N End         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN 1                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN X                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

El fragmento SACK (Acuse de Recibo Selectivo) es cómo un receptor notifica
a un remitente que ha recibido un paquete. Hasta que un remitente obtiene un SACK para un TSN
reenviará el fragmento DATA en cuestión. Sin embargo, un SACK hace más que
actualizar el TSN.

\`TSN ACK Acumulativo\` el TSN más alto que se ha recibido.

\`Crédito de Ventana de Receptor Anunciado\` tamaño del búfer del receptor. El receptor
puede cambiar esto durante la sesión si hay más memoria disponible.

\`Bloques Ack\` TSNs que han sido recibidos después del \`TSN ACK Acumulativo\`.
Esto se usa si hay una brecha en los paquetes entregados. Digamos que los fragmentos DATA con TSNs
\`100\`, \`102\`, \`103\` y \`104\` son entregados. El \`TSN ACK Acumulativo\` sería \`100\`, pero
\`Bloques Ack\` podrían usarse para decirle al remitente que no necesita reenviar \`102\`, \`103\` o \`104\`.

\`TSN Duplicado\` informa al remitente que ha recibido los siguientes fragmentos DATA más de una vez.

### Fragmento HEARTBEAT
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 4    | Chunk  Flags  |      Heartbeat Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/            Heartbeat Information TLV (Variable-Length)        /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

El fragmento HEARTBEAT se usa para afirmar que el remoto todavía está respondiendo.
Útil si no estás enviando fragmentos DATA y necesitas mantener un
mapeo NAT abierto.

### Fragmento ABORT
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 6    |Reserved     |T|           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\               Zero or more Error Causes                       \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

Un fragmento ABORT cierra abruptamente la asociación. Usado cuando
un lado entra en un estado de error. Finalizar la conexión de manera elegante usa
el fragmento SHUTDOWN.

### Fragmento SHUTDOWN
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 7    | Chunk  Flags  |      Length = 8               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

El fragmento SHUTDOWN inicia un cierre elegante de la asociación SCTP.
Cada agente informa al remoto del último TSN que envió. Esto asegura
que no se pierdan paquetes. WebRTC no hace un cierre elegante de
la asociación SCTP. Necesitas cerrar cada canal de datos tú mismo
para manejarlo de manera elegante.

\`TSN ACK Acumulativo\` es el último TSN que fue enviado. Cada lado sabe
que no debe terminar hasta que haya recibido el fragmento DATA con este TSN.

### Fragmento ERROR
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 9    | Chunk  Flags  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                    One or more Error Causes                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

Un fragmento ERROR se usa para notificar al Agente SCTP remoto que ha ocurrido un
error no fatal.

### Fragmento FORWARD TSN
\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 192  |  Flags = 0x00 |        Length = Variable      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      New Cumulative TSN                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-1              |       Stream Sequence-1       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               /
/                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-N              |       Stream Sequence-N       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

El fragmento \`FORWARD TSN\` mueve el TSN global hacia adelante. SCTP hace esto
para que puedas saltar algunos paquetes que ya no te importan. Digamos
que envías \`10 11 12 13 14 15\` y estos paquetes solo son válidos si
todos llegan. Estos datos también son sensibles al tiempo real, así que si llegan
tarde no son útiles.

Si pierdes \`12\` y \`13\` ¡no hay razón para enviar \`14\` y \`15\`!
SCTP usa el fragmento \`FORWARD TSN\` para lograr eso. Le dice al receptor
que \`14\` y \`15\` ya no se entregarán.

\`Nuevo TSN Acumulativo\` este es el nuevo TSN de la conexión. Cualquier paquete
antes de este TSN no se retendrá.

\`Flujo\` y \`Secuencia de Flujo\` se usan para saltar el \`Número de Secuencia de Flujo\`
adelante. Consulta de nuevo el Fragmento DATA para la importancia de este campo.

## Máquina de Estados
Estas son algunas partes interesantes de la máquina de estados SCTP. WebRTC no usa todas
las características de la máquina de estados SCTP, por lo que hemos excluido esas partes. También hemos simplificado algunos componentes para hacerlos comprensibles por sí mismos.

### Flujo de Establecimiento de Conexión
Los fragmentos \`INIT\` e \`INIT ACK\` se usan para intercambiar las capacidades y configuraciones
de cada par. SCTP usa una cookie durante el handshake para validar el par con el que se está comunicando.
Esto es para asegurar que el handshake no sea interceptado y para prevenir ataques DoS.

El fragmento \`INIT ACK\` contiene la cookie. La cookie luego se devuelve a su creador
usando el \`COOKIE ECHO\`. Si la verificación de la cookie es exitosa, se
envía el \`COOKIE ACK\` y los fragmentos DATA están listos para ser intercambiados.

![Establecimiento de conexión](../../images/07-connection-establishment.png "Establecimiento de conexión")

### Flujo de Desconexión
SCTP usa el fragmento \`SHUTDOWN\`. Cuando un agente recibe un fragmento \`SHUTDOWN\`, esperará hasta que
reciba el \`TSN ACK Acumulativo\` solicitado. Esto permite a un usuario asegurar que todos los datos
se entreguen incluso si la conexión tiene pérdidas.

### Mecanismo de Keep-Alive
SCTP usa los fragmentos \`HEARTBEAT REQUEST\` y \`HEARTBEAT ACK\` para mantener la conexión viva. Estos se envían
en un intervalo configurable. SCTP también realiza un backoff exponencial si el paquete no ha llegado.

El fragmento \`HEARTBEAT\` también contiene un valor de tiempo. Esto permite que dos asociaciones calculen el tiempo de viaje entre dos agentes.
