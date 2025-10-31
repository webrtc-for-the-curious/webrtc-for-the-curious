---
title: Seguridad
type: docs
weight: 5
---

# Seguridad

## ¿Qué seguridad tiene WebRTC?

Cada conexión WebRTC está autenticada y cifrada. Puedes estar seguro de que un tercero no puede ver lo que estás enviando ni insertar mensajes falsos. También puedes estar seguro de que el Agente WebRTC que generó la Descripción de Sesión es con quien te estás comunicando.

Es muy importante que nadie manipule esos mensajes. Está bien si un tercero lee la Descripción de Sesión en tránsito. Sin embargo, WebRTC no tiene protección contra su modificación. Un atacante podría realizar un ataque de intermediario (man-in-the-middle) cambiando los Candidatos ICE y actualizando la Huella Digital del Certificado.

## ¿Cómo funciona?
WebRTC usa dos protocolos preexistentes, Seguridad de la Capa de Transporte de Datagramas ([DTLS](https://tools.ietf.org/html/rfc6347)) y el Protocolo de Transporte en Tiempo Real Seguro ([SRTP](https://tools.ietf.org/html/rfc3711)).

DTLS te permite negociar una sesión y luego intercambiar datos de forma segura entre dos pares. Es un hermano de TLS, la misma tecnología que impulsa HTTPS, pero DTLS usa UDP en lugar de TCP como capa de transporte. Eso significa que el protocolo tiene que manejar entregas no confiables. SRTP está específicamente diseñado para intercambiar medios de forma segura. Hay algunas optimizaciones que podemos hacer al usarlo en lugar de DTLS.

DTLS se usa primero. Hace un handshake sobre la conexión proporcionada por ICE. DTLS es un protocolo cliente/servidor, por lo que un lado necesita iniciar el handshake. Los roles de Cliente/Servidor se eligen durante la señalización. Durante el handshake DTLS, ambos lados ofrecen un certificado.
Después de que se completa el handshake, este certificado se compara con el hash del certificado en la Descripción de Sesión. Esto es para asegurar que el handshake ocurrió con el Agente WebRTC que esperabas. La conexión DTLS está entonces disponible para ser utilizada para la comunicación DataChannel.

Para crear una sesión SRTP la inicializamos usando las claves generadas por DTLS. SRTP no tiene un mecanismo de handshake, por lo que tiene que ser iniciado con claves externas. Una vez que esto se hace, ¡los medios pueden ser intercambiados cifrados usando SRTP!

## Seguridad 101
Para entender la tecnología presentada en este capítulo necesitarás entender estos términos primero. La criptografía es un tema complicado, ¡así que valdría la pena consultar otras fuentes también!

### Texto Plano y Texto Cifrado

El texto plano es la entrada a un cifrador. El texto cifrado es la salida de un cifrador.

### Cifrador

Un cifrador es una serie de pasos que lleva el texto plano a texto cifrado. El cifrador puede ser revertido, para que puedas llevar tu texto cifrado de vuelta a texto plano. Un cifrador generalmente tiene una clave para cambiar su comportamiento. Otro término para esto es cifrar y descifrar.

Un cifrador simple es ROT13. Cada letra se mueve 13 caracteres hacia adelante. Para deshacer el cifrador mueves 13 caracteres hacia atrás. El texto plano `HELLO` se convertiría en el texto cifrado `URYYB`. En este caso, el Cifrador es ROT, y la clave es 13.

### Funciones Hash

Una función hash criptográfica es un proceso unidireccional que genera un resumen. Dado una entrada, genera la misma salida cada vez. Es importante que la salida *no* sea reversible. Si tienes una salida, no deberías poder determinar su entrada. El hash es útil cuando quieres confirmar que un mensaje no ha sido manipulado.

Una función hash simple (aunque ciertamente no adecuada para criptografía real) sería tomar solo cada dos letras. `HELLO` se convertiría en `HLO`. No puedes asumir que `HELLO` fue la entrada, pero puedes confirmar que `HELLO` coincidiría con el resumen hash.

### Criptografía de Clave Pública/Privada

La Criptografía de Clave Pública/Privada describe el tipo de cifradores que DTLS y SRTP usan. En este sistema, tienes dos claves, una clave pública y una privada. La clave pública es para cifrar mensajes y es seguro compartirla.
La clave privada es para descifrar, y nunca debe ser compartida. Es la única clave que puede descifrar los mensajes cifrados con la clave pública.

### Intercambio Diffie–Hellman

El intercambio Diffie–Hellman permite que dos usuarios que nunca se han conocido antes creen un secreto compartido de forma segura a través de Internet. El Usuario `A` puede enviar un secreto al Usuario `B` sin preocuparse por escuchas indiscretas. Esto depende de la dificultad de romper el problema del logaritmo discreto.
No necesitas entender completamente cómo funciona esto, pero ayuda saber que esto es lo que hace posible el handshake DTLS.

Wikipedia tiene un ejemplo de esto en acción [aquí](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation).

### Función Pseudoaleatoria

Una Función Pseudoaleatoria (PRF) es una función predefinida para generar un valor que aparece aleatorio. Puede tomar múltiples entradas y generar una única salida.

### Función de Derivación de Clave

La Derivación de Clave es un tipo de Función Pseudoaleatoria. La Derivación de Clave es una función que se usa para hacer una clave más fuerte. Un patrón común es el estiramiento de claves.

Digamos que te dan una clave de 8 bytes. Podrías usar una KDF para hacerla más fuerte.

### Nonce

Un nonce es una entrada adicional a un cifrador. Esto se usa para que puedas obtener una salida diferente del cifrador, incluso si estás cifrando el mismo mensaje varias veces.

Si cifras el mismo mensaje 10 veces, el cifrador te dará el mismo texto cifrado 10 veces. Al usar un nonce puedes obtener una salida diferente, mientras sigues usando la misma clave. ¡Es importante que uses un nonce diferente para cada mensaje! De lo contrario, niega gran parte del valor.

### Código de Autenticación de Mensajes

Un Código de Autenticación de Mensajes es un hash que se coloca al final de un mensaje. Un MAC prueba que el mensaje proviene del usuario que esperabas.

Si no usas un MAC, un atacante podría insertar mensajes inválidos. Después de descifrar solo tendrías basura porque no conocen la clave.

### Rotación de Claves

La Rotación de Claves es la práctica de cambiar tu clave en un intervalo. Esto hace que una clave robada tenga menos impacto. Si una clave es robada o filtrada, se pueden descifrar menos datos.

## DTLS
DTLS (Seguridad de la Capa de Transporte de Datagramas) permite que dos pares establezcan comunicación segura sin configuración preexistente. Incluso si alguien está escuchando la conversación, no podrán descifrar los mensajes.

Para que un Cliente DTLS y un Servidor se comuniquen, necesitan acordar un cifrador y la clave. Determinan estos valores haciendo un handshake DTLS. Durante el handshake, los mensajes están en texto plano.
Cuando un Cliente/Servidor DTLS ha intercambiado suficientes detalles para comenzar a cifrar, envía un `Change Cipher Spec`. ¡Después de este mensaje, cada mensaje subsiguiente será cifrado!

### Formato de Paquete
Cada paquete DTLS comienza con un encabezado.

#### Tipo de Contenido
Puedes esperar los siguientes tipos:

* `20` - Change Cipher Spec
* `22` - Handshake
* `23` - Application Data

`Handshake` se usa para intercambiar los detalles para iniciar la sesión. `Change Cipher Spec` se usa para notificar al otro lado que todo será cifrado. `Application Data` son los mensajes cifrados.

#### Versión
La versión puede ser `0x0000feff` (DTLS v1.0) o `0x0000fefd` (DTLS v1.2), no hay v1.1.

#### Época
La época comienza en `0`, pero se convierte en `1` después de un `Change Cipher Spec`. Cualquier mensaje con una época distinta de cero está cifrado.

#### Número de Secuencia
El Número de Secuencia se usa para mantener los mensajes en orden. Cada mensaje incrementa el Número de Secuencia. Cuando la época se incrementa, el Número de Secuencia comienza de nuevo.

#### Longitud y Carga Útil
La Carga Útil es específica del `Tipo de Contenido`. Para un `Application Data` la `Carga Útil` son los datos cifrados. Para `Handshake` será diferente dependiendo del mensaje. La longitud es para qué tan grande es la `Carga Útil`.

### Máquina de Estados del Handshake
Durante el handshake, el Cliente/Servidor intercambian una serie de mensajes. Estos mensajes se agrupan en vuelos. Cada vuelo puede tener múltiples mensajes (o solo uno).
Un Vuelo no está completo hasta que se han recibido todos los mensajes en el vuelo. Describiremos el propósito de cada mensaje con mayor detalle a continuación.

![Handshake](../../images/04-handshake.png "Handshake")

#### ClientHello
ClientHello es el mensaje inicial enviado por el cliente. Contiene una lista de atributos. Estos atributos le dicen al servidor los cifradores y características que el cliente soporta. Para WebRTC así es como elegimos el Cifrador SRTP también. También contiene datos aleatorios que se usarán para generar las claves para la sesión.

#### HelloVerifyRequest
HelloVerifyRequest es enviado por el servidor al cliente. Es para asegurarse de que el cliente tenía la intención de enviar la solicitud. El Cliente luego reenvía el ClientHello, pero con un token proporcionado en el HelloVerifyRequest.

#### ServerHello
ServerHello es la respuesta del servidor para la configuración de esta sesión. Contiene qué cifrador se usará cuando esta sesión termine. También contiene los datos aleatorios del servidor.

#### Certificate
Certificate contiene el certificado para el Cliente o Servidor. Esto se usa para identificar únicamente con quién nos estábamos comunicando. Después de que termine el handshake nos aseguraremos de que este certificado cuando se hashea coincida con la huella digital en la `SessionDescription`.

#### ServerKeyExchange/ClientKeyExchange
Estos mensajes se usan para transmitir la clave pública. Al inicio, el cliente y el servidor generan un par de claves. Después del handshake estos valores se usarán para generar el `Pre-Master Secret`.

#### CertificateRequest
Un CertificateRequest es enviado por el servidor notificando al cliente que quiere un certificado. El servidor puede Solicitar o Requerir un certificado.

#### ServerHelloDone
ServerHelloDone notifica al cliente que el servidor ha terminado con el handshake.

#### CertificateVerify
CertificateVerify es cómo el remitente prueba que tiene la clave privada enviada en el mensaje Certificate.

#### ChangeCipherSpec
ChangeCipherSpec informa al receptor que todo lo enviado después de este mensaje será cifrado.

#### Finished
Finished está cifrado y contiene un hash de todos los mensajes. Esto es para afirmar que el handshake no fue manipulado.

### Generación de Claves
Después de que el Handshake está completo, puedes comenzar a enviar datos cifrados. El Cifrador fue elegido por el servidor y está en el ServerHello. ¿Cómo se eligió la clave entonces?

Primero generamos el `Pre-Master Secret`. Para obtener este valor se usa Diffie–Hellman en las claves intercambiadas por el `ServerKeyExchange` y `ClientKeyExchange`. Los detalles difieren dependiendo del Cifrador elegido.

A continuación se genera el `Master Secret`. Cada versión de DTLS tiene una `Función Pseudoaleatoria` definida. Para DTLS 1.2 la función toma el `Pre-Master Secret` y valores aleatorios en el `ClientHello` y `ServerHello`.
La salida de ejecutar la `Función Pseudoaleatoria` es el `Master Secret`. El `Master Secret` es el valor que se usa para el Cifrador.

### Intercambio de ApplicationData
El caballo de batalla de DTLS es `ApplicationData`. Ahora que tenemos un cifrador inicializado, podemos comenzar a cifrar y enviar valores.

Los mensajes `ApplicationData` usan un encabezado DTLS como se describió anteriormente. La `Carga Útil` se rellena con texto cifrado. Ahora tienes una Sesión DTLS funcionando y puedes comunicarte de forma segura.

DTLS tiene muchas más características interesantes como la renegociación. No son usadas por WebRTC, por lo que no se cubrirán aquí.

## SRTP
SRTP es un protocolo diseñado específicamente para cifrar paquetes RTP. Para iniciar una sesión SRTP especificas tus claves y cifrador. A diferencia de DTLS no tiene mecanismo de handshake. Toda la configuración y claves fueron generadas durante el handshake DTLS.

DTLS proporciona una API dedicada para exportar las claves para ser utilizadas por otro proceso. Esto está definido en [RFC 5705](https://tools.ietf.org/html/rfc5705).

### Creación de Sesión
SRTP define una Función de Derivación de Clave que se usa en las entradas. Al crear una Sesión SRTP, las entradas se ejecutan a través de esto para generar nuestras claves para nuestro Cifrador SRTP. Después de esto puedes pasar al procesamiento de medios.

### Intercambio de Medios
Cada paquete RTP tiene un SequenceNumber de 16 bits. Estos Números de Secuencia se usan para mantener los paquetes en orden, como una Clave Primaria. Durante una llamada estos se reiniciarán. SRTP rastrea esto y lo llama el contador de reinicio (rollover counter).

Al cifrar un paquete, SRTP usa el contador de reinicio y el número de secuencia como un nonce. Esto es para asegurar que incluso si envías los mismos datos dos veces, el texto cifrado será diferente. Esto es importante para evitar que un atacante identifique patrones o intente un ataque de repetición.
