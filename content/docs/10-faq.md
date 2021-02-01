---
title: FAQ
type: docs
weight: 11
---

# FAQ

{{<details "Why does WebRTC use UDP?">}}
NAT Traversal requires UDP. Without NAT Traversal establishing a P2P connection
wouldn't be possible.  UDP doesn't provide "guaranteed delivery" like TCP, so WebRTC provides it at the
user level.

See [Connecting]({{< ref "03-connecting" >}}) for more info.
{{</details>}}

{{<details "How many DataChannels can I have?">}}
65536 channels as stream identifier has 16 bits. You can close and open a new one ar any time.
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
For un-tuned media you can expect sub-500 milliseconds. If you are willing to tune or sacrifice quality
for latency developers have gotten sub-100ms

DataChannels support "Partial-reliability" option which can reduce latency caused by
data retransmissions over a lossy connection. If configured properly it has been shown to beat TCP TLS connections.
{{</details>}}

{{<details "Why would I want unordered delivery for DataChannels?">}}
When newer information obsoletes the old such as positional information of an
object, or each message is independent from the others and need to avoid
head-of-line blocking delay.
{{</details>}}

{{<details "Can I send audio or video over a DataChannel?">}}
You could send any data over DataChannel. In a browser case, it is your
responsibility to decode the data and pass it to a media player for rendering,
where it is automatically done when you use media channels.
{{</details>}}
