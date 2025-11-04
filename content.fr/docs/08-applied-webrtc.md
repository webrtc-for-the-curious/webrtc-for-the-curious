---
title: WebRTC appliqué
type: docs
weight: 9
---

# WebRTC appliqué
Maintenant que vous savez comment fonctionne WebRTC, il est temps de construire avec ! Ce chapitre explore ce que les gens construisent avec WebRTC, et comment ils le construisent. Vous apprendrez toutes les choses intéressantes qui se
passent avec WebRTC. Le pouvoir de WebRTC a un coût. La construction de services WebRTC de qualité production est
difficile. Ce chapitre essaiera d'expliquer ces défis avant que vous ne les rencontriez.

## Par cas d'usage
Beaucoup pensent que WebRTC n'est qu'une technologie pour la conférence dans le navigateur web. C'est tellement plus que cela cependant !
WebRTC est utilisé dans une large gamme d'applications. De nouveaux cas d'usage apparaissent tout le temps. Dans ce chapitre, nous énumérerons quelques-uns des plus courants et comment WebRTC les révolutionne.

### Conférence
La conférence est le cas d'usage original de WebRTC. Le protocole contient quelques fonctionnalités nécessaires qu'aucun autre protocole n'offre
dans le navigateur. Vous pourriez construire un système de conférence avec WebSockets et il pourrait fonctionner dans des conditions optimales. Si vous voulez
quelque chose qui peut être déployé dans des conditions réseau du monde réel, WebRTC est le meilleur choix.

WebRTC fournit un contrôle de congestion et un débit adaptatif pour les médias. À mesure que les conditions du réseau changent, les utilisateurs obtiendront toujours la
meilleure expérience possible. Les développeurs n'ont pas non plus à écrire de code supplémentaire pour mesurer ces conditions.

Les participants peuvent envoyer et recevoir plusieurs flux. Ils peuvent également ajouter et supprimer ces flux à tout moment pendant l'appel. Les codecs sont négociés
également. Toute cette fonctionnalité est fournie par le navigateur, aucun code personnalisé n'a besoin d'être écrit par le développeur.

La conférence bénéficie également des canaux de données. Les utilisateurs peuvent envoyer des métadonnées ou partager des documents. Vous pouvez créer plusieurs flux
et les configurer si vous avez besoin de performances plutôt que de fiabilité.

### Diffusion
De nombreux nouveaux projets commencent à apparaître dans l'espace de diffusion qui utilisent WebRTC. Le protocole a beaucoup à offrir à la fois pour l'éditeur
et le consommateur de médias.

WebRTC étant dans le navigateur facilite la publication de vidéo pour les utilisateurs. Il supprime l'exigence pour les utilisateurs de télécharger un nouveau client.
Toute plateforme qui a un navigateur web peut publier de la vidéo. Les éditeurs peuvent ensuite envoyer plusieurs pistes et les modifier ou les supprimer à tout moment. C'est
une énorme amélioration par rapport aux protocoles hérités qui n'autorisaient qu'une piste audio ou une piste vidéo par connexion.

WebRTC donne aux développeurs un plus grand contrôle sur les compromis latence versus qualité. S'il est plus important que la latence ne dépasse jamais un
certain seuil, et que vous êtes prêt à tolérer certains artefacts de décodage. Vous pouvez configurer le visualiseur pour lire les médias dès qu'ils
arrivent. Avec d'autres protocoles qui fonctionnent sur TCP, ce n'est pas aussi facile. Dans le navigateur, vous pouvez demander des données et c'est tout.

### Accès à distance
L'accès à distance, c'est lorsque vous accédez à distance à un autre ordinateur via WebRTC. Vous pourriez avoir un contrôle complet de l'hôte distant, ou peut-être juste une
seule application. C'est génial pour exécuter des tâches coûteuses en calcul lorsque le matériel local ne peut pas le faire. Comme exécuter un nouveau jeu vidéo, ou
un logiciel de CAO. WebRTC a pu révolutionner l'espace de trois manières.

