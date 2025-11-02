---
title: Débogage
type: docs
weight: 10
---

# Débogage
Le débogage de WebRTC peut être une tâche décourageante. Il y a de nombreuses parties mobiles, et elles peuvent toutes se casser indépendamment. Si vous n'êtes pas prudent, vous pourriez perdre des semaines à chercher au mauvais endroit. Lorsque vous trouvez enfin la partie qui est cassée, vous devrez apprendre un peu pour comprendre pourquoi.

Ce chapitre vous mettra dans l'état d'esprit nécessaire pour déboguer WebRTC. Il vous montrera comment décomposer le problème. Après avoir identifié le problème, nous ferons un tour rapide des outils de débogage populaires.

## Isoler le problème

Lorsque vous déboguez, vous devez isoler d'où vient le problème. Commencez par le début de la pile WebRTC et descendez jusqu'à ce que vous trouviez le coupable. Voici comment la pile s'organise :

### Échec de signalisation

L'échec de signalisation est lorsque vous ne pouvez pas obtenir une `SessionDescription` locale/distante avec succès. Cela signifie que même avant de créer une connexion réseau, quelque chose s'est mal passé. Y a-t-il des erreurs dans les attributs SDP que vous avez définies ? Les deux agents ont-ils un codec en commun ?

Vous devez vous assurer que les deux pairs peuvent effectuer l'échange entier. Si vous ne répondez pas avec une réponse dans un certain délai, certaines implémentations échoueront.

### Échec réseau

L'échec réseau est lorsque les deux agents WebRTC ne peuvent pas se connecter. C'est la partie la plus difficile de WebRTC. Le débogage du réseau peut être assez difficile car l'échec peut survenir à différents endroits. Voici quelques endroits où chercher :

#### Appairage de candidats

Avez-vous généré des candidats des deux côtés ? Vous devriez voir un candidat de chaque type défini dans votre `SessionDescription` si tout fonctionne correctement.

