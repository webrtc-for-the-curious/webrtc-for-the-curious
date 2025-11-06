---
title: Connecting
type: docs
weight: 4
---

# Connecting

## Mengapa WebRTC membutuhkan subsistem khusus untuk tersambung?

Sebagian besar aplikasi yang digunakan saat ini membangun koneksi _client/server_. Koneksi _client/server_ mengharuskan _server_ memiliki alamat transpor yang stabil dan diketahui. _Client_ menghubungi _server_, dan _server_ merespons.

WebRTC tidak menggunakan model _client/server_, melainkan membangun koneksi _peer-to-peer_ (P2P). Dalam koneksi P2P, tugas membuat koneksi didistribusikan secara merata ke kedua _peer_. Ini karena alamat transpor (IP dan _port_) di WebRTC tidak dapat diasumsikan, dan bahkan mungkin berubah selama sesi. WebRTC akan mengumpulkan semua informasi yang bisa didapat dan akan berusaha keras untuk mencapai komunikasi dua arah antara dua klien WebRTC.

Membangun konektivitas _peer-to-peer_ bisa sulit. Klien-klien ini bisa berada di jaringan yang berbeda tanpa konektivitas langsung. Dalam situasi di mana konektivitas langsung memang ada, Anda masih bisa menghadapi masalah lain. Dalam beberapa kasus, klien Anda tidak menggunakan protokol jaringan yang sama (UDP <-> TCP) atau mungkin menggunakan Versi IP yang berbeda (IPv4 <-> IPv6).

Terlepas dari kesulitan dalam mengatur koneksi P2P, Anda mendapatkan keuntungan dibanding teknologi Client/Server tradisional karena atribut berikut yang ditawarkan WebRTC.

### Pengurangan Biaya _Bandwidth_

Karena komunikasi media terjadi langsung antar _peer_, Anda tidak perlu membayar atau meng-_host_ _server_ terpisah untuk meneruskan media.

### Latensi Lebih Rendah

Komunikasi lebih cepat ketika langsung! Ketika pengguna harus menjalankan semua melalui _server_ Anda, itu membuat transmisi lebih lambat.

### Komunikasi E2E yang Aman

Komunikasi langsung lebih aman. Karena pengguna tidak merutekan data melalui _server_ Anda, mereka bahkan tidak perlu mempercayai Anda untuk tidak mendekripsinya.

## Bagaimana cara kerjanya?