WebRTC peut être utilisé pour accéder à distance à un hôte qui n'est pas routable mondialement. Avec la traversée NAT, vous pouvez accéder à un ordinateur qui n'est disponible
que via STUN. C'est génial pour la sécurité et la confidentialité. Vos utilisateurs n'ont pas à router la vidéo via une ingestion, ou une "jump box". La traversée NAT
facilite également les déploiements. Vous n'avez pas à vous soucier de la redirection de port ou de la configuration d'une IP statique à l'avance.

Les canaux de données sont également vraiment puissants dans ce scénario. Ils peuvent être configurés pour que seules les dernières données soient acceptées. Avec TCP, vous courez le
risque de rencontrer un blocage en tête de ligne. Un ancien clic de souris ou une frappe de touche pourrait arriver en retard et bloquer les suivants.
Les canaux de données de WebRTC sont conçus pour gérer cela et peuvent être configurés pour ne pas renvoyer les paquets perdus. Vous pouvez également mesurer la contre-pression et
vous assurer que vous n'envoyez pas plus de données que votre réseau ne peut en supporter.

WebRTC étant disponible dans le navigateur a été une énorme amélioration de la qualité de vie. Vous n'avez pas à télécharger un client propriétaire pour démarrer la
session. De plus en plus de clients arrivent avec WebRTC intégré, les téléviseurs intelligents obtiennent maintenant des navigateurs web complets.

### Partage de fichiers et contournement de la censure
Le partage de fichiers et le contournement de la censure sont des problèmes radicalement différents. Cependant, WebRTC résout les mêmes problèmes pour eux deux. Il les rend
tous deux facilement disponibles et plus difficiles à bloquer.

Le premier problème que WebRTC résout est l'obtention du client. Si vous voulez rejoindre un réseau de partage de fichiers, vous devez télécharger le client. Même si
le réseau est distribué, vous devez toujours obtenir le client d'abord. Dans un réseau restreint, le téléchargement sera souvent bloqué. Même si vous
pouvez le télécharger, l'utilisateur peut ne pas être en mesure d'installer et d'exécuter le client. WebRTC est déjà disponible dans chaque navigateur web, le rendant facilement disponible.

Le deuxième problème que WebRTC résout est le blocage de votre trafic. Si vous utilisez un protocole qui est juste pour le partage de fichiers ou le contournement de la censure,
il est beaucoup plus facile de le bloquer. Étant donné que WebRTC est un protocole à usage général, le bloquer impacterait tout le monde. Bloquer WebRTC pourrait empêcher d'autres
utilisateurs du réseau de rejoindre des appels de conférence.

### Internet des objets
L'Internet des objets (IoT) couvre quelques cas d'usage différents. Pour beaucoup, cela signifie des caméras de sécurité connectées au réseau. En utilisant WebRTC, vous pouvez diffuser la vidéo vers un autre pair WebRTC
comme votre téléphone ou un navigateur. Un autre cas d'usage consiste à avoir des appareils se connecter et échanger des données de capteurs. Vous pouvez avoir deux appareils dans votre LAN
échanger des lectures de climat, de bruit ou de lumière.

WebRTC a un énorme avantage en matière de confidentialité ici par rapport aux protocoles de flux vidéo hérités. Étant donné que WebRTC prend en charge la connectivité P2P, la caméra peut envoyer la vidéo
directement à votre navigateur. Il n'y a aucune raison pour que votre vidéo soit envoyée à un serveur tiers. Même lorsque la vidéo est chiffrée, un attaquant peut faire
des suppositions à partir des métadonnées de l'appel.

L'interopérabilité est un autre avantage pour l'espace IoT. WebRTC est disponible dans beaucoup de langages différents ; C#, C++, C, Go, Java, Python, Rust
et TypeScript. Cela signifie que vous pouvez utiliser le langage qui fonctionne le mieux pour vous. Vous n'avez pas non plus à vous tourner vers des protocoles ou des formats propriétaires
pour pouvoir connecter vos clients.

