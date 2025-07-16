---
title: Gerçek Zamanlı Ağ İletişimi
type: docs
weight: 6
---

# Gerçek Zamanlı Ağ İletişimi

## Gerçek zamanlı iletişimde ağ iletişimi neden bu kadar önemli?

Ağlar gerçek zamanlı iletişimde sınırlayıcı faktördür. İdeal bir dünyada sınırsız bant genişliğine sahip olurduk ve paketler anında ulaşırdı. Ancak durum böyle değil. Ağlar sınırlıdır ve koşullar her an değişebilir. Ağ koşullarını ölçmek ve gözlemlemek de zor bir problemdir. Donanım, yazılım ve bunların konfigürasyonuna bağlı olarak farklı davranışlar alabilirsiniz.

Gerçek zamanlı iletişim ayrıca diğer çoğu alanda bulunmayan bir problem yaratır. Bir web geliştirici için web sitenizin bazı ağlarda daha yavaş olması ölümcül değildir. Tüm veriler ulaştığı sürece kullanıcılar mutludur. WebRTC ile verileriniz geç gelirse işe yaramaz. Kimse 5 saniye önce bir konferans görüşmesinde söylenenleri umursamaz. Dolayısıyla gerçek zamanlı iletişim sistemi geliştirirken bir ödünleşim yapmanız gerekir. Zaman sınırım nedir ve ne kadar veri gönderebilirim?

Bu bölüm hem veri hem de medya iletişimi için geçerli olan kavramları kapsar. Sonraki bölümlerde teorinin ötesine geçip WebRTC'nin medya ve veri alt sistemlerinin bu problemleri nasıl çözdüğünü tartışıyoruz.

## Ağın zorlaştıran öznitelikleri nelerdir?

Tüm ağlarda etkili çalışan kod karmaşıktır. Birçok farklı faktörünüz var ve hepsi birbirini incelikle etkileyebilir. Geliştiricilerin karşılaşacağı en yaygın sorunlar bunlardır.

#### Bant Genişliği

Bant genişliği, belirli bir yol boyunca aktarılabilecek maksimum veri hızıdır. Bunun da statik bir sayı olmadığını hatırlamak önemlidir. Daha fazla (veya daha az) kişi kullandıkça rota boyunca bant genişliği değişecektir.

#### İletim Süresi ve Gidiş-Geliş Süresi

İletim Süresi, bir paketin hedefine ulaşması için geçen süredir. Bant Genişliği gibi bu da sabit değildir. İletim Süresi her an dalgalanabilir.

`transmission_time = receive_time - send_time`

İletim süresini hesaplamak için gönderen ve alıcıda milisaniye hassasiyetinde senkronize saatlere ihtiyacınız vardır.
Küçük bir sapma bile güvenilmez iletim süresi ölçümü üretir.
WebRTC son derece heterojen ortamlarda çalıştığından, hostlar arasında mükemmel zaman senkronizasyonuna güvenmek neredeyse imkansızdır.

Gidiş-geliş süresi ölçümü, kusurlu saat senkronizasyonu için bir geçici çözümdür.

Dağıtılmış saatler üzerinde çalışmak yerine bir WebRTC eşi kendi zaman damgası `sendertime1` ile özel bir paket gönderir.
İşbirlikçi bir eş paketi alır ve zaman damgasını gönderene geri yansıtır.
Orijinal gönderen yansıtılan zamanı aldığında `sendertime1` zaman damgasını mevcut zaman `sendertime2`'den çıkarır.
Bu zaman deltası "gidiş-geliş yayılım gecikmesi" veya daha yaygın olarak gidiş-geliş süresi olarak adlandırılır.

`rtt = sendertime2 - sendertime1`

Gidiş-geliş süresinin yarısı, iletim süresinin yeterince iyi bir yaklaşımı olarak kabul edilir.

