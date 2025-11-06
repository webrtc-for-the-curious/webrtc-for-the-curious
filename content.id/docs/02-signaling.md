---
title: Signaling
type: docs
weight: 3
---

# Signaling

## Apa itu _Signaling_ pada WebRTC?

Ketika Anda membuat klien WebRTC, pada dasarnya klien tersebut tidak mengetahui apapun tentang _peer_ lainnya. Ia tidak tahu dengan siapa ia akan terhubung dan apa yang akan mereka kirimkan!
_Signaling_ adalah proses awal yang memungkinkan sebuah panggilan terjadi. Setelah nilai-nilai ini dipertukarkan, klien WebRTC dapat berkomunikasi langsung satu sama lain.

Pesan _signaling_ hanyalah teks biasa. Klien WebRTC tidak peduli bagaimana pesan tersebut dikirimkan. Pesan ini umumnya dikirim melalui WebSocket, namun itu bukan keharusan.

## Bagaimana _signaling_ WebRTC bekerja?

WebRTC menggunakan protokol yang sudah ada sebelumnya yang disebut Session Description Protocol. Melalui protokol ini, dua klien WebRTC akan berbagi semua informasi yang diperlukan untuk membangun sebuah koneksi. Protokol ini sendiri cukup sederhana untuk dibaca dan dipahami.
Kompleksitasnya datang dari memahami semua nilai yang diisi oleh WebRTC ke dalamnya.

Protokol ini tidak spesifik untuk WebRTC saja. Kita akan mempelajari Session Description Protocol terlebih dahulu tanpa membahas WebRTC. WebRTC sebenarnya hanya memanfaatkan sebagian kecil dari protokol ini, jadi kita hanya akan membahas apa yang kita butuhkan.
Setelah kita memahami protokolnya, kita akan beralih ke penggunaannya dalam WebRTC.

