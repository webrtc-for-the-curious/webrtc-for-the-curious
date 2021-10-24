---
title: Anslutning
type: docs
weight: 4
---

# Varför behöver WebRTC ett särskilt delsystem för anslutning?
De flesta applikationer som distribueras idag upprättar klient/serveranslutningar. En klient/serveranslutning kräver att servern har en känd och publik adress. En klient ansluter till en server, och servern svarar.

WebRTC använder inte en klient/server-modell utan skapar peer-to-peer (P2P) anslutningar. I en P2P-anslutning fördelas uppgiften att skapa en anslutning lika till båda parterna. Detta beror på att en publik nätverksadress (IP och port) är inget man kan förvänta sig i WebRTC, och den kan till och med ändras mitt under sessionen. WebRTC kommer att samla så mycket information som det går, och sedan göra allt den kan för sätta upp en dubbelriktad kommunikationsväg mellan två WebRTC-agenter.

Det kan dock vara svårt att skapa peer-to-peer-anslutning. Dessa agenter kan finnas i olika nätverk utan direkt anslutning. I situationer där direkt anslutning finns kan du fortfarande ha andra problem. I vissa fall talar dina klienter inte samma nätverksprotokoll (UDP <-> TCP) eller kanske har olika IP-versioner (IPv4 <-> IPv6).

Trots dessa svårigheter med att skapa en P2P-anslutning får du fördelar jämfört med traditionell klient/server-teknik på grund av följande funktioner WebRTC erbjuder.

### Reducerade bandbreddskostnader
Eftersom mediekommunikation sker direkt mellan klienterna behöver du inte betala för eller drifta en egen server för att vidarebefordra media.

### Lägre latens
Kommunikationen går snabbare när den är direkt! När en användare måste köra allt via din server gör det överföringarna långsammare.

### Säker E2E-kommunikation
Direkt kommunikation är säkrare. Eftersom användarnas trafik inte går via din server, behöver de inte ens lita på att du inte dekrypterar den.

