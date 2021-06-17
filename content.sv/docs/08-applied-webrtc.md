---
title: Hur WebRTC används
type: docs
weight: 9
---

# Hur WebRTC används
Nu när du vet hur WebRTC fungerar är det dags att bygga något med det! Detta kapitel utforskar vad människor har
byggt med WebRTC och hur de bygger det. Du kommer att lära dig alla intressanta saker som är
händer med WebRTC. Kraften i WebRTC kostar. Att bygga WebRTC-tjänster med produktionskvalitet är
utmanande. Detta kapitel kommer att försöka förklara dessa utmaningar innan du drabbas av dem.

## Användningsfall
Många tror att WebRTC bara är en teknik för konferenser i webbläsaren, men det finns så mycket mer man kan använda det till!
WebRTC används på många olika sätt och nya användningsfall dyker upp hela tiden. I detta kapitel kommer vi att lista några vanliga användningsfall och hur WebRTC revolutionerar dem.

### Konferenser
Konferenser är det ursprungliga användningsfallet för WebRTC. Protokollet innehåller några nödvändiga funktioner som inget annat protokoll erbjuder
i webbläsaren. Du kan bygga ett konferenssystem med WebSockets och det kan fungera under optimala förhållanden. Men om du vill ha
något som tål alla störningar som finns i våra nätverk är WebRTC det bästa valet.

WebRTC ger överbelastningskontroll och adaptiv bithastighet för media. När villkoren för nätverket ändras kommer användarna fortfarande att få
bästa möjliga upplevelse. Utvecklare behöver inte skriva någon ytterligare kod för att hantera dessa villkor.

Deltagare kan skicka och ta emot flera strömmar. De kan också lägga till och ta bort dessa strömmar när som helst under samtalet. Codecs förhandlas fram
också. All denna funktion tillhandahålls redan av webbläsaren, ingen ny kod behöver skrivas av utvecklaren.

Konferenser drar också nytta av datakanaler. Användare kan skicka metadata eller dela dokument. Du kan skapa flera strömmar
och konfigurera dem om du prioriterar prestanda mer än tillförlitlighet.

### Utsändning
Många nya projekt relaterade till utsändning använder sig av WebRTC. Protokollet har mycket att erbjuda för både utgivare och konsumenter av media.

WebRTC i webbläsaren gör det enkelt för användare att publicera video. Det tar bort kravet för användare att ladda ner en ny klient.
Alla plattformar som har en webbläsare kan publicera video. Utgivare kan sedan skicka flera spår och ändra eller ta bort dem när som helst. Detta är
en enorm förbättring jämfört med äldre protokoll som bara tillät ett ljud eller videospår per anslutning.

WebRTC ger utvecklare större kontroll över avvägningen mellan latens och kvalitet. Det kan vara viktigare att latensen aldrig överstiger ett
visst värde, och du kanske är villig att istället visa lite sämre videokvalitét. Du kan konfigurera dekodern att spela upp media så snart den tagits emot.
Med andra protokoll som körs över TCP är det inte lika enkelt. I webbläsaren kan du begära data och det är allt.

### Fjärranslutning
Fjärråtkomst är när du ansluter till en annan dator via WebRTC. Du kan ha fullständig kontroll över hela datorn, eller kanske bara en
applikation på den. En vanlig tillämpning är att köra tunga beräkningsuppgifter som den lokala hårdvaran inte klarar av. Som att köra ett nytt videospel, eller
CAD-programvara. WebRTC har revolutionerat det här området på tre sätt.

WebRTC kan användas för att ansluta till en server som inte har någon publik adress. Med NAT Traversal kan du komma åt en dator som endast är tillgänglig
via STUN. Detta är bra för säkerhet och anonymitet. Dina användare behöver inte skicka video via någon publik server. NAT Traversal gör också
distributionen enklare. Du behöver inte oroa dig om att öppna portar eller ställa in et statiskt IP i förväg.

Datakanaler är också mycket kraftfulla i det här scenariot. De kan konfigureras så att endast de senaste uppgifterna accepteras. Med TCP riskerar du
att stöta på head-of-line blockering. Ett gammalt musklick eller tangenttryckning kan komma för sent och blockera nyare händelser.
WebRTCs datakanaler är utformade för att hantera detta och kan konfigureras för att inte försöka skicka förlorade paket igen. Du kan också mäta mottrycket (backpressure) och
se till att du inte skickar mer data än ditt nätverk klarar av.

Att WebRTC är tillgängligt i webbläsaren har gjort allt betydligt enklare. Du behöver inte ladda ner någon egen klient för att starta ett samtal.
Fler och fler kunder kommer med WebRTC-paket, till och med smarta TV-apparater har fullt stöd för webbläsare nu.

