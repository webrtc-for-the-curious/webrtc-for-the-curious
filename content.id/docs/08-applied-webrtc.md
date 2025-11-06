---
title: Applied WebRTC
type: docs
weight: 9
---

# Applied WebRTC
Sekarang setelah Anda mengetahui bagaimana WebRTC bekerja, saatnya untuk membangun dengannya! Bab ini mengeksplorasi apa yang orang
bangun dengan WebRTC, dan bagaimana mereka membangunnya. Anda akan mempelajari semua hal menarik yang terjadi
dengan WebRTC. Kekuatan WebRTC datang dengan biaya. Membangun layanan WebRTC tingkat produksi adalah
menantang. Bab ini akan mencoba menjelaskan tantangan tersebut sebelum Anda menghadapinya.

## Berdasarkan Kasus Penggunaan
Banyak yang berpikir WebRTC hanyalah teknologi untuk konferensi di peramban web. Namun itu jauh lebih dari itu!
WebRTC digunakan dalam berbagai aplikasi. Kasus penggunaan baru muncul sepanjang waktu. Dalam bab ini kami akan mencantumkan beberapa yang umum dan bagaimana WebRTC merevolusi mereka.

### Conferencing
_Conferencing_ adalah kasus penggunaan asli untuk WebRTC. Protokol ini berisi beberapa fitur yang diperlukan yang tidak ditawarkan protokol lain
di peramban. Anda bisa membangun sistem konferensi dengan WebSocket dan mungkin bekerja dalam kondisi optimal. Jika Anda ingin
sesuatu yang dapat digunakan dalam kondisi jaringan dunia nyata, WebRTC adalah pilihan terbaik.

WebRTC menyediakan _congestion control_ dan _adaptive bitrate_ untuk media. Seiring kondisi jaringan berubah, pengguna masih akan mendapatkan
pengalaman terbaik yang mungkin. _Developer_ juga tidak perlu menulis kode tambahan untuk mengukur kondisi ini.

Peserta dapat mengirim dan menerima beberapa _stream_. Mereka juga dapat menambah dan menghapus _stream_ tersebut kapan saja selama panggilan. _Codec_ juga dinegosiasikan.
Semua fungsi ini disediakan oleh peramban, tidak ada kode khusus yang perlu ditulis oleh _developer_.

_Conferencing_ juga mendapat manfaat dari _data channel_. Pengguna dapat mengirim metadata atau berbagi dokumen. Anda dapat membuat beberapa _stream_
dan mengonfigurasinya jika Anda membutuhkan performa lebih daripada keandalan.

### _Broadcasting_
Banyak proyek baru mulai muncul di ruang siaran yang menggunakan WebRTC. Protokol ini menawarkan banyak hal baik untuk penerbit
dan konsumen media.

WebRTC yang berada di peramban memudahkan pengguna untuk menerbitkan video. Ini menghilangkan keharusan bagi pengguna untuk mengunduh klien baru.
Platform apa pun yang memiliki peramban web dapat menerbitkan video. Penerbit kemudian dapat mengirim beberapa _track_ dan memodifikasi atau menghapusnya kapan saja. Ini adalah
peningkatan besar dibanding protokol lama yang hanya mengizinkan satu audio atau satu _track_ video per koneksi.

WebRTC memberi _developer_ kontrol yang lebih besar atas _trade-off_ latensi versus kualitas. Jika lebih penting bahwa latensi tidak pernah melebihi
ambang batas tertentu, dan Anda bersedia mentolerir beberapa artefak dekoding. Anda dapat mengonfigurasi penonton untuk memutar media segera setelah
tiba. Dengan protokol lain yang berjalan melalui TCP, itu tidak semudah itu. Di peramban Anda dapat meminta data dan itu saja.

### _Remote Access_
_Remote Access_ adalah ketika Anda mengakses komputer lain dari jarak jauh melalui WebRTC. Anda bisa memiliki kendali penuh atas _host remote_, atau mungkin hanya
satu aplikasi. Ini bagus untuk menjalankan tugas yang mahal secara komputasi ketika perangkat keras lokal tidak dapat melakukannya. Seperti menjalankan video game baru, atau
perangkat lunak CAD. WebRTC mampu merevolusi ruang ini dalam tiga cara.

