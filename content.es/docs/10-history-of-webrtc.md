---
title: Historia
type: docs
weight: 11
---

# Historia
Al aprender WebRTC, los desarrolladores a menudo se sienten frustrados por la complejidad. Ven
características de WebRTC irrelevantes para su proyecto actual y desean que WebRTC fuera
más simple. El problema
es que todos tienen un conjunto diferente de casos de uso. La comunicación en tiempo real tiene una
historia rica con muchas personas diferentes construyendo muchas cosas diferentes.

Este capítulo contiene entrevistas con los autores de los protocolos que componen
WebRTC.
Da una visión de los diseños realizados al construir cada protocolo, y
termina con una
entrevista sobre WebRTC en sí. Si entiendes las intenciones y diseños del software
puedes construir sistemas más efectivos con él.

## RTP
RTP y RTCP es el protocolo que maneja todo el transporte de medios para WebRTC. Fue
definido en [RFC 1889](https://tools.ietf.org/html/rfc1889) en enero de 1996.
Tenemos mucha suerte de que uno de los autores [Ron
Frederick](https://github.com/ronf) hable sobre él mismo. Ron recientemente subió
[Network Video tool](https://github.com/ronf/nv) a GitHub, un proyecto que
informó RTP.

### En sus propias palabras

En octubre de 1992, comencé a experimentar con la tarjeta capturadora de cuadros Sun VideoPix
con la idea de escribir una herramienta de videoconferencia de red basada en multicast IP.
Se modeló según "vat", una herramienta de audioconferencia desarrollada
en LBL, en el sentido de que usaba un protocolo de sesión ligero similar para que los usuarios
se unieran a conferencias, donde simplemente enviabas datos a un
grupo multicast particular y observabas ese grupo en busca de cualquier tráfico de otros miembros
del grupo.

Para que el programa fuera realmente exitoso, necesitaba comprimir los
datos de video antes de ponerlos en la red. Mi objetivo era hacer un
flujo de datos de aspecto aceptable que cupiera en aproximadamente 128 kbps, o el
ancho de banda disponible en una línea ISDN doméstica estándar.

En noviembre temprano de 1992, lancé la herramienta de videoconferencia "nv" (en
forma binaria) a la comunidad de Internet. Después de algunas pruebas iniciales, se usó
para transmitir por video partes del Grupo de Trabajo de Ingeniería de Internet de noviembre por todo
el mundo.

El protocolo de red utilizado para "nv" y otras herramientas de conferencia de Internet
se convirtió en la base del Protocolo de Transporte en Tiempo Real (RTP), estandarizado
a través del Grupo de Trabajo de Ingeniería de Internet (IETF).

## WebRTC
WebRTC requirió un esfuerzo de estandarización que empequeñece todos los otros esfuerzos
descritos en este capítulo. Requirió cooperación entre dos
organismos de estándares diferentes (IETF y W3C) y cientos de individuos a través de muchas
empresas y países. Para darnos una mirada al interior de las motivaciones y
el esfuerzo monumental que tomó hacer que WebRTC sucediera, tenemos a
[Serge Lachapelle](https://twitter.com/slac).

Serge es un gerente de producto en Google, actualmente sirviendo como gerente de producto
para Google Workspace. Este es mi resumen de la entrevista.

### ¿Qué te llevó a trabajar en WebRTC?
He sido apasionado por construir software de comunicaciones desde que estaba en
la universidad. En los años 90, la tecnología como [nv](https://github.com/ronf/nv)
comenzó a aparecer, pero era difícil de usar. Creé un proyecto que te permitía
unirte a una videollamada directamente desde tu navegador.

Llevé esta experiencia a Marratech, una empresa que cofundé. Creamos
software para videoconferencia grupal. Marratech fue adquirida por Google en 2007.
Luego pasaría a trabajar en el proyecto que informaría WebRTC.

### El primer proyecto de Google
El primer proyecto en el que trabajó el futuro equipo de WebRTC fue voz y
chat de video de Gmail. Obtener audio y video en el navegador no fue una tarea fácil.

### Nace WebRTC
Para mí, WebRTC nació con algunas motivaciones. Combinadas, dieron origen al
esfuerzo.

No debería ser tan difícil construir experiencias RTC. Se desperdicia tanto esfuerzo
reimplementando la misma cosa por diferentes desarrolladores.

La comunicación humana debería ser sin trabas y debería ser abierta. ¿Cómo está bien que
el texto y HTML sean abiertos, pero mi voz y mi imagen en tiempo real no lo sean?

La seguridad es una prioridad. Este también era
una oportunidad para hacer un protocolo que fuera seguro por defecto.

### El futuro
WebRTC está en un gran lugar hoy. Hay muchos cambios iterativos
sucediendo, pero nada en particular en lo que he estado trabajando.

Estoy más emocionado por lo que la computación en la nube puede hacer por la comunicación. Usando
algoritmos avanzados podemos eliminar el ruido de fondo de una llamada y hacer
la comunicación posible donde no lo era antes.
