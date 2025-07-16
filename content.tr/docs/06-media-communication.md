---
title: Medya İletişimi
type: docs
weight: 7
---

# Medya İletişimi

## WebRTC'nin medya iletişiminden ne elde ederim?

WebRTC size sınırsız miktarda ses ve video akışı gönderip almanıza izin verir. Bu akışları bir çağrı sırasında istediğiniz zaman ekleyip çıkarabilirsiniz. Bu akışların hepsi bağımsız olabilir veya birlikte paketlenmiş olabilir! Masaüstünüzün video beslemesini gönderebilir ve ardından web kameranızdan ses ve video ekleyebilirsiniz.

WebRTC protokolü codec agnostiktir. Alttaki aktarım her şeyi destekler, henüz var olmayan şeyleri bile! Ancak, iletişim kurduğunuz WebRTC Ajanı bunu kabul etmek için gerekli araçlara sahip olmayabilir.

WebRTC ayrıca dinamik ağ koşullarını ele almak için tasarlanmıştır. Bir çağrı sırasında bant genişliğiniz artabilir veya azalabilir. Belki aniden çok fazla paket kaybı yaşarsınız. Protokol tüm bunları ele almak için tasarlanmıştır. WebRTC ağ koşullarına yanıt verir ve mevcut kaynaklarla size mümkün olan en iyi deneyimi sunmaya çalışır.

## Nasıl çalışır?

