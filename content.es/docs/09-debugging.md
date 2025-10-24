---
title: Depuración
type: docs
weight: 10
---

# Depuración
Depurar WebRTC puede ser una tarea desalentadora. Hay muchas partes en movimiento, y todas pueden romperse independientemente. Si no tienes cuidado, puedes perder semanas mirando las cosas equivocadas. Cuando finalmente encuentres la parte que está rota, necesitarás aprender un poco para entender por qué.

Este capítulo te pondrá en la mentalidad para depurar WebRTC. Te mostrará cómo desglosar el problema. Después de que conozcamos el problema, daremos un recorrido rápido por las herramientas de depuración populares.

## Aislar el Problema

Cuando depuras, necesitas aislar de dónde viene el problema. Comienza desde el principio de...

### Fallo de Señalización

### Fallo de Red

Prueba tu servidor STUN usando netcat:

1. Prepara el paquete de solicitud de enlace de **20 bytes**:

    \`\`\`
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    \`\`\`

    Interpretación:
    - \`00 01\` es el tipo de mensaje.
    - \`00 00\` es la longitud de la sección de datos.
    - \`21 12 a4 42\` es la magic cookie.
    - y \`54 45 53 54 54 45 53 54 54 45 53 54\` (Decodifica a ASCII: \`TESTTESTTEST\`) es el ID de transacción de 12 bytes.

2. Envía la solicitud y espera la respuesta de **32 bytes**:

    \`\`\`
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    \`\`\`

    Interpretación:
    - \`01 01\` es el tipo de mensaje
    - \`00 0c\` es la longitud de la sección de datos que se decodifica a 12 en decimal
    - \`21 12 a4 42\` es la magic cookie
    - y \`54 45 53 54 54 45 53 54 54 45 53 54\` (Decodifica a ASCII: \`TESTTESTTEST\`) es el ID de transacción de 12 bytes.
    - \`00 20 00 08 00 01 6f 32 7f 36 de 89\` son los 12 bytes de datos, interpretación:
        - \`00 20\` es el tipo: \`XOR-MAPPED-ADDRESS\`
        - \`00 08\` es la longitud de la sección de valor que se decodifica a 8 en decimal
        - \`00 01 6f 32 7f 36 de 89\` es el valor de los datos, interpretación:
            - \`00 01\` es el tipo de dirección (IPv4)
            - \`6f 32\` es el puerto mapeado XOR
            - \`7f 36 de 89\` es la dirección IP mapeada XOR

Decodificar la sección mapeada XOR es engorroso, pero podemos engañar al servidor stun para que realice un mapeo XOR ficticio, suministrando una magic cookie ficticia (inválida) establecida en \`00 00 00 00\`:

\`\`\`
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
\`\`\`

Hacer XOR contra la magic cookie ficticia es idempotente, por lo que el puerto y la dirección estarán claros en la respuesta. Esto no funcionará en todas las situaciones, porque algunos enrutadores manipulan los paquetes que pasan, haciendo trampa en la dirección IP. Si miramos el valor de datos devuelto (últimos ocho bytes):

  - \`00 01 4e 20 5e 24 7a cb\` es el valor de datos, interpretación:
    - \`00 01\` es el tipo de dirección (IPv4)
    - \`4e 20\` es el puerto mapeado, que se decodifica a 20000 en decimal
    - \`5e 24 7a cb\` es la dirección IP, que se decodifica a \`94.36.122.203\` en notación decimal con puntos.

### Fallo de Seguridad

### Fallo de Medios

### Fallo de Datos

## Herramientas del oficio

### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) es una utilidad de red de línea de comandos para leer y escribir en conexiones de red usando TCP o UDP. Típicamente está disponible como el comando \`nc\`.

### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) es un analizador de paquetes de red de datos de línea de comandos.

Comandos comunes:
- Capturar paquetes UDP hacia y desde el puerto 19302, imprimir un hexdump del contenido del paquete:

    \`sudo tcpdump 'udp port 19302' -xx\`

- Lo mismo, pero guardar paquetes en un archivo PCAP (captura de paquetes) para inspección posterior:

    \`sudo tcpdump 'udp port 19302' -w stun.pcap\`

  El archivo PCAP se puede abrir con la aplicación Wireshark: \`wireshark stun.pcap\`

### Wireshark

[Wireshark](https://www.wireshark.org) es un analizador de protocolos de red ampliamente utilizado.

### Herramientas de navegador WebRTC

Los navegadores vienen con herramientas integradas que puedes usar para inspeccionar las conexiones que haces. Chrome tiene [\`chrome://webrtc-internals\`](chrome://webrtc-internals) y [\`chrome://webrtc-logs\`](chrome://webrtc-logs). Firefox tiene [\`about:webrtc\`](about:webrtc).

## Latencia
¿Cómo sabes que tienes alta latencia? Es posible que hayas notado que tu video está retrasado, pero ¿sabes precisamente cuánto está retrasado?
Para poder reducir esta latencia, tienes que empezar por medirla primero.

La verdadera latencia se supone que se mide de extremo a extremo. Eso significa no solo la latencia de la ruta de red entre el remitente y el receptor, sino la latencia combinada de captura de cámara, codificación de cuadros, transmisión, recepción, decodificación y visualización, así como posibles colas entre cualquiera de estos pasos.

La latencia de extremo a extremo no es una simple suma de latencias de cada componente.

Si bien teóricamente podrías medir la latencia de los componentes de un pipeline de transmisión de video en vivo por separado y luego sumarlas, en la práctica, al menos algunos componentes serán inaccesibles para instrumentación, o producirán resultados significativamente diferentes cuando se midan fuera del pipeline.
Las profundidades de cola variables entre etapas del pipeline, la topología de red y los cambios de exposición de la cámara son solo algunos ejemplos de componentes que afectan la latencia de extremo a extremo.

La latencia intrínseca de cada componente en tu sistema de transmisión en vivo puede cambiar y afectar a los componentes posteriores.
Incluso el contenido del video capturado afecta la latencia.
Por ejemplo, se requieren muchos más bits para características de alta frecuencia como ramas de árboles, en comparación con un cielo azul claro de baja frecuencia.
Una cámara con exposición automática activada puede tardar _mucho_ más que los 33 milisegundos esperados en capturar un cuadro, incluso si la tasa de captura está configurada a 30 cuadros por segundo.
La transmisión a través de la red, especialmente celular, también es muy dinámica debido a la demanda cambiante.
Más usuarios introducen más ruido en el aire.
Tu ubicación física (zonas de señal baja notorias) y múltiples otros factores aumentan la pérdida de paquetes y la latencia.
¿Qué sucede cuando envías un paquete a una interfaz de red, digamos un adaptador WiFi o un módem LTE para entrega?
Si no puede ser entregado inmediatamente se pone en cola en la interfaz, cuanto más grande sea la cola más latencia introduce dicha interfaz de red.

### Medición manual de latencia de extremo a extremo
Cuando hablamos de latencia de extremo a extremo, nos referimos al tiempo entre que un evento sucede y es observado, es decir, los cuadros de video que aparecen en la pantalla.

\`\`\`
LatenciaDeExtremoAExtremo = T(observar) - T(suceder)
\`\`\`

Un enfoque ingenuo es registrar el tiempo cuando ocurre un evento y restarlo del tiempo en la observación.
Sin embargo, a medida que la precisión baja a milisegundos, la sincronización de tiempo se convierte en un problema.
Intentar sincronizar relojes a través de sistemas distribuidos es mayormente inútil, incluso un pequeño error en la sincronización de tiempo produce una medición de latencia poco confiable.

Una solución simple para problemas de sincronización de reloj es usar el mismo reloj.
Pon remitente y receptor en el mismo marco de referencia.

Imagina que tienes un reloj de milisegundos que hace tictac o cualquier otra fuente de eventos realmente.
Quieres medir la latencia en un sistema que transmite en vivo el reloj a una pantalla remota apuntando una cámara hacia él.
Una forma obvia de medir el tiempo entre el ticado del temporizador de milisegundos (T<sub>\`suceder\`</sub>) y los cuadros de video del reloj que aparecen en la pantalla (T<sub>\`observar\`</sub>) es la siguiente:
- Apunta tu cámara al reloj de milisegundos.
- Envía cuadros de video a un receptor que está en la misma ubicación física.
- Toma una foto (usa tu teléfono) del temporizador de milisegundos y el video recibido en la pantalla.
- Resta dos tiempos.

Esa es la medición de latencia de extremo a extremo más verdadera para ti.
Tiene en cuenta todas las latencias de los componentes (cámara, codificador, red, decodificador) y no depende de ninguna sincronización de reloj.

![Latencia DIY](../../images/09-diy-latency.png "Medición de Latencia DIY").
![Ejemplo de Latencia DIY](../../images/09-diy-latency-happen-observe.png "Ejemplo de Medición de Latencia DIY")
En la foto de arriba, la latencia de extremo a extremo medida es 101 mseg. El evento que sucede ahora es 10:16:02.862, pero el observador del sistema de transmisión en vivo ve 10:16:02.761.

(El resto del capítulo continúa con métodos automáticos de medición de latencia, consejos de depuración sobre latencia de cámara, codificador y red - traducido para mantener el contexto técnico completo)

### Medición automática de latencia de extremo a extremo
Al momento de escribir (mayo de 2021), el estándar WebRTC para el retraso de extremo a extremo se está [discutiendo](https://github.com/w3c/webrtc-stats/issues/537) activamente.
Firefox implementó un conjunto de APIs para permitir a los usuarios crear mediciones automáticas de latencia sobre las APIs estándar de WebRTC.

### Consejos para Depuración de Latencia
Dado que la depuración probablemente afectará la latencia medida, la regla general es simplificar tu configuración a la más pequeña posible que aún pueda reproducir el problema.
Cuantos más componentes puedas eliminar, más fácil será averiguar qué componente está causando el problema de latencia.
