---
title: Conexión
type: docs
weight: 4
---

# Conexión

## ¿Por qué WebRTC necesita un subsistema dedicado para conectarse?

La mayoría de las aplicaciones implementadas hoy en día establecen conexiones cliente/servidor. Una conexión cliente/servidor requiere que el servidor tenga una dirección de transporte estable y bien conocida. Un cliente contacta a un servidor, y el servidor responde.

WebRTC no usa un modelo cliente/servidor, establece conexiones peer-to-peer (P2P). En una conexión P2P, la tarea de crear una conexión se distribuye equitativamente entre ambos pares. Esto se debe a que una dirección de transporte (IP y puerto) en WebRTC no se puede asumir, e incluso puede cambiar durante la sesión. WebRTC recopilará toda la información que pueda e irá a grandes esfuerzos para lograr comunicación bidireccional entre dos Agentes WebRTC.

Sin embargo, establecer conectividad peer-to-peer puede ser difícil. Estos agentes podrían estar en diferentes redes sin conectividad directa. En situaciones donde existe conectividad directa, aún puedes tener otros problemas. En algunos casos, tus clientes no hablan los mismos protocolos de red (UDP <-> TCP) o tal vez usan diferentes versiones de IP (IPv4 <-> IPv6).

A pesar de estas dificultades para establecer una conexión P2P, obtienes ventajas sobre la tecnología cliente/servidor tradicional debido a los siguientes atributos que WebRTC ofrece.

### Costos de Ancho de Banda Reducidos

Dado que la comunicación de medios ocurre directamente entre pares, no tienes que pagar por, u hospedar un servidor separado para transmitir medios.

### Menor Latencia

La comunicación es más rápida cuando es directa. Cuando un usuario tiene que ejecutar todo a través de tu servidor, hace que las transmisiones sean más lentas.

### Comunicación E2E Segura

La comunicación directa es más segura. Dado que los usuarios no están enrutando datos a través de tu servidor, ni siquiera necesitan confiar en que no los descifrarás.

## ¿Cómo funciona?

