---
title: Realtidsnätverk
type: docs
weight: 6
---

# Realtidsnätverk

## Varför är nätverket så viktigt i realtidskommunikation?

Nätverk är den begränsande faktorn i realtidskommunikation. I en idealisk värld skulle vi ha obegränsad bandbredd
och paket skulle komma omedelbart. Detta är dock inte fallet. Nätverk är begränsade och villkoren
kan ändras när som helst. Att mäta och observera nätverksförhållanden är också ett svårt problem. Du kan få olika beteenden
beroende på hårdvara, programvara och konfigurationen av den.

Realtidskommunikation medför också ett problem som inte finns i många andra domäner. För en webbutvecklare är det inte avgörande
om din webbplats är långsammare i vissa nätverk. Så länge all data kommer fram är användarna nöjda. Med WebRTC, om din data kommer fram
sent är den värdelös. Ingen bryr sig om vad som sagts i ett konferenssamtal för 5 sekunder sedan. Det betyder att när man utvecklar ett realtidskommunikationssystem
måste man göra en avvägning. Vad är min tidsgräns och hur mycket data kan jag skicka?

Detta kapitel handlar om de koncept som gäller både data- och mediekommunikation. I senare kapitel går vi igenom mer i detalj hur WebRTCs media- och data-subsystem löser dessa problem.

## Vilka egenskaper har nätverk som gör det svårt?
Kod som effektivt fungerar i alla nätverk är komplicerad. Du har många olika faktorer, och de
kan alla påverka varandra på subtila sätt. Här är några av de vanligaste problemen som utvecklare stöter på.

#### Bandbredd

Bandbredd är den maximala datahastigheten som kan uppnås via en viss väg genom nätet. Det är viktigt att komma ihåg
att värdet kommer att ändras under tiden. Bandbredden ändras längs en rutt (route) beroende på om fler (eller färre) människor använder den.

#### Sändningstid och rundturstid (Round Trip Time)
Sändningstid är hur lång tid det tar för ett paket att anlända till sitt mål. Precis som bandbredd är den inte konstant utan kan variera när som helst.

`transmission_time = mottagningstid - send_time`

För att beräkna sändningstiden behöver klockorna på avsändaren och mottagaren vara synkroniserade med millisekunders precision.
Till och med en väldigt liten avvikelse ger oss en opålitlig mätning av sändningstiden.
Eftersom WebRTC används i väldigt blandade miljöer är det nästan omöjligt att förlita sig på perfekt tidssynkronisering mellan klienterna.

Tidsmätning tur och retur är en bättre lösning när klocksynkronisering inte är möjligt.

Istället för att använda distribuerade klockor skickar en WebRTC-klient ett specialpaket med sin egen tidsstämpel `sendertime1`.
En mottagande klient tar emot paketet och skickar tillbaka tidsstämpeln till avsändaren.
När den ursprungliga avsändaren får tillbaka tidsstämpeln drar den av `sendertime1` från aktuella tiden `sendertime2`.
Denna tidsdelta kallas "round-trip propagation delay" eller rundturstid.

`rtt = sendertime2 - sendertime1`

Hälften av tur- och returresan anses vara en tillräckligt bra approximation av sändningstiden.
Denna lösning är dock inte utan nackdelar.
Den antar att det tar lika lång tid att skicka som att ta emot paket.
Men i mobilnätverk kan sändnings- och mottagnings-tider vara väldigt olika.
Du har kanske märkt att uppladdningshastigheter på din telefon nästan alltid är lägre än nedladdningshastigheter.

`transmission_time = rtt/2`

