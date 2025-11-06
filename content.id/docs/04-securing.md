---
title: Securing
type: docs
weight: 5
---

# Securing

## Keamanan apa yang dimiliki WebRTC?

Setiap koneksi WebRTC diautentikasi dan dienkripsi. Anda dapat yakin bahwa pihak ketiga tidak dapat melihat apa yang Anda kirim atau menyisipkan pesan palsu. Anda juga dapat yakin bahwa klien WebRTC yang membuat Session Description adalah yang Anda komunikasikan dengannya.

Sangat penting bahwa tidak ada yang merusak pesan-pesan tersebut. Tidak apa-apa jika pihak ketiga membaca Session Description saat transit. Namun, WebRTC tidak memiliki perlindungan terhadap modifikasinya. Penyerang dapat melakukan serangan _man-in-the-middle_ pada Anda dengan mengubah ICE Candidate dan memperbarui _Certificate Fingerprint_.

## Bagaimana cara kerjanya?
WebRTC menggunakan dua protokol yang sudah ada sebelumnya, Datagram Transport Layer Security ([DTLS](https://tools.ietf.org/html/rfc6347)) dan Secure Real-time Transport Protocol ([SRTP](https://tools.ietf.org/html/rfc3711)).

DTLS memungkinkan Anda untuk menegosiasikan sesi dan kemudian bertukar data secara aman antara dua _peer_. Ini adalah saudara dari TLS, teknologi yang sama yang mendukung HTTPS, tetapi DTLS menggunakan UDP alih-alih TCP sebagai _transport layer_. Itu berarti protokol harus menangani pengiriman yang tidak andal. SRTP dirancang khusus untuk bertukar media secara aman. Ada beberapa optimisasi yang dapat kita lakukan dengan menggunakannya daripada DTLS.

DTLS digunakan terlebih dahulu. Ia melakukan _handshake_ melalui koneksi yang disediakan oleh ICE. DTLS adalah protokol _client/server_, jadi satu sisi perlu memulai _handshake_. Peran _Client/Server_ dipilih selama _signaling_. Selama _handshake_ DTLS, kedua sisi menawarkan sertifikat.
Setelah _handshake_ selesai, sertifikat ini dibandingkan dengan _hash_ sertifikat di Session Description. Ini untuk memastikan bahwa _handshake_ terjadi dengan klien WebRTC yang Anda harapkan. Koneksi DTLS kemudian tersedia untuk digunakan untuk komunikasi DataChannel.

Untuk membuat sesi SRTP kita menginisialisasinya menggunakan kunci yang dihasilkan oleh DTLS. SRTP tidak memiliki mekanisme _handshake_, jadi harus di-_bootstrap_ dengan kunci eksternal. Setelah ini selesai, media dapat dipertukarkan yang dienkripsi menggunakan SRTP!

## Security 101
Untuk memahami teknologi yang disajikan dalam bab ini, Anda perlu memahami istilah-istilah ini terlebih dahulu. Kriptografi adalah subjek yang rumit, jadi akan bermanfaat untuk berkonsultasi dengan sumber lain juga!

### _Plaintext_ dan _Ciphertext_

_Plaintext_ adalah input ke _cipher_. _Ciphertext_ adalah output dari _cipher_.

### _Cipher_

_Cipher_ adalah serangkaian langkah yang mengubah _plaintext_ menjadi _ciphertext_. _Cipher_ kemudian dapat dibalik, sehingga Anda dapat mengubah _ciphertext_ Anda kembali ke _plaintext_. _Cipher_ biasanya memiliki kunci untuk mengubah perilakunya. Istilah lain untuk ini adalah enkripsi dan dekripsi.

_Cipher_ sederhana adalah ROT13. Setiap huruf dipindahkan 13 karakter ke depan. Untuk membatalkan _cipher_ Anda memindahkan 13 karakter ke belakang. _Plaintext_ `HELLO` akan menjadi _ciphertext_ `URYYB`. Dalam hal ini, _Cipher_ adalah ROT, dan kuncinya adalah 13.

### Fungsi _Hash_

Fungsi _hash_ kriptografi adalah proses satu arah yang menghasilkan _digest_. Diberikan input, ia menghasilkan output yang sama setiap kali. Penting bahwa outputnya *tidak* dapat dibalik. Jika Anda memiliki output, Anda seharusnya tidak dapat menentukan inputnya. _Hashing_ berguna ketika Anda ingin mengonfirmasi bahwa pesan tidak dirusak.

Fungsi _hash_ sederhana (walaupun tentu tidak cocok untuk kriptografi nyata) adalah hanya mengambil setiap huruf lainnya. `HELLO` akan menjadi `HLO`. Anda tidak dapat mengasumsikan `HELLO` adalah inputnya, tetapi Anda dapat mengonfirmasi bahwa `HELLO` akan cocok dengan _digest hash_.

### Kriptografi _Public/Private Key_

Kriptografi _Public/Private Key_ menggambarkan jenis _cipher_ yang digunakan DTLS dan SRTP. Dalam sistem ini, Anda memiliki dua kunci, kunci publik dan pribadi. Kunci publik untuk mengenkripsi pesan dan aman untuk dibagikan.
Kunci pribadi untuk mendekripsi, dan tidak boleh dibagikan. Ini adalah satu-satunya kunci yang dapat mendekripsi pesan yang dienkripsi dengan kunci publik.

### Pertukaran Diffie–Hellman

Pertukaran Diffie–Hellman memungkinkan dua pengguna yang tidak pernah bertemu sebelumnya untuk membuat _shared secret_ secara aman melalui internet. Pengguna `A` dapat mengirim rahasia ke Pengguna `B` tanpa khawatir tentang penyadapan. Ini bergantung pada kesulitan memecahkan masalah logaritma diskrit.
Anda tidak perlu sepenuhnya memahami bagaimana ini bekerja, tetapi ini membantu untuk mengetahui inilah yang membuat _handshake_ DTLS mungkin.

Wikipedia memiliki contoh ini dalam tindakan [di sini](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation).

### Fungsi _Pseudorandom_

Fungsi _Pseudorandom_ (PRF) adalah fungsi yang telah ditentukan untuk menghasilkan nilai yang tampak acak. Ini mungkin mengambil beberapa input dan menghasilkan satu output.

### Fungsi Derivasi Kunci

Derivasi Kunci adalah jenis Fungsi _Pseudorandom_. Derivasi Kunci adalah fungsi yang digunakan untuk membuat kunci lebih kuat. Satu pola umum adalah _key stretching_.

Katakanlah Anda diberi kunci yang berukuran 8 byte. Anda dapat menggunakan KDF untuk membuatnya lebih kuat.

### _Nonce_

_Nonce_ adalah input tambahan ke _cipher_. Ini digunakan sehingga Anda bisa mendapatkan output yang berbeda dari _cipher_, bahkan jika Anda mengenkripsi pesan yang sama beberapa kali.

Jika Anda mengenkripsi pesan yang sama 10 kali, _cipher_ akan memberi Anda _ciphertext_ yang sama 10 kali. Dengan menggunakan _nonce_ Anda dapat mendapatkan output yang berbeda, sambil tetap menggunakan kunci yang sama. Penting Anda menggunakan _nonce_ yang berbeda untuk setiap pesan! Jika tidak, itu meniadakan banyak nilainya.

### _Message Authentication Code_

_Message Authentication Code_ adalah _hash_ yang ditempatkan di akhir pesan. MAC membuktikan bahwa pesan berasal dari pengguna yang Anda harapkan.

Jika Anda tidak menggunakan MAC, penyerang dapat menyisipkan pesan yang tidak valid. Setelah mendekripsi Anda hanya akan mendapatkan sampah karena mereka tidak tahu kuncinya.

### Rotasi Kunci

Rotasi Kunci adalah praktik mengubah kunci Anda pada interval. Ini membuat kunci yang dicuri kurang berdampak. Jika kunci dicuri atau bocor, lebih sedikit data yang dapat didekripsi.

## DTLS
DTLS (Datagram Transport Layer Security) memungkinkan dua _peer_ untuk membangun komunikasi yang aman tanpa konfigurasi yang sudah ada sebelumnya. Bahkan jika seseorang menguping percakapan, mereka tidak akan dapat mendekripsi pesan.

Untuk DTLS Client dan Server berkomunikasi, mereka perlu menyetujui _cipher_ dan kunci. Mereka menentukan nilai-nilai ini dengan melakukan _handshake_ DTLS. Selama _handshake_, pesan dalam _plaintext_.
Ketika DTLS Client/Server telah bertukar cukup detail untuk mulai mengenkripsi, ia mengirim `Change Cipher Spec`. Setelah pesan ini, setiap pesan berikutnya akan dienkripsi!

### Format Paket
Setiap paket DTLS dimulai dengan _header_.

#### Content Type
Anda dapat mengharapkan tipe berikut:

* `20` - Change Cipher Spec
* `22` - Handshake
* `23` - Application Data

`Handshake` digunakan untuk bertukar detail untuk memulai sesi. `Change Cipher Spec` digunakan untuk memberi tahu sisi lain bahwa semuanya akan dienkripsi. `Application Data` adalah pesan yang dienkripsi.

#### Version
Version dapat berupa `0x0000feff` (DTLS v1.0) atau `0x0000fefd` (DTLS v1.2) tidak ada v1.1.

#### Epoch
Epoch dimulai dari `0`, tetapi menjadi `1` setelah `Change Cipher Spec`. Pesan apa pun dengan epoch non-nol dienkripsi.

#### Sequence Number
Sequence Number digunakan untuk menjaga pesan tetap teratur. Setiap pesan meningkatkan Sequence Number. Ketika epoch bertambah, Sequence Number dimulai dari awal.

#### Length dan Payload
Payload adalah `Content Type` spesifik. Untuk `Application Data`, `Payload` adalah data yang dienkripsi. Untuk `Handshake` akan berbeda tergantung pada pesannya. Panjang adalah untuk seberapa besar `Payload`.

### _Handshake State Machine_
Selama _handshake_, Client/Server bertukar serangkaian pesan. Pesan-pesan ini dikelompokkan ke dalam _flight_. Setiap _flight_ mungkin memiliki beberapa pesan di dalamnya (atau hanya satu).
_Flight_ tidak lengkap sampai semua pesan dalam _flight_ telah diterima. Kami akan menjelaskan tujuan setiap pesan lebih detail di bawah ini.

![Handshake](../images/04-handshake.png "Handshake")

#### ClientHello
ClientHello adalah pesan awal yang dikirim oleh _client_. Ini berisi daftar atribut. Atribut ini memberi tahu _server_ _cipher_ dan fitur yang didukung _client_. Untuk WebRTC ini adalah bagaimana kita memilih SRTP Cipher juga. Ini juga berisi data acak yang akan digunakan untuk menghasilkan kunci untuk sesi.

#### HelloVerifyRequest
HelloVerifyRequest dikirim oleh _server_ ke _client_. Ini untuk memastikan bahwa _client_ bermaksud mengirim permintaan. _Client_ kemudian mengirim ulang ClientHello, tetapi dengan _token_ yang disediakan dalam HelloVerifyRequest.

#### ServerHello
ServerHello adalah respons oleh _server_ untuk konfigurasi sesi ini. Ini berisi _cipher_ apa yang akan digunakan ketika sesi ini selesai. Ini juga berisi data acak _server_.

#### Certificate
Certificate berisi sertifikat untuk Client atau Server. Ini digunakan untuk mengidentifikasi secara unik dengan siapa kita berkomunikasi. Setelah _handshake_ selesai, kita akan memastikan sertifikat ini ketika di-_hash_ cocok dengan _fingerprint_ di `SessionDescription`.

#### ServerKeyExchange/ClientKeyExchange
Pesan ini digunakan untuk mengirimkan kunci publik. Saat startup, _client_ dan _server_ keduanya menghasilkan _keypair_. Setelah _handshake_ nilai-nilai ini akan digunakan untuk menghasilkan `Pre-Master Secret`.

#### CertificateRequest
CertificateRequest dikirim oleh _server_ yang memberi tahu _client_ bahwa ia menginginkan sertifikat. _Server_ dapat Meminta atau Mengharuskan sertifikat.

#### ServerHelloDone
ServerHelloDone memberi tahu _client_ bahwa _server_ selesai dengan _handshake_.

#### CertificateVerify
CertificateVerify adalah bagaimana pengirim membuktikan bahwa ia memiliki kunci pribadi yang dikirim dalam pesan Certificate.

#### ChangeCipherSpec
ChangeCipherSpec memberi tahu penerima bahwa segala sesuatu yang dikirim setelah pesan ini akan dienkripsi.

#### Finished
Finished dienkripsi dan berisi _hash_ dari semua pesan. Ini untuk menegaskan bahwa _handshake_ tidak dirusak.

### Pembuatan Kunci
Setelah _Handshake_ selesai, Anda dapat mulai mengirim data terenkripsi. _Cipher_ dipilih oleh _server_ dan ada di ServerHello. Bagaimana kuncinya dipilih?

Pertama kita menghasilkan `Pre-Master Secret`. Untuk mendapatkan nilai ini, Diffie–Hellman digunakan pada kunci yang dipertukarkan oleh `ServerKeyExchange` dan `ClientKeyExchange`. Detailnya berbeda tergantung pada _Cipher_ yang dipilih.

Selanjutnya `Master Secret` dihasilkan. Setiap versi DTLS memiliki `Pseudorandom function` yang ditentukan. Untuk DTLS 1.2 fungsi tersebut mengambil `Pre-Master Secret` dan nilai acak di `ClientHello` dan `ServerHello`.
Output dari menjalankan `Pseudorandom Function` adalah `Master Secret`. `Master Secret` adalah nilai yang digunakan untuk _Cipher_.

### Bertukar ApplicationData
Kuda beban DTLS adalah `ApplicationData`. Sekarang kita memiliki _cipher_ yang diinisialisasi, kita dapat mulai mengenkripsi dan mengirimkan nilai.

Pesan `ApplicationData` menggunakan _header_ DTLS seperti yang dijelaskan sebelumnya. `Payload` diisi dengan _ciphertext_. Anda sekarang memiliki Sesi DTLS yang berfungsi dan dapat berkomunikasi dengan aman.

DTLS memiliki banyak fitur menarik lainnya seperti renegosiasi. Mereka tidak digunakan oleh WebRTC, jadi tidak akan dibahas di sini.

## SRTP
SRTP adalah protokol yang dirancang khusus untuk mengenkripsi paket RTP. Untuk memulai sesi SRTP Anda menentukan kunci dan _cipher_ Anda. Tidak seperti DTLS ia tidak memiliki mekanisme _handshake_. Semua konfigurasi dan kunci dihasilkan selama _handshake_ DTLS.

DTLS menyediakan API khusus untuk mengekspor kunci yang akan digunakan oleh proses lain. Ini didefinisikan dalam [RFC 5705](https://tools.ietf.org/html/rfc5705).

### Pembuatan Sesi
SRTP mendefinisikan Key Derivation Function yang digunakan pada input. Ketika membuat Sesi SRTP, input dijalankan melalui ini untuk menghasilkan kunci kita untuk SRTP Cipher kita. Setelah ini Anda dapat melanjutkan untuk memproses media.

### Bertukar Media
Setiap paket RTP memiliki SequenceNumber 16 bit. SequenceNumber ini digunakan untuk menjaga paket tetap teratur, seperti Primary Key. Selama panggilan ini akan berputar. SRTP melacaknya dan menyebutnya _rollover counter_.

Ketika mengenkripsi paket, SRTP menggunakan _rollover counter_ dan _sequence number_ sebagai _nonce_. Ini untuk memastikan bahwa bahkan jika Anda mengirim data yang sama dua kali, _ciphertext_ akan berbeda. Ini penting untuk mencegah penyerang mengidentifikasi pola atau mencoba serangan _replay_.