El proceso descrito anteriormente se llama Establecimiento de Conectividad Interactiva ([ICE](https://tools.ietf.org/html/rfc8445)). Otro protocolo que es anterior a WebRTC.

ICE es un protocolo que intenta encontrar la mejor manera de comunicarse entre dos Agentes ICE. Cada Agente ICE publica las formas en que es accesible, estas se conocen como candidatos. Un candidato es esencialmente una dirección de transporte del agente que cree que el otro par puede alcanzar. ICE entonces determina el mejor emparejamiento de candidatos.

El proceso ICE real se describe con mayor detalle más adelante en este capítulo. Para entender por qué existe ICE, es útil entender qué comportamientos de red estamos superando.

## Restricciones de redes del mundo real
ICE se trata de superar las restricciones de las redes del mundo real. Antes de explorar la solución, hablemos de los problemas reales.

### No en la misma red
La mayor parte del tiempo el otro Agente WebRTC ni siquiera estará en la misma red. Una llamada típica suele ser entre dos Agentes WebRTC en diferentes redes sin conectividad directa.

A continuación se muestra un gráfico de dos redes distintas, conectadas a través de Internet público. En cada red tienes dos hosts.

![Dos redes](../../images/03-two-networks.png "Dos redes")

Para los hosts en la misma red es muy fácil conectarse. ¡La comunicación entre `192.168.0.1 -> 192.168.0.2` es fácil de hacer! Estos dos hosts pueden conectarse entre sí sin ninguna ayuda externa.

Sin embargo, un host usando `Router B` no tiene forma de acceder directamente a nada detrás de `Router A`. ¿Cómo distinguirías entre `192.168.0.1` detrás de `Router A` y la misma IP detrás de `Router B`? ¡Son IPs privadas! Un host usando `Router B` podría enviar tráfico directamente a `Router A`, pero la solicitud terminaría ahí. ¿Cómo sabe `Router A` a qué host debe reenviar el mensaje?

### Restricciones de Protocolo
Algunas redes no permiten tráfico UDP en absoluto, o tal vez no permiten TCP. Algunas redes pueden tener un MTU (Unidad Máxima de Transmisión) muy bajo. Hay muchas variables que los administradores de red pueden cambiar que pueden dificultar la comunicación.

### Reglas de Firewall/IDS
Otra es la "Inspección Profunda de Paquetes" y otro filtrado inteligente. Algunos administradores de red ejecutarán software que intenta procesar cada paquete. Muchas veces este software no entiende WebRTC, por lo que lo bloquea porque no sabe qué hacer, por ejemplo, tratando los paquetes WebRTC como paquetes UDP sospechosos en un puerto arbitrario que no está en la lista blanca.

## Mapeo NAT
El mapeo NAT (Traducción de Direcciones de Red) es la magia que hace posible la conectividad de WebRTC. Así es como WebRTC permite que dos pares en subredes completamente diferentes se comuniquen, abordando el problema de "no en la misma red" anterior. Si bien crea nuevos desafíos, expliquemos cómo funciona el mapeo NAT en primer lugar.

No utiliza un relé, proxy o servidor. Nuevamente tenemos `Agente 1` y `Agente 2` y están en diferentes redes. Sin embargo, el tráfico fluye completamente. Visualizado se ve así:

![Mapeo NAT](../../images/03-nat-mapping.png "Mapeo NAT")

Para que esta comunicación suceda, estableces un mapeo NAT. El Agente 1 usa el puerto 7000 para establecer una conexión WebRTC con el Agente 2. Esto crea un enlace de `192.168.0.1:7000` a `5.0.0.1:7000`. Esto permite que el Agente 2 alcance al Agente 1 enviando paquetes a `5.0.0.1:7000`. Crear un mapeo NAT como en este ejemplo es como una versión automatizada de hacer reenvío de puertos en tu enrutador.

La desventaja del mapeo NAT es que no hay una sola forma de mapeo (por ejemplo, reenvío de puertos estático), y el comportamiento es inconsistente entre redes. Los ISP y fabricantes de hardware pueden hacerlo de diferentes maneras. En algunos casos, los administradores de red pueden incluso deshabilitarlo.

La buena noticia es que se entiende y observa el rango completo de comportamientos, por lo que un Agente ICE puede confirmar que creó un mapeo NAT y los atributos del mapeo.

El documento que describe estos comportamientos es [RFC 4787](https://tools.ietf.org/html/rfc4787).

### Crear un mapeo
Crear un mapeo es la parte más fácil. ¡Cuando envías un paquete a una dirección fuera de tu red, se crea un mapeo! Un mapeo NAT es solo una IP pública temporal y un puerto que es asignado por tu NAT. El mensaje saliente se reescribirá para tener su dirección de origen dada por la dirección de mapeo recién creada. Si se envía un mensaje al mapeo, se enrutará automáticamente de vuelta al host dentro del NAT que lo creó. Los detalles sobre los mapeos es donde se vuelve complicado.

### Comportamientos de Creación de Mapeos
La creación de mapeos se divide en tres categorías diferentes:

#### Mapeo Independiente del Punto Final
Se crea un mapeo para cada remitente dentro del NAT. Si envías dos paquetes a dos direcciones remotas diferentes, el mapeo NAT se reutilizará. Ambos hosts remotos verían la misma IP y puerto de origen. Si los hosts remotos responden, se enviaría de vuelta al mismo oyente local.

Este es el mejor escenario posible. Para que una llamada funcione, al menos un lado DEBE ser de este tipo.

#### Mapeo Dependiente de la Dirección
Se crea un nuevo mapeo cada vez que envías un paquete a una nueva dirección. Si envías dos paquetes a diferentes hosts, se crearán dos mapeos. Si envías dos paquetes al mismo host remoto pero diferentes puertos de destino, NO se creará un nuevo mapeo.

#### Mapeo Dependiente de Dirección y Puerto
Se crea un nuevo mapeo si la IP o el puerto remoto es diferente. Si envías dos paquetes al mismo host remoto, pero diferentes puertos de destino, se creará un nuevo mapeo.

### Comportamientos de Filtrado de Mapeos
El filtrado de mapeos son las reglas sobre quién puede usar el mapeo. Se dividen en tres clasificaciones similares:

#### Filtrado Independiente del Punto Final
Cualquiera puede usar el mapeo. Puedes compartir el mapeo con múltiples otros pares, y todos podrían enviar tráfico a él.

#### Filtrado Dependiente de la Dirección
Solo el host para el que se creó el mapeo puede usar el mapeo. Si envías un paquete al host `A` solo puedes obtener una respuesta de ese mismo host. Si el host `B` intenta enviar un paquete a ese mapeo, será ignorado.

#### Filtrado Dependiente de Dirección y Puerto
Solo el host y puerto para el que se creó el mapeo pueden usar ese mapeo. Si envías un paquete a `A:5000` solo puedes obtener una respuesta de ese mismo host y puerto. Si `A:5001` intenta enviar un paquete a ese mapeo, será ignorado.

### Actualización de Mapeos
Se recomienda que si un mapeo no se usa durante 5 minutos, debe ser destruido. Esto depende completamente del ISP o fabricante de hardware.

## STUN
STUN (Utilidades de Traversal de Sesión para NAT) es un protocolo que fue creado solo para trabajar con NATs. Esta es otra tecnología que es anterior a WebRTC (¡y a ICE!). Está definido por [RFC 8489](https://tools.ietf.org/html/rfc8489), que también define la estructura del paquete STUN. El protocolo STUN también es utilizado por ICE/TURN.

STUN es útil porque permite la creación programática de Mapeos NAT. Antes de STUN, podíamos crear un mapeo NAT, ¡pero no teníamos idea de cuál era la IP y el puerto! STUN no solo te da la capacidad de crear un mapeo, sino que también te da los detalles para que puedas compartirlos con otros, para que puedan enviarte tráfico de vuelta a través del mapeo que acabas de crear.

Comencemos con una descripción básica de STUN. Más tarde, ampliaremos el uso de TURN e ICE. Por ahora, solo vamos a describir el flujo de Solicitud/Respuesta para crear un mapeo. Luego hablaremos sobre cómo obtener los detalles para compartir con otros. Este es el proceso que ocurre cuando tienes un servidor `stun:` en tus URLs ICE para una PeerConnection de WebRTC. En pocas palabras, STUN ayuda a un punto final detrás de un NAT a descubrir qué mapeo fue creado al pedirle a un servidor STUN fuera del NAT que informe lo que observa.

### Estructura del Protocolo
Cada paquete STUN tiene la siguiente estructura:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|0 0|     STUN Message Type     |         Message Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Magic Cookie                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     Transaction ID (96 bits)                  |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Tipo de Mensaje STUN
Cada paquete STUN tiene un tipo. Por ahora, solo nos importan los siguientes:

* Solicitud de Enlace (Binding Request) - `0x0001`
* Respuesta de Enlace (Binding Response) - `0x0101`

Para crear un mapeo NAT hacemos una `Solicitud de Enlace`. Luego el servidor responde con una `Respuesta de Enlace`.

#### Longitud del Mensaje
Esto es cuán larga es la sección `Data`. Esta sección contiene datos arbitrarios que son definidos por el `Tipo de Mensaje`.

#### Magic Cookie
El valor fijo `0x2112A442` en orden de bytes de red, ayuda a distinguir el tráfico STUN de otros protocolos.

#### ID de Transacción
Un identificador de 96 bits que identifica únicamente una solicitud/respuesta. Esto te ayuda a emparejar tus solicitudes y respuestas.

#### Data
Data contendrá una lista de atributos STUN. Un Atributo STUN tiene la siguiente estructura:

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

La `Solicitud de Enlace STUN` no usa atributos. Esto significa que una `Solicitud de Enlace STUN` contiene solo el encabezado.

La `Respuesta de Enlace STUN` usa un `XOR-MAPPED-ADDRESS (0x0020)`. Este atributo contiene una IP y puerto. ¡Esta es la IP y el puerto del mapeo NAT que se crea!

### Crear un Mapeo NAT
¡Crear un mapeo NAT usando STUN solo requiere enviar una solicitud! Envías una `Solicitud de Enlace STUN` al Servidor STUN. El Servidor STUN entonces responde con una `Respuesta de Enlace STUN`.
Esta `Respuesta de Enlace STUN` contendrá la `Dirección Mapeada`. La `Dirección Mapeada` es cómo el Servidor STUN te ve y es tu `mapeo NAT`.
La `Dirección Mapeada` es lo que compartirías si quisieras que alguien te envíe paquetes.

La gente también llamará a la `Dirección Mapeada` tu `IP Pública` o `Candidato Reflexivo del Servidor`.

### Determinar el Tipo de NAT
Desafortunadamente, la `Dirección Mapeada` puede no ser útil en todos los casos. Si es `Dependiente de la Dirección`, solo el servidor STUN puede enviarte tráfico de vuelta. Si la compartes y otro par intenta enviar mensajes, serán descartados. Esto lo hace inútil para comunicarse con otros. Puedes encontrar que el caso `Dependiente de la Dirección` es de hecho solucionable, ¡si el host que ejecuta el servidor STUN también puede reenviar paquetes para ti al par! Esto nos lleva a la solución usando TURN a continuación.

[RFC 5780](https://tools.ietf.org/html/rfc5780) define un método para ejecutar una prueba para determinar tu Tipo de NAT. Esto es útil porque sabrías de antemano si la conectividad directa es posible.

## TURN
TURN (Traversal Usando Relés alrededor de NAT) está definido en [RFC 8656](https://tools.ietf.org/html/rfc8656) y es la solución cuando la conectividad directa no es posible. Puede ser porque tienes dos Tipos de NAT que son incompatibles, ¡o tal vez no pueden hablar el mismo protocolo! TURN también se puede usar para propósitos de privacidad. Al ejecutar toda tu comunicación a través de TURN, ocultas la dirección real del cliente.

TURN usa un servidor dedicado. Este servidor actúa como un proxy para un cliente. El cliente se conecta a un Servidor TURN y crea una `Asignación`. Al crear una asignación, un cliente obtiene un IP/Puerto/Protocolo temporal que se puede usar para enviar tráfico de vuelta al cliente. Este nuevo oyente se conoce como la `Dirección de Transporte Retransmitida`. ¡Piensa en ella como una dirección de reenvío, la das para que otros puedan enviarte tráfico a través de TURN! Para cada par al que le das la `Dirección de Transporte de Relé`, debes crear un nuevo `Permiso` para permitir la comunicación contigo.

Cuando envías tráfico saliente a través de TURN, se envía a través de la `Dirección de Transporte Retransmitida`. Cuando un par remoto recibe tráfico, lo ve venir del Servidor TURN.

### Ciclo de Vida de TURN
Lo siguiente es todo lo que un cliente que desea crear una asignación TURN tiene que hacer. Comunicarse con alguien que está usando TURN no requiere cambios. El otro par obtiene una IP y puerto, y se comunica con ella como cualquier otro host.

#### Asignaciones
Las asignaciones están en el núcleo de TURN. Una `asignación` es básicamente una "Sesión TURN". Para crear una asignación TURN, te comunicas con la `Dirección de Transporte del Servidor` TURN (generalmente puerto `3478`).

Al crear una asignación, necesitas proporcionar lo siguiente:
* Nombre de Usuario/Contraseña - Crear asignaciones TURN requiere autenticación.
* Transporte de Asignación - El protocolo de transporte entre el servidor (`Dirección de Transporte Retransmitida`) y los pares, puede ser UDP o TCP.
* Even-Port - Puedes solicitar puertos secuenciales para múltiples asignaciones, no relevante para WebRTC.

Si la solicitud tuvo éxito, obtienes una respuesta del Servidor TURN con los siguientes Atributos STUN en la sección Data:
* `XOR-MAPPED-ADDRESS` - `Dirección Mapeada` del `Cliente TURN`. Cuando alguien envía datos a la `Dirección de Transporte Retransmitida`, aquí es donde se reenvía.
* `RELAYED-ADDRESS` - Esta es la dirección que das a otros clientes. Si alguien envía un paquete a esta dirección, se retransmite al cliente TURN.
* `LIFETIME` - Cuánto tiempo hasta que esta Asignación TURN sea destruida. Puedes extender el tiempo de vida enviando una solicitud `Refresh`.

#### Permisos
Un host remoto no puede enviar a tu `Dirección de Transporte Retransmitida` hasta que crees un permiso para ellos. Cuando creas un permiso, le estás diciendo al servidor TURN que esta IP y puerto pueden enviar tráfico entrante.

El host remoto necesita darte la IP y el puerto tal como aparece en el servidor TURN. Esto significa que debe enviar una `Solicitud de Enlace STUN` al Servidor TURN. Un caso de error común es que un host remoto enviará una `Solicitud de Enlace STUN` a un servidor diferente. Luego te pedirán que crees un permiso para esta IP.

Digamos que quieres crear un permiso para un host detrás de un `Mapeo Dependiente de la Dirección`. Si generas la `Dirección Mapeada` desde un servidor TURN diferente, todo el tráfico entrante será descartado. Cada vez que se comunican con un host diferente, genera un nuevo mapeo. Los permisos expiran después de 5 minutos si no se actualizan.

#### SendIndication/ChannelData
Estos dos mensajes son para que el Cliente TURN envíe mensajes a un par remoto.

SendIndication es un mensaje autocontenido. Dentro está los datos que deseas enviar, y a quién deseas enviarlo. Esto es derrochador si estás enviando muchos mensajes a un par remoto. Si envías 1,000 mensajes repetirás su Dirección IP 1,000 veces.

ChannelData te permite enviar datos, pero sin repetir una Dirección IP. Creas un Canal con una IP y puerto. Luego envías con el ChannelId, y la IP y puerto se completarán del lado del servidor. Esta es la mejor opción si estás enviando muchos mensajes.

#### Actualización
Las asignaciones se destruirán automáticamente. El Cliente TURN debe actualizarlas antes del `LIFETIME` dado al crear la asignación.

### Uso de TURN
El uso de TURN existe en dos formas. Usualmente, tienes un par actuando como un "Cliente TURN" y el otro lado comunicándose directamente. En algunos casos, puedes tener uso de TURN en ambos lados, por ejemplo, porque ambos clientes están en redes que bloquean UDP y, por lo tanto, la conexión a los respectivos servidores TURN ocurre a través de TCP.

Estos diagramas ayudan a ilustrar cómo se vería eso.

#### Una Asignación TURN para Comunicación

![Una asignación TURN](../../images/03-one-turn-allocation.png "Una asignación TURN")

#### Dos Asignaciones TURN para Comunicación

![Dos asignaciones TURN](../../images/03-two-turn-allocations.png "Dos asignaciones TURN")

## ICE
ICE (Establecimiento de Conectividad Interactiva) es cómo WebRTC conecta dos Agentes. Definido en [RFC 8445](https://tools.ietf.org/html/rfc8445), ¡esta es otra tecnología que es anterior a WebRTC! ICE es un protocolo para establecer conectividad. Determina todas las rutas posibles entre los dos pares y luego asegura que te mantengas conectado.

Estas rutas se conocen como `Pares de Candidatos`, que es un emparejamiento de una dirección de transporte local y remota. Aquí es donde STUN y TURN entran en juego con ICE. Estas direcciones pueden ser tu Dirección IP local más un puerto, `mapeo NAT`, o `Dirección de Transporte Retransmitida`. Cada lado recopila todas las direcciones que quieren usar, las intercambian, ¡y luego intentan conectarse!

Dos Agentes ICE se comunican usando paquetes de ping ICE (o formalmente llamados verificaciones de conectividad) para establecer conectividad. Después de que se establece la conectividad, pueden enviar los datos que quieran. Será como usar un socket normal. Estas verificaciones usan el protocolo STUN.

### Crear un Agente ICE
Un Agente ICE es `Controlador` o `Controlado`. El Agente `Controlador` es el que decide el `Par de Candidatos` seleccionado. Generalmente, el par que envía la oferta es el lado controlador.

Cada lado debe tener un `fragmento de usuario` y una `contraseña`. Estos dos valores deben intercambiarse antes de que puedan comenzar las verificaciones de conectividad. El `fragmento de usuario` se envía en texto plano y es útil para demultiplexar múltiples Sesiones ICE.
La `contraseña` se usa para generar un atributo `MESSAGE-INTEGRITY`. Al final de cada paquete STUN, hay un atributo que es un hash de todo el paquete usando la `contraseña` como clave. Esto se usa para autenticar el paquete y asegurar que no haya sido manipulado.

Para WebRTC, todos estos valores se distribuyen a través de la `Descripción de Sesión` como se describe en el capítulo anterior.

### Recopilación de Candidatos
Ahora necesitamos recopilar todas las direcciones posibles en las que somos accesibles. Estas direcciones se conocen como candidatos.

#### Host
Un candidato Host está escuchando directamente en una interfaz local. Esto puede ser UDP o TCP.

#### mDNS
Un candidato mDNS es similar a un candidato host, pero la dirección IP está oculta. En lugar de informar al otro lado sobre tu dirección IP, le das un UUID como nombre de host. Luego configuras un oyente de multidifusión y respondes si alguien solicita el UUID que publicaste.

Si estás en la misma red que el agente, pueden encontrarse entre sí a través de Multidifusión. Si no estás en la misma red, no podrás conectarte (a menos que el administrador de red configuró explícitamente la red para permitir que los paquetes de Multidifusión atraviesen).

Esto es útil para propósitos de privacidad. Un usuario podría descubrir tu dirección IP local a través de WebRTC con un candidato Host (sin siquiera intentar conectarse a ti), pero con un candidato mDNS, ahora solo obtienen un UUID aleatorio.

#### Reflexivo del Servidor
Un candidato Reflexivo del Servidor se genera haciendo una `Solicitud de Enlace STUN` a un Servidor STUN.

Cuando obtienes la `Respuesta de Enlace STUN`, el `XOR-MAPPED-ADDRESS` es tu Candidato Reflexivo del Servidor.

#### Reflexivo del Par
Un candidato Reflexivo del Par se crea cuando el par remoto recibe tu solicitud desde una dirección previamente desconocida para el par. Al recibir, el par informa (refleja) dicha dirección de vuelta a ti. El par sabe que la solicitud fue enviada por ti y no por alguien más porque ICE es un protocolo autenticado.

Esto comúnmente ocurre cuando un `Candidato Host` se comunica con un `Candidato Reflexivo del Servidor` que está en una subred diferente, lo que resulta en la creación de un nuevo `mapeo NAT`. Recuerda que dijimos que las verificaciones de conectividad son de hecho paquetes STUN. El formato de la respuesta STUN naturalmente permite que un par informe de vuelta la dirección reflexiva del par.

#### Relé
Un Candidato de Relé se genera usando un Servidor TURN.

Después del handshake inicial con el Servidor TURN, se te da una `RELAYED-ADDRESS`, este es tu Candidato de Relé.

### Verificaciones de Conectividad
¡Ahora conocemos el `fragmento de usuario`, `contraseña` y candidatos del agente remoto. Ahora podemos intentar conectar! Cada candidato se empareja entre sí. Así que si tienes 3 candidatos en cada lado, ahora tienes 9 pares de candidatos.

Visualmente se ve así:

![Verificaciones de conectividad](../../images/03-connectivity-checks.png "Verificaciones de conectividad")

### Selección de Candidatos
El Agente Controlador y Controlado comienzan a enviar tráfico en cada par. Esto es necesario si un Agente está detrás de un `Mapeo Dependiente de la Dirección`, esto causará que se cree un `Candidato Reflexivo del Par`.

Cada `Par de Candidatos` que vio tráfico de red es entonces promovido a un par `Candidato Válido`. El Agente Controlador luego toma un par `Candidato Válido` y lo nomina. Este se convierte en el `Par Nominado`. El Agente Controlador y Controlado luego intentan una ronda más de comunicación bidireccional. Si eso tiene éxito, ¡el `Par Nominado` se convierte en el `Par de Candidatos Seleccionado`! Este par se usa luego para el resto de la sesión.

### Reinicios
Si el `Par de Candidatos Seleccionado` deja de funcionar por cualquier razón (el mapeo NAT expira, el Servidor TURN falla), el Agente ICE pasará al estado `Failed`. Ambos agentes pueden reiniciarse y harán todo el proceso de nuevo.
