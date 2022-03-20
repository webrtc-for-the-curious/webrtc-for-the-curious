---
title: History
type: docs
weight: 11
---


# History
When learning WebRTC developers often feel frustrated by the complexity. They
see
WebRTC features irrelevant to their current project and wish WebRTC was
simpler. The issue
is that everyone has a different set of use cases. Real-time communications has
a rich
history with lots of different people building many different things.

This chapter contains interviews with the authors of the protocols that make up
WebRTC.
It gives insight into the designs made when building each protocol, and
finishes with an
interview about WebRTC itself. If you understand the intentions and designs of
the software
you can build more effective systems with it.

## RTP
RTP and RTCP is the protocol that handles all media transport for WebRTC. It
was defined in [RFC 1889](https://tools.ietf.org/html/rfc1889) in January 1996.
We are very lucky to have one of the authors [Ron
Frederick](https://github.com/ronf) talk about it himself. Ron recently uploaded
[Network Video tool](https://github.com/ronf/nv) to GitHub, a project that
informed RTP.

### In his own words

In October of 1992, I began to experiment with the Sun VideoPix frame grabber
card, with the idea of writing a network videoconferencing tool based upon IP
multicast. It was modeled after "vat" -- an audioconferencing tool developed
at LBL, in that it used a similar lightweight session protocol for users
joining into conferences, where you simply sent data to a particular
multicast group and watched that group for any traffic from other group
members.

In order for the program to really be successful, it needed to compress the
video data before putting it out on the network. My goal was to make an
acceptable looking stream of data that would fit in about 128 kbps, or the
bandwidth available on a standard home ISDN line. I also hoped to produce
something that was still watchable that fit in half this bandwidth. This
meant I needed approximately a factor of 20 in compression for the particular
image size and frame rate I was working with. I was able to achieve this
compression and filed for a patent on the techniques I used, later granted
as patent [US5485212A][1]: Software video compression for teleconferencing.

[1]: https://patents.google.com/patent/US5485212A

In early November of 1992, I released the videoconferencing tool "nv" (in
binary form) to the Internet community. After some initial testing, it was used
to videocast parts of the November Internet Engineering Task Force all around
the world. Approximately 200 subnets in 15 countries were capable of
receiving this broadcast, and approximately 50-100 people received video using
"nv" at some point in the week.

Over the next couple of months, three other workshops and some smaller
meetings used "nv" to broadcast to the Internet at large, including the
Australian NetWorkshop, the MCNC Packet Audio and Video workshop, and the
MultiG workshop on distributed virtual realities in Sweden.

A source code release of "nv" followed in February of 1993, and in March I
released a version of the tool where I introduced a new wavelet-based
compression scheme. In May of 1993, I added support for color video.

The network protocol used for "nv" and other Internet conferencing tools
became the basis of the Realtime Transport Protocol (RTP), standardized
through the Internet Engineering Task Force (IETF), first published in
RFCs [1889][2]-[1890][3] and later revised in RFCs [3550][4]-[3551][5]
along with various other RFCs that covered profiles for carrying specific
formats of audio and video.

[2]: https://tools.ietf.org/html/rfc1889
[3]: https://tools.ietf.org/html/rfc1890
[4]: https://tools.ietf.org/html/rfc3550
[5]: https://tools.ietf.org/html/rfc3551

Over the next couple of years, work continued on "nv", porting the tool
to a number of additional hardware platforms and video capture devices.
It continued to be used as one of the primary tools for broadcasting
conferences on the Internet at the time, including being selected by NASA
to broadcast live coverage of shuttle missions online.

In 1994, I added support in "nv" for supporting video compression algorithms
developed by others, including some hardware compression schemes such as
the CellB format supported by the SunVideo video capture card. This also
allowed "nv" to send video in CUSeeMe format, to send video to users
running CUSeeMe on Macs and PCs.

The last publicly released version of "nv" was version 3.3beta, released
in July of 1994. I was working on a "4.0alpha" release that was intended
to migrate "nv" over to version 2 of the RTP protocol, but this work was
never completed due to my moving on to other projects. A copy of the 4.0
alpha code is included in the [Network Video tool](https://github.com/ronf/nv)
archive for completeness, but it is unfinished and there are known issues
with it, particularly in the incomplete RTPv2 support.

The framework provided in "nv" later went on to become the basis of video
conferencing in the "Jupiter multi-media MOO" project at Xerox PARC, which
eventually became the basis for a spin-off company "PlaceWare", later
acquired by Microsoft. It was also used as the basis for a number of
hardware video conferencing projects that allowed sending of full NTSC
broadcast quality video over high-bandwidth Ethernet and ATM networks.
I also later used some of this code as the basis for "Mediastore", which
was a network-based video recording and playback service.

### Do you remember the motivations/ideas of the other people on the draft?

We were all researchers working on IP multicast, and helping to create
the Internet multicast backbone (aka MBONE). The MBONE was created by
Steve Deering (who first developed IP multicast), Van Jacobson, and Steve
Casner. Steve Deering and I had the same advisor at Stanford, and Steve
ended up going to work at Xerox PARC when he left Stanford, I spent a
summer at Xerox PARC as an intern working on IP multicast-related projects
and continued to work for them part time while at Stanford and later full
time. Van Jacobson and Steve Casner were two of the four authors on
the initial RTP RFCs, along with Henning Schulzrinne and myself. We all
had MBONE tools that we were working on that allowed for various forms of
online collaboration, and trying to come up with a common base protocol
all these tools could use was what led to RTP.

### Multicast is super fascinating. WebRTC is entirely unicast, mind expanding on that?

Before getting to Stanford and learning about IP multicast, I had a
long history working on ways to use computers as a way for people to
communicate with one another. This started in the early 80s for me
where I ran a dial-up bulletin board system where people could log on
and leave messages for one another, both private (sort of the equivalent
of e-mail) and public (discussion groups). Around the same time, I also
learned about the online service provider CompuServe. One of the cool
features on CompuServe was something called a “CB Simulator” where people
could talk to one another in real-time. It was all text-based, but it
had a notion of “channels” like a real CB radio, and multiple people
could see what others typed, as long as they were in the same channel.
I built my own version of CB which ran on a timesharing system I had
access to which let users on that system send messages to one another
in real-time, and over the next few years I worked with friends to
develop more sophisticated versions of real-time communication tools
on several different computer systems and networks. In fact, one of those
systems is still operational, and I use it talk every day to folks I went
to college with 30+ years ago!

All of those tools were text based, since computers at the time generally
didn't have any audio/video capabilities, but when I got to Stanford and
learned about IP multicast, I was intrigued by the notion of using multicast
to get something more like a true “radio” where you could send a signal
out onto the network that wasn't directed at anyone in particular, but
everyone who tuned to that “channel” could receive it. As it happened, the
computer I was porting the IP multicast code to what was the first generation
SPARC-station from Sun, and it actually had built-in telephone-quality audio
hardware! You could digitize sound from a microphone and play it back over
built-in speakers (or via a headphone output). So, my first thought was to
figure out how to send that audio out onto the network in real-time using
IP multicast, and see if I could build a “CB radio” equivalent with actual
audio instead of text.

There were some tricky things to work out, like the fact that the computer
could only play one audio stream at a time, so if multiple people were talking
you needed to mathematically “mix” multiple audio streams into one before
you could play it, but that could all be done in software once you understood
how the audio sampling worked. That audio application led me to working on
the MBONE and eventually moving from audio to video with “nv”.

### Anything that got left out of the protocol that you wish you had added? Anything in the protocol you regret?

I wouldn't say I regret it, but one of the big complaints people ended up
having about RTP was the complexity of implementing RTCP, the control protocol
that ran in parallel with the main RTP data traffic. I think that complexity
was a large part of why RTP wasn't more widely adopted, particularly in the
unicast case where there wasn't as much need for some of RTCP's features.
As network bandwidth became less scarce and congestion wasn't as big a
problem, a lot of people just ended up streaming audio & video over plain
TCP (and later HTTP), and generally speaking it worked “well enough” that
it wasn't worth dealing with RTP.

Unfortunately, using TCP or HTTP meant that multi-party audio and video
applications had to send the same data over the network multiple times,
to each of the peers that needed to receive it, making it much less
efficient from a bandwidth perspective. I sometimes wish we had pushed
harder to get IP multicast adopted beyond just the research community.
I think we could have seen the transition from cable and broadcast
television to Internet-based audio and video much sooner if we had.

### What things did you imagine being built with RTP? Do have any cool RTP projects/ideas that got lost to time?

One of the fun things I built was a version of the classic “Spacewar” game
which used IP multicast. Without having any kind of central server, multiple
clients could each run the spacewar binary and start broadcasting their
ship's location, velocity, the direction it was facing, and similar
information for any “bullets” it had fired, and all of the other instances
would pick up that information and render it locally, allowing users to all
see each other's ships and bullets, with ships “exploding” if they crashed
into each other or bullets hit them. I even made the “debris” from the
explosion a live object that could take out other ships, sometimes leading
to fun chain reactions!

In the spirit of the original game, I rendered it using simulated vector
graphics, so you could do things like zooming your view in & out and
everything would scale up/down. The ships themselves were a bunch of
line segments in vector form that I had some of my colleagues at PARC
helped me to design, so everyone's ship had a unique look to it.

Basically, anything that could benefit from a real-time data stream that
didn't need perfect in-order delivery could benefit from RTP. So, in addition
to audio & video we could build things like a shared whiteboard. Even file
transfers could benefit from RTP, especially in conjunction with IP multicast.

Imagine something like BitTorrent but where you didn't need all the data
going point-to-point between peers. The original seeder could send a multicast
stream to all of the leeches at once, and any packet losses along the way
could be quickly cleaned up by a retransmission from any peer that
successfully received the data. You could even scope your retransmission
requests so that some peer nearby delivered the copy of the data, and that
too could be multicast to others in that region, since a packet loss in
the middle of the network would tend to mean a bunch of clients
downstream of that point all missed the same data.

### Why did you have to roll your own video compression. Was nothing else available at the time?

At the time I began to build “nv”, the only systems I know of that did
videoconferencing were very expensive specialized hardware. For instance,
Steve Casner had access to a system from BBN that was called "DVC" (and
later commercialized as “PictureWindow”). The compression required
specialized hardware, but the decompression could be done in software.
What made “nv” somewhat unique was that both compression and decompression
was being done in software, with the only hardware requirement being
something to digitize an incoming analog video signal.

Many of the basic concepts about how to compress video existed by then, with
things like the MPEG-1 standard appearing right around the same time “nv”
did, but real-time encoding with MPEG-1 was definitely NOT possible at
the time. The changes I made were all about taking those basic concepts and
approximating them with much cheaper algorithms, where I avoided things like
cosine transforms and floating point, and even avoided integer multiplications
since those were very slow on SPARC-stations. I tried to do everything I could
with just additions/subtractions and bit masking and shifting, and that got
back enough speed to still feel somewhat like video.

Within a year or two of the release of "nv", there were many different audio
and video tools to choose from, not only on the MBONE but in other places
like the CU-SeeMe tool built on the Mac. So, it was clearly an idea whose
time had come. I actually ended up making “nv” interoperate with many of
these tools, and in a few cases other tools picked up my “nv” codecs, so
they could interoperate when using my compression scheme.

## WebRTC
WebRTC required a standardization effort that dwarfs all of the other efforts
described in this chapter. It required cooperation across two different
standards bodies (IETF and W3C) and hundreds of individuals across many
companies and countries. To give us a look inside the motivations and
monumental effort it took to make WebRTC happen we have
[Serge Lachapelle](https://twitter.com/slac).

Serge is a product manager at Google, currently serving as a product manager
for Google Workspace. This is my summary of the interview.

### What led you to work on WebRTC?
I have been passionate about building communications software since I was in
college. In the 90s the technology like [nv](https://github.com/ronf/nv)
started to appear, but was difficult to use. I created a project that allowed
you to join a video call right from your browser. I also ported it to Windows.

I took this experience to Marratech, a company I co-founded. We created
software for group video conferencing. Technologically the landscape
was so different. The cutting edge in video was based on multicast networking.
A user could depend on the network to deliver to a video packet to everyone in
the call. This meant that we had very simple servers. This had a big downside
though, networks had to be designed to accommodate it. The industry moved away
from multicast to packet shufflers, more commonly known as SFUs.

Marratech was acquired by Google in 2007. I would then go on to work on the
project that would inform WebRTC.

### The first Google project
The first project that the future WebRTC team worked on was Gmail voice and
video chat. Getting audio and video into the browser was no easy task. It
required specialty components that we had to license from different companies.
Audio was licensed from GIPs, video was licensed for Vidyo and the networking
was libjingle. The magic was then making all of them work together.

Each subsystem has completely different APIs, and assumed you were solving
different problems. To make it all work together you need working knowledge
of networking, cryptography, media and more.
[Justin Uberti](https://juberti.com) was the person that took on this work.
He brought these components together to make a usable product.

Rendering real-time in the browser was also really hard. We had to use the
NPAPI (Netscape Plugin API) and do lots of clever things to make it work.
The lessons we learned from this project greatly influenced WebRTC.

### Chrome
At the same time the Chrome project started inside of Google. There was
so much excitement, and this project had huge goals. There was talk about
WebGL, Offline, Database capabilities, low latency input for gaming just
to name a few.

Moving away from NPAPI became a big focus. It is a powerful API, but comes with
big security consequences. Chrome uses a sandbox design to keep users safe.
Operations that can be potentially unsafe are run in different processes.
Even if something goes wrong an attacker still doesn't have access to the
user data.

### WebRTC is born
For me WebRTC was born with a few motivations. Combined they gave birth to the
effort.

It shouldn't be this hard to build RTC experiences. So much effort is wasted
re-implementing the same thing by different developers. We should solve these
frustrating integration problems once, and focus on other things.

Human communication should be unhampered and should be open. How is it ok for
text and HTML to be open, but my voice and my image in real-time not to be?

Security is a priority. Using the NPAPI wasn't best for users. This was also
a chance to make a protocol that was secure by default.

To make WebRTC happen Google acquired and Open Sourced the components we had
used before. [On2](https://en.wikipedia.org/wiki/On2_Technologies) was
acquired for it’s video technology and
[Global IP Solutions](https://en.wikipedia.org/wiki/Global_IP_Solutions)
for its RTC technology. I was in charge of the effort of acquiring GIPS.
We got to work combining these and making them easy to use in and outside
the browser.

### Standardization
Standardizing WebRTC was something we really wanted to do, but not something I
had done before nor anyone on our immediate team. For this we were really
fortunate to have Harald Alvestrand at Google. He had done extensive work in
the IETF already and started the WebRTC standardization process.

In summer 2010 an informal lunch was scheduled in Maastricht. Developers from
many companies came together to discuss what WebRTC should be. The lunch had
engineers from Google, Cisco, Ericsson, Skype, Mozilla, Linden Labs and more.
You can find the full attendance and presenter slides on
[rtc-web.alvestrand.com](http://rtc-web.alvestrand.com).

Skype also provided some great guidance because of the work they had done with
Opus in the IETF.

### Standing on the shoulders of giants
When working in the IETF you are extending the work that has come before you.
With WebRTC we were lucky that so many things existed. We didn't have to take
on every problem because they already were solved. If you don't like the
pre-existing technology it can be frustrating though. There has to be a pretty
big reason to disregard existing work, so rolling your own isn't an option.

We also consciously didn't attempt to re-standardize things like signaling.
This had already been solved with SIP and other non-IETF efforts, and it
felt like it could end up being very political. In the end it just didn't
feel like there was much value to add to the space.

I didn't stay as involved in standardization as Justin and Harald, but I
enjoyed my time doing it. I was more excited about returning to building
things for users.

### The future
WebRTC is in a great place today. There are lots of iterative changes
happening, but nothing in particular I have been working on.

I am most excited about what cloud computing can do for communication. Using
advanced algorithms we can remove background noise from a call and make
communication possible where it wasn't before. We are also seeing WebRTC
extend far beyond communications… Who knew that it would be powering cloud
based gaming 9 years later? All of this wouldn't be possible without the
foundation of WebRTC.
