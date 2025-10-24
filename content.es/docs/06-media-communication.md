---
title: Comunicación de Medios
type: docs
weight: 7
---

# Comunicación de Medios

## ¿Qué obtengo de la comunicación de medios de WebRTC?

WebRTC te permite enviar y recibir una cantidad ilimitada de flujos de audio y video. Puedes agregar y eliminar estos flujos en cualquier momento durante una llamada. Estos flujos podrían ser todos independientes, o podrían estar agrupados juntos. Podrías enviar una transmisión de video de tu escritorio, y luego incluir audio y video de tu cámara web.

El protocolo WebRTC es agnóstico al códec. El transporte subyacente admite todo, incluso cosas que aún no existen. Sin embargo, el Agente WebRTC con el que te estás comunicando puede no tener las herramientas necesarias para aceptarlo.

WebRTC también está diseñado para manejar condiciones de red dinámicas. Durante una llamada tu ancho de banda podría aumentar o disminuir. Tal vez de repente experimentes mucha pérdida de paquetes. El protocolo está diseñado para manejar todo esto. WebRTC responde a las condiciones de la red e intenta darte la mejor experiencia posible con los recursos disponibles.

## ¿Cómo funciona?
WebRTC usa dos protocolos preexistentes RTP y RTCP, ambos definidos en [RFC 1889](https://tools.ietf.org/html/rfc1889).

RTP (Protocolo de Transporte en Tiempo Real) es el protocolo que transporta los medios. Fue diseñado para permitir la entrega en tiempo real de video. No estipula ninguna regla sobre latencia o confiabilidad, pero te da las herramientas para implementarlas. RTP te da flujos, para que puedas ejecutar múltiples transmisiones de medios sobre una conexión. También te da la información de temporización y ordenamiento que necesitas para alimentar un pipeline de medios.

RTCP (Protocolo de Control RTP) es el protocolo que comunica metadatos sobre la llamada. El formato es muy flexible y te permite agregar cualquier metadato que desees. Esto se usa para comunicar estadísticas sobre la llamada. También se usa para manejar la pérdida de paquetes e implementar el control de congestión. Te da la comunicación bidireccional necesaria para responder a las condiciones cambiantes de la red.

## Latencia vs Calidad
Los medios en tiempo real se tratan de hacer compromisos entre latencia y calidad. Cuanta más latencia estés dispuesto a tolerar, mayor calidad de video puedes esperar.

### Limitaciones del Mundo Real
Estas restricciones son todas causadas por las limitaciones del mundo real. Todas son características de tu red que necesitarás superar.

### El Video es Complejo
Transportar video no es fácil. Para almacenar 30 minutos de video 720 de 8 bits sin comprimir necesitas aproximadamente 110 GB. Con esos números, una llamada de conferencia de 4 personas no va a suceder. Necesitamos una forma de hacerlo más pequeño, y la respuesta es la compresión de video. Eso no viene sin inconvenientes.

## Video 101
No vamos a cubrir la compresión de video en profundidad, sino solo lo suficiente para entender por qué RTP está diseñado de la manera en que está. La compresión de video codifica video en un nuevo formato que requiere menos bits para representar el mismo video.

### Compresión con pérdida y sin pérdida
Puedes codificar video para que sea sin pérdida (no se pierde información) o con pérdida (la información puede perderse). Debido a que la codificación sin pérdida requiere que se envíen más datos a un par, lo que genera un flujo de mayor latencia y más paquetes perdidos, RTP típicamente usa compresión con pérdida aunque la calidad del video no sea tan buena.

### Compresión intra e inter cuadro
La compresión de video viene en dos tipos. El primero es intra-cuadro. La compresión intra-cuadro reduce los bits utilizados para describir un solo cuadro de video. Se usan las mismas técnicas para comprimir imágenes fijas, como el método de compresión JPEG.

El segundo tipo es la compresión inter-cuadro. Dado que el video está compuesto de muchas imágenes, buscamos formas de no enviar la misma información dos veces.

### Tipos de cuadros inter
Luego tienes tres tipos de cuadros:

* **I-Frame** - Una imagen completa, puede ser decodificada sin nada más.
* **P-Frame** - Una imagen parcial, que contiene solo cambios de la imagen anterior.
* **B-Frame** - Una imagen parcial, es una modificación de imágenes anteriores y futuras.

Lo siguiente es una visualización de los tres tipos de cuadros.

![Tipos de cuadros](../../images/06-frame-types.png "Tipos de cuadros")

### El video es delicado
La compresión de video es increíblemente con estado, lo que dificulta la transferencia a través de Internet. ¿Qué sucede si pierdes parte de un I-Frame? ¿Cómo sabe un P-Frame qué modificar? A medida que la compresión de video se vuelve más compleja, esto se está convirtiendo en un problema aún mayor. Afortunadamente, RTP y RTCP tienen la solución.

## RTP
### Formato de Paquete
Cada paquete RTP tiene la siguiente estructura:

\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       Sequence Number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           Timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Synchronization Source (SSRC) identifier            |
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
|            Contributing Source (CSRC) identifiers             |
|                             ....                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

#### Versión (V)
\`Versión\` es siempre \`2\`

#### Relleno (P)
\`Relleno\` es un booleano que controla si la carga útil tiene relleno.

El último byte de la carga útil contiene un recuento de cuántos bytes de relleno se agregaron.

#### Extensión (X)
Si está establecido, el encabezado RTP tendrá extensiones. Esto se describe con mayor detalle a continuación.

#### Recuento CSRC (CC)
La cantidad de identificadores \`CSRC\` que siguen después del \`SSRC\`, y antes de la carga útil.

#### Marcador (M)
El bit de marcador no tiene un significado preestablecido y puede ser usado como el usuario desee.

En algunos casos se establece cuando un usuario está hablando. También se usa comúnmente para marcar un cuadro clave.

#### Tipo de Carga Útil (PT)
\`Tipo de Carga Útil\` es un identificador único para qué códec está siendo transportado por este paquete.

Para WebRTC el \`Tipo de Carga Útil\` es dinámico. VP8 en una llamada puede ser diferente de otra. El oferente en la llamada determina el mapeo de \`Tipos de Carga Útil\` a códecs en la \`Descripción de Sesión\`.

#### Número de Secuencia
\`Número de Secuencia\` se usa para ordenar paquetes en un flujo. Cada vez que se envía un paquete, el \`Número de Secuencia\` se incrementa en uno.

RTP está diseñado para ser útil en redes con pérdida. Esto le da al receptor una forma de detectar cuándo se han perdido paquetes.

#### Marca de Tiempo
El instante de muestreo para este paquete. Esto no es un reloj global, sino cuánto tiempo ha pasado en el flujo de medios. Varios paquetes RTP pueden tener la misma marca de tiempo si, por ejemplo, todos son parte del mismo cuadro de video.

#### Fuente de Sincronización (SSRC)
Un \`SSRC\` es el identificador único para este flujo. Esto te permite ejecutar múltiples flujos de medios sobre un solo flujo RTP.

#### Fuente Contribuyente (CSRC)
Una lista que comunica qué \`SSRC\`s contribuyeron a este paquete.

Esto se usa comúnmente para indicadores de habla. Digamos que del lado del servidor combinaste múltiples transmisiones de audio en un solo flujo RTP. Luego podrías usar este campo para decir "Los flujos de entrada A y C estaban hablando en este momento".

#### Carga Útil
Los datos de carga útil reales. Puede terminar con el recuento de cuántos bytes de relleno se agregaron, si la bandera de relleno está establecida.

### Extensiones

## RTCP

### Formato de Paquete
Cada paquete RTCP tiene la siguiente estructura:

\`\`\`
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|    RC   |       PT      |             length            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\`\`\`

#### Versión (V)
\`Versión\` es siempre \`2\`.

#### Relleno (P)
\`Relleno\` es un booleano que controla si la carga útil tiene relleno.

El último byte de la carga útil contiene un recuento de cuántos bytes de relleno se agregaron.

#### Recuento de Informes de Recepción (RC)
El número de informes en este paquete. Un solo paquete RTCP puede contener múltiples eventos.

#### Tipo de Paquete (PT)
Identificador único para qué tipo de Paquete RTCP es este. Un Agente WebRTC no necesita admitir todos estos tipos, y el soporte entre Agentes puede ser diferente. Estos son los que puedes ver comúnmente:

* \`192\` - Solicitud de Cuadro INTRA completo (\`FIR\`)
* \`193\` - Acuses de Recibo Negativos (\`NACK\`)
* \`200\` - Informe del Remitente
* \`201\` - Informe del Receptor
* \`205\` - Retroalimentación RTP Genérica
* \`206\` - Retroalimentación Específica de Carga Útil

La importancia de estos tipos de paquetes se describirá con mayor detalle a continuación.

### Solicitud de Cuadro INTRA Completo (FIR) e Indicación de Pérdida de Imagen (PLI)
Tanto los mensajes \`FIR\` como \`PLI\` sirven un propósito similar. Estos mensajes solicitan un cuadro clave completo del remitente.
\`PLI\` se usa cuando se dieron cuadros parciales al decodificador, pero no pudo decodificarlos.
Esto podría suceder porque tuviste mucha pérdida de paquetes, o tal vez el decodificador falló.

Según [RFC 5104](https://tools.ietf.org/html/rfc5104#section-4.3.1.2), \`FIR\` no debe usarse cuando se pierden paquetes o cuadros. Ese es el trabajo de \`PLI\`. \`FIR\` solicita un cuadro clave por razones distintas a la pérdida de paquetes, por ejemplo, cuando un nuevo miembro ingresa a una videoconferencia. Necesitan un cuadro clave completo para comenzar a decodificar el flujo de video, el decodificador estará descartando cuadros hasta que llegue el cuadro clave.

Es una buena idea que un receptor solicite un cuadro clave completo justo después de conectarse, esto minimiza el retraso entre la conexión y que aparezca una imagen en la pantalla del usuario.

Los paquetes \`PLI\` son parte de los mensajes de Retroalimentación Específica de Carga Útil.

En la práctica, el software que puede manejar tanto paquetes \`PLI\` como \`FIR\` actuará de la misma manera en ambos casos. Enviará una señal al codificador para producir un nuevo cuadro clave completo.

### Acuse de Recibo Negativo
Un \`NACK\` solicita que un remitente retransmita un solo paquete RTP. Esto generalmente es causado por un paquete RTP que se pierde, pero también podría suceder porque llega tarde.

Los \`NACK\`s son mucho más eficientes en ancho de banda que solicitar que se envíe todo el cuadro nuevamente. Dado que RTP divide los paquetes en partes muy pequeñas, realmente solo estás solicitando una pequeña pieza faltante. El receptor crea un mensaje RTCP con el SSRC y el Número de Secuencia. Si el remitente no tiene este paquete RTP disponible para reenviar, simplemente ignora el mensaje.

### Informes de Remitente y Receptor
Estos informes se usan para enviar estadísticas entre agentes. Esto comunica la cantidad de paquetes realmente recibidos y el jitter.

Los informes se pueden usar para diagnósticos y control de congestión.

## Cómo RTP/RTCP resuelven problemas juntos
RTP y RTCP entonces trabajan juntos para resolver todos los problemas causados por las redes. ¡Estas técnicas todavía están cambiando constantemente!

### Corrección de Errores hacia Adelante
También conocido como FEC. Otro método para lidiar con la pérdida de paquetes. FEC es cuando envías los mismos datos varias veces, sin que siquiera sea solicitado. Esto se hace a nivel RTP, o incluso más bajo con el códec.

Si la pérdida de paquetes para una llamada es constante, entonces FEC es una solución de latencia mucho más baja que NACK. El tiempo de ida y vuelta de tener que solicitar y luego retransmitir el paquete faltante puede ser significativo para NACKs.

### Tasa de Bits Adaptativa y Estimación de Ancho de Banda
Como se discutió en el capítulo de [Redes en tiempo real](../05-real-time-networking/), las redes son impredecibles y poco confiables. La disponibilidad de ancho de banda puede cambiar varias veces durante una sesión.
No es raro ver que el ancho de banda disponible cambie dramáticamente (órdenes de magnitud) dentro de un segundo.

La idea principal es ajustar la tasa de bits de codificación basándose en el ancho de banda de red disponible predicho, actual y futuro.
Esto asegura que se transmita una señal de video y audio de la mejor calidad posible, y que la conexión no se caiga debido a la congestión de la red.
Las heurísticas que modelan el comportamiento de la red e intentan predecirlo se conocen como Estimación de Ancho de Banda.

Hay mucho matiz en esto, así que explorémoslo con mayor detalle.

## Identificar y Comunicar el Estado de la Red
RTP/RTCP se ejecuta sobre todo tipo de redes diferentes y, como resultado, es común que alguna
comunicación se pierda en su camino del remitente al receptor. Al estar construido sobre UDP,
no hay un mecanismo incorporado para la retransmisión de paquetes, y mucho menos para manejar el control de congestión.

Para proporcionar a los usuarios la mejor experiencia, WebRTC debe estimar las cualidades sobre la ruta de la red y
adaptarse a cómo esas cualidades cambian con el tiempo. Los rasgos clave para monitorear incluyen: ancho de banda disponible (en cada dirección, ya que puede no ser simétrico), tiempo de ida y vuelta, y jitter (fluctuaciones
en el tiempo de ida y vuelta). Necesita tener en cuenta la pérdida de paquetes y comunicar cambios en estas
propiedades a medida que las condiciones de red evolucionan.

Hay dos objetivos principales para estos protocolos:

1. Estimar el ancho de banda disponible (en cada dirección) soportado por la red.
2. Comunicar las características de la red entre remitente y receptor.

RTP/RTCP tiene tres enfoques diferentes para abordar este problema. Todos tienen sus pros y contras,
y generalmente cada generación ha mejorado sobre sus predecesores. Qué implementación uses dependerá
principalmente del stack de software disponible para tus clientes y las bibliotecas disponibles para
construir tu aplicación.

### Informes de Receptor / Informes de Remitente
La primera implementación es el par de Informes de Receptor y su complemento, Informes de Remitente. Estos
mensajes RTCP están definidos en [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4), y son
responsables de comunicar el estado de la red entre puntos finales. Los Informes de Receptor se centran en
comunicar cualidades sobre la red (incluida la pérdida de paquetes, el tiempo de ida y vuelta y el jitter), y
se emparejan con otros algoritmos que luego son responsables de estimar el ancho de banda disponible basándose en
estos informes.

Los informes de Remitente y Receptor (SR y RR) juntos pintan una imagen de la calidad de la red. Se
envían en un horario para cada SSRC, y son las entradas utilizadas al estimar el ancho de banda disponible. Esas estimaciones las hace el remitente después de recibir los datos RR, que contienen los
siguientes campos:

* **Fracción Perdida** - Qué porcentaje de paquetes se ha perdido desde el último Informe de Receptor.
* **Número Acumulativo de Paquetes Perdidos** - Cuántos paquetes se han perdido durante toda la llamada.
* **Número de Secuencia Más Alto Extendido Recibido** - Cuál fue el último Número de Secuencia recibido, y
  cuántas veces se ha reiniciado.
* **Jitter de Inter-llegada** - El Jitter continuo para toda la llamada.
* **Marca de Tiempo del Último Informe del Remitente** - Última hora conocida en el remitente, usada para el cálculo del tiempo de ida y vuelta.

SR y RR trabajan juntos para calcular el tiempo de ida y vuelta.

El remitente incluye su hora local, \`sendertime1\` en SR. Cuando el receptor recibe un paquete SR, envía de vuelta RR. Entre otras cosas, el RR incluye \`sendertime1\` recién recibido del remitente.
Habrá un retardo entre recibir el SR y enviar el RR. Por eso, el RR también incluye un tiempo de "retardo desde el último informe del remitente" - \`DLSR\`. El \`DLSR\` se usa para ajustar la
estimación del tiempo de ida y vuelta más adelante en el proceso. Una vez que el remitente recibe el RR, resta
\`sendertime1\` y \`DLSR\` del tiempo actual \`sendertime2\`. Este delta de tiempo se llama retardo de propagación de ida y vuelta o tiempo de ida y vuelta.

\`rtt = sendertime2 - sendertime1 - DLSR\`

Tiempo de ida y vuelta en español sencillo:
- Te envío un mensaje con la lectura actual de mi reloj, digamos que es 4:20pm, 42 segundos y 420 milisegundos.
- Me devuelves esta misma marca de tiempo.
- También incluyes el tiempo transcurrido desde leer mi mensaje hasta enviar el mensaje de vuelta, digamos 5 milisegundos.
- Una vez que recibo el tiempo de vuelta, miro el reloj de nuevo.
- Ahora mi reloj dice 4:20pm, 42 segundos 690 milisegundos.
- Significa que tomó 265 milisegundos (690 - 420 - 5) para llegar a ti y regresar a mí.
- Por lo tanto, el tiempo de ida y vuelta es 265 milisegundos.

![Tiempo de ida y vuelta](../../images/06-rtt.png "Tiempo de ida y vuelta")

<!-- Missing: What is an example congestion-control alg that pairs with RR/SR? -->

### TMMBR, TMMBN, REMB y TWCC, emparejados con GCC

#### Control de Congestión de Google (GCC)
El algoritmo de Control de Congestión de Google (GCC) (descrito en
[draft-ietf-rmcat-gcc-02](https://tools.ietf.org/html/draft-ietf-rmcat-gcc-02)) aborda el
desafío de la estimación de ancho de banda. Se empareja con una variedad de otros protocolos para facilitar los
requisitos de comunicación asociados. En consecuencia, está bien adaptado para ejecutarse en el
lado receptor (cuando se ejecuta con TMMBR/TMMBN o REMB) o en el lado remitente (cuando se ejecuta con TWCC).

Para llegar a estimaciones del ancho de banda disponible, GCC se centra en la pérdida de paquetes y las fluctuaciones en el tiempo de llegada de cuadros como sus dos métricas principales. Ejecuta estas métricas a través de dos controladores vinculados: el
controlador basado en pérdida y el controlador basado en retardo.

El primer componente de GCC, el controlador basado en pérdida, es simple:

* Si la pérdida de paquetes está por encima del 10%, la estimación de ancho de banda se reduce.
* Si la pérdida de paquetes está entre 2-10%, la estimación de ancho de banda permanece igual.
* Si la pérdida de paquetes está por debajo del 2%, la estimación de ancho de banda aumenta.

Las mediciones de pérdida de paquetes se toman con frecuencia. Dependiendo del protocolo de comunicación emparejado,
la pérdida de paquetes puede comunicarse explícitamente (como con TWCC) o inferirse (como con TMMBR/TMMBN
y REMB). Estos porcentajes se evalúan en ventanas de tiempo de alrededor de un segundo.

El controlador basado en retardo coopera con el controlador basado en pérdida y observa las variaciones en el tiempo de llegada de paquetes. Este controlador basado en retardo tiene como objetivo identificar cuándo los enlaces de red se están volviendo
cada vez más congestionados, y puede reducir las estimaciones de ancho de banda incluso antes de que ocurra la pérdida de paquetes. La
teoría es que la interfaz de red más ocupada a lo largo de la ruta continuará poniendo en cola los paquetes
hasta que la interfaz se quede sin capacidad dentro de sus búferes. Si esa interfaz continúa recibiendo
más tráfico del que puede enviar, se verá obligada a descartar todos los paquetes que no pueda caber en
su espacio de búfer. Este tipo de pérdida de paquetes es particularmente disruptivo para la comunicación en tiempo real/baja latencia, pero también puede degradar el rendimiento para toda la comunicación sobre ese enlace y debería
idealmente evitarse. Por lo tanto, GCC intenta averiguar si los enlaces de red están creciendo colas cada vez más grandes _antes_ de que realmente ocurra la pérdida de paquetes. Reducirá el uso de ancho de banda si observa
retardos de cola crecientes con el tiempo.

Para lograr esto, GCC intenta inferir aumentos en la profundidad de la cola midiendo aumentos sutiles en el tiempo de ida y vuelta. Registra el "tiempo inter-llegada" de los cuadros, \`t(i) - t(i-1)\`: la diferencia en el tiempo de llegada
de dos grupos de paquetes (generalmente, cuadros de video consecutivos). Estos grupos de paquetes frecuentemente
parten a intervalos regulares de tiempo (por ejemplo, cada 1/24 segundos para un video de 24 fps). Como resultado,
medir el tiempo inter-llegada es tan simple como registrar la diferencia de tiempo entre el inicio del
primer grupo de paquetes (es decir, cuadro) y el primer cuadro del siguiente.

En el diagrama a continuación, el aumento mediano del retardo inter-paquete es +20 mseg, un claro indicador de
congestión de red.

![TWCC con retardo](../../images/06-twcc.png "TWCC con retardo")

Si el tiempo inter-llegada aumenta con el tiempo, eso se presume como evidencia de una mayor profundidad de cola en
las interfaces de red conectadas y se considera congestión de red. (Nota: GCC es lo suficientemente inteligente como para
controlar estas mediciones para fluctuaciones en los tamaños de bytes de los cuadros.) GCC refina sus mediciones de latencia
usando un [filtro de Kalman](https://en.wikipedia.org/wiki/Kalman_filter) y toma muchas
mediciones de los tiempos de ida y vuelta de la red (y sus variaciones) antes de señalar congestión. Uno puede
pensar en el filtro de Kalman de GCC como tomando el lugar de una regresión lineal: ayudando a hacer predicciones precisas
incluso cuando el jitter agrega ruido a las mediciones de tiempo. Al señalar congestión, GCC
reducirá la tasa de bits disponible. Alternativamente, bajo condiciones de red estables, puede aumentar lentamente
sus estimaciones de ancho de banda para probar valores de carga más altos.

#### TMMBR, TMMBN y REMB
Para TMMBR/TMMBN y REMB, el lado receptor primero estima el ancho de banda entrante disponible (usando un
protocolo como GCC), y luego comunica estas estimaciones de ancho de banda a los remitentes remotos. No necesitan intercambiar detalles sobre la pérdida de paquetes u otras cualidades sobre la congestión de la red
porque operar en el lado receptor les permite medir el tiempo inter-llegada y la pérdida de paquetes
directamente. En su lugar, TMMBR, TMMBN y REMB intercambian solo las estimaciones de ancho de banda en sí:

* **Solicitud Temporal de Tasa de Bits Máxima de Flujo de Medios** - Una mantisa/exponente de una tasa de bits solicitada
  para un solo SSRC.
* **Notificación Temporal de Tasa de Bits Máxima de Flujo de Medios** - Un mensaje para notificar que se ha recibido un TMMBR.
* **Tasa de Bits Máxima Estimada del Receptor** - Una mantisa/exponente de una tasa de bits solicitada para toda la sesión.

TMMBR y TMMBN llegaron primero y están definidos en [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB
llegó más tarde, hubo un borrador presentado en
[draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), pero
nunca fue estandarizado.

Una sesión de ejemplo que usa REMB podría comportarse de la siguiente manera:

![REMB](../../images/06-remb.png "REMB")

Este método funciona genial en papel. El Remitente recibe estimación del receptor, establece la tasa de bits del codificador al valor recibido. ¡Tada! Nos hemos ajustado a las condiciones de la red.

Sin embargo, en la práctica, el enfoque REMB tiene múltiples inconvenientes.

La ineficiencia del codificador es el primero. Cuando estableces una tasa de bits para el codificador, no necesariamente
producirá la tasa de bits exacta que solicitaste. La codificación puede producir más o menos bits, dependiendo de la
configuración del codificador y el cuadro que se está codificando.

Por ejemplo, usar el codificador x264 con \`tune=zerolatency\` puede desviarse significativamente de la tasa de bits objetivo especificada. Aquí hay un escenario posible:

- Digamos que comenzamos estableciendo la tasa de bits a 1000 kbps.
- El codificador produce solo 700 kbps, porque no hay suficientes características de alta frecuencia para codificar. (AKA - "mirando una pared".)
- También imaginemos que el receptor obtiene el video de 700 kbps con cero pérdida de paquetes. Luego aplica la regla 1 de REMB para aumentar la tasa de bits entrante en un 8%.
- El receptor envía un paquete REMB con una sugerencia de 756 kbps (700 kbps * 1.08) al remitente.
- El remitente establece la tasa de bits del codificador a 756 kbps.
- El codificador produce una tasa de bits aún más baja.
- Este proceso continúa repitiéndose, reduciendo la tasa de bits al mínimo absoluto.

Puedes ver cómo esto causaría un ajuste pesado de parámetros del codificador, y sorprendería a los usuarios con video imposible de ver incluso en una gran conexión.

#### Control de Congestión de Transporte Amplio
El Control de Congestión de Transporte Amplio es el último desarrollo en la comunicación del estado de la red RTCP. Está definido en
[draft-holmer-rmcat-transport-wide-cc-extensions-01](https://datatracker.ietf.org/doc/html/draft-holmer-rmcat-transport-wide-cc-extensions-01),
pero tampoco ha sido estandarizado.

TWCC usa un principio bastante simple:

![TWCC](../../images/06-twcc-idea.png "TWCC")

Con REMB, el receptor instruye al lado remitente en la tasa de bits de descarga disponible. Usa
mediciones precisas sobre la pérdida de paquetes inferida y datos solo que tiene sobre el tiempo de llegada inter-paquete.

TWCC es casi un enfoque híbrido entre las generaciones SR/RR y REMB de protocolos. Lleva las
estimaciones de ancho de banda de vuelta al lado remitente (similar a SR/RR), pero su técnica de estimación de ancho de banda
se asemeja más a la generación REMB.

Con TWCC, el receptor le permite al remitente conocer el tiempo de llegada de cada paquete. Esto es suficiente
información para que el remitente mida la variación del retardo de llegada inter-paquete, así como identificar
qué paquetes fueron descartados o llegaron demasiado tarde para contribuir a la transmisión de audio/video. Con estos datos
siendo intercambiados frecuentemente, el remitente puede ajustarse rápidamente a las condiciones cambiantes de la red y
variar su ancho de banda de salida usando un algoritmo como GCC.

El remitente mantiene un seguimiento de los paquetes enviados, sus números de secuencia, tamaños y marcas de tiempo. Cuando el
remitente recibe mensajes RTCP del receptor, compara los retardos inter-paquete de envío con
los retardos de recepción. Si los retardos de recepción aumentan, señala congestión de red, y el remitente
debe tomar medidas correctivas.

Al proporcionar al remitente los datos sin procesar, TWCC proporciona una excelente vista de las condiciones de red en tiempo real:
- Comportamiento de pérdida de paquetes casi instantáneo, hasta los paquetes perdidos individuales
- Tasa de bits de envío precisa
- Tasa de bits de recepción precisa
- Medición del jitter
- Diferencias entre los retardos de paquetes de envío y recepción
- Descripción de cómo la red toleró la entrega de ancho de banda ráfaga o constante

Una de las contribuciones más significativas de TWCC es la flexibilidad que brinda a los
desarrolladores de WebRTC. Al consolidar el algoritmo de control de congestión en el lado remitente, permite un código de
cliente simple que puede ser ampliamente usado y requiere mejoras mínimas con el tiempo. Los complejos
algoritmos de control de congestión pueden entonces iterarse más rápidamente en el hardware que controlan directamente (como la Unidad de Reenvío Selectivo, discutida en la sección 8). En el caso de navegadores y
dispositivos móviles, esto significa que esos clientes pueden beneficiarse de mejoras de algoritmos sin tener que
esperar la estandarización o actualizaciones del navegador (que pueden tomar bastante tiempo para estar ampliamente disponibles).

## Alternativas de Estimación de Ancho de Banda
La implementación más desplegada es "Un Algoritmo de Control de Congestión de Google para Comunicación en Tiempo Real" definido en
[draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).

Hay varias alternativas a GCC, por ejemplo [NADA: Un Esquema de Control de Congestión Unificado para
Medios en Tiempo Real](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) y [SCReAM - Adaptación de Tasa Auto-Cronometrada para Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
