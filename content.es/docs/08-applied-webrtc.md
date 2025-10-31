---
title: WebRTC Aplicado
type: docs
weight: 9
---

# WebRTC Aplicado
Ahora que sabes cómo funciona WebRTC, ¡es hora de construir con él! Este capítulo explora qué están
construyendo las personas con WebRTC y cómo lo están construyendo. Aprenderás todas las cosas interesantes que están
sucediendo con WebRTC. El poder de WebRTC viene con un costo. Construir servicios WebRTC de grado producción es
desafiante. Este capítulo intentará explicar esos desafíos antes de que los encuentres.

## Por Caso de Uso
Muchos piensan que WebRTC es solo una tecnología para conferencias en el navegador web. ¡Es mucho más que eso!
WebRTC se usa en una amplia gama de aplicaciones. Nuevos casos de uso están apareciendo todo el tiempo. En este capítulo enumeraremos algunos comunes y cómo WebRTC los está revolucionando.

### Conferencias
Las conferencias son el caso de uso original para WebRTC. El protocolo contiene algunas características necesarias que ningún otro protocolo ofrece
en el navegador. Podrías construir un sistema de conferencias con WebSockets y podría funcionar en condiciones óptimas. Si quieres
algo que pueda implementarse en condiciones de red del mundo real, WebRTC es la mejor opción.

WebRTC proporciona control de congestión y tasa de bits adaptativa para medios. A medida que las condiciones de la red cambian, los usuarios seguirán obteniendo la
mejor experiencia posible. Los desarrolladores tampoco tienen que escribir ningún código adicional para medir estas condiciones.

Los participantes pueden enviar y recibir múltiples flujos. También pueden agregar y eliminar esos flujos en cualquier momento durante la llamada. Los códecs se negocian
también. Toda esta funcionalidad es proporcionada por el navegador, no se requiere que el desarrollador escriba código personalizado.

Las conferencias también se benefician de los canales de datos. Los usuarios pueden enviar metadatos o compartir documentos. Puedes crear múltiples flujos
y configurarlos si necesitas rendimiento más que confiabilidad.

### Transmisión
Muchos proyectos nuevos están comenzando a aparecer en el espacio de transmisión que usan WebRTC. El protocolo tiene mucho que ofrecer tanto para el publicador
como para el consumidor de medios.

WebRTC estar en el navegador facilita que los usuarios publiquen video. Elimina el requisito de que los usuarios descarguen un nuevo cliente.
Cualquier plataforma que tenga un navegador web puede publicar video. Los publicadores pueden entonces enviar múltiples pistas y modificarlas o eliminarlas en cualquier momento. Esta es
una gran mejora sobre los protocolos heredados que solo permitían una pista de audio o una pista de video por conexión.

WebRTC les da a los desarrolladores un mayor control sobre los compromisos entre latencia y calidad. Si es más importante que la latencia nunca exceda un
cierto umbral, y estás dispuesto a tolerar algunos artefactos de decodificación. Puedes configurar el visor para reproducir medios tan pronto como
lleguen. Con otros protocolos que se ejecutan sobre TCP, eso no es tan fácil. En el navegador puedes solicitar datos y eso es todo.

### Acceso Remoto
El Acceso Remoto es cuando accedes remotamente a otra computadora a través de WebRTC. Podrías tener control completo del host remoto, o tal vez solo una
aplicación individual. Esto es genial para ejecutar tareas computacionalmente costosas cuando el hardware local no puede hacerlo. Como ejecutar un nuevo videojuego, o
software CAD. WebRTC pudo revolucionar el espacio de tres maneras.

WebRTC puede usarse para acceder remotamente a un host que no es enrutable mundialmente. Con NAT Traversal puedes acceder a una computadora que solo está disponible
a través de STUN. Esto es genial para seguridad y privacidad. Tus usuarios no tienen que enrutar video a través de una ingesta, o una "caja de salto". NAT Traversal también
hace que las implementaciones sean más fáciles. No tienes que preocuparte por el reenvío de puertos o configurar una IP estática con anticipación.

Los canales de datos también son realmente poderosos en este escenario. Pueden configurarse para que solo se acepten los datos más recientes. Con TCP corres el
riesgo de encontrar bloqueo Head-of-line. Un clic de mouse o pulsación de tecla antiguo podría llegar tarde y bloquear los subsiguientes de ser aceptados.
Los canales de datos de WebRTC están diseñados para manejar esto y pueden configurarse para no reenviar paquetes perdidos. También puedes medir la contrapresión y
asegurarte de que no estás enviando más datos de los que tu red soporta.

WebRTC estar disponible en el navegador ha sido una gran mejora de calidad de vida. No tienes que descargar un cliente propietario para iniciar la
sesión. Cada vez más clientes vienen con WebRTC incluido, las Smart TVs están obteniendo navegadores web completos ahora.