Proses yang dijelaskan di atas disebut Interactive Connectivity Establishment ([ICE](https://tools.ietf.org/html/rfc8445)). Protokol lain yang sudah ada sebelum WebRTC.

ICE adalah protokol yang mencoba menemukan cara terbaik untuk berkomunikasi antara dua ICE Agent. Setiap ICE Agent mempublikasikan cara-cara ia dapat dijangkau, ini dikenal sebagai _candidate_. _Candidate_ pada dasarnya adalah alamat transpor dari _agent_ yang ia yakini dapat dijangkau oleh _peer_ lainnya. ICE kemudian menentukan pasangan _candidate_ terbaik.

Proses ICE yang sebenarnya dijelaskan lebih detail nanti di bab ini. Untuk memahami mengapa ICE ada, berguna untuk memahami perilaku jaringan apa yang kita atasi.

## Kendala jaringan di dunia nyata
ICE adalah tentang mengatasi kendala jaringan di dunia nyata. Sebelum kita mengeksplorasi solusinya, mari kita bicarakan masalah sebenarnya.

### Tidak dalam jaringan yang sama
Sebagian besar waktu, klien WebRTC lainnya bahkan tidak akan berada dalam jaringan yang sama. Panggilan khas biasanya terjadi antara dua klien WebRTC di jaringan yang berbeda tanpa konektivitas langsung.

Berikut adalah grafik dari dua jaringan yang berbeda, terhubung melalui internet publik. Di setiap jaringan Anda memiliki dua _host_.

![Two networks](../images/03-two-networks.png "Two networks")

Untuk _host_ dalam jaringan yang sama, sangat mudah untuk terhubung. Komunikasi antara `192.168.0.1 -> 192.168.0.2` mudah dilakukan! Kedua _host_ ini dapat terhubung satu sama lain tanpa bantuan luar.

Namun, _host_ yang menggunakan `Router B` tidak memiliki cara untuk langsung mengakses apapun di belakang `Router A`. Bagaimana Anda membedakan antara `192.168.0.1` di belakang `Router A` dan IP yang sama di belakang `Router B`? Mereka adalah IP pribadi! _Host_ yang menggunakan `Router B` dapat mengirim traffic langsung ke `Router A`, tetapi permintaan akan berakhir di situ. Bagaimana `Router A` tahu _host_ mana yang harus ia teruskan pesannya?

### Pembatasan Protokol
Beberapa jaringan tidak mengizinkan traffic UDP sama sekali, atau mungkin mereka tidak mengizinkan TCP. Beberapa jaringan mungkin memiliki MTU (Maximum Transmission Unit) yang sangat rendah. Ada banyak variabel yang dapat diubah oleh administrator jaringan yang dapat menyulitkan komunikasi.

### Aturan _Firewall_/IDS
Lainnya adalah "Deep Packet Inspection" dan penyaringan cerdas lainnya. Beberapa administrator jaringan akan menjalankan perangkat lunak yang mencoba memproses setiap paket. Seringkali perangkat lunak ini tidak memahami WebRTC, jadi ia memblokirnya karena tidak tahu harus berbuat apa, misalnya memperlakukan paket WebRTC sebagai paket UDP yang mencurigakan pada _port_ acak yang tidak masuk _whitelist_.

## Pemetaan NAT
Pemetaan NAT (Network Address Translation) adalah keajaiban yang membuat konektivitas WebRTC mungkin. Inilah cara WebRTC memungkinkan dua _peer_ di subnet yang benar-benar berbeda untuk berkomunikasi, menangani masalah "tidak dalam jaringan yang sama" di atas. Meskipun ini menciptakan tantangan baru, mari kita jelaskan bagaimana pemetaan NAT bekerja pada awalnya.

Ini tidak menggunakan relay, proxy, atau _server_. Sekali lagi kita memiliki `Agent 1` dan `Agent 2` dan mereka berada di jaringan yang berbeda. Namun, traffic mengalir sepenuhnya. Divisualisasikan terlihat seperti ini:

![NAT mapping](../images/03-nat-mapping.png "NAT mapping")

Untuk membuat komunikasi ini terjadi, Anda membentuk pemetaan NAT. Agent 1 menggunakan _port_ 7000 untuk membangun koneksi WebRTC dengan Agent 2. Ini menciptakan pengikatan dari `192.168.0.1:7000` ke `5.0.0.1:7000`. Ini kemudian memungkinkan Agent 2 untuk mencapai Agent 1 dengan mengirimkan paket ke `5.0.0.1:7000`. Membuat pemetaan NAT seperti dalam contoh ini seperti versi otomatis dari melakukan _port forwarding_ di _router_ Anda.

Kelemahan pemetaan NAT adalah bahwa tidak ada satu bentuk pemetaan tunggal (misalnya _port forwarding_ statis), dan perilakunya tidak konsisten antar jaringan. ISP dan produsen perangkat keras mungkin melakukannya dengan cara berbeda. Dalam beberapa kasus, administrator jaringan bahkan mungkin menonaktifkannya.

Kabar baiknya adalah rentang lengkap perilaku dipahami dan dapat diamati, sehingga ICE Agent mampu mengonfirmasi ia telah membuat pemetaan NAT, dan atribut pemetaan.

Dokumen yang menjelaskan perilaku ini adalah [RFC 4787](https://tools.ietf.org/html/rfc4787).

### Membuat pemetaan
Membuat pemetaan adalah bagian paling mudah. Ketika Anda mengirim paket ke alamat di luar jaringan Anda, pemetaan dibuat! Pemetaan NAT hanyalah IP publik sementara dan _port_ yang dialokasikan oleh NAT Anda. Pesan keluar akan ditulis ulang agar alamat sumbernya diberikan oleh alamat pemetaan yang baru. Jika pesan dikirim ke pemetaan, itu akan secara otomatis dirutekan kembali ke _host_ di dalam NAT yang membuatnya. Detail seputar pemetaan adalah di mana ia menjadi rumit.

### Perilaku Pembuatan Pemetaan
Pembuatan pemetaan terbagi dalam tiga kategori berbeda:

#### Endpoint-Independent Mapping
Satu pemetaan dibuat untuk setiap pengirim di dalam NAT. Jika Anda mengirim dua paket ke dua alamat _remote_ yang berbeda, pemetaan NAT akan digunakan kembali. Kedua _host remote_ akan melihat IP dan _port_ sumber yang sama. Jika _host remote_ merespons, itu akan dikirim kembali ke pendengar lokal yang sama.

Ini adalah skenario terbaik. Agar panggilan berfungsi, setidaknya satu sisi HARUS dari tipe ini.

#### Address Dependent Mapping
Pemetaan baru dibuat setiap kali Anda mengirim paket ke alamat baru. Jika Anda mengirim dua paket ke _host_ yang berbeda, dua pemetaan akan dibuat. Jika Anda mengirim dua paket ke _host remote_ yang sama tetapi _port_ tujuan yang berbeda, pemetaan baru TIDAK akan dibuat.

#### Address and Port Dependent Mapping
Pemetaan baru dibuat jika IP atau _port remote_ berbeda. Jika Anda mengirim dua paket ke _host remote_ yang sama, tetapi _port_ tujuan yang berbeda, pemetaan baru akan dibuat.

### Perilaku Penyaringan Pemetaan
Penyaringan pemetaan adalah aturan tentang siapa yang diizinkan menggunakan pemetaan. Mereka terbagi dalam tiga klasifikasi serupa:

#### Endpoint-Independent Filtering
Siapa saja dapat menggunakan pemetaan. Anda dapat membagikan pemetaan dengan beberapa _peer_ lain, dan mereka semua dapat mengirim traffic ke sana.

#### Address Dependent Filtering
Hanya _host_ untuk siapa pemetaan dibuat yang dapat menggunakan pemetaan. Jika Anda mengirim paket ke _host_ `A` Anda hanya dapat mendapat respons dari _host_ yang sama. Jika _host_ `B` mencoba mengirim paket ke pemetaan itu, itu akan diabaikan.

#### Address and Port Dependent Filtering
Hanya _host_ dan _port_ untuk siapa pemetaan dibuat yang dapat menggunakan pemetaan itu. Jika Anda mengirim paket ke `A:5000` Anda hanya dapat mendapat respons dari _host_ dan _port_ yang sama. Jika `A:5001` mencoba mengirim paket ke pemetaan itu, itu akan diabaikan.

### Penyegaran Pemetaan
Disarankan agar jika pemetaan tidak digunakan selama 5 menit, pemetaan harus dihancurkan. Ini sepenuhnya tergantung pada ISP atau produsen perangkat keras.

## STUN
STUN (Session Traversal Utilities for NAT) adalah protokol yang dibuat khusus untuk bekerja dengan NAT. Ini adalah teknologi lain yang sudah ada sebelum WebRTC (dan ICE!). Ini didefinisikan oleh [RFC 8489](https://tools.ietf.org/html/rfc8489), yang juga mendefinisikan struktur paket STUN. Protokol STUN juga digunakan oleh ICE/TURN.

STUN berguna karena memungkinkan pembuatan pemetaan NAT secara programatik. Sebelum STUN, kita dapat membuat pemetaan NAT, tetapi kita tidak tahu apa IP dan _port_-nya! STUN tidak hanya memberi Anda kemampuan untuk membuat pemetaan, tetapi juga memberi Anda detailnya sehingga Anda dapat membagikannya dengan orang lain, sehingga mereka dapat mengirim traffic kembali kepada Anda melalui pemetaan yang baru saja Anda buat.

Mari kita mulai dengan deskripsi dasar STUN. Nanti, kita akan memperluas penggunaan TURN dan ICE. Untuk saat ini, kita hanya akan menjelaskan alur Request/Response untuk membuat pemetaan. Kemudian kita akan membicarakan cara mendapatkan detailnya untuk dibagikan dengan orang lain. Ini adalah proses yang terjadi ketika Anda memiliki _server_ `stun:` dalam ICE URL Anda untuk WebRTC PeerConnection. Singkatnya, STUN membantu _endpoint_ di belakang NAT mengetahui pemetaan apa yang dibuat dengan meminta _server_ STUN di luar NAT untuk melaporkan apa yang diamatinya.

### Struktur Protokol
Setiap paket STUN memiliki struktur berikut:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|0 0|     STUN Message Type     |         Message Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Magic Cookie                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     Transaction ID (96 bits)                  |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### STUN Message Type
Setiap paket STUN memiliki tipe. Untuk saat ini, kita hanya peduli tentang yang berikut:

* Binding Request - `0x0001`
* Binding Response - `0x0101`

Untuk membuat pemetaan NAT kita membuat `Binding Request`. Kemudian _server_ merespons dengan `Binding Response`.

#### Message Length
Ini adalah panjang bagian `Data`. Bagian ini berisi data sembarang yang didefinisikan oleh `Message Type`.

#### Magic Cookie
Nilai tetap `0x2112A442` dalam urutan _byte_ jaringan, ini membantu membedakan traffic STUN dari protokol lain.

#### Transaction ID
Pengenal 96-bit yang secara unik mengidentifikasi _request/response_. Ini membantu Anda memasangkan _request_ dan _response_ Anda.

#### Data
Data akan berisi daftar atribut STUN. Atribut STUN memiliki struktur berikut:

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

`STUN Binding Request` tidak menggunakan atribut. Ini berarti `STUN Binding Request` hanya berisi _header_.

`STUN Binding Response` menggunakan `XOR-MAPPED-ADDRESS (0x0020)`. Atribut ini berisi IP dan _port_. Ini adalah IP dan _port_ dari pemetaan NAT yang dibuat!

### Membuat Pemetaan NAT
Membuat pemetaan NAT menggunakan STUN hanya memerlukan pengiriman satu _request_! Anda mengirim `STUN Binding Request` ke STUN Server. STUN Server kemudian merespons dengan `STUN Binding Response`.
`STUN Binding Response` ini akan berisi `Mapped Address`. `Mapped Address` adalah bagaimana STUN Server melihat Anda dan merupakan `pemetaan NAT` Anda.
`Mapped Address` adalah yang akan Anda bagikan jika Anda ingin seseorang mengirimkan paket kepada Anda.

Orang juga akan menyebut `Mapped Address` sebagai `Public IP` atau `Server Reflexive Candidate` Anda.

### Menentukan Tipe NAT
Sayangnya, `Mapped Address` mungkin tidak berguna dalam semua kasus. Jika itu adalah `Address Dependent`, hanya _server_ STUN yang dapat mengirim traffic kembali kepada Anda. Jika Anda membagikannya dan _peer_ lain mencoba mengirim pesan masuk, mereka akan dijatuhkan. Ini membuatnya tidak berguna untuk berkomunikasi dengan orang lain. Anda mungkin menemukan kasus `Address Dependent` sebenarnya dapat dipecahkan, jika _host_ yang menjalankan _server_ STUN juga dapat meneruskan paket untuk Anda ke _peer_! Ini membawa kita ke solusi menggunakan TURN di bawah ini.

[RFC 5780](https://tools.ietf.org/html/rfc5780) mendefinisikan metode untuk menjalankan tes untuk menentukan Tipe NAT Anda. Ini berguna karena Anda akan tahu sebelumnya apakah konektivitas langsung mungkin.

## TURN
TURN (Traversal Using Relays around NAT) didefinisikan dalam [RFC 8656](https://tools.ietf.org/html/rfc8656) adalah solusi ketika konektivitas langsung tidak mungkin. Ini bisa karena Anda memiliki dua Tipe NAT yang tidak kompatibel, atau mungkin tidak dapat berbicara dengan protokol yang sama! TURN juga dapat digunakan untuk tujuan privasi. Dengan menjalankan semua komunikasi Anda melalui TURN Anda menyembunyikan alamat sebenarnya klien.

TURN menggunakan _server_ khusus. _Server_ ini bertindak sebagai proxy untuk klien. Klien terhubung ke TURN Server dan membuat `Allocation`. Dengan membuat alokasi, klien mendapatkan IP/Port/Protokol sementara yang dapat digunakan untuk mengirim traffic kembali ke klien. Pendengar baru ini dikenal sebagai `Relayed Transport Address`. Anggap itu sebagai alamat penerusan, Anda memberikan ini sehingga orang lain dapat mengirimkan traffic kepada Anda melalui TURN! Untuk setiap _peer_ yang Anda berikan `Relay Transport Address`, Anda harus membuat `Permission` baru untuk mengizinkan komunikasi dengan Anda.

Ketika Anda mengirim traffic keluar melalui TURN, itu dikirim melalui `Relayed Transport Address`. Ketika _peer remote_ mendapat traffic, mereka melihatnya datang dari TURN Server.

### Siklus Hidup TURN
Berikut adalah semua yang harus dilakukan oleh klien yang ingin membuat alokasi TURN. Berkomunikasi dengan seseorang yang menggunakan TURN tidak memerlukan perubahan. _Peer_ lain mendapat IP dan _port_, dan mereka berkomunikasi dengannya seperti _host_ lainnya.

#### Allocations
Allocation adalah inti dari TURN. `Allocation` pada dasarnya adalah "TURN Session". Untuk membuat alokasi TURN, Anda berkomunikasi dengan TURN `Server Transport Address` (biasanya _port_ `3478`).

Saat membuat alokasi, Anda perlu memberikan yang berikut:
* Username/Password - Membuat alokasi TURN memerlukan autentikasi.
* Allocation Transport - Protokol transpor antara _server_ (`Relayed Transport Address`) dan _peer_, bisa UDP atau TCP.
* Even-Port - Anda dapat meminta _port_ berurutan untuk beberapa alokasi, tidak relevan untuk WebRTC.

Jika _request_ berhasil, Anda mendapat respons dengan TURN Server dengan Atribut STUN berikut di bagian Data:
* `XOR-MAPPED-ADDRESS` - `Mapped Address` dari `TURN Client`. Ketika seseorang mengirim data ke `Relayed Transport Address` ini adalah tempat ia diteruskan.
* `RELAYED-ADDRESS` - Ini adalah alamat yang Anda berikan kepada klien lain. Jika seseorang mengirim paket ke alamat ini, itu diteruskan ke klien TURN.
* `LIFETIME` - Berapa lama sampai Alokasi TURN ini dihancurkan. Anda dapat memperpanjang masa hidup dengan mengirim _request_ `Refresh`.

#### Permissions
_Host remote_ tidak dapat mengirim ke `Relayed Transport Address` Anda sampai Anda membuat izin untuk mereka. Ketika Anda membuat izin, Anda memberi tahu _server_ TURN bahwa IP dan _port_ ini diizinkan untuk mengirim traffic masuk.

_Host remote_ perlu memberi Anda IP dan _port_ seperti yang terlihat oleh _server_ TURN. Ini berarti ia harus mengirim `STUN Binding Request` ke TURN Server. Kasus kesalahan umum adalah bahwa _host remote_ akan mengirim `STUN Binding Request` ke _server_ yang berbeda. Mereka kemudian akan meminta Anda untuk membuat izin untuk IP ini.

Katakanlah Anda ingin membuat izin untuk _host_ di belakang `Address Dependent Mapping`. Jika Anda menghasilkan `Mapped Address` dari _server_ TURN yang berbeda, semua traffic masuk akan dijatuhkan. Setiap kali mereka berkomunikasi dengan _host_ yang berbeda, itu menghasilkan pemetaan baru. Izin kedaluwarsa setelah 5 menit jika tidak disegarkan.

#### SendIndication/ChannelData
Kedua pesan ini adalah untuk TURN Client mengirim pesan ke _peer remote_.

SendIndication adalah pesan yang berdiri sendiri. Di dalamnya adalah data yang ingin Anda kirim, dan kepada siapa Anda ingin mengirimnya. Ini boros jika Anda mengirim banyak pesan ke _peer remote_. Jika Anda mengirim 1.000 pesan, Anda akan mengulangi Alamat IP mereka 1.000 kali!

ChannelData memungkinkan Anda mengirim data, tetapi tidak mengulangi Alamat IP. Anda membuat Channel dengan IP dan _port_. Anda kemudian mengirim dengan ChannelId, dan IP serta _port_ akan diisi di sisi _server_. Ini adalah pilihan yang lebih baik jika Anda mengirim banyak pesan.

#### Refreshing
Alokasi akan menghancurkan diri mereka sendiri secara otomatis. TURN Client harus menyegarkannya lebih cepat dari `LIFETIME` yang diberikan saat membuat alokasi.

### Penggunaan TURN
Penggunaan TURN ada dalam dua bentuk. Biasanya, Anda memiliki satu _peer_ yang bertindak sebagai "TURN Client" dan sisi lain berkomunikasi langsung. Dalam beberapa kasus Anda mungkin memiliki penggunaan TURN di kedua sisi, misalnya karena kedua klien berada di jaringan yang memblokir UDP dan oleh karena itu koneksi ke _server_ TURN masing-masing terjadi melalui TCP.

Diagram ini membantu menggambarkan seperti apa itu.

#### Satu Alokasi TURN untuk Komunikasi

![One TURN allocation](../images/03-one-turn-allocation.png "One TURN allocation")

#### Dua Alokasi TURN untuk Komunikasi

![Two TURN allocations](../images/03-two-turn-allocations.png "Two TURN allocations")

## ICE
ICE (Interactive Connectivity Establishment) adalah bagaimana WebRTC menghubungkan dua Agent. Didefinisikan dalam [RFC 8445](https://tools.ietf.org/html/rfc8445), ini adalah teknologi lain yang sudah ada sebelum WebRTC! ICE adalah protokol untuk membangun konektivitas. Ini menentukan semua rute yang mungkin antara kedua _peer_ dan kemudian memastikan Anda tetap terhubung.

Rute-rute ini dikenal sebagai `Candidate Pair`, yang merupakan pasangan alamat transpor lokal dan _remote_. Di sinilah STUN dan TURN ikut bermain dengan ICE. Alamat ini dapat berupa Alamat IP lokal Anda plus _port_, `pemetaan NAT`, atau `Relayed Transport Address`. Setiap sisi mengumpulkan semua alamat yang ingin mereka gunakan, menukarnya, dan kemudian mencoba untuk terhubung!

Dua ICE Agent berkomunikasi menggunakan paket ping ICE (atau secara resmi disebut pemeriksaan konektivitas) untuk membangun konektivitas. Setelah konektivitas terbentuk, mereka dapat mengirim data apa pun yang mereka inginkan. Ini akan seperti menggunakan _socket_ normal. Pemeriksaan ini menggunakan protokol STUN.

### Membuat ICE Agent
ICE Agent adalah `Controlling` atau `Controlled`. `Controlling` Agent adalah yang memutuskan `Candidate Pair` yang dipilih. Biasanya, _peer_ yang mengirim _offer_ adalah sisi _controlling_.

Setiap sisi harus memiliki `user fragment` dan `password`. Kedua nilai ini harus ditukar sebelum pemeriksaan konektivitas bahkan dapat dimulai. `user fragment` dikirim dalam teks biasa dan berguna untuk demuxing beberapa Sesi ICE.
`password` digunakan untuk menghasilkan atribut `MESSAGE-INTEGRITY`. Di akhir setiap paket STUN, ada atribut yang merupakan _hash_ dari seluruh paket menggunakan `password` sebagai kunci. Ini digunakan untuk mengautentikasi paket dan memastikan itu tidak dirusak.

Untuk WebRTC, semua nilai ini didistribusikan melalui `Session Description` seperti dijelaskan di bab sebelumnya.

### Pengumpulan _Candidate_
Kita sekarang perlu mengumpulkan semua alamat yang mungkin di mana kita dapat dijangkau. Alamat ini dikenal sebagai _candidate_.

#### Host
_Candidate Host_ mendengarkan langsung pada antarmuka lokal. Ini dapat berupa UDP atau TCP.

#### mDNS
_Candidate_ mDNS mirip dengan _candidate host_, tetapi alamat IP-nya disamarkan. Alih-alih memberi tahu sisi lain tentang alamat IP Anda, Anda memberi mereka UUID sebagai _hostname_. Anda kemudian menyiapkan pendengar multicast, dan merespons jika ada yang meminta UUID yang Anda publikasikan.

Jika Anda berada di jaringan yang sama dengan _agent_, Anda dapat menemukan satu sama lain melalui Multicast. Jika Anda tidak berada di jaringan yang sama, Anda tidak akan dapat terhubung (kecuali administrator jaringan secara eksplisit mengonfigurasi jaringan untuk mengizinkan paket Multicast melewati).

Ini berguna untuk tujuan privasi. Pengguna dapat mengetahui alamat IP lokal Anda melalui WebRTC dengan _candidate Host_ (tanpa bahkan mencoba terhubung kepada Anda), tetapi dengan _candidate_ mDNS, sekarang mereka hanya mendapat UUID acak.

#### Server Reflexive
_Candidate Server Reflexive_ dihasilkan dengan melakukan `STUN Binding Request` ke STUN Server.

Ketika Anda mendapat `STUN Binding Response`, `XOR-MAPPED-ADDRESS` adalah _Candidate Server Reflexive_ Anda.

#### Peer Reflexive
_Candidate Peer Reflexive_ dibuat ketika _peer remote_ menerima _request_ Anda dari alamat yang sebelumnya tidak diketahui oleh _peer_. Setelah menerima, _peer_ melaporkan (memantulkan) alamat yang disebutkan kembali kepada Anda. _Peer_ tahu bahwa _request_ dikirim oleh Anda dan bukan orang lain karena ICE adalah protokol yang terautentikasi.

Ini umumnya terjadi ketika `Host Candidate` berkomunikasi dengan `Server Reflexive Candidate` yang berada di subnet yang berbeda, yang menghasilkan `pemetaan NAT` baru yang dibuat. Ingat kita mengatakan pemeriksaan konektivitas sebenarnya adalah paket STUN? Format respons STUN secara alami memungkinkan _peer_ untuk melaporkan kembali alamat _peer-reflexive_.

#### Relay
_Candidate Relay_ dihasilkan dengan menggunakan TURN Server.

Setelah _handshake_ awal dengan TURN Server, Anda diberi `RELAYED-ADDRESS`, ini adalah _Candidate Relay_ Anda.

### Pemeriksaan Konektivitas
Kita sekarang tahu `user fragment`, `password`, dan _candidate_ dari _agent remote_. Kita sekarang dapat mencoba untuk terhubung! Setiap _candidate_ dipasangkan satu sama lain. Jadi jika Anda memiliki 3 _candidate_ di setiap sisi, Anda sekarang memiliki 9 pasangan _candidate_.

Secara visual terlihat seperti ini:

![Connectivity checks](../images/03-connectivity-checks.png "Connectivity checks")

### Pemilihan _Candidate_
Controlling dan Controlled Agent keduanya mulai mengirim traffic pada setiap pasangan. Ini diperlukan jika satu Agent berada di belakang `Address Dependent Mapping`, ini akan menyebabkan `Peer Reflexive Candidate` dibuat.

Setiap `Candidate Pair` yang melihat traffic jaringan kemudian dipromosikan ke pasangan `Valid Candidate`. Controlling Agent kemudian mengambil satu pasangan `Valid Candidate` dan menominasikannya. Ini menjadi `Nominated Pair`. Controlling dan Controlled Agent kemudian mencoba satu putaran lagi komunikasi dua arah. Jika itu berhasil, `Nominated Pair` menjadi `Selected Candidate Pair`! Pasangan ini kemudian digunakan untuk sisa sesi.

### Restart
Jika `Selected Candidate Pair` berhenti bekerja karena alasan apa pun (pemetaan NAT kedaluwarsa, TURN Server _crash_) ICE Agent akan masuk ke status `Failed`. Kedua _agent_ dapat di-_restart_ dan akan melakukan seluruh proses lagi.
