---
title: Real-time Networking
type: docs
weight: 6
---

# Why is networking so important in Real-time communication?
Networks are the limiting factor in Real-time communication. In an ideal world we would have unlimited bandwidth
and packets would arrive instantaneously. This isn't the case though. Networks are limited, and the conditions
could change at anytime. Measuring and observing network condition is also a difficult problem. You can get different behaviors
depending on hardware, software and the configuration of it.

Real-time communication also poses a problem that doesn't exist in most other domains. For a web developer it isn't fatal
if your website is slower on some networks. As long as all the data arrives users are happy. With WebRTC, if your data is
late it is useless. No one cares about what was said in a conference call 5 seconds ago.  So when developing an RTC system
you have to make a trade-off. What is my time limit, and how much can I send?

This chapter covers the concepts that apply to both data and media communication. In later chapters we go beyond
the theoretical and discuss how WebRTC's media and data subsystems solve these problems.

## What are the attributes of the network that make it difficult?
Code that effectively works across all network is complicated. You have lots of different factors, and they
can all affect each other subtly. These are the most common issues that developers will encounter.

#### Bandwidth
Bandwidth is the maximum rate of data that can be transferred across a given path. It is important to remember
this isn't a static number either. The bandwidth will change along the route as more (or less) people use it.

#### Transmission Time
Transmission Time is how long it takes for a packet to arrive. Like Bandwidth this isn't constant.
The Transmission Time can fluctuate at anytime.

#### Jitter
Jitter is the fact that `Transmission Time` may vary for each packet. Your packets could be delayed, but then
arrive in bursts.

#### Packet Loss
Packet Loss is when messages are lost in transmission. The loss could be steady, or it could come in spikes.
This could be because of the network type like satellite or Wi-Fi. Or it could be introduced by the software
along the way.

#### Maximum Transmission Unit
Maximum Transmission Unit is the limit on how large a single packet can be. Networks don't allow you to send
one giant message. At the protocol level, messages might have to be split into multiple smaller packets.

The MTU will also differ depending on what network path you take. You can
use a protocol like [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) to figure out the largest packet size you can send.

### Congestion
Congestion is when the limits of the network have been reached. This is usually because you have reached the peak
bandwidth that the current route can handle. Or it could be operator imposed lke hourly limits your ISP configures.

Congestion exhibits itself in many different ways. There is no standardized behavior. In most cases when congestion is
reached the network will drop excess packets. In other cases the network will buffer. This will cause the Transmission Time
for your packets to increase. You could also see more Jitter as your network becomes congested. This is a rapidly changing area
and new algorithms for congestion detection are still being written.

### Dynamic
Networks are incredibly dynamic and conditions can change rapidly. During a call you may send and receive hundreds of thousands of packets.
Those packets will be traveling through multiple hops. Those hops will be shared by millions of other users. Even in your local network you could have
HD movies being downloaded or maybe a device decides to download a software update.

Having a good call isn't as simple as measuring your network on startup. You need to be constantly evaluating. You also need to handle all the different
behaviors that come from a multitude of network hardware and software.

## Solving Packet Loss
Solving loss is the first problem most solve. There are multiple ways to solve it, each with their own benefits. It depends on what you are sending and how
latency tolerant you are. It is also important to note that not all packet loss is fatal. Losing some video might not be a problem, the human eye might not
even able to perceive it. Losing a users text messages are fatal.

Lets say you send 10 packets, and packets 5 and 6 are lost. Here are the ways you can solve it.

### Acknowledgments
Acknowledgments is when the receiver notifies the sender of every packet they have received. The sender is aware of packet loss when it gets an acknowledgment
for a packet twice that isn't final. When the sender gets an `ACK` for packet 4 twice, it knows that 5 hasn't been seen yet.

### Selective Acknowledgments
Selective Acknowledgments is an improvement upon Acknowledgments. A Receiver can send a `SACK` that acknowledgment multiple packets and notifies the sender of gaps.
Now the sender will get a `SACK` for 4 and 7. It the knows it needs to re-send 5 and 6.

### Negative Acknowledgments
Negative Acknowledgments solve the problem the opposite way. Instead of notify the sender what it has received, it notifies what has been lost. In our case a `NACK`
will be sent for packets 5 and 6. The sender only knows packets the receiver wishes to have sent again.

### Forward Error Correction
Forward Error Correction fixes packet loss pre-emptively. The sender sends redundant data, meaning a lost packet doesn't effect the final stream. One popular algorithm for
this is Reed–Solomon error correction.

This reduces the latency/complexity of sending and handling Acknowledgments. It would be wasteful if the network you are in has zero loss.

## Solving Jitter

## Detecting Congestion

## Resolving Congestion
### Sending Slower
### Sending Less