### Compartir Archivos y Elusión de Censura
Compartir Archivos y Elusión de Censura son problemas dramáticamente diferentes. Sin embargo, WebRTC resuelve los mismos problemas para ambos. Los hace
a ambos fácilmente disponibles y más difíciles de bloquear.

El primer problema que WebRTC resuelve es obtener el cliente. Si quieres unirte a una red de intercambio de archivos, necesitas descargar el cliente. Incluso si
la red está distribuida, aún necesitas obtener el cliente primero. En una red restringida, la descarga a menudo será bloqueada. Incluso si puedes
descargarlo, el usuario puede no ser capaz de instalar y ejecutar el cliente. WebRTC está disponible en cada navegador web, ya lo que hace que esté fácilmente disponible.

El segundo problema que WebRTC resuelve es que tu tráfico sea bloqueado. Si usas un protocolo que es solo para compartir archivos o elusión de censura
es mucho más fácil bloquearlo. Dado que WebRTC es un protocolo de propósito general, bloquearlo impactaría a todos. Bloquear WebRTC podría evitar que otros
usuarios de la red se unan a llamadas de conferencia.

### Internet de las Cosas
Internet de las Cosas (IoT) cubre algunos casos de uso diferentes. Para muchos esto significa cámaras de seguridad conectadas a la red. Usando WebRTC puedes transmitir el video a otro par WebRTC
como tu teléfono o un navegador. Otro caso de uso es tener dispositivos que se conecten e intercambien datos de sensores. Puedes tener dos dispositivos en tu LAN
que intercambien lecturas de clima, ruido o luz.

WebRTC tiene una gran ventaja de privacidad aquí sobre los protocolos de transmisión de video heredados. Dado que WebRTC admite conectividad P2P, la cámara puede enviar el video
directamente a tu navegador. No hay razón para que tu video sea enviado a un servidor de terceros. Incluso cuando el video está cifrado, un atacante puede hacer
suposiciones a partir de los metadatos de la llamada.

La interoperabilidad es otra ventaja para el espacio IoT. WebRTC está disponible en muchos lenguajes diferentes; C#, C++, C, Go, Java, Python, Rust
y TypeScript. Esto significa que puedes usar el lenguaje que mejor funcione para ti. Tampoco tienes que recurrir a protocolos o formatos propietarios
para poder conectar tus clientes.

### Puente de Protocolo de Medios
Tienes hardware y software existente que está produciendo video, pero aún no puedes actualizarlo. Esperar que los usuarios descarguen un cliente propietario
para ver videos es frustrante. La respuesta es ejecutar un puente WebRTC. El puente traduce entre los dos protocolos para que los usuarios puedan usar el
navegador con tu configuración heredada.

Muchos de los formatos con los que los desarrolladores hacen puentes usan los mismos protocolos que WebRTC. SIP comúnmente se expone a través de WebRTC y permite a los usuarios hacer llamadas telefónicas
desde su navegador. RTSP se usa en muchas cámaras de seguridad heredadas. Ambos usan los mismos protocolos subyacentes (RTP y SDP) por lo que es computacionalmente barato
ejecutar. El puente solo se requiere para agregar o eliminar cosas que son específicas de WebRTC.

### Puente de Protocolo de Datos
Un navegador web solo puede hablar un conjunto restringido de protocolos. Puedes usar HTTP, WebSockets, WebRTC y QUIC. Si quieres conectarte
a cualquier otra cosa, necesitas usar un puente de protocolo. Un puente de protocolo es un servidor que convierte tráfico extranjero en algo que el navegador
puede acceder. Un ejemplo popular es usar SSH desde tu navegador para acceder a un servidor. Los canales de datos de WebRTC tienen dos ventajas sobre la competencia.

Los canales de datos de WebRTC permiten entrega no confiable y desordenada. En casos donde la baja latencia es crítica, esto es necesario. No quieres que los nuevos datos sean
bloqueados por datos antiguos, esto se conoce como bloqueo head-of-line. Imagina que estás jugando un shooter multijugador en primera persona. ¿Realmente te importa dónde estaba el
jugador hace dos segundos? Si esos datos no llegaron a tiempo, no tiene sentido seguir intentando enviarlos. La entrega no confiable y desordenada te permite
usar los datos tan pronto como lleguen.

Los canales de datos también proporcionan presión de retroalimentación. Esto te dice si estás enviando datos más rápido de lo que tu conexión puede soportar. Entonces tienes dos
opciones cuando esto sucede. El canal de datos puede configurarse para almacenar en búfer y entregar los datos tarde, o puedes descartar los datos que no han llegado
en tiempo real.

### Teleoperación
La teleoperación es el acto de controlar un dispositivo remotamente a través de canales de datos WebRTC, y enviar el video de vuelta a través de RTP. Los desarrolladores están conduciendo autos remotamente
a través de WebRTC hoy. Esto se usa para controlar robots en sitios de construcción y entregar paquetes. Usar WebRTC para estos problemas tiene sentido por dos razones.