WebRTC dapat digunakan untuk mengakses _host_ dari jarak jauh yang tidak dapat di-_route_ secara global. Dengan NAT _Traversal_ Anda dapat mengakses komputer yang hanya tersedia
melalui STUN. Ini bagus untuk keamanan dan privasi. Pengguna Anda tidak perlu merutekan video melalui _ingest_, atau "jump box". NAT _Traversal_ juga
membuat penerapan lebih mudah. Anda tidak perlu khawatir tentang _port forwarding_ atau mengatur IP statis sebelumnya.

_Data channel_ juga sangat kuat dalam skenario ini. Mereka dapat dikonfigurasi sehingga hanya data terbaru yang diterima. Dengan TCP Anda menjalankan
risiko mengalami _Head-of-line blocking_. Klik mouse atau penekanan tombol lama bisa tiba terlambat, dan memblokir yang berikutnya agar tidak diterima.
_Data channel_ WebRTC dirancang untuk menangani ini dan dapat dikonfigurasi untuk tidak mengirim ulang paket yang hilang. Anda juga dapat mengukur _backpressure_ dan
memastikan bahwa Anda tidak mengirim lebih banyak data daripada yang didukung jaringan Anda.

WebRTC yang tersedia di peramban telah menjadi peningkatan kualitas hidup yang besar. Anda tidak perlu mengunduh klien propriet untuk memulai
sesi. Semakin banyak klien yang dilengkapi dengan WebRTC, Smart TV sekarang mendapatkan peramban web lengkap.

### Berbagi File dan Penghindaran Sensor
Berbagi File dan Penghindaran Sensor adalah masalah yang sangat berbeda. Namun, WebRTC menyelesaikan masalah yang sama untuk keduanya. Ini membuat
keduanya mudah tersedia dan lebih sulit untuk diblokir.

Masalah pertama yang diselesaikan WebRTC adalah mendapatkan klien. Jika Anda ingin bergabung dengan jaringan berbagi file, Anda perlu mengunduh klien. Bahkan jika
jaringan terdistribusi, Anda masih perlu mendapatkan klien terlebih dahulu. Dalam jaringan yang dibatasi, unduhan sering diblokir. Bahkan jika Anda
dapat mengunduhnya, pengguna mungkin tidak dapat menginstal dan menjalankan klien. WebRTC tersedia di setiap peramban web yang membuatnya mudah tersedia.

Masalah kedua yang diselesaikan WebRTC adalah traffic Anda yang diblokir. Jika Anda menggunakan protokol yang hanya untuk berbagi file atau penghindaran sensor
lebih mudah untuk memblokirnya. Karena WebRTC adalah protokol tujuan umum, memblokirnya akan berdampak pada semua orang. Memblokir WebRTC mungkin mencegah
pengguna jaringan lain dari bergabung dengan panggilan konferensi.

### Internet of Things
Internet of Things (IoT) mencakup beberapa kasus penggunaan yang berbeda. Bagi banyak orang ini berarti kamera keamanan yang terhubung ke jaringan. Menggunakan WebRTC Anda dapat melakukan _streaming_ video ke _peer_ WebRTC lain
seperti ponsel Anda atau peramban. Kasus penggunaan lainnya adalah memiliki perangkat yang terhubung dan bertukar data sensor. Anda dapat memiliki dua perangkat di LAN Anda
bertukar pembacaan iklim, kebisingan, atau cahaya.

WebRTC memiliki keuntungan privasi besar di sini dibandingkan protokol _stream_ video lama. Karena WebRTC mendukung konektivitas P2P, kamera dapat mengirim video
langsung ke peramban Anda. Tidak ada alasan untuk video Anda dikirim ke _server_ pihak ketiga. Bahkan ketika video dienkripsi, penyerang dapat membuat
asumsi dari metadata panggilan.

Interoperabilitas adalah keuntungan lain untuk ruang IoT. WebRTC tersedia dalam banyak bahasa berbeda; C#, C++, C, Go, Java, Python, Rust
dan TypeScript. Ini berarti Anda dapat menggunakan bahasa yang paling cocok untuk Anda. Anda juga tidak perlu beralih ke protokol atau format proprietary
untuk dapat menghubungkan klien Anda.

### _Media Protocol Bridging_
Anda memiliki perangkat keras dan perangkat lunak yang ada yang menghasilkan video, tetapi Anda belum dapat mengupgradenya. Mengharapkan pengguna untuk mengunduh klien proprietary
untuk menonton video itu membuat frustrasi. Jawabannya adalah menjalankan _bridge_ WebRTC. _Bridge_ menerjemahkan antara dua protokol sehingga pengguna dapat menggunakan
peramban dengan pengaturan lama Anda.

