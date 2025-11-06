---
title: Real-time Networking
type: docs
weight: 6
---

# Real-time Networking

## Mengapa jaringan begitu penting dalam komunikasi _Real-time_?

Jaringan adalah faktor pembatas dalam komunikasi _Real-time_. Dalam dunia yang ideal kita akan memiliki _bandwidth_ tak terbatas
dan paket akan tiba secara instan. Namun ini tidak terjadi. Jaringan terbatas, dan kondisinya
dapat berubah kapan saja. Mengukur dan mengamati kondisi jaringan juga merupakan masalah yang sulit. Anda bisa mendapatkan perilaku yang berbeda
tergantung pada perangkat keras, perangkat lunak dan konfigurasinya.

Komunikasi _real-time_ juga menghadirkan masalah yang tidak ada di sebagian besar domain lain. Untuk _developer_ web, tidak fatal
jika situs web Anda lebih lambat di beberapa jaringan. Selama semua data tiba, pengguna senang. Dengan WebRTC, jika data Anda
terlambat, itu tidak berguna. Tidak ada yang peduli tentang apa yang dikatakan dalam panggilan konferensi 5 detik yang lalu. Jadi ketika mengembangkan sistem komunikasi _realtime_,
Anda harus membuat _trade-off_. Apa batas waktu saya, dan berapa banyak data yang dapat saya kirim?

Bab ini mencakup konsep yang berlaku untuk komunikasi data dan media. Pada bab selanjutnya kita akan melampaui
teorinya dan membahas bagaimana subsistem media dan data WebRTC menyelesaikan masalah ini.

## Apa atribut jaringan yang membuatnya sulit?
Kode yang efektif bekerja di semua jaringan adalah rumit. Anda memiliki banyak faktor berbeda, dan mereka
semua dapat saling mempengaruhi secara halus. Ini adalah masalah paling umum yang akan dihadapi _developer_.

#### _Bandwidth_
_Bandwidth_ adalah laju maksimum data yang dapat ditransfer melintasi jalur tertentu. Penting untuk diingat
ini juga bukan angka statis. _Bandwidth_ akan berubah sepanjang rute seiring lebih banyak (atau lebih sedikit) orang menggunakannya.

#### _Transmission Time_ dan _Round Trip Time_
_Transmission Time_ adalah berapa lama waktu yang dibutuhkan paket untuk tiba di tujuannya. Seperti _Bandwidth_ ini tidak konstan. _Transmission Time_ dapat berfluktuasi kapan saja.

`transmission_time = receive_time - send_time`

Untuk menghitung _transmission time_, Anda memerlukan jam pada pengirim dan penerima yang disinkronkan dengan presisi milidetik.
Bahkan penyimpangan kecil akan menghasilkan pengukuran _transmission time_ yang tidak dapat diandalkan.
Karena WebRTC beroperasi di lingkungan yang sangat heterogen, hampir mustahil untuk mengandalkan sinkronisasi waktu sempurna antara _host_.

Pengukuran _round-trip time_ adalah solusi untuk sinkronisasi jam yang tidak sempurna.

Alih-alih beroperasi pada jam terdistribusi, _peer_ WebRTC mengirim paket khusus dengan _timestamp_-nya sendiri `sendertime1`.
_Peer_ yang bekerja sama menerima paket dan memantulkan _timestamp_ kembali ke pengirim.
Setelah pengirim asli mendapat waktu yang dipantulkan, ia mengurangi _timestamp_ `sendertime1` dari waktu saat ini `sendertime2`.
Delta waktu ini disebut "_round-trip propagation delay_" atau lebih umum _round-trip time_.

`rtt = sendertime2 - sendertime1`

Setengah dari _round trip time_ dianggap sebagai perkiraan yang cukup baik dari _transmission time_.
Solusi ini tidak tanpa kekurangan.
Ini membuat asumsi bahwa dibutuhkan waktu yang sama untuk mengirim dan menerima paket.
Namun pada jaringan seluler, operasi pengiriman dan penerimaan mungkin tidak simetris waktu.
Anda mungkin telah memperhatikan bahwa kecepatan unggah pada ponsel Anda hampir selalu lebih rendah daripada kecepatan unduh.

`transmission_time = rtt/2`

