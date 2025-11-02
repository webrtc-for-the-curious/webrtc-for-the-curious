---
title: Sécurisation
type: docs
weight: 5
---

# Sécurisation

## Quelle sécurité offre WebRTC ?

Chaque connexion WebRTC est authentifiée et chiffrée. Vous pouvez être sûr qu'un tiers ne peut pas voir ce que vous envoyez ou insérer de faux messages. Vous pouvez également être sûr que l'agent WebRTC qui a généré la description de session est celui avec lequel vous communiquez.

Il est très important que personne ne modifie ces messages. Il est acceptable qu'un tiers lise la description de session en transit. Cependant, WebRTC n'a aucune protection contre sa modification. Un attaquant pourrait effectuer une attaque de l'homme du milieu sur vous en changeant les candidats ICE et en mettant à jour l'empreinte du certificat.

## Comment cela fonctionne-t-il ?
WebRTC utilise deux protocoles préexistants, Datagram Transport Layer Security ([DTLS](https://tools.ietf.org/html/rfc6347)) et le Secure Real-time Transport Protocol ([SRTP](https://tools.ietf.org/html/rfc3711)).

DTLS vous permet de négocier une session puis d'échanger des données en toute sécurité entre deux pairs. C'est un frère de TLS, la même technologie qui alimente HTTPS, mais DTLS utilise UDP au lieu de TCP comme couche de transport. Cela signifie que le protocole doit gérer la livraison non fiable. SRTP est spécifiquement conçu pour échanger des médias de manière sécurisée. Il y a quelques optimisations que nous pouvons faire en l'utilisant au lieu de DTLS.

DTLS est utilisé en premier. Il effectue une négociation sur la connexion fournie par ICE. DTLS est un protocole client/serveur, donc un côté doit démarrer la négociation. Les rôles Client/Serveur sont choisis lors de la signalisation. Pendant la négociation DTLS, les deux côtés offrent un certificat.
Une fois la négociation terminée, ce certificat est comparé au hachage du certificat dans la description de session. Ceci est pour s'assurer que la négociation s'est produite avec l'agent WebRTC attendu. La connexion DTLS est ensuite disponible pour être utilisée pour la communication DataChannel.

Pour créer une session SRTP, nous l'initialisons en utilisant les clés générées par DTLS. SRTP n'a pas de mécanisme de négociation, donc il doit être amorcé avec des clés externes. Une fois cela fait, les médias peuvent être échangés en étant chiffrés en utilisant SRTP !

## Sécurité 101
Pour comprendre la technologie présentée dans ce chapitre, vous devrez d'abord comprendre ces termes. La cryptographie est un sujet délicat, il vaudrait donc la peine de consulter d'autres sources également !

### Texte en clair et texte chiffré

Le texte en clair est l'entrée d'un chiffrement. Le texte chiffré est la sortie d'un chiffrement.

### Chiffrement

Le chiffrement est une série d'étapes qui prend du texte en clair pour le transformer en texte chiffré. Le chiffrement peut ensuite être inversé, de sorte que vous puissiez ramener votre texte chiffré en texte en clair. Un chiffrement a généralement une clé pour changer son comportement. Un autre terme pour cela est le chiffrement et le déchiffrement.

Un chiffrement simple est ROT13. Chaque lettre est déplacée de 13 caractères en avant. Pour annuler le chiffrement, vous déplacez 13 caractères en arrière. Le texte en clair `HELLO` deviendrait le texte chiffré `URYYB`. Dans ce cas, le chiffrement est ROT, et la clé est 13.

### Fonctions de hachage

Une fonction de hachage cryptographique est un processus à sens unique qui génère un condensé. Étant donné une entrée, elle génère la même sortie à chaque fois. Il est important que la sortie ne soit *pas* réversible. Si vous avez une sortie, vous ne devriez pas être capable de déterminer son entrée. Le hachage est utile lorsque vous voulez confirmer qu'un message n'a pas été altéré.

Une fonction de hachage simple (bien que certainement pas adaptée à la cryptographie réelle) serait de ne prendre qu'une lettre sur deux. `HELLO` deviendrait `HLO`. Vous ne pouvez pas supposer que `HELLO` était l'entrée, mais vous pouvez confirmer que `HELLO` correspondrait au condensé de hachage.

### Cryptographie à clé publique/privée

La cryptographie à clé publique/privée décrit le type de chiffrements que DTLS et SRTP utilisent. Dans ce système, vous avez deux clés, une clé publique et une clé privée. La clé publique est pour chiffrer les messages et peut être partagée en toute sécurité.
La clé privée est pour déchiffrer, et ne doit jamais être partagée. C'est la seule clé qui peut déchiffrer les messages chiffrés avec la clé publique.

### Échange Diffie–Hellman

L'échange Diffie–Hellman permet à deux utilisateurs qui ne se sont jamais rencontrés auparavant de créer un secret partagé en toute sécurité sur Internet. L'utilisateur `A` peut envoyer un secret à l'utilisateur `B` sans se soucier de l'écoute clandestine. Cela dépend de la difficulté de casser le problème du logarithme discret.
Vous n'avez pas besoin de comprendre pleinement comment cela fonctionne, mais il est utile de savoir que c'est ce qui rend possible la négociation DTLS.

Wikipédia a un exemple de ceci en action [ici](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation).

### Fonction pseudo-aléatoire

Une fonction pseudo-aléatoire (PRF) est une fonction prédéfinie pour générer une valeur qui semble aléatoire. Elle peut prendre plusieurs entrées et générer une seule sortie.

### Fonction de dérivation de clé

La dérivation de clé est un type de fonction pseudo-aléatoire. La dérivation de clé est une fonction utilisée pour rendre une clé plus forte. Un modèle courant est l'étirement de clé.

Disons que vous recevez une clé de 8 octets. Vous pourriez utiliser une KDF pour la rendre plus forte.

### Nonce

Un nonce est une entrée supplémentaire à un chiffrement. Ceci est utilisé pour que vous puissiez obtenir une sortie différente du chiffrement, même si vous chiffrez le même message plusieurs fois.

Si vous chiffrez le même message 10 fois, le chiffrement vous donnera le même texte chiffré 10 fois. En utilisant un nonce, vous pouvez obtenir une sortie différente, tout en utilisant la même clé. Il est important d'utiliser un nonce différent pour chaque message ! Sinon, cela annule une grande partie de la valeur.

### Code d'authentification de message

Un code d'authentification de message est un hachage qui est placé à la fin d'un message. Un MAC prouve que le message provient de l'utilisateur attendu.

Si vous n'utilisez pas de MAC, un attaquant pourrait insérer des messages invalides. Après déchiffrement, vous n'auriez que des ordures car ils ne connaissent pas la clé.

### Rotation de clé

La rotation de clé est la pratique de changer votre clé à intervalles réguliers. Cela rend une clé volée moins impactante. Si une clé est volée ou divulguée, moins de données peuvent être déchiffrées.

## DTLS
DTLS (Datagram Transport Layer Security) permet à deux pairs d'établir une communication sécurisée sans aucune configuration préexistante. Même si quelqu'un écoute la conversation, il ne pourra pas déchiffrer les messages.

Pour qu'un client DTLS et un serveur communiquent, ils doivent se mettre d'accord sur un chiffrement et la clé. Ils déterminent ces valeurs en effectuant une négociation DTLS. Pendant la négociation, les messages sont en texte clair.
Lorsqu'un client/serveur DTLS a échangé suffisamment de détails pour commencer à chiffrer, il envoie un `Change Cipher Spec`. Après ce message, chaque message suivant sera chiffré !

### Format de paquet
Chaque paquet DTLS commence par un en-tête.

#### Type de contenu
Vous pouvez vous attendre aux types suivants :

* `20` - Change Cipher Spec
* `22` - Handshake
* `23` - Application Data

`Handshake` est utilisé pour échanger les détails pour démarrer la session. `Change Cipher Spec` est utilisé pour notifier l'autre côté que tout sera chiffré. `Application Data` sont les messages chiffrés.

#### Version
La version peut être soit `0x0000feff` (DTLS v1.0) soit `0x0000fefd` (DTLS v1.2), il n'y a pas de v1.1.

#### Époque
L'époque commence à `0`, mais devient `1` après un `Change Cipher Spec`. Tout message avec une époque non nulle est chiffré.

#### Numéro de séquence
Le numéro de séquence est utilisé pour garder les messages dans l'ordre. Chaque message augmente le numéro de séquence. Lorsque l'époque est incrémentée, le numéro de séquence recommence.

#### Longueur et charge utile
La charge utile est spécifique au `Type de contenu`. Pour un `Application Data`, la `Charge utile` est les données chiffrées. Pour `Handshake`, ce sera différent selon le message. La longueur indique la taille de la `Charge utile`.

### Machine à états de négociation
Pendant la négociation, le client/serveur échange une série de messages. Ces messages sont regroupés en vols. Chaque vol peut avoir plusieurs messages (ou juste un).
Un vol n'est pas complet tant que tous les messages du vol n'ont pas été reçus. Nous décrirons le but de chaque message plus en détail ci-dessous.

![Négociation](../images/04-handshake.png "Négociation")

#### ClientHello
ClientHello est le message initial envoyé par le client. Il contient une liste d'attributs. Ces attributs indiquent au serveur les chiffrements et fonctionnalités que le client prend en charge. Pour WebRTC, c'est ainsi que nous choisissons également le chiffrement SRTP. Il contient également des données aléatoires qui seront utilisées pour générer les clés de la session.

#### HelloVerifyRequest
HelloVerifyRequest est envoyé par le serveur au client. C'est pour s'assurer que le client avait l'intention d'envoyer la requête. Le client renvoie ensuite le ClientHello, mais avec un jeton fourni dans le HelloVerifyRequest.

#### ServerHello
ServerHello est la réponse du serveur pour la configuration de cette session. Il contient quel chiffrement sera utilisé lorsque cette session sera terminée. Il contient également les données aléatoires du serveur.

#### Certificate
Certificate contient le certificat pour le client ou le serveur. Ceci est utilisé pour identifier de manière unique avec qui nous communiquions. Après la fin de la négociation, nous nous assurerons que ce certificat, lorsqu'il est haché, correspond à l'empreinte dans la `SessionDescription`.

#### ServerKeyExchange/ClientKeyExchange
Ces messages sont utilisés pour transmettre la clé publique. Au démarrage, le client et le serveur génèrent tous deux une paire de clés. Après la négociation, ces valeurs seront utilisées pour générer le `Pre-Master Secret`.

#### CertificateRequest
Un CertificateRequest est envoyé par le serveur notifiant le client qu'il veut un certificat. Le serveur peut soit demander soit exiger un certificat.

#### ServerHelloDone
ServerHelloDone notifie le client que le serveur a terminé avec la négociation.

#### CertificateVerify
CertificateVerify est la façon dont l'expéditeur prouve qu'il a la clé privée envoyée dans le message Certificate.

#### ChangeCipherSpec
ChangeCipherSpec informe le récepteur que tout ce qui est envoyé après ce message sera chiffré.

#### Finished
Finished est chiffré et contient un hachage de tous les messages. Ceci est pour affirmer que la négociation n'a pas été altérée.

### Génération de clé
Après la fin de la négociation, vous pouvez commencer à envoyer des données chiffrées. Le chiffrement a été choisi par le serveur et se trouve dans le ServerHello. Comment la clé a-t-elle été choisie cependant ?

D'abord, nous générons le `Pre-Master Secret`. Pour obtenir cette valeur, Diffie–Hellman est utilisé sur les clés échangées par le `ServerKeyExchange` et le `ClientKeyExchange`. Les détails diffèrent selon le chiffrement choisi.

Ensuite, le `Master Secret` est généré. Chaque version de DTLS a une `fonction pseudo-aléatoire` définie. Pour DTLS 1.2, la fonction prend le `Pre-Master Secret` et les valeurs aléatoires dans le `ClientHello` et le `ServerHello`.
La sortie de l'exécution de la `fonction pseudo-aléatoire` est le `Master Secret`. Le `Master Secret` est la valeur qui est utilisée pour le chiffrement.

### Échange d'ApplicationData
Le cheval de bataille de DTLS est `ApplicationData`. Maintenant que nous avons un chiffrement initialisé, nous pouvons commencer à chiffrer et à envoyer des valeurs.

Les messages `ApplicationData` utilisent un en-tête DTLS comme décrit précédemment. La `Charge utile` est remplie avec du texte chiffré. Vous avez maintenant une session DTLS fonctionnelle et pouvez communiquer en toute sécurité.

DTLS a beaucoup plus de fonctionnalités intéressantes comme la renégociation. Elles ne sont pas utilisées par WebRTC, donc elles ne seront pas couvertes ici.

## SRTP
SRTP est un protocole conçu spécifiquement pour chiffrer les paquets RTP. Pour démarrer une session SRTP, vous spécifiez vos clés et votre chiffrement. Contrairement à DTLS, il n'a pas de mécanisme de négociation. Toute la configuration et les clés ont été générées pendant la négociation DTLS.

DTLS fournit une API dédiée pour exporter les clés à utiliser par un autre processus. Ceci est défini dans la [RFC 5705](https://tools.ietf.org/html/rfc5705).

### Création de session
SRTP définit une fonction de dérivation de clé qui est utilisée sur les entrées. Lors de la création d'une session SRTP, les entrées sont passées à travers cela pour générer nos clés pour notre chiffrement SRTP. Après cela, vous pouvez passer au traitement des médias.

### Échange de médias
Chaque paquet RTP a un numéro de séquence de 16 bits. Ces numéros de séquence sont utilisés pour garder les paquets dans l'ordre, comme une clé primaire. Pendant un appel, ceux-ci déborderont. SRTP garde une trace de cela et l'appelle le compteur de débordement.

Lors du chiffrement d'un paquet, SRTP utilise le compteur de débordement et le numéro de séquence comme nonce. Ceci est pour garantir que même si vous envoyez les mêmes données deux fois, le texte chiffré sera différent. Ceci est important pour empêcher un attaquant d'identifier des modèles ou de tenter une attaque par rejeu.
