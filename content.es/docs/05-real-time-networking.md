---
title: Redes en Tiempo Real
type: docs
weight: 6
---

# Redes en Tiempo Real

## ¿Por qué las redes son tan importantes en la comunicación en tiempo real?

Las redes son el factor limitante en la comunicación en tiempo real. En un mundo ideal tendríamos ancho de banda ilimitado
y los paquetes llegarían instantáneamente. Sin embargo, este no es el caso. Las redes son limitadas, y las condiciones
pueden cambiar en cualquier momento. Medir y observar las condiciones de la red también es un problema difícil. Puedes obtener diferentes comportamientos
dependiendo del hardware, software y su configuración.

La comunicación en tiempo real también plantea un problema que no existe en la mayoría de los otros dominios. Para un desarrollador web no es fatal
si tu sitio web es más lento en algunas redes. Mientras todos los datos lleguen, los usuarios están felices. Con WebRTC, si tus datos llegan
tarde son inútiles. A nadie le importa lo que se dijo en una llamada de conferencia hace 5 segundos. Así que cuando desarrollas un sistema de comunicación en tiempo real,
tienes que hacer un compromiso. ¿Cuál es mi límite de tiempo, y cuántos datos puedo enviar?

Este capítulo cubre los conceptos que se aplican tanto a la comunicación de datos como de medios. En capítulos posteriores vamos más allá
de lo teórico y discutimos cómo los subsistemas de medios y datos de WebRTC resuelven estos problemas.

## ¿Cuáles son los atributos de la red que la hacen difícil?
El código que funciona efectivamente en todas las redes es complicado. Tienes muchos factores diferentes, y todos
pueden afectarse sutilmente entre sí. Estos son los problemas más comunes que los desarrolladores encontrarán.

#### Ancho de Banda
El ancho de banda es la tasa máxima de datos que se pueden transferir a través de una ruta dada. Es importante recordar
que este tampoco es un número estático. El ancho de banda cambiará a lo largo de la ruta a medida que más (o menos) personas lo usen.

#### Tiempo de Transmisión y Tiempo de Ida y Vuelta
El Tiempo de Transmisión es cuánto tiempo tarda un paquete en llegar a su destino. Como el Ancho de Banda, esto no es constante. El Tiempo de Transmisión puede fluctuar en cualquier momento.

`transmission_time = receive_time - send_time`

Para calcular el tiempo de transmisión, necesitas relojes en el remitente y el receptor sincronizados con precisión de milisegundos.
Incluso una pequeña desviación produciría una medición poco confiable del tiempo de transmisión.
Dado que WebRTC está operando en entornos altamente heterogéneos, es casi imposible confiar en una sincronización de tiempo perfecta entre hosts.

La medición del tiempo de ida y vuelta es una solución alternativa para la sincronización imperfecta del reloj.

En lugar de operar con relojes distribuidos, un par WebRTC envía un paquete especial con su propia marca de tiempo `sendertime1`.
Un par cooperante recibe el paquete y refleja la marca de tiempo de vuelta al remitente.
Una vez que el remitente original obtiene el tiempo reflejado, resta la marca de tiempo `sendertime1` del tiempo actual `sendertime2`.
Este delta de tiempo se llama "retardo de propagación de ida y vuelta" o más comúnmente tiempo de ida y vuelta.

`rtt = sendertime2 - sendertime1`

La mitad del tiempo de ida y vuelta se considera una aproximación suficientemente buena del tiempo de transmisión.
Esta solución alternativa no está exenta de inconvenientes.
Asume que toma la misma cantidad de tiempo enviar y recibir paquetes.
Sin embargo, en redes celulares, las operaciones de envío y recepción pueden no ser simétricas en tiempo.
Es posible que hayas notado que las velocidades de carga en tu teléfono son casi siempre más bajas que las velocidades de descarga.

`transmission_time = rtt/2`