WebRTC önceden var olan iki protokol kullanır: RTP ve RTCP, her ikisi de [RFC 1889](https://tools.ietf.org/html/rfc1889)'da tanımlanmıştır.

RTP (Gerçek zamanlı Aktarım Protokolü), medyayı taşıyan protokoldür. Videonun gerçek zamanlı teslimatına izin verecek şekilde tasarlanmıştır. Gecikme veya güvenilirlik etrafında herhangi bir kural koymazken, bunları uygulamak için araçları verir. RTP size akışlar verir, böylece tek bir bağlantı üzerinden birden fazla medya beslemesi çalıştırabilirsiniz. Ayrıca bir medya pipeline'ını beslemek için ihtiyacınız olan zamanlama ve sıralama bilgilerini de verir.

RTCP (RTP Kontrol Protokolü), çağrı hakkındaki meta verileri ileten protokoldür. Format çok esnektir ve istediğiniz meta verileri eklemenize izin verir. Bu, çağrı hakkındaki istatistikleri iletmek için kullanılır. Ayrıca paket kaybını ele almak ve tıkanıklık kontrolü uygulamak için de kullanılır. Değişen ağ koşullarına yanıt vermek için gerekli çift yönlü iletişimi sağlar.

## Gecikme vs Kalite

Gerçek zamanlı medya, gecikme ve kalite arasında ödünleşimler yapmakla ilgilidir. Tolere etmeye istekli olduğunuz gecikme ne kadar fazlaysa, o kadar yüksek kaliteli video bekleyebilirsiniz.

### Gerçek Dünya Sınırlamaları

Bu kısıtlamaların hepsi gerçek dünyanın sınırlamaları nedeniyle oluşur. Bunların hepsi üstesinden gelmeniz gereken ağınızın özellikleridir.

### Video Karmaşıktır

Video taşımak kolay değildir. 30 dakikalık sıkıştırılmamış 720 8-bit video depolamak için yaklaşık 110 GB'a ihtiyacınız var. Bu rakamlarla 4 kişilik konferans görüşmesi gerçekleşmeyecektir. Daha küçük hale getirmenin bir yoluna ihtiyacımız var ve cevap video sıkıştırmadır. Yine de bunun dezavantajları yok değildir.

## Video 101

Video sıkıştırmayı derinlemesine ele almayacağız, ancak RTP'nin neden bu şekilde tasarlandığını anlamak için yeterli kadarını ele alacağız. Video sıkıştırma, videoyu aynı videoyu temsil etmek için daha az bit gerektiren yeni bir formata kodlar.

### Kayıplı ve Kayıpsız sıkıştırma

Videoyu kayıpsız (hiçbir bilgi kaybolmaz) veya kayıplı (bilgi kaybolabilir) olacak şekilde kodlayabilirsiniz. Kayıpsız kodlama bir eşe daha fazla veri gönderilmesini gerektirdiği için, daha yüksek gecikmeli akış ve daha fazla düşürülen paket oluşturduğu için, video kalitesi o kadar iyi olmasa da RTP tipik olarak kayıplı sıkıştırma kullanır.

### Çerçeve içi ve çerçeveler arası sıkıştırma

Video sıkıştırma iki türde gelir. İlki çerçeve içidir. Çerçeve içi sıkıştırma, tek bir video çerçevesini tanımlamak için kullanılan bitleri azaltır. Aynı teknikler JPEG sıkıştırma yöntemi gibi durağan resimleri sıkıştırmak için kullanılır.

İkinci tür çerçeveler arası sıkıştırmadır. Video birçok resimden oluştuğu için aynı bilgiyi iki kez göndermemenin yollarını ararız.

### Çerçeve arası türler

Üç çerçeve türü vardır:

- **I-Frame** - Tam bir resim, başka bir şey olmadan decode edilebilir.
- **P-Frame** - Kısmi bir resim, sadece önceki resimden değişiklikleri içerir.
- **B-Frame** - Kısmi bir resim, önceki ve gelecek resimlerin bir modifikasyonudur.

Aşağıda üç çerçeve türünün görselleştirmesi verilmiştir.

![Frame types](../images/06-frame-types.png "Frame types")

### Video hassastır

Video sıkıştırma inanılmaz derecede durumludur, bu da internet üzerinden aktarımını zorlaştırır. Bir I-Frame'in bir parçasını kaybederseniz ne olur? P-Frame neyi değiştireceğini nasıl biliyor? Video sıkıştırma daha karmaşık hale geldikçe, bu daha da büyük bir sorun haline geliyor. Neyse ki RTP ve RTCP'nin çözümü var.

## RTP

### Paket Formatı

Her RTP paketi aşağıdaki yapıya sahiptir:

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

`Version` her zaman `2`'dir.

#### Padding (P)

`Padding`, payload'ın padding'i olup olmadığını kontrol eden bir boolean'dır.

Payload'ın son byte'ı kaç padding byte'ının eklendiğini içerir.

#### Extension (X)

Ayarlanırsa, RTP başlığının uzantıları olacaktır. Bu aşağıda daha ayrıntılı olarak açıklanmaktadır.

#### CSRC count (CC)

`SSRC`'den sonra ve payload'dan önce gelen `CSRC` tanımlayıcılarının miktarı.

#### Marker (M)

İşaretleyici bit önceden belirlenmiş bir anlama sahip değildir ve kullanıcının istediği şekilde kullanılabilir.

Bazı durumlarda kullanıcı konuşurken ayarlanır. Ayrıca yaygın olarak bir anahtar çerçeveyi işaretlemek için kullanılır.

#### Payload Type (PT)

`Payload Type`, bu paket tarafından taşınan codec'in benzersiz tanımlayıcısıdır.

WebRTC için `Payload Type` dinamiktir. Bir çağrıdaki VP8 diğerinden farklı olabilir. Çağrıdaki teklif veren, `Session Description`'da `Payload Types`'ın codec'lere eşlemesini belirler.

#### Sequence Number

`Sequence Number`, bir akıştaki paketleri sıralamak için kullanılır. Her paket gönderildiğinde `Sequence Number` bir artırılır.

RTP, kayıplı ağlar üzerinde yararlı olacak şekilde tasarlanmıştır. Bu, alıcıya paketlerin ne zaman kaybolduğunu tespit etme yolu verir.

#### Timestamp

Bu paket için örnekleme anı. Bu küresel bir saat değildir, medya akışında ne kadar zaman geçtiğidir. Birkaç RTP paketi, örneğin hepsi aynı video çerçevesinin parçasıysa aynı zaman damgasına sahip olabilir.

#### Synchronization Source (SSRC)

`SSRC`, bu akış için benzersiz tanımlayıcıdır. Bu, tek bir RTP akışı üzerinden birden fazla medya akışı çalıştırmanıza olanak tanır.

#### Contributing Source (CSRC)

Bu pakete hangi `SSRC`'lerin katkıda bulunduğunu ileten bir liste.

Bu yaygın olarak konuşma göstergeleri için kullanılır. Diyelim ki sunucu tarafında birden fazla ses beslemesini tek bir RTP akışında birleştirdiniz. Daha sonra bu alanı "Bu anda Giriş akışı A ve C konuşuyordu" demek için kullanabilirsiniz.

#### Payload

Gerçek payload verisi. Padding bayrağı ayarlanmışsa, kaç padding byte'ının eklendiğinin sayısıyla sonlanabilir.

### Uzantılar

## RTCP

### Paket Formatı

Her RTCP paketi aşağıdaki yapıya sahiptir:

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

`Version` her zaman `2`'dir.

#### Padding (P)

`Padding`, payload'ın padding'i olup olmadığını kontrol eden bir boolean'dır.

Payload'ın son byte'ı kaç padding byte'ının eklendiğini içerir.

#### Reception Report Count (RC)

Bu paketteki raporların sayısı. Tek bir RTCP paketi birden fazla olay içerebilir.

#### Packet Type (PT)

Bu RTCP Paketinin ne tür olduğunun benzersiz tanımlayıcısı. Bir WebRTC Ajanının tüm bu türleri desteklemesi gerekmez ve Ajanlar arasındaki destek farklı olabilir. Yaygın olarak görebilecekleriniz şunlardır:

- `192` - Full INTRA-frame Request (`FIR`)
- `193` - Negative ACKnowledgements (`NACK`)
- `200` - Sender Report
- `201` - Receiver Report
- `205` - Generic RTP Feedback
- `206` - Payload Specific Feedback

Bu paket türlerinin önemi aşağıda daha ayrıntılı olarak açıklanacaktır.

### Full INTRA-frame Request (FIR) ve Picture Loss Indication (PLI)

Hem `FIR` hem de `PLI` mesajları benzer bir amaca hizmet eder. Bu mesajlar gönderenden tam bir anahtar çerçeve ister.
`PLI`, kısmi çerçeveler decoder'a verildiğinde ancak bunları decode edemediğinde kullanılır.
Bu, çok fazla paket kaybınız olması veya belki decoder'ın çökmesi nedeniyle olabilir.

[RFC 5104](https://tools.ietf.org/html/rfc5104#section-4.3.1.2)'e göre, paketler veya çerçeveler kaybolduğunda `FIR` kullanılmamalıdır. Bu `PLI`'nin işidir. `FIR`, paket kaybı dışındaki nedenlerle bir anahtar çerçeve ister - örneğin yeni bir üye video konferansına girdiğinde. Video akışını decode etmeye başlamak için tam bir anahtar çerçeveye ihtiyaçları vardır, decoder anahtar çerçeve gelene kadar çerçeveleri atıyor olacaktır.

Alıcının bağlandıktan hemen sonra tam bir anahtar çerçeve istemesi iyi bir fikirdir, bu bağlanma ile kullanıcının ekranında görüntü çıkması arasındaki gecikmeyi minimize eder.

`PLI` paketleri Payload Specific Feedback mesajlarının bir parçasıdır.

Pratikte, hem `PLI` hem de `FIR` paketlerini işleyebilen yazılım her iki durumda da aynı şekilde davranacaktır. Encoder'a yeni bir tam anahtar çerçeve üretmesi için sinyal gönderecektir.

### Negative Acknowledgment

Bir `NACK`, gönderenin tek bir RTP paketini yeniden iletmesini ister. Bu genellikle bir RTP paketinin kaybolması nedeniyle olur, ancak geç kaldığı için de olabilir.

`NACK`'ler, tüm çerçevenin tekrar gönderilmesini istemekten çok daha bant genişliği açısından verimlidir. RTP paketleri çok küçük parçalara böldüğü için, gerçekten sadece küçük eksik bir parça istiyorsunuz. Alıcı SSRC ve Sequence Number ile bir RTCP mesajı oluşturur. Gönderen bu RTP paketini yeniden göndermek için mevcut değilse, mesajı görmezden gelir.

### Sender ve Receiver Reports

Bu raporlar ajanlar arasında istatistik göndermek için kullanılır. Bu, gerçekten alınan paket miktarını ve jitter'ı iletir.

Raporlar tanılama ve tıkanıklık kontrolü için kullanılabilir.

## RTP/RTCP nasıl birlikte sorunları çözer

RTP ve RTCP daha sonra ağların neden olduğu tüm sorunları çözmek için birlikte çalışır. Bu teknikler hala sürekli değişiyor!

### Forward Error Correction

FEC olarak da bilinir. Paket kaybıyla başa çıkmanın başka bir yöntemi. FEC, istenmeden bile aynı veriyi birden fazla kez göndermenizdir. Bu RTP seviyesinde veya codec ile daha da alt seviyede yapılır.

Bir çağrı için paket kaybı sabitiyse, FEC, NACK'ten çok daha düşük gecikmeli bir çözümdür. İstemek ve sonra eksik paketi yeniden iletmek zorunda kalmanın gidiş-dönüş süresi NACK'ler için önemli olabilir.

### Adaptive Bitrate ve Bandwidth Estimation

[Real-time networking](../05-real-time-networking/) bölümünde tartışıldığı gibi, ağlar öngörülemez ve güvenilmezdir. Bant genişliği kullanılabilirliği bir oturum boyunca birden fazla kez değişebilir.
Mevcut bant genişliğinin bir saniye içinde dramatik olarak (büyüklük mertebeleri) değiştiğini görmek nadir değildir.

Ana fikir, tahmin edilen, mevcut ve gelecekteki mevcut ağ bant genişliğine dayalı olarak kodlama bitrate'ini ayarlamaktır.
Bu, mümkün olan en iyi kalitede video ve ses sinyalinin iletilmesini ve ağ tıkanıklığı nedeniyle bağlantının düşmemesini sağlar.
Ağ davranışını modelleyen ve tahmin etmeye çalışan buluşsal yöntemler Bandwidth estimation olarak bilinir.

Bunun çok fazla nüansı vardır, bu yüzden daha ayrıntılı olarak inceleyelim.

## Ağ Durumunu Tanımlama ve İletişim

RTP/RTCP her türlü farklı ağ üzerinde çalışır ve sonuç olarak, bazı iletişimin gönderenden alıcıya giderken düşürülmesi yaygındır. UDP üzerine kurulduğu için, paket yeniden iletimi için yerleşik bir mekanizma yoktur, tıkanıklık kontrolünü ele almak şöyle dursun.

Kullanıcılara en iyi deneyimi sağlamak için WebRTC, ağ yolu hakkındaki nitelikleri tahmin etmeli ve bu niteliklerin zaman içinde nasıl değiştiğine uyum sağlamalıdır. İzlenmesi gereken temel özellikler şunlardır: mevcut bant genişliği (her yönde, simetrik olmayabilir), gidiş-dönüş süresi ve jitter (gidiş-dönüş süresindeki dalgalanmalar). Paket kaybını hesaba katması ve ağ koşulları değiştikçe bu özelliklerdeki değişiklikleri iletmesi gerekir.

Bu protokoller için iki temel amaç vardır:

1. Ağ tarafından desteklenen mevcut bant genişliğini (her yönde) tahmin etmek.
2. Gönderen ve alıcı arasında ağ özelliklerini iletmek.

RTP/RTCP'nin bu sorunu ele almak için üç farklı yaklaşımı vardır. Hepsinin artıları ve eksileri vardır ve genellikle her nesil öncekilerine göre gelişmiştir. Hangi uygulamayı kullanacağınız öncelikle istemcileriniz için mevcut yazılım yığınına ve uygulamanızı oluşturmak için mevcut kütüphanelere bağlı olacaktır.

### Receiver Reports / Sender Reports

İlk uygulama, Receiver Reports çifti ve tamamlayıcısı Sender Reports'tır. Bu RTCP mesajları [RFC 3550](https://tools.ietf.org/html/rfc3550#section-6.4)'de tanımlanmıştır ve uç noktalar arasında ağ durumunu iletmekten sorumludur. Receiver Reports, ağ hakkındaki nitelikleri (paket kaybı, gidiş-dönüş süresi ve jitter dahil) iletmeye odaklanır ve bu raporlara dayalı olarak mevcut bant genişliğini tahmin etmekten sorumlu diğer algoritmalarla eşleşir.

Sender ve Receiver raporları (SR ve RR) birlikte ağ kalitesinin bir resmini çizer. Her SSRC için bir programda gönderilirler ve mevcut bant genişliğini tahmin ederken kullanılan girdilerdir. Bu tahminler, aşağıdaki alanları içeren RR verilerini aldıktan sonra gönderen tarafından yapılır:

- **Fraction Lost** - Son Receiver Report'tan bu yana paketlerin yüzde kaçı kayboldu.
- **Cumulative Number of Packets Lost** - Tüm çağrı boyunca kaç paket kayboldu.
- **Extended Highest Sequence Number Received** - Alınan son Sequence Number neydi ve kaç kez döndü.
- **Interarrival Jitter** - Tüm çağrı için rolling Jitter.
- **Last Sender Report Timestamp** - Gönderendeki son bilinen zaman, gidiş-dönüş süresi hesaplaması için kullanılır.

SR ve RR, gidiş-dönüş süresini hesaplamak için birlikte çalışır.

Gönderen SR'de yerel zamanını `sendertime1`'i içerir. Alıcı bir SR paketi aldığında, RR'yi geri gönderir. Diğer şeylerin yanı sıra, RR gönderenden az önce alınan `sendertime1`'i içerir.
SR'yi alma ve RR'yi gönderme arasında bir gecikme olacaktır. Bu nedenle, RR ayrıca bir "son gönderen raporundan bu yana gecikme" zamanını - `DLSR`'yi de içerir. `DLSR`, gidiş-dönüş süresini ayarlamak için kullanılır.

İşlemde daha sonra gidiş-dönüş süresi tahminini yapmak için kullanılır. Gönderen RR'yi aldığında, mevcut zaman `sendertime2`'den `sendertime1` ve `DLSR`'yi çıkarır. Bu zaman deltası gidiş-dönüş yayılma gecikmesi veya gidiş-dönüş süresi olarak adlandırılır.

`rtt = sendertime2 - sendertime1 - DLSR`

Gidiş-dönüş süresi sade İngilizcede:

- Size saatimin mevcut okumasını içeren bir mesaj gönderirim, diyelim ki 16:20, 42 saniye ve 420 milisaniye.
- Siz de bu aynı zaman damgasını bana geri gönderirsiniz.
- Ayrıca mesajımı okumaktan mesajı geri göndermeye kadar geçen zamanı da dahil edersiniz, diyelim ki 5 milisaniye.
- Zamanı geri aldığımda, saate tekrar bakarım.
- Şimdi saatim 16:20, 42 saniye 690 milisaniye diyor.
- Bu, size ulaşıp bana geri dönmek için 265 milisaniye (690 - 420 - 5) aldığı anlamına gelir.
- Dolayısıyla, gidiş-dönüş süresi 265 milisaniyedir.

![Round-trip time](../images/06-rtt.png "Round-trip time")

### TMMBR, TMMBN, REMB ve TWCC, GCC ile eşleştirilmiş

#### Google Congestion Control (GCC)

Google Congestion Control (GCC) algoritması ([draft-ietf-rmcat-gcc-02](https://tools.ietf.org/html/draft-ietf-rmcat-gcc-02)'de özetlenmiştir) bant genişliği tahmininin zorluğunu ele alır. İlişkili iletişim gereksinimlerini kolaylaştırmak için çeşitli diğer protokollerle eşleşir. Sonuç olarak, alıcı tarafında (TMMBR/TMMBN veya REMB ile çalıştırıldığında) veya gönderen tarafında (TWCC ile çalıştırıldığında) çalışmaya çok uygundur.

Mevcut bant genişliği tahminlerine ulaşmak için GCC, iki temel metrik olarak paket kaybına ve çerçeve varış zamanındaki dalgalanmalara odaklanır. Bu metrikleri iki bağlantılı kontrolör üzerinden çalıştırır: kayıp-tabanlı kontrolör ve gecikme-tabanlı kontrolör.

GCC'nin ilk bileşeni olan kayıp-tabanlı kontrolör basittir:

- Paket kaybı %10'un üzerindeyse, bant genişliği tahmini azaltılır.
- Paket kaybı %2-10 arasındaysa, bant genişliği tahmini aynı kalır.
- Paket kaybı %2'nin altındaysa, bant genişliği tahmini artırılır.

Paket kaybı ölçümleri sık sık alınır. Eşleştirilmiş iletişim protokolüne bağlı olarak, paket kaybı ya açıkça iletilir (TWCC'de olduğu gibi) ya da çıkarılır (TMMBR/TMMBN ve REMB'de olduğu gibi). Bu yüzdeler yaklaşık bir saniye civarındaki zaman pencereleri üzerinde değerlendirilir.

Gecikme-tabanlı kontrolör, kayıp-tabanlı kontrolörle işbirliği yapar ve paket varış zamanındaki varyasyonlara bakar. Bu gecikme-tabanlı kontrolör, ağ bağlantılarının ne zaman giderek daha tıkanık hale geldiğini belirlemeyi amaçlar ve paket kaybı oluşmadan önce bile bant genişliği tahminlerini azaltabilir. Teori, yol boyunca en meşgul ağ arayüzünün, arayüz tamponlarının içindeki kapasitesi bitene kadar paketleri sıraya koymaya devam edeceğidir. Bu arayüz gönderebileceğinden daha fazla trafik almaya devam ederse, tampon alanına sığdıramadığı tüm paketleri düşmeye zorlanacaktır. Bu tür paket kaybı, düşük gecikmeli/gerçek zamanlı iletişim için özellikle yıkıcıdır, ancak aynı zamanda bu bağlantı üzerindeki tüm iletişim için verimi de bozabilir ve ideal olarak kaçınılmalıdır. Bu nedenle, GCC, paket kaybı gerçekten gerçekleşmeden _önce_ ağ bağlantılarının giderek büyüyen kuyruk derinlikleri olup olmadığını anlamaya çalışır. Zaman içinde artan sıralama gecikmelerini gözlemlerse bant genişliği kullanımını azaltacaktır.

Bunu başarmak için GCC, gidiş-dönüş süresindeki ince artışları ölçerek kuyruk derinliğindeki artışları çıkarmaya çalışır. Çerçevelerin "varış-arası zamanını" kaydeder, `t(i) - t(i-1)`: iki paket grubunun (genellikle ardışık video çerçeveleri) varış zamanındaki fark. Bu paket grupları sıklıkla düzenli zaman aralıklarında ayrılır (örneğin, 24 fps bir video için her 1/24 saniyede bir). Sonuç olarak, varış-arası zamanı ölçmek, ilk paket grubunun (yani çerçevenin) başlangıcı ile bir sonrakinin ilk çerçevesi arasındaki zaman farkını kaydetmek kadar basittir.

Aşağıdaki diyagramda, medyan paketler arası gecikme artışı +20 msn'dir, ağ tıkanıklığının açık bir göstergesidir.

![TWCC with delay](../images/06-twcc.png "TWCC with delay")

Varış-arası zaman zaman içinde artıyorsa, bu bağlayan ağ arayüzlerinde artan kuyruk derinliğinin kanıtı olarak kabul edilir ve ağ tıkanıklığı olarak değerlendirilir. (Not: GCC, çerçeve byte boyutlarındaki dalgalanmalar için bu ölçümleri kontrol edecek kadar akıllıdır.) GCC, gecikme ölçümlerini bir [Kalman filtresini](https://en.wikipedia.org/wiki/Kalman_filter) kullanarak rafine eder ve tıkanıklığı işaretlemeden önce ağ gidiş-dönüş sürelerinin (ve varyasyonlarının) birçok ölçümünü alır. GCC'nin Kalman filtresini doğrusal regresyonun yerini alacak şekilde düşünebilirsiniz: jitter zamanlama ölçümlerine gürültü eklediğinde bile doğru tahminler yapmaya yardımcı olur. Tıkanıklığı işaretledikten sonra, GCC mevcut bitrate'i azaltacaktır. Alternatif olarak, sabit ağ koşulları altında, daha yüksek yük değerlerini test etmek için bant genişliği tahminlerini yavaşça artırabilir.

#### TMMBR, TMMBN ve REMB

TMMBR/TMMBN ve REMB için, alıcı taraf önce mevcut gelen bant genişliğini tahmin eder (GCC gibi bir protokol kullanarak) ve ardından bu bant genişliği tahminlerini uzak gönderenlere iletir. Paket kaybı veya ağ tıkanıklığı hakkındaki diğer nitelikler hakkında ayrıntı alışverişi yapmaları gerekmez çünkü alıcı tarafında çalışmak onların varış-arası zamanı ve paket kaybını doğrudan ölçmelerine olanak tanır. Bunun yerine, TMMBR, TMMBN ve REMB sadece bant genişliği tahminlerinin kendilerini alışverişi yapar:

- **Temporary Maximum Media Stream Bit Rate Request** - Tek bir SSRC için istenen bitrate'in mantissa/üssü.
- **Temporary Maximum Media Stream Bit Rate Notification** - Bir TMMBR'nin alındığını bildiren mesaj.
- **Receiver Estimated Maximum Bitrate** - Tüm oturum için istenen bitrate'in mantissa/üssü.

TMMBR ve TMMBN önce geldi ve [RFC 5104](https://tools.ietf.org/html/rfc5104)'te tanımlandı. REMB daha sonra geldi, [draft-alvestrand-rmcat-remb](https://tools.ietf.org/html/draft-alvestrand-rmcat-remb-03)'de bir taslak sunuldu, ancak hiçbir zaman standartlaştırılmadı.

REMB kullanan örnek bir oturum aşağıdaki gibi davranabilir:

![REMB](../images/06-remb.png "REMB")

Bu yöntem kağıt üzerinde harika çalışır. Gönderen alıcıdan tahmin alır, encoder bitrate'ini alınan değere ayarlar. Tada! Ağ koşullarına uyum sağladık.

Ancak pratikte, REMB yaklaşımının birden fazla dezavantajı vardır.

Encoder verimsizliği birincisidir. Encoder için bir bitrate ayarladığınızda, mutlaka istediğiniz tam bitrate'i çıkarmayacaktır. Kodlama, encoder ayarlarına ve kodlanan çerçeveye bağlı olarak daha fazla veya daha az bit çıkarabilir.

Örneğin, x264 encoder'ını `tune=zerolatency` ile kullanmak belirtilen hedef bitrate'ten önemli ölçüde sapabilir. İşte olası bir senaryo:

- Diyelim ki bitrate'i 1000 kbps'ye ayarlayarak başlıyoruz.
- Encoder sadece 700 kbps çıkarıyor, çünkü kodlamak için yeterli yüksek frekans özelliği yok. (AKA - "duvara bakmak".)
- Ayrıca alıcının 700 kbps videoyu sıfır paket kaybıyla aldığını hayal edelim. Daha sonra gelen bitrate'i %8 artırmak için REMB kuralı 1'i uygular.
- Alıcı gönderene 756 kbps önerisi (700 kbps \* 1.08) ile bir REMB paketi gönderir.
- Gönderen encoder bitrate'ini 756 kbps'ye ayarlar.
- Encoder daha da düşük bir bitrate çıkarır.
- Bu süreç kendini tekrar etmeye devam eder ve bitrate'i mutlak minimuma düşürür.

Bunun nasıl ağır encoder parametre ayarlamasına neden olacağını ve harika bir bağlantıda bile izlenemez videoyla kullanıcıları şaşırtacağını görebilirsiniz.

#### Transport Wide Congestion Control

Transport Wide Congestion Control, RTCP ağ durumu iletişimindeki en son gelişmedir. [draft-holmer-rmcat-transport-wide-cc-extensions-01](https://datatracker.ietf.org/doc/html/draft-holmer-rmcat-transport-wide-cc-extensions-01)'de tanımlanmıştır, ancak aynı zamanda hiçbir zaman standartlaştırılmamıştır.

TWCC oldukça basit bir prensip kullanır:

![TWCC](../images/06-twcc-idea.png "TWCC")

REMB ile alıcı, gönderen tarafa mevcut indirme bitrate'ini bildirir. Çıkarılan paket kaybı hakkında kesin ölçümler ve sadece kendisinin sahip olduğu paketler arası varış zamanı hakkında veri kullanır.

TWCC, SR/RR ve REMB protokol nesilleri arasında neredeyse hibrit bir yaklaşımdır. Bant genişliği tahminlerini gönderen tarafa geri getirir (SR/RR'ye benzer), ancak bant genişliği tahmin tekniği REMB nesline daha çok benzer.

TWCC ile alıcı, gönderene her paketin varış zamanını bildirir. Bu, gönderenin paketler arası varış gecikme varyasyonunu ölçmesi ve ses/video beslemesine katkıda bulunamayacak kadar düşürülen veya geç gelen paketleri tanımlaması için yeterli bilgidir. Bu veriler sık sık alışverişi edildiğinde, gönderen değişen ağ koşullarına hızla uyum sağlayabilir ve GCC gibi bir algoritma kullanarak çıkış bant genişliğini değiştirebilir.

Gönderen gönderilen paketleri, sıra numaralarını, boyutlarını ve zaman damgalarını takip eder. Gönderen alıcıdan RTCP mesajları aldığında, gönderme paketler arası gecikmelerini alma gecikmeleriyle karşılaştırır. Alma gecikmeleri artıyorsa, ağ tıkanıklığını işaret eder ve gönderen düzeltici önlemler almalıdır.

Gönderene ham veri sağlayarak, TWCC gerçek zamanlı ağ koşullarına mükemmel bir görünüm sağlar:

- Bireysel kayıp paketlere kadar neredeyse anında paket kaybı davranışı
- Doğru gönderme bitrate'i
- Doğru alma bitrate'i
- Jitter ölçümü
- Gönderme ve alma paket gecikmeleri arasındaki farklar
- Ağın patlamalı veya sabit bant genişliği teslimatını nasıl tolere ettiğinin açıklaması

TWCC'nin en önemli katkılarından biri, WebRTC geliştiricilerine sağladığı esnekliktir. Tıkanıklık kontrol algoritmasını gönderen tarafa konsolide ederek, yaygın olarak kullanılabilen ve zaman içinde minimal geliştirmeler gerektiren basit istemci koduna olanak tanır. Karmaşık tıkanıklık kontrol algoritmaları daha sonra doğrudan kontrol ettikleri donanımda (Bölüm 8'de tartışılan Selective Forwarding Unit gibi) daha hızlı bir şekilde yinelenebilir. Tarayıcılar ve mobil cihazlar söz konusu olduğunda, bu, bu istemcilerin standartlaştırma veya tarayıcı güncellemelerini beklemek zorunda kalmadan (yaygın olarak kullanılabilir olması oldukça uzun sürebilir) algoritma geliştirmelerinden faydalanabileceği anlamına gelir.

## Bant Genişliği Tahmini Alternatifleri

En çok dağıtılan uygulama, [draft-alvestrand-rmcat-congestion](https://tools.ietf.org/html/draft-alvestrand-rmcat-congestion-02)'da tanımlanan "Gerçek Zamanlı İletişim için Google Tıkanıklık Kontrol Algoritması"dır.

GCC'ye birkaç alternatif vardır, örneğin [NADA: Gerçek Zamanlı Medya için Birleşik Tıkanıklık Kontrol Şeması](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04) ve [SCReAM - Multimedya için Kendi Kendine Saatli Hız Adaptasyonu](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05).
