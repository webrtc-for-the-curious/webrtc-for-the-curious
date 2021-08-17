---
title: Applied WebRTC
type: docs
weight: 9
---

# Applied WebRTC
Now that you know how WebRTC works it is time to build with it! This chapter explores what people are
building with WebRTC, and how they are building it. You will learn all the interesting things that are
happening with WebRTC. The power of WebRTC comes at a cost. Building production grade WebRTC services is
challenging. This chapter will try to explain those challenges before you hit them.

## By Use Case
Many think WebRTC is just a technology for conferencing in the web browser. It is so much more than that though!
WebRTC is used in a wide range of applications. New use cases are showing up all the time. In this chapter we will list some common ones and how WebRTC is revolutionizing them.

### Conferencing
Conferencing is the original use case for WebRTC. The protocol contains a few necessary features that no other protocol offers
in the browser. You could build a conferencing system with WebSockets and it may work in optimal conditions. If you want
something that can be deployed in real world network conditions, WebRTC is the best choice.

WebRTC provides congestion control and adaptive bitrate for media. As the conditions of the network change, users will still get the
best experience possible. Developers don't have to write any additional code to measure these conditions either.

Participants can send and receive multiple streams. They can also add and remove those streams at any time during the call. Codecs are negotiated
as well. All of this functionality is provided by the browser, no custom code is required to be written by the developer.

Conferencing also benefits from data channels. Users can send metadata or share documents. You can create multiple streams
and configure them if you need performance more than reliability.

### Broadcasting
Lots of new projects are starting to appear in the broadcast space that use WebRTC. The protocol has a lot to offer for both the publisher
and consumer of media.

WebRTC being in the browser makes it easy for users to publish video. It removes the requirement for users to download a new client.
Any platform that has a web browser can publish video. Publishers can then send multiple tracks and modify or remove them at anytime. This is
a huge improvement over legacy protocols that only allowed one audio or one video track per connection.

WebRTC gives developers greater control over the latency versus quality trade-offs. If it is more important that latency never exceeds a
certain threshold, and you are willing to tolerate some decoding artifacts. You can configure the viewer to play media as soon as it
arrives. With other protocols that run over TCP, that isn't as easy. In the browser you can request data and that is it.

### Remote Access
Remote Access is when you remotely access another computer via WebRTC. You could have complete control of the remote host, or maybe just a
single application. This is great for running computationally expensive tasks when the local hardware can't do it. Like running a new video game, or
CAD software. WebRTC was able to revolutionize the space in three ways.

WebRTC can be used to remotely access a host that isn't world routable. With NAT Traversal you can access a computer that is only available
via STUN. This is great for security and privacy. Your users don't have to route video through an ingest, or a "jump box". NAT Traversal also
makes deployments easier. You don't have to worry about port forwarding or setting up a static IP ahead of time.

Data channels are really powerful as well in this scenario. They can be configured so that only the latest data is accepted. With TCP you run the
risk of encountering Head-of-line blocking. An old mouse click or keypress could arrive late, and block the subsequent ones from being accepted.
WebRTC's data channels are designed to handle this and can be configured to not resend lost packets. You can also measure the backpressure and
make sure that you aren't sending more data than your network supports.

WebRTC being available in the browser has been a huge quality of life improvement. You don't have to download a proprietary client to start the
session. More and more clients are coming with WebRTC bundled, smart TVs are getting full web browsers now.

### File Sharing and Censorship Circumvention
File Sharing and Censorship Circumvention are dramatically different problems. However, WebRTC solves the same problems for them both. It makes
them both easily available and harder to block.

The first problem that WebRTC solves is getting the client. If you want to join a file sharing network, you need to download the client. Even if
the network is distributed, you still need to get the client first. In a restricted network the download will often be blocked. Even if you
can download it, the user may not be able to install and run the client. WebRTC is available in every web browser already making it readily available.

The second problem that WebRTC solves is your traffic being blocked. If you use a protocol that is just for file sharing or censorship circumvention
it is much easier to block it. Since WebRTC is a general purpose protocol, blocking it would impact everyone. Blocking WebRTC might prevent other
users of the network from joining conference calls.

### Internet of Things
Internet of Things (IoT) covers a few different use cases. For many this means network connected security cameras. Using WebRTC you can stream the video to another WebRTC
peer like your phone or a browser. Another use case is having devices connect and exchange sensor data. You can have two devices in your LAN
exchange climate, noise or light readings.

WebRTC has a huge privacy advantage here over legacy video stream protocols. Since WebRTC supports P2P connectivity the camera can send the video
directly to your browser. There is no reason for your video to be sent to a 3rd party server. Even when video is encrypted, an attacker can make
assumptions from the metadata of the call.

Interoperability is another advantage for the IoT space. WebRTC is available in lots of different languages; C#, C++, C, Go, Java, Python, Rust
and TypeScript. This means you can use the language that works best for you. You also don't have to turn to proprietary protocols or formats
to be able to connect your clients.

### Media Protocol Bridging
You have existing hardware and software that is producing video, but you can't upgrade it yet. Expecting users to download a proprietary
client to watch videos is frustrating. The answer is to run a WebRTC bridge. The bridge translates between the two protocols so users can use the
browser with your legacy setup.

