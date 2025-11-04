---
title: Signalisation
type: docs
weight: 3
---

# Signalisation

## Qu'est-ce que la signalisation WebRTC ?

Lorsque vous créez un agent WebRTC, il ne sait rien sur l'autre pair. Il n'a aucune idée avec qui il va se connecter ni ce qu'ils vont envoyer !
La signalisation est l'amorçage initial qui rend un appel possible. Après l'échange de ces valeurs, les agents WebRTC peuvent communiquer directement entre eux.

Les messages de signalisation sont simplement du texte. Les agents WebRTC ne se soucient pas de la manière dont ils sont transportés. Ils sont généralement partagés via Websockets, mais ce n'est pas une exigence.

## Comment fonctionne la signalisation WebRTC ?

WebRTC utilise un protocole existant appelé Session Description Protocol. Via ce protocole, les deux agents WebRTC partageront tout l'état requis pour établir une connexion. Le protocole lui-même est simple à lire et à comprendre.
La complexité vient de la compréhension de toutes les valeurs dont WebRTC le remplit.

Ce protocole n'est pas spécifique à WebRTC. Nous allons d'abord apprendre le Session Description Protocol sans même parler de WebRTC. WebRTC ne tire vraiment parti que d'un sous-ensemble du protocole, donc nous ne couvrirons que ce dont nous avons besoin.
Après avoir compris le protocole, nous passerons à son utilisation appliquée dans WebRTC.

