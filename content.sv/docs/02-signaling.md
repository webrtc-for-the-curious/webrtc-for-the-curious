---
title: Signalering
type: docs
weight: 3
---

# Signalering

## Vad är WebRTC-signalering?

När du skapar en WebRTC-agent vet den ingenting om den andra parten. Den har ingen aning om vem den kommer att ansluta till eller vad för data de ska skicka!
Signalering är den första konfigureringen som gör ett samtal möjligt. Efter att dessa värden har utbytts kan WebRTC-agenterna kommunicera direkt med varandra.

Signalmeddelanden är bara vanlig text och WebRTC-agenterna bryr sig inte hur de skickas. De utbyts vanligtvis via Websockets, men det är inte ett krav.

## Hur fungerar WebRTC-signalering?

WebRTC använder ett befintligt protokoll som kallas Session Description Protocol. Via detta protokoll delar de två WebRTC-agenterna alla tillstånd som krävs för att upprätta en anslutning. Protokollet i sig är enkelt att läsa och förstå.
Komplexiteten kommer när man försöker förstå alla värden som WebRTC fyller i åt dig.

SDP protokollet är inte skapat specifikt för WebRTC. Eftersom WebRTC bara utnyttjar en liten del av protokollet ska vi bara gå igenom det vi behöver.
När vi förstår protokollet kommer vi att gå vidare till hur det används i WebRTC.

