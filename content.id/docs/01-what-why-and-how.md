---
title: Apa, Mengapa, dan Bagaimana
type: docs
weight: 2
---

# Apa, Mengapa, dan Bagaimana

## Apa itu WebRTC?

WebRTC, singkatan dari _Web Real-Time Communication_, pada dasarnya adalah gabungan API dan Protokol. Protokol WebRTC merupakan sekumpulan aturan bagi dua klien WebRTC untuk saling berkomunikasi secara dua arah melalui jalur komunikasi langsung yang aman. Sedangkan API WebRTC memungkinkan para pengembang aplikasi untuk menggunakan protokol WebRTC. API WebRTC yang dimaksud di sini hanya diperuntukkan bagi JavaScript.

Salah satu contoh yang mungkin setara adalah relasi antara HTTP dan API _Fetch_. Di mana WebRTC sebagai protokol sama seperti HTTP, dan API WebRTC sama seperti API _Fetch_.

Prokotol WebRTC juga tersedia dalam bentuk API lainnya dan bahasa selain JavaScript. Anda dapat menemukan banyak _server_ dan perangkat lunak spesifik lainnya untuk WebRTC. Semuanya menggunakan protokol WebRTC, dan seharusnya dapat saling berkomunikasi satu sama lain.

Protokol WebRTC diampu oleh IETF dalam kelompok kerja [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/). Sedangkan API WebRTC didokumentasikan di dalam W3C sebagai [webrtc](https://www.w3.org/TR/webrtc/).

## Mengapa saya harus mempelajari WebRTC?

Ada beberapa hal yang akan Anda pelajari mengenai WebRTC di sini. Daftar di bawah ini mungkin tidak lengkap, hanya sebagian contoh dari apa yang akan Anda dapat selama membaca buku ini. Jangan khawatir jika Anda belum paham mengenai istilah-istilah berikut, karena buku ini akan menjelaskannya kepada Anda.

* Standar terbuka
* Beragam implementasi WebRTC
* Penggunaan di peramban web
* Enkripsi wajib
* NAT _Traversal_
* Penggunaan teknologi terdahulu
* _Congestion control_
* _Sub-second latency_

## Protokol WebRTC merupakan sekumpulan dari teknologi lain

Ada banyak teknologi yang akan dibahas oleh buku ini secara keseluruhan. Namun jangan khawatir, kita akan membaginya ke dalam empat tahap.

* _Signaling_
* _Connecting_
* _Securing_
* _Communicating_

Keempat tahap tersebut harus berjalan secara berurutan. Setiap tahapan harus berhasil 100% agar tahap selanjunya dapat dijalakan.

Fakta menarik tentang WebRTC adalah setiap tahapan di atas sebenarnya tersusun atas banyak protokol lainnya! Untuk membuat aplikasi WebRTC, kita harus menyusun banyak teknologi lain yang sebenarnya sudah ada sebelumnya. Itu artinya, WebRTC lebih merupakan kombinasi dan konfigurasi dari beberapa teknologi terdahulu sejak awal tahun 2000-an.

Setiap tahapan ditulis dalam masing-masing bab, tetapi akan sangat membantu untuk memahaminya secara berurutan. Karena setiap tahapan bergantung satu sama lain, tentu ini akan membantu ketika memahami lebih lanjut.

### _Signaling_: Bagaimana setiap _peer_ saling berinteraksi di WebRTC

Pada dasarnya setiap klien WebRTC tidak tahu bagaimana cara berkomunikasi dan apa yang akan dikomunikasikan dengan klien lainnya. Untuk itulah _signaling_ hadir untuk memecahkan masalah tersebut! _Signaling_ digunakan untuk membangun komunikasi sehingga dua atau lebih klien WebRTC dapat saling berinteraksi.

_Signaling_ menggunakan protokol SDP yang sudah ada sebelumnya. SDP merupakan protokol berbasis teks. Setiap pesan SDP disusun atas pasangan _key/value_ dan berisi sekumpulan daftar "informasi media". SDP yang digunakan oleh dua klien WebRTC untuk saling berkomunikasi biasanya terdiri dari:

* Daftar alamat IP dan _port_ di mana klient tersebut dapat dihubungi (_candidates_).
* Berapa banyak _track_ audio dan video yang akan dikirimkan.
* Apa _codec_ dari audio dan video yang klien tersebut gunakan.
* Parameter yang digunakan ketika proses _connecting_ (`uFrag`/`uPwd`).
* Parameter yang digunakan ketika proses _securing_ (_certificate fingerprint_).

Perlu dicatat bahwa proses _signaling_ biasanya terjadi "_out of band_"; artinya aplikasi umumnya tidak menggunakan WebRTC itu sendiri dalam proses _signaling_. Beberapa arsitektur yang bisa digunakan untuk mengirim data dapat juga digunakan untuk bertukar SDP antar _peer_, serta banyak aplikasi yang menggunakan infrastruktur bawaan mereka (contohnya REST, WebSocket, dan lain sebagainya) yang digunaan dalam proses pertukaran SDP antar klien.

### _Connecting_ dan NAT _Traversal_ dengan STUN/TURN

Pada tahap ini dua klien WebRTC sudah saling mengetahui cara untuk saling berkomunikasi satu sama lain. Selanjutya WebRTC memanfaatkan teknologi lain yang disebutkan ICE.

ICE (_Interactive Connectivity Establishment_) merupakan protokol yang sudah ada sejak lama. ICE memungkinkan terbentuknya sambungan antara dua klien. Kedua klien ini bisa jadi berada dalam satu jaringan yang sama, atau di jaringan yang berbeda di belahan dunia lain. ICE merupakan cara untuk membangun sambungan langsung tanpa _server_ perantara.

Hal yang paling penting di sini adalah NAT _Traversal_ dan STUN/TURN _Server_. Kedua teknologi ini yang akan Anda butuhkan dalam proses komunikasi antar klien ICE di dalam subnet yang berbeda. Kita akan ulas lebih lengkap kedua konsep ini nanti.

Ketika ICE berhasil tersambung, WebRTC kemudian akan mencoba membangun jalur transpor yang aman. Jalur transpor ini digunakan untuk audio, video, dan data.

### _Securing_ jalur transpor dengan DTLS dan SRTP

Setelah kita telah memiliki jalur komunikasi dua arah (menggunakan ICE), tahap selanjutnya kita perlu membangun jalur komunikasi yang aman. Ini juga memanfatkan protokol yang sudah ada sebelum WebRTC. Protokol pertama adala DTLS (_Datagram Transport Layer Security_), yang merupakan protokol TLS melalui UDP. TLS adalah protokol kriptografi yang digunakan untuk mengamankan komunikasi melalui HTTPS. Protokol kedua adalah SRTP (_Secure Real-time Transport_).

Pertama, WebRTC tersambung dengan melakukan DTLS _handshake_ melalui sambungan yang dibentuk oleh ICE. Tidak seperti HTTPS, WebRTC tidak menggunakan sertifikat _authority_ terpusat. Melainkan, WebRTC melakukan pertukaran sertifikat melalui pencocokan DTLS _fingerprint_ pada saat proses _signaling_. DTLS ini kemudian akan digunakan untuk _DataChannel_.

Kemudian WebRTC menggunakan protokol lainnya untuk mengirimkan audio dan video yang dikenal dengan RTP. Kita perlu mengamankan paket RTP kita menggunakan SRTP. Proses inisiasi sesi SRTP terjadi dengan cara mendapatkan kunci/sertifikat di dalam sesi DTLS sebelumnya. Pada tahapan berikutnya, kita akan membahas mengapa pengiriman audio dan video ini harus menggunakan protokol tersendiri.

Selesai! Sekarang kita telah memiliki jalur komunikasi dua arah yang aman. Jika Anda memiliki jaringan yang stabil di antara dua klien WebRTC Anda, semua proses rumit yang perlu dilalui telah selesai. Namun sayangnya, pada kenyataannya sering terjadi _packet loss_ dan keterbatasan _bandwith_, dan di bab selanjutnya kita akan membahas bagaimana mengatasinya.

### _Communicating_ antar _peer_ melalui RTP dan SCTP

Kini kita telah memiliki dua klien WebRTC yang telah bisa berkomunikasi dua arah secara aman. Selanjutnya mari berinteraksi! Sama seperti sebelumnya, kita akan menggunakan dua protokol yang sudah ada sebelumnya: RTP (_Real-time Transport Protocol_) dan SCTP (_Stream Control Transmission Protocol_). Kita meggunakan RTP untuk bertukar media terenkripsi dengan SRTP, dan menggunakan SCTP unuk menggirim dan menerima pesan _DataChannel_ yang terenkripsi dengan DTLS.

Protokol RTP cukup sederhana, namun menyediakan apa yang dibutuhkan dalam implementasi video _streaming_. Hal yang paling penting adalah adalah RTC memberikan keleluasaan bagi para pengembang, sehingga mereka dapat menangani _latency_, _loss_, dan _congestion sesuai dengan apa yang diinginkan. Kita akan membahas lebih lanjut mengenai ini pada bab media.

Protokol terakhir adalah SCTP. SCTP memungkinkan banyak opsi pengiriman data. Anda bisa memilih opsi _unreliable_, pengiriman dengan urutan acak, agar Anda dapat mengurangi _latency_ pada aplikasi yang _real-time_.

## WebRTC, sekumpulan protokol

WebRTC dapat menyelesaikan banyak masalah. Mungkin ini tampak berlebihan. Namun kelebihan dari WebRTC adalah kesederhanaannya. Ia tidak menyatakan bahwa ia dapat menyelesaikan semua permasalahan dengan lebih baik. Sebaliknya, ia memanfaatkan banyak terknologi terdahulu dan menggabungkannya bersama-sama.

Ini memungkinkan kita untuk mempelajari masing-masing bagian secara terpisah tanpa perlu membuat kewalahan. Cara yang benar untuk menggambarkannya adalah WebRTC sebenarnya hanyalah sekumpulan dari banyak protokol yang berbeda.

![WebRTC Agent](../images/01-webrtc-agent.png "WebRTC Agent Diagram")

## Bagaimana WebRTC (API) bekerja

Bagian ini akan menjelaskan kepada Anda bagaimana API JavaScript pada WebRTC. Ini bukan dimaksudkan untuk menunjukkan demo dari API WebRTC, namun sebatas menunjukkan contoh bagaimana API tersebut saling bekerja sama.

Jika Anda belum familier, tidak ada masalah. Ini akan menjadi bagian yang yang menyenangkan!

### `new RTCPeerConnection`

`RTCPeerConnection` adalah level teratas dari "_WebRTC Session_". Ini berisi semua protokol yang telah disebutkan sebelumnya. Semua subsistem yang bekerja di dalamnya telah dialokasikan, namun belum terjadi apa-apa.

### `addTrack`

`addTrack` berfungsi untuk membuat RTP _stream_ baru. Sebuah _Synchronization Source_ (SSRC) acak akan dibuat pada _stream_ tersebut. _Stream_ ini kemudian akan dimasukkan ke dalam _Session Description_ yang dibuat oleh `createOffer`. Setiap pemanggilan `addTrack` akan selalu membuat SSRC dan media baru.

Segera setelah sesi SRTP terbentuk, paket media ini akan dikirimkan melalui ICE setelah dienkripsi menggunakan SRTP.

### `createDataChannel`

`createDataChannel` berfungsi untuk membuat SCTP _stream_ baru jika tidak ada SCTP yang tersedia sebelumnya. Pada dasarnya SCTP tidak akan diinisiasi secara otomatis, kecuali salah satu pihak melakukan permintaan data _channel_.

Segera setelah sesi DTLS terbentuk, SCTP yang telah diinisiasi akan mulai mengirimkan paket melalui ICE dan dienkripsi menggunakan DTLS.

### `createOffer`

`createOffer` digunakan untuk membuat _Session Description_ di lokal yang kemudian akan dikirim ke _remote peer_ tujuan.

Pemanggilan `createOffer` tidak akan mengubah apapun di sisi _local peer_.

### `setLocalDescription`

`setLocalDescription` bertugas untuk melakukan perubahan yang dilakukan. `addTrack`, `createDataChannel`, dan fungsi lainnya tidak akan berlaku sampai fungsi ini dipanggil. `setLocalDescription` biasanya dipanggil dengan memuat SDP yang dihasilkan `createOffer`.

Biasanya setelah memanggil fungsi ini, Anda akan mengirimkan SDP _offer_ kepada _remote peer_ tujuan, dan mereka akan membalasnya dengan memanggil `setRemoteDescription`.

### `setRemoteDescription`

`setRemoteDescription` digunakan untuk menginformasikan _local peer_ mengenai SDP _remote peer_. Ini adalah bagaimana proses _signaling_ dilakukan dengan API JavaScript.

Ketika `setRemoteDescription` telah dipanggil pada kedua sisi, kedua klien WebRTC kini telah memiliki informasi yang cukup untuk saling berkomunikasi secara _Peer-To-Peer_ (P2P)!

### `addIceCandidate`

`addIceCandidate` memungkinkan klien WebRTC untuk menambahkan _remote_ ICE _Candidate_ kapanpun. API ini akan mengirimkan ICE _Candidate_ langsung ke dalam subsistem ICE dan tidak berpengaruh apapun terkait dengan sambungan WebRTC.

### `ontrack`

`ontrack` merupakan sebuah _callback_ yang dipanggil ketika ada sebuah paket RTP yang diterima dari _remote peer_. Paket yang datang telah didefinisikan sebelumnya pada _Session Description_ yang dikirimkan melalui `setRemoteDescription`.

WebRTC menggunakan SSRC dan akan mencari `MediaStream` dan `MediaStreamTrack` terkait, yang kemudian akan memanggil _callback_ ini dengan informasi tersebut.

### `oniceconnectionstatechange`

`oniceconnectionstatechange` merupakan sebuah _callback_ yang merupakan status dari ICE. Ketika Anda memiliki perubahan status dari jaringan atau terputus dari jaringan, ini merupakan cara Anda mengetahuinya.

### `onconnectionstatechange`

`onconnectionstatechange` adalah sebuah _callback_ yang merupakan gabungan dari status ICE dan DTLS. Anda bisa memanggil ini untuk mengetahui ketika ICE dan DTLS telah selesai diproses.