### Fildelning och undvika censur
Fildelning och att undvika censur är väldigt olika problem. WebRTC kan dock lösa båda problemen. Den gör
båda lätt tillgängliga och svårare att blockera.

Det första problemet som WebRTC löser är att du redan har en klient. Om du vill gå med i ett nätverk för fildelning måste du ladda ner klienten. Även om
nätverket distribueras måste du fortfarande få klienten först. I ett begränsat nätverk kommer nedladdningar ofta att blockeras. Och även om du
kan ladda ner den kanske du inte kan installera och köra klienten. WebRTC är redan tillgängligt i alla moderna webbläsare.

Det andra problemet som WebRTC löser är att din trafik blockeras. Om du använder ett protokoll som bara är gjort för fildelning eller f;r att kringgå censur,
är det mycket lättare att blockera det. Eftersom WebRTC är ett mer generellt protokoll kan blockering av det påverka vem som helt. Blockering av WebRTC kan till exempel hindra
andra användare i nätverket från att koppla upp sig till ett konferenssamtal.

### Internet of Things
Internet of Things (IoT) täcker några olika användningsfall. För många betyder detta nätverksanslutna säkerhetskameror. Med WebRTC kan du strömma videon till en annan WebRTC
klient som till exempel din telefon eller en webbläsare. Ett annat användningsfall är att enheter ansluter och utbyter sensordata. Du kan ha två enheter i ditt lokala nätverk
utbyta temperatur, ljud eller ljus-mätvärden.

WebRTC har en enorm integritetsfördel här jämfört med äldre videoströmprotokoll. Eftersom WebRTC stöder P2P-anslutning kan kameran skicka videon
direkt till din webbläsare. Det finns ingen anledning att din video ska skickas via en tredjepartsserver. Även när video är krypterad kan en angripare göra
antaganden baserat på samtalens metadata.

Interoperabilitet är en annan fördel när det kommer till IoT. WebRTC finns implementerat för många olika språk; C#, C++, C, Go, Java, Python, Rust
och TypeScript. Det betyder att du kan använda det språk som fungerar bäst för dig. Du behöver inte heller använda företagsspecifika protokoll eller proprietära format
för att koppla ihop dina klienter.

### Översättning av medieprotokoll
Tänk dig att du har befintlig hårdvara och programvara som producerar video, men du kan inte uppgradera den just nu. Att förvänta sig att användare ska ladda ner en proprietär
klient för att kunna se videon är onödigt frustrerande. En enklare lösning är att sätta upp en WebRTC-bro. Bron översätter mellan det gamla och nya protokollen så att 
användarna kan använda webbläsare för att se videon från din äldre installation.

Många av de format som utvecklare sätter upp broar mot med använder samma protokoll som WebRTC. SIP exponeras vanligtvis via WebRTC och tillåter användare att ringa telefonsamtal
direkt från webbläsaren. RTSP används i många äldre säkerhetskameror. De använder båda samma underliggande protokoll (RTP och SDP) eftersom de kräver väldigt lite beräkningskraft
att köra. WebRTC-bron krävs bara för att lägga till eller ta bort saker som är WebRTC-specifika.

### Översättning av dataprotokoll
En webbläsare kan bara tala en begränsad uppsättning protokoll. Du kan använda HTTP, WebSockets, WebRTC och QUIC. Om du vill ansluta
till något annat behöver du översätta protokollet. En protokollbro är en server som omvandlar data trafik till något som webbläsaren
kan förstå. Ett populärt exempel är att använda SSH från din webbläsare för att komma åt en server. WebRTCs datakanaler har två fördelar framför konkurrenterna.

WebRTCs datakanaler möjliggör opålitlig och oordnad leverans. I fall där låg latens är avgörande är detta ett måste. Du vill inte att ny data
blockeras av gammal data, så kallad head-of-line blocking. Tänk dig att du spelar en snabbt multiplayer förstapersonsspel. Bryr du dig verkligen om var en annan
spelare var för två sekunder sedan? Om datan inte kom fram i tid är det meningslöst att fortsätta försöka skicka den. Otillförlitlig och oordnad leverans låter
dig få datan så snart den anländer.

Datakanaler ger också information om belastningen i nätet. Det berättar om du skickar data snabbare än vad din anslutning kan hantera. Du har två
lösningar att välja på när det händer. Datakanalen kan antingen konfigureras för att buffra och leverera data lite senare, eller så kan du strunta i data som inte har kommit
fram i tid.

### Teleoperation
Teleoperation är när man fjärrstyr en enhet via WebRTC-datakanaler och skickar tillbaka videon via RTP. Utvecklare kör bilar på avstånd
via WebRTC idag! Det används för att kontrollera robotar på byggarbetsplatser och för att leverera paket. Att använda WebRTC för dessa problem är praktiskt av två skäl.

