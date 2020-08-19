---
title: Securing
type: docs
weight: 5
---


## What security does WebRTC have?
Every WebRTC connection is authenticated and encrypted. You can be confident that a 3rd paert can't what you are sending. They also can't insert bogus messages. You can also be sure the WebRTC Agent that generated the Session Description is the one you are communicating with.

It is very important that no one tampers with those messages. It is ok if a 3rd party reads the Session Description in transit. However WebRTC has no protection against it being modified. An attacker could MITM you by changing ICE Candidates and the Certificate Fingerprint.


## How does it work?

WebRTC 


## Security 101
To understand the technology presented in this chapter you will need to understand these first. Cryptography is a tricky subject so would be worth consulting other sources also!


* Cipher
* Hash
* Plaintext/Ciphertext
* RSA
* ECDSA
* Perfect Forward Secrecy
* Diffie-Helman
* Public/Private Key
* Certificate

## DTLS
## SRTP

## Tying it all together
