---
title: Quoi, Pourquoi et Comment
type: docs
weight: 2
---

# Quoi, Pourquoi et Comment

## Qu’est-ce que le WebRTC ?

WebRTC, raccourci pour Web Real-Time Communication, est une API et un protocole. Le protocole WebRTC est un ensemble de règles pour que deux agents WebRTC négocient une communication temps réel, bidirectionnelle et sécurisée. L’API WebRTC permet au développeur d’utiliser le protocole WebRTC. L’API WebRTC est seulement spécifiée pour le JavaScript.

Une relation similaire serait celle entre HTTP et l’API Fetch. Le protocole WebRTC serait HTTP, et l’API WebRTC serait l’API Fetch.

Le protocole WebRTC est disponible dans d’autres API et langages en plus du JavaScript. Vous pouvez aussi trouver des serveurs et des outils spécifiques au domaine du WebRTC. Toutes les implémentations utilisent le protocole WebRTC et peuvent donc interagir entre elles.

Le protocole WebRTC est maintenue au sein de l’IETF par le groupe de travail [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/). L’API WebRTC est documentée par le W3C en tant que [webrtc](https://www.w3.org/TR/webrtc/).


## Pourquoi devrais-je apprendre le WebRTC ?

Il y a des choses que le WebRTC peut vous apporter. Cette liste n’est pas exhaustive, c’est juste un exemple de choses que vous pourriez apprécier dans votre voyage. Ne vous inquiétez pas si vous ne connaissez pas encore tous ces termes, ce livre va vous les apprendre en cours de lecture.

* Standards ouverts
* Implémentations multiples
* Disponible dans le navigateur
* Chiffrement obligatoire
* Traversé des NAT
* Repositionnement de technologies existantes
* Contrôle de congestion
* Latence inférieure à la seconde

## Le Protocole WebRTC est une collection d’autres technologies

C’est un sujet qui demanderait un livre entier pour l’expliquer. Cependant, pour démarrer, nous l’avons divisé en quatre étapes.

* La signalisation
* La connexion
* La sécurité
* La communication

Ces quatre étapes se déroulent séquentiellement. L’étape précédente doit être finalisée avec succès à 100 % avant d’entamer la suivante.

Un des aspects particulier du WebRTC est que chacune des étapes est réellement constituée des nombreux autres protocoles ! Pour faire le WebRTC, nous devons assembler un grand nombre de technologies déjà existantes. En ce sens, le WebRTC est plus une combinaison et une configuration de technologies bien connues qui nous entourent depuis le début des années 2000.   

Chacune de ces étapes possède un chapitre dédié, mais cela aide de les comprendre à un haut niveau pour commencer. Et comme elles dépendent les unes des autres, cela va aider à expliquer un peu plus le but de chacune de ces étapes.

### La signalisation : Comment les agents se trouvent dans le WebRTC

Quand un agent WebRTC démarre, il n’a aucune idée avec qui il va communiquer et en quoi va consister cette communication. La signalisation résout ce problème ! La signalisation est utilisée pour amorcer l’appel pour que deux agents WebRTC puissent commencer à communiquer.

La signalisation utilise un protocole déjà existant appelé SDP (Session Description Protocol). Le SDP est un protocole en texte brut. Chaque message SDP est constitué de paire Clé/Valeur et contient une liste de “section média”. Les SDP que deux agents WebRTC échangent contiennent des détails tels que :
* IPs et Ports sur lesquels l’agent est joignable  (les candidats);
* Combien de flux audio et vidéo l’agent désire recevoir;
* Quel codec audio et vidéo les agents supportent;
* Des valeurs utiles à la connexion (`uFrag`/`uPwd`);
* Des valeurs utiles à la sécurisation (la signature des certificats).

Il est à noter que normalement la signalisation se réalise “out-of-band”, c'est-à-dire que les applications n’utilisent pas le WebRTC lui-même pour échanger les messages de signalisation. Toute architecture appropriée pour l’échange de message peut être utilisée pour relayer les SDP entre les agents. Bon nombre d’applications vont utiliser leur infrastructure déjà en place (comme des endpoints REST, connexion WebSocket ou autre proxy d’authentification) pour faciliter l’échange des SDP entre leurs propres clients.

### Connexion est traversée des NATs avec STUN/TURN

Les deux agents WebRTC connaissent maintenant suffisamment de détails pour tenter de se connecter l’un l’autre. Le WebRTC va alors utiliser une autre technologie bien rodée appelée ICE.
L’ICE (Interactive Connectivity Establishement) est un protocole antérieur au WebRTC. L’ICE permet l’établissement d’une connexion entre deux agents. Ces agents peuvent être sur le même réseau, ou à l’autre bout du monde. L’ICE est la solution pour établir une connexion directe sans serveur central.

La véritable magie repose ici porte sur la traversée des NATs avec les serveurs STUN/TURN. Ces deux concepts sont tout ce dont vous avez besoin pour communiquer avec un agent ICE sur un autre sous réseau. Nous allons explorer ce sujet en profondeur plus loin.

Une fois la connexion ICE établie, le WebRTC va alors passer à l’établissement d’un canal de transport chiffré des données. Ce canal de transport est utilisé pour l’audio, la vidéo et les données.

### Sécuriser la couche de transport avec DTLS et SRTP

Maintenant que nous avons une communication bidirectionnelle (avec ICE), nous devons établir une connexion sécurisée. Ceci est fait au travers de deux protocoles antérieurs au WebRTC. Le premier protocole est le DTLS (Datagram Transport Layer Security) qui est juste du TLS sur UDP. Le TLS est le protocole cryptographique utilisé pour sécuriser les communications du HTTPS. Le second protocole est le SRTP (Secure Real-Time Transport Protocol).

Tout d'abord, le WebRTC se connecte par un HandCheck DTLS sur la connexion établie par ICE. À la différence du HTTPS, le WebRTC n’utilise pas une autorité centrale de gestion des certificats. À la place, le WebRTC s’assure juste que l’échange de certificat via DTLS correspond bien au Fingerprint partagé par l’étape de signalisation. Cette connexion DTLS est ensuite utilisée pour les messages du DataChannel.

Le WebRTC utilise ensuite un protocole différent pour la transmission audio/vidéo appelé RTP (RealTime Transport Protocol). Nous sécurisons nos paquets RTP en utilisant SRTP. La session SRTP est initialisée par l’extraction des clés de la négociation de la session DTLS. Dans un chapitre ultérieur, nous discuterons pourquoi la transmission média à son propre protocole.

Maintenant, nous avons réussi ! Vous avez une communication bidirectionnelle et sécurisée entre deux agents. Si vous avez une connexion stable entre vos deux agents WebRTC, c’est toute la complexité dont vous avez besoin.
Malheureusement, le monde réel a des pertes de paquet et des limites de bande passante, nous allons voir comment traiter cela dans la prochaine section.

### Communiquer entre agents via le RTP et le SCTP

Nous avons maintenant deux agents WebRTC avec un canal de communication bidirectionnel et sécurisé. Commençons à communiquer ! Encore une fois, nous utilisons deux protocoles préexistants : RTP (RealTime Transport Protocol) et SCTP (Stream Control Transmission Protocol). Le SRTP, pour RTP encrypté, est utilisé pour l’échange de média et le SCTP pour recevoir et envoyer des messages de donnée cryptée via le DTLS.

Le RTP est assez minimaliste, mais fournit ce qu’il faut pour du streaming temps réel.  La chose importante est que le RTP donne de la flexibilité aux développeurs, ils peuvent donc traiter la latence, la perte de paquets et la congestion comme ils le veulent.  Nous discuterons de cela dans le chapitre sur les médias.

Le dernier protocole dans la stack est le SCTP. Le SCTP autorise un grand nombre d’options dans la transmission des messages. Vous pouvez choisir d’avoir une transmission non fiable, désordonnée, ce qui permet d’attendre la latence nécessaire aux systèmes temps-réel.

## Le WebRTC, une collection de protocole

Le WebRTC résout un grand nombre de problèmes. Premièrement, cela peut sembler trop complexe. Le génie du WebRTC est en réalité son humilité. Il ne prétendait pas qu’il pouvait tout résoudre mieux que les autres. À la place, il reprend un grand nombre de technologies existantes ciblant un domaine précis et les rassemble dans un protocole unique.

Cela nous permet d’examiner et d’apprendre chaque partie de façon individuelle sans être submergé. Une bonne manière de visualiser un “Agent WebRTC” est de le voir comme un orchestrateur d’un ensemble de différents protocoles.

![WebRTC Agent](../images/01-webrtc-agent.png "WebRTC Agent Diagram")

## Comment marche le WebRTC (l’API)

Cette section montre comment l’API Javascript WebRTC se calque sur le protocole. Il ne s’agit pas de montrer une démo détaillée de l’API WebRTC, mais plus de créer une représentation mentale de la manière dont tout cela est lié. Si vous n’êtes pas familier avec cela, tout va bien. Cela pourra être une section intéressante à regarder une fois que vous en aurez appris un peu plus.

### `new RTCPeerConnection`

La `RTCPeerConnection` est le niveau le plus haut d’une session WebRTC. Elle contient tous les protocoles mentionnés jusqu’ici. Les sous-systèmes sont tous initialisés, mais rien n’a encore commencé.

### `addTrack`

`addTrack` crée un nouveau flux RTP. Une source de synchronisation aléatoire (ssrc) sera générée pour ce flux. Ce flux sera ensuite ajouté dans dans la section média du SDP généré par `createOffer`. Chaque appel à `addTrack` va créer une nouvelle SSRC et une section média.

Immédiatement après l’établissement d’une session SRTP, les paquets média vont commencer à être envoyés via ICE en étant chiffrés par le SRTP.


### `createDataChannel`

`createDataChannel` crée un nouveau flux SCTP si aucune association SCTP n’existe. Par défaut, SCTP n’est pas activé, mais juste démarré quand un agent demande un canal de données.

Immédiatement après l’établissement de la session DTLS, l’association SCTP va commencer à envoyer des paquets via ICE en étant chiffré par DTLS.


### `createOffer`

`createOffer` génère la description de session de l’état de l’agent local afin de la partager avec l’autre agent.
Le fait d’appeler `createOffer` ne change rien sur l’agent local.


### `setLocalDescription`

`setLocalDescription` applique n’importe quelle demande de changement. `addTrack`, `CreateDataChannel` et les appels similaires sont tous temporaires avant cet appel. `setLocalDescription` est appelé avec la valeur générée par `createOffer`.

Habituellement, après cet appel, vous allez envoyer cette description de session à l’agent distant, et il va appeler `setRemoteDescription` avec celle-ci.


### `setRemoteDescription`

`setRemoteDescription` sert à informer l’agent local sur l’état des candidats distants. C’est de cette façon que la “Signalisation” est réalisée du côté de l'API Javascript.

Quand `setRemoteDescription` est appelé des deux cotés, les agents WebRTC ont suffisamment d’information pour commencer leur communication paire à paire (P2P) !  

### `addIceCandidate`

`addIceCandidate` permet à un agent WebRTC d’ajouter plus de candidats ICE distants quand il le veut. Cette API envoie le candidat ICE directement dans le sous-système ICE et n’a aucun autre effet dans la grande connexion WebRTC.

### `ontrack`

`ontrack` est un callback appelé lorsqu’un paquet RTP est reçu de l’agent distant. Les paquets entrants doivent avoir été déclarés dans la description de session (SDP) qui a été passée à `setRemoteDescription`.

Le WebRTC utilise le SSRC et regarde les `MediaStream` et `MediaStreamTrack` associé, il lance le callback quand tous les détails du flux sont récupérés.


### `oniceconnectionstatechange`

`oniceconnectionstatechange` est un callback qui est appelé quand l’état de l’agent ICE est modifié. Quand vous avez une nouvelle connexion réseau ou bien lorsque vous êtes déconnecté, c’est comme cela que vous êtes notifié.

### `onconnectionstatechange`

`onconnectionstatechange` est une combinaison de l’état de l’agent ICE et de l’agent DTLS. Vous pouvez regarder ce callback pour être notifié lorsque ICE et DTLS ont tous les deux été connectés avec succès.