Teknisnya pengukuran _round-trip time_ dijelaskan lebih detail dalam [bab RTCP Sender dan Receiver Reports](../06-media-communication/#receiver-reports--sender-reports).

#### _Jitter_
_Jitter_ adalah fakta bahwa `Transmission Time` dapat bervariasi untuk setiap paket. Paket Anda dapat ditunda, tetapi kemudian tiba dalam ledakan.

#### _Packet Loss_
_Packet Loss_ adalah ketika pesan hilang dalam transmisi. Kehilangan bisa stabil, atau bisa datang dalam lonjakan.
Ini bisa karena jenis jaringan seperti satelit atau Wi-Fi. Atau bisa diperkenalkan oleh perangkat lunak di sepanjang jalan.

#### _Maximum Transmission Unit_
_Maximum Transmission Unit_ adalah batas seberapa besar satu paket tunggal bisa. Jaringan tidak mengizinkan Anda mengirim
satu pesan raksasa. Pada level protokol, pesan mungkin harus dipecah menjadi beberapa paket yang lebih kecil.

MTU juga akan berbeda tergantung pada jalur jaringan apa yang Anda ambil. Anda dapat
menggunakan protokol seperti [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) untuk mengetahui ukuran paket terbesar yang dapat Anda kirim.

### _Congestion_
_Congestion_ adalah ketika batas jaringan telah tercapai. Ini biasanya karena Anda telah mencapai puncak
_bandwidth_ yang dapat ditangani rute saat ini. Atau bisa operator yang memaksakan seperti batas per jam yang dikonfigurasi ISP Anda.

_Congestion_ menampakkan dirinya dalam banyak cara berbeda. Tidak ada perilaku standar. Dalam kebanyakan kasus ketika _congestion_
tercapai jaringan akan menjatuhkan paket berlebih. Dalam kasus lain jaringan akan _buffer_. Ini akan menyebabkan _Transmission Time_
untuk paket Anda meningkat. Anda juga dapat melihat lebih banyak _jitter_ saat jaringan Anda menjadi padat. Ini adalah area yang berubah dengan cepat
dan algoritma baru untuk deteksi _congestion_ masih ditulis.

### Dinamis
Jaringan sangat dinamis dan kondisinya dapat berubah dengan cepat. Selama panggilan Anda dapat mengirim dan menerima ratusan ribu paket.
Paket-paket itu akan melakukan perjalanan melalui beberapa _hop_. _Hop_ tersebut akan dibagikan oleh jutaan pengguna lain. Bahkan di jaringan lokal Anda, Anda dapat memiliki
film HD yang diunduh atau mungkin perangkat memutuskan untuk mengunduh pembaruan perangkat lunak.

Memiliki panggilan yang baik tidak sesederhana mengukur jaringan Anda saat startup. Anda perlu terus mengevaluasi. Anda juga perlu menangani semua perilaku berbeda
yang berasal dari banyak perangkat keras dan perangkat lunak jaringan.

## Menyelesaikan _Packet Loss_
Menangani _packet loss_ adalah masalah pertama untuk diselesaikan. Ada beberapa cara untuk menyelesaikannya, masing-masing dengan manfaatnya sendiri. Ini tergantung pada apa yang Anda kirim dan seberapa
toleran Anda terhadap latensi. Penting juga untuk dicatat bahwa tidak semua _packet loss_ fatal. Kehilangan beberapa video mungkin bukan masalah, mata manusia mungkin bahkan tidak
mampu menganggapnya. Kehilangan pesan teks pengguna adalah fatal.

Katakanlah Anda mengirim 10 paket, dan paket 5 dan 6 hilang. Ini adalah cara Anda dapat menyelesaikannya.

### _Acknowledgments_
_Acknowledgments_ adalah ketika penerima memberi tahu pengirim setiap paket yang telah mereka terima. Pengirim menyadari _packet loss_ ketika ia mendapat _acknowledgment_
untuk paket dua kali yang bukan final. Ketika pengirim mendapat `ACK` untuk paket 4 dua kali, ia tahu bahwa paket 5 belum terlihat.

### _Selective Acknowledgments_
_Selective Acknowledgments_ adalah peningkatan dari _Acknowledgments_. Penerima dapat mengirim `SACK` yang mengakui beberapa paket dan memberi tahu pengirim tentang kesenjangan.
Sekarang pengirim dapat mendapat `SACK` untuk paket 4 dan 7. Kemudian ia tahu ia perlu mengirim ulang paket 5 dan 6.

### _Negative Acknowledgments_
_Negative Acknowledgments_ menyelesaikan masalah dengan cara sebaliknya. Alih-alih memberi tahu pengirim apa yang telah diterimanya, penerima memberi tahu pengirim apa yang telah hilang. Dalam kasus kami `NACK`
akan dikirim untuk paket 5 dan 6. Pengirim hanya mengetahui paket yang ingin dikirim ulang oleh penerima.

### _Forward Error Correction_
_Forward Error Correction_ memperbaiki _packet loss_ secara pre-emptif. Pengirim mengirim data redundan, yang berarti paket yang hilang tidak mempengaruhi _stream_ akhir. Salah satu algoritma populer untuk
ini adalah koreksi kesalahan Reed–Solomon.

Ini mengurangi latensi/kompleksitas pengiriman dan penanganan _Acknowledgments_. _Forward Error Correction_ adalah pemborosan _bandwidth_ jika jaringan tempat Anda berada memiliki nol kehilangan.

## Menyelesaikan _Jitter_
_Jitter_ hadir di sebagian besar jaringan. Bahkan di dalam LAN Anda memiliki banyak perangkat yang mengirim data pada tingkat yang berfluktuasi. Anda dapat dengan mudah mengamati _jitter_ dengan melakukan ping perangkat lain dengan perintah `ping` dan memperhatikan fluktuasi dalam latensi _round-trip_.

Untuk menyelesaikan _jitter_, klien menggunakan JitterBuffer. JitterBuffer memastikan waktu pengiriman paket yang stabil. Kelemahannya adalah JitterBuffer menambahkan beberapa latensi ke paket yang tiba lebih awal.
Sisi baiknya adalah paket yang terlambat tidak menyebabkan _jitter_. Bayangkan bahwa selama panggilan, Anda melihat waktu kedatangan paket berikut:

```
* time=1.46 ms
* time=1.93 ms
* time=1.57 ms
* time=1.55 ms
* time=1.54 ms
* time=1.72 ms
* time=1.45 ms
* time=1.73 ms
* time=1.80 ms
```

Dalam kasus ini, sekitar 1,8 ms akan menjadi pilihan yang baik. Paket yang tiba terlambat akan menggunakan jendela latensi kami. Paket yang tiba lebih awal akan ditunda sedikit dan dapat
mengisi jendela yang habis oleh paket yang terlambat. Ini berarti kita tidak lagi memiliki gagap dan memberikan tingkat pengiriman yang lancar untuk klien.

### Operasi JitterBuffer

![JitterBuffer](../images/05-jitterbuffer.png "JitterBuffer")

Setiap paket ditambahkan ke _jitter buffer_ segera setelah diterima.
Setelah ada cukup paket untuk merekonstruksi _frame_, paket yang membentuk _frame_ dilepaskan dari _buffer_ dan dikeluarkan untuk dekoding.
Decoder, pada gilirannya, mendekode dan menggambar _frame_ video di layar pengguna.
Karena _jitter buffer_ memiliki kapasitas terbatas, paket yang tetap di _buffer_ terlalu lama akan dibuang.

Baca lebih lanjut tentang bagaimana _frame_ video dikonversi menjadi paket RTP, dan mengapa rekonstruksi diperlukan [dalam bab komunikasi media](../06-media-communication/#rtp).

`jitterBufferDelay` memberikan wawasan yang baik tentang kinerja jaringan Anda dan pengaruhnya pada kelancaran pemutaran.
Ini adalah bagian dari [WebRTC statistics API](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) yang relevan dengan _stream_ masuk penerima.
Penundaan mendefinisikan jumlah waktu _frame_ video menghabiskan di _jitter buffer_ sebelum dikeluarkan untuk dekoding.
Penundaan _jitter buffer_ yang panjang berarti jaringan Anda sangat padat.

## Mendeteksi _Congestion_
Sebelum kita dapat menyelesaikan _congestion_, kita perlu mendeteksinya. Untuk mendeteksinya kita menggunakan _congestion controller_. Ini adalah subjek yang rumit, dan masih berubah dengan cepat.
Algoritma baru masih diterbitkan dan diuji. Pada level tinggi mereka semua beroperasi sama. _Congestion controller_ memberikan estimasi _bandwidth_ yang diberikan beberapa input.
Ini beberapa input yang mungkin:

* **Packet Loss** - Paket dijatuhkan saat jaringan menjadi padat.
* **Jitter** - Saat peralatan jaringan menjadi lebih kelebihan beban, antrian paket akan menyebabkan waktu menjadi tidak menentu.
* **Round Trip Time** - Paket membutuhkan waktu lebih lama untuk tiba ketika padat. Tidak seperti _jitter_, _Round Trip Time_ terus meningkat.
* **Explicit Congestion Notification** - Jaringan yang lebih baru dapat menandai paket sebagai berisiko dijatuhkan untuk mengurangi _congestion_.

Nilai-nilai ini perlu diukur terus-menerus selama panggilan. Pemanfaatan jaringan dapat meningkat atau menurun, sehingga _bandwidth_ yang tersedia dapat terus berubah.

## Menyelesaikan _Congestion_
Sekarang kita memiliki estimasi _bandwidth_ kita perlu menyesuaikan apa yang kita kirim. Bagaimana kita menyesuaikan tergantung pada jenis data apa yang ingin kita kirim.

### Mengirim Lebih Lambat
Membatasi kecepatan di mana Anda mengirim data adalah solusi pertama untuk mencegah _congestion_. _Congestion Controller_ memberi Anda estimasi, dan itu adalah
tanggung jawab pengirim untuk membatasi laju.

Ini adalah metode yang digunakan untuk sebagian besar komunikasi data. Dengan protokol seperti TCP ini semua dilakukan oleh sistem operasi dan sepenuhnya transparan bagi pengguna dan _developer_.

### Mengirim Lebih Sedikit
Dalam beberapa kasus kita dapat mengirim lebih sedikit informasi untuk memenuhi batas kita. Kita juga memiliki tenggat waktu keras untuk kedatangan data kita, jadi kita tidak bisa mengirim lebih lambat. Ini adalah kendala
yang dimiliki media _Real-time_.

Jika kita tidak memiliki cukup _bandwidth_ yang tersedia, kita dapat menurunkan kualitas video yang kita kirim. Ini memerlukan _feedback loop_ yang ketat antara _video encoder_ dan _congestion controller_ Anda.
