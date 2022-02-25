---
title: Felsökning
type: docs
weight: 10
---

# Felsökning
Felsökning av WebRTC kan vara en trixig uppgift. Det finns många rörliga delar, och de kan alla gå sönder oberoende av varandra. Om du inte är försiktig kan du förlora veckor på att kolla på fel saker. När du äntligen hittar den del som är trasig måste du lära dig mer för att förstå varför.

Detta kapitel kommer att få dig att tänka på rätt sätt för att felsöka WebRTC. Det kommer att visa dig hur du bryter ner problemet. När vi känner till problemet ger vi en snabb översikt av de mest populära felsökningsverktygen.

## Isolera problemet
När du felsöker måste du isolera var problemet kommer ifrån. Börja från början av...

### Signalfel
TODO!

### Nätverksfel

Testa din STUN-server med netcat:

1. Förbered ett **20-byte** bindningsförfråganspaket:

    ```
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    ```

   Förklaring:
    - `00 01` är meddelandetypen.
    - `00 00` är längden på datan.
    - `21 12 a4 42` är den magiska kakan.
    - och `54 45 53 54 54 45 53 54 54 45 53 54` (I ASCII: `TESTTESTTEST`) är ett 12-byte långt transaktions-ID.

2. Skicka meddelandet och vänta på det **32 byte** stora svaret:

    ```
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    ```

   Förklaring:
    - `01 01` är meddelandetypen.
    - `00 0c` är längden på datan, i det hör fallet 12 i decimaltal.
    - `21 12 a4 42` är den magiska kakan.
    - och `54 45 53 54 54 45 53 54 54 45 53 54` (I ASCII: `TESTTESTTEST`) är ett 12-bitars transaktions-ID
    - `00 20 00 08 00 01 6f 32 7f 36 de 89` de 12-bitarna med data, som översatt blir:
        - `00 20` är typen: `XOR-MAPPED-ADDRESS`.
        - `00 08` är längden på värdet, i det här fallet 8 bytes
        - `00 01 6f 32 7f 36 de 89` är själva värdet, som översatt blir:
            - `00 01` adresstyp (IPv4)
            - `6f 32` den XOR-mappade porten
            - `7f 36 de 89` den XOR-mappede IP-adressen

Avkodning av det XOR-mappade avsnittet är lite krångligt, men vi kan lura stun-servern att utföra en dummy-XOR-mappning genom att skicka en (ogiltig) dummy-magisk cookie inställd på `00 00 00 00`:

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

XOR på en magiska kakan med bara nollor ändrar inget, så porten och adressen kommer att vara i klartext i svaret. Detta fungerar inte alltid, eftersom vissa routrar manipulerar de passerande paketen, fusk på IP-adressen. Om vi tittar på det returnerade värdet (senaste åtta byten):

  - `00 01 4e 20 5e 24 7a cb` data värdet, som översatt blir:
    - `00 01` adresstyp (IPv4)
    - `4e 20` portwn, i det hör fallet 20000 i decimal tal.
    - `5e 24 7a cb` är IP adressen, `94.36.122.203` i mer lättläst form.

### Säkerhetsfel

### Mediefel

### Datafel

## Praktiska verktyg

### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) är ett nätverksverktyg för kommandoraden som kan läsa och skriva till nätverksanslutningar via TCP eller UDP. Det är vanligtvis tillgängligt som kommandot `nc`.

### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) är ett datanätverkspaketanalysverktyg för kommandoraden.

Vanliga kommandon:
- Fånga UDP-paket till och från port 19302, skriv ut en hexdump av paketinnehållet:

  `sudo tcpdump 'udp port 19302' -xx`

- Samma, men spara istället paketen i en PCAP-fil (packet capture) för senare inspektion:

  `sudo tcpdump 'udp port 19302' -w stun.pcap`

  PCAP-filen kan öppnas med Wireshark-applikationen: `wireshark stun.pcap`

### wireshark

### webrtc-internals

