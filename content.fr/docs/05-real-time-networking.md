---
title: Réseau en temps réel
type: docs
weight: 6
---

# Réseau en temps réel

## Pourquoi le réseau est-il si important dans la communication en temps réel ?

Les réseaux sont le facteur limitant dans la communication en temps réel. Dans un monde idéal, nous aurions une bande passante illimitée
et les paquets arriveraient instantanément. Ce n'est cependant pas le cas. Les réseaux sont limités, et les conditions
peuvent changer à tout moment. Mesurer et observer les conditions du réseau est également un problème difficile. Vous pouvez obtenir des comportements différents
selon le matériel, le logiciel et sa configuration.

La communication en temps réel pose également un problème qui n'existe pas dans la plupart des autres domaines. Pour un développeur web, ce n'est pas fatal
si votre site web est plus lent sur certains réseaux. Tant que toutes les données arrivent, les utilisateurs sont satisfaits. Avec WebRTC, si vos données sont
en retard, elles sont inutiles. Personne ne se soucie de ce qui a été dit dans une conférence téléphonique il y a 5 secondes. Donc, lors du développement d'un système de communication en temps réel,
vous devez faire un compromis. Quelle est ma limite de temps, et combien de données puis-je envoyer ?

Ce chapitre couvre les concepts qui s'appliquent à la fois à la communication de données et de médias. Dans les chapitres ultérieurs, nous allons au-delà
du théorique et discutons de la façon dont les sous-systèmes de médias et de données de WebRTC résolvent ces problèmes.

## Quels sont les attributs du réseau qui le rendent difficile ?
Le code qui fonctionne efficacement sur tous les réseaux est compliqué. Vous avez beaucoup de facteurs différents, et ils
peuvent tous s'affecter mutuellement subtilement. Ce sont les problèmes les plus courants que les développeurs rencontreront.

#### Bande passante
La bande passante est le taux maximum de données qui peuvent être transférées sur un chemin donné. Il est important de se rappeler
que ce n'est pas non plus un nombre statique. La bande passante changera le long de la route à mesure que plus (ou moins) de personnes l'utilisent.

#### Temps de transmission et temps de trajet aller-retour
Le temps de transmission est le temps qu'il faut pour qu'un paquet arrive à sa destination. Comme la bande passante, ce n'est pas constant. Le temps de transmission peut fluctuer à tout moment.

`transmission_time = receive_time - send_time`

Pour calculer le temps de transmission, vous avez besoin d'horloges sur l'expéditeur et le récepteur synchronisées avec une précision à la milliseconde.
Même une petite déviation produirait une mesure de temps de transmission peu fiable.
Étant donné que WebRTC fonctionne dans des environnements hautement hétérogènes, il est presque impossible de s'appuyer sur une synchronisation temporelle parfaite entre les hôtes.

La mesure du temps de trajet aller-retour est une solution de contournement pour une synchronisation d'horloge imparfaite.

Au lieu d'opérer sur des horloges distribuées, un pair WebRTC envoie un paquet spécial avec son propre horodatage `sendertime1`.
Un pair coopérant reçoit le paquet et reflète l'horodatage vers l'expéditeur.
Une fois que l'expéditeur original obtient le temps réfléchi, il soustrait l'horodatage `sendertime1` du temps actuel `sendertime2`.
Ce delta de temps est appelé "délai de propagation aller-retour" ou plus communément temps aller-retour.

`rtt = sendertime2 - sendertime1`

La moitié du temps aller-retour est considérée comme une approximation suffisamment bonne du temps de transmission.
Cette solution de contournement n'est pas sans inconvénients.
Elle suppose qu'il faut un temps égal pour envoyer et recevoir des paquets.
Cependant, sur les réseaux cellulaires, les opérations d'envoi et de réception peuvent ne pas être symétriques dans le temps.
Vous avez peut-être remarqué que les vitesses de téléchargement sur votre téléphone sont presque toujours inférieures aux vitesses de téléchargement descendant.

`transmission_time = rtt/2`

