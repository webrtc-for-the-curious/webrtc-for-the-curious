---
title: Debugging
type: docs
weight: 10
---


# Debugging
_Debugging_ WebRTC bisa menjadi tugas yang menakutkan. Ada banyak bagian yang bergerak, dan semuanya bisa rusak secara independen. Jika Anda tidak hati-hati, Anda dapat kehilangan berminggu-minggu waktu melihat hal yang salah. Ketika Anda akhirnya menemukan bagian yang rusak, Anda perlu belajar sedikit untuk memahami mengapa.

Bab ini akan membawa Anda ke pola pikir untuk men-_debug_ WebRTC. Ini akan menunjukkan kepada Anda cara memecah masalah. Setelah kami mengetahui masalahnya, kami akan memberikan tur singkat dari alat _debugging_ yang populer.

## Isolasi Masalah

Saat men-_debug_, Anda perlu mengisolasi dari mana masalah berasal. Mulai dari awal...

### Kegagalan Signaling

### Kegagalan Jaringan

Uji _server_ STUN Anda menggunakan netcat:

1. Siapkan paket permintaan pengikatan **20-byte**:

    ```
    echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
    00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54                                       |TEST|
    00000014
    ```

    Interpretasi:
    - `00 01` adalah tipe pesan.
    - `00 00` adalah panjang bagian data.
    - `21 12 a4 42` adalah _magic cookie_.
    - dan `54 45 53 54 54 45 53 54 54 45 53 54` (Dekode ke ASCII: `TESTTESTTEST`) adalah _transaction ID_ 12-byte.

2. Kirim permintaan dan tunggu respons **32 byte**:

    ```
    stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
    00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
    00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
    00000020
    ```

    Interpretasi:
    - `01 01` adalah tipe pesan
    - `00 0c` adalah panjang bagian data yang didekode menjadi 12 dalam desimal
    - `21 12 a4 42` adalah _magic cookie_
    - dan `54 45 53 54 54 45 53 54 54 45 53 54` (Dekode ke ASCII: `TESTTESTTEST`) adalah _transaction ID_ 12-byte.
    - `00 20 00 08 00 01 6f 32 7f 36 de 89` adalah data 12-byte, interpretasi:
        - `00 20` adalah tipenya: `XOR-MAPPED-ADDRESS`
        - `00 08` adalah panjang bagian nilai yang didekode menjadi 8 dalam desimal
        - `00 01 6f 32 7f 36 de 89` adalah nilai data, interpretasi:
            - `00 01` adalah tipe alamat (IPv4)
            - `6f 32` adalah _port_ yang di-_XOR-mapped_
            - `7f 36 de 89` adalah alamat IP yang di-_XOR-mapped_

Mendekode bagian _XOR-mapped_ merepotkan, tetapi kita dapat mengelabui _server stun_ untuk melakukan _dummy XOR-mapping_, dengan memberikan _dummy magic cookie_ (tidak valid) yang disetel ke `00 00 00 00`:

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

_XOR-ing_ terhadap _dummy magic cookie_ adalah idempoten, jadi _port_ dan alamat akan jelas dalam respons. Ini tidak akan bekerja dalam semua situasi, karena beberapa _router_ memanipulasi paket yang lewat, curang pada alamat IP. Jika kita melihat nilai data yang dikembalikan (delapan _byte_ terakhir):

  - `00 01 4e 20 5e 24 7a cb` adalah nilai data, interpretasi:
    - `00 01` adalah tipe alamat (IPv4)
    - `4e 20` adalah _port_ yang di-_mapped_, yang didekode menjadi 20000 dalam desimal
    - `5e 24 7a cb` adalah alamat IP, yang didekode menjadi `94.36.122.203` dalam notasi _dotted-decimal_.

### Kegagalan Keamanan

### Kegagalan Media

### Kegagalan Data

## Alat perdagangan

### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat) adalah utilitas jaringan _command-line_ untuk membaca dari dan menulis ke koneksi jaringan menggunakan TCP atau UDP. Ini biasanya tersedia sebagai perintah `nc`.

### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) adalah penganalisis paket jaringan data _command-line_.