Banyak format yang di-_bridge_ oleh _developer_ menggunakan protokol yang sama dengan WebRTC. SIP umumnya diekspos melalui WebRTC dan memungkinkan pengguna untuk melakukan panggilan telepon
dari peramban mereka. RTSP digunakan di banyak kamera keamanan lama. Keduanya menggunakan protokol dasar yang sama (RTP dan SDP) sehingga murah secara komputasi
untuk dijalankan. _Bridge_ hanya diperlukan untuk menambahkan atau menghapus hal-hal yang spesifik untuk WebRTC.

### _Data Protocol Bridging_
Peramban web hanya dapat berbicara dengan set protokol yang terbatas. Anda dapat menggunakan HTTP, WebSocket, WebRTC dan QUIC. Jika Anda ingin terhubung
ke hal lain, Anda perlu menggunakan _protocol bridge_. _Protocol bridge_ adalah _server_ yang mengonversi traffic asing menjadi sesuatu yang dapat diakses peramban.
Contoh populer adalah menggunakan SSH dari peramban Anda untuk mengakses _server_. _Data channel_ WebRTC memiliki dua keuntungan dibanding kompetisi.

_Data channel_ WebRTC memungkinkan pengiriman tidak andal dan tidak terurut. Dalam kasus di mana latensi rendah kritis ini diperlukan. Anda tidak ingin data baru
diblokir oleh data lama, ini dikenal sebagai _head-of-line blocking_. Bayangkan Anda bermain game _First-person shooter_ multipemain. Apakah Anda benar-benar peduli di mana
pemain berada dua detik yang lalu? Jika data itu tidak tiba tepat waktu, tidak masuk akal untuk terus mencoba mengirimnya. Pengiriman tidak andal dan tidak terurut memungkinkan
Anda menggunakan data segera setelah tiba.

_Data channel_ juga menyediakan _feedback pressure_. Ini memberi tahu Anda jika Anda mengirim data lebih cepat daripada yang dapat didukung koneksi Anda. Anda kemudian memiliki dua
pilihan ketika ini terjadi. _Data channel_ dapat dikonfigurasi untuk _buffer_ dan mengirimkan data terlambat, atau Anda dapat menjatuhkan data yang belum tiba
dalam _real-time_.

### Teleoperation
_Teleoperation_ adalah tindakan mengendalikan perangkat dari jarak jauh melalui _data channel_ WebRTC, dan mengirim video kembali melalui RTP. _Developer_ mengemudikan mobil dari jarak jauh
melalui WebRTC hari ini! Ini digunakan untuk mengendalikan robot di lokasi konstruksi dan mengirim paket. Menggunakan WebRTC untuk masalah ini masuk akal karena dua alasan.

Keberadaan WebRTC di mana-mana memudahkan untuk memberikan kontrol kepada pengguna. Yang dibutuhkan pengguna hanyalah peramban web dan perangkat input. Peramban bahkan
mendukung pengambilan input dari _joystick_ dan _gamepad_. WebRTC sepenuhnya menghilangkan kebutuhan untuk menginstal klien tambahan di perangkat pengguna.

### CDN Terdistribusi
CDN terdistribusi adalah subset dari berbagi file. File yang didistribusikan dikonfigurasi oleh operator CDN sebagai gantinya. Ketika pengguna bergabung dengan jaringan CDN
mereka dapat mengunduh dan berbagi file yang diizinkan. Pengguna mendapat semua manfaat yang sama seperti berbagi file.

CDN ini bekerja dengan baik ketika Anda berada di kantor dengan konektivitas eksternal yang buruk, tetapi konektivitas LAN yang bagus. Anda dapat memiliki satu pengguna mengunduh video, dan
kemudian membagikannya dengan orang lain. Karena tidak semua orang mencoba mengambil file yang sama melalui jaringan eksternal, transfer akan selesai lebih cepat.

## Topologi WebRTC
WebRTC adalah protokol untuk menghubungkan dua _agent_, jadi bagaimana _developer_ menghubungkan ratusan orang sekaligus? Ada beberapa cara berbeda
yang dapat Anda lakukan, dan semuanya memiliki pro dan kontra. Solusi ini secara luas terbagi dalam dua kategori; _Peer-to-Peer_ atau _Client/Server_. Fleksibilitas WebRTC
memungkinkan kita untuk membuat keduanya.