Les aspects techniques de la mesure du temps aller-retour sont décrits plus en détail dans le [chapitre Rapports d'expéditeur et de récepteur RTCP](../06-media-communication/#receiver-reports--sender-reports).

#### Gigue
La gigue est le fait que le `temps de transmission` peut varier pour chaque paquet. Vos paquets pourraient être retardés, mais ensuite arriver en rafales.

#### Perte de paquets
La perte de paquets est lorsque les messages sont perdus en transmission. La perte pourrait être régulière, ou elle pourrait venir en pics.
Cela pourrait être dû au type de réseau comme le satellite ou le Wi-Fi. Ou cela pourrait être introduit par le logiciel en cours de route.

#### Unité de transmission maximale
L'unité de transmission maximale est la limite de la taille d'un seul paquet. Les réseaux ne vous permettent pas d'envoyer
un message géant. Au niveau du protocole, les messages peuvent devoir être divisés en plusieurs paquets plus petits.

La MTU différera également en fonction du chemin réseau que vous empruntez. Vous pouvez
utiliser un protocole comme [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) pour déterminer la plus grande taille de paquet que vous pouvez envoyer.

### Congestion
La congestion est lorsque les limites du réseau ont été atteintes. C'est généralement parce que vous avez atteint le pic
de bande passante que la route actuelle peut gérer. Ou cela pourrait être imposé par l'opérateur comme des limites horaires que votre FAI configure.

La congestion se manifeste de nombreuses façons différentes. Il n'y a pas de comportement standardisé. Dans la plupart des cas, lorsque la congestion est
atteinte, le réseau abandonnera les paquets excédentaires. Dans d'autres cas, le réseau mettra en mémoire tampon. Cela augmentera le temps de transmission
pour vos paquets. Vous pourriez également voir plus de gigue à mesure que votre réseau devient congestionné. C'est un domaine en évolution rapide
et de nouveaux algorithmes pour la détection de congestion sont encore en cours d'écriture.

### Dynamique
Les réseaux sont incroyablement dynamiques et les conditions peuvent changer rapidement. Au cours d'un appel, vous pouvez envoyer et recevoir des centaines de milliers de paquets.
Ces paquets passeront par plusieurs sauts. Ces sauts seront partagés par des millions d'autres utilisateurs. Même dans votre réseau local, vous pourriez avoir
des films HD en cours de téléchargement ou peut-être qu'un appareil décide de télécharger une mise à jour logicielle.

Avoir un bon appel n'est pas aussi simple que de mesurer votre réseau au démarrage. Vous devez constamment évaluer. Vous devez également gérer tous les différents
comportements qui proviennent d'une multitude de matériels et de logiciels réseau.

## Résolution de la perte de paquets
La gestion de la perte de paquets est le premier problème à résoudre. Il existe plusieurs façons de le résoudre, chacune avec ses propres avantages. Cela dépend de ce que vous envoyez et de votre
tolérance à la latence. Il est également important de noter que toutes les pertes de paquets ne sont pas fatales. Perdre de la vidéo pourrait ne pas être un problème, l'œil humain pourrait ne pas
même être capable de la percevoir. Perdre les messages texte d'un utilisateur est fatal.

Disons que vous envoyez 10 paquets, et que les paquets 5 et 6 sont perdus. Voici les façons de le résoudre.

### Accusés de réception
Les accusés de réception sont lorsque le récepteur notifie l'expéditeur de chaque paquet qu'il a reçu. L'expéditeur est conscient de la perte de paquets lorsqu'il obtient un accusé de réception
pour un paquet deux fois qui n'est pas final. Lorsque l'expéditeur obtient un `ACK` pour le paquet 4 deux fois, il sait que le paquet 5 n'a pas encore été vu.

### Accusés de réception sélectifs
Les accusés de réception sélectifs sont une amélioration des accusés de réception. Un récepteur peut envoyer un `SACK` qui accuse réception de plusieurs paquets et notifie l'expéditeur des lacunes.
Maintenant l'expéditeur peut obtenir un `SACK` pour les paquets 4 et 7. Il sait alors qu'il doit renvoyer les paquets 5 et 6.

### Accusés de réception négatifs
Les accusés de réception négatifs résolvent le problème de manière opposée. Au lieu de notifier l'expéditeur de ce qu'il a reçu, le récepteur notifie l'expéditeur de ce qui a été perdu. Dans notre cas, un `NACK`
sera envoyé pour les paquets 5 et 6. L'expéditeur ne connaît que les paquets que le récepteur souhaite recevoir à nouveau.

### Correction d'erreur directe
La correction d'erreur directe corrige la perte de paquets de manière préventive. L'expéditeur envoie des données redondantes, ce qui signifie qu'un paquet perdu n'affecte pas le flux final. Un algorithme populaire pour
cela est la correction d'erreur Reed–Solomon.

Cela réduit la latence/complexité de l'envoi et du traitement des accusés de réception. La correction d'erreur directe est un gaspillage de bande passante si le réseau dans lequel vous vous trouvez n'a aucune perte.

## Résolution de la gigue
La gigue est présente dans la plupart des réseaux. Même à l'intérieur d'un LAN, vous avez de nombreux appareils envoyant des données à des vitesses fluctuantes. Vous pouvez facilement observer la gigue en pinguant un autre appareil avec la commande `ping` et en remarquant les fluctuations de la latence aller-retour.

Pour résoudre la gigue, les clients utilisent un JitterBuffer. Le JitterBuffer garantit un temps de livraison stable des paquets. L'inconvénient est que JitterBuffer ajoute une certaine latence aux paquets qui arrivent tôt.
L'avantage est que les paquets en retard ne causent pas de gigue. Imaginez que pendant un appel, vous voyez les temps d'arrivée de paquets suivants :

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

Dans ce cas, environ 1,8 ms serait un bon choix. Les paquets qui arrivent en retard utiliseront notre fenêtre de latence. Les paquets qui arrivent tôt seront retardés un peu et peuvent
remplir la fenêtre épuisée par les paquets en retard. Cela signifie que nous n'avons plus de bégaiement et que nous fournissons un taux de livraison fluide au client.

### Fonctionnement du JitterBuffer

![JitterBuffer](../images/05-jitterbuffer.png "JitterBuffer")

Chaque paquet est ajouté au tampon de gigue dès qu'il est reçu.
Une fois qu'il y a suffisamment de paquets pour reconstruire la trame, les paquets qui composent la trame sont libérés du tampon et émis pour le décodage.
Le décodeur, à son tour, décode et dessine la trame vidéo sur l'écran de l'utilisateur.
Étant donné que le tampon de gigue a une capacité limitée, les paquets qui restent trop longtemps dans le tampon seront abandonnés.

En savoir plus sur la façon dont les trames vidéo sont converties en paquets RTP, et pourquoi la reconstruction est nécessaire [dans le chapitre communication média](../06-media-communication/#rtp).

`jitterBufferDelay` fournit un excellent aperçu de vos performances réseau et de son influence sur la fluidité de lecture.
Il fait partie de l'[API de statistiques WebRTC](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) pertinent pour le flux entrant du récepteur.
Le délai définit le temps que les trames vidéo passent dans le tampon de gigue avant d'être émises pour le décodage.
Un long délai de tampon de gigue signifie que votre réseau est fortement congestionné.

## Détection de la congestion
Avant même de pouvoir résoudre la congestion, nous devons la détecter. Pour la détecter, nous utilisons un contrôleur de congestion. C'est un sujet compliqué, et il change encore rapidement.
De nouveaux algorithmes sont encore publiés et testés. À un niveau élevé, ils fonctionnent tous de la même manière. Un contrôleur de congestion fournit des estimations de bande passante étant donné certaines entrées.
Voici quelques entrées possibles :

* **Perte de paquets** - Les paquets sont abandonnés à mesure que le réseau devient congestionné.
* **Gigue** - À mesure que l'équipement réseau devient plus surchargé, la mise en file d'attente des paquets rendra les temps erratiques.
* **Temps aller-retour** - Les paquets mettent plus de temps à arriver lorsqu'ils sont congestionnés. Contrairement à la gigue, le temps aller-retour continue d'augmenter.
* **Notification explicite de congestion** - Les réseaux plus récents peuvent marquer les paquets comme étant à risque d'être abandonnés pour soulager la congestion.

Ces valeurs doivent être mesurées en continu pendant l'appel. L'utilisation du réseau peut augmenter ou diminuer, donc la bande passante disponible pourrait changer constamment.

## Résolution de la congestion
Maintenant que nous avons une bande passante estimée, nous devons ajuster ce que nous envoyons. La façon dont nous ajustons dépend du type de données que nous voulons envoyer.

### Envoyer plus lentement
Limiter la vitesse à laquelle vous envoyez des données est la première solution pour prévenir la congestion. Le contrôleur de congestion vous donne une estimation, et c'est la
responsabilité de l'expéditeur de limiter le débit.

C'est la méthode utilisée pour la plupart des communications de données. Avec des protocoles comme TCP, tout cela est fait par le système d'exploitation et est complètement transparent pour les utilisateurs et les développeurs.

### Envoyer moins
Dans certains cas, nous pouvons envoyer moins d'informations pour satisfaire nos limites. Nous avons également des délais stricts sur l'arrivée de nos données, donc nous ne pouvons pas envoyer plus lentement. Ce sont les contraintes
sous lesquelles les médias en temps réel tombent.

Si nous n'avons pas assez de bande passante disponible, nous pouvons réduire la qualité de la vidéo que nous envoyons. Cela nécessite une boucle de rétroaction étroite entre votre encodeur vidéo et le contrôleur de congestion.