Chrome har en inbyggd WebRTC-statistiksida som du hittar på [chrome://webrtc-internals](chrome://webrtc-internals).

## Latens
Hur vet du om du har hög latens? Du kanske har märkt att din video släpar efter, men vet du exakt hur mycket efter den är?
För att kunna minska latensen måste du börja med att mäta den först.

Sann latens ska mätas hela vägen. Det betyder inte bara latensen för nätverket mellan avsändaren och mottagaren, utan den kombinerade latensen för kamera, kodande av video, överföring, mottagning, avkodning och visning, samt eventuell a köer mellan dessa steg.

Total latens kan inte beräknas som en summa av latensen för varje komponent.

Även om du teoretiskt kan mäta latensen för alla komponenter i en live videoöverföring separat och sedan lägga hop dem, i praktiken kommer åtminstone vissa komponenter antingen att vara oåtkomliga för instrumentering eller ge ett helt annat resultat när de mäts utanför överföringen.
Olika buffrings-effekter mellan steg i video pipelinen, nätverkstopologi och automatiska kamera justeringar är bara några exempel på komponenter som påverkar den faktiska latensen.

Den inneboende latensen för varje komponent i ditt livesändningssystem kan förändras och påverka nedströms komponenter.
Även innehållet i den inspelade videon påverkar latensen.
Till exempel krävs många fler bitar för komplexa bilder såsom trädgrenar, jämfört med en klarblå himmel som innehåller mycket mindre information.
En kamera med automatisk exponering aktiverad kan ta _mycket_ längre tid än de förväntade 33 millisekunderna för att ta en bild, även om inspelningshastigheten är inställd på 30 bilder per sekund.
Överföring över nätverket, särskilt mobila nät, ändras också ofta på grund av förändrad efterfrågan och kapacitet.
Fler användare introducerar mer störningar i luften.
Din fysiska plats (områden med dålig täckning) och flera andra faktorer ökar paketförlust och latens.
Vad händer när du skickar ett paket till ett nätverksinterface, till exempel en WiFi-adapter eller ett LTE-modem?
Om paketet inte kan skickas omedelbart köas det upp, ju längre kö desto mer latens introducerar ett sådant nätverksinterface.

### Manuell mätning från start till slut
När vi pratar om start-till-slut-latens menar vi tiden mellan en händelse som inträffar och när den observeras, det vill säga att bilden visas på skärmen.

```
EndToEndLatency = T(observe) - T(happen)
```

Ett naivt tillvägagångssätt är att mäta tiden när en viss händelse sker och subtrahera den från tiden vid när man kan se videon av händelsen.
Men när precisionen är nere på millisekunder blir tidssynkronisering ett problem.
Att försöka synkronisera klockor över distribuerade system är oftast meningslöst, även ett litet fel i tidssynkronisering ger opålitliga mätningar.

En enkel lösning på klocksynkroniseringsproblemet är att använda samma klocka, att
placera sändare och mottagare i samma referensram.

Tänk dig att du verkligen har en tickande millisekund-klocka eller någon annan händelsekälla.
Du vill mäta latens i ett system som live streamar klockan till en skärm genom att peka en kamera mot den.
Ett uppenbart sätt att mäta tiden mellan att millisekundtimern tickar (T<sub>`happen`</sub>) och klockans bild visas på skärmen (T<sub>`observe`</sub>) är följande:
- Rikta kameran mot klockan.
- Skicka videon till en mottagare som är på samma fysiska plats.
- Ta en bild (använd din telefon) av klockan och den mottagna videon på skärmen.
- Subtrahera två gånger.

Det är den mest riktiga mätningen för start-till-slut-latens.
Den innehåller alla komponenters latens (kamera, kodek, nätverk, avkodare) och är inte beroende av någon klocksynkronisering.

![DIY Latency](../../images/09-diy-latency.png "DIY Latency Measurement").
![DIY Latency Example](../../images/09-diy-latency-happen-observe.png "DIY Latency Measurement Example")
På bilden ovan är uppmätta start-till-slut-latensen 101 ms. Tiden som syns just nu är 10:16:02.862, men observatören av live-streaming-systemet ser 10:16:02.761.

### Automatisk start-till-slut-mätning
I skrivande stund (maj 2021) [diskuteras](https://github.com/w3c/webrtc-stats/issues/537) WebRTC-standarden för start-till-slut-latens aktivt.
Firefox implementerade en uppsättning API:er för att låta användare skapa automatisk latensmätning över standard WebRTC API:et.
Men i det här kapitlet diskuterar vi det mest kompatibla sättet att automatiskt mäta latens.

![NTP Style Latency Measurement](../images/09-ntp-latency.png "NTP Style Latency Measurement")

Tur-och-returtid i ett nötskal: Jag skickar dig min tid `tR1`, när jag får tillbaka min `tR1` vid tiden `tR2` vet jag att tur-och-returtiden är `tR2 - tR1`.

Tänk dig att du har en kommunikationskanal mellan sändare och mottagare (t.ex. en [DataChannel](https://webrtc.org/getting-started/data-channels). Då kan mottagaren modellera avsändarens monotona klocka genom att följa nedanstående steg:
1. Vid tidpunkten `tR1` skickar mottagaren ett meddelande med sin lokala klocktid.
2. När den tas emot av sändaren med lokal tid `tS1`, svarar sändaren med en kopia av `tR1` samt sändarens `tS1` och sändarens video-tid `tSV1`.
3. Vid tidpunkten `tR2` hos mottagaren beräknas tur-och-retur-tiden genom att subtrahera meddelandets sändnings- och mottagningstider: `RTT = tR2 - tR1`.
4. Tur-och-retur-tid (`RTT`) tillsammans med avsändarens lokala tid `tS1` är tillräckligt för att göra en uppskattning av avsändarens monotona klocka. Den aktuella tiden hos avsändaren vid tiden `tR2` bör vara lika med `tS1` plus hälften av tur-och-retur-tiden.
5. Avsändarens lokala klocka `tS1` tillsammans med videospårets tidsstämpel `tSV1` och tur-och-retur-tiden `RTT` räcker därför för att synkronisera mottagarens video med avsändarens video.

Nu när vi vet hur mycket tid som har gått sedan senaste video-bilden (`tSV1`), kan vi göra en ungefärlig uppskattning av latensen genom att dra bort klockstämpeln hos video-bilden som visas just nu från den uppskattade tiden:

```
expected_video_time = tSV1 + time_since(tSV1)
latency = expected_video_time - actual_video_time
```

Metodens nackdel är att den inte inkluderar själva kamerans latens.
De flesta videosystem anser att tidsstämpeln för bildtagning är den tid då kameran skickat bilden till minnet, vilket kommer att vara några ögonblick efter att själva kamera sensorn tog emot bilden.

#### Exempel på latensuppskattning
I exemplet nedan öppnas en datakanal kallad `latency` hos mottagaren, som periodiskt skickar tidsstämplar till sändaren. Sändaren svarar tillbaka med ett JSON-meddelande.
Mottagaren beräknar latensen baserat på det meddelandet.

```json
{
    "received_time": 64714,       // Timestamp sent by receiver, sender reflects the timestamp. 
    "delay_since_received": 46,   // Time elapsed since last `received_time` received on sender.
    "local_clock": 1597366470336, // The sender's current monotonic clock time.
    "track_times_msec": {
        "myvideo_track1": [
            13100,        // Video frame RTP timestamp (in milliseconds).
            1597366470289 // Video frame monotonic clock timestamp.
        ]
    }
}
```

Öppna en data-kanal hos mottagaren:
```javascript
dataChannel = peerConnection.createDataChannel('latency');
```

Skicka mottagarens tid `tR1` med jämna mellanrum. Valet av 2 sekunder har ingen specifik betydelse:
```javascript
setInterval(() => {
    let tR1 = Math.trunc(performance.now());
    dataChannel.send("" + tR1);
}, 2000);
```

Hantera inkommande meddelanden från mottagaren hos sändaren:
```javascript
// Assuming event.data is a string like "1234567".
tR1 = event.data
now = Math.trunc(performance.now());
tSV1 = 42000; // Current frame RTP timestamp converted to millisecond timescale.
tS1 = 1597366470289; // Current frame monotonic clock timestamp.
msg = {
    "received_time": tR1,
    "delay_since_received": 0,
    "local_clock": now,
    "track_times_msec": {
        "myvideo_track1": [tSV1, tS1]
    }
}
dataChannel.send(JSON.stringify(msg));
```

Hantera inkommande meddelande från sändaren och visa den beräknade latensen i konsolen:
```javascript
let tR2 = performance.now();
let fromSender = JSON.parse(event.data);
let tR1 = fromSender['received_time'];
let delay = fromSender['delay_since_received']; // How much time that has passed between the sender receiving and sending the response.
let senderTimeFromResponse = fromSender['local_clock'];
let rtt = tR2 - delay - tR1;
let networkLatency = rtt / 2;
let senderTime = (senderTimeFromResponse + delay + networkLatency);
VIDEO.requestVideoFrameCallback((now, framemeta) => {
    // Estimate current time of the sender.
    let delaySinceVideoCallbackRequested = now - tR2;
    senderTime += delaySinceVideoCallbackRequested;
    let [tSV1, tS1] = Object.entries(fromSender['track_times_msec'])[0][1]
    let timeSinceLastKnownFrame = senderTime - tS1;
    let expectedVideoTimeMsec = tSV1 + timeSinceLastKnownFrame;
    let actualVideoTimeMsec = Math.trunc(framemeta.rtpTimestamp / 90); // Convert RTP timebase (90000) to millisecond timebase.
    let latency = expectedVideoTimeMsec - actualVideoTimeMsec;
    console.log('latency', latency, 'msec');
});
```

#### Actual video time in browser
> `<video>.requestVideoFrameCallback()` tillåter webbutvecklare att få ett meddelande när en bild har är tillgänglig att visas.

Fram till mycket nyligen (maj 2020), var det nästan omöjligt att på ett tillförlitligt sätt få en tidsstämpel för den visade bilden i en webbläsare. Lösningar baserade på `video.currentTime` fanns, men de var inte särskilt exakta.
Utvecklare från både Chrome och Mozilla [stödde](https://github.com/mozilla/standards-positions/issues/250) införandet av en ny W3C-standard, [`HTMLVideoElement.requestVideoFrameCallback()`](https://wicg.github.io/video-rvfc/), som lägger till ett nytt API för att komma åt den aktuella bildens tidsstämpel.
Även om tillägget låter trivialt, har det möjliggjort flera avancerade medieapplikationer via nätet som kräver ljud- och videosynkronisering.
För WebRTC inkluderar API:et fältet `rtpTimestamp` i meddelandet, RTP-tidsstämpeln associerad med den aktuella bilden.
Detta fält finns bara för WebRTC-applikationer, annars saknas det.

### Tips för att felsöka latensproblem
Eftersom felsökning sannolikt kommer att påverka den uppmätta latensen är den allmänna regeln att förenkla dit system till minsta möjliga som fortfarande kan reproducera problemet.
Ju fler komponenter du kan ta bort, desto lättare blir det att ta reda på vilken komponent som orsakar latensproblemet.

#### Kameralatens
Beroende på kamerainställningar kan kamerans latens variera.
Kontrollera inställningar för automatisk exponering, autofokus och automatisk vitbalans.
Alla "auto"-funktionerna på webbkameror tar lite extra tid för att analysera den tagna bilden innan den är tillgänglig för WebRTC-stacken.

Om du kör Linux kan du använda kommandoradsverktyget `v4l2-ctl` för att ändra kamerainställningarna:
```bash
# Stäng av autofocus:
v4l2-ctl -d /dev/video0 -c focus_auto=0
# Sätt fokus till max:
v4l2-ctl -d /dev/video0 -c focus_absolute=0
```

Du kan också använda det grafiska verktyget `guvcview` för att kontrollera och justera kamerainställningarna.

#### Kodarens latens
De flesta moderna kodare kommer att buffra ett antal bilder innan de kodas.
Deras högsta prioritet är att hitta en balans mellan kvaliteten på den producerade bilden och hur mycket data varje bild använder (bitrate).
Multipass-kodning är ett extremt exempel där kodaren helt bortser från latensen.
Under det första passet tar den in hela videon och först därefter börjar utmatning av bilder.

Men med rätt inställningar är det möjligt att nå latens lägre än den önskade bildfrekvensen.
Se till att din kodare inte använder för många I-bilder eller förlitar dig på B-bilder.
Varje codecs inställningar för latensinställning är olika, men för x264 rekommenderar vi att du använder `tune=zerolatency` och `profile=baseline` för få så låg latens som möjligt.

#### Nätverksfördröjning
Nätverksfördröjningar är nog det kan göra minst åt, förutom att uppgradera till en bättre internetanslutning.
Nätverksfördröjningar är ungefär som vädret - du kan inte stoppa regnet, men du kan kolla prognosen och ta med ett paraply.
WebRTC mäter nätverksförhållanden med millisekundprecision.
Viktiga mätvärden är:
- Tur-och-returtid
- Paketförlust och omskickande av paket.

**Tur-och-returtid**

WebRTC-stacken har en inbyggd [nätverksmätningsmekanism](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats-roundtriptime) för tur-och-returtid.
En tillräckligt bra uppskattning av latens är hälften av RTT. Det förutsätter att det tar samma tid att skicka och ta emot ett paket, vilket inte alltid är fallet.
Tur-och-returtid sätter den lägre gränsen för start-till-slut-latens.
Dina bilder når inte mottagaren snabbare än `RTT/2`, oavsett hur snabbt din kamera skickar bilder till kodaren.

Den inbyggda RTT-mekanismen är baserad på speciella RTCP-paket som kallas avsändar-/mottagarrapporter.
Avsändaren skickar sin tidsavläsning till mottagaren, mottagaren återspeglar i sin tur samma tidsstämpel till avsändaren.
Därmed vet avsändaren hur mycket tid det tog för paketet att skickas till mottagaren och tillbaka.
Se kapitlet [Avsändar-/mottagarrapporter](../06-media-communication/#senderreceiver-reports) för mer information om RTT-mätning.

**Paketförlust och omskickande av paket**

Både RTP och RTCP är protokoll baserade på UDP som inte har någon garanti för varken ordning, leverans eller duplicering.
Allt ovanstående fall dyker upp när du använder WebRTC-applikationer.
En osofistikerad avkodarimplementering förväntar sig att alla paket i en bild ska levereras för att avkodaren ska sätta ihop bilden igen.
Vid paketförlust kan avkodningsartefakter uppstå om paket med en [P-bild](../06-media-communication/#inter-frame-types) går förlorade.
Om en I-bild-paket tappas får alla följande bilder antingen grava artefakter, eller kommer inte att avkodas och visas alls.
Mest troligt kommer detta att få videon att "frysa" för ett ögonblick.

För att undvika (åtminstone försöka undvika) att videon fryser eller är full av avkodningsartefakter använder WebRTC negativa bekräftelsemeddelanden ([NACK](../06-media-communication/#negative-acknowledgment)).
När mottagaren inte får ett förväntat RTP-paket returnerar det ett NACK-meddelande för att be avsändaren att skicka det saknade paketet igen.
Mottagaren _väntar_ på omskickandet av paketet.
Sådana omskickningar orsakar givetvis ökad latens.
Antalet skickade och mottagna NACK-paket registreras i WebRTCs inbyggda statistikfält [outbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-nackcount) och [inbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-nackcount).

Du kan se fina diagram över inkommande och utgående `nackCount` på [webrtc internals sidan](#webrtc-internals).
Om du ser att `nackCount` ökar, betyder det att nätverket upplever höga paketförluster, och WebRTC-stacken gör sitt bästa för att skapa en smidig video och ljudupplevelse trots det.

När paketförlusten är så hög att avkodaren inte kan producera en bild eller efterföljande beroende bilder, som i fallet med en helt förlorad I-bild, kommer alla framtida P-bilder inte att avkodas.
Mottagaren kommer att försöka mildra det genom att skicka ett speciellt bildförlustindikationsmeddelande (Picture Loss Indication message, [PLI](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)).
När sändaren får ett `PLI` meddelande kommer den att skicka en ny I-bild för att hjälpa mottagarens avkodare.
I-bilder är normalt större än P-bilder, så det ökar mängden data som behöver sändas.
Precis som med NACK-meddelanden måste mottagaren vänta på den nya I-bilden vilket ökar latensen ytterligare.

Kolla efter `pliCount` på [webrtc internals sidan](#webrtc-internals). Om den ökar, justera din kodare så att den skickar mindre data, eller producerar paket med mer redundans.

#### Latens på mottagarsidan
Latens kommer att påverkas av paket som kommer fram i fel ordning.
Om den nedre halvan av en bild kommer före toppen måste du vänta på toppen innan du kan avkoda den.
Detta förklaras mer noggrant i kapitlet [Solving Jitter](../05-real-time-networking/#solving-jitter).

Du kan också hänvisa till det inbyggda [jitterBufferDelay](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) mätningen för att se hur länge en bild hölls i mottagningsbufferten i väntan på alla paket, innan den skickades vidare till avkodaren.
