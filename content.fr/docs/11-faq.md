---
title: FAQ
type: docs
weight: 12
---

# FAQ

{{<details "Pourquoi WebRTC utilise-t-il UDP ?">}}
La traversée NAT nécessite UDP. Sans traversée NAT, l'établissement d'une connexion P2P
ne serait pas possible. UDP ne fournit pas de "livraison garantie" comme TCP, donc WebRTC la fournit au
niveau utilisateur.

Voir [Connexion]({{< ref "03-connecting" >}}) pour plus d'informations.
{{</details>}}

{{<details "Combien de DataChannels puis-je avoir ?">}}
65534 canaux car l'identifiant de flux a 16 bits. Vous pouvez fermer et ouvrir un nouveau à tout moment.
{{</details>}}

{{<details "WebRTC impose-t-il des limites de bande passante ?">}}
Les DataChannels et RTP utilisent tous deux le contrôle de congestion. Cela signifie que WebRTC mesure activement
votre bande passante et tente d'utiliser la quantité optimale. C'est un équilibre entre envoyer autant
que possible, sans surcharger la connexion.
{{</details>}}

{{<details "Puis-je envoyer des données binaires ?">}}
Oui, vous pouvez envoyer à la fois des données texte et binaires via les DataChannels.
{{</details>}}

{{<details "Quelle latence puis-je attendre avec WebRTC ?">}}
Pour les médias non ajustés, vous pouvez vous attendre à moins de 500 millisecondes. Si vous êtes prêt à ajuster ou à sacrifier la qualité
pour la latence, les développeurs ont obtenu une latence inférieure à 100 ms.

Les DataChannels prennent en charge l'option "Partial-reliability" qui peut réduire la latence causée par
les retransmissions de données sur une connexion avec perte. S'il est configuré correctement, il a été démontré qu'il bat les connexions TCP TLS.
{{</details>}}

{{<details "Pourquoi voudrais-je une livraison non ordonnée pour les DataChannels ?">}}
Lorsque de nouvelles informations rendent les anciennes obsolètes, comme les informations de position d'un
objet, ou lorsque chaque message est indépendant des autres et doit éviter
le délai de blocage en tête de ligne.
{{</details>}}

{{<details "Puis-je envoyer de l'audio ou de la vidéo sur un DataChannel ?">}}
Oui, vous pouvez envoyer n'importe quelle donnée sur un DataChannel. Dans le cas du navigateur, il sera de votre
responsabilité de décoder les données et de les transmettre à un lecteur multimédia pour le rendu,
alors que tout cela est fait automatiquement si vous utilisez des canaux médias.
{{</details>}}