### _One-To-One_
_One-to-One_ adalah tipe koneksi pertama yang akan Anda gunakan dengan WebRTC. Anda menghubungkan dua klien WebRTC secara langsung dan mereka dapat mengirim media dan data dua arah.
Koneksi terlihat seperti ini.

![One-to-One](../images/08-one-to-one.png "One-to-One")

### _Full Mesh_
_Full mesh_ adalah jawabannya jika Anda ingin membangun panggilan konferensi atau game multipemain. Dalam topologi ini setiap pengguna membuat koneksi
dengan setiap pengguna lain secara langsung. Ini memungkinkan Anda membangun aplikasi Anda, tetapi datang dengan beberapa kekurangan.

Dalam topologi _Full Mesh_ setiap pengguna terhubung langsung. Itu berarti Anda harus mengenkode dan mengunggah video secara independen untuk setiap anggota panggilan.
Kondisi jaringan antara setiap koneksi akan berbeda, jadi Anda tidak dapat menggunakan kembali video yang sama. Penanganan kesalahan juga sulit dalam
penerapan ini. Anda perlu mempertimbangkan dengan hati-hati apakah Anda telah kehilangan konektivitas lengkap, atau hanya konektivitas dengan satu _peer remote_.

Karena masalah ini, _Full Mesh_ paling baik digunakan untuk grup kecil. Untuk apa pun yang lebih besar, topologi _client/server_ adalah yang terbaik.

![Full mesh](../images/08-full-mesh.png "Full mesh")

### _Hybrid Mesh_
_Hybrid Mesh_ adalah alternatif untuk _Full Mesh_ yang dapat meringankan beberapa masalah _Full Mesh_. Dalam _Hybrid Mesh_ koneksi tidak dibuat
antara setiap pengguna. Sebaliknya, media direlai melalui _peer_ di jaringan. Ini berarti bahwa pencipta media tidak perlu menggunakan sebanyak
_bandwidth_ untuk mendistribusikan media.

Ini memiliki beberapa kekurangan. Dalam pengaturan ini, pencipta asli media tidak tahu kepada siapa videonya dikirim, atau apakah
tiba dengan sukses. Anda juga akan memiliki peningkatan latensi dengan setiap _hop_ di jaringan _Hybrid Mesh_ Anda.

![Hybrid mesh](../images/08-hybrid-mesh.png "Hybrid mesh")

### _Selective Forwarding Unit_
SFU (_Selective Forwarding Unit_) juga menyelesaikan masalah _Full Mesh_, tetapi dengan cara yang sama sekali berbeda. SFU mengimplementasikan topologi _client/server_, bukannya P2P.
Setiap _peer_ WebRTC terhubung ke SFU dan mengunggah medianya. SFU kemudian meneruskan media ini ke setiap klien yang terhubung.

Dengan SFU setiap klien WebRTC hanya perlu mengenkode dan mengunggah video mereka sekali. Beban mendistribusikannya ke semua penonton ada pada SFU.
Konektivitas dengan SFU juga jauh lebih mudah daripada P2P. Anda dapat menjalankan SFU pada alamat yang dapat di-_route_ secara global, membuatnya jauh lebih mudah bagi klien untuk terhubung.
Anda tidak perlu khawatir tentang _NAT Mapping_. Anda masih perlu memastikan SFU Anda tersedia melalui TCP (baik melalui ICE-TCP atau TURN).

Membangun SFU sederhana dapat dilakukan dalam satu akhir pekan. Membangun SFU yang baik yang dapat menangani semua jenis klien tidak pernah berakhir. Menyetel _Congestion Control_, _Error
Correction_ dan Kinerja adalah tugas yang tidak pernah berakhir.

![Selective Forwarding Unit](../images/08-sfu.png "Selective Forwarding Unit")

### MCU
MCU (_Multi-point Conferencing Unit_) adalah topologi _client/server_ seperti SFU, tetapi menyusun _stream_ output. Alih-alih mendistribusikan media keluar
yang tidak dimodifikasi, ia mengenkodekannya kembali sebagai satu _feed_.

![Multi-point Conferencing Unit](../images/08-mcu.png "Multi-point Conferencing Unit")
