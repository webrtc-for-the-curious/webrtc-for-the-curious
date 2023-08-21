---
title: Mediakommunikation
type: docs
weight: 7
---

# Mediakommunikation

## Vad får jag från WebRTCs mediakommunikation?

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

## Identifiera och kommunicera nätverksstatus
RTP/RTCP skickas över alla typer av nätverk, och som ett resultat av det är det vanligt för viss kommunikation 
försvinner på väg från avsändaren till mottagaren. Eftersom det bygger på UDP finns det ingen inbyggd mekanism 
för att skicka om paket och inte heller något sätt att hantera överbelastning.

För att ge användarna den bästa upplevelsen måste WebRTC uppskatta kvaliteten på nätverket och
anpassa sig till hur dessa egenskaper förändras över tiden. De viktigaste egenskaperna att övervaka inkluderar:
tillgänglig bandbredd (i varje riktning, eftersom den kanske inte är symmetrisk), tur-och-returtid och jitter.
WebRTC måste ta hänsyn till paketförluster och kommunicera förändringar i dessa egenskaper allt eftersom
nätverksförhållandena ändras.

Det finns två primära mål för dessa protokoll:

1. Uppskatta den tillgängliga bandbredden (i varje riktning) i nätverket.
2. Kommunicera nätverksegenskaper mellan avsändare och mottagare.

RTP/RTCP har tre olika tillvägagångssätt för att lösa detta problem. De har alla sina för- och nackdelar,
och i allmänhet har varje generation förbättrats jämfört med sina föregångare. Vilken implementation du använder beror
i första hand på vilken mjukvara som är tillgänglig för dina klienter och vilka bibliotek som är tillgängliga för
dig för att bygga din applikation.

### Mottagar- och Avsändarrapporter
Den första implementeringen är paret av mottagarrapporter och dess komplement, avsändarrapporter. Dessa
RTCP-meddelanden definieras i [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4) och är
ansvariga för att kommunicera nätverksstatus mellan ändpunkter. Mottagarrapporter fokuserar på
kommunikationsegenskaper hos nätverket (inklusive paketförlust, tur-och-returtid och jitter), och det
paras ihop med andra algoritmer som sedan är ansvariga för att uppskatta tillgänglig bandbredd baserat på
dessa rapporter.

Avsändar- och mottagarerapporter (SR och RR) målar tillsammans en bild av nätverkskvaliteten. Dom skickas enligt ett
schema för varje SSRC, och de är den indata som används vid uppskattning av tillgänglig bandbredd. Dessa uppskattningar 
görs av avsändaren efter att ha mottagit RR-data som innehåller följande fält:

* **Fraktion förlorad** - Hur stor andel av paketen som har gått förlorade sedan den senaste mottagarrapporten.
* **Kumulativt antal förlorade paket** - Hur många paket som har gått förlorade under hela samtalet.
* **Utökat högsta mottagna sekvensnummer** - Vad var det senaste mottagna sekvensnumret och hur många gånger har det rullat över.
* **Interarrival Jitter** - Det rullande jittret för hela samtalet.
* **Senaste avsändarrapportens tidsstämpel** - Senast kända tid på avsändaren, används för beräkning av tur och retur-tid.

Avsändar- och mottagarrapporter (SR och RR) används tillsammans för att beräkna tur-och-returtid.

Avsändaren inkluderar sin lokala tid, `sendertime1` i avsändarrapporten (SR). När mottagaren får SR-paket skickar den
tillbaka mottagarrapporten (RR). RR inkluderar bland annat `sendertime1` som just erhållits från avsändaren. Det kommer
att finnas en fördröjning mellan att ta emot SR och att skicka RR. På grund av detta inkluderar RR också en
"fördröjning sedan senaste avsändares rapport" - `DLSR`. `DLSR` används för att justera uppskattningen av
tur-och-retur-tiden senare i processen. När avsändaren tar emot RR drar den bort `sendertime1` och `DLSR` från aktuell
tid som vi kallar `sendertime2`. Detta tidsdelta kallas tur-och-retur-fördröjning.

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

### TMMBR, TMMBN, REMB och TWCC, tillsammans med GCC

