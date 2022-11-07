---
title: FAQ
type: docs
weight: 12
---

# FAQ

{{<details "¿Por qué WebRTC usa UDP?">}}
La NAT Transversal requiere UDP. Sin la NAT Transversal, establecer una conexión P2P
no sería posible. UDP no provee una "entrega garantizada" como TCP, así que WebRTC lo hace a nivel de
usuario.

Mira [Conexión]({{< ref "03-connecting" >}}) para más información.
{{</details>}}

{{<details "¿Qué tantos DataChannel puedo tener?">}}
65534 canales como identificador de flujo tiene 16 bits. Puedes cerrar y abrir uno nuevo cuando quieras
{{</details>}}

{{<details "Does WebRTC impose bandwidth limits?">}}
Both DataChannels and RTP use congestion control. This means that WebRTC actively measures
your bandwidth and attempts to use the optimal amount. It is a balance between sending as much
as possible, without overwhelming the connection.
{{</details>}}

{{<details "Can I send binary data?">}}
Yes, you can send both text and binary data via DataChannels.
{{</details>}}

{{<details "What latency can I expect with WebRTC?">}}
For un-tuned media, you can expect sub-500 milliseconds. If you are willing to tune or sacrifice quality
for latency, developers have gotten sub-100ms latency.

DataChannels support "Partial-reliability" option which can reduce latency caused by
data retransmissions over a lossy connection. If configured properly, it has been shown to beat TCP TLS connections.
{{</details>}}

{{<details "Why would I want unordered delivery for DataChannels?">}}
When newer information obsoletes the old such as positional information of an
object, or each message is independent from the others and need to avoid
head-of-line blocking delay.
{{</details>}}

{{<details "Can I send audio or video over a DataChannel?">}}
Yes, you can send any data over a DataChannel. In the browser case, it will be your
responsibility to decode the data and pass it to a media player for rendering,
while all of that is done automatically if you use media channels.
{{</details>}}