Los tecnicismos de la medición del tiempo de ida y vuelta se describen con mayor detalle en el [capítulo de Informes de Remitente y Receptor RTCP](../06-media-communication/#receiver-reports--sender-reports).

#### Jitter
El jitter es el hecho de que el `Tiempo de Transmisión` puede variar para cada paquete. Tus paquetes podrían retrasarse, pero luego llegar en ráfagas.

#### Pérdida de Paquetes
La Pérdida de Paquetes es cuando los mensajes se pierden en la transmisión. La pérdida podría ser constante, o podría venir en picos.
Esto podría ser por el tipo de red como satélite o Wi-Fi. O podría ser introducido por el software en el camino.

#### Unidad Máxima de Transmisión
La Unidad Máxima de Transmisión es el límite de qué tan grande puede ser un solo paquete. Las redes no te permiten enviar
un mensaje gigante. A nivel de protocolo, los mensajes pueden tener que dividirse en múltiples paquetes más pequeños.

La MTU también diferirá dependiendo de qué ruta de red tomes. Puedes
usar un protocolo como [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) para averiguar el tamaño de paquete más grande que puedes enviar.

### Congestión
La congestión es cuando se han alcanzado los límites de la red. Esto generalmente es porque has alcanzado el ancho de banda máximo
que la ruta actual puede manejar. O podría ser impuesto por el operador como límites horarios que tu ISP configura.

La congestión se manifiesta de muchas maneras diferentes. No hay un comportamiento estandarizado. En la mayoría de los casos, cuando se alcanza la congestión
la red descartará paquetes en exceso. En otros casos, la red almacenará en búfer. Esto causará que el Tiempo de Transmisión
de tus paquetes aumente. También podrías ver más jitter a medida que tu red se congestiona. Esta es un área que cambia rápidamente
y aún se están escribiendo nuevos algoritmos para la detección de congestión.

### Dinámica
Las redes son increíblemente dinámicas y las condiciones pueden cambiar rápidamente. Durante una llamada puedes enviar y recibir cientos de miles de paquetes.
Esos paquetes viajarán a través de múltiples saltos. Esos saltos serán compartidos por millones de otros usuarios. Incluso en tu red local podrías tener
películas HD siendo descargadas o tal vez un dispositivo decide descargar una actualización de software.

Tener una buena llamada no es tan simple como medir tu red al inicio. Necesitas estar evaluando constantemente. También necesitas manejar todos los diferentes
comportamientos que provienen de una multitud de hardware y software de red.

## Resolver la Pérdida de Paquetes
Manejar la pérdida de paquetes es el primer problema a resolver. Hay múltiples formas de resolverlo, cada una con sus propios beneficios. Depende de qué estés enviando y qué tan
tolerante a la latencia seas. También es importante notar que no toda pérdida de paquetes es fatal. Perder algo de video podría no ser un problema, el ojo humano podría no
incluso poder percibirlo. Perder mensajes de texto de un usuario es fatal.

Digamos que envías 10 paquetes, y los paquetes 5 y 6 se pierden. Aquí hay formas de resolverlo.

### Acuses de Recibo
Los Acuses de Recibo es cuando el receptor notifica al remitente de cada paquete que ha recibido. El remitente es consciente de la pérdida de paquetes cuando obtiene un acuse de recibo
para un paquete dos veces que no es final. Cuando el remitente obtiene un `ACK` para el paquete 4 dos veces, sabe que el paquete 5 aún no se ha visto.

### Acuses de Recibo Selectivos
Los Acuses de Recibo Selectivos son una mejora sobre los Acuses de Recibo. Un receptor puede enviar un `SACK` que reconoce múltiples paquetes y notifica al remitente de las brechas.
Ahora el remitente puede obtener un `SACK` para el paquete 4 y 7. Entonces sabe que necesita reenviar los paquetes 5 y 6.

### Acuses de Recibo Negativos
Los Acuses de Recibo Negativos resuelven el problema de manera opuesta. En lugar de notificar al remitente lo que ha recibido, el receptor notifica al remitente lo que se ha perdido. En nuestro caso se enviará un `NACK`
para los paquetes 5 y 6. El remitente solo conoce los paquetes que el receptor desea que se envíen de nuevo.

### Corrección de Errores hacia Adelante
La Corrección de Errores hacia Adelante corrige la pérdida de paquetes de manera preventiva. El remitente envía datos redundantes, lo que significa que un paquete perdido no afecta el flujo final. Un algoritmo popular para
esto es la corrección de errores Reed–Solomon.

Esto reduce la latencia/complejidad de enviar y manejar Acuses de Recibo. La Corrección de Errores hacia Adelante es un desperdicio de ancho de banda si la red en la que estás tiene cero pérdida.

## Resolver el Jitter
El jitter está presente en la mayoría de las redes. Incluso dentro de una LAN tienes muchos dispositivos enviando datos a tasas fluctuantes. Puedes observar fácilmente el jitter haciendo ping a otro dispositivo con el comando `ping` y notando las fluctuaciones en la latencia de ida y vuelta.

Para resolver el jitter, los clientes usan un JitterBuffer. El JitterBuffer asegura un tiempo de entrega constante de paquetes. La desventaja es que JitterBuffer agrega algo de latencia a los paquetes que llegan temprano.
La ventaja es que los paquetes tardíos no causan jitter. Imagina que durante una llamada, ves los siguientes tiempos de llegada de paquetes:

```
* time=1.46 ms
* time=1.93 ms
* time=1.57 ms
* time=1.55 ms
* time=1.54 ms
* time=1.72 ms
* time=1.45 ms
* time=1.73 ms
* time=1.80 ms
```

En este caso, alrededor de 1.8 ms sería una buena elección. Los paquetes que llegan tarde usarán nuestra ventana de latencia. Los paquetes que llegan temprano se retrasarán un poco y pueden
llenar la ventana agotada por paquetes tardíos. Esto significa que ya no tenemos tartamudeo y proporcionamos una tasa de entrega suave para el cliente.

### Operación del JitterBuffer

![JitterBuffer](../../images/05-jitterbuffer.png "JitterBuffer")

Cada paquete se agrega al jitter buffer tan pronto como se recibe.
Una vez que hay suficientes paquetes para reconstruir el cuadro, los paquetes que conforman el cuadro se liberan del búfer y se emiten para decodificación.
El decodificador, a su vez, decodifica y dibuja el cuadro de video en la pantalla del usuario.
Dado que el jitter buffer tiene una capacidad limitada, los paquetes que permanecen en el búfer durante demasiado tiempo se descartarán.

Lee más sobre cómo los cuadros de video se convierten en paquetes RTP, y por qué la reconstrucción es necesaria [en el capítulo de comunicación de medios](../06-media-communication/#rtp).

`jitterBufferDelay` proporciona una gran visión sobre el rendimiento de tu red y su influencia en la suavidad de reproducción.
Es parte de la [API de estadísticas de WebRTC](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) relevante para el flujo entrante del receptor.
El retardo define la cantidad de tiempo que los cuadros de video pasan en el jitter buffer antes de ser emitidos para decodificación.
Un largo retardo del jitter buffer significa que tu red está altamente congestionada.

## Detectar la Congestión
Antes de que podamos incluso resolver la congestión, necesitamos detectarla. Para detectarla usamos un controlador de congestión. Este es un tema complicado, y todavía está cambiando rápidamente.
Aún se están publicando y probando nuevos algoritmos. A alto nivel todos operan de la misma manera. Un controlador de congestión proporciona estimaciones de ancho de banda dadas algunas entradas.
Estas son algunas entradas posibles:

* **Pérdida de Paquetes** - Los paquetes se descartan a medida que la red se congestiona.
* **Jitter** - A medida que el equipo de red se sobrecarga más, los paquetes en cola harán que los tiempos sean erráticos.
* **Tiempo de Ida y Vuelta** - Los paquetes tardan más en llegar cuando están congestionados. A diferencia del jitter, el Tiempo de Ida y Vuelta sigue aumentando.
* **Notificación Explícita de Congestión** - Las redes más nuevas pueden etiquetar paquetes como en riesgo de ser descartados para aliviar la congestión.

Estos valores necesitan ser medidos continuamente durante la llamada. La utilización de la red puede aumentar o disminuir, por lo que el ancho de banda disponible podría estar cambiando constantemente.

## Resolver la Congestión
Ahora que tenemos un ancho de banda estimado necesitamos ajustar lo que estamos enviando. Cómo ajustamos depende de qué tipo de datos queremos enviar.

### Enviar Más Lento
Limitar la velocidad a la que envías datos es la primera solución para prevenir la congestión. El Controlador de Congestión te da una estimación, y es
responsabilidad del remitente limitar la tasa.

Este es el método utilizado para la mayoría de la comunicación de datos. Con protocolos como TCP esto es todo hecho por el sistema operativo y completamente transparente tanto para usuarios como para desarrolladores.

### Enviar Menos
En algunos casos podemos enviar menos información para satisfacer nuestros límites. También tenemos plazos difíciles en la llegada de nuestros datos, por lo que no podemos enviar más lento. Estas son las restricciones
bajo las que caen los medios en tiempo real.

Si no tenemos suficiente ancho de banda disponible, podemos reducir la calidad del video que enviamos. Esto requiere un ciclo de retroalimentación ajustado entre tu codificador de video y controlador de congestión.
