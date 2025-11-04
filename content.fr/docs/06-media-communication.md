---
title: Communication média
type: docs
weight: 7
---

# Communication média

## Que m'apporte la communication média de WebRTC ?

WebRTC vous permet d'envoyer et de recevoir une quantité illimitée de flux audio et vidéo. Vous pouvez ajouter et supprimer ces flux à tout moment pendant un appel. Ces flux peuvent tous être indépendants, ou ils peuvent être regroupés ! Vous pourriez envoyer un flux vidéo de votre bureau, puis inclure l'audio et la vidéo de votre webcam.

Le protocole WebRTC est agnostique au codec. Le transport sous-jacent prend en charge tout, même des choses qui n'existent pas encore ! Cependant, l'agent WebRTC avec lequel vous communiquez peut ne pas avoir les outils nécessaires pour l'accepter.

WebRTC est également conçu pour gérer des conditions réseau dynamiques. Pendant un appel, votre bande passante peut augmenter ou diminuer. Peut-être que vous subissez soudainement beaucoup de perte de paquets. Le protocole est conçu pour gérer tout cela. WebRTC répond aux conditions du réseau et essaie de vous donner la meilleure expérience possible avec les ressources disponibles.

## Comment cela fonctionne-t-il ?
WebRTC utilise deux protocoles préexistants RTP et RTCP, tous deux définis dans la [RFC 1889](https://tools.ietf.org/html/rfc1889).

RTP (Real-time Transport Protocol) est le protocole qui transporte les médias. Il a été conçu pour permettre la livraison en temps réel de vidéo. Il ne stipule aucune règle concernant la latence ou la fiabilité, mais vous donne les outils pour les implémenter. RTP vous donne des flux, afin que vous puissiez exécuter plusieurs flux de médias sur une seule connexion. Il vous donne également les informations de timing et d'ordonnancement dont vous avez besoin pour alimenter un pipeline média.

RTCP (RTP Control Protocol) est le protocole qui communique les métadonnées sur l'appel. Le format est très flexible et vous permet d'ajouter toutes les métadonnées que vous souhaitez. Ceci est utilisé pour communiquer des statistiques sur l'appel. Il est également utilisé pour gérer la perte de paquets et pour implémenter le contrôle de congestion. Il vous donne la communication bidirectionnelle nécessaire pour répondre aux conditions réseau changeantes.

## Latence vs Qualité
Les médias en temps réel consistent à faire des compromis entre la latence et la qualité. Plus vous êtes prêt à tolérer de latence, plus la qualité vidéo que vous pouvez attendre est élevée.

### Limitations du monde réel
Ces contraintes sont toutes causées par les limitations du monde réel. Ce sont toutes des caractéristiques de votre réseau que vous devrez surmonter.

### La vidéo est complexe
Transporter de la vidéo n'est pas facile. Pour stocker 30 minutes de vidéo 720 8 bits non compressée, vous avez besoin d'environ 110 GB. Avec ces chiffres, une conférence téléphonique à 4 personnes ne va pas se produire. Nous avons besoin d'un moyen de la rendre plus petite, et la réponse est la compression vidéo. Cela ne vient pas sans inconvénients cependant.

## Vidéo 101
Nous n'allons pas couvrir la compression vidéo en profondeur, mais juste assez pour comprendre pourquoi RTP est conçu de la manière dont il l'est. La compression vidéo encode la vidéo dans un nouveau format qui nécessite moins de bits pour représenter la même vidéo.

### Compression avec perte et sans perte
Vous pouvez encoder la vidéo pour qu'elle soit sans perte (aucune information n'est perdue) ou avec perte (l'information peut être perdue). Étant donné que l'encodage sans perte nécessite plus de données à envoyer à un pair, ce qui entraîne un flux de latence plus élevée et plus de paquets abandonnés, RTP utilise généralement une compression avec perte même si la qualité vidéo ne sera pas aussi bonne.

### Compression intra et inter-image
La compression vidéo se présente en deux types. Le premier est intra-image. La compression intra-image réduit les bits utilisés pour décrire une seule image vidéo. Les mêmes techniques sont utilisées pour comprimer les images fixes, comme la méthode de compression JPEG.

Le deuxième type est la compression inter-image. Étant donné que la vidéo est composée de nombreuses images, nous cherchons des moyens de ne pas envoyer la même information deux fois.

### Types d'images inter
Vous avez ensuite trois types d'images :

* **I-Frame** - Une image complète, peut être décodée sans rien d'autre.
* **P-Frame** - Une image partielle, ne contenant que les changements par rapport à l'image précédente.
* **B-Frame** - Une image partielle, est une modification des images précédentes et futures.

Voici une visualisation des trois types d'images.

![Types d'images](../images/06-frame-types.png "Types d'images")

### La vidéo est délicate
La compression vidéo est incroyablement avec état, ce qui la rend difficile à transférer sur Internet. Que se passe-t-il si vous perdez une partie d'une I-Frame ? Comment une P-Frame sait-elle quoi modifier ? À mesure que la compression vidéo devient plus complexe, cela devient un problème encore plus important. Heureusement, RTP et RTCP ont la solution.

## RTP
### Format de paquet
Chaque paquet RTP a la structure suivante :

```
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
```

#### Version (V)
`Version` est toujours `2`

#### Remplissage (P)
`Remplissage` est un booléen qui contrôle si la charge utile a du remplissage.

Le dernier octet de la charge utile contient un décompte du nombre d'octets de remplissage qui ont été ajoutés.

#### Extension (X)
S'il est défini, l'en-tête RTP aura des extensions. Ceci est décrit plus en détail ci-dessous.

#### Nombre CSRC (CC)
Le nombre d'identifiants `CSRC` qui suivent après le `SSRC`, et avant la charge utile.

#### Marqueur (M)
Le bit de marqueur n'a pas de signification prédéfinie et peut être utilisé comme l'utilisateur le souhaite.

Dans certains cas, il est défini lorsqu'un utilisateur parle. Il est également couramment utilisé pour marquer une image clé.

#### Type de charge utile (PT)
`Type de charge utile` est un identifiant unique pour quel codec est transporté par ce paquet.

Pour WebRTC, le `Type de charge utile` est dynamique. VP8 dans un appel peut être différent d'un autre. L'offrant dans l'appel détermine le mappage des `Types de charge utile` aux codecs dans la `Description de session`.

#### Numéro de séquence
`Numéro de séquence` est utilisé pour ordonner les paquets dans un flux. Chaque fois qu'un paquet est envoyé, le `Numéro de séquence` est incrémenté de un.

RTP est conçu pour être utile sur des réseaux avec perte. Cela donne au récepteur un moyen de détecter quand des paquets ont été perdus.

#### Horodatage
L'instant d'échantillonnage pour ce paquet. Ce n'est pas une horloge globale, mais combien de temps s'est écoulé dans le flux média. Plusieurs paquets RTP peuvent avoir le même horodatage s'ils font par exemple tous partie de la même image vidéo.

#### Source de synchronisation (SSRC)
Un `SSRC` est l'identifiant unique pour ce flux. Cela vous permet d'exécuter plusieurs flux de médias sur un seul flux RTP.

#### Source contributrice (CSRC)
Une liste qui communique quels `SSRC` ont contribué à ce paquet.

Ceci est couramment utilisé pour les indicateurs de conversation. Disons que côté serveur, vous avez combiné plusieurs flux audio en un seul flux RTP. Vous pourriez alors utiliser ce champ pour dire "Les flux d'entrée A et C parlaient à ce moment".

#### Charge utile
Les données de charge utile réelles. Peut se terminer par le décompte du nombre d'octets de remplissage qui ont été ajoutés, si le drapeau de remplissage est défini.

### Extensions

## RTCP

### Format de paquet
Chaque paquet RTCP a la structure suivante :

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|    RC   |       PT      |             length            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
`Version` est toujours `2`.

#### Remplissage (P)
`Remplissage` est un booléen qui contrôle si la charge utile a du remplissage.

Le dernier octet de la charge utile contient un décompte du nombre d'octets de remplissage qui ont été ajoutés.

#### Nombre de rapports de réception (RC)
Le nombre de rapports dans ce paquet. Un seul paquet RTCP peut contenir plusieurs événements.

#### Type de paquet (PT)
Identifiant unique pour quel type de paquet RTCP c'est. Un agent WebRTC n'a pas besoin de prendre en charge tous ces types, et le support entre les agents peut être différent. Voici ceux que vous pouvez couramment voir cependant :

* `192` - Requête d'image INTRA complète (`FIR`)
* `193` - Accusés de réception négatifs (`NACK`)
* `200` - Rapport d'expéditeur
* `201` - Rapport de récepteur
* `205` - Rétroaction RTP générique
* `206` - Rétroaction spécifique à la charge utile

La signification de ces types de paquets sera décrite plus en détail ci-dessous.

### Requête d'image INTRA complète (FIR) et indication de perte d'image (PLI)
Les messages `FIR` et `PLI` servent un objectif similaire. Ces messages demandent une image clé complète de l'expéditeur.
`PLI` est utilisé lorsque des images partielles ont été données au décodeur, mais qu'il n'a pas pu les décoder.
Cela pourrait se produire parce que vous avez eu beaucoup de perte de paquets, ou peut-être que le décodeur s'est écrasé.

Selon la [RFC 5104](https://tools.ietf.org/html/rfc5104#section-4.3.1.2), `FIR` ne doit pas être utilisé lorsque des paquets ou des images sont perdus. C'est le travail de `PLI`. `FIR` demande une image clé pour des raisons autres que la perte de paquets - par exemple lorsqu'un nouveau membre entre dans une conférence vidéo. Ils ont besoin d'une image clé complète pour commencer à décoder le flux vidéo, le décodeur abandonnera les images jusqu'à ce que l'image clé arrive.

C'est une bonne idée pour un récepteur de demander une image clé complète juste après la connexion, cela minimise le délai entre la connexion et l'apparition d'une image sur l'écran de l'utilisateur.

Les paquets `PLI` font partie des messages de rétroaction spécifiques à la charge utile.

En pratique, le logiciel qui est capable de gérer à la fois les paquets `PLI` et `FIR` agira de la même manière dans les deux cas. Il enverra un signal à l'encodeur pour produire une nouvelle image clé complète.

### Accusé de réception négatif
Un `NACK` demande qu'un expéditeur retransmette un seul paquet RTP. Cela est généralement causé par la perte d'un paquet RTP, mais pourrait également se produire parce qu'il est en retard.

Les `NACK` sont beaucoup plus efficaces en bande passante que de demander que toute l'image soit envoyée à nouveau. Étant donné que RTP divise les paquets en très petits morceaux, vous ne demandez vraiment qu'une petite pièce manquante. Le récepteur crée un message RTCP avec le SSRC et le numéro de séquence. Si l'expéditeur n'a pas ce paquet RTP disponible pour le renvoyer, il ignore simplement le message.

### Rapports d'expéditeur et de récepteur
Ces rapports sont utilisés pour envoyer des statistiques entre les agents. Cela communique la quantité de paquets réellement reçus et la gigue.

Les rapports peuvent être utilisés pour les diagnostics et le contrôle de congestion.

## Comment RTP/RTCP résolvent les problèmes ensemble
RTP et RTCP travaillent ensuite ensemble pour résoudre tous les problèmes causés par les réseaux. Ces techniques changent encore constamment !

### Correction d'erreur directe
Également connu sous le nom de FEC. Une autre méthode pour gérer la perte de paquets. FEC, c'est lorsque vous envoyez les mêmes données plusieurs fois, sans même qu'elles soient demandées. Cela se fait au niveau RTP, ou même plus bas avec le codec.

Si la perte de paquets pour un appel est stable, alors FEC est une solution de latence beaucoup plus faible que NACK. Le temps d'aller-retour pour avoir à demander, puis retransmettre le paquet manquant peut être significatif pour les NACK.

### Débit adaptatif et estimation de bande passante
Comme discuté dans le chapitre [Réseau en temps réel](../05-real-time-networking/), les réseaux sont imprévisibles et peu fiables. La disponibilité de la bande passante peut changer plusieurs fois au cours d'une session.
Il n'est pas rare de voir la bande passante disponible changer de façon spectaculaire (ordres de grandeur) en une seconde.

L'idée principale est d'ajuster le débit d'encodage en fonction de la bande passante réseau disponible prédite, actuelle et future.
Cela garantit qu'un signal vidéo et audio de la meilleure qualité possible est transmis, et que la connexion n'est pas interrompue en raison de la congestion du réseau.
Les heuristiques qui modélisent le comportement du réseau et essaient de le prédire sont connues sous le nom d'estimation de bande passante.

Il y a beaucoup de nuances à cela, explorons donc plus en détail.

## Identification et communication de l'état du réseau
RTP/RTCP fonctionne sur tous les types de réseaux différents, et en conséquence, il est courant qu'une partie de la
communication soit abandonnée sur son chemin de l'expéditeur au récepteur. Étant construit sur UDP,
il n'y a pas de mécanisme intégré pour la retransmission de paquets, et encore moins pour gérer le contrôle de congestion.

Pour offrir aux utilisateurs la meilleure expérience, WebRTC doit estimer les qualités du chemin réseau, et
s'adapter à la façon dont ces qualités changent au fil du temps. Les traits clés à surveiller incluent : la bande passante disponible (dans chaque direction, car elle peut ne pas être symétrique), le temps d'aller-retour et la gigue (fluctuations
du temps d'aller-retour). Il doit tenir compte de la perte de paquets et communiquer les changements dans ces
propriétés à mesure que les conditions réseau évoluent.

Il y a deux objectifs principaux pour ces protocoles :

1. Estimer la bande passante disponible (dans chaque direction) prise en charge par le réseau.
2. Communiquer les caractéristiques du réseau entre l'expéditeur et le récepteur.

RTP/RTCP a trois approches différentes pour résoudre ce problème. Elles ont toutes leurs avantages et leurs inconvénients,
et généralement chaque génération s'est améliorée par rapport à ses prédécesseurs. L'implémentation que vous utilisez dépendra principalement de la pile logicielle disponible pour vos clients et des bibliothèques disponibles pour
construire votre application.

### Rapports de récepteur / Rapports d'expéditeur
La première implémentation est la paire de rapports de récepteur et son complément, les rapports d'expéditeur. Ces
messages RTCP sont définis dans la [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4), et sont
responsables de la communication de l'état du réseau entre les points de terminaison. Les rapports de récepteur se concentrent sur
la communication des qualités du réseau (y compris la perte de paquets, le temps d'aller-retour et la gigue), et
ils s'associent à d'autres algorithmes qui sont alors responsables de l'estimation de la bande passante disponible en fonction de
ces rapports.

Les rapports d'expéditeur et de récepteur (SR et RR) dressent ensemble un tableau de la qualité du réseau. Ils sont
envoyés selon un calendrier pour chaque SSRC, et ce sont les entrées utilisées lors de l'estimation de la bande passante disponible. Ces estimations sont faites par l'expéditeur après avoir reçu les données RR, contenant les
champs suivants :

* **Fraction perdue** - Quel pourcentage de paquets a été perdu depuis le dernier rapport de récepteur.
* **Nombre cumulatif de paquets perdus** - Combien de paquets ont été perdus pendant tout l'appel.
* **Numéro de séquence le plus élevé étendu reçu** - Quel était le dernier numéro de séquence reçu, et
  combien de fois a-t-il débordé.
* **Gigue d'interarrivée** - La gigue glissante pour tout l'appel.
* **Horodatage du dernier rapport d'expéditeur** - Dernière heure connue sur l'expéditeur, utilisée pour le calcul du temps d'aller-retour.

SR et RR travaillent ensemble pour calculer le temps d'aller-retour.

L'expéditeur inclut son heure locale, `sendertime1` dans SR. Lorsque le récepteur obtient un paquet SR, il
renvoie RR. Entre autres choses, le RR inclut `sendertime1` qui vient d'être reçu de l'expéditeur.
Il y aura un délai entre la réception du SR et l'envoi du RR. Pour cette raison, le RR inclut également un temps "délai depuis le dernier rapport d'expéditeur" - `DLSR`. Le `DLSR` est utilisé pour ajuster l'estimation du temps d'aller-retour plus tard dans le processus. Une fois que l'expéditeur reçoit le RR, il soustrait
`sendertime1` et `DLSR` de l'heure actuelle `sendertime2`. Ce delta de temps est appelé délai de propagation aller-retour ou temps d'aller-retour.

`rtt = sendertime2 - sendertime1 - DLSR`

Temps d'aller-retour en langage clair :
- Je vous envoie un message avec la lecture actuelle de mon horloge, disons qu'il est 4:20pm, 42 secondes et 420 millisecondes.
- Vous me renvoyez ce même horodatage.
- Vous incluez également le temps écoulé entre la lecture de mon message et l'envoi du message de retour, disons 5 millisecondes.
- Une fois que je reçois l'heure de retour, je regarde à nouveau l'horloge.
- Maintenant mon horloge dit 4:20pm, 42 secondes 690 millisecondes.
- Cela signifie qu'il a fallu 265 millisecondes (690 - 420 - 5) pour vous atteindre et revenir vers moi.
- Par conséquent, le temps d'aller-retour est de 265 millisecondes.

![Temps d'aller-retour](../images/06-rtt.png "Temps d'aller-retour")

<!-- Missing: What is an example congestion-control alg that pairs with RR/SR? -->

### TMMBR, TMMBN, REMB et TWCC, associés à GCC

#### Contrôle de congestion Google (GCC)
L'algorithme de contrôle de congestion Google (GCC) (décrit dans
[draft-ietf-rmcat-gcc-02](https://tools.ietf.org/html/draft-ietf-rmcat-gcc-02)) relève le
défi de l'estimation de la bande passante. Il s'associe à une variété d'autres protocoles pour faciliter les
exigences de communication associées. Par conséquent, il est bien adapté pour s'exécuter soit du côté
récepteur (lorsqu'il est exécuté avec TMMBR/TMMBN ou REMB) soit du côté expéditeur (lorsqu'il est exécuté avec TWCC).

Pour arriver à des estimations de la bande passante disponible, GCC se concentre sur la perte de paquets et les fluctuations du temps d'arrivée des images comme ses deux métriques principales. Il exécute ces métriques à travers deux contrôleurs liés : le
contrôleur basé sur les pertes et le contrôleur basé sur les délais.

Le premier composant de GCC, le contrôleur basé sur les pertes, est simple :

* Si la perte de paquets est supérieure à 10%, l'estimation de la bande passante est réduite.
* Si la perte de paquets est entre 2 et 10%, l'estimation de la bande passante reste la même.
* Si la perte de paquets est inférieure à 2%, l'estimation de la bande passante est augmentée.

Les mesures de perte de paquets sont prises fréquemment. Selon le protocole de communication associé,
la perte de paquets peut soit être explicitement communiquée (comme avec TWCC) soit déduite (comme avec TMMBR/TMMBN
et REMB). Ces pourcentages sont évalués sur des fenêtres de temps d'environ une seconde.

Le contrôleur basé sur les délais coopère avec le contrôleur basé sur les pertes, et examine les variations dans 
le temps d'arrivée des paquets. Ce contrôleur basé sur les délais vise à identifier quand les liens réseau deviennent
de plus en plus congestionnés, et peut réduire les estimations de bande passante même avant que la perte de paquets ne se produise. La
théorie est que l'interface réseau la plus occupée le long du chemin continuera à mettre en file d'attente des paquets
jusqu'à ce que l'interface manque de capacité dans ses tampons. Si cette interface continue à recevoir
plus de trafic qu'elle n'est capable d'envoyer, elle sera forcée d'abandonner tous les paquets qu'elle ne peut pas adapter dans
son espace tampon. Ce type de perte de paquets est particulièrement perturbateur pour la communication à faible latence/en temps réel, mais il peut également dégrader le débit pour toute communication sur ce lien et devrait
idéalement être évité. Ainsi, GCC essaie de déterminer si les liens réseau développent des profondeurs de file d'attente de plus en plus grandes _avant_ que la perte de paquets ne se produise réellement. Il réduira l'utilisation de la bande passante s'il observe
des délais de mise en file d'attente accrus au fil du temps.

Pour y parvenir, GCC essaie de déduire les augmentations de profondeur de file d'attente en mesurant des augmentations subtiles du temps d'aller-retour. Il enregistre le "temps d'inter-arrivée" des images, `t(i) - t(i-1)` : la différence de temps d'arrivée
de deux groupes de paquets (généralement, des images vidéo consécutives). Ces groupes de paquets partent fréquemment
à intervalles de temps réguliers (par exemple, toutes les 1/24 secondes pour une vidéo à 24 fps). En conséquence,
mesurer le temps d'inter-arrivée est alors aussi simple que d'enregistrer la différence de temps entre le début de
la première groupe de paquets (c'est-à-dire l'image) et la première image de la suivante.

Dans le diagramme ci-dessous, l'augmentation médiane du délai inter-paquets est de +20 msec, un indicateur clair de
congestion du réseau.

![TWCC avec délai](../images/06-twcc.png "TWCC avec délai")

Si le temps d'inter-arrivée augmente au fil du temps, c'est une preuve présumée d'une profondeur de file d'attente accrue sur
les interfaces réseau de connexion et considéré comme une congestion du réseau. (Note : GCC est assez intelligent pour
contrôler ces mesures pour les fluctuations de taille d'octets d'image.) GCC affine ses mesures de latence
en utilisant un [filtre de Kalman](https://en.wikipedia.org/wiki/Kalman_filter) et prend de nombreuses
mesures des temps d'aller-retour du réseau (et de ses variations) avant de signaler la congestion. On peut
penser au filtre de Kalman de GCC comme prenant la place d'une régression linéaire : aidant à faire des prédictions précises même lorsque la gigue ajoute du bruit dans les mesures de timing. Lors du signalement de la congestion, GCC
réduira le débit disponible. Alternativement, dans des conditions réseau stables, il peut lentement
augmenter ses estimations de bande passante pour tester des valeurs de charge plus élevées.

#### TMMBR, TMMBN et REMB
Pour TMMBR/TMMBN et REMB, le côté récepteur estime d'abord la bande passante entrante disponible (en utilisant un
protocole tel que GCC), puis communique ces estimations de bande passante aux expéditeurs distants. Ils
n'ont pas besoin d'échanger des détails sur la perte de paquets ou d'autres qualités sur la congestion du réseau
parce que fonctionner du côté récepteur leur permet de mesurer le temps d'inter-arrivée et la perte de paquets
directement. Au lieu de cela, TMMBR, TMMBN et REMB échangent juste les estimations de bande passante elles-mêmes :

* **Demande de débit binaire maximum temporaire du flux média** - Une mantisse/exposant d'un débit binaire demandé
  pour un seul SSRC.
* **Notification de débit binaire maximum temporaire du flux média** - Un message pour notifier qu'un TMMBR a
  été reçu.
* **Débit binaire maximum estimé du récepteur** - Une mantisse/exposant d'un débit binaire demandé pour la
  session entière.

TMMBR et TMMBN sont venus en premier et sont définis dans la [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB
est venu plus tard, il y avait un brouillon soumis dans
[draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), mais il
n'a jamais été standardisé.

Un exemple de session qui utilise REMB pourrait se comporter comme suit :

![REMB](../images/06-remb.png "REMB")

Cette méthode fonctionne bien sur le papier. L'expéditeur reçoit l'estimation du récepteur, règle le débit binaire de l'encodeur à la valeur reçue. Et voilà ! Nous nous sommes adaptés aux conditions du réseau.

Cependant, en pratique, l'approche REMB a plusieurs inconvénients.

L'inefficacité de l'encodeur est la première. Lorsque vous définissez un débit binaire pour l'encodeur, il ne produira pas nécessairement
exactement le débit binaire que vous avez demandé. L'encodage peut produire plus ou moins de bits, selon les
paramètres de l'encodeur et l'image en cours d'encodage.

Par exemple, utiliser l'encodeur x264 avec `tune=zerolatency` peut s'écarter significativement du débit binaire cible spécifié. Voici un scénario possible :

- Disons que nous commençons par définir le débit binaire à 1000 kbps.
- L'encodeur ne produit que 700 kbps, car il n'y a pas assez de fonctionnalités à haute fréquence à encoder. (AKA - "regarder un mur".)
- Imaginons également que le récepteur obtienne la vidéo à 700 kbps avec zéro perte de paquets. Il applique ensuite la règle REMB 1 pour augmenter le débit binaire entrant de 8%.
- Le récepteur envoie un paquet REMB avec une suggestion de 756 kbps (700 kbps * 1.08) à l'expéditeur.
- L'expéditeur règle le débit binaire de l'encodeur à 756 kbps.
- L'encodeur produit un débit binaire encore plus faible.
- Ce processus continue à se répéter, abaissant le débit binaire au minimum absolu.

Vous pouvez voir comment cela causerait un réglage lourd des paramètres de l'encodeur, et surprendrait les utilisateurs avec une vidéo impossible à regarder même sur une excellente connexion.

#### Contrôle de congestion étendu au transport
Le contrôle de congestion étendu au transport est le dernier développement dans la communication de l'état du réseau RTCP. Il est défini dans
[draft-holmer-rmcat-transport-wide-cc-extensions-01](https://datatracker.ietf.org/doc/html/draft-holmer-rmcat-transport-wide-cc-extensions-01),
mais n'a également jamais été standardisé.

TWCC utilise un principe assez simple :

![TWCC](../images/06-twcc-idea.png "TWCC")

Avec REMB, le récepteur instruit le côté émetteur du débit binaire de téléchargement disponible. Il utilise
des mesures précises sur la perte de paquets déduite et des données qu'il possède uniquement sur le temps d'arrivée inter-paquets.

TWCC est presque une approche hybride entre les générations de protocoles SR/RR et REMB. Il ramène les
estimations de bande passante du côté de l'expéditeur (similaire à SR/RR), mais sa technique d'estimation de bande passante
ressemble plus étroitement à la génération REMB.

Avec TWCC, le récepteur fait savoir à l'expéditeur l'heure d'arrivée de chaque paquet. C'est suffisant
d'informations pour que l'expéditeur mesure la variation du délai d'arrivée inter-paquets, ainsi que pour identifier
quels paquets ont été abandonnés ou sont arrivés trop tard pour contribuer au flux audio/vidéo. Avec ces données
échangées fréquemment, l'expéditeur est capable de s'adapter rapidement aux conditions réseau changeantes et
de varier sa bande passante de sortie en utilisant un algorithme tel que GCC.

L'expéditeur garde une trace des paquets envoyés, leurs numéros de séquence, tailles et horodatages. Lorsque l'expéditeur reçoit des messages RTCP du récepteur, il compare les délais inter-paquets d'envoi avec
les délais de réception. Si les délais de réception augmentent, cela signale une congestion du réseau, et l'expéditeur
doit prendre des mesures correctives.

En fournissant à l'expéditeur les données brutes, TWCC offre une excellente vue des conditions réseau en temps réel :
- Comportement de perte de paquets presque instantané, jusqu'aux paquets perdus individuels
- Débit binaire d'envoi précis
- Débit binaire de réception précis
- Mesure de la gigue
- Différences entre les délais d'envoi et de réception des paquets
- Description de la façon dont le réseau a toléré la livraison de bande passante en rafale ou stable

L'une des contributions les plus importantes de TWCC est la flexibilité qu'il offre aux
développeurs WebRTC. En consolidant l'algorithme de contrôle de congestion du côté expéditeur, il permet un code client simple
qui peut être largement utilisé et nécessite des améliorations minimales au fil du temps. Les algorithmes complexes de contrôle de congestion peuvent ensuite être itérés plus rapidement sur le matériel qu'ils contrôlent directement (comme l'unité de transfert sélectif, discutée dans la section 8). Dans le cas des navigateurs et
des appareils mobiles, cela signifie que ces clients peuvent bénéficier d'améliorations d'algorithmes sans avoir à
attendre la standardisation ou les mises à jour du navigateur (ce qui peut prendre beaucoup de temps pour être largement disponible).

## Alternatives d'estimation de bande passante
L'implémentation la plus déployée est "A Google Congestion Control Algorithm for Real-Time
Communication" définie dans
[draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).

Il existe plusieurs alternatives à GCC, par exemple [NADA: A Unified Congestion Control Scheme for
Real-Time Media](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) et [SCReAM - Self-Clocked
Rate Adaptation for Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
