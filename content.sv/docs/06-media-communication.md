---
title: Mediakommunikation
type: docs
weight: 7
---

# Vad får jag från WebRTCs mediakommunikation?
WebRTC låter dig skicka och ta emot ett obegränsat antal ljud- och videoströmmar. Du kan lägga till och plocka bort strömmar när som helst under ett samtal. Dessa strömmar kan alla vara oberoende, eller de kan buntas ihop! Du kan skicka ett videoflöde som visar din presentation och samtidigt inkludera ljud och video från din webbkamera.

WebRTC-protokollet är kodek-agnostiskt. Den underliggande transporten stöder allt, även kodeks som inte finns ännu! Det är dock fullt möjligt att WebRTC-agenten som du kommunicerar med inte har det nödvändiga stödet för att kunna acceptera den.

WebRTC är också utformat för att hantera dynamiska nätverksförhållanden. Under ett samtal kan din bandbredd öka eller minska. Kanske upplever du plötsligt mycket paketförlust. Protokollet är utformat för att hantera allt detta. WebRTC svarar på nätverksförhållanden och försöker ge dig bästa möjliga upplevelse utifrån de tillgängliga resurserna.

## Hur fungerar det?
WebRTC använder två befintliga protokoll RTP och RTCP, båda definierade i [RFC 1889](https://tools.ietf.org/html/rfc1889).

RTP (Real-time Transport Protocol) är protokollet som media skickas över. Det var utformat för att möjliggöra leverans av video i realtid. Det innehåller inga regler kring latens eller tillförlitlighet, men ger dig verktygen för att implementera dem. RTP ger dig strömmar så att du kan köra flera medieflöden över en anslutning. Det ger dig också tidpunkten och beställningsinformationen du behöver för att mata en mediapipeline.

RTCP (RTP Control Protocol) är det protokoll som skickar metadata om samtalet. Formatet är mycket flexibelt och låter dig lägga till all möjlig metadata du vill ha. Detta används till exempel för att kommunicera statistik om samtalet. Det används också för att hantera paketförluster och för överbelastningskontroll. Det ger dig den dubbelriktade kommunikation som krävs för att du ska kunna anpassa dig till varierande nätverksförhållanden.

## Latens mot kvalitet
Realtidsmedia handlar om att göra avvägningar mellan latens och kvalitet. Ju mer latens du är villig att tolerera, desto högre kvalitet kan du förvänta dig.

### Begränsningar i verkliga världen
Dessa begränsningar orsakas alla av den verkliga världens begränsningar. De är alla egenskaper hos ditt nätverk som du kommer att behöva hantera.

### Video är komplext
Att transportera video är inte lätt. För att lagra 30 minuter okomprimerad 720 8-bitars video behöver du circa 110 GB. Med dessa siffror kommer ett konferenssamtal på 4 personer inte gå att genomföra. Vi behöver ett sätt att göra det mindre, och svaret är videokomprimering. Det kommer dock att medföra andra nackdelar.

## Video 101
Vi kommer inte att gå igenom videokomprimering alltför detaljerat, bara tillräckligt för att förstå varför RTP är utformat som det är. Videokomprimering kodar video till ett nytt format som kräver färre bitar för att representera samma video.

### Förlustfri och inexakt komprimering
Du kan koda video för att vara förlustfri (ingen information går förlorad) eller inexakt (information kan gå förlorad). Eftersom förlustfri kodning kräver att mer data skickas till mottagaren, vilket ger högre latens och fler tappade paket, använder RTP vanligtvis inexakt komprimering även om videokvaliteten inte blir lika bra.

### Inexakt videokomprimering
Videokomprimering finns i två typer. Den första är enkel komprimering vilket betyder att man minskar bitarna som används för att beskriva en bild en bild i taget. Samma teknik används för att komprimera stillbilder, som till exempel JPEG-komprimering.

Den andra typen är dubbelriktad komprimering. Eftersom video består av många bilder letar vi efter sätt att inte skicka samma information två gånger.

### Dubbelriktad bildruta
Du har då tre bildtyper:

* **I-Bild** - En komplett bild, kan avkodas utan något annat
* **P-Bild** - En komprimerad bild som bara innehåller det som skiljer den från föregående bild.
* **B-Bild** - En dubbelriktad bildruta. Bilden återställs med hjälp av information från både den föregående och den efterföljande bildrutan.

Följande är visualisering av de tre bildtyperna.

![Frame types](../../images/06-frame-types.png "Bildtyper")

### Video är känslig
Videokomprimering är otroligt tillståndsbaserad, vilket gör den svår att överföra via internet. Vad händer om du förlorar en del av en I-Bild? Hur vet en P-Bild vad den ska ändra? Eftersom videokomprimering blivit mer och mer komplex har detta blivit ett ännu större problem. Lyckligtvis har RTP och RTCP en lösning på problemet.

## RTP
### Paketformat
Varje RTP-paket har följande struktur:

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
`Version` är alltid `2`

#### Padding (P)
`Padding` är en boolean som kontrollerar om datan har blivit utfylld till ett jämnt värde.

Den sista byten av data visar hur många utfyllnadsbytes som lagts till.

#### Tillägg (X)
Om inställt kommer RTP-rubriken att ha tillägg. Detta beskrivs närmare nedan.

#### CSRC-antal (CC)
Mängden `CSRC`-identifierare som följer efter `SSRC` och före datan.

#### Markör (M)
Markörbiten har ingen fördefinierad betydelse och kan användas som man vill.

I vissa fall sätts den när en användare pratar. Den används också ofta för att markera en nyckelbild (`key frame`).

#### Payload Type (PT)
`Payload Type` är en unik identifierare som beskriver vilken codec som används för detta paket.

För WebRTC är `Payload Type` dynamisk. VP8 i ett samtal kan vara annorlunda än ett annat. Avsändaren i samtalet bestämmer mappningen av `Payload Type` till kodekarna i sessionsbeskrivningen (`Session Description`).

#### Sekvensnummer
Sekvensnummer används för att hålla koll på ordningen av paketen i en ström. Varje gång ett paket skickas ökas sekvensnumret med ett.

RTP är utformat för att vara användbart över nätverk där man tappar paket. Sekvensnummer ger mottagaren ett sätt att upptäcka när paket har gått förlorade.

#### Tidsstämpel
Samplingsögonblicket för detta paket. Det här är inte en global klocka, utan hur mycket tid som har gått i mediaströmmen. Flera RTP paket kan ha samma tidsstämpel om de till exempel tillhör samma bild i en videoström.

#### Synkroniseringskälla (SSRC)
En `SSRC` är den unika identifieraren för denna ström. Detta gör att du kan köra flera mediaströmmar över en enda RTP-ström.

#### Bidragande källa (CSRC)
En lista som visar vilka källor (`SSRC`er) som bidrog till detta paket.

Detta används ofta för att visa vem som pratar. Om du kombinerade flera ljudflöden på serversidan till en enda RTP-ström, kan använda det här fältet för att säga "Källorna A och C pratade just nu".

#### Payload
Den faktiska datan. Den sista byten kan innehålla hur många utfyllnadsbytes som lagts till om utfyllnadsflaggan (`P`) är satt.

### Tillägg

## RTCP

### Paketformat
Varje RTCP-paket har följande struktur:

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
`Version` är alltid `2`.

#### Padding (P)
`Padding` är en boolean som kontrollerar om datan har blivit utfylld till ett jämnt värde.

Den sista byten av data visar hur många utfyllnadsbytes som lagts till.

#### Antal mottagningsrapporter (RC)
Antalet rapporter i detta paket. Ett enda RTCP-paket kan innehålla flera händelser.

#### Pakettyp (PT)
Unik identifierare för vilken typ av RTCP-paket detta är. En WebRTC-agent behöver inte stödja alla dessa typer, och stöd mellan klienter kan vara annorlunda. De följande är dock de som du ofta ser:

* `192` - Fullständig INTRA-frame Request (`FIR`)
* `193` - Negativa bekräftelser (`NACK`)
* `200` - Avsändarrapport
* `200` - Mottagarrapport
* `200` - Generisk RTP-feedback
* `200` - Specifik feedback för datan

Betydelsen av dessa pakettyper kommer att beskrivas mer detaljerat nedan.

### Full INTRA-frame Request (FIR) och Picture Loss Indication (PLI)
Både `FIR` och `PLI`-meddelanden tjänar ett liknande syfte. Dessa meddelanden begär en fullständig nyckelbild (`I-Bild`) från avsändaren.
`PLI` används när partiella bilder anländer till avkodaren som den inte kan avkoda.
Detta kan hända om du hade mycket paketförlust, eller kanske avkodaren kraschade.

Enligt [RFC 5104](https://tools.ietf.org/html/rfc5104#section-4.3.1.2) ska `FIR` inte användas när paket eller bilder går förlorade, det är `PLI`s jobb. `FIR` begär en nyckelbild av andra skäl än paketförlust - till exempel när en ny klient går med i en videokonferens. De behöver en hel nyckelram för att starta avkodning av videoströmmen, avkodaren kommer att kasta bort alla partiella bilder tills nyckelbild kommer.

Det är en bra idé för en mottagare att begära en fullständig nyckelbild direkt efter anslutning, detta minimerar fördröjningen mellan anslutning till att en bild visas på användarens skärm.

`PLI` paket är en del av dataspecifika feedback-meddelanden.

I praktiken kommer programvara som kan hantera både `PLI` och `FIR`-paket att fungera på samma sätt i båda fallen. Den kommer att skicka en signal till kodaren för att producera en ny nyckelbild.

### Negativa bekräftelser
Ett `NACK` begär att en avsändare sänder igen ett enda RTP-paket. Detta orsakas vanligtvis när ett RTP-paket går förlorat, men kan också hända eftersom det är sent.

`NACK` är mycket mer bandbreddseffektivt än att begära att hela bilden skickas igen. Eftersom RTP delar upp paket i många små bitar, begär du egentligen bara en liten saknad del. Mottagaren skapar ett RTCP-meddelande med SSRC och sekvensnummer. Om avsändaren inte har detta RTP-paket tillgängligt för att skicka igen ignorerar det bara meddelandet.

### Avsändar- och mottagarrapporter
Dessa rapporter används för att skicka statistik mellan agenter. Detta kommunicerar mängden paket som faktiskt mottagits och jitter.

Rapporterna kan användas för diagnostik och trängselskontroll.

## Hur RTP/RTCP löser problem tillsammans
RTP och RTCP arbetar sedan tillsammans för att lösa alla problem som orsakas av nätverk. Dessa tekniker förändras fortfarande.

### Vidarekorrigering av fel
Även känd som Forward Error Correction (FEC). En annan metod för att hantera paketförlust. FEC är när du skickar samma data flera gånger, utan att det ens begärs. Detta görs på RTP-nivå, eller till och med lägre nivå via kodeken.

Om paketförlusten för ett samtal är stabil get FEC en mycket lägre latens än NACK. Tur-och-returtiden för att begära och sedan skicka om ett paketet kan vara ganska stor när man använder NACK.

### Adaptiv bittakt och uppskattning av bandbredd
Nätverk är oförutsägbara och opålitliga, som vi tidigare diskuterade i kapitlet om [Realtidsnätverk](../05-real-time-networking/). Bandbredds tillgänglighet kan ändras flera gånger under en session.
Det är inte ovanligt att tillgänglig bandbredd förändras dramatiskt (flera storleksordningar) inom en sekund.

Huvudidén är att justera kodningshastigheten baserat på förutsagd, aktuell och framtida tillgänglig nätverksbandbredd.
Detta säkerställer att video- och ljudsignaler av bästa möjliga kvalitet överförs och att anslutningen inte tappas på grund av trängsel i nätverket.
Heuristik som modellerar nätverksbeteendet och försöker förutsäga det kallas uppskattning av bandbredd.

Det finns mycket nyans i detta, så låt oss utforska det mer i detalj.

## Kommunicera nätverksstatus
Det första problemet med att implementera trängselskontroll är att UDP och RTP inte kommunicerar nätverksstatus. Som avsändare har jag ingen aning om när mina paket anländer eller om de kom fram över huvud taget!

RTP/RTCP har tre olika lösningar på detta problem som alla har sina för- och nackdelar. Vad du använder beror på vilka klienter du arbetar med. Vad är topologin du arbetar med, eller till och med bara hur mycket utvecklingstid du har kvar.

### Mottagarrapporter
Mottagarrapporter är RTCP-meddelanden, det ursprungliga sättet att kommunicera nätverksstatus. Du hittar dem i [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4). De skickas enligt ett schema för varje SSRC och innehåller följande fält:

* **Fraktion förlorad** - Hur stor andel av paketen som har gått förlorade sedan den senaste mottagarrapporten.
* **Kumulativt antal förlorade paket** - Hur många paket som har gått förlorade under hela samtalet.
* **Utökat högsta mottagna sekvensnummer** - Vad var det senaste mottagna sekvensnumret och hur många gånger har det rullat över.
* **Interarrival Jitter** - Den rullande jittren för hela samtalet.
* **Senaste avsändarrapportens tidsstämpel** - Senast kända tid på avsändaren, används för beräkning av tur och retur-tid.

Avsändar- och mottagarrapporter (SR och RR) används tillsammans för att beräkna tur och retur-tid.

Avsändaren inkluderar sin lokala tid, `sendertime1` i avsändarrapporten (SR).
När mottagaren får SR-paket skickar den tillbaka mottagarrapporten (RR).
RR inkluderar bland annat `sendertime1` som just erhållits från avsändaren.
Det kommer att finnas en fördröjning mellan att ta emot SR och att skicka RR. På grund av detta inkluderar RR också en "fördröjning sedan senaste avsändares rapport" - `DLSR`.
`DLSR` används för att justera uppskattningen av tur och retur-tiden senare i processen.
När avsändaren tar emot RR drar den bort `sendertime1` och `DLSR` från aktuell tid som vi kallar `sendertime2`.
Detta tidsdelta kallas tur-och-retur-fördröjning.

`rtt = sendertime2 - sendertime1 - DLSR`

Rundturstid på vanlig svenska:
- Jag skickar ett meddelande till dig med min klockas nuvarande tid, säg att klockan är 16:20, 42 sekunder och 420 millisekunder.
- Du skickar tillbaka samma tidsstämpel till mig.
- Du inkluderar också tiden som gått från att du läste mitt meddelande tills att du skickade tillbaka meddelandet, säg 5 millisekunder.
- När jag har fått tiden tillbaka kollar jag på min klocka igen.
- Nu säger min klocka 16:20, 42 sekunder 690 millisekunder.
- Det betyder att det tog 265 millisekunder (690 - 420 - 5) att nå till dig och tillbaka till mig.
- Därför är tur-och-retur-tiden 265 millisekunder.

![Rundturstid](../../images/06-rtt.png "Rundturstid")

### TMMBR, TMMBN och REMB
Nästa generation av nätverksstatusmeddelanden involverar alla mottagare som skickar meddelanden via RTCP med uttryckliga bittaktförfrågningar.

* **Tillfällig maximal medieströmförfrågan för bittakt (TMMBR)** - En mantissa/exponent för en begärd bittakt för en enda SSRC.
* **Tillfällig maximal mediaströmbittaktsmeddelande (TMMBN)** - Ett meddelande om att en förfrågan har mottagits.
* **Mottagarens beräknade maximala bittakt (REMB)** - En mantissa/exponent för en begärd bithastighet för hela sessionen.

TMMBR och TMMBN kom först och definieras i [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB kom senare, det finns ett utkast i [draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), men det blev aldrig standardiserat.

En session som använder REMB skulle se ut enligt följande:

![REMB](../../images/06-remb.png "REMB")

Webbläsare använder en enkel tumregel för uppskattning av bandbredd:
1. Be omkodaren att öka bithastigheten om nuvarande paketförlust är mindre än 2%.
2. Om paketförlusten är högre än 10%, sänk bithastigheten med hälften av den aktuella paketförlustprocenten.
```
if (packetLoss < 2%) video_bitrate *= 1.08
if (packetLoss > 10%) video_bitrate *= (1 - 0.5*lossRate)
```

Denna metod fungerar bra på papper. Avsändaren tar emot uppskattning från mottagaren, ställer in kodningshastigheten till det mottagna värdet. Allt klart! Vi har anpassat oss till nätverksförhållandena.

I praktiken har REMB-metoden dock flera nackdelar.

Omkodares ineffektivitet är en av dem. När du anger en bithastighet för omkodare kommer den inte nödvändigtvis att mata ut den exakta bithastigheten du begärde. Den kan mata ut fler eller färre bitar, beroende på omkodarinställningarna och bilden som ska skickas.

Till exempel kan användning av x264-omkodaren med `tune=zerolatency` avsevärt avvika från den önskade bittakten. Här är ett möjligt scenario:

- Låt oss säga att vi börjar med att sätta bittakten till 1000 kbps.
- Omkodaren matar bara ut 700 kbps, eftersom det inte finns tillräckligt med detaljer i bilden att koda. (Också känt som "stirrar på en vägg".)
- Låt oss också föreställa oss att mottagaren tar emot 700 kbps-videon helt utan paketförlust. Den tillämpar då REMB-regel 1 för att öka den inkommande bithastigheten med 8%.
- Mottagaren skickar ett REMB-paket med ett förslag på 756 kbps (700 kbps * 1.08) till avsändaren.
- Avsändaren ställer in kodningshastigheten på 756 kbps.
- Kodaren matar ut en ännu lägre bithastighet.
- Denna process fortsätter att upprepa sig själv och sänker bittakten till det absoluta minimumet.

Man kan se hur detta snabbt skulle orsaka en alldeles för låg bittaktsinställning för omkodaren och på så sätt överraska användare med mycket dålig video även över en bra nätverksanslutning.

### Transport Wide Congestion Control
Transport Wide Congestion Control är den senaste utvecklingen inom RTCP-nätverksstatuskommunikation.

TWCC använder en ganska enkel princip:

![TWCC](../../images/06-twcc-idea.png "TWCC")

Till skillnad från i REMB försöker en TWCC-mottagare inte uppskatta sin egen inkommande bithastighet. Det låter bara avsändaren veta vilka paket som togs emot och när. Baserat på dessa rapporter har avsändaren en mycket uppdaterad uppfattning om vad som händer i nätverket.

- Avsändaren skapar ett RTP-paket med en speciell TWCC-header som innehåller en lista över paketsekvensnummer.
- Mottagaren svarar med ett speciellt RTCP-feedbackmeddelande som meddelar avsändaren om och när varje paket mottogs.

Avsändaren håller reda på skickade paket, deras sekvensnummer, storlekar och tidsstämplar.
När avsändaren tar emot RTCP-meddelanden från mottagaren jämför den sändningsfördröjningarna mellan paket med mottagningsfördröjningar.
Om mottagningsfördröjningarna ökar betyder det att det finns trängsel i nätverket som avsändaren måste anpassa sig till.

I diagrammet nedan är medianfördröjningen mellan paketet +20 msek, en tydlig indikator på att det är trängsel i nätverket.

! [TWCC med fördröjning](../../images/06-twcc.png "TWCC med fördröjning")

TWCC tillhandahåller rådata och en utmärkt insikt i nätverksförhållanden i realtid:
- Nästan omedelbar statistik över paketförluster, inte bara den procentuella förlusten utan de exakta paketen som förlorades.
- Exakt skickad bittakt.
- Exakt mottagningshastighet.
- En jitter uppskattning.
- Skillnaden i fördröjningar mellan att skicka och ta emot paket.

En trivial överbelastningskontrollalgoritm för att uppskatta den inkommande bitakten hos mottagaren från avsändaren är att summera paketstorlekar som mottagits och dela den med tiden som passerat.

## Skapa en uppskattning av bandbredd
Nu när vi har information om tillståndet för nätverket kan vi göra uppskattningar om tillgänglig bandbredd. 2012 startade IETF arbetsgruppen RMCAT (RTP Media Congestion Avoidance Techniques).
Denna arbetsgrupp innehåller flera inlämnade standarder för algoritmer för överbelastning. Innan dess var alla algoritmer för överbelastningskontroll egna.

Den mest använda implementeringen är "A Google Congestion Control Algorithm for Real-Time Communication" definierad i [draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).
In kan köra i två iterationer. Först ett "förlustbaserat" pass som bara använder mottagarrapporter. Om TWCC är tillgängligt kommer det också att ta hänsyn till den informationen.
Den förutspår nuvarande och framtida nätverksbandbredd genom att använda ett [Kalman-filter](https://en.wikipedia.org/wiki/Kalman_filter).

Det finns också flera alternativ till GCC, till exempel [NADA: A Unified Congestion Control Scheme for Real-Time Media](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) och [SCReAM - Self-Clocked Rate Adaptation for Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