### Pontage de protocole média
Vous avez du matériel et des logiciels existants qui produisent de la vidéo, mais vous ne pouvez pas encore le mettre à niveau. Attendre des utilisateurs qu'ils téléchargent un
client propriétaire pour regarder des vidéos est frustrant. La réponse est d'exécuter un pont WebRTC. Le pont traduit entre les deux protocoles afin que les utilisateurs puissent utiliser le
navigateur avec votre configuration héritée.

Beaucoup des formats avec lesquels les développeurs font le pont utilisent les mêmes protocoles que WebRTC. SIP est couramment exposé via WebRTC et permet aux utilisateurs de passer des appels téléphoniques
depuis leur navigateur. RTSP est utilisé dans beaucoup de caméras de sécurité héritées. Ils utilisent tous deux les mêmes protocoles sous-jacents (RTP et SDP), donc c'est peu coûteux en calcul
à exécuter. Le pont est juste nécessaire pour ajouter ou supprimer des choses qui sont spécifiques à WebRTC.

### Pontage de protocole de données
Un navigateur web ne peut parler qu'un ensemble contraint de protocoles. Vous pouvez utiliser HTTP, WebSockets, WebRTC et QUIC. Si vous voulez vous connecter
à autre chose, vous devez utiliser un pont de protocole. Un pont de protocole est un serveur qui convertit le trafic étranger en quelque chose que le navigateur
peut accéder. Un exemple populaire est l'utilisation de SSH depuis votre navigateur pour accéder à un serveur. Les canaux de données de WebRTC ont deux avantages par rapport à la concurrence.

Les canaux de données de WebRTC permettent une livraison non fiable et non ordonnée. Dans les cas où la faible latence est critique, cela est nécessaire. Vous ne voulez pas que de nouvelles données soient
bloquées par d'anciennes données, c'est ce qu'on appelle le blocage en tête de ligne. Imaginez que vous jouez à un jeu de tir à la première personne multijoueur. Vous souciez-vous vraiment de l'endroit où le
joueur était il y a deux secondes ? Si ces données n'arrivent pas à temps, cela n'a pas de sens de continuer à essayer de les envoyer. La livraison non fiable et non ordonnée vous permet
d'utiliser les données dès qu'elles arrivent.

Les canaux de données fournissent également une pression de rétroaction. Cela vous indique si vous envoyez des données plus rapidement que votre connexion ne peut le supporter. Vous avez alors deux
choix lorsque cela se produit. Le canal de données peut soit être configuré pour mettre en mémoire tampon et livrer les données en retard, soit vous pouvez abandonner les données qui ne sont pas arrivées
en temps réel.

### Téléopération
La téléopération est l'acte de contrôler un appareil à distance via des canaux de données WebRTC, et d'envoyer la vidéo en retour via RTP. Les développeurs conduisent des voitures à distance
via WebRTC aujourd'hui ! Ceci est utilisé pour contrôler des robots sur des chantiers de construction et livrer des colis. Utiliser WebRTC pour ces problèmes a du sens pour deux raisons.

L'ubiquité de WebRTC facilite le contrôle pour les utilisateurs. Tout ce dont l'utilisateur a besoin est un navigateur web et un périphérique d'entrée. Les navigateurs prennent même
en charge la saisie depuis des joysticks et des manettes de jeu. WebRTC supprime complètement le besoin d'installer un client supplémentaire sur l'appareil de l'utilisateur.

### CDN distribué
Les CDN distribués sont un sous-ensemble du partage de fichiers. Les fichiers distribués sont configurés par l'opérateur CDN à la place. Lorsque les utilisateurs rejoignent le réseau CDN,
ils peuvent télécharger et partager les fichiers autorisés. Les utilisateurs obtiennent tous les mêmes avantages que le partage de fichiers.

Ces CDN fonctionnent très bien lorsque vous êtes dans un bureau avec une mauvaise connectivité externe, mais une excellente connectivité LAN. Vous pouvez avoir un utilisateur télécharger une vidéo, et
ensuite la partager avec tout le monde. Étant donné que tout le monde n'essaie pas de récupérer le même fichier via le réseau externe, le transfert se terminera plus rapidement.

