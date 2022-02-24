---
title: Säkerhet
type: docs
weight: 5
---

# Säkerhet

## Säkerhet och WebRTC

Varje WebRTC-anslutning är autentiserad och krypterad. Du kan vara säker på att en tredje part inte kan se vad du skickar eller infoga falska meddelanden. Du kan också vara säker på att WebRTC-agenten som genererade sessionsbeskrivningen är den du kommunicerar med.

Det är mycket viktigt att ingen kan modifiera dina meddelanden. Det är ok om en tredje part läser sessionsbeskrivningen under transport. WebRTC har dock inget skydd mot att det ändras. En angripare kan utföra en man-i-mitten-attack genom att ändra ICE-kandidaterna och uppdatera certifikatets fingeravtryck.

## Hur fungerar det?
WebRTC använder två befintliga protokoll, Datagram Transport Layer Security ([DTLS](https://tools.ietf.org/html/rfc6347)) och Secure Real-time Transport Protocol ([SRTP](https://tools.ietf.org/html/rfc3711)).

Med DTLS kan du sätta upp en session och sedan utbyta data säkert mellan två parter. Det är ett syskon till TLS, samma teknik som används för HTTPS, men DTLS använder UDP istället för TCP som transportlager. Det betyder att protokollet måste hantera tappade paket. SRTP är speciellt utformat för säkert skicka ljud och bild. Det finns några optimeringar vi kan göra genom att använda det protokollet istället för DTLS.

DTLS används först. Det gör en handskakning över anslutningen från ICE. DTLS är ett klient/serverprotokoll, så en sida måste starta handskakningen. Klient/serverroller väljs under uppsättningen. Under DTLS-handskakningen erbjuder båda sidor ett certifikat.
När handskakningen är klar jämförs detta certifikat med certifikat-hashen i sessionsbeskrivningen. Detta för att säkerställa att handskakningen gjorts med den WebRTC-agent du förväntade dig. DTLS-anslutningen kan sen användas för vanlig DataChannel-kommunikation.

För att skapa en SRTP-session initialiserar vi den med hjälp av nycklarna som genereras med DTLS. SRTP har ingen handskakningsmekanism, så vi måste använda nycklar som genererats på något annat sätt. När detta är gjort kan vi skicka media krypterat över SRTP!

## Grundläggande säkerhet
För att förstå tekniken som presenteras i detta kapitel finns det några termer som är bra att känna till. Kryptografi är ett knepigt ämne så det kan vara värt att konsultera andra källor också.

#### Klartext och Kryptotext
Klartext är originaltexten man skickar in till ett chiffer. Kryptotext är resultatet av en chiffer.

#### Kryptering
Ett chiffer är en serie steg som tar vanlig text till kryptotext. Chiffret kan sedan vändas så att du kan ta din kryptotext tillbaka till klartext. Ett chiffer har vanligtvis en nyckel för att ändra sitt beteende. En annan term för detta är kryptering och dekryptering.

Ett enkelt chiffer är ROT13. Varje bokstav flyttas 13 tecken framåt. För att dekryptera chiffret flyttar du 13 tecken bakåt. Den klara texten `HEJSAN` skulle bli krypteringstexten `URWFNA`. I det här fallet är krypteringen ROT och nyckeln är 13.

#### Hashfunktioner
Hash är en enkelriktad funktion som genererar en kontrollsumma. Från samma meddelande genererar den samma kontrollsumma varje gång. Det är viktigt att funktionen *inte* är reversibel. Om du har en kontrollsumma ska du inte kunna lista ut meddelandet som den genererades från. Hashing är användbart när du vill bekräfta att ett meddelande inte har manipulerats.

En enkel hash funktion skulle vara att bara ta varannan bokstav. `HEJSAN` skulle bli `HJA`. Du kan inte anta att `HEJSAN` var ingången, men du kan bekräfta att `HEJSAN` skulle vara en matcha kontrollsumman.

#### Kryptografi för offentlig / privat nyckel
Public/Private Key Cryptography beskriver vilken typ av kod som DTLS och SRTP använder. I det här systemet har du två nycklar, en offentlig och en privat nyckel. Den offentliga nyckeln är för kryptering av meddelanden och är säker att dela.
Den privata nyckeln är för dekryptering och ska aldrig delas. Det är den enda nyckeln som kan dekryptera meddelanden som är krypterade med den offentliga nyckeln.

#### Diffie–Hellmans nyckelöverföring
Diffie–Hellman nyckelöverföring tillåter två användare som aldrig har träffats tidigare att skapa en delad hemlighet säkert över internet. Användaren `A` kan skicka en hemlighet till användaren `B` utan att oroa sig för avlyssning. Detta beror på svårigheten att bryta det diskreta logaritmproblemet.
Du behöver inte helt förstå hur det fungerar, men det är bra att veta att det här är tekniken DTLS-handskakningen är baserad på.

Wikipedia har ett exempel på hur det fungerar [här](https://sv.wikipedia.org/wiki/Diffie-Hellmans_nyckel%C3%B6verf%C3%B6ring).

#### Pseudorandom-funktioner
En Pseudorandom-funktion (PRF) är en fördefinierad funktion för att generera ett värde som verkar slumpmässigt. Det kan ta flera indata och generera en enda utdata.

#### Key Derivation Function
Key Derivation är en typ av pseudorandom-funktion. Key Derivation är en funktion som används för att göra en nyckel starkare. Ett vanligt sätt är nyckelsträckning (key stretching).

Låt oss säga att du får en nyckel som är 8 byte. Du kan använda en KDF för att göra den starkare.

#### Nonce
En nonce är ytterligare indata till ett chiffer. Detta är så att du kan få olika utdata från krypteringen, även om du krypterar samma meddelande flera gånger.

Om du krypterar samma meddelande tio gånger kommer krypteringen att ge dig samma kryptotext 10 gånger. Genom att använda ett nonce kan du få olika indata medan du fortfarande använder samma nyckel. Det är viktigt att du använder ett nytt nonce för varje meddelande! Annars ger det ger det inte någon extra säkerhet.

#### Meddelandeautentiseringskod
En meddelandeautentiseringskod (Message Authentication Code) är en hash som placeras i slutet av ett meddelande. En MAC visar att meddelandet kommer från den användare du förväntade dig.

Om du inte använder en MAC kan en angripare infoga ogiltiga meddelanden. Efter dekryptering skulle du bara ha skräp eftersom de inte vet nyckeln.

#### Nyckelrotation
Nyckelrotation är praxis att byta ut nyckeln med jämna mellanrum. Detta gör att det inte är lika allvarligt att en nyckel blivit stulen. Om en nyckel blir stulen eller har läckt är det mindre data som kan dekrypteras.

## DTLS
DTLS (Datagram Transport Layer Security) tillåter två klienter att etablera säker kommunikation utan någon befintlig konfiguration. Även om någon lyssnar på konversationen kan de inte dekryptera meddelandena.

För att en DTLS-klient och en server ska kunna kommunicera måste de komma överens om ett chiffer och en nyckel. De bestämmer dessa värden genom att göra ett DTLS-handskakning. Under handskakningen är meddelandena i klartext.
När en DTLS-klient och server har utbytt tillräckligt med information för att börja kryptera skickar den en `Change Cipher Spec`. Efter detta meddelande kommer varje efterföljande meddelande att vara krypterat!

### Paketformat
Varje DTLS-paket börjar med en rubrik.

#### Innehållstyp
Du kan förvänta dig följande typer (Content Type):

* `20` - Ändra krypteringsspecifikation (Change Cipher Spec)
* `22` - Handskakning (Handshake)
* `23` - Applikationsdata (Application Data)

`Handskakning` används för att utbyta detaljer för att starta sessionen. `Ändra krypteringsspecifikation` används för att meddela den andra sidan att allt kommer att krypteras. `Applikationsdata` är de krypterade meddelandena.

#### Version
Version kan antingen vara `0x0000feff` (DTLS v1.0) eller `0x0000fefd` (DTLS v1.2) det finns ingen v1.1.

#### Epoch
Epoken börjar vid `0` men blir `1` efter en `Ändra krypteringsspecifikation`. Alla meddelanden med en epok som inte är noll är krypterade.

#### Sekvensnummer
Sekvensnummer används för att hålla meddelanden i ordning. Varje meddelande ökar sekvensnumret. När epoken ökas börjar sekvensnumret om.

#### Längd och data
Datan (Payload) som skickas är specifik för varje "innehållstyp" (`Content Type`). För en `Applikationsdata` är det krypterad data. För `Handskakning` kommer det att vara olika beroende på meddelandet. Längden säger bara hur stor datan är.

### Handskakningens tillstånd
Under handskakningen utbyter klienten och servern en serie meddelanden. Dessa meddelanden grupperas i stegar. Varje stege kan ha flera meddelanden (eller bara ett).
En stege är inte klar förrän alla meddelanden i stegen har tagits emot. Vi kommer att beskriva syftet med varje meddelande mer detaljerat nedan.

![Handskakning](../../images/04-handshake.png "Handskakning")

#### ClientHello
ClientHello är det första meddelandet som skickas av klienten. Den innehåller en lista med attribut. Dessa attribut berättar för servern vilka chiffer och funktioner som klienten stöder. För WebRTC så väljer vi också SRTP-chiffer med ClientHello. Den innehåller också slumpmässig data som kommer att användas för att generera nycklarna för sessionen.

#### HelloVerifyRequest
HelloVerifyRequest skickas av servern till klienten. Det är för att se till att klienten avsåg att skicka begäran. Klienten skickar sedan ClientHello igen, men med ett token den fick från HelloVerifyRequest:et.

#### ServerHello
ServerHello är svaret från servern för konfigurationen av sessionen. Den innehåller vilket chiffer som ska användas när den här sessionen är klar. Den innehåller också serverns slumpmässiga data.

#### Certifikat
Certifikatet (Certificate) innehåller certifikatet för klienten eller servern. Detta används för att unikt identifiera vem vi kommunicerade med. Efter att handskakningen är över ser vi till att detta certifikat när det hashas matchar fingeravtrycket i `SessionDescription`.

#### ServerKeyExchange/ClientKeyExchange
Dessa meddelanden används för att överföra den offentliga nyckeln. Vid start genererar klienten och servern båda ett knappsats. Efter handskakningen kommer dessa värden att användas för att generera en `Pre-Master Secret`.

#### CertificateRequest
En CertificateRequest skickas av servern som meddelar klienten att den vill ha ett certifikat. Servern kan antingen begära eller kräva ett certifikat.

#### ServerHelloDone
ServerHelloDone meddelar klienten att servern är klar med handskakningen.

#### CertificateVerify
CertificateVerify är hur avsändaren visar att den har den privata nyckeln som skickas i certifikatmeddelandet.

#### ChangeCipherSpec
ChangeCipherSpec informerar mottagaren om att allt som skickas efter detta meddelande kommer att krypteras.

#### Färdiga
Färdig (Finished) är krypterat och innehåller en hash av alla skickade meddelanden. Det används för att verifiera att handskakningen inte har blivit manipulerad.

### Nyckelgenerering
När handskakningen är klar kan du börja skicka krypterad data. Chiffret valdes av servern och finns i ServerHello. Men hur valdes nyckeln?

Först genererar vi en `Pre-Master Secret`. För att göra det värde används Diffie–Hellman på nycklarna som byts via `ServerKeyExchange` och `ClientKeyExchange`. Detaljerna varierar beroende på vilket chiffer vi valt.

Därefter genereras en `Master Secret`. Varje version av DTLS har en egen pseudorandom-funktion. För DTLS 1.2 tar funktionen `Pre-Master Secret` och slumpvärdena i `ClientHello` och `ServerHello`.
Resultatet från att köra pseudorandom-funktionen är vår `Master Secret` som används för chiffret.

### Utbyta applikationsdata
Arbetshästen för DTLS är `ApplicationData`. Nu när vi har ett initialiserat chiffer kan vi börja kryptera och skicka data.

Meddelanden med `applikationsdata` använder den DTLS-header vi beskrev tidigare. Datan är skickas som krypterad text. Du har nu en fungerande DTLS-session och kan kommunicera säkert.

DTLS har många fler intressanta funktioner som till exempel omförhandling (renegotiation). Men eftersom de inte används i WebRTC hoppar vi över det.

## SRTP
SRTP är ett protokoll utformat speciellt för kryptering av RTP-paket. För att starta en SRTP-session anger du dina nycklar och chiffer. Till skillnad från DTLS har den ingen handskakningsmekanism. All konfiguration och nycklar genererades under DTLS-handskakningen.

DTLS tillhandahåller ett dedikerat API för att exportera nycklarna som ska användas av en annan process. Detta definieras i [RFC 5705](https://tools.ietf.org/html/rfc5705).

### Sessionsskapande
SRTP definierar en Key Derivation-funktion som används på indatat. När du skapar en SRTP-session skickas indatat genom funktionen för att generera nycklar för vår SRTP-kryptering. Efter detta kan du gå vidare till att skicka ljud och bild.

### Utbyta media
Varje RTP-paket har ett 16-bitars sekvensnummer. Dessa sekvensnummer används för att hålla ordning på paket, som en primär nyckel. Under ett samtal kommer numret bli för stort och "rulla över". SRTP håller reda på det och kallar detta för övergångsräknare (rollover counter).

Vid kryptering av ett paket använder SRTP övergångsräknaren och sekvensnumret som ett nonce. Detta för att säkerställa att även om du skickar samma data två gånger kommer krypteringstexten att vara annorlunda. Detta är viktigt för att förhindra att en angripare identifierar mönster eller försöker en uppspelningsattack (replay attack).