Perintah umum:
- Tangkap paket UDP ke dan dari _port_ 19302, cetak _hexdump_ dari konten paket:

    `sudo tcpdump 'udp port 19302' -xx`

- Sama, tetapi simpan paket dalam file PCAP (_packet capture_) untuk inspeksi nanti:

    `sudo tcpdump 'udp port 19302' -w stun.pcap`

  File PCAP dapat dibuka dengan aplikasi Wireshark: `wireshark stun.pcap`

### Wireshark

[Wireshark](https://www.wireshark.org) adalah penganalisis protokol jaringan yang banyak digunakan.

### Alat peramban WebRTC

Peramban dilengkapi dengan alat bawaan yang dapat Anda gunakan untuk memeriksa koneksi yang Anda buat. Chrome memiliki [`chrome://webrtc-internals`](chrome://webrtc-internals) dan [`chrome://webrtc-logs`](chrome://webrtc-logs). Firefox memiliki [`about:webrtc`](about:webrtc).

## Latensi
Bagaimana Anda tahu Anda memiliki latensi tinggi? Anda mungkin telah memperhatikan bahwa video Anda tertinggal, tetapi apakah Anda tahu persis berapa banyak tertinggal? 
Untuk dapat mengurangi latensi ini, Anda harus mulai dengan mengukurnya terlebih dahulu.

Latensi sejati seharusnya diukur _end-to-end_. Itu berarti tidak hanya latensi jalur jaringan antara pengirim dan penerima, tetapi latensi gabungan dari pengambilan kamera, pengkodean _frame_, transmisi, penerimaan, dekoding dan tampilan, serta kemungkinan antrian antara salah satu langkah ini.

Latensi _end-to-end_ bukan jumlah sederhana dari latensi setiap komponen.

Meskipun Anda secara teoritis dapat mengukur latensi komponen dari _pipeline_ transmisi video langsung secara terpisah dan kemudian menambahkannya bersama-sama, dalam praktiknya, setidaknya beberapa komponen akan tidak dapat diakses untuk instrumentasi, atau menghasilkan hasil yang sangat berbeda ketika diukur di luar _pipeline_.
Kedalaman antrian variabel antara tahap _pipeline_, topologi jaringan dan perubahan eksposur kamera hanyalah beberapa contoh komponen yang mempengaruhi latensi _end-to-end_.

Latensi intrinsik dari setiap komponen dalam sistem _live-streaming_ Anda dapat berubah dan mempengaruhi komponen _downstream_.
Bahkan konten video yang ditangkap mempengaruhi latensi. 
Misalnya, lebih banyak bit diperlukan untuk fitur frekuensi tinggi seperti cabang pohon, dibandingkan dengan langit biru yang jelas dengan frekuensi rendah.
Kamera dengan eksposur otomatis yang diaktifkan mungkin memakan waktu _jauh_ lebih lama daripada 33 milidetik yang diharapkan untuk menangkap _frame_, bahkan jika ketika tingkat pengambilan disetel ke 30 _frame_ per detik.
Transmisi melalui jaringan, terutama seluler, juga sangat dinamis karena permintaan yang berubah. 
Lebih banyak pengguna memperkenalkan lebih banyak obrolan di udara. 
Lokasi fisik Anda (zona sinyal rendah yang terkenal) dan beberapa faktor lain meningkatkan _packet loss_ dan latensi.
Apa yang terjadi ketika Anda mengirim paket ke antarmuka jaringan, katakanlah adaptor WiFi atau modem LTE untuk pengiriman?
Jika tidak dapat segera dikirim, ia akan diantrekan pada antarmuka, semakin besar antrian semakin banyak latensi yang diperkenalkan antarmuka jaringan tersebut.

### Pengukuran latensi _end-to-end_ manual
Ketika kita berbicara tentang latensi _end-to-end_, yang kami maksud adalah waktu antara _event_ terjadi dan diamati, artinya _frame_ video muncul di layar.

```
EndToEndLatency = T(observe) - T(happen)
```

Pendekatan naif adalah merekam waktu ketika _event_ terjadi dan menguranginya dari waktu pengamatan.
Namun, karena presisi turun ke milidetik sinkronisasi waktu menjadi masalah.
Mencoba menyinkronkan jam di seluruh sistem terdistribusi sebagian besar sia-sia, bahkan kesalahan kecil dalam sinkronisasi waktu menghasilkan pengukuran latensi yang tidak dapat diandalkan.

Solusi sederhana untuk masalah sinkronisasi jam adalah menggunakan jam yang sama.
Tempatkan pengirim dan penerima dalam kerangka referensi yang sama.

Bayangkan Anda memiliki jam milidetik yang berdetak atau sumber _event_ lainnya sebenarnya.
Anda ingin mengukur latensi dalam sistem yang melakukan _live stream_ jam ke layar _remote_ dengan mengarahkan kamera padanya.
Cara yang jelas untuk mengukur waktu antara _timer_ milidetik berdetak (T<sub>`happen`</sub>) dan _frame_ video jam muncul di layar (T<sub>`observe`</sub>) adalah sebagai berikut:
- Arahkan kamera Anda ke jam milidetik.
- Kirim _frame_ video ke penerima yang berada di lokasi fisik yang sama.
- Ambil gambar (gunakan ponsel Anda) dari _timer_ milidetik dan video yang diterima di layar.
- Kurangi dua waktu.

Itu adalah pengukuran latensi _end-to-end_ yang paling benar untuk diri Anda sendiri.
Ini memperhitungkan semua latensi komponen (kamera, _encoder_, jaringan, _decoder_) dan tidak bergantung pada sinkronisasi jam apa pun.

![DIY Latency](../images/09-diy-latency.png "DIY Latency Measurement").
![DIY Latency Example](../images/09-diy-latency-happen-observe.png "DIY Latency Measurement Example")
Dalam foto di atas latensi _end-to-end_ yang diukur adalah 101 milidetik. _Event_ yang terjadi sekarang adalah 10:16:02.862, tetapi pengamat sistem _live-streaming_ melihat 10:16:02.761. 

### Pengukuran latensi _end-to-end_ otomatis
Pada saat penulisan (Mei 2021) standar WebRTC untuk penundaan _end-to-end_ sedang aktif [dibahas](https://github.com/w3c/webrtc-stats/issues/537).
Firefox mengimplementasikan satu set API untuk membiarkan pengguna membuat pengukuran latensi otomatis di atas API WebRTC standar.
Namun dalam paragraf ini, kami membahas cara yang paling kompatibel untuk mengukur latensi secara otomatis.

![NTP Style Latency Measurement](../images/09-ntp-latency.png "NTP Style Latency Measurement")

_Roundtrip time_ dalam singkatnya: Saya mengirim Anda waktu saya `tR1`, ketika saya menerima kembali `tR1` saya pada waktu `tR2`, saya tahu _round trip time_ adalah `tR2 - tR1`.

Diberikan saluran komunikasi antara pengirim dan penerima (misalnya [DataChannel](https://webrtc.org/getting-started/data-channels)), penerima dapat memodelkan jam _monotonic_ pengirim dengan mengikuti langkah-langkah di bawah ini:
1. Pada waktu `tR1`, penerima mengirim pesan dengan _timestamp_ jam _monotonic_ lokalnya.
2. Ketika diterima di pengirim dengan waktu lokal `tS1`, pengirim merespons dengan salinan `tR1` serta `tS1` pengirim dan waktu _track video_ pengirim `tSV1`.
3. Pada waktu `tR2` di sisi penerima, _round trip time_ dihitung dengan mengurangi waktu pengiriman dan penerimaan pesan: `RTT = tR2 - tR1`.
4. _Round trip time_ `RTT` bersama dengan _timestamp_ lokal pengirim `tS1` cukup untuk membuat estimasi jam _monotonic_ pengirim. Waktu saat ini pada pengirim pada waktu `tR2` akan sama dengan `tS1` ditambah setengah dari _round trip time_.  
5. _Timestamp_ jam lokal pengirim `tS1` dipasangkan dengan _timestamp track video_ `tSV1` bersama dengan _round trip time_ `RTT` karena itu cukup untuk menyinkronkan waktu _track video_ penerima ke _track video_ pengirim. 

Sekarang kita tahu berapa banyak waktu telah berlalu sejak waktu _frame video_ pengirim yang dikenal terakhir `tSV1`, kita dapat memperkirakan latensi dengan mengurangi waktu _frame video_ yang ditampilkan saat ini (`actual_video_time`) dari waktu yang diharapkan:

```
expected_video_time = tSV1 + time_since(tSV1)
latency = expected_video_time - actual_video_time
```

Kelemahan metode ini adalah tidak termasuk latensi intrinsik kamera.
Sebagian besar sistem video menganggap _timestamp_ pengambilan _frame_ adalah waktu ketika _frame_ dari kamera dikirim ke memori utama, yang akan beberapa saat setelah _event_ yang direkam benar-benar terjadi.

#### Contoh estimasi latensi
Implementasi sampel membuka _data channel_ `latency` pada penerima dan secara berkala mengirim _timestamp timer monotonic_ penerima ke pengirim. Pengirim merespons kembali dengan pesan JSON dan penerima menghitung latensi berdasarkan pesan.

```json
{
    "received_time": 64714,       // Timestamp dikirim oleh penerima, pengirim memantulkan timestamp. 
    "delay_since_received": 46,   // Waktu yang berlalu sejak `received_time` terakhir diterima di pengirim.
    "local_clock": 1597366470336, // Waktu jam monotonic pengirim saat ini.
    "track_times_msec": {
        "myvideo_track1": [
            13100,        // Timestamp RTP frame video (dalam milidetik).
            1597366470289 // Timestamp jam monotonic frame video.
        ]
    }
}
```

Buka _data channel_ pada penerima:
```javascript
dataChannel = peerConnection.createDataChannel('latency');
```

Kirim waktu penerima `tR1` secara berkala. Contoh ini menggunakan 2 detik tanpa alasan tertentu:
```javascript
setInterval(() => {
    let tR1 = Math.trunc(performance.now());
    dataChannel.send("" + tR1);
}, 2000);
```

Tangani pesan masuk dari penerima di pengirim:
```javascript
// Assuming event.data is a string like "1234567".
tR1 = event.data
now = Math.trunc(performance.now());
tSV1 = 42000; // Current frame RTP timestamp converted to millisecond timescale.
tS1 = 1597366470289; // Current frame monotonic clock timestamp.
msg = {
  "received_time": tR1,
  "delay_since_received": 0,
  "local_clock": now,
  "track_times_msec": {
    "myvideo_track1": [tSV1, tS1]
  }
}
dataChannel.send(JSON.stringify(msg));
```

Tangani pesan masuk dari pengirim dan cetak latensi yang diestimasi ke `console`:
```javascript
let tR2 = performance.now();
let fromSender = JSON.parse(event.data);
let tR1 = fromSender['received_time'];
let delay = fromSender['delay_since_received']; // How much time that has passed between the sender receiving and sending the response.
let senderTimeFromResponse = fromSender['local_clock'];
let rtt = tR2 - delay - tR1;
let networkLatency = rtt / 2;
let senderTime = (senderTimeFromResponse + delay + networkLatency);
VIDEO.requestVideoFrameCallback((now, framemeta) => {
    // Estimate current time of the sender.
    let delaySinceVideoCallbackRequested = now - tR2;
    senderTime += delaySinceVideoCallbackRequested;
    let [tSV1, tS1] = Object.entries(fromSender['track_times_msec'])[0][1]
    let timeSinceLastKnownFrame = senderTime - tS1;
    let expectedVideoTimeMsec = tSV1 + timeSinceLastKnownFrame;
    let actualVideoTimeMsec = Math.trunc(framemeta.rtpTimestamp / 90); // Convert RTP timebase (90000) to millisecond timebase.
    let latency = expectedVideoTimeMsec - actualVideoTimeMsec;
    console.log('latency', latency, 'msec');
});
```

#### Waktu video aktual di peramban
> `<video>.requestVideoFrameCallback()` memungkinkan penulis web untuk diberi tahu ketika _frame_ telah disajikan untuk komposisi.

Sampai sangat baru-baru ini (Mei 2020), hampir tidak mungkin untuk mendapatkan _timestamp_ dari _frame video_ yang ditampilkan saat ini di peramban dengan andal. Metode solusi berdasarkan `video.currentTime` ada, tetapi tidak terlalu tepat. 
Baik pengembang peramban Chrome dan Mozilla [mendukung](https://github.com/mozilla/standards-positions/issues/250) pengenalan standar W3C baru, [`HTMLVideoElement.requestVideoFrameCallback()`](https://wicg.github.io/video-rvfc/), yang menambahkan _callback_ API untuk mengakses waktu _frame video_ saat ini.
Meskipun penambahan terdengar sepele, ini telah memungkinkan beberapa aplikasi media lanjutan di web yang memerlukan sinkronisasi audio dan video.
Khusus untuk WebRTC, _callback_ akan menyertakan bidang `rtpTimestamp`, _timestamp_ RTP yang terkait dengan _frame video_ saat ini. 
Ini harus ada untuk aplikasi WebRTC, tetapi tidak ada selain itu.

### Tips _Debugging_ Latensi
Karena _debugging_ kemungkinan akan mempengaruhi latensi yang diukur, aturan umum adalah menyederhanakan pengaturan Anda ke yang terkecil yang mungkin yang masih dapat mereproduksi masalah.
Semakin banyak komponen yang dapat Anda hapus, semakin mudah untuk mencari tahu komponen mana yang menyebabkan masalah latensi.

#### Latensi kamera
Tergantung pada pengaturan kamera latensi kamera mungkin bervariasi.
Periksa pengaturan eksposur otomatis, fokus otomatis dan keseimbangan putih otomatis.
Semua fitur "auto" dari kamera web memerlukan waktu ekstra untuk menganalisis gambar yang ditangkap sebelum membuatnya tersedia untuk _stack_ WebRTC.

Jika Anda di Linux, Anda dapat menggunakan alat _command line_ `v4l2-ctl` untuk mengontrol pengaturan kamera:
```bash
# Disable autofocus:
v4l2-ctl -d /dev/video0 -c focus_auto=0
# Set focus to infinity:
v4l2-ctl -d /dev/video0 -c focus_absolute=0
```

Anda juga dapat menggunakan alat UI grafis `guvcview` untuk dengan cepat memeriksa dan men-_tweak_ pengaturan kamera.

#### Latensi _encoder_
Sebagian besar _encoder_ modern akan _buffer_ beberapa _frame_ sebelum mengeluarkan yang dikode.
Prioritas pertama mereka adalah keseimbangan antara kualitas gambar yang dihasilkan dan _bitrate_. 
Pengkodean _multipass_ adalah contoh ekstrem dari pengabaian latensi output _encoder_.
Selama _pass_ pertama _encoder_ mencerna seluruh video dan hanya setelah itu mulai mengeluarkan _frame_.

Namun, dengan penyetelan yang tepat orang telah mencapai latensi _sub-frame_.
Pastikan _encoder_ Anda tidak menggunakan _reference frame_ yang berlebihan atau bergantung pada _B-frame_.
Pengaturan penyetelan latensi setiap _codec_ berbeda, tetapi untuk x264 kami merekomendasikan menggunakan `tune=zerolatency` dan `profile=baseline` untuk latensi output _frame_ terendah.

#### Latensi jaringan
Latensi jaringan adalah salah satu yang dapat Anda lakukan paling sedikit, selain meningkatkan ke koneksi jaringan yang lebih baik.
Latensi jaringan sangat mirip dengan cuaca - Anda tidak dapat menghentikan hujan, tetapi Anda dapat memeriksa prakiraan dan membawa payung.
WebRTC mengukur kondisi jaringan dengan presisi milidetik.
Metrik penting adalah:
- _Round-trip time_.
- _Packet loss_ dan retransmisi paket.

**Round-Trip Time**

_Stack_ WebRTC memiliki mekanisme pengukuran _round trip time_ (RTT) jaringan bawaan [mechanism](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats-roundtriptime).
Perkiraan latensi yang cukup baik adalah setengah dari RTT. Ini mengasumsikan bahwa dibutuhkan waktu yang sama untuk mengirim dan menerima paket, yang tidak selalu terjadi.
RTT menetapkan batas bawah pada latensi _end-to-end_.
_Frame video_ Anda tidak dapat mencapai penerima lebih cepat dari `RTT/2`, tidak peduli seberapa dioptimalkan _pipeline_ kamera ke _encoder_ Anda.

Mekanisme RTT bawaan didasarkan pada paket RTCP khusus yang disebut _sender/receiver reports_.
Pengirim mengirim pembacaan waktunya ke penerima, penerima pada gilirannya memantulkan _timestamp_ yang sama ke pengirim. 
Dengan demikian pengirim tahu berapa banyak waktu yang dibutuhkan paket untuk melakukan perjalanan ke penerima dan kembali.
Lihat bab [Sender/Receiver Reports](../06-media-communication/#senderreceiver-reports) untuk lebih detail tentang pengukuran RTT. 

**Packet loss dan retransmisi paket**

Baik RTP dan RTCP adalah protokol berdasarkan UDP, yang tidak memiliki jaminan pengurutan, pengiriman yang berhasil, atau non-duplikasi.
Semua hal di atas dapat dan memang terjadi dalam aplikasi WebRTC dunia nyata.
Implementasi _decoder_ yang tidak canggih mengharapkan semua paket dari _frame_ dikirim agar _decoder_ berhasil merakit gambar.
Dalam kehadiran _packet loss_ artefak dekoding mungkin muncul jika paket dari [P-frame](../06-media-communication/#inter-frame-types) hilang.
Jika paket I-frame hilang maka semua _frame_ dependen akan mendapatkan artefak berat atau tidak akan didekode sama sekali. 
Kemungkinan besar ini akan membuat video "membeku" untuk sesaat.

Untuk menghindari (yah, setidaknya untuk mencoba menghindari) pembekuan video atau artefak dekoding, WebRTC menggunakan pesan pengakuan negatif ([NACK](../06-media-communication/#negative-acknowledgment)).
Ketika penerima tidak mendapatkan paket RTP yang diharapkan, ia mengembalikan pesan NACK untuk memberi tahu pengirim untuk mengirim paket yang hilang lagi.
Penerima _menunggu_ untuk retransmisi paket.
Retransmisi seperti itu menyebabkan peningkatan latensi.
Jumlah paket NACK yang dikirim dan diterima dicatat dalam bidang statistik bawaan WebRTC [outbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-nackcount) dan [inbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-nackcount).

Anda dapat melihat grafik bagus dari `nackCount` _inbound_ dan _outbound_ di [halaman webrtc internals](#webrtc-browser-tools). 
Jika Anda melihat `nackCount` meningkat, itu berarti jaringan mengalami _packet loss_ tinggi, dan _stack_ WebRTC melakukan yang terbaik untuk membuat pengalaman video/audio yang mulus meskipun itu.

Ketika _packet loss_ sangat tinggi sehingga _decoder_ tidak dapat menghasilkan gambar, atau gambar dependen berikutnya seperti dalam kasus I-frame yang hilang sepenuhnya, semua P-frame masa depan tidak akan didekode. 
Penerima akan mencoba mengurangi itu dengan mengirim pesan _Picture Loss Indication_ khusus ([PLI](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)).
Setelah pengirim menerima `PLI`, ia akan menghasilkan I-frame baru untuk membantu _decoder_ penerima.
I-frame biasanya lebih besar dalam ukuran daripada P-frame. Ini meningkatkan jumlah paket yang perlu ditransmisikan.
Seperti dengan pesan NACK, penerima perlu menunggu I-frame baru, memperkenalkan latensi tambahan.

Perhatikan `pliCount` di [halaman webrtc internals](#webrtc-browser-tools). Jika meningkat, _tweak encoder_ Anda untuk menghasilkan lebih sedikit paket atau aktifkan mode yang lebih tahan kesalahan.

#### Latensi sisi penerima
Latensi akan dipengaruhi oleh paket yang tiba tidak berurutan.
Jika paket setengah bawah gambar datang sebelum atas Anda harus menunggu atas sebelum dekoding.
Ini dijelaskan dalam bab [Solving Jitter](../05-real-time-networking/#solving-jitter) dengan sangat detail.

Anda juga dapat merujuk ke metrik bawaan [jitterBufferDelay](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) untuk melihat berapa lama _frame_ ditahan di _buffer_ penerimaan, menunggu semua paketnya sampai dilepaskan ke _decoder_.