Many of the formats that developers bridge with use the same protocols as WebRTC. SIP is commonly exposed via WebRTC and allows users to make phone calls
from their browser. RTSP is used in lots of legacy security cameras. They both use the same underlying protocols (RTP and SDP) so it is computationally cheap
to run. The bridge is just required to add or remove things that are WebRTC specific.

### Data Protocol Bridging
A web browser is only able to speak a constrained set of protocols. You can use HTTP, WebSockets, WebRTC and QUIC. If you want to connect
to anything else, you need to use a protocol bridge. A protocol bridge is a server that converts foreign traffic into something the browser
can access. A popular example is using SSH from your browser to access a server. WebRTC's data channels have two advantages over the competition.

WebRTC's data channels allow unreliable and unordered delivery. In cases where low latency is critical this is needed. You don't want new data to be
blocked by old data, this is known as head-of-line blocking. Imagine you are playing a multiplayer First-person shooter. Do you really care where the
player was two seconds ago? If that data didn't arrive in time, it doesn't make sense to keep trying to send it. Unreliable and unordered delivery allows
you to use the data as soon as it arrives.

Data channels also provide feedback pressure. This tells you if you are sending data faster than your connection can support. You then have two
choices when this happens. The data channel can either be configured to buffer and deliver the data late, or you can drop the data that hasn't arrived
in real-time.

### Teleoperation
Teleoperation is the act of controlling a device remotely via WebRTC data channels, and sending the video back via RTP. Developers are driving cars remotely
via WebRTC today! This is used to control robots at construction sites and deliver packages. Using WebRTC for these problems makes sense for two reasons.

The ubiquity of WebRTC makes it easy to give users control. All the user needs is a web browser and an input device. Browsers even
support taking input from joysticks and gamepads. WebRTC completely removes the need to install an additional client on the user's device.

### Distributed CDN
Distributed CDNs are a subset of file sharing. The files being distributed are configured by the CDN operator instead. When users join the CDN network
they can download and share the allowed files. Users get all the same benefits as file sharing.

These CDNs work great when you are at an office with poor external connectivity, but great LAN connectivity. You can have one user download a video, and
then share it with everyone else. Since everyone isn't attempting to fetch the same file via the external network, the transfer will complete faster.

## WebRTC Topologies
WebRTC is a protocol for connecting two agents, so how are developers connecting hundreds of people at once? There are a few different
ways you can do it, and they all have pros and cons. These solutions broadly fall into two categories; Peer-to-Peer or Client/Server. WebRTC's
flexibility allows us to create both.

### One-To-One
One-to-One is the first connection type you will use with WebRTC. You connect two WebRTC Agents directly and they can send bi-directional media and data.
The connection looks like this.

![One-to-One](../images/08-one-to-one.png "One-to-One")

### Full Mesh
Full mesh is the answer if you want to build a conference call or a multiplayer game. In this topology each user establishes a connection
with every other user directly. This allows you to build your application, but it comes with some downsides.

In a Full Mesh topology each user is connected directly. That means you have to encode and upload video independently for each member of the call.
The network conditions between each connection will be different, so you can't reuse the same video. Error handling is also difficult in these
deployments. You need to carefully consider if you have lost complete connectivity, or just connectivity with one remote peer.

Because of these concerns, a Full Mesh is best used for small groups. For anything larger a client/server topology is best.

![Full mesh](../images/08-full-mesh.png "Full mesh")

### Hybrid Mesh
Hybrid Mesh is an alternative to Full Mesh that can alleviate some of the Full Mesh's issues. In a Hybrid Mesh connections aren't established
between every user. Instead, media is relayed through peers in the network. This means that the creator of the media doesn't have to use as
much bandwidth to distribute media.

This does have some downsides. In this set up, the original creator of the media has no idea who its video is being sent too, and if
it arrived successfully. You also will have an increase in latency with every hop in your Hybrid Mesh network.

![Hybrid mesh](../images/08-hybrid-mesh.png "Hybrid mesh")

### Selective Forwarding Unit
An SFU (Selective Forwarding Unit) also solves the issues of Full Mesh, but in an entirely different way. An SFU implements a client/server topology, instead of P2P.
Each WebRTC peer connects to the SFU and uploads its media. The SFU then forwards this media out to each connected client.

With an SFU each WebRTC Agent only has to encode and upload their video once. The burden of distributing it to all the viewers is on the SFU.
Connectivity with an SFU is much easier than P2P as well. You can run an SFU on a world routable address, making it much easier for clients to connect.
You don't need to worry about NAT Mappings. You do still need to make sure your SFU is available via TCP (either via ICE-TCP or TURN).

Building a simple SFU can be done in a weekend. Building a good SFU that can handle all types of clients is never ending. Tuning the Congestion Control, Error
Correction and Performance is a never ending task.

![Selective Forwarding Unit](../images/08-sfu.png "Selective Forwarding Unit")

### MCU
A MCU (Multi-point Conferencing Unit) is a client/server topology like an SFU, but composites the output streams. Instead of distributing the outbound media
unmodified it re-encodes them as one feed.

![Multi-point Conferencing Unit](../images/08-mcu.png "Multi-point Conferencing Unit")