## Qu'est-ce que le *Session Description Protocol* (SDP) ?
Le Session Description Protocol est défini dans la [RFC 8866](https://tools.ietf.org/html/rfc8866). Il s'agit d'un protocole clé/valeur avec un retour à la ligne après chaque valeur. Il ressemblera à un fichier INI.
Une description de session contient zéro ou plusieurs descriptions de média. Mentalement, vous pouvez le modéliser comme une description de session qui contient un tableau de descriptions de média.

Une description de média correspond généralement à un seul flux de média. Donc, si vous vouliez décrire un appel avec trois flux vidéo et deux pistes audio, vous auriez cinq descriptions de média.

### Comment lire le SDP
Chaque ligne d'une description de session commencera par un seul caractère, c'est votre clé. Elle sera ensuite suivie d'un signe égal. Tout ce qui suit ce signe égal est la valeur. Après que la valeur est complète, vous aurez un retour à la ligne.

Le Session Description Protocol définit toutes les clés qui sont valides. Vous ne pouvez utiliser que des lettres pour les clés telles que définies dans le protocole. Ces clés ont toutes une signification importante, qui sera expliquée plus tard.

Prenez cet extrait de description de session :

```
a=my-sdp-value
a=second-value
```

Vous avez deux lignes. Chacune avec la clé `a`. La première ligne a la valeur `my-sdp-value`, la deuxième ligne a la valeur `second-value`.

### WebRTC n'utilise que certaines clés SDP
Toutes les valeurs de clé définies par le Session Description Protocol ne sont pas utilisées par WebRTC. Seules les clés utilisées dans le JavaScript Session Establishment Protocol (JSEP), défini dans la [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829), sont importantes. Les sept clés suivantes sont les seules que vous devez comprendre pour le moment :

* `v` - Version, doit être égale à `0`.
* `o` - Origin (Origine), contient un identifiant unique utile pour les renégociations.
* `s` - Session Name (Nom de session), doit être égal à `-`.
* `t` - Timing (Temporisation), doit être égal à `0 0`.
* `m` - Media Description (Description de média) (`m=<media> <port> <proto> <fmt> ...`), décrite en détail ci-dessous.
* `a` - Attribute (Attribut), un champ de texte libre. C'est la ligne la plus courante dans WebRTC.
* `c` - Connection Data (Données de connexion), doit être égal à `IN IP4 0.0.0.0`.

### Descriptions de média dans une description de session

Une description de session peut contenir un nombre illimité de descriptions de média.

Une définition de description de média contient une liste de formats. Ces formats correspondent aux types de charge utile RTP. Le codec réel est ensuite défini par un attribut avec la valeur `rtpmap` dans la description de média.
L'importance de RTP et des types de charge utile RTP est discutée plus loin dans le chapitre sur les médias. Chaque description de média peut contenir un nombre illimité d'attributs.

Prenez cet extrait de description de session comme exemple :

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

Vous avez deux descriptions de média, une de type audio avec le format `111` et une de type video avec le format `96`. La première description de média n'a qu'un seul attribut. Cet attribut associe le type de charge utile `111` à Opus.
La deuxième description de média a deux attributs. Le premier attribut associe le type de charge utile `96` à VP8, et le deuxième attribut est simplement `my-sdp-value`.

### Exemple complet

Ce qui suit rassemble tous les concepts dont nous avons parlé. Ce sont toutes les fonctionnalités du Session Description Protocol que WebRTC utilise.
Si vous pouvez lire ceci, vous pouvez lire n'importe quelle description de session WebRTC !

```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 127.0.0.1
t=0 0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4002 RTP/AVP 96
a=rtpmap:96 VP8/90000
```

* `v`, `o`, `s`, `c`, `t` sont définis, mais ils n'affectent pas la session WebRTC.
* Vous avez deux descriptions de média. Une de type `audio` et une de type `video`.
* Chacune d'elles a un attribut. Cet attribut configure les détails du pipeline RTP, qui est discuté dans le chapitre "Communication média".

## Comment le *Session Description Protocol* et WebRTC fonctionnent ensemble

La pièce suivante du puzzle est de comprendre _comment_ WebRTC utilise le Session Description Protocol.

### Que sont les offres et les réponses ?

WebRTC utilise un modèle offre/réponse. Tout cela signifie qu'un agent WebRTC fait une "offre" pour démarrer un appel, et l'autre agent WebRTC "répond" s'il est prêt à accepter ce qui a été offert.

Cela donne au répondeur une chance de rejeter les codecs non pris en charge dans les descriptions de média. C'est ainsi que deux pairs peuvent comprendre quels formats ils sont prêts à échanger.

### Les transceivers servent à envoyer et recevoir

Transceiver est un concept spécifique à WebRTC que vous verrez dans l'API. Ce qu'il fait, c'est exposer la "description de média" à l'API JavaScript. Chaque description de média devient un transceiver.
Chaque fois que vous créez un transceiver, une nouvelle description de média est ajoutée à la description de session locale.

Chaque description de média dans WebRTC aura un attribut de direction. Cela permet à un agent WebRTC de déclarer "Je vais vous envoyer ce codec, mais je ne suis pas prêt à accepter quoi que ce soit en retour". Il existe quatre valeurs valides :

* `send`
* `recv`
* `sendrecv`
* `inactive`

### Valeurs SDP utilisées par WebRTC

Voici une liste de certains attributs communs que vous verrez dans une description de session provenant d'un agent WebRTC. Beaucoup de ces valeurs contrôlent les sous-systèmes que nous n'avons pas encore discutés.

#### `group:BUNDLE`
Le bundling (regroupement) est un acte d'exécution de plusieurs types de trafic sur une seule connexion. Certaines implémentations WebRTC utilisent une connexion dédiée par flux média. Le bundling devrait être préféré.

#### `fingerprint:sha-256`
Il s'agit d'un hachage du certificat qu'un pair utilise pour DTLS. Après la fin de la négociation DTLS, vous comparez ceci au certificat réel pour confirmer que vous communiquez avec qui vous attendez.

#### `setup:`
Ceci contrôle le comportement de l'agent DTLS. Cela détermine s'il s'exécute en tant que client ou serveur après la connexion ICE. Les valeurs possibles sont :

* `setup:active` - Exécuter en tant que client DTLS.
* `setup:passive` - Exécuter en tant que serveur DTLS.
* `setup:actpass` - Demander à l'autre agent WebRTC de choisir.

#### `mid`
L'attribut "mid" est utilisé pour identifier les flux média dans une description de session.

#### `ice-ufrag`
Il s'agit de la valeur du fragment utilisateur pour l'agent ICE. Utilisé pour l'authentification du trafic ICE.

#### `ice-pwd`
Il s'agit du mot de passe pour l'agent ICE. Utilisé pour l'authentification du trafic ICE.

#### `rtpmap`
Cette valeur est utilisée pour associer un codec spécifique à un type de charge utile RTP. Les types de charge utile ne sont pas statiques, donc pour chaque appel, l'offrant décide des types de charge utile pour chaque codec.

#### `fmtp`
Définit des valeurs supplémentaires pour un type de charge utile. Ceci est utile pour communiquer un profil vidéo spécifique ou un paramètre d'encodeur.

#### `candidate`
Il s'agit d'un candidat ICE provenant de l'agent ICE. C'est une adresse possible sur laquelle l'agent WebRTC est disponible. Ceux-ci sont entièrement expliqués dans le chapitre suivant.

#### `ssrc`
Une source de synchronisation (SSRC) définit une seule piste de flux média.

`label` est l'identifiant pour ce flux individuel. `mslabel` est l'identifiant pour un conteneur qui peut avoir plusieurs flux à l'intérieur.

### Exemple d'une description de session WebRTC
Ce qui suit est une description de session complète générée par un client WebRTC :

```
v=0
o=- 3546004397921447048 1596742744 IN IP4 0.0.0.0
s=-
t=0 0
a=fingerprint:sha-256 0F:74:31:25:CB:A2:13:EC:28:6F:6D:2C:61:FF:5D:C2:BC:B9:DB:3D:98:14:8D:1A:BB:EA:33:0C:A4:60:A8:8E
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=setup:active
a=mid:0
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ssrc:350842737 cname:yvKPspsHcYcwGFTw
a=ssrc:350842737 msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=ssrc:350842737 mslabel:yvKPspsHcYcwGFTw
a=ssrc:350842737 label:DfQnKjQQuwceLFdV
a=msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=setup:active
a=mid:1
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=ssrc:2180035812 cname:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=ssrc:2180035812 mslabel:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 label:JgtwEhBWNEiOnhuW
a=msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=sendrecv
```

Voici ce que nous savons de ce message :

* Nous avons deux sections média, une audio et une vidéo.
* Les deux sont des transceivers `sendrecv`. Nous recevons deux flux et nous pouvons en renvoyer deux.
* Nous avons des candidats ICE et des détails d'authentification, donc nous pouvons tenter de nous connecter.
* Nous avons une empreinte de certificat, donc nous pouvons avoir un appel sécurisé.

### Sujets ultérieurs
Dans les versions ultérieures de ce livre, les sujets suivants seront également abordés :

* Renégociation
* Simulcast
