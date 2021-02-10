Welcome to WebRTC for the Curious!

# What is this book.

Start reading the book directly from GitHub [index](content/_index.md) or at [webrtcforthecurious.com](https://webrtcforthecurious.com)

When we announced the book to social media we used the following copy

```
Title: WebRTC for the Curious: Go beyond the APIs

Subject: The WebRTC book that explains everything.
WebRTC is a real-time communication framework that makes it easy
to build real-time interactions for web and mobile devices.

You will learn about the WebRTC specification and how all the
protocols work in depth, not just a tour of the APIs.
The book is completely Open Source and available at
https://webrtcforthecurious.com and
https://github.com/webrtc-for-the-curious/webrtc-for-the-curious

Learn the full details of ICE, SCTP, DTLS, SRTP, and how they work
together to make up the WebRTC stack.

Hear how WebRTC implementers debug issues with
the tools of the trade.

Listen to interviews with the authors of foundational
WebRTC tech! Hear the motivations and design details
that pre-dated WebRTC by 20 years.

Explore the cutting edge of what people are building with
WebRTC. Learn about interesting use cases and how real-world
applications get designed, tested and implemented in production.

Written by developers who have written all of this
from scratch. We learned it the hard way, now we want
to share it with you!

This book is vendor agnostic and multiple Open Source projects
and companies are involved. We would love to have you involved!
```

# Running/Deploying

* Clone this repo and it's submodules `git clone --recursive https://github.com/webrtc-for-the-curious/webrtc-for-the-curious.git`
* Download the extended version of [hugo](https://github.com/gohugoio/hugo)
* Run `hugo server`

# Contributing

We would love contributions! We are open to suggestions about the content as well. This is a community-owned project, and we want to hear what is important to you. Below is a rough guide to where each chapter stands.

|Chapter|Stage|Authors|Current need|
|-------|-----|-------|------------|
|What, Why and How|Finishing Touches|@Sean-Der|[Issues](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/new) for minor tweaks|
|Signaling|Finishing Touches|@Sean-Der|[Issues](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/new) for minor tweaks, [Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/02-signaling.md) for additional content|
|Connecting|Finishing Touches|@Sean-Der|[Issues](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/new) for minor tweaks|
|Securing|Finishing Touches|@Sean-Der|[Issues](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/new) for minor tweaks|
|Media Communication|Authoring|@Sean-Der @zhuker|[Issues](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/new) for minor tweaks, [Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/05-media-communication.md) for additional content|
|Data Communication|Planning|@Sean-Der @enobufs|[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/06-data-communication.md) for content|
|Applied WebRTC|Planning|@Sean-Der @leewardbound|[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/07-applied-webrtc.md) for content|
|Debugging|Planning|@Sean-Der|[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/08-debugging.md) for content, Chapter [Ownership](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/10)|
|History|Planning|@Sean-Der|[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/09-history-of-webrtc.md) for content, Chapter [Ownership](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/10)|
|FAQ|Unstarted||[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/10-faq.md) for content, Chapter [Ownership](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/10)|
|Contributing|Unstarted||[Edits](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/edit/master/content//docs/11-contributing.md) for content, Chapter [Ownership](https://github.com/webrtc-for-the-curious/webrtc-for-the-curious/issues/10)|

## Contributing from your browser (via Codespaces!)

We support [*Github Codespaces*](https://github.com/features/codespaces) so helping out is as easy as starting up a Codespace from this repo.

Once started, click "Run Live Docs Server" in the statusbar to start the Hugo server. Note that Hugo's autoreload doesn't trigger a browser refresh from Codespaces yet due to missing proxying of WebSockets traffic. Reload a page manually to rerender it.

# License

This book is available under the CC0 license. The authors have waived all their copyright and related rights in their works to the fullest extent allowed by law. You May use this work however you want and no attribution is required.

The only intention of this book is to make the world a better place. WebRTC is a wonderful technology but is difficult to use. This book is vendor agnostic, and we have tried to remove any conflicts of interest.
