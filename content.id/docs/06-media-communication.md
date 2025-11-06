---
title: Media Communication
type: docs
weight: 7
---

# Media Communication

## Apa yang saya dapatkan dari komunikasi media WebRTC?

WebRTC memungkinkan Anda mengirim dan menerima jumlah _stream_ audio dan video yang tidak terbatas. Anda dapat menambah dan menghapus _stream_ ini kapan saja selama panggilan. _Stream_ ini semuanya bisa independen, atau bisa digabungkan bersama! Anda dapat mengirim _feed_ video desktop Anda, dan kemudian menyertakan audio dan video dari _webcam_ Anda.

Protokol WebRTC adalah _codec agnostic_. Transpor yang mendasarinya mendukung semuanya, bahkan hal-hal yang belum ada! Namun, _Agent_ WebRTC yang berkomunikasi dengan Anda mungkin tidak memiliki alat yang diperlukan untuk menerimanya.

WebRTC juga dirancang untuk menangani kondisi jaringan yang dinamis. Selama panggilan _bandwidth_ Anda mungkin meningkat, atau menurun. Mungkin Anda tiba-tiba mengalami banyak _packet loss_. Protokol ini dirancang untuk menangani semua ini. WebRTC merespons kondisi jaringan dan mencoba memberi Anda pengalaman terbaik yang mungkin dengan sumber daya yang tersedia.