Si vous ne générez pas de candidats de relais, cela signifie que votre connexion au serveur TURN échoue. Assurez-vous que vous utilisez le protocole correct (TURN s'exécute sur UDP, TCP ou TLS). Vous pourriez également avoir saisi des informations d'identification incorrectes.

Si vous ne générez pas de candidats mDNS, cela signifie que l'agent réseau n'a pas pu interroger le LAN local. Cela peut être dû à des permissions ou parce que vous n'êtes tout simplement pas sur un LAN.

Si vous ne générez pas de candidats réflexifs, cela signifie que vos requêtes STUN ne réussissent pas. Assurez-vous que rien n'est en train de bloquer les paquets UDP sortants. Vous pouvez tester votre serveur STUN avec des outils en ligne de commande comme `netcat`.

Même si vous générez ces candidats, votre réseau peut toujours bloquer le trafic. Certains réseaux n'autorisent le trafic que vers/depuis des ports spécifiques ou des protocoles spécifiques. Vous pouvez avoir un candidat réflexif, mais le trafic est tout de même bloqué. Essayez d'utiliser un serveur TURN sur le port `443` sur TCP. `443` et `80` sont les ports les plus susceptibles de ne pas être filtrés car ils sont utilisés pour le trafic HTTPS et HTTP.

#### Connectivité réseau

Même si vous avez plusieurs candidats, vous ne pouvez peut-être toujours pas vous connecter ! Un candidat contient une adresse IP, qui peut être bloquée. Les réseaux d'entreprise peuvent bloquer tout le trafic UDP. Les FAI peuvent ne pas autoriser les connexions pair-à-pair.

Dans ces cas, vous devrez utiliser un candidat de relais. Vous pouvez forcer WebRTC à utiliser uniquement des candidats de relais si vous le souhaitez. C'est utile pour tester !

#### Pare-feu/Équipement réseau

Certains réseaux ont du matériel qui tente d'être intelligent. Il y a des dispositifs qui inspectent et tentent de modifier le trafic WebRTC. Certains modems et routeurs tentent d'ouvrir des ports ou de réécrire les messages. Ces dispositifs peuvent causer des problèmes car ils ne sont pas toujours bien implémentés.

### Échec de sécurité

L'échec de sécurité est lorsque la poignée de main DTLS échoue. Cela peut se produire pour plusieurs raisons. Si l'horloge d'un agent est incorrecte, il rejettera le certificat de l'autre. Si vous modifiez la `SessionDescription` entre les agents, l'empreinte digitale DTLS ne correspondra pas. Les agents réseau peuvent également bloquer ou modifier les messages DTLS.

### Échec de média

L'échec de média est lorsque deux agents sont connectés, mais ils n'obtiennent pas les médias qu'ils attendent. Vous devez d'abord vous assurer que les médias sont même envoyés. Certains réseaux peuvent supprimer les types de paquets de manière agressive, créant ainsi des conditions difficiles à reproduire.

Ensuite, vous devez déterminer si les codecs fonctionnent correctement. Assurez-vous que vous avez configuré votre MediaStream correctement. Certains déploiements peuvent échouer à encoder/décoder au début.

### Échec de données

L'échec de données est lorsque les canaux de données d'un agent ne fonctionnent pas. Tout d'abord, assurez-vous que SCTP est activé. Certaines implémentations ne l'activent pas par défaut.

Comme avec les médias, certains réseaux peuvent bloquer les paquets SCTP. Vous pouvez constater que SCTP fonctionne sur certains réseaux, mais pas sur tous.

## Outils du métier

Ces outils vous aideront à isoler les problèmes. Certains de ces outils sont plus utilisables si vous avez accès au serveur ou au réseau. Dans d'autres cas, vous ne pourrez examiner que le code côté client.

### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) est un utilitaire réseau en ligne de commande pour lire et écrire vers des connexions réseau en utilisant TCP ou UDP. Il est généralement disponible sous la commande `nc`.

Tester votre serveur STUN en utilisant netcat :

1. Préparez le paquet de requête de liaison de **20 octets** :

    ```
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    ```

    Interprétation :
    - `00 01` est le type de message.
    - `00 00` est la longueur de la section de données.
    - `21 12 a4 42` est le cookie magique.
    - et `54 45 53 54 54 45 53 54 54 45 53 54` (Se décode en ASCII : `TESTTESTTEST`) est l'ID de transaction de 12 octets.

2. Envoyez la requête et attendez la réponse de **32 octets** :

    ```
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    ```

    Interprétation :
    - `01 01` est le type de message
    - `00 0c` est la longueur de la section de données qui se décode en 12 en décimal
    - `21 12 a4 42` est le cookie magique
    - et `54 45 53 54 54 45 53 54 54 45 53 54` (Se décode en ASCII : `TESTTESTTEST`) est l'ID de transaction de 12 octets.
    - `00 20 00 08 00 01 6f 32 7f 36 de 89` sont les 12 octets de données, interprétation :
        - `00 20` est le type : `XOR-MAPPED-ADDRESS`
        - `00 08` est la longueur de la section de valeur qui se décode en 8 en décimal
        - `00 01 6f 32 7f 36 de 89` est la valeur des données, interprétation :
            - `00 01` est le type d'adresse (IPv4)
            - `6f 32` est le port XOR mappé
            - `7f 36 de 89` est l'adresse IP XOR mappée

Décoder la section XOR mappée est fastidieux, mais nous pouvons tromper le serveur STUN pour qu'il effectue un mappage XOR fictif, en fournissant un cookie magique fictif (invalide) défini sur `00 00 00 00` :

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

Faire un XOR contre le cookie magique fictif est idempotent, donc le port et l'adresse seront clairs dans la réponse. Cela ne fonctionnera pas dans toutes les situations, car certains routeurs manipulent les paquets qui passent, en trichant sur l'adresse IP. Si nous regardons la valeur de données retournée (derniers huit octets) :

  - `00 01 4e 20 5e 24 7a cb` est la valeur de données, interprétation :
    - `00 01` est le type d'adresse (IPv4)
    - `4e 20` est le port mappé, qui se décode en 20000 en décimal
    - `5e 24 7a cb` est l'adresse IP, qui se décode en `94.36.122.203` en notation décimale pointée.

### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) est un analyseur de paquets réseau de données en ligne de commande.

Commandes courantes :
- Capturer les paquets UDP vers et depuis le port 19302, imprimer un hexdump du contenu du paquet :

    `sudo tcpdump 'udp port 19302' -xx`

- Idem, mais sauvegarder les paquets dans un fichier PCAP (capture de paquets) pour inspection ultérieure :

    `sudo tcpdump 'udp port 19302' -w stun.pcap`

  Le fichier PCAP peut être ouvert avec l'application Wireshark : `wireshark stun.pcap`

### Wireshark

[Wireshark](https://www.wireshark.org) est un analyseur de protocoles réseau largement utilisé.

### Outils WebRTC du navigateur

Les navigateurs sont livrés avec des outils intégrés que vous pouvez utiliser pour inspecter les connexions que vous établissez. Chrome a [`chrome://webrtc-internals`](chrome://webrtc-internals) et [`chrome://webrtc-logs`](chrome://webrtc-logs). Firefox a [`about:webrtc`](about:webrtc).

## Latence
Comment savez-vous que vous avez une latence élevée ? Vous avez peut-être remarqué que votre vidéo est en retard, mais savez-vous précisément de combien elle est en retard ?
Pour pouvoir réduire cette latence, vous devez d'abord la mesurer.

La vraie latence est censée être mesurée de bout en bout. Cela signifie non seulement la latence du chemin réseau entre l'expéditeur et le récepteur, mais la latence combinée de la capture de caméra, de l'encodage des trames, de la transmission, de la réception, du décodage et de l'affichage, ainsi que des files d'attente possibles entre l'une de ces étapes.

La latence de bout en bout n'est pas une simple somme des latences de chaque composant.

Bien que vous puissiez théoriquement mesurer la latence des composants d'un pipeline de streaming vidéo en direct séparément puis les additionner, en pratique, au moins certains composants seront inaccessibles pour l'instrumentation, ou produiront des résultats significativement différents lorsqu'ils seront mesurés en dehors du pipeline.
Les profondeurs de file d'attente variables entre les étapes du pipeline, la topologie réseau et les changements d'exposition de la caméra ne sont que quelques exemples de composants qui affectent la latence de bout en bout.

La latence intrinsèque de chaque composant dans votre système de streaming en direct peut changer et affecter les composants en aval.
Même le contenu de la vidéo capturée affecte la latence.
Par exemple, il faut beaucoup plus de bits pour les caractéristiques haute fréquence comme les branches d'arbres, par rapport à un ciel bleu clair de basse fréquence.
Une caméra avec exposition automatique activée peut prendre _beaucoup_ plus que les 33 millisecondes attendues pour capturer une trame, même si le taux de capture est réglé sur 30 trames par seconde.
La transmission sur le réseau, en particulier cellulaire, est également très dynamique en raison de la demande changeante.
Plus d'utilisateurs introduisent plus de bruit dans l'air.
Votre emplacement physique (zones de signal faible notoires) et de multiples autres facteurs augmentent la perte de paquets et la latence.
Que se passe-t-il lorsque vous envoyez un paquet à une interface réseau, disons un adaptateur WiFi ou un modem LTE pour livraison ?
S'il ne peut pas être livré immédiatement, il est mis en file d'attente dans l'interface, plus la file d'attente est grande, plus de latence cette interface réseau introduit.

### Mesure manuelle de la latence de bout en bout
Lorsque nous parlons de latence de bout en bout, nous entendons le temps entre le moment où un événement se produit et où il est observé, c'est-à-dire les trames vidéo apparaissant sur l'écran.

```
LatenceDeBoutEnBout = T(observer) - T(se produire)
```

Une approche naïve consiste à enregistrer l'heure lorsqu'un événement se produit et à la soustraire de l'heure à l'observation.
Cependant, à mesure que la précision descend aux millisecondes, la synchronisation temporelle devient un problème.
Essayer de synchroniser les horloges à travers des systèmes distribués est principalement futile, même une petite erreur dans la synchronisation temporelle produit une mesure de latence peu fiable.

Une solution simple aux problèmes de synchronisation d'horloge est d'utiliser la même horloge.
Mettez l'expéditeur et le récepteur dans le même cadre de référence.

Imaginez que vous avez une horloge en millisecondes qui fait tic-tac ou toute autre source d'événements réellement.
Vous voulez mesurer la latence dans un système qui diffuse en direct l'horloge sur un écran distant en pointant une caméra vers elle.
Une façon évidente de mesurer le temps entre le tic du minuteur en millisecondes (T<sub>`se produire`</sub>) et les trames vidéo de l'horloge apparaissant sur l'écran (T<sub>`observer`</sub>) est la suivante :
- Pointez votre caméra vers l'horloge en millisecondes.
- Envoyez les trames vidéo à un récepteur qui se trouve au même emplacement physique.
- Prenez une photo (utilisez votre téléphone) du minuteur en millisecondes et de la vidéo reçue sur l'écran.
- Soustrayez les deux temps.

C'est la mesure de latence de bout en bout la plus vraie pour vous.
Elle prend en compte toutes les latences des composants (caméra, encodeur, réseau, décodeur) et ne dépend d'aucune synchronisation d'horloge.

![Latence DIY](../images/09-diy-latency.png "Mesure de latence DIY").
![Exemple de latence DIY](../images/09-diy-latency-happen-observe.png "Exemple de mesure de latence DIY")
Dans la photo ci-dessus, la latence de bout en bout mesurée est de 101 msec. L'événement qui se produit maintenant est 10:16:02.862, mais l'observateur du système de streaming en direct voit 10:16:02.761.

### Mesure automatique de la latence de bout en bout
Au moment de la rédaction (mai 2021), la norme WebRTC pour le délai de bout en bout est activement [discutée](https://github.com/w3c/webrtc-stats/issues/537).
Firefox a implémenté un ensemble d'API pour permettre aux utilisateurs de créer des mesures de latence automatiques sur les API WebRTC standard.

### Conseils de débogage de la latence
Étant donné que le débogage affectera probablement la latence mesurée, la règle générale est de simplifier votre configuration à la plus petite possible qui peut encore reproduire le problème.
Plus vous pouvez éliminer de composants, plus il sera facile de déterminer quel composant cause le problème de latence.

#### Débogage de la latence de la caméra

Pour tester uniquement la latence de la caméra, sautez complètement le streaming vidéo.
Accédez simplement au flux de la caméra sur le navigateur à l'aide de `getUserMedia` et passez-le à l'élément `<video>`.
Cela vous donnera les limites inférieures de la latence, puisque la latence de bout en bout inclut la latence de la caméra.
Si vous avez un problème de latence de caméra, toutes les optimisations de pipeline de streaming vidéo seront inutiles.

#### Débogage de la latence de l'encodeur

La latence de l'encodeur dépend de nombreux facteurs.
Les fabricants d'encodeurs peuvent sacrifier un peu de latence pour obtenir un débit plus élevé dans la même bande passante.
Ils peuvent également compter sur des techniques de codage qui utilisent des trames futures pour réduire la taille des trames actuelles.
Habituellement, il y a un compromis entre latence et qualité.
Les encodeurs logiciels et matériels exposent parfois des indicateurs pour contrôler ce compromis.
L'encodeur d'un fabricant peut également être tout simplement meilleur qu'un autre.
Réduire la résolution de la vidéo source ou diminuer la qualité de codage peut réduire la latence de l'encodeur.

#### Débogage de la latence du réseau

Le débogage de la latence du réseau dans un pipeline de streaming vidéo est difficile.
Le meilleur indicateur de la latence du réseau dans WebRTC est le temps aller-retour.
WebRTC utilise RTCP Receiver Reports pour mesurer le temps aller-retour.
La mesure du temps aller-retour est décrite dans le [chapitre 6 Communication média](../06-media-communication).

Le temps aller-retour mesure le temps qu'il faut à un paquet pour voyager de vous au pair et revenir.
Les paquets envoyés d'un pair distant traversent la même route réseau sur le chemin du retour, donc le temps aller-retour devrait être un indicateur fiable de votre latence réseau _approximative_.
Pourquoi approximative ? Parce que les conditions du réseau fluctuent et changent, mais cela vous donnera une idée approximative.
Pour voir l'impact des conditions du réseau sur votre latence de bout en bout, exécutez votre pipeline de streaming vidéo localement sur une machine.
Cela élimine tous les effets de la latence réseau et du tampon de gigue.
Comparez votre latence de bout en bout à travers le réseau avec celle sur la machine locale.
Ajoutez 1/2 du temps aller-retour, que vous avez obtenu à partir de la mesure RTCP Receiver Report, à la latence de bout en bout locale.
Vous devriez obtenir quelque chose de similaire à la latence de bout en bout à travers le réseau réel.

Une autre chose à considérer qui affecte la latence de bout en bout est le tampon de gigue.
Il est utilisé par le décodeur pour lisser le flux vidéo entrant et lisser les tremblements du réseau.
L'API WebRTC Stats expose les statistiques sur le tampon de gigue pour le flux entrant.
Essayez de réduire la taille du tampon de gigue, si votre implémentation WebRTC l'expose, et observez comment cela affecte votre latence de bout en bout.

#### Débogage de la latence du décodeur

La latence du décodeur dépend de nombreux facteurs.
Le décodeur peut avoir besoin de trames futures pour construire la trame actuelle.
Ou il peut être configuré pour supprimer des trames afin de rattraper le retard, ce qui peut introduire de la latence lorsque les conditions du réseau deviennent mauvaises.
Essayez d'utiliser différents décodeurs et voyez comment ils affectent la latence de bout en bout.
