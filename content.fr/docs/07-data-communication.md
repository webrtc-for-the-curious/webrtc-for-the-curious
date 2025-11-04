---
title: Communication de données
type: docs
weight: 8
---

# Communication de données

## Que m'apporte la communication de données de WebRTC ?

WebRTC fournit des canaux de données pour la communication de données. Entre deux pairs, vous pouvez ouvrir 65 534 canaux de données.
Un canal de données est basé sur des datagrammes, et chacun a ses propres paramètres de durabilité. Par défaut, chaque canal de données garantit une livraison ordonnée.

Si vous abordez WebRTC à partir d'un contexte média, les canaux de données peuvent sembler gaspilleurs. Pourquoi ai-je besoin de tout ce sous-système alors que je pourrais simplement utiliser HTTP ou WebSockets ?

Le véritable pouvoir des canaux de données est que vous pouvez les configurer pour qu'ils se comportent comme UDP avec une livraison non ordonnée/avec perte.
Ceci est nécessaire pour les situations de faible latence et de haute performance. Vous pouvez mesurer la contre-pression et vous assurer que vous n'envoyez que ce que votre réseau prend en charge.

## Comment cela fonctionne-t-il ?
WebRTC utilise le Stream Control Transmission Protocol (SCTP), défini dans la [RFC 4960](https://tools.ietf.org/html/rfc4960). SCTP est un
protocole de couche transport qui était destiné comme alternative à TCP ou UDP. Pour WebRTC, nous l'utilisons comme protocole de couche application qui s'exécute sur notre connexion DTLS.

SCTP vous donne des flux et chaque flux peut être configuré indépendamment. Les canaux de données WebRTC ne sont que de minces abstractions autour d'eux. Les paramètres
concernant la durabilité et l'ordonnancement sont simplement transmis directement à l'agent SCTP.

Les canaux de données ont certaines fonctionnalités que SCTP ne peut pas exprimer, comme les étiquettes de canal. Pour résoudre cela, WebRTC utilise le Data Channel Establishment Protocol (DCEP)
qui est défini dans la [RFC 8832](https://tools.ietf.org/html/rfc8832). DCEP définit un message pour communiquer l'étiquette et le protocole du canal.

## DCEP
DCEP n'a que deux messages `DATA_CHANNEL_OPEN` et `DATA_CHANNEL_ACK`. Pour chaque canal de données ouvert, le distant doit répondre avec un accusé de réception.

### DATA_CHANNEL_OPEN
Ce message est envoyé par l'agent WebRTC qui souhaite ouvrir un canal.

#### Format de paquet
```
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
```

#### Type de message
Le type de message est une valeur statique de `0x03`.

#### Type de canal
Le type de canal contrôle les attributs de durabilité/ordonnancement du canal. Il peut avoir les valeurs suivantes :

* `DATA_CHANNEL_RELIABLE` (`0x00`) - Aucun message n'est perdu et arrivera dans l'ordre
* `DATA_CHANNEL_RELIABLE_UNORDERED` (`0x80`) - Aucun message n'est perdu, mais ils peuvent arriver dans le désordre.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT` (`0x01`) - Les messages peuvent être perdus après avoir essayé le nombre de fois demandé, mais ils arriveront dans l'ordre.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED` (`0x81`) - Les messages peuvent être perdus après avoir essayé le nombre de fois demandé et peuvent arriver dans le désordre.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED` (`0x02`) - Les messages peuvent être perdus s'ils n'arrivent pas dans le délai demandé, mais ils arriveront dans l'ordre.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED` (`0x82`) - Les messages peuvent être perdus s'ils n'arrivent pas dans le délai demandé et peuvent arriver dans le désordre.

#### Priorité
La priorité du canal de données. Les canaux de données ayant une priorité plus élevée seront planifiés en premier. Les messages utilisateur volumineux de priorité inférieure ne retarderont pas l'envoi de messages utilisateur de priorité plus élevée.

#### Paramètre de fiabilité
Si le type de canal de données est `DATA_CHANNEL_PARTIAL_RELIABLE`, les suffixes configurent le comportement :

* `REXMIT` - Définit combien de fois l'expéditeur renverra le message avant d'abandonner.
* `TIMED` - Définit pendant combien de temps (en ms) l'expéditeur renverra le message avant d'abandonner.

#### Étiquette
Une chaîne encodée UTF-8 contenant le nom du canal de données. Cette chaîne peut être vide.

#### Protocole
Si c'est une chaîne vide, le protocole n'est pas spécifié. Si c'est une chaîne non vide, elle devrait spécifier un protocole enregistré dans le "WebSocket Subprotocol Name Registry", défini dans la [RFC 6455](https://tools.ietf.org/html/rfc6455#page-61).

### DATA_CHANNEL_ACK
Ce message est envoyé par l'agent WebRTC pour accuser réception que ce canal de données a été ouvert.

#### Format de paquet
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
```

## Stream Control Transmission Protocol
SCTP est le véritable pouvoir derrière les canaux de données WebRTC. Il fournit toutes ces fonctionnalités du canal de données :

* Multiplexage
* Livraison fiable utilisant un mécanisme de retransmission similaire à TCP
* Options de fiabilité partielle
* Évitement de la congestion
* Contrôle de flux

Pour comprendre SCTP, nous l'explorerons en trois parties. L'objectif est que vous en sachiez assez pour déboguer et apprendre les détails profonds de SCTP par vous-même après ce chapitre.

## Concepts
SCTP est un protocole riche en fonctionnalités. Cette section ne couvrira que les parties de SCTP utilisées par WebRTC.
Les fonctionnalités de SCTP qui ne sont pas utilisées par WebRTC incluent le multi-homing et la sélection de chemin.

Avec plus de vingt ans de développement, SCTP peut être difficile à saisir pleinement.

### Association
L'association est le terme utilisé pour une session SCTP. C'est l'état qui est partagé
entre deux agents SCTP pendant qu'ils communiquent.

### Flux
Un flux est une séquence bidirectionnelle de données utilisateur. Lorsque vous créez un canal de données, vous ne créez en fait qu'un flux SCTP. Chaque association SCTP contient une liste de flux. Chaque flux peut être configuré avec différents types de fiabilité.

WebRTC vous permet uniquement de configurer lors de la création du flux, mais SCTP permet en réalité de changer la configuration à tout moment.

### Basé sur les datagrammes
SCTP encadre les données comme des datagrammes et non comme un flux d'octets. L'envoi et la réception de données ressemblent à l'utilisation d'UDP plutôt que de TCP.
Vous n'avez pas besoin d'ajouter de code supplémentaire pour transférer plusieurs fichiers sur un seul flux.

Les messages SCTP n'ont pas de limites de taille comme UDP. Un seul message SCTP peut faire plusieurs gigaoctets de taille.

### Morceaux
Le protocole SCTP est composé de morceaux. Il existe de nombreux types différents de morceaux. Ces morceaux sont utilisés pour toute communication.
Les données utilisateur, l'initialisation de connexion, le contrôle de congestion, et plus encore sont tous effectués via des morceaux.

Chaque paquet SCTP contient une liste de morceaux. Donc, dans un paquet UDP, vous pouvez avoir plusieurs morceaux transportant des messages de différents flux.

### Numéro de séquence de transmission
Le numéro de séquence de transmission (TSN) est un identifiant unique global pour les morceaux DATA. Un morceau DATA est ce qui transporte tous les messages qu'un utilisateur souhaite envoyer. Le TSN est important car il aide un récepteur à déterminer si des paquets sont perdus ou dans le désordre.

Si le récepteur remarque un TSN manquant, il ne donne pas les données à l'utilisateur tant qu'il n'est pas satisfait.

### Identifiant de flux
Chaque flux a un identifiant unique. Lorsque vous créez un canal de données avec un ID explicite, il est en fait simplement passé directement à SCTP comme identifiant de flux. Si vous ne passez pas d'ID, l'identifiant de flux est choisi pour vous.

### Identifiant de protocole de charge utile
Chaque morceau DATA a également un identifiant de protocole de charge utile (PPID). Ceci est utilisé pour identifier de manière unique quel type de données est échangé.
SCTP a de nombreux PPID, mais WebRTC n'utilise que les cinq suivants :

* `WebRTC DCEP` (`50`) - Messages DCEP.
* `WebRTC String` (`51`) - Messages de chaîne DataChannel.
* `WebRTC Binary` (`53`) - Messages binaires DataChannel.
* `WebRTC String Empty` (`56`) - Messages de chaîne DataChannel de longueur 0.
* `WebRTC Binary Empty` (`57`) - Messages binaires DataChannel de longueur 0.

## Protocole
Voici quelques-uns des morceaux utilisés par le protocole SCTP. Ce n'est
pas une démonstration exhaustive. Cela fournit suffisamment de structures pour que la
machine à états ait du sens.

Chaque morceau commence par un champ `type`. Avant une liste de morceaux, vous aurez
également un en-tête.

### Morceau DATA
```
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
```
Le morceau DATA est la façon dont toutes les données utilisateur sont échangées. Lorsque vous envoyez
quoi que ce soit sur le canal de données, c'est ainsi qu'il est échangé.

Le bit `U` est défini si c'est un paquet non ordonné. Nous pouvons ignorer le
numéro de séquence de flux.

`B` et `E` sont les bits de début et de fin. Si vous voulez envoyer un
message trop grand pour un morceau DATA, il doit être fragmenté en plusieurs morceaux DATA envoyés dans des paquets séparés.
Avec le bit `B` et `E` et les numéros de séquence, SCTP est capable d'exprimer
cela.

* `B=1`, `E=0` - Première pièce d'un message utilisateur fragmenté.
* `B=0`, `E=0` - Pièce intermédiaire d'un message utilisateur fragmenté.
* `B=0`, `E=1` - Dernière pièce d'un message utilisateur fragmenté.
* `B=1`, `E=1` - Message non fragmenté.

`TSN` est le numéro de séquence de transmission. C'est l'identifiant unique
global pour ce morceau DATA. Après 4 294 967 295 morceaux, cela reviendra à 0.
Le TSN est incrémenté pour chaque morceau dans un message utilisateur fragmenté afin que le récepteur sache comment ordonner les morceaux reçus pour reconstruire le message original.

`Identifiant de flux` est l'identifiant unique pour le flux auquel ces données appartiennent.

`Numéro de séquence de flux` est un nombre de 16 bits incrémenté à chaque message utilisateur et inclus dans l'en-tête du morceau de message DATA. Après 65 535 messages, cela reviendra à 0. Ce nombre est utilisé pour décider l'ordre de livraison des messages au récepteur si `U` est défini à 0. Semblable au TSN, sauf que le numéro de séquence de flux n'est incrémenté que pour chaque message dans son ensemble et non pour chaque morceau DATA individuel.

`Identifiant de protocole de charge utile` est le type de données qui circule à travers
ce flux. Pour WebRTC, ce sera DCEP, String ou Binary.

`Données utilisateur` est ce que vous envoyez. Toutes les données que vous envoyez via un canal de données WebRTC
sont transmises via un morceau DATA.

### Morceau INIT
```
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
```

Le morceau INIT démarre le processus de création d'une association.

`Initiate Tag` est utilisé pour la génération de cookies. Les cookies sont utilisés pour la protection contre l'homme du milieu
et le déni de service. Ils sont décrits plus en détail dans la section de la machine
à états.

`Advertised Receiver Window Credit` est utilisé pour le contrôle de congestion de SCTP. Cela
communique la taille du tampon que le récepteur a alloué pour cette association.

`Nombre de flux sortants/entrants` notifie le distant du nombre de flux que cet
agent prend en charge.

`TSN initial` est un `uint32` aléatoire pour démarrer le TSN local.

`Paramètres optionnels` permet à SCTP d'introduire de nouvelles fonctionnalités dans le protocole.


### Morceau SACK

```
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
```

Le morceau SACK (Accusé de réception sélectif) est la façon dont un récepteur notifie
un expéditeur qu'il a reçu un paquet. Jusqu'à ce qu'un expéditeur reçoive un SACK pour un TSN,
il renverra le morceau DATA en question. Un SACK fait plus que simplement
mettre à jour le TSN.

`TSN cumulatif ACK` le TSN le plus élevé qui a été reçu.

`Crédit de fenêtre de récepteur annoncé` taille du tampon du récepteur. Le récepteur
peut changer cela pendant la session si plus de mémoire devient disponible.

`Blocs Ack` TSN qui ont été reçus après le `TSN cumulatif ACK`.
Ceci est utilisé s'il y a un écart dans les paquets livrés. Disons que des morceaux DATA avec des TSN
`100`, `102`, `103` et `104` sont livrés. Le `TSN cumulatif ACK` serait `100`, mais
`Blocs Ack` pourrait être utilisé pour dire à l'expéditeur qu'il n'a pas besoin de renvoyer `102`, `103` ou `104`.

`TSN dupliqué` informe l'expéditeur qu'il a reçu les morceaux DATA suivants plus d'une fois.

### Morceau HEARTBEAT
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 4    | Chunk  Flags  |      Heartbeat Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/            Heartbeat Information TLV (Variable-Length)        /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Le morceau HEARTBEAT est utilisé pour affirmer que le distant répond toujours.
Utile si vous n'envoyez aucun morceau DATA et devez maintenir un
mappage NAT ouvert.

### Morceau ABORT
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 6    |Reserved     |T|           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\               Zero or more Error Causes                       \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Un morceau ABORT ferme brusquement l'association. Utilisé lorsque
un côté entre dans un état d'erreur. La fin gracieuse de la connexion utilise
le morceau SHUTDOWN.

### Morceau SHUTDOWN
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 7    | Chunk  Flags  |      Length = 8               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Le morceau SHUTDOWN démarre une fermeture gracieuse de l'association SCTP.
Chaque agent informe le distant du dernier TSN qu'il a envoyé. Cela garantit
qu'aucun paquet n'est perdu. WebRTC n'effectue pas de fermeture gracieuse de
l'association SCTP. Vous devez démonter chaque canal de données vous-même
pour le gérer gracieusement.

`TSN cumulatif ACK` est le dernier TSN qui a été envoyé. Chaque côté sait
ne pas terminer jusqu'à ce qu'il ait reçu le morceau DATA avec ce TSN.

### Morceau ERROR
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 9    | Chunk  Flags  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                    One or more Error Causes                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Un morceau ERROR est utilisé pour notifier l'agent SCTP distant qu'une erreur non fatale
s'est produite.

### Morceau FORWARD TSN
```
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
```

Le morceau `FORWARD TSN` déplace le TSN global vers l'avant. SCTP fait cela, 
pour que vous puissiez sauter certains paquets qui ne vous intéressent plus. Disons
que vous envoyez `10 11 12 13 14 15` et que ces paquets ne sont valides que s'ils
arrivent tous. Ces données sont également sensibles au temps réel, donc si elles arrivent
tard, elles ne sont pas utiles.

Si vous perdez `12` et `13`, il n'y a aucune raison d'envoyer `14` et `15` !
SCTP utilise le morceau `FORWARD TSN` pour y parvenir. Il dit au récepteur
que `14` et `15` ne seront plus livrés.

`Nouveau TSN cumulatif` c'est le nouveau TSN de la connexion. Tous les paquets
avant ce TSN ne seront pas conservés.

`Flux` et `Séquence de flux` sont utilisés pour faire avancer le `numéro de séquence de flux`
en avant. Reportez-vous au morceau DATA pour la signification de ce champ.

## Machine à états
Voici quelques parties intéressantes de la machine à états SCTP. WebRTC n'utilise pas toutes
les fonctionnalités de la machine à états SCTP, nous avons donc exclu ces parties. Nous avons également simplifié certains composants pour les rendre compréhensibles par eux-mêmes.

### Flux d'établissement de connexion
Les morceaux `INIT` et `INIT ACK` sont utilisés pour échanger les capacités et configurations
de chaque pair. SCTP utilise un cookie pendant la négociation pour valider le pair avec lequel il communique.
Cela garantit que la négociation n'est pas interceptée et pour prévenir les attaques DoS.

Le morceau `INIT ACK` contient le cookie. Le cookie est ensuite renvoyé à son créateur
en utilisant le `COOKIE ECHO`. Si la vérification du cookie réussit, le `COOKIE ACK` est
envoyé et les morceaux DATA sont prêts à être échangés.

![Établissement de connexion](../images/07-connection-establishment.png "Établissement de connexion")

### Flux de démontage de connexion
SCTP utilise le morceau `SHUTDOWN`. Lorsqu'un agent reçoit un morceau `SHUTDOWN`, il attendra jusqu'à ce qu'il
reçoive le `TSN cumulatif ACK` demandé. Cela permet à un utilisateur de s'assurer que toutes les données
sont livrées même si la connexion a des pertes.

### Mécanisme de maintien en vie
SCTP utilise les morceaux `HEARTBEAT REQUEST` et `HEARTBEAT ACK` pour maintenir la connexion en vie. Ceux-ci sont envoyés
à un intervalle configurable. SCTP effectue également un backoff exponentiel si le paquet n'est pas arrivé.

Le morceau `HEARTBEAT` contient également une valeur temporelle. Cela permet à deux associations de calculer le temps de trajet entre deux agents.