## Apa itu *Session Description Protocol* (SDP)?
Session Description Protocol didefinisikan dalam [RFC 8866](https://tools.ietf.org/html/rfc8866). Ini adalah protokol _key/value_ dengan baris baru setelah setiap nilai. Terasa mirip dengan file INI.
Sebuah Session Description berisi nol atau lebih Media Description. Secara mental Anda dapat memodelkannya sebagai Session Description yang berisi array dari Media Description.

Sebuah Media Description biasanya dipetakan ke satu _stream_ media tunggal. Jadi jika Anda ingin menggambarkan panggilan dengan tiga _stream_ video dan dua _track_ audio, Anda akan memiliki lima Media Description.

### Cara membaca SDP
Setiap baris dalam Session Description akan dimulai dengan satu karakter, ini adalah _key_ Anda. Kemudian akan diikuti dengan tanda sama dengan. Semua yang ada setelah tanda sama dengan adalah nilainya. Setelah nilai selesai, akan ada baris baru.

Session Description Protocol mendefinisikan semua _key_ yang valid. Anda hanya dapat menggunakan huruf untuk _key_ sebagaimana didefinisikan dalam protokol. _Key_ ini semuanya memiliki arti penting, yang akan dijelaskan nanti.

Perhatikan cuplikan Session Description berikut:

```
a=my-sdp-value
a=second-value
```

Anda memiliki dua baris. Masing-masing dengan _key_ `a`. Baris pertama memiliki nilai `my-sdp-value`, baris kedua memiliki nilai `second-value`.

### WebRTC hanya menggunakan beberapa _key_ SDP
Tidak semua nilai _key_ yang didefinisikan oleh Session Description Protocol digunakan oleh WebRTC. Hanya _key_ yang digunakan dalam JavaScript Session Establishment Protocol (JSEP), yang didefinisikan dalam [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829), yang penting. Tujuh _key_ berikut adalah satu-satunya yang perlu Anda pahami saat ini:

* `v` - Version, harus sama dengan `0`.
* `o` - Origin, berisi ID unik yang berguna untuk renegosiasi.
* `s` - Session Name, harus sama dengan `-`.
* `t` - Timing, harus sama dengan `0 0`.
* `m` - Media Description (`m=<media> <port> <proto> <fmt> ...`), dijelaskan secara detail di bawah.
* `a` - Attribute, sebuah _field_ teks bebas. Ini adalah baris yang paling umum dalam WebRTC.
* `c` - Connection Data, harus sama dengan `IN IP4 0.0.0.0`.

### Media Description dalam Session Description

Sebuah Session Description dapat berisi jumlah Media Description yang tidak terbatas.

Definisi Media Description berisi daftar format. Format ini dipetakan ke RTP Payload Type. _Codec_ sebenarnya kemudian didefinisikan oleh Attribute dengan nilai `rtpmap` dalam Media Description.
Pentingnya RTP dan RTP Payload Type dibahas kemudian dalam bab Media. Setiap Media Description dapat berisi jumlah atribut yang tidak terbatas.

Perhatikan cuplikan Session Description sebagai contoh:

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

Anda memiliki dua Media Description, satu berjenis audio dengan fmt `111` dan satu berjenis video dengan format `96`. Media Description pertama hanya memiliki satu atribut. Atribut ini memetakan Payload Type `111` ke Opus.
Media Description kedua memiliki dua atribut. Atribut pertama memetakan Payload Type `96` menjadi VP8, dan atribut kedua hanyalah `my-sdp-value`.

### Contoh Lengkap

Berikut ini menggabungkan semua konsep yang telah kita bicarakan. Ini adalah semua fitur Session Description Protocol yang digunakan WebRTC.
Jika Anda dapat membaca ini, Anda dapat membaca Session Description WebRTC apapun!

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

* `v`, `o`, `s`, `c`, `t` didefinisikan, tetapi tidak mempengaruhi sesi WebRTC.
* Anda memiliki dua Media Description. Satu berjenis `audio` dan satu berjenis `video`.
* Masing-masing memiliki satu atribut. Atribut ini mengonfigurasi detail _pipeline_ RTP, yang dibahas dalam bab "Media Communication".

## Bagaimana *Session Description Protocol* dan WebRTC bekerja bersama

Bagian selanjutnya dari teka-teki adalah memahami _bagaimana_ WebRTC menggunakan Session Description Protocol.

### Apa itu _Offer_ dan _Answer_?

WebRTC menggunakan model _offer/answer_. Artinya, satu klien WebRTC membuat "Offer" untuk memulai panggilan, dan klien WebRTC lainnya "Answer" jika bersedia menerima apa yang ditawarkan.

Ini memberi penjawab kesempatan untuk menolak _codec_ yang tidak didukung dalam Media Description. Inilah cara dua _peer_ dapat memahami format apa yang bersedia mereka pertukarkan.

### _Transceiver_ untuk mengirim dan menerima

_Transceiver_ adalah konsep khusus WebRTC yang akan Anda lihat di API. Ini mengekspos "Media Description" ke API JavaScript. Setiap Media Description menjadi _Transceiver_.
Setiap kali Anda membuat _Transceiver_, Media Description baru akan ditambahkan ke Session Description lokal.

Setiap Media Description dalam WebRTC akan memiliki atribut arah. Ini memungkinkan klien WebRTC untuk menyatakan "Saya akan mengirimkan _codec_ ini kepada Anda, tetapi saya tidak bersedia menerima apapun kembali". Ada empat nilai yang valid:

* `send`
* `recv`
* `sendrecv`
* `inactive`

### Nilai SDP yang digunakan oleh WebRTC

Ini adalah daftar beberapa atribut umum yang akan Anda lihat dalam Session Description dari klien WebRTC. Banyak dari nilai ini mengontrol subsistem yang belum kita bahas.

#### `group:BUNDLE`
_Bundling_ adalah tindakan menjalankan beberapa jenis traffic melalui satu koneksi. Beberapa implementasi WebRTC menggunakan koneksi khusus per _media stream_. _Bundling_ harus lebih diutamakan.

#### `fingerprint:sha-256`
Ini adalah _hash_ dari sertifikat yang digunakan _peer_ untuk DTLS. Setelah _handshake_ DTLS selesai, Anda membandingkannya dengan sertifikat sebenarnya untuk mengonfirmasi bahwa Anda berkomunikasi dengan siapa yang Anda harapkan.

#### `setup:`
Ini mengontrol perilaku DTLS Agent. Ini menentukan apakah ia berjalan sebagai _client_ atau _server_ setelah ICE terhubung. Nilai yang mungkin adalah:

* `setup:active` - Berjalan sebagai DTLS Client.
* `setup:passive` - Berjalan sebagai DTLS Server.
* `setup:actpass` - Minta klien WebRTC lainnya untuk memilih.

#### `mid`
Atribut "mid" digunakan untuk mengidentifikasi _media stream_ dalam _session description_.

#### `ice-ufrag`
Ini adalah nilai _user fragment_ untuk ICE Agent. Digunakan untuk autentikasi traffic ICE.

#### `ice-pwd`
Ini adalah _password_ untuk ICE Agent. Digunakan untuk autentikasi traffic ICE.

#### `rtpmap`
Nilai ini digunakan untuk memetakan _codec_ tertentu ke RTP Payload Type. Payload Type tidak statis, jadi untuk setiap panggilan, pemberi _offer_ memutuskan Payload Type untuk setiap _codec_.

#### `fmtp`
Mendefinisikan nilai tambahan untuk satu Payload Type. Ini berguna untuk mengkomunikasikan _video profile_ tertentu atau pengaturan _encoder_.

#### `candidate`
Ini adalah ICE Candidate yang berasal dari ICE Agent. Ini adalah satu alamat yang mungkin di mana klien WebRTC tersedia. Ini dijelaskan sepenuhnya di bab berikutnya.

#### `ssrc`
_Synchronization Source_ (SSRC) mendefinisikan satu _media stream track_ tunggal.

`label` adalah ID untuk _stream_ individual ini. `mslabel` adalah ID untuk kontainer yang dapat memiliki beberapa _stream_ di dalamnya.

### Contoh Session Description WebRTC
Berikut adalah Session Description lengkap yang dihasilkan oleh klien WebRTC:

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

Inilah yang kita ketahui dari pesan ini:

* Kita memiliki dua _media section_, satu audio dan satu video.
* Keduanya adalah _transceiver_ `sendrecv`. Kita menerima dua _stream_, dan kita dapat mengirim dua kembali.
* Kita memiliki ICE Candidate dan detail autentikasi, jadi kita dapat mencoba untuk terhubung.
* Kita memiliki _fingerprint_ sertifikat, jadi kita dapat melakukan panggilan yang aman.

### Topik Lebih Lanjut
Dalam versi selanjutnya dari buku ini, topik berikut juga akan dibahas:

* Renegotiation
* Simulcast