Att WebRTCs är så lättillgängligt gör det enkelt att ge användare kontrollen. Allt användaren behöver är en webbläsare och något att styra med. Webbläsare har till och med
stöd för joysticks och gamepads. WebRTC tar helt enkelt bort behovet av att installera ytterligare en klient på användarens enhet.

### Distribuerad CDN
Distribuerade CDN:er är en typ av fildelning. Filerna som distribueras konfigureras istället av CDN-operatören. När användare ansluter sig till CDN-nätverket
de kan ladda ner och dela de tillåtna filerna. Användare får samma fördelar som fildelning.

Dessa CDN fungerar bra när du är på ett kontor som har en dålig internetuppkoppling, men ett snabbt lokalt nätverk. Du kan låta en användare ladda ner en video och
dela det sedan med alla andra. Eftersom alla inte försöker hämta samma fil via det externa nätverket kommer överföringen att gå mycket snabbare.

## WebRTC Topologier
WebRTC är ett protokoll för att ansluta två klienter, så hur ansluter utvecklare hundratals människor på en gång? Det finns några olika
sätt du kan göra det, och de har alla olika för och nackdelar. Dessa lösningar faller i stort sett i två kategorier; peer-to-peer eller klient/server. WebRTCs
flexibilitet tillåter oss att implementera båda.

### En till en
En-till-en är den första anslutningstypen du använder med WebRTC. Du ansluter två WebRTC-agenter direkt och de kan skicka dubbelriktad media och data.
Anslutningen ser ut så här.

![En-till-en](../images/08-one-to-one.png "En-till-en")

### Full Mesh
Full mesh är svaret om du vill bygga ett konferenssamtal eller ett multiplayer-spel. I denna topologi upprättar varje användare en anslutning
med alla andra användare direkt. Detta gör att du kan bygga din applikation, men det kommer med några nackdelar.

I en Full Mesh kopplas varje användare direkt mot alla andra. Det betyder att du måste koda och ladda upp video oberoende för varje medlem i samtalet.
Nätverksförhållandena mellan varje anslutning kommer att vara olika, så du kan inte återanvända samma video. Felhanteringen är också svår i den här typen av lösningar.
Du måste noga överväga om du har helt tappat din anslutning eller bara anslutning med en av de andra klienterna.

På grund av dessa problem används ett Full Mesh bäst för små grupper. För större grupper är en klient/server topologi bäst.

![Full mesh](../../images/08-full-mesh.png "Full mesh")

### Hybrid Mesh
Hybrid Mesh är ett alternativ till Full Mesh som kan lindra några av problemen mett ett Full Mesh. I en Hybrid Mesh-anslutning upprättas inte
mellan varje användare. Istället vidarebefordras media genom andra klienter i nätverket. Detta betyder att avsändaren av media inte behöver använda lika
mycket bandbredd för att distribuera media.

Detta har dock några nackdelar. I denna konfiguration har den ursprungliga skaparen av media ingen aning vem dess video skickas till, eller om
den ens kom fram. Du kommer också att öka latensen för varje hopp i ditt Hybrid Mesh-nätverk.

![Hybrid mesh](../../images/08-hybrid-mesh.png "Hybrid mesh")

### Selektiv vidarebefordringsenhet
En SFU (Selective Forwarding Unit) löser också problemen med ett Full Mesh, men på ett helt annat sätt. En SFU implementerar en klient/server topologi istället för P2P.
Varje WebRTC-peer ansluter till SFU:en och laddar upp sin media. SFU:en vidarebefordrar sedan denna media till varje ansluten klient.

Med en SFU behöver varje WebRTC-agent bara koda och ladda upp sin video en gång. Arbetet att distribuera den till alla tittare ligger på SFUn.
Anslutning till en SFU är också mycket enklare än P2P. Du kan köra en SFU på en publik IP adress, vilket gör det mycket lättare för kunder att ansluta.
Du behöver inte oroa dig för NAT Mappings. Du måste fortfarande se till att din SFU är tillgänglig via TCP (antingen via ICE-TCP eller TURN).

Att bygga en enkel SFU kan göras på en helg. Att bygga en bra SFU som kan hantera alla typer av klienter är näst intill omöjligt. Att justera trängselkontroll, felkorrigering och prestanda är ett arbete som aldrig tar slut.

![Selektiv vidarebefordringsenhet](../../images/08-sfu.png "Selektiv vidarebefordringsenhet")

### MCU
En MCU (Multi-point Conferencing Unit) är en klient/server-topologi som en SFU, men den sätter ihop videoströmmarna. Istället för att distribuera utgående media
omodifierad kodar den om alla inkommande strömmar till en utgående videoström.

![Multi-point Conferencing Unit](../../images/08-mcu.png "Multi-point Conferencing Unit")