## Vad är *Session Description Protocol* (SDP)?
Sessionsbeskrivningsprotokollet definieras i [RFC 8866](https://tools.ietf.org/html/rfc8866). Det är ett nyckel/värde-protokoll med en ny rad efter varje värde, ungefär som en INI-fil.
En sessionsbeskrivning (Session Description) innehåller noll eller fler mediebeskrivningar (Media Descriptions). Mentalt kan du se det som att en sessionsbeskrivning innehåller en uppsättning mediebeskrivningar.

En mediebeskrivning beskriver vanligtvis en enda ström av media. Så om du ville beskriva ett samtal med tre videoströmmar och två ljudspår skulle du ha fem mediebeskrivningar.

### Hur man läser SDP
Varje rad i en sessionsbeskrivning börjar med ett enda tecken, det här är din nyckel. Det kommer sedan att följas av ett likhetstecken. Allt efter det lika tecknet är värdet. När värdet är klart kommer du att ha en ny rad.

Session Description Protocol definierar alla nycklar som är giltiga. Du kan bara använda bokstäver för nycklar enligt definitionen i protokollet. Dessa nycklar har alla betydande betydelse, vilket kommer att förklaras senare.

Här är ett exempel på en del av en sessionsbeskrivning:

```
a=my-sdp-value
a=second-value
```

Du har två rader. Var och en med nyckeln `a`. Den första raden har värdet `my-sdp-value`, den andra raden har värdet `second-value`.

### WebRTC använder bara vissa SDP-nycklar
Inte alla nycklar som definieras i SDP används av WebRTC. Bara nycklar som används i JavaScript Session Establishment Protocol (JSEP), definierat i [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829), är viktiga. Följande sju nycklar är de enda du behöver förstå just nu:

* `v` - Version, ska vara satt till `0`.
* `o` - Ursprung (Origin). Innehåller ett unikt ID som är användbart för omförhandlingar.
* `s` - Sessionsnamn, ska vara satt till `-`.
* `t` - Timing, ska vara satt till `0 0`.
* `m` - Mediebeskrivning (`m=<media> <port> <proto> <fmt> ... `), beskriven i detalj nedan.
* `a` - Attribut, ett fritextfält. Detta är den vanligaste raden i WebRTC.
* `c` - Anslutningsdata bör vara satt till `IN IP4 0.0.0.0`.

### Mediebeskrivningar i en sessionsbeskrivning

En sessionsbeskrivning kan innehålla ett obegränsat antal mediebeskrivningar.

Varje mediabeskrivning kan innehålla en lista med olika format. Dessa format kopplas till RTP Payload Types. Den faktiska kodeken definieras sedan av ett attribut med värdet `rtpmap` i mediabeskrivningen.
Vikten av RTP och RTP Payload Types diskuteras senare i kapitlet om Media. Varje mediebeskrivning kan innehålla ett obegränsat antal attribut.

Ta den här delen av en sessionsbeskrivning som ett exempel:

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

Du har två medibeskrivningar, en av typ ljud med fmt `111` och en av typ video med formatet `96`. Den första mediebeskrivningen har bara ett attribut. Detta attribut specificerar att Payload Type är `111` för Opus.
Den andra mediebeskrivningen har två attribut. Det första attributet specificerar Payload Type är `96` för VP8, och det andra attributet är helt enkelt bara `my-sdp-value`.

### Ett komplett exempel

Följande exempel innehåller alla begrepp som vi har pratat om. Det här är alla funktioner i SDP som WebRTC använder.
Om du kan läsa och förstå detta, kan du läsa vilken WebRTC-session som helst!

```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 127.0.0.1
t=0 0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4002 RTP/AVP 96
a=rtpmap:96 VP8/90000
```

* `v`, `o`, `s`, `c`, `t` är definierade, men de påverkar inte WebRTC-sessionen.
* Du har två mediebeskrivningar. En av typen `audio` (ljud) och en av typen `video`.
* Var och en av dessa har ett attribut. Detta attribut konfigurerar detaljer om RTP-pipelinen, vilket diskuteras i kapitlet "Mediekommunikation".

## Hur *Session Description Protocol* och WebRTC fungerar tillsammans

Nästa pusselbit är att förstå _hur_ WebRTC använder Session Description protokollet.

### Vad är erbjudanden och svar?

WebRTC använder en erbjudande/svar-modell. Det betyder att den ena WebRTC-agenten gör ett "erbjudande" ("Offer") för att starta ett samtal, och den andra WebRTC-agenten ger ett "svar" ("Answer") om den är villig att acceptera det som erbjudits.

Detta ger svararen en chans att säga nej till kodeks i media-beskrivningarna (Media Descriptions). Det här är sättet två parter kommer överens om vilka format de är villiga att utbyta.

### Transceivers är avsedda för sändning och mottagning

Transceivers är ett WebRTC-specifikt koncept som du kommer att se i API:et. Vad den gör är att exponera "Media Description" för JavaScript API. Varje mediebeskrivning blir en sändtagare.
Varje gång du skapar en Transceiver läggs en ny mediebeskrivning till den lokala sessionsbeskrivningen.

Varje mediebeskrivning i WebRTC har ett riktningsattribut (direction attribute). Detta gör det möjligt för en WebRTC-agent att förklara "Jag ska skicka dig denna codec, men jag är inte villig att acceptera något tillbaka". Det finns fyra giltiga värden:

* `send`
* `recv`
* `sendrecv`
* `inactive`

### SDP-värden som används av WebRTC

Nedan är en lista över några vanliga attribut som du kommer att se i en sessionsbeskrivning från en WebRTC-agent. Många av dessa värden styr delsystem som vi ännu inte har diskuterat.

#### `group:BUNDLE`
Bundling är när man kör flera typer av trafik över en och samma anslutning. Vissa WebRTC-implementeringar använder en dedikerad anslutning per mediaström. Buntning är att föredra.

#### `fingerprint:sha-256`
Detta är en hash av certifikatet som en part använder för DTLS. När DTLS-handskakningen är klar jämför du detta med det faktiska certifikatet för att bekräfta att du kommunicerar med den du har förväntat dig.

#### `setup:`
Detta kontrollerar beteendet för DTLS-agenten. Detta avgör om det körs som en klient eller server efter att ICE har anslutit. De möjliga värdena är:

* `setup:active`  - Kör som DTLS-klient.
* `setup:passive` - Kör som DTLS-server.
* `setup:actpass` - Be den andra WebRTC-agenten att välja.

#### `mid`
Attributet "mid" används för att identifiera mediaströmmar i en sessionsbeskrivning.

#### `ice-ufrag`
Detta är användarfragmentvärdet för ICE-agenten. Används för verifiering av ICE trafik.

#### `ice-pwd`
Detta är lösenordet för ICE-agenten. Används för autentisering av ICE trafik.

#### `rtpmap`
Detta värde används för att koppla en specifik kodek till en RTP Payload Type. Payload Types är inte statiska, så för varje samtal bestämmer avsändaren typen för varje kodek.

#### `fmtp`
Definierar ytterligare värden för en Payload Type. Detta är användbart för att kommunicera en viss videoprofil eller kodekinställning.

#### `candidate`
Detta är en ICE-kandidat som kommer från ICE-agenten. Det här är en möjlig adress som WebRTC-agenten är tillgänglig på. Dessa förklaras i mer detalj i nästa kapitel.

#### `ssrc`
En synkroniseringskälla (SSRC) definierar ett enda mediaströmspår.

`label` är ID:t för den individuella strömmen. `mslabel` är ID:t för en container som kan innehålla flera strömmar.

### Exempel på en WebRTC-sessionsbeskrivning
Följande är en fullständig sessionsbeskrivning genererad av en WebRTC-klient:

```
v=0
o=- 3546004397921447048 1596742744 IN IP4 0.0.0.0
s=-
t=0 0
a=fingerprint:sha-256 0F:74:31:25:CB:A2:13:EC:28:6F:6D:2C:61:FF:5D:C2:BC:B9:DB:3D:98:14:8D:1A:BB:EA:33:0C:A4:60:A8:8E
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=setup:active
a=mid:0
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ssrc:350842737 cname:yvKPspsHcYcwGFTw
a=ssrc:350842737 msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=ssrc:350842737 mslabel:yvKPspsHcYcwGFTw
a=ssrc:350842737 label:DfQnKjQQuwceLFdV
a=msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=setup:active
a=mid:1
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=ssrc:2180035812 cname:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=ssrc:2180035812 mslabel:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 label:JgtwEhBWNEiOnhuW
a=msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=sendrecv
```

Det här är vad vi får reda på från det här meddelandet:

* Vi har två mediasektioner, en för ljud och en för video.
* Båda är `sendrecv` transceiver. Vi får två strömmar och vi kan skicka tillbaka två.
* Vi har ICE-kandidater och autentiseringsdetaljer, så vi kan försöka ansluta.
* Vi har ett certifikatfingeravtryck, så vi kan ha ett säkert samtal.

### Ytterligare ämnen
I senare versioner av denna bok kommer även följande ämnen att behandlas:

* Renegotiation
* Simulcast
