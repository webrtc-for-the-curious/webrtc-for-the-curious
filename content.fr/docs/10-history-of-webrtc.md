---
title: Histoire
type: docs
weight: 11
---

# Histoire
En apprenant WebRTC, les développeurs se sentent souvent frustrés par la complexité. Ils voient
des fonctionnalités de WebRTC non pertinentes pour leur projet actuel et souhaitent que WebRTC soit
plus simple. Le problème
est que tout le monde a un ensemble différent de cas d'usage. La communication en temps réel a une
histoire riche avec de nombreuses personnes différentes construisant de nombreuses choses différentes.

Ce chapitre contient des entretiens avec les auteurs des protocoles qui composent
WebRTC.
Il donne un aperçu des conceptions réalisées lors de la construction de chaque protocole, et
se termine par un
entretien sur WebRTC lui-même. Si vous comprenez les intentions et les conceptions du logiciel,
vous pouvez construire des systèmes plus efficaces avec lui.

## RTP
RTP et RTCP sont les protocoles qui gèrent tout le transport des médias pour WebRTC. Il a été
défini dans la [RFC 1889](https://tools.ietf.org/html/rfc1889) en janvier 1996.
Nous avons beaucoup de chance que l'un des auteurs [Ron
Frederick](https://github.com/ronf) parle de lui-même. Ron a récemment téléchargé
[Network Video tool](https://github.com/ronf/nv) sur GitHub, un projet qui
a informé RTP.

### Dans ses propres mots

En octobre 1992, j'ai commencé à expérimenter avec la carte de capture d'images Sun VideoPix
avec l'idée d'écrire un outil de vidéoconférence réseau basé sur le multicast IP.
Il était modélisé d'après "vat", un outil d'audioconférence développé
au LBL, en ce sens qu'il utilisait un protocole de session léger similaire pour que les utilisateurs
rejoignent des conférences, où vous envoyiez simplement des données à un
groupe multicast particulier et observiez ce groupe pour tout trafic d'autres membres
du groupe.

Pour que le programme soit vraiment réussi, j'avais besoin de compresser les
données vidéo avant de les mettre sur le réseau. Mon objectif était de faire un
flux de données d'apparence acceptable qui tiendrait dans environ 128 kbps, ou la
bande passante disponible sur une ligne ISDN domestique standard.

Début novembre 1992, j'ai lancé l'outil de vidéoconférence "nv" (sous
forme binaire) à la communauté Internet. Après quelques tests initiaux, il a été utilisé
pour diffuser en vidéo des parties du Groupe de travail d'ingénierie Internet de novembre dans le monde
entier.

Le protocole réseau utilisé pour "nv" et d'autres outils de conférence Internet
est devenu la base du Real-time Transport Protocol (RTP), normalisé
par l'Internet Engineering Task Force (IETF).

## WebRTC
WebRTC a nécessité un effort de normalisation qui éclipse tous les autres efforts
décrits dans ce chapitre. Il a nécessité une coopération entre deux
organismes de normalisation différents (IETF et W3C) et des centaines d'individus à travers de nombreuses
entreprises et pays. Pour nous donner un aperçu des motivations et
de l'effort monumental qu'il a fallu pour faire en sorte que WebRTC se produise, nous avons
[Serge Lachapelle](https://twitter.com/slac).

Serge est un chef de produit chez Google, servant actuellement de chef de produit
pour Google Workspace. Voici mon résumé de l'entretien.

### Qu'est-ce qui vous a amené à travailler sur WebRTC ?
J'ai été passionné par la construction de logiciels de communication depuis que j'étais à
l'université. Dans les années 90, des technologies comme [nv](https://github.com/ronf/nv)
ont commencé à apparaître, mais elles étaient difficiles à utiliser. J'ai créé un projet qui vous permettait de
rejoindre un appel vidéo directement depuis votre navigateur.

J'ai apporté cette expérience à Marratech, une entreprise que j'ai cofondée. Nous avons créé
des logiciels pour la vidéoconférence de groupe. Marratech a été acquis par Google en 2007.
Je passerais ensuite à travailler sur le projet qui informerait WebRTC.

### Le premier projet de Google
Le premier projet sur lequel la future équipe WebRTC a travaillé était la voix et le
chat vidéo de Gmail. Obtenir de l'audio et de la vidéo dans le navigateur n'était pas une tâche facile.

### La naissance de WebRTC
Pour moi, WebRTC est né avec quelques motivations. Combinées, elles ont donné naissance à
l'effort.

Il ne devrait pas être si difficile de construire des expériences RTC. Tant d'efforts sont gaspillés
à réimplémenter la même chose par différents développeurs.

La communication humaine devrait être sans entraves et devrait être ouverte. Comment est-il acceptable que
le texte et le HTML soient ouverts, mais que ma voix et mon image en temps réel ne le soient pas ?

La sécurité est une priorité. C'était aussi
une opportunité de créer un protocole qui serait sécurisé par défaut.

### L'avenir
WebRTC est dans une excellente position aujourd'hui. Il y a beaucoup de changements itératifs
en cours, mais rien de particulier sur lequel j'ai travaillé.

Je suis plus enthousiaste à propos de ce que le cloud computing peut faire pour la communication. En utilisant
des algorithmes avancés, nous pouvons éliminer le bruit de fond d'un appel et rendre
la communication possible là où elle ne l'était pas auparavant.
