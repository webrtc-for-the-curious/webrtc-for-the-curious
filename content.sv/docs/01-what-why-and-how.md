---
title: Vad, varför och hur
type: docs
weight: 2
---

# Vad är WebRTC?
WebRTC, förkortning för Web Real-Time Communication, är både ett API och ett protokoll. WebRTC-protokollet är en uppsättning regler som två WebRTC-agenter använder för att sätta upp en säker tvåvägs realtidskommunikation. WebRTC API:et tillåter sedan utvecklare att använda WebRTC-protokollet. WebRTC API:et är endast specificerat för JavaScript.

Ett liknande förhållande skulle vara det mellan HTTP och Fetch API:et. WebRTC protokollet skulle vara HTTP, och WebRTC API:et motsvarar Fetch API:et.

WebRTC-protokollet finns tillgängligt i andra API:er och språk än JavaScript. Du kan också hitta servrar och domänspecifika verktyg för WebRTC. Alla dessa implementationer använder WebRTC-protokollet så att de kan kommunicera med varandra.

WebRTC-protokollet upprätthålls i IETF i arbetsgruppen [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/). WebRTC API:et är dokumenterat i W3C som [webrtc-pc](https://w3c.github.io/webrtc-pc/).

## Varför ska jag lära mig WebRTC?

Det här är en lista på några saker som WebRTC kommer att ge dig. Listan är inte komplett, bara exempel på saker. Oroa dig inte om du inte känner till alla dessa termer ännu, den här boken kommer att lära dig dem på vägen.

* Öppen standard
* Flera implementeringar
* Fungerar direkt i webbläsare
* Obligatorisk kryptering
* NAT Traversal
* Byggt på beprövad, befintlig, teknik
* Trängselkontroll
* Latens som kan mätas i bråkdelar av en sekund

## WebRTC Protokollet är en samling av andra tekniker

Detta är ett ämne som kan ta en hel bok att förklara, men till att börja med delar vi upp det i fyra steg.

* Signalering
* Anslutning
* Säkerhet
* Kommunikation

Dessa fyra steg sker alltid i den här ordningen. Varje steg måste vara helt klart utan problem för att det efterföljande steget ska kunna börja.

En intressant sak med WebRTC är att varje steg faktiskt består av många andra protokoll och befintliga tekniker. I den meningen är WebRTC egentligen bara en kombination av beprövad teknik som har funnits sedan början av 2000-talet.

Vi kommer att gå igenom alla dessa steg i detalj senare, men det är bra att först förstå dem på en hög nivå. Eftersom de är beroende av varandra kommer det att hjälpa dig när vi senare förklarar syftet med vart och ett av dessa steg.

### Signalering: Hur parter hittar varandra i WebRTC

När en WebRTC-agent startar har den ingen aning om vem den ska kommunicera med och vad de ska kommunicera om. Signalering löser problemet! Signalering används för att starta samtalet så att två WebRTC-agenter kan börja kommunicera.

Signalering använder ett befintligt protokoll SDP (Session Description Protocol). SDP är ett enkelt textbaserat protokoll. Varje SDP-meddelande består av nyckel/värdepar och innehåller en lista med "media sections". SDP:n som de två WebRTC agenterna utbyter innehåller detaljer som:

* IP-adresser och portar som agenten kan nås på (kandidater).
* Hur många ljud- och videospår agenten vill skicka.
* Vilka ljud- och video-kodek som varje agent stöder.
* Värden som används vid anslutning (`uFrag`/`uPwd`).
* Värden som används vid säkringen (certifikatfingeravtryck).

Observera att signalering vanligtvis sker i en separat kanal (out-of-band); applikationer använder i allmänhet inte WebRTC för att skicka signalmeddelanden. Vilken arkitektur som helst som är lämplig för att skicka meddelanden kan användas för att vidarebefordra SDP:erna mellan de anslutande parterna. Många applikationer använder sin befintliga infrastruktur (som REST-API:er, WebSocket-anslutningar eller autentiserande proxys) för att på enklaste sätt utbyta SDP:er mellan rätt klienter.

### Anslutning och NAT Traversal med STUN/TURN

De två WebRTC-agenterna vet nu tillräckligt med detaljer för att försöka ansluta till varandra. WebRTC använder sedan en annan etablerad teknik som kallas ICE.

ICE (Interactive Connectivity Establishment) är ett protokoll som skapades före WebRTC. ICE används för att upprätt av en anslutning mellan två agenter. Dessa agenter kan vara i samma nätverk eller på andra sidan världen. ICE är används för att skapa en direktanslutning utan att gå via en central server.

Den verkliga magin här är "NAT Traversal" och STUN/TURN-servrar. Dessa två begrepp är allt du behöver för att kommunicera med en ICE-agent i ett annat sub-nät. Vi kommer att utforska dessa ämnen djupare senare.

När ICE väl har anslutits går WebRTC vidare till att upprätta en krypterad transport. Denna kommunikationskanal används för ljud, video och data.

### Säkra transportskiktet med DTLS och SRTP

Nu när vi har dubbelriktad kommunikation (via ICE) måste vi sätta upp en säker kommunikationskanal. Detta görs genom två protokoll som också är äldre än WebRTC. Det första protokollet är DTLS (Datagram Transport Layer Security) som helt enkelt är TLS över UDP. TLS är det kryptografiska protokollet som används för att säkra kommunikation via HTTPS. Det andra protokollet är SRTP (Secure Real-time Transport Protocol).

Först ansluter WebRTC genom att göra en DTLS-handskakning över anslutningen som upprättats av ICE. Till skillnad från HTTPS använder WebRTC inte en vanlig CA (Certificate Authority) för certifikatet. Istället hävdar WebRTC bara att certifikatet som utbyts via DTLS matchar. Denna DTLS-anslutning används sedan för DataChannel-meddelanden.

WebRTC använder sedan ett annat protokoll för ljud- och video-överföring som heter RTP. Vi skyddar våra RTP-paket med SRTP. Vi initierar vår SRTP-session genom att extrahera nycklarna från den förhandlade DTLS-sessionen. Vi kommer att gå igenom varför medieöverföring har ett eget protokoll i ett senare kapitel.

Nu är vi klara! Du har nu dubbelriktad och säker kommunikation. Om du har en stabil anslutning mellan dina WebRTC-agenter är det här all komplexitet du behöver. Tyvärr har den verkliga världen andra problem som paketförlust och brist på bandbredd. Nästa avsnitt handlar om hur vi hanterar dem.

### Kommunicera med parter via RTP och SCTP

Vi har nu två WebRTC-agenter med säker dubbelriktad kommunikation. Låt oss börja kommunicera! Återigen använder vi två befintliga protokoll: RTP (Real-time Transport Protocol) och SCTP (Stream Control Transmission Protocol). Använd RTP för att utbyta media krypterat med SRTP och använd SCTP för att skicka och ta emot DataChannel-meddelanden krypterade med DTLS.

RTP är ganska minimalt, men ger oss allt vi behöver för att implementera realtidsströmning. Det viktiga är att RTP ger utvecklaren flexibilitet, så att de kan hantera latens, förlust och trängsel som de vill. Vi kommer att gå igenom detta ytterligare i mediekapitlet.

Det slutliga protokollet i stacken är SCTP. SCTP tillåter många leveransalternativ för meddelanden. Du kan till exempel välja att ha opålitlig leverans utan ordning, så att du kan få den latens som behövs för realtidssystem.

## WebRTC, en samling protokoll
WebRTC löser väldigt många problem åt oss. Först kan detta verka väldigt ambitiöst, men det smarta med WebRTCs är att man inte försökte lösa allt själva. Istället återanvände man många befintliga tekniker för enskilda ändamål och kombinerade dem.

Detta gör att vi kan undersöka och lära oss om varje del individuellt, utan att bli överväldigade. Ett bra sätt att visualisera det hela är att en "WebRTC Agent" egentligen bara är en samordnare av många olika protokoll.

![WebRTC Agent](../../images/01-webrtc-agent.png "WebRTC Agent")

## Hur fungerar API:et WebRTC

Det här avsnittet visar hur JavaScript API:et kopplas till protokollet. Detta är inte tänkt som ett omfattande demo av WebRTC API:et, utan mer för att skapa en mental modell för hur det hela hänger ihop.
Om du inte känner till någon av dem är det ok. Det här kan vara ett roligt avsnitt att återvända till när du lär dig mer!

#### `new RTCPeerConnection`
`RTCPeerConnection` är den högsta nivån av en "WebRTC Session". Den innehåller alla ovan nämnda protokoll. Delsystemen är alla allokerade men ingenting händer ännu.

#### `addTrack`

`addTrack` skapar en ny RTP-ström. En slumpmässig synkroniseringskälla (SSRC) kommer att genereras för denna ström. Den här strömmen kommer sedan att finnas i Sessionsbeskrivningen som genereras av `createOffer` inuti en media-sektion. Varje samtal till `addTrack` skapar en ny SSRC och media-sektion.

Omedelbart efter att en SRTP-session har upprättats kommer dessa mediepaket att skickas via ICE efter att ha krypterats med SRTP.

#### `createDataChannel`

`createDataChannel` skapar en ny SCTP-ström om det inte finns någon SCTP-koppling. Som standard är SCTP inte aktiverat men startas bara när en sida begär en datakanal.

Omedelbart efter att en DTLS-session har upprättats kommer SCTP-föreningen att skicka paket via ICE och krypteras med DTLS.

#### `createOffer`

`createOffer` genererar en sessionsbeskrivning (Session Description) av det lokala tillståndet som ska delas med den andra parten.

Handlingen att anropa `createOffer` förändrar ingenting för den lokala parten.

#### `setLocalDescription`

`setLocalDescription` gör alla begärda ändringar. `addTrack`, `createDataChannel` och liknande anrop är alla tillfälliga tills detta anrop görs. `setLocalDescription` anropas med det värde som genereras av `createOffer`.

Vanligtvis, efter det här anropet, kommer du att skicka erbjudandet till den andra parten, och de kommer att kalla `setRemoteDescription` med den.

#### `setRemoteDescription`

`setRemoteDescription` är hur vi informerar den lokala agenten om andra kandidaters tillstånd. Så här görs signalering med JavaScript API:et.

När `setRemoteDescription` har anropats på båda sidor har WebRTC Agenterna nu tillräckligt med information för att börja kommunicera direkt part-till-part (P2P)!

#### `addIceCandidate`

`addIceCandidate` tillåter en WebRTC-agent att lägga till fler ICE-kandidater på avstånd när de vill. Detta API skickar ICE-kandidaten direkt in i ICE-delsystemet och har ingen annan effekt på den större WebRTC-anslutningen.

#### `ontrack`

`ontrack` är ett återanrop som avfyras när ett RTP-paket tas emot från den andra parten. De inkommande paketen skulle ha deklarerats i Sessionsbeskrivningen som skickades till `setRemoteDescription`.

WebRTC använder SSRC för att hitta rätt `MediaStream` och `MediaStreamTrack`, och avfyrar återanropet med dessa detaljer fyllda.

#### `oniceconnectionstatechange`

`oniceconnectionstatechange` är en återanrop som avfyras för att visa tillståndet hos ICE-agenten. När du har fått en nätverksanslutning eller när du kopplas bort så får du det här meddelandet.

#### `onconnectionstatechange`

`onconnectionstatechange` är en kombination av ICE Agenten och DTLS Agentens tillstånd. Du kan lyssna på detta meddelande för att få veta när uppsättningen av både ICE och DTLS har slutförts.