#### Google Congestion Control (GCC)
Algoritmen för Google Congestion Control (GCC) som beskrivs i
[draft-ietf-rmcat-gcc-02](https://tools.ietf.org/html/draft-ietf-rmcat-gcc-02) beskriver ett sätt att hantera
utmaningarna att uppskatta bandbredd. Den paras ihop med en mängd andra protokoll för att hantera de önskade
kommunikationskraven. Den går att köra antingen hos mottagaren (när man använder TMMBR/TMMBN eller REMB) 
eller hos avsändaren (för TWCC).

För att göra uppskattningar av tillgänglig bandbredd fokuserar GCC på paketförlust och fluktuationer i bild-ankomsttid 
som de primära källorna. Den kör dessa mätvärden genom två länkade kontroller: den förlustbaserad kontrollern och den
fördröjningsbaserade kontrollern.

GCC:s första komponent, den förlustbaserade kontrollern, är enkel:

* Om paketförlusten är över 10 %, minskas uppskattningen av bandbredden.
* Om paketförlusten är mellan 2-10 % behåller man bandbreddsuppskattningen densamma.
* Om paketförlusten är under 2 %, ökas bandbreddsuppskattningen.

Paketförlustmätningar görs ofta. Beroende på vilket kommunikationsprotokoll som används kan paketförlust antingen
skickas uttryckligen (som med TWCC) eller härledas (som med TMMBR/TMMBN och REMB). Dessa procentsatser utvärderas
över perioder på cirka en sekund.

Den fördröjningsbaserade kontrollern samarbetar med den förlustbaserade kontrollern, men kollar istället på 
variationen i ankomsttiderna för paketen. Den fördröjningsbaserade kontrollern kan känna av när nätverkslänkar 
blir alltmer överbelastade, och kan minska bandbredden redan innan paket börjar tappas. Teorin är att det högst
belastade nätverksgränssnittet längs vägen kommer att fortsätta att köa upp paket tills dess buffertar fylls up.
Om det gränssnittet fortsätter att ta emot mer trafik än det kan skicka, kommer den att tvingas slänga alla paket
som den inte får plats dess buffer. Denna typ av paketförlust är särskilt störande för låg latens/realtid
kommunikation, men kan också försämra kapaciteten för all kommunikation över den länken och bör helst undvikas.
Således försöker GCC ta reda på om köerna i nätverket växer sig större och större _innan_ paket börjar tappas. 
Algoritmen kommer att minska bandbreddsanvändningen om den märker att köerna ökar i storlek.

GCC försöker räkna ut ökningar i köstorlek genom att mäta subtila ökningar i tiden det tar att skicka och ta emot
paket. Den registrerar skillnaden i bildernas ankomsttid, `t(i) - t(i-1)`: skillnaden i ankomsttid mellan två
grupper av paket (oftast två bilder i ordning). Dessa paketgrupper skickas ofta med regelbundna tidsintervall
(t.ex. var 1/24:e sekund för en 24 fps video). På grund av det är det lätt att mäta ankomsttiden genom att 
registrera tidsskillnaden mellan starten av den första paketgruppen (dvs. en bild) och den första bilden i nästa grupp.

I diagrammet nedan är medianökningen mellan paketfördröjningen +20 msek, en tydlig indikator på överbelastning.

![TWCC med fördröjning](../../images/06-twcc.png "TWCC med fördröjning")

Om skillnaden i ankomsttider ökar över tiden, antas det vara bevis på att köerna ökar i storlek och nätverket anses vara
överbelastat. (Obs: GCC är smart nog att kontrollera dessa mätningar för fluktuationer i bildstorlekar.) GCC förfinar
sina latens mätningar med hjälp av ett [Kalman-filter](https://en.wikipedia.org/wiki/Kalman_filter) och tar många
mätningar av nätverkets tur-och-returtid (och dess variationer) innan den rapporterar att det är överbelastat. Man kan
säga att GCCs Kalman-filter används istället för en linjär regression och hjälper till att göra bättre
förutsägelser även när jitter gör timingmätningarna lite oberäkneliga. När GCC rapporterar att nätet är överbelastat
kommer den också att minska den tillgängliga näthastigheten. Alternativt, under stabila nätverksförhållanden, kan den 
långsamt öka sina bandbreddsuppskattningar för att testa om nätet har mer kapacitet.

#### TMMBR, TMMBN, och REMB
För TMMBR/TMMBN och REMB uppskattar mottagaren först tillgänglig inkommande bandbredd (med hjälp av ett protokoll som
GCC), och kommunicerar sedan sina bandbreddsuppskattningar till avsändarna. De behöver inte utbyta information om
paketförlust eller överbelastning i nätverket eftersom som mottagare kan de mäta intervallet mellan ankomsttiderna och 
paketförluster direkt. Istället utbyter TMMBR, TMMBN och REMB bara själva bandbreddsuppskattningarna:

* **Tillfällig maximal medieströmförfrågan för bittakt (TMMBR)** - En mantissa/exponent för en begärd bittakt för en enda SSRC.
* **Tillfällig maximal mediaströmbittaktsmeddelande (TMMBN)** - Ett meddelande om att en förfrågan har mottagits.
* **Mottagarens beräknade maximala bittakt (REMB)** - En mantissa/exponent för en begärd bithastighet för hela sessionen.

TMMBR och TMMBN kom först och definieras i [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB kom senare, det finns
ett utkast i [draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), men det blev
aldrig standardiserat.

En session som använder REMB skulle se ut enligt följande:

![REMB](../../images/06-remb.png "REMB")

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
Transport Wide Congestion Control är den senaste utvecklingen inom RTCP-nätverksstatuskommunikation. Det definieras i
[draft-holmer-rmcat-transport-wide-cc-extensions-01](https://datatracker.ietf.org/doc/html/draft-holmer-rmcat-transport-wide-cc-extensions-01),
men har aldrig standardiserats.

TWCC använder en ganska enkel princip:

![TWCC](../../images/06-twcc-idea.png "TWCC")

Med REMB skickar mottagaren hur hög bandbredd den har tillgängligt till avsändaren. Mottagaren använder
precisa mätningar av uppskattade paketförluster och data som bara den har om ankomsttiden mellan paket.

TWCC är ungefär som en hybrid mellan SR/RR och REMB-generationerna av protokoll. Det ger
bandbreddsuppskattningar tillbaka till avsändarsidan (som SR/RR), men dess bandbreddsuppskattningsteknik
påminner mer om REMB-generationen.

Med TWCC skickar mottagaren tillbaka ankomsttiden för varje paket till avsändaren. Det är all information
avsändaren behöver för att mäta variationen mellan paketens ankomstfördröjning, och dessutom identifiera
vilka paket som tappades eller kom för sent för att kunna bidra till ljud-/videoflödet. Eftersom dessa uppgifter
utbyts ofta kan avsändaren snabbt anpassa sig till ändrade nätverksförhållanden och variera sin bandbredd med
hjälp av en algoritm såsom GCC.

Avsändaren håller reda på skickade paket, deras sekvensnummer, storlekar och tidsstämplar. När avsändaren tar 
emot RTCP-meddelanden från mottagaren, jämför den fördröjningarna mellan paketen som skickats med fördröjningarna
hos mottagaren. Om mottagningsförseningarna ökar signalerar det att nätverket är överbelastat, och avsändaren måste
vidta korrigerande åtgärder.

TWCC tillhandahåller rådata och ger en utmärkt insikt i nätverksförhållanden i realtid:
- Nästan omedelbar statistik över paketförluster, inte bara den procentuella förlusten utan de exakta paketen som förlorades.
- Exakt skickad bittakt.
- Exakt mottagningshastighet.
- En jitter uppskattning.
- Skillnaden i fördröjningar mellan att skicka och ta emot paket.
- Beskrivning av hur nätverket tolererade sprängd eller jämn bandbreddsleverans

Ett av de viktigaste bidragen från TWCC är den flexibilitet det ger WebRTC-utvecklare. Att konsolidera algoritmen
för överbelastningskontroll till sändningssidan gör klientkoden enklare och att den kräver mindre förändringar. 
Komplexa algoritmer för överbelastningskontroll kan sedan itereras på snabbare direk på hårdvaran de har
kontroll över (som den selektiva vidarebefordringsenheten, diskuterad i avsnitt 8). När det gäller webbläsare och
mobila enheter innebär detta att dessa klienter kan dra nytta av algoritmförbättringar utan att behöva vänta på
standardisering eller webbläsaruppdateringar (vilket kan ta ganska lång tid att bli allmänt tillgänglig).

## Alternativ för uppskattning av bandbredd
Den mest använda implementeringen är "A Google Congestion Control Algorithm for Real-Time Communication" definierad i
[draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).

Det finns också flera alternativ till GCC, till exempel [NADA: A Unified Congestion Control Scheme for Real-Time Media](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04)
och [SCReAM - Self-Clocked Rate Adaptation for Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
