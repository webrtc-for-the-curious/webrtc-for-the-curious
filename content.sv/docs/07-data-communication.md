---
title: Datakommunikation
type: docs
weight: 8
---

# Vad får jag från WebRTCs datakommunikation?
WebRTC tillhandahåller datakanaler för datakommunikation. Mellan två klienter kan du öppna 65534 datakanaler.
En datakanal är UDP-baserad och alla har sina egna hållbarhetsinställningar. Som standard har varje data kanal garanterad leveransordning på skickade paket.

Om du närmar dig WebRTC från ett mediabakgrund kan datakanaler verka slösaktiga. Varför använda hela detta delsystem när du bara kan använda HTTP eller WebSockets?

Den verkliga kraften hos datakanaler är att du kan konfigurera dem så att de beter sig som UDP med oordnad/osäker leverans.
Detta är nödvändigt för situationer med låg latens och höga prestanda. Du kan mäta mottrycket och försäkra dig att du bar skickar bara så mycket data som ditt nätverk klarar.

## Hur fungerar det?
WebRTC använder Stream Control Transmission Protocol (SCTP), definierat i [RFC 4960](https://tools.ietf.org/html/rfc4960). SCTP är ett
transportlagerprotokoll som var tänkt som ett alternativ till TCP eller UDP. För WebRTC använder vi det som ett applikationslagerprotokoll via vår DTLS-anslutning.

SCTP ger dig strömmar och varje ström kan konfigureras oberoende. WebRTC-datakanaler är bara tunna abstraktioner kring dem. Inställningarna
kring hållbarhet och beställning skickas precis in i SCTP-agenten.

Datakanaler har vissa funktioner som SCTP inte kan hantera, till exempel kanaletiketter (labels). För att lösa det använder WebRTC DCEP (Data Channel Establishment Protocol)
vilket definieras i [RFC 8832](https://tools.ietf.org/html/rfc8832). DCEP definierar meddelanden för att kommunicera kanaletiketten och protokollet.

## DCEP
DCEP har bara två meddelanden `DATA_CHANNEL_OPEN` och `DATA_CHANNEL_ACK`. För varje datakanal som öppnas måste mottagaren svara med ett ack.

### DATA_CHANNEL_OPEN
Detta meddelande skickas av WebRTC-agenten som vill öppna en kanal.

#### Paketformat
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |  Channel Type |            Priority           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Reliability Parameter                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Label Length          |       Protocol Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                             Label                             /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            Protocol                           /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Message Type
Message Type har alltid samma värde, `0x03`.

#### Channel Type
Med Channel Type sätter man kanalens hållbarhet och ordningsattribut. Den kan ha följande värden:

* `DATA_CHANNEL_RELIABLE` (` 0x00`) - Inga meddelanden går förlorade och de levereras i ordning.
* `DATA_CHANNEL_RELIABLE_UNORDERED` (` 0x80`) - Inga meddelanden går förlorade, men kan komma i fel ordning.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT` (` 0x01`) - Meddelanden kan gå förlorade efter att ha försökt ett givet antal gånger, men de kommer i ordning.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED` (` 0x81`) - Meddelanden kan gå förlorade efter att ha försökt ett givet antal gånger och kan också komma i fel ordning.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED` (` 0x02`) - Meddelanden kan gå förlorade om de inte kommer fram inom den önskade tiden, men de kommer fram i ordning.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED` (` 0x82`) - Meddelanden kan gå förlorade om de inte kommer fram inom önskad tid och kan komma i vilken ordning som helst.

#### Prioritet
Datakanalens prioritet. Datakanaler med högre prioritet schemaläggs först. Stora meddelanden med lägre prioritet kommer inte att orsaka fördröjningar för meddelanden med högre prioritet.

#### Pålitlighetsparameter
Om datakanaltypen är `DATA_CHANNEL_PARTIAL_RELIABLE` konfigurerar suffixet beteendet:

* `REXMIT` - Definierar hur många gånger avsändaren ska skicka meddelandet igen innan den ger upp.
* `TIMED` - Definierar hur länge (i ms) avsändaren ska skicka meddelandet igen innan den ger upp.

#### Etikett (Label)
Namnet på datakanalen som en UTF-8-kodad sträng. Det kan vara en tom sträng.

#### Protokoll
Om det är en tom sträng är protokollet ospecificerat. Om fältet innehåller text ska det vara ett protokoll registrerat i "WebSocket Subprotocol Name Registry", definierat i [RFC 6455](https://tools.ietf.org/html/rfc6455#page-61).

### DATA_CHANNEL_ACK
Detta meddelande skickas av WebRTC-agenten för att bekräfta att datakanalen har öppnats.

#### Paketformat
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
```

## Stream Control Transmission Protocol
SCTP är den kraftfulla biten med WebRTC-datakanaler. Det ger alla dessa funktioner i datakanalen:

* Multiplexing av data.
* Pålitlig leverans med en TCP-liknande återsändningsmekanism.
* Alternativ för tillåta en viss paketförlust.
* Inställningar för att undvika trängsel i nätet. 
* Flödeskontroll.

För att förstå SCTP kommer vi att utforska protokollet i tre delar. Målet är att du ska veta tillräckligt för att kunna felsöka och själv lära dig detaljer om SCTP efter detta kapitel.

## Begrepp
SCTP är ett protokoll med många funktioner. Detta avsnitt kommer endast att gå igenom de delar av SCTP som används av WebRTC.
Funktioner i SCTP som inte används av WebRTC inkluderar multi-homing och sökväg (path selection).

Med över tjugo års utveckling bakom sig kan det vara svårt att få en överblick av SCTP.

### Association
Association är den term som används för en SCTP-session. Det är tillståndet som delas
mellan två SCTP-agenter medan de kommunicerar.

### Strömmar
En ström är en dubbelriktad sekvens av användardata. När du skapar en datakanal skapar du bara en SCTP-ström. Varje SCTP Association innehåller en lista med strömmar. Varje ström kan konfigureras med olika tillförlitlighetstyper.

WebRTC låter dig bara konfigurera när strömmen skapas, men SCTP tillåter egentligen att ändra konfigurationen när som helst.

### Datagrambaserat
SCTP skickar data som datagram och inte som en byte-ström. Att skicka och ta emot data känns mer som att använda UDP istället för TCP.
Du behöver inte lägga till någon extra kod för att skicka flera filer över en ström.

SCTP-meddelanden har inga storleksgränser, till skillnad från UDP. Ett enda SCTP-meddelande kan innehålla flera gigabyte.

### Avsnitt
SCTP-protokollet består av avsnitt (chunks). Det finns många olika typer av avsnitt och de används för all kommunikation.
Användardata, initialisering av anslutningar, överbelastningskontroll och mer görs via avsnitt.

Varje SCTP-paket innehåller en lista med avsnitt. Så i ett UDP-paket kan du ha flera avsnitt med meddelanden från olika strömmar.

### Sändningssekvensnummer
Transmission Sequence Number (TSN) är en global unik identifierare för DATA-avsnitt. Ett DATA-avsnitt är det som innehåller alla meddelanden en användare vill skicka. TSN är viktigt eftersom det hjälper en mottagaren att avgöra om paket har tappats eller om de inte fungerar.

Om mottagaren märker att en TSN saknas, ger den inte datan till användaren förrän den har tagit emot den.

### Strömidentifierare
Varje ström har en unik identifierare. När du skapar en datakanal med ett uttryckligt ID skickas det faktiskt precis in i SCTP som strömidentifierare. Om du inte skickar ett ID väljs strömidentifieraren åt dig.

### Payload Protocol Identifier
Varje DATA-avsnitt har också en Payload Protocol Identifier (PPID). Detta används för att unikt identifiera vilken typ av data som utbyts.
SCTP har många PPID, men WebRTC använder bara följande fem:

* `WebRTC DCEP` (`50`) - DCEP-meddelanden.
* `WebRTC String` (`51`) - Strängmeddelanden.
* `WebRTC Binary` (`53`) - Binära meddelanden.
* `WebRTC String Empty` (`56`) - Strängmeddelanden med 0 längd.
* `WebRTC Binary Empty` (`57`) - Binära meddelanden med 0 längd.

## Protokoll
Följande är några av de bitar som används av SCTP-protokollet. Detta är
inte någon utförlig beskrivning, utan bara de grundläggande strukturerna
för att förstå tillståndsmaskinen.

Varje avsnitt börjar med ett `type`-fält. Innan en lista med avsnitt kommer du att finnas en rubrik (header).

### DATA-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 0    | Reserved|U|B|E|    Length                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              TSN                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Stream Identifier        |   Stream Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Payload Protocol Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            User Data                          /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
När du skickar data över datakanalen packeteras allt som DATA-avsnitt.

`U`-flaggan är satt om detta är ett oordnat paket. Då kan vi ignorera strömsekvensnumret.

`B` och `E` är början och slutet. Om du vill skicka ett
meddelande som är för stort för ett DATA-avsnitt, måste det fragmenteras till flera mindre
DATA-avsnitt som skickas var för sig.
Flaggorna `B` och `E` och sekvensnummret är hur SCTP kommunicerar detta.

* `B=1`, `E=0` - Första delen av ett fragmenterat användarmeddelande.
* `B=0`, `E=0` - Mellanstycke i ett fragmenterat användarmeddelande.
* `B=0`, `E=1` - Sista delen av ett fragmenterat användarmeddelande.
* `B=1`, `E=1` - Ofragmenterat meddelande.

`TSN` är sändningssekvensnumret. Det är det globala unika
identifierare för detta meddelande. Efter 4 294 967 295 DATA-avsnitt börjar räknaren om.
Om ett meddelande fragmenterats till flera DATA-avsnitt, uppdateras sändningssekvensnumret
för varje DATA-avsnitt så att mottagaren kan återskapa det usprungliga meddelandet korrekt.

`Stream Identifier` är det unika IDt för strömmen som den här datan tillhör.    

`Stream Sequence Number` (strömssekvensnumret) är ett 16-bitars nummer som ökas på för användarmeddelande och ingår i rubriken för varje DATA-avsnitt. Efter 65 535 meddelanden börjar räknaren om på 0. Detta nummer används för att bestämma meddelandets leveransordning till mottagaren om flaggan `U` inte är satt. Det liknar TSN, förutom att strömssekvensnumret bara ökas för varje meddelande som skickas och inte varje enskilt DATA-avsnitt.            

`Payload Protocol Identifier` visar vilken typ av data som skickas via
den här strömmen. För WebRTC kommer det att vara DCEP, String eller Binary.

`User Data` är den data du skickar. All data du skickar via en WebRTC-datakanal
överförs i DATA-avsnitt.

### INIT-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 1    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Initiate Tag                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Advertised Receiver Window Credit (a_rwnd)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Number of Outbound Streams   |  Number of Inbound Streams    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Initial TSN                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/              Optional/Variable-Length Parameters              /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

INIT-avsnittet startar processen att skapa en koppling.

`Initiate Tag` används för att generera kakor. Cookies används för Man-In-The-Middle
och Denial of Service-skydd. De beskrivs mer detaljerat i staten
maskinsektion.

`Advertised Receiver Window Credit` används för SCTPs trängselskontroll. Fältet 
visar hur stor buffert mottagaren har tilldelat för den här kopplingen.

`Number of Outbound/Inbound Streams` meddelar mottagaren hur många strömmar avsändaren klarar av.

`Initial TSN` är en slumpmässigt vald `uint32` att starta den lokala räknaren på.

`Optional Parameters` gör det möjligt att introducera nya funktioner till SCTP protokollet.


### SACK-avsnitt

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 3    |Chunk  Flags   |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Advertised Receiver Window Credit (a_rwnd)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Number of Gap Ack Blocks = N  |  Number of Duplicate TSNs = X |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Gap Ack Block #1 Start       |   Gap Ack Block #1 End        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Gap Ack Block #N Start      |  Gap Ack Block #N End         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN 1                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN X                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

SACK (Selective Acknowledgment) avsnitt är hur en mottagare meddelar
en avsändare att den har fått ett paket. En avsändare kommer att skicka den aktuella DATA-biten om och om igen tills den får en SACK. En SACK gör mer än bara
uppdatera TSN dock.

`Cumulative TSN ACK` är det högsta TSN som har mottagits.

`Advertised Receiver Window Credit` är mottagarens buffertstorlek för det annonserade mottagarfönstret`. Mottagaren kan ändra detta under sessionen om mer minne blir tillgängligt.

`Ack Blocks` är TSN:er som har tagits emot efter `Cumulative TSN ACK`.
Detta används om det finns ett lucka av levererade paket. Låt oss säga DATA-avsnitt med TSN
`100`,` 102`, `103` och` 104` levereras. `Cumulative TSN ACK` skulle vara `100`, men
`Ack Blocks` kan användas för att meddela avsändaren att den inte behöver skicka `102`, `103` eller `104` igen.

`Duplicate TSN` meddelar avsändaren att den har fått följande DATA-avsnitt mer än en gång.

### HEARTBEAT-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 4    | Chunk  Flags  |      Heartbeat Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/            Heartbeat Information TLV (Variable-Length)        /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

HEARTBEAT-avsnitt används för att kontrollera att mottagaren fortfarande svarar.
Användbart om du inte skickar några DATA-avsnitt, men vill behålla en NAT
mappning öppen.

### ABORT-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 6    |Reserved     |T|           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\               Zero or more Error Causes                       \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Ett ABORT-avsnitt stänger plötsligt av kopplingen. Används när
ena sidan får ett kritiskt fel. För att avsluta på ett snyggare sätt
används SHUTDOWN-avsnitt istället.

### SHUTDOWN-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 7    | Chunk  Flags  |      Length = 8               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

SHUTDOWN-avsnitt startar en kontrollerad avstängning av SCTP-kopplingen.
Varje klient informerar mottagaren om den senaste TSN som den skickade. 
Detta säkerställer att inga paket har tappats. WebRTC gör inte en graciös 
avstängning av själva SCTP-kopplingen. Du måste stänga ner varje datakanal 
själv för att hantera det graciöst.

`Cumulative TSN ACK` är den sista TSN som skickades. Varje sida vet att
den inte ska stänga ner förrän de har fått DATA-avsnittet med denna TSN.

### ERROR-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 9    | Chunk  Flags  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                    One or more Error Causes                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Ett ERROR-avsnitt används för att meddela den andra SCTP klienten
att ett icke-kritiskt fel har inträffat.

### FORWARD TSN-avsnitt
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 192  |  Flags = 0x00 |        Length = Variable      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      New Cumulative TSN                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-1              |       Stream Sequence-1       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               /
/                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-N              |       Stream Sequence-N       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

`FORWARD TSN`-avsnitt flyttar den globala TSN framåt. SCTP gör detta så 
att du kan hoppa över några paket som du inte bryr dig om längre. Låt oss säga
du skickar `10 11 12 13 14 15` och dessa paket endast är giltiga om alla
kommer fram. Den här datan måste komma fram i realtid, så om ett paket anländer
för sent är det inte användbart.

Om du tappar `12` och `13` finns det ingen anledning att skicka `14` och `15`!
SCTP använder `FORWARD TSN`-avsnitt för att göra det. Meddelandet låter mottagaren
veta att paket `14` och `15` inte kommer att skickas längre.

`New Cumulative TSN` är den nya TSN:en för anslutningen. Alla paket
innan detta TSN kommer att slängas.

`Stream` och `Stream Sequence` används för att hoppa `Stream Sequence Number`
antal avsnitt framåt. Gå tillbaka till DATA-avsnitt för betydelsen av detta fält.

## Tillståndsmaskinen för SCTP
Det finns några intressanta delar av SCTPs tillståndsmaskin. WebRTC använder inte alla
funktioner i SCTP-tillståndsmaskinen, så vi har uteslutit vissa delar. Vi har också förenklat vissa komponenter för att göra dem begripliga på egen hand.

### Anslutningsetableringsflöde
`INIT` och `INIT ACK` avsnitt används för att utbyta funktioner och konfigurationer
mellan varje klient. SCTP använder en kaka (cookie) under handskakningen för att validera den kollega den kommunicerar med.
Detta för att säkerställa att handskakningen inte avlyssnas och för att förhindra DoS-attacker.

`INIT ACK` avsnittet innehåller kakan. Kakan returneras sedan till dess skapare
med `COOKIE ECHO`. Om cookieverifiering lyckas skickas ett `COOKIE ACK`
och DATA-avsnitt är redo att börja skickas.

![Uppkoppling](../../images/07-connection-establishment.png "Uppkoppling")

### Anslutning av kopplingen
SCTP använder `SHUTDOWN` avsnittet. När en agent får ett `SHUTDOWN`-avsnitt kommer den att vänta tills den
fått det begärda `Cumulative TSN ACK`. Detta gör det möjligt för en användare att se till att all data
levereras även om anslutningen har hög paketförlust.

### Keep-Alive mekanism
SCTP använder `HEARTBEAT REQUEST` och `HEARTBEAT ACK` avsnitt för att hålla anslutningen vid liv. Dessa meddelanden skickas
på ett konfigurerbart intervall. SCTP använder sig av exponentiell backoff om paketet inte har kommit fram.

`HEARTBEAT`-avsnitt innehåller också ett tidsvärde. Detta gör det möjligt för två kopplingar att beräkna tur-och-retur-tiden mellan två klienter.
