---
title: History
type: docs
weight: 11
---


# History
Ketika mempelajari WebRTC, _developer_ sering merasa frustrasi dengan kompleksitasnya. Mereka
melihat fitur WebRTC yang tidak relevan dengan proyek mereka saat ini dan berharap WebRTC lebih
sederhana. Masalahnya adalah bahwa setiap orang memiliki set kasus penggunaan yang berbeda. Komunikasi _real-time_ memiliki
sejarah yang kaya dengan banyak orang yang berbeda membangun banyak hal yang berbeda.

Bab ini berisi wawancara dengan penulis protokol yang membentuk WebRTC.
Ini memberikan wawasan tentang desain yang dibuat saat membangun setiap protokol, dan
diakhiri dengan wawancara tentang WebRTC itu sendiri. Jika Anda memahami niat dan desain dari
perangkat lunak, Anda dapat membangun sistem yang lebih efektif dengannya.

## RTP
RTP dan RTCP adalah protokol yang menangani semua transpor media untuk WebRTC. Ini
didefinisikan dalam [RFC 1889](https://tools.ietf.org/html/rfc1889) pada Januari 1996.
Kami sangat beruntung memiliki salah satu penulis [Ron
Frederick](https://github.com/ronf) berbicara tentang itu sendiri. Ron baru-baru ini mengunggah
[Network Video tool](https://github.com/ronf/nv) ke GitHub, sebuah proyek yang
menginformasikan RTP.

### Dengan kata-katanya sendiri

Pada Oktober 1992, saya mulai bereksperimen dengan kartu _frame grabber_ Sun VideoPix, dengan ide menulis alat konferensi video jaringan berdasarkan _multicast_ IP. Ini dimodelkan setelah "vat" -- alat konferensi audio yang dikembangkan
di LBL, karena menggunakan protokol sesi _lightweight_ yang serupa untuk pengguna
bergabung ke konferensi, di mana Anda cukup mengirim data ke grup _multicast_ tertentu dan menonton grup itu untuk lalu lintas apa pun dari anggota grup
lainnya.

Agar program benar-benar berhasil, ia perlu mengompresi
data video sebelum menempatkannya di jaringan. Tujuan saya adalah membuat
_stream_ data yang terlihat dapat diterima yang akan masuk dalam sekitar 128 kbps, atau _bandwidth_ yang tersedia pada jalur ISDN rumah standar. Saya juga berharap menghasilkan
sesuatu yang masih dapat ditonton yang masuk dalam setengah _bandwidth_ ini. Ini
berarti saya memerlukan faktor kompresi sekitar 20 untuk ukuran
gambar dan _frame rate_ tertentu yang saya kerjakan. Saya dapat mencapai kompresi ini dan mengajukan paten untuk teknik yang saya gunakan, kemudian diberikan
sebagai paten [US5485212A][1]: Kompresi video perangkat lunak untuk konferensi telepon.

[1]: https://patents.google.com/patent/US5485212A

Pada awal November 1992, saya merilis alat konferensi video "nv" (dalam
bentuk biner) ke komunitas Internet. Setelah beberapa pengujian awal, itu digunakan
untuk _videocast_ bagian dari _Internet Engineering Task Force_ November ke seluruh
dunia. Sekitar 200 subnet di 15 negara mampu
menerima siaran ini, dan sekitar 50-100 orang menerima video menggunakan
"nv" di beberapa titik dalam minggu itu.

Selama beberapa bulan berikutnya, tiga _workshop_ lain dan beberapa pertemuan yang lebih kecil
menggunakan "nv" untuk menyiarkan ke Internet secara luas, termasuk
_Australian NetWorkshop_, _workshop MCNC Packet Audio and Video_, dan
_workshop_ MultiG tentang realitas virtual terdistribusi di Swedia.

Rilis _source code_ dari "nv" mengikuti pada Februari 1993, dan pada Maret saya
merilis versi alat di mana saya memperkenalkan skema kompresi berbasis _wavelet_ yang baru. Pada Mei 1993, saya menambahkan dukungan untuk video berwarna.

Protokol jaringan yang digunakan untuk "nv" dan alat konferensi Internet lainnya
menjadi dasar dari _Realtime Transport Protocol_ (RTP), distandarisasi
melalui _Internet Engineering Task Force_ (IETF), pertama kali diterbitkan dalam
RFC [1889][2]-[1890][3] dan kemudian direvisi dalam RFC [3550][4]-[3551][5]
bersama dengan berbagai RFC lain yang mencakup profil untuk membawa format
audio dan video tertentu.

[2]: https://tools.ietf.org/html/rfc1889
[3]: https://tools.ietf.org/html/rfc1890
[4]: https://tools.ietf.org/html/rfc3550
[5]: https://tools.ietf.org/html/rfc3551

Selama beberapa tahun berikutnya, pekerjaan berlanjut pada "nv", mem-_port_ alat
ke sejumlah platform perangkat keras dan perangkat pengambilan video tambahan.
Ini terus digunakan sebagai salah satu alat utama untuk menyiarkan
konferensi di Internet pada saat itu, termasuk dipilih oleh NASA
untuk menyiarkan liputan langsung misi _shuttle_ secara _online_.

Pada 1994, saya menambahkan dukungan dalam "nv" untuk mendukung algoritma kompresi video
yang dikembangkan oleh orang lain, termasuk beberapa skema kompresi perangkat keras seperti
format CellB yang didukung oleh kartu pengambilan video SunVideo. Ini juga
memungkinkan "nv" untuk mengirim video dalam format CUSeeMe, untuk mengirim video ke pengguna
yang menjalankan CUSeeMe pada Mac dan PC.

Versi yang dirilis secara publik terakhir dari "nv" adalah versi 3.3beta, dirilis
pada Juli 1994. Saya sedang mengerjakan rilis "4.0alpha" yang dimaksudkan
untuk memigrasikan "nv" ke versi 2 dari protokol RTP, tetapi pekerjaan ini tidak
pernah selesai karena saya pindah ke proyek lain. Salinan kode 4.0
alpha disertakan dalam arsip [Network Video tool](https://github.com/ronf/nv)
untuk kelengkapan, tetapi tidak lengkap dan ada masalah yang diketahui
dengannya, terutama dalam dukungan RTPv2 yang tidak lengkap.

_Framework_ yang disediakan dalam "nv" kemudian menjadi dasar konferensi video
dalam proyek "Jupiter _multi-media_ MOO" di Xerox PARC, yang
akhirnya menjadi dasar untuk perusahaan _spin-off_ "PlaceWare", kemudian
diakuisisi oleh Microsoft. Ini juga digunakan sebagai dasar untuk sejumlah
proyek konferensi video perangkat keras yang memungkinkan pengiriman video berkualitas siaran NTSC penuh melalui _Ethernet_ dan jaringan ATM _bandwidth_ tinggi.
Saya juga kemudian menggunakan beberapa kode ini sebagai dasar untuk "Mediastore", yang
adalah layanan perekaman dan pemutaran video berbasis jaringan.

### Apakah Anda ingat motivasi/ide orang lain di _draft_?

Kami semua adalah peneliti yang bekerja pada _multicast_ IP, dan membantu membuat
_Internet multicast backbone_ (alias MBONE). MBONE diciptakan oleh
Steve Deering (yang pertama kali mengembangkan _multicast_ IP), Van Jacobson, dan Steve
Casner. Steve Deering dan saya memiliki penasihat yang sama di Stanford, dan Steve
akhirnya pergi bekerja di Xerox PARC ketika ia meninggalkan Stanford, saya menghabiskan
musim panas di Xerox PARC sebagai _intern_ yang bekerja pada proyek terkait _multicast_ IP
dan terus bekerja untuk mereka paruh waktu saat di Stanford dan kemudian penuh
waktu. Van Jacobson dan Steve Casner adalah dua dari empat penulis pada
RFC RTP awal, bersama dengan Henning Schulzrinne dan saya sendiri. Kami semua
memiliki alat MBONE yang kami kerjakan yang memungkinkan berbagai bentuk
kolaborasi _online_, dan mencoba untuk menghasilkan protokol dasar umum
yang dapat digunakan semua alat ini adalah yang mengarah pada RTP.

### _Multicast_ sangat menarik. WebRTC sepenuhnya _unicast_, bisakah Anda menjelaskan tentang itu?

Sebelum sampai ke Stanford dan belajar tentang _multicast_ IP, saya memiliki
sejarah panjang bekerja pada cara menggunakan komputer sebagai cara bagi orang untuk
berkomunikasi satu sama lain. Ini dimulai pada awal 80-an untuk saya
di mana saya menjalankan sistem _bulletin board dial-up_ di mana orang dapat masuk
dan meninggalkan pesan untuk satu sama lain, baik pribadi (semacam setara
dengan e-mail) dan publik (grup diskusi). Sekitar waktu yang sama, saya juga
belajar tentang penyedia layanan _online_ CompuServe. Salah satu fitur keren
pada CompuServe adalah sesuatu yang disebut "CB Simulator" di mana orang
dapat berbicara satu sama lain secara _real-time_. Itu semua berbasis teks, tetapi memiliki
gagasan tentang "saluran" seperti radio CB nyata, dan beberapa orang
dapat melihat apa yang diketik orang lain, selama mereka berada di saluran yang sama.
Saya membangun versi CB saya sendiri yang berjalan pada sistem _timesharing_ yang saya miliki
akses ke yang memungkinkan pengguna pada sistem itu mengirim pesan satu sama lain
secara _real-time_, dan selama beberapa tahun berikutnya saya bekerja dengan teman-teman untuk
mengembangkan versi yang lebih canggih dari alat komunikasi _real-time_
pada beberapa sistem komputer dan jaringan yang berbeda. Bahkan, salah satu dari sistem itu masih beroperasi, dan saya menggunakannya untuk berbicara setiap hari kepada orang-orang yang saya
kuliah bersama 30+ tahun yang lalu!

Semua alat itu berbasis teks, karena komputer pada saat itu umumnya
tidak memiliki kemampuan audio/video apa pun, tetapi ketika saya sampai ke Stanford dan
belajar tentang _multicast_ IP, saya tertarik dengan gagasan menggunakan _multicast_
untuk mendapatkan sesuatu yang lebih seperti "radio" nyata di mana Anda dapat mengirim sinyal
keluar ke jaringan yang tidak ditujukan kepada siapa pun khususnya, tetapi
semua orang yang menyetel ke "saluran" itu dapat menerimanya. Kebetulan,
komputer tempat saya mem-_port_ kode _multicast_ IP adalah generasi pertama
SPARC-station dari Sun, dan itu sebenarnya memiliki perangkat keras audio berkualitas telepon bawaan! Anda dapat mendigitalkan suara dari mikrofon dan memutarnya kembali melalui
_speaker_ bawaan (atau melalui output _headphone_). Jadi, pikiran pertama saya adalah untuk
mencari tahu bagaimana mengirim audio itu keluar ke jaringan secara _real-time_ menggunakan
_multicast_ IP, dan melihat apakah saya dapat membangun setara "radio CB" dengan audio
aktual alih-alih teks.

Ada beberapa hal rumit yang harus diselesaikan, seperti fakta bahwa komputer
hanya dapat memutar satu _stream_ audio pada satu waktu, jadi jika beberapa orang berbicara
Anda perlu secara matematis "mencampur" beberapa _stream_ audio menjadi satu sebelum
Anda dapat memutarnya, tetapi itu semua dapat dilakukan dalam perangkat lunak setelah Anda memahami
bagaimana pengambilan sampel audio bekerja. Aplikasi audio itu membawa saya untuk bekerja pada
MBONE dan akhirnya berpindah dari audio ke video dengan "nv".

### Apakah ada yang tertinggal dari protokol yang Anda harap Anda tambahkan? Apakah ada dalam protokol yang Anda sesali?

Saya tidak akan mengatakan saya menyesalinya, tetapi salah satu keluhan besar yang akhirnya dimiliki orang
tentang RTP adalah kompleksitas mengimplementasikan RTCP, protokol kontrol
yang berjalan paralel dengan lalu lintas data RTP utama. Saya pikir kompleksitas itu
adalah bagian besar mengapa RTP tidak lebih banyak diadopsi, terutama dalam
kasus _unicast_ di mana tidak ada banyak kebutuhan untuk beberapa fitur RTCP.
Karena _bandwidth_ jaringan menjadi kurang langka dan kemacetan bukan masalah besar,
banyak orang hanya akhirnya _streaming_ audio & video melalui TCP biasa
(dan kemudian HTTP), dan secara umum itu bekerja "cukup baik" sehingga
tidak layak berurusan dengan RTP.

Sayangnya, menggunakan TCP atau HTTP berarti bahwa aplikasi audio dan video multi-pihak
harus mengirim data yang sama melalui jaringan beberapa kali,
ke setiap _peer_ yang perlu menerimanya, membuatnya jauh kurang
efisien dari perspektif _bandwidth_. Saya kadang-kadang berharap kami telah mendorong
lebih keras untuk mendapatkan _multicast_ IP yang diadopsi di luar hanya komunitas penelitian.
Saya pikir kami bisa melihat transisi dari televisi kabel dan siaran
ke audio dan video berbasis Internet jauh lebih cepat jika kami melakukannya.

### Hal-hal apa yang Anda bayangkan dibangun dengan RTP? Apakah Anda memiliki proyek/ide RTP keren yang hilang dalam waktu?

Salah satu hal yang menyenangkan yang saya bangun adalah versi dari permainan klasik "Spacewar"
yang menggunakan _multicast_ IP. Tanpa memiliki jenis _server_ pusat apa pun, beberapa
klien dapat masing-masing menjalankan _binary spacewar_ dan mulai menyiarkan
lokasi kapal mereka, kecepatan, arah yang dihadapi, dan informasi serupa
untuk "peluru" apa pun yang telah mereka tembakkan, dan semua _instance_ lain
akan mengambil informasi itu dan merendernya secara lokal, memungkinkan pengguna untuk semua
melihat kapal dan peluru satu sama lain, dengan kapal "meledak" jika mereka menabrak
satu sama lain atau peluru mengenai mereka. Saya bahkan membuat "puing-puing" dari
ledakan objek hidup yang dapat mengeluarkan kapal lain, kadang-kadang mengarah ke
reaksi berantai yang menyenangkan!

Dalam semangat permainan asli, saya merendernya menggunakan grafik vektor
yang disimulasikan, jadi Anda dapat melakukan hal-hal seperti memperbesar tampilan Anda masuk & keluar dan
semuanya akan naik/turun skala. Kapal-kapal itu sendiri adalah sekelompok
segmen garis dalam bentuk vektor yang saya minta beberapa rekan saya di PARC
bantu saya desain, jadi kapal setiap orang memiliki tampilan unik padanya.

Pada dasarnya, apa pun yang dapat mengambil manfaat dari _stream_ data _real-time_ yang
tidak memerlukan pengiriman _in-order_ yang sempurna dapat mengambil manfaat dari RTP. Jadi, selain
audio & video kami dapat membangun hal-hal seperti _shared whiteboard_. Bahkan transfer file
dapat mengambil manfaat dari RTP, terutama dalam hubungannya dengan _multicast_ IP.

Bayangkan sesuatu seperti BitTorrent tetapi di mana Anda tidak memerlukan semua data
yang berjalan _point-to-point_ antara _peer_. _Seeder_ asli dapat mengirim _stream multicast_
ke semua _leeche_ sekaligus, dan kehilangan paket apa pun di sepanjang jalan
dapat dengan cepat dibersihkan oleh retransmisi dari _peer_ apa pun yang
berhasil menerima data. Anda bahkan dapat membatasi permintaan retransmisi Anda
sehingga beberapa _peer_ di dekatnya mengirimkan salinan data, dan itu
juga dapat di-_multicast_ ke orang lain di wilayah itu, karena kehilangan paket di
tengah jaringan akan cenderung berarti sekelompok klien
_downstream_ dari titik itu semua melewatkan data yang sama.

### Mengapa Anda harus membuat kompresi video Anda sendiri. Tidak ada yang tersedia pada saat itu?

Pada saat saya mulai membangun "nv", satu-satunya sistem yang saya tahu yang melakukan
konferensi video adalah perangkat keras khusus yang sangat mahal. Misalnya,
Steve Casner memiliki akses ke sistem dari BBN yang disebut "DVC" (dan
kemudian dikomersialisasikan sebagai "PictureWindow"). Kompresi memerlukan
perangkat keras khusus, tetapi dekompresi dapat dilakukan dalam perangkat lunak.
Apa yang membuat "nv" agak unik adalah bahwa baik kompresi dan dekompresi
dilakukan dalam perangkat lunak, dengan satu-satunya persyaratan perangkat keras adalah
sesuatu untuk mendigitalkan sinyal video analog yang masuk.

Banyak konsep dasar tentang cara mengompresi video ada pada saat itu, dengan
hal-hal seperti standar MPEG-1 muncul tepat pada waktu yang sama dengan "nv",
tetapi pengkodean _real-time_ dengan MPEG-1 jelas TIDAK mungkin pada
saat itu. Perubahan yang saya buat adalah semua tentang mengambil konsep dasar itu dan
memperkirakan mereka dengan algoritma yang jauh lebih murah, di mana saya menghindari hal-hal seperti
transformasi kosinus dan _floating point_, dan bahkan menghindari perkalian integer
karena itu sangat lambat pada SPARC-station. Saya mencoba melakukan semua yang saya bisa
dengan hanya penambahan/pengurangan dan _masking_ dan _shifting_ bit, dan itu mendapatkan
kembali cukup kecepatan untuk masih terasa agak seperti video.

Dalam satu atau dua tahun setelah rilis "nv", ada banyak alat audio
dan video yang berbeda untuk dipilih, tidak hanya di MBONE tetapi di tempat lain
seperti alat CU-SeeMe yang dibangun di Mac. Jadi, itu jelas merupakan ide yang
waktunya telah tiba. Saya sebenarnya akhirnya membuat "nv" interoperasi dengan banyak
alat ini, dan dalam beberapa kasus alat lain mengambil _codec_ "nv" saya, jadi
mereka dapat berinteroperasi ketika menggunakan skema kompresi saya.

## WebRTC
WebRTC memerlukan upaya standardisasi yang mengerdilkan semua upaya lain
yang dijelaskan dalam bab ini. Ini memerlukan kerja sama di dua
badan standar yang berbeda (IETF dan W3C) dan ratusan individu di banyak
perusahaan dan negara. Untuk memberi kami pandangan ke dalam motivasi dan
upaya monumental yang diperlukan untuk membuat WebRTC terjadi kami memiliki
[Serge Lachapelle](https://twitter.com/slac).

Serge adalah _product manager_ di Google, saat ini melayani sebagai _product manager_
untuk Google Workspace. Ini adalah ringkasan saya dari wawancara.

### Apa yang membawa Anda untuk bekerja pada WebRTC?
Saya telah bersemangat tentang membangun perangkat lunak komunikasi sejak saya di
perguruan tinggi. Pada tahun 90-an teknologi seperti [nv](https://github.com/ronf/nv)
mulai muncul, tetapi sulit digunakan. Saya membuat proyek yang memungkinkan
Anda untuk bergabung dengan panggilan video langsung dari peramban Anda. Saya juga mem-_port_-nya ke Windows.

Saya membawa pengalaman ini ke Marratech, sebuah perusahaan yang saya ikut dirikan. Kami membuat
perangkat lunak untuk konferensi video grup. Secara teknologi lanskap
sangat berbeda. Ujung tombak dalam video didasarkan pada jaringan _multicast_.
Pengguna dapat bergantung pada jaringan untuk mengirimkan paket video ke semua orang dalam
panggilan. Ini berarti bahwa kami memiliki _server_ yang sangat sederhana. Ini memiliki kelemahan besar
meskipun, jaringan harus dirancang untuk mengakomodasi itu. Industri bergerak menjauh
dari _multicast_ ke _packet shuffler_, lebih umum dikenal sebagai SFU.

Marratech diakuisisi oleh Google pada 2007. Saya kemudian akan bekerja pada
proyek yang akan menginformasikan WebRTC.

### Proyek Google pertama
Proyek pertama yang dikerjakan oleh tim WebRTC masa depan adalah _chat_ suara dan
video Gmail. Mendapatkan audio dan video ke dalam peramban bukanlah tugas yang mudah. Ini
memerlukan komponen khusus yang harus kami lisensikan dari perusahaan yang berbeda.
Audio dilisensikan dari GIPs, video dilisensikan untuk Vidyo dan jaringan
adalah libjingle. Keajaibannya kemudian membuat semuanya bekerja bersama.

Setiap subsistem memiliki API yang sangat berbeda, dan mengasumsikan Anda memecahkan
masalah yang berbeda. Untuk membuat semuanya bekerja bersama Anda memerlukan pengetahuan kerja
tentang jaringan, kriptografi, media dan banyak lagi.
[Justin Uberti](https://juberti.com) adalah orang yang mengambil pekerjaan ini.
Dia membawa komponen-komponen ini bersama untuk membuat produk yang dapat digunakan.

Rendering _real-time_ di peramban juga sangat sulit. Kami harus menggunakan
NPAPI (_Netscape Plugin API_) dan melakukan banyak hal cerdas untuk membuatnya bekerja.
Pelajaran yang kami pelajari dari proyek ini sangat mempengaruhi WebRTC.

### Chrome
Pada saat yang sama proyek Chrome dimulai di dalam Google. Ada
begitu banyak kegembiraan, dan proyek ini memiliki tujuan besar. Ada pembicaraan tentang
WebGL, Offline, kemampuan _Database_, input latensi rendah untuk permainan hanya
untuk beberapa nama.

Bergerak menjauh dari NPAPI menjadi fokus besar. Ini adalah API yang kuat, tetapi datang dengan
konsekuensi keamanan yang besar. Chrome menggunakan desain _sandbox_ untuk menjaga pengguna tetap aman.
Operasi yang berpotensi tidak aman dijalankan dalam proses yang berbeda.
Bahkan jika sesuatu yang salah terjadi, penyerang masih tidak memiliki akses ke
data pengguna.

### WebRTC lahir
Bagi saya WebRTC lahir dengan beberapa motivasi. Digabungkan mereka melahirkan
upaya.

Seharusnya tidak sesulit ini untuk membangun pengalaman RTC. Begitu banyak upaya terbuang
mengimplementasikan ulang hal yang sama oleh _developer_ yang berbeda. Kami harus menyelesaikan masalah integrasi yang membuat frustrasi ini sekali, dan fokus pada hal-hal lain.

Komunikasi manusia harus tidak terhalangi dan harus terbuka. Bagaimana oke untuk
teks dan HTML menjadi terbuka, tetapi suara saya dan gambar saya secara _real-time_ tidak?

Keamanan adalah prioritas. Menggunakan NPAPI bukan yang terbaik untuk pengguna. Ini juga
adalah kesempatan untuk membuat protokol yang aman secara default.

Untuk membuat WebRTC terjadi Google mengakuisisi dan Open Source komponen yang telah kami
gunakan sebelumnya. [On2](https://en.wikipedia.org/wiki/On2_Technologies) diakuisisi untuk teknologi videonya dan
[Global IP Solutions](https://en.wikipedia.org/wiki/Global_IP_Solutions)
untuk teknologi RTC-nya. Saya bertanggung jawab atas upaya mengakuisisi GIPS.
Kami bekerja menggabungkan ini dan membuatnya mudah digunakan di dalam dan di luar
peramban.

### Standardisasi
Standardisasi WebRTC adalah sesuatu yang benar-benar kami ingin lakukan, tetapi bukan sesuatu yang
pernah saya lakukan sebelumnya maupun siapa pun di tim langsung kami. Untuk ini kami benar-benar
beruntung memiliki Harald Alvestrand di Google. Dia telah melakukan pekerjaan ekstensif di
IETF sudah dan memulai proses standardisasi WebRTC.

Pada musim panas 2010 makan siang informal dijadwalkan di Maastricht. _Developer_ dari
banyak perusahaan datang bersama untuk mendiskusikan apa yang seharusnya WebRTC. Makan siang memiliki
_engineer_ dari Google, Cisco, Ericsson, Skype, Mozilla, Linden Labs dan lainnya.
Anda dapat menemukan kehadiran penuh dan slide presenter di
[rtc-web.alvestrand.com](http://rtc-web.alvestrand.com).

Skype juga memberikan beberapa panduan hebat karena pekerjaan yang mereka lakukan dengan
Opus di IETF.

### Berdiri di bahu raksasa
Ketika bekerja di IETF Anda memperluas pekerjaan yang telah datang sebelum Anda.
Dengan WebRTC kami beruntung bahwa begitu banyak hal ada. Kami tidak harus mengambil
setiap masalah karena mereka sudah terpecahkan. Jika Anda tidak suka
teknologi yang sudah ada sebelumnya, itu bisa membuat frustrasi. Harus ada alasan yang cukup
besar untuk mengabaikan pekerjaan yang ada, jadi membuat sendiri bukan pilihan.

Kami juga secara sadar tidak mencoba untuk standarisasi ulang hal-hal seperti _signaling_.
Ini sudah diselesaikan dengan SIP dan upaya non-IETF lainnya, dan
terasa seperti bisa berakhir sangat politik. Pada akhirnya itu hanya tidak
terasa seperti ada banyak nilai untuk ditambahkan ke ruang.

Saya tidak tetap terlibat dalam standardisasi seperti Justin dan Harald, tetapi saya
menikmati waktu saya melakukannya. Saya lebih bersemangat tentang kembali membangun
hal-hal untuk pengguna.

### Masa depan
WebRTC berada di tempat yang bagus hari ini. Ada banyak perubahan berulang
terjadi, tetapi tidak ada yang khususnya yang telah saya kerjakan.

Saya paling bersemangat tentang apa yang dapat dilakukan _cloud computing_ untuk komunikasi. Menggunakan
algoritma canggih kami dapat menghapus kebisingan latar belakang dari panggilan dan membuat
komunikasi mungkin di mana tidak mungkin sebelumnya. Kami juga melihat WebRTC
memperluas jauh melampaui komunikasi… Siapa yang tahu bahwa itu akan menggerakkan _gaming_ berbasis _cloud_ 9 tahun kemudian? Semua ini tidak akan mungkin tanpa
fondasi WebRTC.