## Topologies WebRTC
WebRTC est un protocole pour connecter deux agents, alors comment les développeurs connectent-ils des centaines de personnes à la fois ? Il existe quelques façons
différentes de le faire, et elles ont toutes des avantages et des inconvénients. Ces solutions se répartissent globalement en deux catégories ; Pair-à-pair ou Client/Serveur. La
flexibilité de WebRTC nous permet de créer les deux.

### Un à un
Un à un est le premier type de connexion que vous utiliserez avec WebRTC. Vous connectez deux agents WebRTC directement et ils peuvent envoyer des médias et des données bidirectionnels.
La connexion ressemble à ceci.

![Un à un](../images/08-one-to-one.png "Un à un")

### Maillage complet
Le maillage complet est la réponse si vous voulez construire une conférence téléphonique ou un jeu multijoueur. Dans cette topologie, chaque utilisateur établit une connexion
avec chaque autre utilisateur directement. Cela vous permet de construire votre application, mais cela vient avec quelques inconvénients.

Dans une topologie de maillage complet, chaque utilisateur est connecté directement. Cela signifie que vous devez encoder et télécharger la vidéo indépendamment pour chaque membre de l'appel.
Les conditions réseau entre chaque connexion seront différentes, vous ne pouvez donc pas réutiliser la même vidéo. La gestion des erreurs est également difficile dans ces
déploiements. Vous devez considérer attentivement si vous avez perdu une connectivité complète, ou juste une connectivité avec un pair distant.

En raison de ces préoccupations, un maillage complet est mieux utilisé pour de petits groupes. Pour quoi que ce soit de plus grand, une topologie client/serveur est préférable.

![Maillage complet](../images/08-full-mesh.png "Maillage complet")

### Maillage hybride
Le maillage hybride est une alternative au maillage complet qui peut alléger certains des problèmes du maillage complet. Dans un maillage hybride, les connexions ne sont pas établies
entre chaque utilisateur. Au lieu de cela, les médias sont relayés via des pairs dans le réseau. Cela signifie que le créateur des médias n'a pas à utiliser autant
de bande passante pour distribuer les médias.

Cela a cependant quelques inconvénients. Dans cette configuration, le créateur original des médias n'a aucune idée à qui sa vidéo est envoyée, ni si
elle est arrivée avec succès. Vous aurez également une augmentation de la latence à chaque saut dans votre réseau de maillage hybride.

![Maillage hybride](../images/08-hybrid-mesh.png "Maillage hybride")

### Unité de transfert sélectif
Un SFU (Selective Forwarding Unit) résout également les problèmes du maillage complet, mais d'une manière entièrement différente. Un SFU implémente une topologie client/serveur, au lieu de P2P.
Chaque pair WebRTC se connecte au SFU et télécharge ses médias. Le SFU transfère ensuite ces médias à chaque client connecté.

Avec un SFU, chaque agent WebRTC ne doit encoder et télécharger sa vidéo qu'une seule fois. Le fardeau de la distribuer à tous les spectateurs incombe au SFU.
La connectivité avec un SFU est également beaucoup plus facile que P2P. Vous pouvez exécuter un SFU sur une adresse routable mondiale, ce qui facilite la connexion des clients.
Vous n'avez pas à vous soucier des mappages NAT. Vous devez toujours vous assurer que votre SFU est disponible via TCP (soit via ICE-TCP soit TURN).

Construire un SFU simple peut être fait en un week-end. Construire un bon SFU qui peut gérer tous les types de clients n'a jamais de fin. Régler le contrôle de congestion, la correction d'erreur
et les performances est une tâche sans fin.

![Unité de transfert sélectif](../images/08-sfu.png "Unité de transfert sélectif")

### MCU
Un MCU (Multi-point Conferencing Unit) est une topologie client/serveur comme un SFU, mais compose les flux de sortie. Au lieu de distribuer les médias sortants
non modifiés, il les réencode en un seul flux.

![Unité de conférence multipoint](../images/08-mcu.png "Unité de conférence multipoint")