## Bagaimana cara kerjanya?
WebRTC menggunakan dua protokol yang sudah ada sebelumnya RTP dan RTCP, keduanya didefinisikan dalam [RFC 1889](https://tools.ietf.org/html/rfc1889).

RTP (_Real-time Transport Protocol_) adalah protokol yang membawa media. Ini dirancang untuk memungkinkan pengiriman video _real-time_. Ini tidak menetapkan aturan apa pun mengenai latensi atau keandalan, tetapi memberi Anda alat untuk mengimplementasikannya. RTP memberi Anda _stream_, sehingga Anda dapat menjalankan beberapa _feed_ media melalui satu koneksi. Ini juga memberi Anda informasi _timing_ dan pengurutan yang Anda butuhkan untuk memberi makan _pipeline_ media.

RTCP (_RTP Control Protocol_) adalah protokol yang mengomunikasikan metadata tentang panggilan. Formatnya sangat fleksibel dan memungkinkan Anda menambahkan metadata apa pun yang Anda inginkan. Ini digunakan untuk mengomunikasikan statistik tentang panggilan. Ini juga digunakan untuk menangani _packet loss_ dan untuk mengimplementasikan _congestion control_. Ini memberi Anda komunikasi dua arah yang diperlukan untuk merespons kondisi jaringan yang berubah.

## Latensi vs Kualitas
Media _real-time_ adalah tentang membuat _trade-off_ antara latensi dan kualitas. Semakin banyak latensi yang bersedia Anda toleransi, semakin tinggi kualitas video yang dapat Anda harapkan.

### Keterbatasan Dunia Nyata
Batasan ini semua disebabkan oleh keterbatasan dunia nyata. Ini semua adalah karakteristik jaringan Anda yang perlu Anda atasi.

### Video itu Kompleks
Mengangkut video tidaklah mudah. Untuk menyimpan 30 menit video 720 8-bit yang tidak dikompresi, Anda memerlukan sekitar 110 GB. Dengan angka-angka itu, panggilan konferensi 4 orang tidak akan terjadi. Kita memerlukan cara untuk membuatnya lebih kecil, dan jawabannya adalah kompresi video. Itu tidak datang tanpa kekurangan.

## Video 101
Kami tidak akan membahas kompresi video secara mendalam, tetapi cukup untuk memahami mengapa RTP dirancang seperti itu. Kompresi video mengenkode video ke dalam format baru yang memerlukan lebih sedikit bit untuk merepresentasikan video yang sama.

### Kompresi _Lossy_ dan _Lossless_
Anda dapat mengenkode video menjadi _lossless_ (tidak ada informasi yang hilang) atau _lossy_ (informasi mungkin hilang). Karena pengkodean _lossless_ memerlukan lebih banyak data yang dikirim ke _peer_, membuat _stream_ latensi lebih tinggi dan lebih banyak paket yang dijatuhkan, RTP biasanya menggunakan kompresi _lossy_ meskipun kualitas videonya tidak akan sebaik itu.

### Kompresi _Intra_ dan _Inter frame_
Kompresi video hadir dalam dua jenis. Yang pertama adalah _intra-frame_. Kompresi _intra-frame_ mengurangi bit yang digunakan untuk mendeskripsikan satu _frame_ video. Teknik yang sama digunakan untuk mengompresi gambar diam, seperti metode kompresi JPEG.

Jenis kedua adalah kompresi _inter-frame_. Karena video terdiri dari banyak gambar, kita mencari cara untuk tidak mengirim informasi yang sama dua kali.

### Jenis _Inter-frame_
Anda kemudian memiliki tiga jenis _frame_:

* **I-Frame** - Gambar lengkap, dapat didekode tanpa apa pun.
* **P-Frame** - Gambar parsial, hanya berisi perubahan dari gambar sebelumnya.
* **B-Frame** - Gambar parsial, adalah modifikasi dari gambar sebelumnya dan masa depan.

Berikut adalah visualisasi dari tiga jenis _frame_.

![Frame types](../images/06-frame-types.png "Frame types")

### Video itu rapuh
Kompresi video sangat _stateful_, membuatnya sulit untuk ditransfer melalui internet. Apa yang terjadi jika Anda kehilangan bagian dari I-Frame? Bagaimana P-Frame tahu apa yang harus dimodifikasi? Seiring kompresi video menjadi lebih kompleks, ini menjadi masalah yang lebih besar. Untungnya RTP dan RTCP memiliki solusinya.

## RTP
### Format Paket
Setiap paket RTP memiliki struktur berikut:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       Sequence Number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           Timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Synchronization Source (SSRC) identifier            |
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
|            Contributing Source (CSRC) identifiers             |
|                             ....                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
`Version` selalu `2`

#### Padding (P)
`Padding` adalah _bool_ yang mengontrol apakah _payload_ memiliki _padding_.

_Byte_ terakhir dari _payload_ berisi hitungan berapa banyak _byte padding_ yang ditambahkan.

#### Extension (X)
Jika disetel, _header_ RTP akan memiliki ekstensi. Ini dijelaskan lebih detail di bawah ini.

#### CSRC count (CC)
Jumlah pengidentifikasi `CSRC` yang mengikuti setelah `SSRC`, dan sebelum _payload_.

#### Marker (M)
_Marker bit_ tidak memiliki arti yang telah ditetapkan, dan dapat digunakan sesuai keinginan pengguna.

Dalam beberapa kasus, ini disetel ketika pengguna sedang berbicara. Ini juga biasanya digunakan untuk menandai _keyframe_.

#### Payload Type (PT)
`Payload Type` adalah pengidentifikasi unik untuk _codec_ apa yang dibawa oleh paket ini.

Untuk WebRTC, `Payload Type` adalah dinamis. VP8 dalam satu panggilan mungkin berbeda dari yang lain. _Offerer_ dalam panggilan menentukan pemetaan `Payload Types` ke _codec_ dalam `Session Description`.

#### Sequence Number
`Sequence Number` digunakan untuk mengurutkan paket dalam _stream_. Setiap kali paket dikirim, `Sequence Number` ditambah satu.

RTP dirancang agar berguna melalui jaringan yang _lossy_. Ini memberi penerima cara untuk mendeteksi kapan paket telah hilang.

#### Timestamp
Momen pengambilan sampel untuk paket ini. Ini bukan jam global, tetapi berapa banyak waktu yang telah berlalu dalam _stream_ media. Beberapa paket RTP dapat memiliki _timestamp_ yang sama jika mereka misalnya semua bagian dari _frame_ video yang sama.

#### Synchronization Source (SSRC)
`SSRC` adalah pengidentifikasi unik untuk _stream_ ini. Ini memungkinkan Anda menjalankan beberapa _stream_ media melalui satu _stream_ RTP.

#### Contributing Source (CSRC)
Daftar yang mengomunikasikan `SSRC` mana yang berkontribusi pada paket ini.

Ini biasanya digunakan untuk indikator berbicara. Katakanlah _server side_ Anda menggabungkan beberapa _feed_ audio menjadi satu _stream_ RTP. Anda kemudian dapat menggunakan bidang ini untuk mengatakan "Input _stream_ A dan C sedang berbicara pada saat ini".

#### Payload
Data _payload_ yang sebenarnya. Mungkin diakhiri dengan hitungan berapa banyak _byte padding_ yang ditambahkan, jika _flag padding_ disetel.

### Extensions

## RTCP

### Format Paket
Setiap paket RTCP memiliki struktur berikut:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|    RC   |       PT      |             length            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Payload                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Version (V)
`Version` selalu `2`.

#### Padding (P)
`Padding` adalah _bool_ yang mengontrol apakah _payload_ memiliki _padding_.

_Byte_ terakhir dari _payload_ berisi hitungan berapa banyak _byte padding_ yang ditambahkan.

#### Reception Report Count (RC)
Jumlah laporan dalam paket ini. Satu paket RTCP dapat berisi beberapa _event_.

#### Packet Type (PT)
Pengidentifikasi Unik untuk jenis paket RTCP apa ini. _Agent_ WebRTC tidak perlu mendukung semua jenis ini, dan dukungan antar _Agent_ dapat berbeda. Ini adalah yang mungkin sering Anda lihat:

* `192` - Full INTRA-frame Request (`FIR`)
* `193` - Negative ACKnowledgements (`NACK`)
* `200` - Sender Report
* `201` - Receiver Report
* `205` - Generic RTP Feedback
* `206` - Payload Specific Feedback

Signifikansi jenis paket ini akan dijelaskan lebih detail di bawah ini.

### Full INTRA-frame Request (FIR) dan Picture Loss Indication (PLI)
Pesan `FIR` dan `PLI` melayani tujuan yang serupa. Pesan-pesan ini meminta _key frame_ penuh dari pengirim.
`PLI` digunakan ketika _frame_ parsial diberikan ke _decoder_, tetapi tidak dapat mendekodenya.
Ini bisa terjadi karena Anda memiliki banyak _packet loss_, atau mungkin _decoder_ crash.

Menurut [RFC 5104](https://tools.ietf.org/html/rfc5104#section-4.3.1.2), `FIR` tidak boleh digunakan ketika paket atau _frame_ hilang. Itu adalah tugas `PLI`. `FIR` meminta _key frame_ untuk alasan selain _packet loss_ - misalnya ketika anggota baru memasuki konferensi video. Mereka memerlukan _key frame_ penuh untuk mulai mendekode _stream_ video, _decoder_ akan membuang _frame_ sampai _key frame_ tiba.

Ini adalah ide yang baik bagi penerima untuk meminta _key frame_ penuh segera setelah terhubung, ini meminimalkan penundaan antara koneksi, dan gambar yang muncul di layar pengguna.

Paket `PLI` adalah bagian dari pesan _Payload Specific Feedback_.

Dalam praktiknya, perangkat lunak yang dapat menangani paket `PLI` dan `FIR` akan bertindak dengan cara yang sama dalam kedua kasus. Ini akan mengirim sinyal ke _encoder_ untuk menghasilkan _key frame_ penuh yang baru.

### Negative Acknowledgment
`NACK` meminta pengirim mengirim ulang satu paket RTP. Ini biasanya disebabkan oleh paket RTP yang hilang, tetapi juga bisa terjadi karena terlambat.

`NACK` jauh lebih efisien _bandwidth_ daripada meminta seluruh _frame_ dikirim lagi. Karena RTP memecah paket menjadi potongan yang sangat kecil, Anda benar-benar hanya meminta satu bagian kecil yang hilang. Penerima membuat pesan RTCP dengan SSRC dan _Sequence Number_. Jika pengirim tidak memiliki paket RTP ini tersedia untuk dikirim ulang, ia hanya mengabaikan pesan tersebut.

### Sender dan Receiver Reports
Laporan ini digunakan untuk mengirim statistik antar _agent_. Ini mengomunikasikan jumlah paket yang benar-benar diterima dan _jitter_.

Laporan dapat digunakan untuk diagnostik dan _congestion control_.

## Bagaimana RTP/RTCP menyelesaikan masalah bersama-sama
RTP dan RTCP kemudian bekerja sama untuk menyelesaikan semua masalah yang disebabkan oleh jaringan. Teknik-teknik ini masih terus berubah!

### Forward Error Correction
Juga dikenal sebagai FEC. Metode lain untuk menangani _packet loss_. FEC adalah ketika Anda mengirim data yang sama beberapa kali, tanpa diminta. Ini dilakukan pada level RTP, atau bahkan lebih rendah dengan _codec_.

Jika _packet loss_ untuk panggilan stabil maka FEC adalah solusi latensi yang jauh lebih rendah daripada NACK. _Round trip time_ untuk meminta, dan kemudian mengirim ulang paket yang hilang bisa signifikan untuk NACK.

### Adaptive Bitrate dan Bandwidth Estimation
Seperti yang dibahas dalam bab [Real-time networking](../05-real-time-networking/), jaringan tidak dapat diprediksi dan tidak dapat diandalkan. Ketersediaan _bandwidth_ dapat berubah beberapa kali sepanjang sesi.
Tidak jarang melihat _bandwidth_ yang tersedia berubah secara dramatis (beberapa kali lipat) dalam satu detik.

Ide utamanya adalah menyesuaikan _bitrate_ pengkodean berdasarkan _bandwidth_ jaringan yang tersedia yang diprediksi, saat ini, dan masa depan.
Ini memastikan bahwa sinyal video dan audio dengan kualitas terbaik yang mungkin ditransmisikan, dan koneksi tidak terputus karena kemacetan jaringan.
Heuristik yang memodelkan perilaku jaringan dan mencoba memprediksinya dikenal sebagai _Bandwidth estimation_.

Ada banyak nuansa untuk ini, jadi mari kita jelajahi lebih detail.

## Mengidentifikasi dan Mengomunikasikan Status Jaringan
RTP/RTCP berjalan di atas semua jenis jaringan yang berbeda, dan sebagai hasilnya, adalah umum untuk beberapa
komunikasi dijatuhkan dalam perjalanan dari pengirim ke penerima. Dibangun di atas UDP,
tidak ada mekanisme bawaan untuk retransmisi paket, apalagi menangani _congestion control_.

Untuk memberikan pengalaman terbaik kepada pengguna, WebRTC harus memperkirakan kualitas tentang jalur jaringan, dan
beradaptasi dengan bagaimana kualitas tersebut berubah dari waktu ke waktu. Sifat kunci untuk dipantau meliputi: _bandwidth_ yang tersedia (di setiap arah, karena mungkin tidak simetris), _round trip time_, dan _jitter_ (fluktuasi
dalam _round trip time_). Ini perlu memperhitungkan _packet loss_, dan mengomunikasikan perubahan dalam properti ini seiring kondisi jaringan berkembang.

Ada dua tujuan utama untuk protokol ini:

1. Memperkirakan _bandwidth_ yang tersedia (di setiap arah) yang didukung oleh jaringan.
2. Mengomunikasikan karakteristik jaringan antara pengirim dan penerima.

RTP/RTCP memiliki tiga pendekatan berbeda untuk mengatasi masalah ini. Semuanya memiliki pro dan kontra,
dan umumnya setiap generasi telah meningkat dari pendahulunya. Implementasi mana yang Anda gunakan akan
bergantung terutama pada _stack_ perangkat lunak yang tersedia untuk klien Anda dan _library_ yang tersedia untuk
membangun aplikasi Anda.

### Receiver Reports / Sender Reports
Implementasi pertama adalah pasangan _Receiver Reports_ dan komplemennya, _Sender Reports_. Ini
pesan RTCP didefinisikan dalam [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4), dan
bertanggung jawab untuk mengomunikasikan status jaringan antar _endpoint_. _Receiver Reports_ berfokus pada
mengomunikasikan kualitas tentang jaringan (termasuk _packet loss_, _round-trip time_, dan _jitter_), dan
berpasangan dengan algoritma lain yang kemudian bertanggung jawab untuk memperkirakan _bandwidth_ yang tersedia berdasarkan
laporan ini.

_Sender_ dan _Receiver report_ (SR dan RR) bersama-sama melukiskan gambaran kualitas jaringan. Mereka
dikirim sesuai jadwal untuk setiap SSRC, dan mereka adalah input yang digunakan saat memperkirakan _bandwidth_ yang tersedia. Perkiraan tersebut dibuat oleh pengirim setelah menerima data RR, yang berisi
bidang-bidang berikut:

* **Fraction Lost** - Berapa persentase paket yang hilang sejak _Receiver Report_ terakhir.
* **Cumulative Number of Packets Lost** - Berapa banyak paket yang hilang selama seluruh panggilan.
* **Extended Highest Sequence Number Received** - Apa _Sequence Number_ terakhir yang diterima, dan
  berapa kali telah berputar.
* **Interarrival Jitter** - _Jitter_ bergulir untuk seluruh panggilan.
* **Last Sender Report Timestamp** - Waktu terakhir yang diketahui pada pengirim, digunakan untuk perhitungan _round-trip time_.

SR dan RR bekerja bersama untuk menghitung _round-trip time_.

Pengirim menyertakan waktu lokalnya, `sendertime1` dalam SR. Ketika penerima mendapat paket SR, ia
mengirim kembali RR. Di antara hal-hal lain, RR menyertakan `sendertime1` yang baru saja diterima dari pengirim.
Akan ada penundaan antara menerima SR dan mengirim RR. Karena itu, RR juga
menyertakan waktu "delay since last sender report" - `DLSR`. `DLSR` digunakan untuk menyesuaikan
perkiraan _round-trip time_ nanti dalam proses. Setelah pengirim menerima RR, ia mengurangi
`sendertime1` dan `DLSR` dari waktu saat ini `sendertime2`. Delta waktu ini disebut _round-trip
propagation delay_ atau _round-trip time_.

`rtt = sendertime2 - sendertime1 - DLSR`

_Round-trip time_ dalam bahasa Inggris sederhana:
- Saya mengirim Anda pesan dengan pembacaan jam saya saat ini, katakanlah jam 4:20 sore, 42 detik dan 420 milidetik.
- Anda mengirim saya _timestamp_ yang sama ini kembali.
- Anda juga menyertakan waktu yang berlalu dari membaca pesan saya hingga mengirim pesan kembali, katakanlah 5 milidetik.
- Setelah saya menerima waktu kembali, saya melihat jam lagi.
- Sekarang jam saya mengatakan jam 4:20 sore, 42 detik 690 milidetik.
- Itu berarti dibutuhkan 265 milidetik (690 - 420 - 5) untuk mencapai Anda dan kembali ke saya.
- Oleh karena itu, _round-trip time_ adalah 265 milidetik.

![Round-trip time](../images/06-rtt.png "Round-trip time")

<!-- Missing: What is an example congestion-control alg that pairs with RR/SR? -->

### TMMBR, TMMBN, REMB dan TWCC, dipasangkan dengan GCC

#### Google Congestion Control (GCC)
Algoritma _Google Congestion Control_ (GCC) (dijelaskan dalam
[draft-ietf-rmcat-gcc-02](https://tools.ietf.org/html/draft-ietf-rmcat-gcc-02)) mengatasi
tantangan estimasi _bandwidth_. Ini berpasangan dengan berbagai protokol lain untuk memfasilitasi
persyaratan komunikasi terkait. Akibatnya, ini sangat cocok untuk berjalan baik di sisi
penerima (ketika dijalankan dengan TMMBR/TMMBN atau REMB) atau di sisi pengirim (ketika dijalankan dengan TWCC).

Untuk mencapai perkiraan untuk _bandwidth_ yang tersedia, GCC berfokus pada _packet loss_ dan fluktuasi dalam waktu
kedatangan _frame_ sebagai dua metrik utamanya. Ini menjalankan metrik ini melalui dua _controller_ yang terhubung:
_controller_ berbasis kehilangan dan _controller_ berbasis penundaan.

Komponen pertama GCC, _loss-based controller_, sederhana:

* Jika _packet loss_ di atas 10%, perkiraan _bandwidth_ dikurangi.
* Jika _packet loss_ antara 2-10%, perkiraan _bandwidth_ tetap sama.
* Jika _packet loss_ di bawah 2%, perkiraan _bandwidth_ ditingkatkan.

Pengukuran _packet loss_ dilakukan dengan sering. Tergantung pada protokol komunikasi berpasangan,
_packet loss_ dapat dikomunikasikan secara eksplisit (seperti dengan TWCC) atau disimpulkan (seperti dengan TMMBR/TMMBN
dan REMB). Persentase ini dievaluasi melalui jendela waktu sekitar satu detik.

_Delay-based controller_ bekerja sama dengan _loss-based controller_, dan melihat variasi dalam 
waktu kedatangan paket. _Delay-based controller_ ini bertujuan untuk mengidentifikasi kapan tautan jaringan menjadi
semakin padat, dan dapat mengurangi perkiraan _bandwidth_ bahkan sebelum _packet loss_ terjadi.
Teorinya adalah bahwa antarmuka jaringan yang paling sibuk di sepanjang jalur akan terus mengantri paket
sampai antarmuka kehabisan kapasitas di dalam _buffer_-nya. Jika antarmuka itu terus menerima
lebih banyak lalu lintas daripada yang dapat dikirimnya, ia akan dipaksa untuk menjatuhkan semua paket yang tidak dapat masuk ke dalam
ruang _buffer_-nya. Jenis _packet loss_ ini sangat mengganggu untuk komunikasi latensi rendah/_real-time_,
tetapi juga dapat menurunkan throughput untuk semua komunikasi melalui tautan itu dan idealnya
harus dihindari. Dengan demikian, GCC mencoba mencari tahu apakah tautan jaringan menumbuhkan kedalaman antrian yang semakin besar dan lebih besar _sebelum_ _packet loss_ benar-benar terjadi. Ini akan mengurangi penggunaan _bandwidth_ jika mengamati
peningkatan penundaan antrian dari waktu ke waktu.

Untuk mencapai ini, GCC mencoba menyimpulkan peningkatan kedalaman antrian dengan mengukur peningkatan halus dalam _round
trip time_. Ini mencatat "inter-arrival time" _frame_, `t(i) - t(i-1)`: perbedaan waktu kedatangan
dari dua kelompok paket (umumnya, _frame_ video berturut-turut). Kelompok paket ini sering
berangkat pada interval waktu yang teratur (misalnya setiap 1/24 detik untuk video 24 fps). Sebagai hasilnya,
mengukur _inter-arrival time_ kemudian sesederhana merekam perbedaan waktu antara awal dari
kelompok paket pertama (yaitu _frame_) dan _frame_ pertama dari yang berikutnya.

Dalam diagram di bawah ini, peningkatan penundaan _inter-packet_ median adalah +20 milidetik, indikator yang jelas dari
kemacetan jaringan.

![TWCC with delay](../images/06-twcc.png "TWCC with delay")

Jika _inter-arrival time_ meningkat dari waktu ke waktu, itu dianggap bukti peningkatan kedalaman antrian pada
antarmuka jaringan yang menghubungkan dan dianggap kemacetan jaringan. (Catatan: GCC cukup pintar untuk
mengontrol pengukuran ini untuk fluktuasi dalam ukuran _byte frame_.) GCC memperbaiki pengukuran latensinya menggunakan [filter Kalman](https://en.wikipedia.org/wiki/Kalman_filter) dan mengambil banyak
pengukuran _round-trip time_ jaringan (dan variasinya) sebelum menandai kemacetan. Orang dapat
menganggap filter Kalman GCC sebagai pengganti regresi linier: membantu membuat prediksi yang akurat
bahkan ketika _jitter_ menambahkan kebisingan ke dalam pengukuran _timing_. Setelah menandai kemacetan, GCC
akan mengurangi _bitrate_ yang tersedia. Atau, dalam kondisi jaringan yang stabil, ia dapat perlahan-lahan
meningkatkan perkiraan _bandwidth_-nya untuk menguji nilai beban yang lebih tinggi.

#### TMMBR, TMMBN, dan REMB
Untuk TMMBR/TMMBN dan REMB, sisi penerima pertama-tama memperkirakan _bandwidth_ masuk yang tersedia (menggunakan
protokol seperti GCC), dan kemudian mengomunikasikan perkiraan _bandwidth_ ini ke pengirim _remote_. Mereka
tidak perlu bertukar detail tentang _packet loss_ atau kualitas lain tentang kemacetan jaringan
karena beroperasi di sisi penerima memungkinkan mereka mengukur _inter-arrival time_ dan _packet loss_
secara langsung. Sebaliknya, TMMBR, TMMBN, dan REMB hanya bertukar perkiraan _bandwidth_ itu sendiri:

* **Temporary Maximum Media Stream Bit Rate Request** - Mantissa/eksponen dari _bitrate_ yang diminta
  untuk satu SSRC.
* **Temporary Maximum Media Stream Bit Rate Notification** - Pesan untuk memberi tahu bahwa TMMBR telah
  diterima.
* **Receiver Estimated Maximum Bitrate** - Mantissa/eksponen dari _bitrate_ yang diminta untuk
  seluruh sesi.

TMMBR dan TMMBN datang pertama dan didefinisikan dalam [RFC 5104](https://tools.ietf.org/html/rfc5104). REMB
datang kemudian, ada _draft_ yang diajukan dalam
[draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03), tetapi
tidak pernah distandarisasi.

Contoh sesi yang menggunakan REMB mungkin berperilaku seperti berikut:

![REMB](../images/06-remb.png "REMB")

Metode ini bekerja dengan baik di atas kertas. Pengirim menerima estimasi dari penerima, mengatur _bitrate encoder_ ke nilai yang diterima. Tada! Kami telah menyesuaikan dengan kondisi jaringan.

Namun dalam praktiknya, pendekatan REMB memiliki beberapa kekurangan.

Ketidakefisienan _encoder_ adalah yang pertama. Ketika Anda menetapkan _bitrate_ untuk _encoder_, itu tidak selalu
menghasilkan _bitrate_ yang tepat yang Anda minta. Pengkodean dapat menghasilkan lebih banyak atau lebih sedikit bit, tergantung pada
pengaturan _encoder_ dan _frame_ yang dikode.

Misalnya, menggunakan _encoder_ x264 dengan `tune=zerolatency` dapat secara signifikan menyimpang dari _target bitrate_ yang ditentukan. Berikut adalah skenario yang mungkin:

- Katakanlah kita mulai dengan mengatur _bitrate_ ke 1000 kbps.
- _Encoder_ hanya menghasilkan 700 kbps, karena tidak ada cukup fitur frekuensi tinggi untuk dikode. (AKA - "menatap dinding".)
- Mari kita juga bayangkan bahwa penerima mendapat video 700 kbps dengan nol _packet loss_. Kemudian ia menerapkan aturan REMB 1 untuk meningkatkan _bitrate_ masuk sebesar 8%.
- Penerima mengirim paket REMB dengan saran 756 kbps (700 kbps * 1.08) ke pengirim.
- Pengirim mengatur _bitrate encoder_ ke 756 kbps.
- _Encoder_ menghasilkan _bitrate_ yang lebih rendah lagi.
- Proses ini terus berulang, menurunkan _bitrate_ ke minimum absolut.

Anda dapat melihat bagaimana ini akan menyebabkan penyetelan parameter _encoder_ yang berat, dan mengejutkan pengguna dengan video yang tidak dapat ditonton bahkan pada koneksi yang bagus.

#### Transport Wide Congestion Control
_Transport Wide Congestion Control_ adalah perkembangan terbaru dalam komunikasi status jaringan RTCP. Ini didefinisikan dalam
[draft-holmer-rmcat-transport-wide-cc-extensions-01](https://datatracker.ietf.org/doc/html/draft-holmer-rmcat-transport-wide-cc-extensions-01),
tetapi juga tidak pernah distandarisasi.

TWCC menggunakan prinsip yang cukup sederhana:

![TWCC](../images/06-twcc-idea.png "TWCC")

Dengan REMB, penerima menginstruksikan sisi pengirim dalam _bitrate download_ yang tersedia. Ini menggunakan
pengukuran yang tepat tentang _packet loss_ yang disimpulkan dan data hanya yang dimilikinya tentang waktu kedatangan _inter-packet_.

TWCC hampir merupakan pendekatan hibrida antara SR/RR dan generasi protokol REMB. Ini membawa
perkiraan _bandwidth_ kembali ke sisi pengirim (mirip dengan SR/RR), tetapi teknik estimasi _bandwidth_-nya
lebih mirip dengan generasi REMB.

Dengan TWCC, penerima memberi tahu pengirim waktu kedatangan setiap paket. Ini adalah informasi yang cukup
untuk pengirim mengukur variasi penundaan kedatangan _inter-packet_, serta mengidentifikasi
paket mana yang dijatuhkan atau tiba terlambat untuk berkontribusi pada _feed_ audio/video. Dengan data ini
yang dipertukarkan dengan sering, pengirim dapat dengan cepat menyesuaikan dengan kondisi jaringan yang berubah dan
bervariasi _output bandwidth_-nya menggunakan algoritma seperti GCC.

Pengirim melacak paket yang dikirim, nomor urutnya, ukuran dan _timestamp_. Ketika
pengirim menerima pesan RTCP dari penerima, ia membandingkan penundaan _inter-packet_ pengiriman dengan
penundaan penerimaan. Jika penundaan penerimaan meningkat, ini menandakan kemacetan jaringan, dan pengirim
harus mengambil tindakan korektif.

Dengan memberikan pengirim data mentah, TWCC menyediakan pandangan yang sangat baik ke dalam kondisi jaringan _real time_:
- Perilaku _packet loss_ hampir instan, hingga paket individual yang hilang
- _Bitrate_ pengiriman yang akurat
- _Bitrate_ penerimaan yang akurat
- Pengukuran _jitter_
- Perbedaan antara penundaan paket pengiriman dan penerimaan
- Deskripsi tentang bagaimana jaringan mentolerir pengiriman _bandwidth_ yang _bursty_ atau stabil

Salah satu kontribusi paling signifikan dari TWCC adalah fleksibilitas yang diberikannya kepada _developer_ WebRTC. Dengan mengkonsolidasikan algoritma _congestion control_ ke sisi pengirim, ini memungkinkan kode klien sederhana yang dapat digunakan secara luas dan memerlukan peningkatan minimal dari waktu ke waktu. Algoritma _congestion control_ yang kompleks kemudian dapat diiterasi lebih cepat pada perangkat keras yang mereka kontrol langsung (seperti _Selective Forwarding Unit_, dibahas di bagian 8). Dalam kasus peramban dan perangkat seluler, ini berarti klien tersebut dapat mengambil manfaat dari peningkatan algoritma tanpa harus menunggu standardisasi atau pembaruan peramban (yang dapat memakan waktu cukup lama untuk tersedia secara luas).

## Alternatif Bandwidth Estimation
Implementasi yang paling banyak diterapkan adalah "A Google Congestion Control Algorithm for Real-Time
Communication" yang didefinisikan dalam
[draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02).

Ada beberapa alternatif untuk GCC, misalnya [NADA: A Unified Congestion Control Scheme for
Real-Time Media](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) dan [SCReAM - Self-Clocked
Rate Adaptation for Multimedia](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