Tekniken WebRTC använder för att mäta rundturstid beskrivs mer detaljerat i [kapitlet om RTCP Sender and Receiver Reports](../06-media-communication/#mottagar--och-avsändarrapporter).

#### Jitter
Jitter är det faktum att "sändningstid" (`Transmission Time`) kan variera för varje paket. Dina paket kan bli fördröjda, men sen kommer alla på en gång.

#### Paketförlust
Paketförlust är när meddelanden går förlorade vid överföring. Förlusten kan vara jämn, eller så kan den komma i korta perioder.
Detta kan bero på olika nätverkstyper som satellit eller Wi-Fi, eller introduceras av programvara längs vägen.

#### Maximal överföringsenhet
Maximal paket storlek (MTU) är gränsen för hur stort ett enskilt data-paket kan vara. Nätverk tillåter dig inte att skicka
hur stora meddelanden som helst. På protokollnivå kan meddelanden behöva delas upp i flera mindre paket.

MTU kommer också att skilja sig beroende på vilken nätverksväg du tar. Du kan
använda ett protokoll som [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) för att räkna ut den största paketstorleken du kan skicka utan att det måste fragmenteras.

#### Trängsel
Trängsel är när nätverksgränserna har uppnåtts. Detta beror vanligtvis på att du har nått den maximala
bandbredd som den aktuella rutten klarar. Eller så kan det vara operatören som begränsar din datamängd per timme.

Trängsel visar sig på många olika sätt. Det finns inget standardiserat beteende. I de flesta fall brukar
nätverket tappa överflödiga paket. I andra fall kommer nätverket att buffra. Detta gör att sändningstiden
för dina paket kommer att öka. Du kan också märka mer jitter när ditt nätverk blir överbelastat. Detta här är ett område där mycket ändras
och nya algoritmer för att upptäcka överbelastning utvecklas fortfarande.

#### Dynamisk
Nätverk är oerhört dynamiska och förhållandena kan förändras snabbt. Under ett samtal kan du skicka och ta emot hundratusentals paket.
Dessa paket kommer att resa genom flera nätverkshopp. De här nätverkshoppen kommer att delas med miljontals andra användare. Även i ditt lokala nätverk kan du ha
HD-filmer som laddas ner eller kanske en enhet bestämmer sig för att ladda ner en stor programuppdatering.

För att ha ett bra videosamtal räcker det inte att bara mäta nätverket vid starten. Du måste ständigt utvärdera och hantera alla förändringar 
 som kommer från nätverket och programvaran som är inblandad.

## Lösa paketförlust
Att hantera paketförlust är det första problemet att lösa. Det finns flera sätt att lösa det, alla med olika för- och nackdelar. Dels beror det på vad du skickar och hur mycket
latens som är acceptabelt. Det är också viktigt att notera att inte all paketförlust är kritisk. Att förlora lite video behöver inte vara ett problem, det mänskliga ögat kanske inte
även uppfattar det. Att förlora en användares textmeddelanden är ödesdigert.

Låt oss säga att du skickar 10 paket, och paket 5 och 6 går förlorade. Här är några exempel på hur man kan lösa det.

### Bekräftelser
Bekräftelser är när mottagaren meddelar avsändaren om varje paket de har fått. Avsändaren är medveten om paketförlust när den får ett bekräftelse
för samma paket två gånger som inte är det sista paketet. När avsändaren får ett `ACK` för paket nummer 4 två gånger, vet den att paket nummer 5 inte har levererats än.

### Selektiva bekräftelser
Selektiva bekräftelser är en förbättring jämfört med bekräftelser. En mottagare kan skicka ett `SACK` som bekräftar flera paket och meddelar avsändaren om luckor.
Om avsändaren får ett `SACK` för paket 4 och 7. Då vet den att den måste skicka paket 5 och 6 igen.

### Negativa bekräftelser
Negativa bekräftelser löser problemet tvärtom. Istället för att meddela avsändaren vad den har fått, meddelar mottagaren avsändaren vad den saknar. I vårt fall kommer ett `NACK`
att skickas för paket 5 och 6. Avsändaren får bara reda på paket som mottagaren vill ska skickas igen.

### Forward Error Correction
Forward Error Correction är ett sätt att tåla viss paketförlust. Avsändaren skickar redundant data, vilket innebär att ett enstaka förlorat paket inte påverkar den slutliga strömmen. En populär algoritm för detta är Reed–Solomon-felkorrigering.

Detta minskar latensen och komplexiteten för att skicka och hantera bekräftelser. Forward Error Correction är ett slöseri med bandbredd om nätverket du använder inte har någon paketförlust.

## Hantera jitter
Jitter finns i de flesta nätverk. Även på ett lokalt nätverk har du många enheter som skickar data med varierande hastigheter. Du kan enkelt se jitter genom att pinga en annan enhet med kommandot `ping` och notera variationen i tiden det tar att få svar.

För att hantera jitter använder du en JitterBuffer. En JitterBuffer garanterar en stabil leveranstid för paketen. Nackdelen är att JitterBuffer lägger till lite extra latens för varje paket som kommer i tid.
Fördelen är att sena paket inte orsakar något jitter. Föreställ dig att du ser följande ankomsttider för några paket under ett samtal:

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

I det här fallet skulle cirka 1,8 ms vara ett bra val. Paket som kommer försent kommer att använda vårt latensfönster. Paket som kommer tidigt kommer att fördröjas lite och kan
fylla ut luckan från sena paket. Det betyder att videoströmmen inte längre stammar och ger klienten en jämn leveranshastighet.

### JitterBuffer-funktion

![JitterBuffer](../../images/05-jitterbuffer.png "JitterBuffer")

Varje paket läggs till jitterbufferten så snart det tas emot.
När det finns tillräckligt med paket för att återskapa hela bilden släpps paketen som utgör bilden från bufferten och skickas för avkodning.
Avkodaren i sin tur ritar upp bilden på användarens skärm.
Eftersom jitterbufferten har en begränsad storlek kommer paket som fastnat för länge i bufferten att kasseras.

Läs mer om hur video konverteras till RTP-paket och varför rekonstruktion är nödvändig [i kapitlet om mediekommunikation](../06-media-communication/#rtp).

`jitterBufferDelay` visar tydligt ditt nätverks prestanda och hur den påverkar videouppspelningens jämnhet.
Det är en del av [WebRTC Statistics API](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) och spelar roll för mottagarens inkommande videoström.
Förseningen definierar hur mycket tid bilder spenderar i jitterbuffern innan de skickas vidare för avkodning.
En lång jitterbuffertfördröjning innebär att ditt nätverk är överbelastat.

## Upptäcka trängsel
Innan vi ens kan lösa trängsel måste vi upptäcka det. För att upptäcka det använder vi en trängselregulator (congestion controller). Detta är ett komplicerat ämne och förändras fortfarande snabbt.
Nya algoritmer publiceras fortfarande och testas. På en hög nivå fungerar de alla på samma sätt. En överbelastningsregulator ger en uppskattning av bandbredd givet en viss indata.
Det här är några möjliga indata:

* **Paketförlust** - Paket tappas när nätverket blir överbelastat.
* **Jitter** - När nätverksutrustningen blir mer överbelastad kommer köande av paket orsaka oregelbundna leveranstider.
* **Rundturstid** - Paket tar längre tid att anlända när uppkopplingen är överbelastad. Till skillnad från jitter fortsätter rundturstiden bara att öka.
* **Explicit trängselnotis** - Nyare nätverk kan märka paket som riskerar att tappas för att undvika trängsel.

Dessa värden måste mätas kontinuerligt under samtalet. Användningen av nätverket kan öka eller minska, så den tillgängliga bandbredden kan ständigt förändras.

## Lösa trängsel
Nu när vi har en uppskattad bandbredd måste vi justera vad vi skickar. Hur vi justerar beror på vilken typ av data vi vill skicka.

### Skicka långsammare
Att begränsa hastigheten med vilken du skickar data är ett enkelt sätt att förhindra trängsel. Trängselregulatorn ger dig en uppskattning, och det är
avsändarens ansvar att bedöma hur mycket hastigheten ska begränsas.

Detta är den vanligaste metoden som brukar användas. Med protokoll som TCP görs allt detta av operativsystemet och helt transparent för både användare och utvecklare.

### Skicka mindre
I vissa fall kan vi skicka mindre information för att undvika att slå i taket. Vi kan också ha hårda tidsbegränsningar för när våra data ska levereras, så vi kanske kan inte skicka långsammare. Det här är en typisk begränsning som realtidsmedier faller under.

Om vi inte har tillräckligt med bandbredd kan vi sänka kvaliteten på den video vi skickar. Detta kräver en tät feedbackslinga mellan din videoencoder och din trängselregulator.
