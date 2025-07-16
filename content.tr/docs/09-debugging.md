---
title: Hata Ayıklama
type: docs
weight: 10
---

# Hata Ayıklama

WebRTC hata ayıklama göz korkutucu bir görev olabilir. Çok sayıda hareketli parça vardır ve hepsi bağımsız olarak bozulabilir. Dikkatli olmazsanız, yanlış şeylere bakarak haftalar kaybedebilirsiniz. Sonunda bozuk olan kısmı bulduğunuzda, nedenini anlamak için biraz öğrenmeniz gerekecek.

Bu bölüm sizi WebRTC hata ayıklama zihniyetine sokacaktır. Size problemi nasıl parçalara ayıracağınızı gösterecektir. Problemi öğrendikten sonra, popüler hata ayıklama araçlarının hızlı bir turunu vereceğiz.

## Problemi İzole Edin

Hata ayıklama yaparken, sorunun nereden geldiğini izole etmeniz gerekir. Başlangıçtan başlayın...

### Sinyalleşme Hatası

### Ağ Hatası

STUN sunucunuzu netcat kullanarak test edin:

1. **20-byte** bağlama istek paketini hazırlayın:

   ```
   echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | hexdump -C
   00000000  00 01 00 00 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
   00000010  54 45 53 54                                       |TEST|
   00000014
   ```

   Yorumlama:

   - `00 01` mesaj türüdür.
   - `00 00` veri bölümünün uzunluğudur.
   - `21 12 a4 42` sihirli çerezdır.
   - ve `54 45 53 54 54 45 53 54 54 45 53 54` (ASCII'ye dekod edildiğinde: `TESTTESTTEST`) 12-byte işlem ID'sidir.

2. İsteği gönderin ve **32 byte** yanıtı bekleyin:

   ```
   stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x21\x12\xA4\x42TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
   00000000  01 01 00 0c 21 12 a4 42  54 45 53 54 54 45 53 54  |....!..BTESTTEST|
   00000010  54 45 53 54 00 20 00 08  00 01 6f 32 7f 36 de 89  |TEST. ....o2.6..|
   00000020
   ```

   Yorumlama:

   - `01 01` mesaj türüdür
   - `00 0c` veri bölümünün uzunluğudur (ondalık olarak 12'ye dekod edilir)
   - `21 12 a4 42` sihirli çerezdır
   - ve `54 45 53 54 54 45 53 54 54 45 53 54` (ASCII'ye dekod edildiğinde: `TESTTESTTEST`) 12-byte işlem ID'sidir.
   - `00 20 00 08 00 01 6f 32 7f 36 de 89` 12-byte veridir, yorumlama:
     - `00 20` tür: `XOR-MAPPED-ADDRESS`
     - `00 08` değer bölümünün uzunluğudur (ondalık olarak 8'e dekod edilir)
     - `00 01 6f 32 7f 36 de 89` veri değeridir, yorumlama:
       - `00 01` adres türüdür (IPv4)
       - `6f 32` XOR-eşlenen porttur
       - `7f 36 de 89` XOR-eşlenen IP adresidir

XOR-eşlenen bölümü dekod etmek zahmetlidir, ancak `00 00 00 00`'a ayarlanmış (geçersiz) sahte sihirli çerez sağlayarak stun sunucusunu sahte XOR-eşleme gerçekleştirmesi için kandırabiliriz:

```
stunserver=stun1.l.google.com;stunport=19302;listenport=20000;echo -ne "\x00\x01\x00\x00\x00\x00\x00\x00TESTTESTTEST" | nc -u -p $listenport $stunserver $stunport -w 1 | hexdump -C
00000000  01 01 00 0c 00 00 00 00  54 45 53 54 54 45 53 54  |........TESTTEST|
00000010  54 45 53 54 00 01 00 08  00 01 4e 20 5e 24 7a cb  |TEST......N ^$z.|
00000020
```

Sahte sihirli çereze karşı XOR yapmak idempotanttır, bu yüzden port ve adres yanıtta açık olacaktır. Bu tüm durumlarda çalışmayacaktır, çünkü bazı router'lar geçen paketleri manipüle eder, IP adresinde hile yapar. Döndürülen veri değerine (son sekiz byte) bakarsak:

- `00 01 4e 20 5e 24 7a cb` veri değeridir, yorumlama:
  - `00 01` adres türüdür (IPv4)
  - `4e 20` eşlenen porttur (ondalık olarak 20000'e dekod edilir)
  - `5e 24 7a cb` IP adresidir (noktalı ondalık notasyonda `94.36.122.203`'e dekod edilir).

### Güvenlik Hatası

### Medya Hatası

### Veri Hatası

## Mesleğin Araçları

### netcat (nc)

[netcat](https://en.wikipedia.org/wiki/Netcat), TCP veya UDP kullanan ağ bağlantılarından okuma ve yazma için komut satırı ağ yardımcı programıdır. Genellikle `nc` komutu olarak mevcuttur.

### tcpdump

[tcpdump](https://en.wikipedia.org/wiki/Tcpdump) komut satırı veri ağı paket analizörüdür.

Yaygın komutlar:

- Port 19302'ye gelen ve giden UDP paketlerini yakalayın, paket içeriğinin hexdump'ını yazdırın:

  `sudo tcpdump 'udp port 19302' -xx`

- Aynısı, ancak paketleri daha sonra inceleme için PCAP (paket yakalama) dosyasına kaydedin:

  `sudo tcpdump 'udp port 19302' -w stun.pcap`

  PCAP dosyası Wireshark uygulamasıyla açılabilir: `wireshark stun.pcap`

### Wireshark

[Wireshark](https://www.wireshark.org) yaygın olarak kullanılan ağ protokol analizörüdür.

### WebRTC tarayıcı araçları

Tarayıcılar kurduğunuz bağlantıları incelemek için kullanabileceğiniz yerleşik araçlarla gelir. Chrome'da [`chrome://webrtc-internals`](chrome://webrtc-internals) ve [`chrome://webrtc-logs`](chrome://webrtc-logs) vardır. Firefox'ta [`about:webrtc`](about:webrtc) vardır.

## Gecikme

Yüksek gecikmeniz olduğunu nasıl bilirsiniz? Videonuzun gecikmeli olduğunu fark etmiş olabilirsiniz, ancak tam olarak ne kadar geciktiğini biliyor musunuz?
Bu gecikmeyi azaltabilmek için önce onu ölçerek başlamanız gerekir.

Gerçek gecikme uçtan uca ölçülmesi beklenir. Bu, sadece gönderen ve alıcı arasındaki ağ yolunun gecikmesi değil, kamera yakalama, çerçeve kodlama, iletim, alma, dekodlama ve görüntüleme ile bu adımlardan herhangi biri arasında olası kuyruklama gecikmesinin birleşik gecikmesi anlamına gelir.

Uçtan uca gecikme, her bileşenin gecikmelerinin basit toplamı değildir.

Teorik olarak canlı video iletim hattının bileşenlerinin gecikmesini ayrı ayrı ölçüp sonra bunları toplayabilseniz de, pratikte en azından bazı bileşenler ya enstrümantasyon için erişilemez olacak ya da hat dışında ölçüldüğünde önemli ölçüde farklı sonuçlar üretecektir.
Hat aşamaları arasındaki değişken kuyruk derinlikleri, ağ topolojisi ve kamera pozlama değişiklikleri uçtan uca gecikmeyi etkileyen bileşenlerin sadece birkaç örneğidir.

Canlı yayın sisteminizde her bileşenin içsel gecikmesi değişebilir ve aşağı akış bileşenlerini etkileyebilir.
Yakalanan videonun içeriği bile gecikmeyi etkiler.
Örneğin, ağaç dalları gibi yüksek frekans özellikler için, açık mavi gökyüzü gibi düşük frekanslıya kıyasla çok daha fazla bit gerekir.
Otomatik pozlama açık olan kamera, yakalama hızı saniyede 30 kareye ayarlanmış olsa bile bir kareyi yakalamak için beklenen 33 milisaniyeden _çok_ daha uzun sürebilir.
Ağ üzerinden iletim, özellikle hücresel, değişen talep nedeniyle çok dinamiktir.
Daha fazla kullanıcı havada daha fazla konuşma getirir.
Fiziksel konumunuz (kötü şöhretli düşük sinyal bölgeleri) ve diğer birçok faktör paket kaybını ve gecikmeyi artırır.
Teslimat için bir ağ arayüzüne, diyelim WiFi adaptörü veya LTE modeme paket gönderdiğinizde ne olur?
Hemen teslim edilemezse arayüzde kuyruğa alınır, kuyruk ne kadar büyükse böyle ağ arayüzü o kadar gecikme getirir.

### Manuel uçtan uca gecikme ölçümü

Uçtan uca gecikmeden bahsettiğimizde, bir olayın gerçekleşmesi ile gözlemlenmesi arasındaki zamanı kastediyoruz, yani video karelerinin ekranda görünmesi.

```
UctanUcaGecikme = T(gözlemle) - T(gerçekleş)
```

Naif yaklaşım, bir olayın gerçekleştiği zamanı kaydetmek ve bunu gözlem zamanından çıkarmaktır.
Ancak, hassasiyet milisaniyelere düştüğünde zaman senkronizasyonu sorun haline gelir.
Dağıtık sistemlerde saatleri senkronize etmeye çalışmak çoğunlukla boşunadır, zaman senkronizasyonundaki küçük bir hata bile güvenilmez gecikme ölçümü üretir.

Saat senkronizasyon sorunları için basit bir geçici çözüm aynı saati kullanmaktır.
Gönderen ve alıcıyı aynı referans çerçevesine koyun.

Milisaniyelik tikan bir saatiniz veya gerçekten başka herhangi bir olay kaynağınız olduğunu hayal edin.
Saati kameraya doğrultarak uzak ekrana canlı yayın yapan sistemde gecikmeyi ölçmek istiyorsunuz.
Milisaniye zamanlayıcısının tiklemesi (T<sub>`gerçekleş`</sub>) ile saatin video karelerinin ekranda görünmesi (T<sub>`gözlemle`</sub>) arasındaki zamanı ölçmenin açık yolu şudur:

- Kameranızı milisaniyelik saate doğrultun.
- Video karelerini aynı fiziksel konumda olan alıcıya gönderin.
- Milisaniyelik zamanlayıcının ve ekranda alınan videonun fotoğrafını çekin (telefonunuzu kullanın).
- İki zamanı çıkarın.

Bu en gerçek uçtan uca gecikme ölçümüdür.
Tüm bileşen gecikmelerini (kamera, kodlayıcı, ağ, dekoder) hesaba katar ve herhangi bir saat senkronizasyonuna dayanmaz.

![DIY Latency](../images/09-diy-latency.png "DIY Latency Measurement").
![DIY Latency Example](../images/09-diy-latency-happen-observe.png "DIY Latency Measurement Example")

Yukarıdaki fotoğrafta ölçülen uçtan uca gecikme 101 msn'dir. Şu anda gerçekleşen olay 10:16:02.862, ancak canlı yayın sistemi gözlemcisi 10:16:02.761'i görüyor.

### Otomatik uçtan uca gecikme ölçümü

Bu yazının yazıldığı tarih itibariyle (Mayıs 2021) uçtan uca gecikme için WebRTC standardı aktif olarak [tartışılmaktadır](https://github.com/w3c/webrtc-stats/issues/537).
Firefox, kullanıcıların standart WebRTC API'lerinin üstünde otomatik gecikme ölçümü oluşturmalarına izin veren bir dizi API uyguladı.
Ancak bu paragrafta, gecikmeyi otomatik olarak ölçmenin en uyumlu yolunu tartışıyoruz.

![NTP Style Latency Measurement](../images/09-ntp-latency.png "NTP Style Latency Measurement")

Gidiş-dönüş süresi özetle: Size zamanımı `tR1` gönderiyorum, `tR1`'imi `tR2` zamanında geri aldığımda, gidiş-dönüş süresinin `tR2 - tR1` olduğunu biliyorum.

Gönderen ve alıcı arasında bir iletişim kanalı verildiğinde (örneğin [DataChannel](https://webrtc.org/getting-started/data-channels)), alıcı aşağıdaki adımları izleyerek gönderenin monotonik saatini modelleyebilir:

1. `tR1` zamanında, alıcı yerel monotonik saat zaman damgası ile bir mesaj gönderir.
2. Yerel zaman `tS1` ile gönderene ulaştığında, gönderen `tR1`'in kopyası ile birlikte gönderenin `tS1`'i ve gönderenin video track zamanı `tSV1`'i ile yanıt verir.
3. Alıcı tarafta `tR2` zamanında, gidiş-dönüş süresi mesajın gönderme ve alma zamanları çıkarılarak hesaplanır: `RTT = tR2 - tR1`.
4. Gidiş-dönüş süresi `RTT` ile gönderen yerel zaman damgası `tS1` birlikte gönderenin monotonik saatinin tahmini oluşturmak için yeterlidir. `tR2` zamanında gönderendeki mevcut zaman `tS1` artı gidiş-dönüş süresinin yarısına eşit olur.
5. Gönderenin yerel saat zaman damgası `tS1`'in video track zaman damgası `tSV1` ile eşleştirilmesi ve gidiş-dönüş süresi `RTT` ile birlikte alıcı video track zamanını gönderen video track'e senkronize etmek için yeterlidir.

Şimdi son bilinen gönderen video karesi zamanından `tSV1`'den ne kadar zaman geçtiğini bildiğimize göre, şu anda görüntülenen video karesinin zamanını (`actual_video_time`) beklenen zamandan çıkararak gecikmeyi yaklaşık olarak hesaplayabiliriz:

```
expected_video_time = tSV1 + time_since(tSV1)
latency = expected_video_time - actual_video_time
```

Bu yöntemin dezavantajı kameranın içsel gecikmesini içermemesidir.
Çoğu video sistemi kare yakalama zaman damgasını kameradan kareyi ana belleğe teslim etme zamanı olarak kabul eder, bu kayıt edilen olayın gerçekten gerçekleşmesinden birkaç an sonra olacaktır.

#### Örnek gecikme tahmini

Örnek uygulama alıcıda bir `latency` veri kanalı açar ve periyodik olarak alıcının monotonik zamanlayıcı zaman damgalarını gönderene gönderir. Gönderen JSON mesajı ile geri yanıt verir ve alıcı mesaja dayalı gecikmeyi hesaplar.

```json
{
  "received_time": 64714, // Alıcı tarafından gönderilen zaman damgası, gönderen zaman damgasını yansıtır.
  "delay_since_received": 46, // Gönderici üzerinde son `received_time` alındığından beri geçen zaman.
  "local_clock": 1597366470336, // Gönderenin mevcut monotonik saat zamanı.
  "track_times_msec": {
    "myvideo_track1": [
      13100, // Video karesi RTP zaman damgası (milisaniye cinsinden).
      1597366470289 // Video karesi monotonik saat zaman damgası.
    ]
  }
}
```

Alıcıda veri kanalını açın:

```javascript
dataChannel = peerConnection.createDataChannel("latency");
```

Alıcının zamanını `tR1` periyodik olarak gönderin. Bu örnek özel bir nedeni olmadan 2 saniye kullanır:

```javascript
setInterval(() => {
  let tR1 = Math.trunc(performance.now());
  dataChannel.send("" + tR1);
}, 2000);
```

Gönderici üzerinde alıcıdan gelen mesajı işleyin:

```javascript
// event.data'nın "1234567" gibi bir string olduğunu varsayarak.
tR1 = event.data;
now = Math.trunc(performance.now());
tSV1 = 42000; // Mevcut kare RTP zaman damgası milisaniye zaman ölçeğine dönüştürülmüş.
tS1 = 1597366470289; // Mevcut kare monotonik saat zaman damgası.
msg = {
  received_time: tR1,
  delay_since_received: 0,
  local_clock: now,
  track_times_msec: {
    myvideo_track1: [tSV1, tS1],
  },
};
dataChannel.send(JSON.stringify(msg));
```

Gönderenden gelen mesajı işleyin ve tahmini gecikmeyi `console`'a yazdırın:

```javascript
let tR2 = performance.now();
let fromSender = JSON.parse(event.data);
let tR1 = fromSender["received_time"];
let delay = fromSender["delay_since_received"]; // Gönderenin alma ve yanıt gönderme arasında geçen zaman.
let senderTimeFromResponse = fromSender["local_clock"];
let rtt = tR2 - delay - tR1;
let networkLatency = rtt / 2;
let senderTime = senderTimeFromResponse + delay + networkLatency;
VIDEO.requestVideoFrameCallback((now, framemeta) => {
  // Gönderenin mevcut zamanını tahmin edin.
  let delaySinceVideoCallbackRequested = now - tR2;
  senderTime += delaySinceVideoCallbackRequested;
  let [tSV1, tS1] = Object.entries(fromSender["track_times_msec"])[0][1];
  let timeSinceLastKnownFrame = senderTime - tS1;
  let expectedVideoTimeMsec = tSV1 + timeSinceLastKnownFrame;
  let actualVideoTimeMsec = Math.trunc(framemeta.rtpTimestamp / 90); // RTP timebase'ini (90000) milisaniye timebase'ine dönüştür.
  let latency = expectedVideoTimeMsec - actualVideoTimeMsec;
  console.log("latency", latency, "msec");
});
```

#### Tarayıcıda gerçek video zamanı

> `<video>.requestVideoFrameCallback()` web yazarlarının kompozisyon için bir kare sunulduğunda bilgilendirilmelerine izin verir.

Çok yakın zamana kadar (Mayıs 2020), tarayıcılarda şu anda görüntülenen video karesinin zaman damgasını güvenilir şekilde almak neredeyse imkansızdı. `video.currentTime` tabanlı geçici çözüm yöntemleri vardı, ancak özellikle hassas değildi.
Hem Chrome hem de Mozilla tarayıcı geliştiricileri mevcut video kare zamanına erişim için API callback'i ekleyen yeni W3C standardı [`HTMLVideoElement.requestVideoFrameCallback()`](https://wicg.github.io/video-rvfc/)'nin tanıtımını [desteklediler](https://github.com/mozilla/standards-positions/issues/250).
Ekleme basit gelir, ancak web üzerinde ses ve video senkronizasyonu gerektiren birden fazla gelişmiş medya uygulamasını etkinleştirmiştir.
Özellikle WebRTC için callback, mevcut video karesi ile ilişkili RTP zaman damgası olan `rtpTimestamp` alanını içerecektir.
Bu WebRTC uygulamaları için mevcut olmalı, aksi takdirde mevcut olmamalıdır.

### Gecikme Hata Ayıklama İpuçları

Hata ayıklama muhtemelen ölçülen gecikmeyi etkileyeceği için, genel kural kurulumunuzu sorunu hala yeniden üretebilecek en küçük olasılığa basitleştirmektir.
Ne kadar çok bileşeni kaldırabilirseniz, hangi bileşenin gecikme problemine neden olduğunu anlamak o kadar kolay olacaktır.

#### Kamera gecikmesi

Kamera ayarlarına bağlı olarak kamera gecikmesi değişebilir.
Otomatik pozlama, otomatik odaklama ve otomatik beyaz denge ayarlarını kontrol edin.
Web kameralarının tüm "otomatik" özellikleri, yakalanan görüntüyü WebRTC yığınına kullanılabilir hale getirmeden önce analiz etmek için ekstra zaman alır.

Linux'taysanız, kamera ayarlarını kontrol etmek için `v4l2-ctl` komut satırı aracını kullanabilirsiniz:

```bash
# Otomatik odaklamayı devre dışı bırakın:
v4l2-ctl -d /dev/video0 -c focus_auto=0
# Odağı sonsuzluğa ayarlayın:
v4l2-ctl -d /dev/video0 -c focus_absolute=0
```

Kamera ayarlarını hızla kontrol etmek ve ayarlamak için `guvcview` grafik UI aracını da kullanabilirsiniz.

#### Kodlayıcı gecikmesi

Çoğu modern kodlayıcı kodlanmış bir tane çıkarmadan önce bazı kareleri tamponlayacaktır.
Öncelikleri üretilen resmin kalitesi ve bitrate arasında bir denge kurmaktır.
Çok geçişli kodlama, kodlayıcının çıkış gecikmesini umursamamasının aşırı örneğidir.
İlk geçiş sırasında kodlayıcı tüm videoyu alır ve ancak ondan sonra kareleri çıkarmaya başlar.

Ancak, uygun ayarlama ile insanlar alt-kare gecikmelerine ulaştılar.
Kodlayıcınızın aşırı referans kareleri kullanmadığından veya B-karelerine dayanmadığından emin olun.
Her codec'in gecikme ayarlama ayarları farklıdır, ancak x264 için en düşük kare çıkış gecikmesi için `tune=zerolatency` ve `profile=baseline` kullanmanızı öneririz.

#### Ağ gecikmesi

Ağ gecikmesi, daha iyi ağ bağlantısına yükseltmek dışında tartışmalı olarak en az yapabileceğiniz şeydir.
Ağ gecikmesi hava durumu gibidir - yağmuru durduramazsınız, ancak hava durumunu kontrol edip şemsiye alabilirsiniz.
WebRTC ağ koşullarını milisaniye hassasiyetle ölçer.
Önemli metrikler:

- Gidiş-dönüş süresi.
- Paket kaybı ve paket yeniden iletimleri.

**Gidiş-Dönüş Süresi**

WebRTC yığınının yerleşik ağ gidiş dönüş süresi (RTT) ölçüm [mekanizması](https://www.w3.org/TR/webrtc-stats/#dom-rtcremoteinboundrtpstreamstats-roundtriptime) vardır.
Gecikmenin yeterince iyi yaklaşımı RTT'nin yarısıdır. Paket gönderme ve alma süresinin aynı olduğunu varsayar, ki bu her zaman böyle değildir.
RTT uçtan uca gecikmenin alt sınırını belirler.
Video kareleriniz kamera-kodlayıcı hattınız ne kadar optimize olursa olsun alıcıya `RTT/2`'den daha hızlı ulaşamaz.

Yerleşik RTT mekanizması gönderen/alıcı raporları adlı özel RTCP paketlerine dayanır.
Gönderen zaman okumasını alıcıya gönderir, alıcı aynı zaman damgasını gönderene yansıtır.
Böylece gönderen paketin alıcıya gidip geri dönmesi için ne kadar zaman aldığını bilir.
RTT ölçümünün daha fazla detayı için [Sender/Receiver Reports](../06-media-communication/#senderreceiver-reports) bölümüne bakın.

**Paket kaybı ve paket yeniden iletimleri**

Hem RTP hem de RTCP, sıralama, başarılı teslimat veya tekrarlama garantisi olmayan UDP tabanlı protokollerdir.
Yukarıdakilerin hepsi gerçek dünya WebRTC uygulamalarında olabilir ve olur.
Sofistike olmayan dekoder uygulaması dekoderin görüntüyü başarıyla yeniden birleştirebilmesi için bir karenin tüm paketlerinin teslim edilmesini bekler.
Paket kaybı varlığında [P-frame](../06-media-communication/#inter-frame-types) paketleri kaybolursa dekodlama artefaktları görünebilir.
I-frame paketleri kaybolursa tüm bağımlı kareler ya ağır artefaktlar alacak ya da hiç dekod edilmeyeceklerdir.
Büyük olasılıkla bu videonun bir an için "donmasına" neden olacaktır.

Video donmasını veya dekodlama artefaktlarını önlemek için (en azından önlemeye çalışmak için), WebRTC olumsuz onay mesajları ([NACK](../06-media-communication/#negative-acknowledgment)) kullanır.
Alıcı beklenen RTP paketini almadığında, gönderene eksik paketi tekrar göndermesini söylemek için NACK mesajı döndürür.
Alıcı paketin yeniden iletimini _bekler_.
Bu tür yeniden iletimler artan gecikmeye neden olur.
Gönderilen ve alınan NACK paketlerinin sayısı WebRTC'nin yerleşik istatistik alanlarında [outbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcoutboundrtpstreamstats-nackcount) ve [inbound stream nackCount](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-nackcount) kaydedilir.

[webrtc internals sayfasında](#webrtc-browser-tools) gelen ve giden `nackCount`'un güzel grafiklerini görebilirsiniz.
`nackCount`'un arttığını görüyorsanız, ağın yüksek paket kaybı yaşadığı ve WebRTC yığının buna rağmen düzgün video/ses deneyimi oluşturmak için elinden geleni yaptığı anlamına gelir.

Paket kaybı o kadar yüksek ki dekoder görüntü üretemiyor veya tamamen kayıp I-frame durumunda olduğu gibi sonraki bağımlı görüntüleri üretemiyor, gelecekteki tüm P-frameler dekod edilmeyecek.
Alıcı özel Picture Loss Indication mesajı ([PLI](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)) göndererek bunu hafifletmeye çalışacaktır.
Gönderen `PLI` aldığında, alıcının dekoderine yardımcı olmak için yeni I-frame üretecektir.
I-frameler normalde P-framelerden boyut olarak daha büyüktür. Bu iletilmesi gereken paket sayısını artırır.
NACK mesajları gibi, alıcının yeni I-frame'i beklemesi gerekecek, ek gecikme getirecektir.

[webrtc internals sayfasında](#webrtc-browser-tools) `pliCount`'u izleyin. Artıyorsa, kodlayıcınızı daha az paket üretecek şekilde ayarlayın veya daha hata dirençli modu etkinleştirin.

#### Alıcı tarafı gecikmesi

Gecikme, sıra dışı gelen paketlerden etkilenecektir.
Görüntü paketinin alt yarısı üstten önce gelirse dekodlamadan önce üstü beklemeniz gerekir.
Bu [Solving Jitter](../05-real-time-networking/#solving-jitter) bölümünde büyük detayda açıklanmıştır.

Bir karenin dekodere serbest bırakılmadan önce tüm paketlerini beklerken alma tamponunda ne kadar süre tutulduğunu görmek için yerleşik [jitterBufferDelay](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) metriğine de başvurabilirsiniz.