Bu geçici çözümün dezavantajları yok değildir.
Paket gönderme ve almanın eşit miktarda zaman aldığı varsayımını yapar.
Ancak hücresel ağlarda gönderme ve alma işlemleri zaman-simetrik olmayabilir.
Telefonunuzdaki yükleme hızlarının neredeyse her zaman indirme hızlarından düşük olduğunu fark etmiş olabilirsiniz.

`transmission_time = rtt/2`

Gidiş-geliş süresi ölçümünün teknik detayları [RTCP Gönderen ve Alıcı Raporları bölümünde](../06-media-communication/#receiver-reports--sender-reports) daha ayrıntılı olarak açıklanmıştır.

#### Jitter

Jitter, her paket için `İletim Süresinin` değişebileceği gerçeğidir. Paketleriniz gecikebilir, ancak daha sonra patlamalar halinde gelebilir.

#### Paket Kaybı

Paket Kaybı, iletim sırasında mesajların kaybolmasıdır. Kayıp sabit olabilir veya ani artışlar halinde gelebilir.
Bu, uydu veya Wi-Fi gibi ağ tipinden kaynaklanabilir. Veya yol boyunca yazılım tarafından tanıtılabilir.

#### Maksimum İletim Birimi

Maksimum İletim Birimi, tek bir paketin ne kadar büyük olabileceğinin sınırıdır. Ağlar bir dev mesaj göndermenize izin vermez. Protokol seviyesinde, mesajların birden fazla küçük pakete bölünmesi gerekebilir.

MTU ayrıca hangi ağ yolunu aldığınıza bağlı olarak da farklılık gösterecektir.
Gönderebileceğiniz en büyük paket boyutunu anlamak için [Path MTU Discovery](https://tools.ietf.org/html/rfc1191) gibi bir protokol kullanabilirsiniz.

### Tıkanıklık

Tıkanıklık, ağın sınırlarına ulaşıldığında ortaya çıkar. Bu genellikle mevcut rotanın kaldırabileceği en yüksek bant genişliğine ulaştığınız içindir. Veya ISP'nizin yapılandırdığı saatlik sınırlar gibi operatör dayatmalı olabilir.

Tıkanıklık kendini birçok farklı şekilde gösterir. Standartlaştırılmış davranış yoktur. Çoğu durumda tıkanıklığa ulaşıldığında ağ fazla paketleri düşürür. Diğer durumlarda ağ tamponlayacaktır. Bu paketlerinizin İletim Süresinin artmasına neden olur. Ağınız tıkandıkça daha fazla jitter de görebilirsiniz. Bu hızla değişen bir alan ve tıkanıklık tespiti için yeni algoritmalar hala yazılmaktadır.

### Dinamik

Ağlar inanılmaz derecede dinamiktir ve koşullar hızla değişebilir. Bir çağrı sırasında yüz binlerce paket gönderip alabilirsiniz.
Bu paketler birden fazla atlama üzerinden seyahat edecektir. Bu atlamalar milyonlarca başka kullanıcı tarafından paylaşılacaktır. Yerel ağınızda bile HD filmler indiriliyor olabilir veya belki bir cihaz yazılım güncellemesi indirmeye karar verir.

İyi bir çağrı yapmak başlangıçta ağınızı ölçmek kadar basit değildir. Sürekli değerlendirmeniz gerekir. Ayrıca çok sayıda ağ donanımı ve yazılımından gelen tüm farklı davranışları ele almanız gerekir.

## Paket Kaybını Çözme

Paket kaybını ele almak çözülecek ilk problemdir. Bunu çözmenin birden fazla yolu vardır, her birinin kendi faydaları vardır. Neyi gönderdiğinize ve gecikme toleransınızın ne olduğuna bağlıdır. Ayrıca tüm paket kaybının ölümcül olmadığını belirtmek önemlidir. Bazı video kaybetmek problem olmayabilir, insan gözü bunu algılayamayabilir bile. Kullanıcının metin mesajlarını kaybetmek ölümcüldür.

Diyelim ki 10 paket gönderiyorsunuz ve 5. ve 6. paketler kayboldu. Bunu çözmenin yolları şunlardır.

### Onaylar

Onaylar, alıcının gönderene aldığı her paketi bildirmesidir. Gönderen, son olmayan bir paket için iki kez onay aldığında paket kaybının farkına varır. Gönderen paket 4 için iki kez `ACK` aldığında, paket 5'in henüz görülmediğini bilir.

### Seçici Onaylar

Seçici Onaylar, Onayların gelişmiş halidir. Bir alıcı birden fazla paketi onaylayan ve gönderene boşlukları bildiren bir `SACK` gönderebilir.
Şimdi gönderen paket 4 ve 7 için bir `SACK` alabilir. Daha sonra paket 5 ve 6'yı yeniden göndermesi gerektiğini bilir.

### Negatif Onaylar

Negatif Onaylar problemi ters şekilde çözer. Gönderene neyi aldığını bildirmek yerine, alıcı gönderene neyin kaybolduğunu bildirir. Bizim durumumuzda paket 5 ve 6 için bir `NACK` gönderilecektir. Gönderen sadece alıcının yeniden gönderilmesini istediği paketleri bilir.

### İleri Hata Düzeltme

İleri Hata Düzeltme paket kaybını önceden düzeltir. Gönderen gereksiz veri gönderir, yani kayıp bir paket son akışı etkilemez. Bunun için popüler bir algoritma Reed–Solomon hata düzeltmesidir.

Basit bir örnekte, gönderen 3 paket gönderir ancak aynı mesaj 3 kez tekrarlanır. Alıcı bu 3 paketten herhangi ikisini alabildikçe mesajı yeniden yapılandırabilir.

### JitterBuffer

JitterBuffer akış halindeki gecikmeyi çözer. Geç gelen paketlerin titreşime neden olmaması avantajdır. Çağrı sırasında şu paket varış zamanlarını gördüğünüzü hayal edin:

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

Bu durumda, yaklaşık 1.8 ms iyi bir seçim olacaktır. Geç gelen paketler gecikme penceremizi kullanacak. Erken gelen paketler biraz geciktirilecek ve geç gelen paketlerin boşalttığı pencereyi dolduracak. Bu artık takılma olmadığı ve istemci için düzgün bir teslimat oranı sağladığı anlamına gelir.

### JitterBuffer işleyişi

![JitterBuffer](../images/05-jitterbuffer.png "JitterBuffer")

Her paket alınır alınmaz jitter buffer'a eklenir.
Çerçeveyi yeniden yapılandırmak için yeterli paket olduğunda, çerçeveyi oluşturan paketler buffer'dan serbest bırakılır ve decode için gönderilir.
Decoder, video çerçevesini decode eder ve kullanıcının ekranında çizer.
Jitter buffer sınırlı kapasiteye sahip olduğundan, buffer'da çok uzun süre kalan paketler atılacaktır.

Video çerçevelerinin RTP paketlerine nasıl dönüştürüldüğü ve yeniden yapılandırmanın neden gerekli olduğu hakkında daha fazla bilgi için [medya iletişimi bölümünü](../06-media-communication/#rtp) okuyun.

`jitterBufferDelay` ağ performansınız ve oynatma düzgünlüğü üzerindeki etkisini anlama konusunda harika bir içgörü sağlar.
Bu, alıcının gelen akışıyla ilgili [WebRTC istatistik API'sinin](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) bir parçasıdır.
Gecikme, video çerçevelerinin decode için gönderilmeden önce jitter buffer'da harcadığı zamanı tanımlar.
Uzun jitter buffer gecikmesi ağınızın yoğun olduğu anlamına gelir.

## Tıkanıklığı Tespit Etme

Tıkanıklığı çözmeden önce onu tespit etmemiz gerekir. Bunu tespit etmek için tıkanıklık kontrolcüsü kullanırız. Bu karmaşık bir konudur ve hala hızla değişmektedir.
Yeni algoritmalar hala yayınlanmakta ve test edilmektedir. Üst düzeyde hepsi aynı şekilde çalışır. Tıkanıklık kontrolcüsü, bazı girdiler verilen bant genişliği tahminleri sağlar.
Bunlar olası girdilerden bazıları:

- **Paket Kaybı** - Ağ tıkandıkça paketler düşürülür.
- **Jitter** - Ağ ekipmanı daha fazla yüklenirken paket sıralama zamanların düzensiz olmasına neden olur.
- **Gidiş-Geliş Süresi** - Tıkanıklık olduğunda paketlerin gelmesi daha uzun sürer. Jitter'ın aksine, Gidiş-Geliş Süresi artmaya devam eder.
- **Açık Tıkanıklık Bildirimi** - Yeni ağlar tıkanıklığı azaltmak için düşürülme riski taşıyan paketleri etiketleyebilir.

Bu değerlerin çağrı sırasında sürekli olarak ölçülmesi gerekir. Ağın kullanımı artabilir veya azalabilir, bu nedenle mevcut bant genişliği sürekli değişebilir.

## Tıkanıklığı Çözme

Artık tahmini bir bant genişliğimiz olduğuna göre gönderdiğimizi ayarlamamız gerekiyor. Nasıl ayarladığımız ne tür veri göndermek istediğimize bağlıdır.

### Daha Yavaş Gönderme

Veri gönderme hızınızı sınırlamak tıkanıklığı önlemenin ilk çözümüdür. Tıkanıklık Kontrolcüsü size bir tahmin verir ve hız sınırlamak gönderenin sorumluluğundadır.

Bu çoğu veri iletişimi için kullanılan yöntemdir. TCP gibi protokollerle bu işletim sistemi tarafından yapılır ve hem kullanıcılar hem de geliştiriciler için tamamen şeffaftır.

### Daha Az Gönderme

Bazı durumlarda sınırlarımızı karşılamak için daha az bilgi gönderebiliriz. Ayrıca verilerimizin gelişi için katı son teslim tarihlerimiz var, bu yüzden daha yavaş gönderemeyiz. Bunlar
Gerçek zamanlı medyanın altında kaldığı kısıtlamalardır.

Yeterli bant genişliğimiz yoksa, gönderdiğimiz video kalitesini düşürebiliriz. Bu video kodlayıcınız ve tıkanıklık kontrolcüsü arasında sıkı bir geri bildirim döngüsü gerektirir.

Bu, Onayları gönderme ve ele almanın gecikme/karmaşıklığını azaltır. İçinde bulunduğunuz ağın sıfır kaybı varsa İleri Hata Düzeltme bant genişliği israfıdır.

## Jitter'ı Çözme

Jitter çoğu ağda mevcuttur. Bir LAN içinde bile dalgalanan hızlarda veri gönderen birçok cihazınız vardır. `ping` komutuyla başka bir cihaza ping atarak ve gidiş-geliş gecikmesindeki dalgalanmaları fark ederek jitter'ı kolayca gözlemleyebilirsiniz.

Jitter'ı çözmek için istemciler JitterBuffer kullanır. JitterBuffer paketlerin sabit teslimat süresini sağlar. Dezavantajı JitterBuffer'ın erken gelen paketlere biraz gecikme eklemesidir.
Avantajı ise geç paketlerin jitter'a neden olmamasıdır. Bir çağrı sırasında aşağıdaki paket varış sürelerini gördüğünüzü hayal edin:

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

Bu durumda, yaklaşık 1.8 ms iyi bir seçim olurdu. Geç gelen paketler gecikme penceremizi kullanacaktır. Erken gelen paketler biraz geciktirilecek ve geç paketlerin tükettiği pencereyi doldurabilecektir. Bu, artık takılma olmadığı ve istemci için pürüzsüz teslimat hızı sağladığımız anlamına gelir.

### JitterBuffer işlemi

![JitterBuffer](../images/05-jitterbuffer.png "JitterBuffer")

Her paket alınır alınmaz jitter buffer'a eklenir.
Çerçeveyi yeniden oluşturmak için yeterli paket olduğunda, çerçeveyi oluşturan paketler buffer'dan serbest bırakılır ve dekodlama için gönderilir.
Dekoder, sırayla dekod eder ve video çerçevesini kullanıcının ekranında çizer.
Jitter buffer'ın sınırlı kapasitesi olduğundan, buffer'da çok uzun kalan paketler atılacaktır.

Video çerçevelerinin RTP paketlerine nasıl dönüştürüldüğü ve yeniden oluşturmanın neden gerekli olduğu hakkında daha fazla bilgi [medya iletişimi bölümünde](../06-media-communication/#rtp) okuyun.

`jitterBufferDelay` ağ performansınız ve oynatma pürüzsüzlüğü üzerindeki etkisi hakkında harika bir bakış açısı sağlar.
Alıcının gelen akışıyla ilgili [WebRTC istatistik API'sinin](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay) bir parçasıdır.
Gecikme, video çerçevelerinin dekodlama için gönderilmeden önce jitter buffer'da geçirdikleri süreyi tanımlar.
Uzun jitter buffer gecikmesi ağınızın yoğun şekilde tıkandığı anlamına gelir.

## Tıkanıklığı Tespit Etme

Tıkanıklığı çözmeden önce onu tespit etmemiz gerekir. Bunu tespit etmek için bir tıkanıklık kontrolörü kullanırız. Bu karmaşık bir konudur ve hala hızla değişmektedir.
Yeni algoritmalar hala yayınlanıyor ve test ediliyor. Yüksek seviyede hepsi aynı şekilde çalışır. Bir tıkanıklık kontrolörü bazı girdiler verildiğinde bant genişliği tahminleri sağlar.
Bunlar bazı olası girdilerdir:

- **Paket Kaybı** - Ağ tıkandıkça paketler düşürülür.
- **Jitter** - Ağ ekipmanı daha fazla yüklendiğinde paket kuyruğu zamanların düzensiz olmasına neden olur.
- **Gidiş-Geliş Süresi** - Tıkandığında paketlerin gelmesi daha uzun sürer. Jitter'dan farklı olarak, Gidiş-Geliş Süresi artmaya devam eder.
- **Açık Tıkanıklık Bildirimi** - Yeni ağlar tıkanıklığı hafifletmek için düşürülme riski altındaki paketleri etiketleyebilir.

Bu değerlerin çağrı sırasında sürekli ölçülmesi gerekir. Ağın kullanımı artabilir veya azalabilir, dolayısıyla mevcut bant genişliği sürekli değişiyor olabilir.

## Tıkanıklığı Çözme

Artık tahmini bir bant genişliğimiz olduğuna göre gönderdiğimizi ayarlamamız gerekiyor. Nasıl ayarladığımız hangi tür veri göndermek istediğimize bağlıdır.

### Daha Yavaş Gönderme

Veri gönderme hızınızı sınırlamak tıkanıklığı önlemenin ilk çözümüdür. Tıkanıklık Kontrolörü size bir tahmin verir ve gönderenin hızı sınırlaması sorumluluğundadır.

Bu çoğu veri iletişimi için kullanılan yöntemdir. TCP gibi protokollerde bu işletim sistemi tarafından yapılır ve hem kullanıcılar hem de geliştiriciler için tamamen şeffaftır.

### Daha Az Gönderme

Bazı durumlarda sınırlarımızı karşılamak için daha az bilgi gönderebiliriz. Ayrıca verilerimizin varışı için sert son teslim tarihlerimiz var, bu yüzden daha yavaş gönderemeyiz. Bunlar Gerçek zamanlı medyanın altında kaldığı kısıtlamalardır.

Yeterli bant genişliğimiz yoksa, gönderdiğimiz video kalitesini düşürebiliriz. Bu, video kodlayıcınız ve tıkanıklık kontrolörünüz arasında sıkı bir geri bildirim döngüsü gerektirir.
