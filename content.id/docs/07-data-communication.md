---
title: Data Communication
type: docs
weight: 8
---

# Data Communication

## Apa yang saya dapatkan dari komunikasi data WebRTC?

WebRTC menyediakan _data channel_ untuk komunikasi data. Antara dua _peer_ Anda dapat membuka 65.534 _data channel_.
_Data channel_ berbasis datagram, dan masing-masing memiliki pengaturan daya tahan sendiri. Secara default, setiap _data channel_ memiliki pengiriman berurutan yang dijamin.

Jika Anda mendekati WebRTC dari latar belakang media, _data channel_ mungkin tampak boros. Mengapa saya memerlukan seluruh subsistem ini ketika saya bisa menggunakan HTTP atau WebSocket?

Kekuatan sebenarnya dengan _data channel_ adalah Anda dapat mengonfigurasinya untuk berperilaku seperti UDP dengan pengiriman tidak berurutan/_lossy_.
Ini diperlukan untuk situasi latensi rendah dan kinerja tinggi. Anda dapat mengukur _backpressure_ dan memastikan Anda hanya mengirim sebanyak yang didukung jaringan Anda.

## Bagaimana cara kerjanya?
WebRTC menggunakan _Stream Control Transmission Protocol_ (SCTP), didefinisikan dalam [RFC 4960](https://tools.ietf.org/html/rfc4960). SCTP adalah
protokol lapisan transpor yang dimaksudkan sebagai alternatif untuk TCP atau UDP. Untuk WebRTC kami menggunakannya sebagai protokol lapisan aplikasi yang berjalan di atas koneksi DTLS kami.

SCTP memberi Anda _stream_ dan setiap _stream_ dapat dikonfigurasi secara independen. _Data channel_ WebRTC hanyalah abstraksi tipis di sekitarnya. Pengaturan
sekitar daya tahan dan pengurutan hanya diteruskan langsung ke _Agent_ SCTP.

_Data channel_ memiliki beberapa fitur yang tidak dapat diekspresikan oleh SCTP, seperti _label channel_. Untuk mengatasi itu WebRTC menggunakan _Data Channel Establishment Protocol_ (DCEP)
yang didefinisikan dalam [RFC 8832](https://tools.ietf.org/html/rfc8832). DCEP mendefinisikan pesan untuk mengomunikasikan _label channel_ dan protokol.

## DCEP
DCEP hanya memiliki dua pesan `DATA_CHANNEL_OPEN` dan `DATA_CHANNEL_ACK`. Untuk setiap _data channel_ yang dibuka, _remote_ harus merespons dengan _ack_.

### DATA_CHANNEL_OPEN
Pesan ini dikirim oleh _Agent_ WebRTC yang ingin membuka _channel_.

#### Format Paket
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |  Channel Type |            Priority           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Reliability Parameter                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Label Length          |       Protocol Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                             Label                             /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            Protocol                           /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Message Type
_Message Type_ adalah nilai statis `0x03`.

#### Channel Type
_Channel Type_ mengontrol atribut daya tahan/pengurutan dari _channel_. Ini mungkin memiliki nilai berikut:

* `DATA_CHANNEL_RELIABLE` (`0x00`) - Tidak ada pesan yang hilang dan akan tiba secara berurutan
* `DATA_CHANNEL_RELIABLE_UNORDERED` (`0x80`) - Tidak ada pesan yang hilang, tetapi mereka mungkin tiba tidak berurutan.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT` (`0x01`) - Pesan mungkin hilang setelah mencoba jumlah yang diminta, tetapi mereka akan tiba secara berurutan.
* `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED` (`0x81`) - Pesan mungkin hilang setelah mencoba jumlah yang diminta dan mungkin tiba tidak berurutan.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED` (`0x02`) - Pesan mungkin hilang jika mereka tidak tiba dalam jumlah waktu yang diminta, tetapi mereka akan tiba secara berurutan.
* `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED` (`0x82`) - Pesan mungkin hilang jika mereka tidak tiba dalam jumlah waktu yang diminta dan mungkin tiba tidak berurutan.

#### Priority
Prioritas dari _data channel_. _Data channel_ yang memiliki prioritas lebih tinggi akan dijadwalkan terlebih dahulu. Pesan pengguna prioritas rendah yang besar tidak akan menunda pengiriman pesan pengguna prioritas lebih tinggi.

#### Reliability Parameter
Jika tipe _data channel_ adalah `DATA_CHANNEL_PARTIAL_RELIABLE`, akhiran mengonfigurasi perilaku:

* `REXMIT` - Mendefinisikan berapa kali pengirim akan mengirim ulang pesan sebelum menyerah.
* `TIMED` - Mendefinisikan berapa lama waktu (dalam ms) pengirim akan mengirim ulang pesan sebelum menyerah.

#### Label
_String_ yang dikode UTF-8 yang berisi nama _data channel_. _String_ ini mungkin kosong.

#### Protocol
Jika ini adalah _string_ kosong, protokol tidak ditentukan. Jika itu adalah _string_ yang tidak kosong, itu harus menentukan protokol yang terdaftar dalam "_WebSocket Subprotocol Name Registry_", didefinisikan dalam [RFC 6455](https://tools.ietf.org/html/rfc6455#page-61).

### DATA_CHANNEL_ACK
Pesan ini dikirim oleh _Agent_ WebRTC untuk mengakui bahwa _data channel_ ini telah dibuka.

#### Format Paket
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
```

## Stream Control Transmission Protocol
SCTP adalah kekuatan sebenarnya di balik _data channel_ WebRTC. Ini menyediakan semua fitur _data channel_ ini:

* Multiplexing
* Pengiriman andal menggunakan mekanisme retransmisi seperti TCP
* Opsi keandalan parsial
* _Congestion Avoidance_
* _Flow Control_

Untuk memahami SCTP kita akan menjelajahinya dalam tiga bagian. Tujuannya adalah Anda akan tahu cukup untuk men-_debug_ dan mempelajari detail mendalam SCTP sendiri setelah bab ini.

## Konsep
SCTP adalah protokol yang kaya fitur. Bagian ini hanya akan membahas bagian-bagian SCTP yang digunakan oleh WebRTC.
Fitur dalam SCTP yang tidak digunakan oleh WebRTC termasuk _multi-homing_ dan _path selection_.

Dengan lebih dari dua puluh tahun pengembangan SCTP bisa sulit untuk sepenuhnya dipahami.

### Association
_Association_ adalah istilah yang digunakan untuk Sesi SCTP. Ini adalah _state_ yang dibagikan
antara dua _Agent_ SCTP saat mereka berkomunikasi.

### Streams
_Stream_ adalah satu urutan data pengguna dua arah. Ketika Anda membuat _data channel_, Anda sebenarnya hanya membuat _stream_ SCTP. Setiap _Association_ SCTP berisi daftar _stream_. Setiap _stream_ dapat dikonfigurasi dengan jenis keandalan yang berbeda.

WebRTC hanya memungkinkan Anda mengonfigurasi saat pembuatan _stream_, tetapi SCTP sebenarnya memungkinkan mengubah konfigurasi kapan saja.

### Berbasis Datagram
SCTP membingkai data sebagai datagram dan bukan sebagai _byte stream_. Mengirim dan menerima data terasa seperti menggunakan UDP daripada TCP.
Anda tidak perlu menambahkan kode tambahan untuk mentransfer beberapa file melalui satu _stream_.

Pesan SCTP tidak memiliki batas ukuran seperti UDP. Satu pesan SCTP bisa berukuran beberapa gigabyte.

### Chunks
Protokol SCTP terdiri dari _chunk_. Ada banyak jenis _chunk_ yang berbeda. _Chunk_ ini digunakan untuk semua komunikasi.
Data pengguna, inisialisasi koneksi, _congestion control_, dan lainnya semuanya dilakukan melalui _chunk_.

Setiap paket SCTP berisi daftar _chunk_. Jadi dalam satu paket UDP Anda dapat memiliki beberapa _chunk_ yang membawa pesan dari _stream_ yang berbeda.

### Transmission Sequence Number
_Transmission Sequence Number_ (TSN) adalah pengidentifikasi unik global untuk _chunk_ DATA. _Chunk_ DATA adalah yang membawa semua pesan yang ingin dikirim pengguna. TSN penting karena membantu penerima menentukan apakah paket hilang atau tidak berurutan.

Jika penerima menyadari TSN yang hilang, ia tidak memberikan data kepada pengguna sampai dipenuhi.

### Stream Identifier
Setiap _stream_ memiliki pengidentifikasi unik. Ketika Anda membuat _data channel_ dengan ID eksplisit, itu sebenarnya hanya diteruskan langsung ke SCTP sebagai _stream identifier_. Jika Anda tidak memberikan ID, _stream identifier_ dipilih untuk Anda.

### Payload Protocol Identifier
Setiap _chunk_ DATA juga memiliki _Payload Protocol Identifier_ (PPID). Ini digunakan untuk mengidentifikasi secara unik jenis data apa yang sedang dipertukarkan.
SCTP memiliki banyak PPID, tetapi WebRTC hanya menggunakan lima berikut:

* `WebRTC DCEP` (`50`) - Pesan DCEP.
* `WebRTC String` (`51`) - Pesan _string_ DataChannel.
* `WebRTC Binary` (`53`) - Pesan biner DataChannel.
* `WebRTC String Empty` (`56`) - Pesan _string_ DataChannel dengan panjang 0.
* `WebRTC Binary Empty` (`57`) - Pesan biner DataChannel dengan panjang 0.

## Protokol
Berikut adalah beberapa _chunk_ yang digunakan oleh protokol SCTP. Ini
bukan demonstrasi lengkap. Ini memberikan cukup struktur agar _state
machine_ masuk akal.

Setiap _Chunk_ dimulai dengan bidang `type`. Sebelum daftar _chunk_, Anda juga
akan memiliki _header_.

### DATA Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 0    | Reserved|U|B|E|    Length                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              TSN                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Stream Identifier        |   Stream Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Payload Protocol Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            User Data                          /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
_Chunk_ DATA adalah bagaimana semua data pengguna dipertukarkan. Ketika Anda mengirim
apa pun melalui _data channel_, ini adalah cara pertukaran.

_Bit_ `U` disetel jika ini adalah paket tidak berurutan. Kita dapat mengabaikan
_Stream Sequence Number_.

`B` dan `E` adalah _bit_ awal dan akhir. Jika Anda ingin mengirim
pesan yang terlalu besar untuk satu _chunk_ DATA, ia perlu difragmentasi menjadi beberapa _chunk_ DATA yang dikirim dalam paket terpisah.
Dengan _bit_ `B` dan `E` dan _Sequence Number_ SCTP dapat mengekspresikan
ini.

* `B=1`, `E=0` - Bagian pertama dari pesan pengguna yang terfragmentasi.
* `B=0`, `E=0` - Bagian tengah dari pesan pengguna yang terfragmentasi.
* `B=0`, `E=1` - Bagian terakhir dari pesan pengguna yang terfragmentasi.
* `B=1`, `E=1` - Pesan yang tidak terfragmentasi.

`TSN` adalah _Transmission Sequence Number_. Ini adalah pengidentifikasi unik global
untuk _chunk_ DATA ini. Setelah 4.294.967.295 _chunk_ ini akan kembali ke 0.
TSN ditambah untuk setiap _chunk_ dalam pesan pengguna yang terfragmentasi sehingga penerima tahu cara mengurutkan _chunk_ yang diterima untuk merekonstruksi pesan asli.

`Stream Identifier` adalah pengidentifikasi unik untuk _stream_ tempat data ini berada.

`Stream Sequence Number` adalah angka 16-bit yang ditambah setiap pesan pengguna dan disertakan dalam _header chunk_ pesan DATA. Setelah 65535 pesan ini akan kembali ke 0. Angka ini digunakan untuk memutuskan urutan pengiriman pesan ke penerima jika `U` disetel ke 0. Mirip dengan TSN, kecuali _Stream Sequence Number_ hanya ditambah untuk setiap pesan secara keseluruhan dan bukan setiap _chunk_ DATA individual.

`Payload Protocol Identifier` adalah jenis data yang mengalir melalui
_stream_ ini. Untuk WebRTC, itu akan menjadi DCEP, String atau Binary.

`User Data` adalah apa yang Anda kirim. Semua data yang Anda kirim melalui _data channel_ WebRTC
ditransmisikan melalui _chunk_ DATA.

### INIT Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 1    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Initiate Tag                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Advertised Receiver Window Credit (a_rwnd)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Number of Outbound Streams   |  Number of Inbound Streams    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Initial TSN                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/              Optional/Variable-Length Parameters              /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ INIT memulai proses pembuatan _association_.

`Initiate Tag` digunakan untuk pembuatan _cookie_. _Cookie_ digunakan untuk perlindungan _Man-In-The-Middle_
dan _Denial of Service_. Mereka dijelaskan lebih detail di bagian _state
machine_.

`Advertised Receiver Window Credit` digunakan untuk _Congestion Control_ SCTP. Ini
mengomunikasikan seberapa besar _buffer_ yang dialokasikan penerima untuk _association_ ini.

`Number of Outbound/Inbound Streams` memberi tahu _remote_ berapa banyak _stream_ yang didukung _agent_ ini.

`Initial TSN` adalah `uint32` acak untuk memulai TSN lokal.

`Optional Parameters` memungkinkan SCTP memperkenalkan fitur baru ke protokol.


### SACK Chunk

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 3    |Chunk  Flags   |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Advertised Receiver Window Credit (a_rwnd)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Number of Gap Ack Blocks = N  |  Number of Duplicate TSNs = X |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Gap Ack Block #1 Start       |   Gap Ack Block #1 End        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Gap Ack Block #N Start      |  Gap Ack Block #N End         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN 1                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\                              ...                              \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Duplicate TSN X                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ SACK (_Selective Acknowledgment_) adalah bagaimana penerima memberi tahu
pengirim bahwa ia telah mendapatkan paket. Sampai pengirim mendapat SACK untuk TSN
ia akan mengirim ulang _chunk_ DATA yang dimaksud. SACK melakukan lebih dari sekedar
memperbarui TSN.

`Cumulative TSN ACK` TSN tertinggi yang telah diterima.

`Advertised Receiver Window Credit` ukuran _buffer_ penerima. Penerima
mungkin mengubah ini selama sesi jika lebih banyak memori menjadi tersedia.

`Ack Blocks` TSN yang telah diterima setelah `Cumulative TSN ACK`.
Ini digunakan jika ada kesenjangan dalam paket yang dikirim. Katakanlah _chunk_ DATA dengan TSN
`100`, `102`, `103` dan `104` dikirim. `Cumulative TSN ACK` akan menjadi `100`, tetapi
`Ack Blocks` dapat digunakan untuk memberi tahu pengirim bahwa ia tidak perlu mengirim ulang `102`, `103` atau `104`.

`Duplicate TSN` menginformasikan pengirim bahwa ia telah menerima _chunk_ DATA berikut lebih dari sekali.

### HEARTBEAT Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 4    | Chunk  Flags  |      Heartbeat Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/            Heartbeat Information TLV (Variable-Length)        /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ HEARTBEAT digunakan untuk menegaskan _remote_ masih merespons.
Berguna jika Anda tidak mengirim _chunk_ DATA apa pun dan perlu menjaga _mapping_ NAT
tetap terbuka.

### ABORT Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 6    |Reserved     |T|           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/                                                               /
\               Zero or more Error Causes                       \
/                                                               /
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ ABORT menutup _association_ secara tiba-tiba. Digunakan ketika
satu sisi memasuki _state_ kesalahan. Mengakhiri koneksi dengan anggun menggunakan
_chunk_ SHUTDOWN.

### SHUTDOWN Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 7    | Chunk  Flags  |      Length = 8               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ SHUTDOWN memulai penutupan anggun dari _association_ SCTP.
Setiap _agent_ menginformasikan _remote_ tentang TSN terakhir yang dikirimnya. Ini memastikan
bahwa tidak ada paket yang hilang. WebRTC tidak melakukan penutupan anggun dari
_association_ SCTP. Anda perlu merobohkan setiap _data channel_ sendiri
untuk menanganinya dengan anggun.

`Cumulative TSN ACK` adalah TSN terakhir yang dikirim. Setiap sisi tahu
untuk tidak mengakhiri sampai mereka menerima _chunk_ DATA dengan TSN ini.

### ERROR Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 9    | Chunk  Flags  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                    One or more Error Causes                   /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ ERROR digunakan untuk memberi tahu _Agent_ SCTP _remote_ bahwa kesalahan non-fatal
telah terjadi.

### FORWARD TSN Chunk
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 192  |  Flags = 0x00 |        Length = Variable      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      New Cumulative TSN                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-1              |       Stream Sequence-1       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               /
/                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Stream-N              |       Stream Sequence-N       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

_Chunk_ `FORWARD TSN` memindahkan TSN global ke depan. SCTP melakukan ini, 
sehingga Anda dapat melewati beberapa paket yang tidak Anda pedulikan lagi. Katakanlah
Anda mengirim `10 11 12 13 14 15` dan paket-paket ini hanya valid jika mereka
semua tiba. Data ini juga sensitif terhadap _real-time_, jadi jika tiba
terlambat itu tidak berguna.

Jika Anda kehilangan `12` dan `13` tidak ada alasan untuk mengirim `14` dan `15`!
SCTP menggunakan _chunk_ `FORWARD TSN` untuk mencapai itu. Ini memberi tahu penerima
bahwa `14` dan `15` tidak akan dikirim lagi.

`New Cumulative TSN` ini adalah TSN baru dari koneksi. Setiap paket
sebelum TSN ini tidak akan dipertahankan.

`Stream` dan `Stream Sequence` digunakan untuk melompat `Stream Sequence Number`
nomor ke depan. Rujuk kembali ke DATA Chunk untuk signifikansi bidang ini.

## State Machine
Ini adalah beberapa bagian menarik dari _state machine_ SCTP. WebRTC tidak menggunakan semua
fitur _state machine_ SCTP, jadi kami telah mengecualikan bagian-bagian itu. Kami juga telah menyederhanakan beberapa komponen untuk membuatnya dapat dipahami sendiri.

### Connection Establishment Flow
_Chunk_ `INIT` dan `INIT ACK` digunakan untuk bertukar kemampuan dan konfigurasi
dari setiap _peer_. SCTP menggunakan _cookie_ selama _handshake_ untuk memvalidasi _peer_ yang berkomunikasi dengannya.
Ini untuk memastikan bahwa _handshake_ tidak dicegat dan untuk mencegah serangan DoS.

_Chunk_ `INIT ACK` berisi _cookie_. _Cookie_ kemudian dikembalikan ke pembuatnya
menggunakan `COOKIE ECHO`. Jika verifikasi _cookie_ berhasil, `COOKIE ACK` dikirim dan _chunk_ DATA siap untuk dipertukarkan.

![Connection establishment](../images/07-connection-establishment.png "Connection establishment")

### Connection Teardown Flow
SCTP menggunakan _chunk_ `SHUTDOWN`. Ketika _agent_ menerima _chunk_ `SHUTDOWN` ia akan menunggu sampai ia
menerima `Cumulative TSN ACK` yang diminta. Ini memungkinkan pengguna untuk memastikan bahwa semua data
dikirim bahkan jika koneksi _lossy_.

### Keep-Alive Mechanism
SCTP menggunakan _Chunk_ `HEARTBEAT REQUEST` dan `HEARTBEAT ACK` untuk menjaga koneksi tetap hidup. Ini dikirim
pada interval yang dapat dikonfigurasi. SCTP juga melakukan _exponential backoff_ jika paket belum tiba.

_Chunk_ `HEARTBEAT` juga berisi nilai waktu. Ini memungkinkan dua _association_ menghitung waktu perjalanan antara dua _agent_.