La ubicuidad de WebRTC facilita dar control a los usuarios. Todo lo que el usuario necesita es un navegador web y un dispositivo de entrada. Los navegadores incluso
admiten tomar entrada de joysticks y gamepads. WebRTC elimina completamente la necesidad de instalar un cliente adicional en el dispositivo del usuario.

### CDN Distribuido
Los CDNs distribuidos son un subconjunto del intercambio de archivos. Los archivos que se distribuyen son configurados por el operador del CDN en su lugar. Cuando los usuarios se unen a la red CDN
pueden descargar y compartir los archivos permitidos. Los usuarios obtienen todos los mismos beneficios que el intercambio de archivos.

Estos CDNs funcionan muy bien cuando estás en una oficina con mala conectividad externa, pero gran conectividad LAN. Puedes tener un usuario que descargue un video, y
luego lo comparta con todos los demás. Dado que no todos están intentando obtener el mismo archivo a través de la red externa, la transferencia se completará más rápido.

## Topologías WebRTC
WebRTC es un protocolo para conectar dos agentes, entonces, ¿cómo están los desarrolladores conectando cientos de personas a la vez? Hay algunas maneras diferentes
en que puedes hacerlo, y todas tienen pros y contras. Estas soluciones se dividen ampliamente en dos categorías; Peer-to-Peer o Cliente/Servidor. La
flexibilidad de WebRTC nos permite crear ambos.

### Uno-a-Uno
Uno-a-Uno es el primer tipo de conexión que usarás con WebRTC. Conectas dos Agentes WebRTC directamente y pueden enviar medios y datos bidireccionales.
La conexión se ve así.

![Uno-a-Uno](../../images/08-one-to-one.png "Uno-a-Uno")

### Malla Completa
La malla completa es la respuesta si quieres construir una llamada de conferencia o un juego multijugador. En esta topología, cada usuario establece una conexión
con cada otro usuario directamente. Esto te permite construir tu aplicación, pero viene con algunas desventajas.

En una topología de Malla Completa, cada usuario está conectado directamente. Eso significa que tienes que codificar y cargar video independientemente para cada miembro de la llamada.
Las condiciones de red entre cada conexión serán diferentes, por lo que no puedes reutilizar el mismo video. El manejo de errores también es difícil en estas
implementaciones. Necesitas considerar cuidadosamente si has perdido conectividad completa, o solo conectividad con un par remoto.

Debido a estas preocupaciones, una Malla Completa se usa mejor para grupos pequeños. Para cualquier cosa más grande, una topología cliente/servidor es mejor.

![Malla completa](../../images/08-full-mesh.png "Malla completa")

### Malla Híbrida
La Malla Híbrida es una alternativa a la Malla Completa que puede aliviar algunos de los problemas de la Malla Completa. En una Malla Híbrida, las conexiones no se establecen
entre cada usuario. En su lugar, los medios se retransmiten a través de pares en la red. Esto significa que el creador de los medios no tiene que usar tanto
ancho de banda para distribuir medios.

Esto tiene algunas desventajas. En esta configuración, el creador original de los medios no tiene idea de a quién se está enviando su video, ni si
llegó con éxito. También tendrás un aumento en la latencia con cada salto en tu red de Malla Híbrida.

![Malla híbrida](../../images/08-hybrid-mesh.png "Malla híbrida")

### Unidad de Reenvío Selectivo
Un SFU (Unidad de Reenvío Selectivo) también resuelve los problemas de Malla Completa, pero de una manera completamente diferente. Un SFU implementa una topología cliente/servidor, en lugar de P2P.
Cada par WebRTC se conecta al SFU y carga sus medios. El SFU luego reenvía estos medios a cada cliente conectado.

Con un SFU, cada Agente WebRTC solo tiene que codificar y cargar su video una vez. La carga de distribuirlo a todos los espectadores está en el SFU.
La conectividad con un SFU también es mucho más fácil que P2P. Puedes ejecutar un SFU en una dirección enrutable mundialmente, lo que hace que sea mucho más fácil para los clientes conectarse.
No necesitas preocuparte por Mapeos NAT. Aún necesitas asegurarte de que tu SFU esté disponible a través de TCP (ya sea a través de ICE-TCP o TURN).

Construir un SFU simple se puede hacer en un fin de semana. Construir un buen SFU que pueda manejar todo tipo de clientes es una tarea interminable. Ajustar el Control de Congestión, la Corrección de
Errores y el Rendimiento es una tarea que nunca termina.

![Unidad de Reenvío Selectivo](../../images/08-sfu.png "Unidad de Reenvío Selectivo")

### MCU
Un MCU (Unidad de Conferencia Multipunto) es una topología cliente/servidor como un SFU, pero compone los flujos de salida. En lugar de distribuir los medios salientes
sin modificar, los recodifica como una sola transmisión.

![Unidad de Conferencia Multipunto](../../images/08-mcu.png "Unidad de Conferencia Multipunto")