## Hur fungerar det?
Processen som beskrivs ovan kallas Interactive Connectivity Establishment ([ICE](https://tools.ietf.org/html/rfc8445)). Ytterligare ett protokoll som är äldre än WebRTC.

ICE är ett protokoll som försöker hitta det bästa sättet att kommunicera mellan två ICE-agenter. Varje ICE-agent publicerar hur den kan nås, dessa kallas kandidater. En kandidat är i huvudsak en nätverksadress för agenten som den tror att den andra klienten kan nå. ICE bestämmer sedan det bästa hopkopplingen av klienterna.

Den faktiska ICE-processen beskrivs mer detaljerat senare i detta kapitel. För att förstå varför ICE existerar är det bra att förstå vilket nätverksproblem vi behöver hantera.

## Nätverksbegränsningar
ICE handlar om att övervinna begränsningarna i dagens nätverk. Innan vi utforskar lösningen, låt oss prata om några vanliga problem.

### Inte i samma nätverk
För det mesta kommer den andra WebRTC-agenten inte ens att vara i samma nätverk. Ett typiskt samtal är vanligtvis mellan två WebRTC-agenter i olika nätverk utan direktanslutning.

Nedan är en figur som visar två distinkta nätverk, anslutna via internet. I varje nätverk har du två parter.

![Två nätverk](../../images/03-two-networks.png "Två nätverk")

För parterna i samma nätverk är det mycket enkelt att ansluta. Kommunikation mellan `192.168.0.1 -> 192.168.0.2` är lätt att göra! Dessa två parter kan ansluta till varandra utan någon extern hjälp.

En värd som använder `Router B` har dock inget sätt att komma åt något bakom "Router A". Hur kan den se skillnad på `191.168.0.1` bakom `Router A` och samma IP bakom `Router B`? De är privata IP-adresser! En värd som använder `Router B` kan skicka trafik direkt till `Router A`, men anropet slutar där. Hur vet `Router A` vilken värd den ska vidarebefordra meddelandet till?

### Protokollbegränsningar
Vissa nätverk tillåter inte UDP-trafik alls, eller kanske tillåter de inte TCP. Vissa nätverk kan ha en mycket låg MTU (Maximum Transmission Unit, storleken på varje paket). Det finns många variabler som nätverksadministratörer kan ändra som kan göra det svårt att kommunicera.

### Brandvägg/IDS-regler
En annan är "Deep Packet Inspection" och andra intelligenta filtreringar. Vissa nätverksadministratörer kommer att köra programvara som försöker bearbeta varje paket. Många gånger förstår inte denna programvara WebRTC, så den blockerar den eftersom den inte vet vad den ska göra, t.ex. behandlas WebRTC-paket som misstänkta UDP-paket när de kommer på en godtycklig port som inte är känd.

## NAT-kartläggning
NAT (Network Address Translation) är den magi som gör anslutningen av WebRTC möjlig. Så här tillåter WebRTC att två parter i helt olika subnät kommunicerar och behandlar problemet "inte i samma nätverk" ovan. Medan det skapar nya utmaningar, låt oss förklara hur NAT Mapping fungerar först.

Det använder inte ett relay, proxy eller server. Återigen har vi `Agent 1` och `Agent 2` och de finns i olika nätverk, men ändå flyter trafiken utan problem. Visualiserat ser det ut så här:

![NAT mapping](../../images/03-nat-mapping.png "NAT mapping")

För att få denna kommunikation att upprätta skapar du en översättning med hjälp av NAT. Agent 1 använder port 7000 för att upprätta en WebRTC-anslutning med Agent 2. Detta skapar en koppling från `192.168.0.1:7000` till `5.0.0.1:7000`. Detta gör det möjligt för Agent 2 att nå Agent 1 genom att skicka paket till `5.0.0.1:7000`. Att skapa en NAT-mappning som i det här exemplet är som en automatisk version av att forward:a en port i din router.

Nackdelen med NAT är att det inte finns något konsekvent sätt att göra det på (t.ex. vidarebefordran av en statisk port), och att beteendet är olika i olika nätverk. Internetleverantörer och hårdvarutillverkare kan göra det på olika sätt. I vissa fall kan nätverksadministratörer till och med inaktivera det.

Den goda nyheten är att hela beteendet är förstått och observerbart, så en ICE-agent kan bekräfta att den har satt upp NAT rätt och vet då alla inställningarna i mappningen.

Dokumentet som beskriver dessa beteenden är [RFC 4787](https://tools.ietf.org/html/rfc4787).

### Skapa en NAT-mappning
Att skapa en NAT-mappning är den enkla biten. När du skickar ett paket till en adress utanför ditt nätverk skapas en mappning! En NAT-mappning är bara en tillfällig offentlig IP och port som tilldelas av din NAT. Det utgående meddelandet kommer att skrivas om så att dess källadress ges av den nyligen mappade adressen. Om ett meddelande skickas tillbaka till den adressen, så dirigeras det automatiskt tillbaka till värden bakom den NAT:ade interna adressen. Detaljerna kring NAT är där det blir komplicerat.

### Olika sorters NAT
En NAT tillhör en av tre olika kategorier:

#### Slutpunktoberoende mappning (Endpoint-Independent)
En mappning skapas för varje avsändare i NAT:at nätverk. Om du skickar två paket till två olika adresser kommer NAT-mappningen att återanvändas. Båda parterna utanför det lokala nätet skulle se samma avsändare IP och port. Om de svarar, skulle det skickas tillbaka till samma lokala lyssnare.

Detta är det bästa fallet. För att ett samtal ska fungera, MÅSTE åtminstone en av parterna vara av den här typen.

#### Adressberoende mappning
En ny mappning skapas varje gång du skickar ett paket till en ny adress. Om du skickar två paket till olika parter skapas två mappningar. Om du skickar två paket till samma part men till olika destinationsportar skapas INTE en ny mappning.

#### Adress- och port-beroende mappning
En ny mappning skapas om fjärr-IP:t eller porten är annorlunda. Om du skickar två paket till samma IP utanför det lokala nätet, men olika portar, skapas en ny mappning för varje.

### Mappning av filtreringsbeteenden
Mappningsfiltrering handlar om reglerna kring vem som får använda mappningen. Det finns tre liknande klassificeringar:

#### Slutpunktsoberoende filtrering
Vem som helst kan använda mappningen. Du kan dela mappningen med flera andra parter och de kan alla skicka trafik till den.

#### Adressberoende filtrering
Endast värden som mappningen skapades för kan använda mappningen. Om du skickar ett paket till agent `A` kan det svara tillbaka med så många paket som det vill. Om agent `B` försöker skicka ett paket till den mappningen ignoreras det.

#### Adress- och port-beroende filtrering
Endast IP:t och porten för vilken mappningen skapades för kan använda den. Om du skickar ett paket till agent `A:5000` kan det svara tillbaka med så många paket som det vill. Om en agent `A:5001` försöker skicka ett paket till samma mappningen ignoreras paketet.

### Uppdatera en mappning
Det rekommenderas att om en mappningen inte används på 5 minuter ska den förstöras. Detta är helt upp till ISP eller hårdvarutillverkaren.

## STUN
STUN (Session Traversal Utilities for NAT) är ett protokoll som skapades för att jobba med NATs. Det är ytterligare en teknik som skapats före WebRTC (och ICE!). Specifikationen hittar du i [RFC 8489](https://tools.ietf.org/html/rfc8489), som också definierar STUN-paketformatet. STUN-protokollet används också av ICE/TURN.

STUN är användbart eftersom det tillåter programmering av NAT mappning. Innan STUN kunde vi sätta upp ett NAT, men vi hade ingen aning om vilket IP och port det var! STUN ger dig inte bara möjligheten att skapa en NAT mappning, du får också detaljerna så att du kan dela dem med andra så att de kan skicka trafik till dig via den mappning du just skapade.

Låt oss börja med en grundläggande beskrivning av STUN. Senare kommer vi att utöka TURN- och ICE-användningen. För närvarande ska vi bara beskriva flödet för begäran / svar för att skapa en kartläggning. Sedan kommer vi att prata om hur man får detaljerna i den att dela med andra. Detta är processen som händer när du har en `stun:`-server i dina ICE-URL:er för en WebRTC PeerConnection. Kort sagt, STUN hjälper en server bakom ett NAT:at nätverk att lista ut vilken mappning som skapades genom att fråga en STUN-server utanför det lokala nätverket vad den kan se.

### Protokollstruktur
Varje STUN-paket har följande format:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|0 0|     STUN Message Type     |         Message Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Magic Cookie                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     Transaction ID (96 bits)                  |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### STUN Meddelande typ
Varje STUN-paket har en typ. Just nu bryr vi oss bara om följande två:

* Bindningsförfrågan - `0x0001`
* Bindningssvar - `0x0101`

För att skapa en NAT-mappning gör vi ett `Binding Request`. Sedan svarar servern med ett `Binding Response`.

#### Meddelandets längd
Hur långt avsnittet `Data` är. Detta avsnitt innehåller godtycklig data som definieras av `Message Type`.

#### Magic Cookie
Det fasta värdet `0x2112A442` i nätverksbyteordning (network byte order), det hjälper till att skilja STUN-trafik från andra protokoll.

#### Transaktions ID
En 96-bitars identifierare som unikt identifierar en begäran/svar. Detta hjälper dig att para ihop dina begäran och svar.

#### Data
Data kommer att innehålla en lista med STUN-attribut. Ett STUN-attribut har följande struktur:

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 ```

Ett `STUN Binding Request` använder inga attribut. Det betyder att en `STUN Binding Request` endast innehåller en header.

En `STUN Binding Response` använder en `XOR-MAPPED-ADDRESS (0x0020)`. Detta attribut innehåller en IP och port. Detta är IP och port för den NAT-mappning som skapas!

### Skapa en NAT-mappning
Att skapa en NAT-mappning med STUN kräver bara att skicka en begäran! Du skickar ett `STUN Binding Request` till STUN-servern. STUN-servern svarar sedan med en `STUN Binding Response`.
Denna `STUN Binding Response` kommer att innehålla en `Mapped Address`. Den "mappade adressen" är hur STUN-servern ser dig. Det är din "NAT-mappning".
Den "mappade adressen" är vad du skulle dela om du vill att någon ska skicka paket till dig.

Din "mappade adress" kallas också för ditt "publika IP" eller ibland `Server Reflexive Candidate`.

### Bestämma NAT-typ
Tyvärr kan en "mappad adress" kanske ändå inte vara användbar. Om reglerna är "adressberoende" (`Address Dependent`) kan bara STUN-servern skicka trafik till dig. Om du delade adressen och en annan agent försöker skicka meddelanden kommer de att ignoreras. Detta gör det värdelöst för att kommunicera med andra. Du kanske tycker att fallet "adressberoende" faktiskt går att lösa om STUN-servern också kan vidarebefordra paket åt dig till din andra part! Detta leder oss till en annan teknik, TURN.

[RFC 5780](https://tools.ietf.org/html/rfc5780) definierar en metod för att göra ett test för att lista ut din NAT-typ. Detta är användbart eftersom du kan veta i förväg om direktanslutning var möjlig.

## TURN
TURN (Traversal Using Relays around NAT) definieras i [RFC 8656] (https://tools.ietf.org/html/rfc8656) är lösningen när direktanslutning inte är möjlig. Det kan bero på att du har två NAT-typer som är oförenliga eller kanske inte kan tala samma protokoll! TURN kan också användas för sekretessändamål. Genom att köra all din kommunikation genom TURN döljer du klientens faktiska adress.

TURN använder en dedikerad server. Denna server fungerar som en proxy för en klient. Klienten ansluter till en TURN-server och skapar en allokering (`Allocation`). Genom att skapa en allokering får en klient en tillfällig IP/port/protokoll som kan användas för att skicka trafik tillbaka till klienten. Den här nya lyssnaren kallas en `Relayed Transport Address`. Tänk på det som en vidarebefordringsadress, du använder den så att andra kan skicka dig trafik via TURN! För varje klient du ger din `Relay Transport Address` till måste du skapa ett nytt "tillstånd" (`Permission`) för att tillåta kommunikation med dig.

När du skickar utgående trafik via TURN skickas den via din `Relayed Transport Address`. När en annan klient får trafik ser den ut att komma från TURN-servern.

### TURN Livscykel
Följande är allt som en klient som vill skapa en TURN-allokering måste göra. Kommunikation med någon som använder TURN kräver inga ändringar. Den andra klienten får ett IP och en port, och de kommunicerar med den som vilken annan server som helst.

#### Tilldelningar (Allocations)
Tilldelningar är kärnan i TURN. En "allokering" är i grunden en "TURN Session". För att skapa en TURN-allokering kommunicerar du med en TURN `Server Transport Address` (vanligtvis på port `3478`).

När du skapar en tilldelning måste du ange följande:
* Användarnamn/lösenord - För att skapa TURN-tilldelningar krävs autentisering
* Allokeringstransport - Den 'vidarebefordrade transportadressen' kan vara UDP eller TCP
* Even-Port - Du kan begära sekventiella portar för flera tilldelningar, inte relevanta för WebRTC.

Om begäran lyckades får du svar med TURN-servern med följande STUN-attribut i Data-sektionen:
* `XOR-MAPPED-ADRESS` - `Mappad adress` för din `TURN Client`. När någon skickar data till "Relayed Transport Address", vidarebefordras den till.
* `RELAYED-ADRESS` - Det här är adressen som du ger ut till andra klienter. Om någon skickar ett paket till den här adressen vidarebefordras det till TURN-klienten.
* `LIFETIME`- Hur länge tills denna TURN-fördelning tas bort. Du kan förlänga livslängden genom att skicka ett uppdaterings anrop (`Refresh`).

#### Behörigheter
En klient kan inte skicka till din `Relayed Transport Address` förrän du skapar ett tillstånd för den. När du skapar en behörighet berättar du för TURN-servern att denna IP och Port får skicka inkommande trafik.

Klienten måste ge dig IP och port som den ser ut för TURN-servern. Det betyder att den ska skicka ett `STUN Binding Request` till TURN-servern. Ett vanligt felfall är att en klient skickar ett `STUN Binding Request` till en annan server. De kommer då att be dig skapa en behörighet för denna IP.

Låt oss säga att du vill skapa en behörighet (`permission`) för en klient bakom en "adressberoende mappning". Om du genererar en "mappad adress" från en annan TURN-server kommer all inkommande trafik att ignoreras. Varje gång de kommunicerar med en annan klient genererar den en ny mappning. Behörigheterna löper ut efter 5 minuter om de inte uppdateras.

#### SendIndication/ChannelData
Dessa två meddelanden är avsedda för TURN-klienten att skicka meddelanden till en klient.

SendIndication är ett fristående meddelande. Det innehåller den information du vill skicka, och vem du vill skicka den till. Detta är slösaktigt om du skickar många meddelanden till en annan klient. Om du skickar 1000 meddelanden kommer du att upprepa deras IP-adress 1000 gånger!

ChannelData låter dig skicka data, utan att upprepa IP-adressen. Du skapar en kanal med en IP och port. Du skickar sedan med ChannelId och IP och port fylls i på serversidan. Detta är bättre om du skickar många av meddelanden.

#### Refreshing
Allokeringar kommer att ta bort sig själva automatiskt. TURN-klienten måste uppdatera dem innan deras `LIFETIME` som ges när tilldelningen skapas går ut.

### TURN Användning
TURN Användningen finns i två former. Vanligtvis har du en part som fungerar som en "TURN klient" och den andra sidan kommunicerar direkt. I vissa fall kan du ha TURN-server på båda sidor, till exempel för att båda klienterna finns i nätverk som blockerar UDP, och därför sker anslutningen till respektive TURN-servrar via TCP.

Dessa figurer hjälper till att illustrera hur det skulle se ut.

#### En TURN allokering för kommunikation

![En TURN allokering](../../images/03-one-turn-allocation.png "En TURN allokering")

#### Två TURN allokeringar för kommunikation

![Två TURN allokeringar](../../images/03-two-turn-allocations.png "Två TURN allokeringar")

## ICE
ICE (Interactive Connectivity Establishment) är tekniken WebRTC använder för att ansluta två klienter med varandra. Definierad i [RFC 8445](https://tools.ietf.org/html/rfc8445), detta är ytterligare en standard som är återanvänd i WebRTC. ICE är ett protokoll för att sätta upp av anslutningar. Det hittar alla möjliga rutter (routes) mellan de två klienterna och säkerställer att de kan kommunicera med varandra.

Dessa rutter är kända som `Candidate Pairs`, vilket är en anslutning mellan en lokal och en extern adress. Det är här STUN och TURN används tillsammans med ICE. Dessa adresser kan vara din lokala IP-adress plus en port, "NAT-mappning" eller en `Relayed Transport Address`. Båda klienterna listar alla adresser de vill använda, skickar över dem och försöker sedan ansluta.

Två ICE-agenter kommunicerar med hjälp av ICE-ping-paket (`connectivity checks`) för att sätta upp en anslutning. När anslutningen har upprättats kan de skicka vilken data de vill. Det blir som att använda en normal socket. Dessa kontroller använder STUN-protokollet.

### Skapa en ICE-agent
En ICE-agent är antingen `Controlling` eller `Controlled`. Den "kontrollerande" agenten är den som bestämmer vilken kandidat (`Candidate Pair`) som ska användas. Vanligtvis är den klient som skickar erbjudandet den kontrollerande sidan.

Varje klient måste ha ett "användarfragment" (`user fragment`) och ett "lösenord" (`password`). Dessa två värden måste utbytas innan anslutningskontroller kan göras. "Användarfragmentet" skickas i klartext och är användbart för att separera (demuxing) flera ICE-sessioner.
Lösenordet används för att generera attributet `MESSAGE-INTEGRITY`. I slutet av varje STUN-paket finns det ett attribut som är en hash för hela paketet med "lösenordet" som en nyckel. Detta används för att autentisera paketet och se till att det inte har blivit manipulerat.

För WebRTC skickas alla dessa värden via "sessionsbeskrivningen" som beskrevs i förra kapitlet.

### Kandidatsamling
Vi måste nu samla alla möjliga adresser vi kan nås på. Dessa adresser kallas kandidater.

#### Klient
En klientkandidat lyssnar direkt på ett lokalt nätverksinterface, antingen via UDP eller TCP.

#### mDNS
En mDNS-kandidat liknar en klientkandidat, men IP-adressen är dold. Istället för att informera den andra sidan om din IP-adress, ger du dem ett UUID som värdnamn. Du ställer istället upp en multicast-lyssnare och svarar om någon frågar efter det UUID som du publicerat.

Om du är i samma nätverk som agenten kan du hitta varandra via multicast. Om du inte är i samma nätverk kommer du inte att kunna ansluta (om inte nätverksadministratören uttryckligen konfigurerat nätverket så att multicast-paket kan passera).

Detta är användbart för sekretessändamål. En användare kan ta reda på din lokala IP-adress via WebRTC med en klientkandidat (utan att ens försöka ansluta till dig), men med en mDNS-kandidat får de nu bara ett slumpmässigt UUID.

#### Serverreflexiv kandidat
En serverreflexiv kandidat genereras genom att göra ett `STUN Binding Request` till en STUN-server.

När du får en `STUN Binding Response`, är `XOR-MAPPED-ADDRESS` din serverreflexiva kandidat.

#### Peer Reflexive
En Peer Reflexive-kandidat är när du får en inkommande begäran från en adress som du inte känner till. Eftersom ICE är ett autentiserat protokoll vet du att trafiken är giltig. Detta betyder bara att den andra klienten försöker kommunicera med dig från en extern adress den ännu inte känner till.

Detta händer ofta när en "klientkandidat" kommunicerar med en "serverreflexiv kandidat". En ny "NAT-mappning" skapades eftersom du kommunicerar utanför ditt subnät. Kommer du ihåg att vi sa att anslutningskontrollerna faktiskt är STUN-paket? Formatet för STUN-svar tillåter naturligtvis en peer att rapportera tillbaka den peer-reflexiva adressen.

#### Relä (Relay)
En reläkandidat genereras med hjälp av en TURN-server.

Efter den första handskakningen med TURN-servern får du en `RELAYED-ADDRESS`, detta är din reläkandidat.

### Anslutningskontroller
Vi känner nu till den andra klientens "användarfragment", "lösenord" och kandidater. Vi kan nu försöka ansluta! Alla kandidater matchas med varandra, så om du har 3 kandidater på varje sida har du nu 9 kandidatpar.

Visuellt ser det ut så här:

![Anslutningskontroller](../../images/03-connectivity-checks.png "Anslutningskontroller")

### Kandidatval
Den kontrollerande och kontrollerade agenten skickar a trafik över varje par. Detta behövs om en agent står bakom en "adressberoende mappning" (`Address Dependent Mapping`). Detta kommer att skapa en ny "peer reflexive kandidat".

Varje "kandidatpar" som lyckades skicka nätverkstrafik befordras till ett "giltigt kandidatpar". Den kontrollerande agenten nominerar sedan ett giltigt kandidatpart. Detta blir det "nominerade paret". Den kontrollerande och kontrollerade agenten försöker sedan ytterligare en runda dubbelriktad kommunikation. Om det lyckas blir det "nominerade paret" det "utvalda kandidatparet" (`Selected Candidate Pair`)! Detta par används sedan under resten av sessionen.

### Startar om
Om ditt `Selected Candidate Pair` slutar fungera av någon anledning (NAT-mappning upphör att gälla, TURN-server kraschar) kommer ICE-agenten att få status `Failed`. Båda agenterna kan startas om och kommer att göra hela processen om igen.
