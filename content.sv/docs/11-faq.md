---
title: FAQ
type: docs
weight: 12
---

# FAQ

{{<details "Varför använder WebRTC UDP?">}}
NAT Traversal kräver UDP. Utan att NAT Traversal är det inte möjligt att sätta upp en P2P-anslutning. UDP har inte "garanterad leverans" som TCP, så WebRTC sköter det på
applikationsnivån istället.

Se [Connecting]({{< ref "03-connecting" >}}) för mer info.
{{</details>}}

{{<details "Hut många DataChannels kan jag ha?">}}
65534 kanaler, eftersom strömidentifieraren har 16 bitar. Du kan när som helst stänga eller öppna nya kanaler.
{{</details>}}

{{<details "Begränsar WebRTC bandbreden på något sätt?">}}
Både DataChannels och RTP använder trängselskontroll. Detta innebär att WebRTC aktivt mäter 
din bandbredd och försöker använda den optimala mängden. Det är en balansgång att skicka så mycket data som möjligt
utan att överväldiga anslutningen.
{{</details>}}

{{<details "Kan jag skicka binär data?">}}
Ja, du kan skicka både text och binär data över DataChannels.
{{</details>}}

{{<details "Vilken latens kan jag förvänta mig från WebRTC?">}}
För icke-optimerad media kan du förvänta dig under 500 millisekunder. Om du tar dig tid att optimera videon eller kan tumma lite på kvalitèten
och istället optimera för latens, har utvecklare fått ner den under 100 ms.

DataChannels har alternativet "partiell tillförlitlighet", vilket kan minska latens orsakad av
tappade paket. Om det har konfigurerats korrekt har det visat sig vara snabbare än TCP TLS-anslutningar.
{{</details>}}

{{<details "Varför skulle jag vilja ignorera paketordningen i DataChannels?">}}
När nyare information gör den gamla värdelös, till exempel positionsinformation för ett
objekt, eller när varje meddelande är helt oberoende av de andra och vi vill undvika
head-of-line blockering.
{{</details>}}

{{<details "Kan jag skicka ljud eller video över en DataChannel?">}}
Ja, du kan skicka vilken data som helst via en DataChannel. I webbläsarfallet är det då ditt
ansvar att avkoda data och skicka dem till en mediaspelare för uppspelning, medans allt
det görs automatiskt om du använder mediekanaler.
{{</details>}}
