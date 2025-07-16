---
title: Bağlanma
type: docs
weight: 4
---

# Bağlanma

## WebRTC neden bağlanma için özel bir alt sisteme ihtiyaç duyar?

Bugün dağıtılan çoğu uygulama istemci/sunucu bağlantıları kurar. Bir istemci/sunucu bağlantısı, sunucunun kararlı, iyi bilinen bir aktarım adresine sahip olmasını gerektirir. Bir istemci sunucuyla iletişime geçer ve sunucu yanıt verir.

WebRTC bir istemci/sunucu modeli kullanmaz, eşten-eşe (P2P) bağlantılar kurar. P2P bağlantısında, bağlantı oluşturma görevi her iki eşe eşit olarak dağıtılır. Bunun nedeni, WebRTC'de bir aktarım adresinin (IP ve port) varsayılamayacak olması ve hatta oturum sırasında değişebilmesidir. WebRTC tüm toplayabileceği bilgileri toplayacak ve iki WebRTC Ajanı arasında çift yönlü iletişim sağlamak için büyük çaba gösterecektir.

Ancak eşten-eşe bağlantı kurmak zor olabilir. Bu ajanlar doğrudan bağlantısı olmayan farklı ağlarda olabilir. Doğrudan bağlantının mevcut olduğu durumlarda bile başka sorunlarınız olabilir. Bazı durumlarda, istemcileriniz aynı ağ protokollerini konuşmaz (UDP <-> TCP) veya belki farklı IP Sürümleri (IPv4 <-> IPv6) kullanır.

P2P bağlantı kurmada bu zorluklara rağmen, WebRTC'nin sunduğu aşağıdaki özellikler nedeniyle geleneksel İstemci/Sunucu teknolojisine göre avantajlar elde edersiniz.

### Azaltılmış Bant Genişliği Maliyetleri

Medya iletişimi doğrudan eşler arasında gerçekleştiği için medyayı aktarmak için ayrı bir sunucu için ödeme yapmanız veya barındırmanız gerekmez.

### Daha Düşük Gecikme

İletişim doğrudan olduğunda daha hızlıdır! Bir kullanıcı her şeyi sunucunuzdan geçirmek zorunda kaldığında, aktarımları yavaşlatır.

### Güvenli Uçtan Uca İletişim

Doğrudan İletişim daha güvenlidir. Kullanıcılar verileri sunucunuzdan yönlendirmediği için, şifresini çözmeyeceğinize güvenmeleri bile gerekmez.

## Nasıl çalışır?

Yukarıda açıklanan işleme Etkileşimli Bağlantı Kurma ([ICE](https://tools.ietf.org/html/rfc8445)) denir. WebRTC'den önce var olan başka bir protokol.

ICE, iki ICE Ajanı arasında iletişim kurmanın en iyi yolunu bulmaya çalışan bir protokoldür. Her ICE Ajanı ulaşılabilir olduğu yolları yayınlar, bunlar adaylar olarak bilinir. Bir aday, esasen ajanın diğer eşin ulaşabileceğine inandığı aktarım adresidir. ICE daha sonra adayların en iyi eşleşmesini belirler.

Gerçek ICE süreci bu bölümün ilerleyen kısımlarında daha ayrıntılı olarak açıklanmıştır. ICE'nin neden var olduğunu anlamak için, hangi ağ davranışlarını aştığımızı anlamak yararlıdır.

## Gerçek dünya ağ kısıtlamaları

ICE tamamen gerçek dünya ağlarının kısıtlamalarını aşmakla ilgilidir. Çözümü keşfetmeden önce, gerçek problemleri konuşalım.

### Aynı ağda değil

Çoğu zaman diğer WebRTC Ajanı aynı ağda bile olmayacaktır. Tipik bir çağrı genellikle doğrudan bağlantısı olmayan farklı ağlardaki iki WebRTC Ajanı arasındadır.

Aşağıda genel internet üzerinden bağlanan iki farklı ağın grafiği bulunmaktadır. Her ağda iki host bulunmaktadır.

Aynı ağdaki hostlar için bağlantı kurmak çok kolaydır. `192.168.0.1 -> 192.168.0.2` arasındaki iletişim kolay yapılabilir! Bu iki host herhangi bir dış yardım olmadan birbirine bağlanabilir.

Ancak, `Router B` kullanan bir host'un `Router A`'nın arkasındaki hiçbir şeye doğrudan erişim yolu yoktur. `Router A`'nın arkasındaki `192.168.0.1` ile `Router B`'nin arkasındaki aynı IP arasındaki farkı nasıl anlarsınız? Bunlar özel IP'lerdir! `Router B` kullanan bir host doğrudan `Router A`'ya trafik gönderebilir, ancak istek orada sonlanır. `Router A` mesajı hangi host'a yönlendirmesi gerektiğini nasıl bilir?

### Protokol Kısıtlamaları

Bazı ağlar UDP trafiğine hiç izin vermez, belki de TCP'ye izin vermezler. Bazı ağlarda çok düşük MTU (Maksimum İletim Birimi) olabilir. Ağ yöneticilerinin değiştirebileceği ve iletişimi zorlaştırabilecek birçok değişken vardır.

### Firewall/IDS Kuralları

Bir diğeri "Derin Paket İncelemesi" ve diğer akıllı filtrelemelerdir. Bazı ağ yöneticileri her paketi işlemeye çalışan yazılım çalıştırır. Çoğu zaman bu yazılım WebRTC'yi anlamaz, bu yüzden ne yapacağını bilmediği için onu bloklar, örneğin WebRTC paketlerini beyaz listede olmayan rastgele bir port üzerindeki şüpheli UDP paketleri olarak değerlendirir.

## NAT Mapping

NAT (Ağ Adresi Çevirisi) eşlemesi WebRTC'nin bağlantısını mümkün kılan sihirdir. WebRTC'nin tamamen farklı alt ağlardaki iki eşin iletişim kurmasına nasıl izin verdiği, yukarıdaki "aynı ağda değil" problemini ele aldığı budur. Yeni zorluklar yaratsa da, NAT eşlemesinin ilk etapta nasıl çalıştığını açıklayalım.

Relay, proxy veya sunucu kullanmaz. Yine `Ajan 1` ve `Ajan 2`'miz var ve farklı ağlardalar. Ancak, trafik tamamen akıyor. Görselleştirildiğinde şöyle görünür:

![NAT mapping](../images/03-nat-mapping.png "NAT mapping")

Bu iletişimi gerçekleştirmek için bir NAT eşlemesi kurarsınız. Ajan 1, Ajan 2 ile WebRTC bağlantısı kurmak için port 7000'i kullanır. Bu, `192.168.0.1:7000`'i `5.0.0.1:7000`'e bağlama oluşturur. Bu daha sonra Ajan 2'nin `5.0.0.1:7000`'e paketler göndererek Ajan 1'e ulaşmasına izin verir. Bu örnekteki gibi NAT eşlemesi oluşturmak, router'ınızda port yönlendirme yapmanın otomatik versiyonu gibidir.

NAT eşlemesinin dezavantajı, tek bir eşleme formu olmaması (örneğin statik port yönlendirme) ve davranışın ağlar arasında tutarsız olmasıdır. ISP'ler ve donanım üreticileri bunu farklı şekillerde yapabilir. Bazı durumlarda, ağ yöneticileri bunu devre dışı bile bırakabilir.

İyi haber, davranış aralığının tam olarak anlaşılması ve gözlemlenebilir olmasıdır, bu yüzden bir ICE Ajanı bir NAT eşlemesi oluşturduğunu ve eşlemenin özelliklerini doğrulayabilir.

Bu davranışları açıklayan belge [RFC 4787](https://tools.ietf.org/html/rfc4787)'dir.

### Eşleme Oluşturma

Eşleme oluşturmak en kolay kısımdır. Ağınızın dışındaki bir adrese paket gönderdiğinizde, bir eşleme oluşturulur! NAT eşlemesi, NAT'ınız tarafından tahsis edilen sadece geçici bir genel IP ve port'tur. Giden mesaj, kaynak adresinin yeni eşleme adresi tarafından verilmesi için yeniden yazılacaktır. Eşlemeye bir mesaj gönderilirse, onu oluşturan NAT içindeki host'a otomatik olarak geri yönlendirilecektir. Eşlemeler etrafındaki ayrıntılar karmaşık hale geldiği yerdir.

### Eşleme Oluşturma Davranışları

Eşleme oluşturma üç farklı kategoriye ayrılır:

#### Endpoint-Independent Mapping

NAT içindeki her gönderen için bir eşleme oluşturulur. İki farklı uzak adrese iki paket gönderirseniz, NAT eşlemesi yeniden kullanılacaktır. Her iki uzak host da aynı kaynak IP ve port'u görecektir. Uzak hostlar yanıt verirlerse, aynı yerel dinleyiciye geri gönderilecektir.

Bu en iyi durum senaryosudur. Bir çağrının çalışması için en az bir tarafın bu türde olması GEREKİR.

#### Address Dependent Mapping

Yeni bir adrese paket gönderdiğiniz her seferde yeni bir eşleme oluşturulur. İki farklı host'a iki paket gönderirseniz, iki eşleme oluşturulacaktır. Aynı uzak host'a ancak farklı hedef portlara iki paket gönderirseniz, yeni bir eşleme oluşturulmayacaktır.

#### Address and Port Dependent Mapping

Uzak IP veya port farklıysa yeni bir eşleme oluşturulur. Aynı uzak host'a ancak farklı hedef portlara iki paket gönderirseniz, yeni bir eşleme oluşturulacaktır.

### Eşleme Filtreleme Davranışları

Eşleme filtreleme, eşlemeyi kimlerin kullanmasına izin verildiği etrafındaki kurallardır. Benzer üç sınıflandırmaya ayrılırlar:

#### Endpoint-Independent Filtering

Herkes eşlemeyi kullanabilir. Eşlemeyi birden fazla diğer eşle paylaşabilirsiniz ve hepsi ona trafik gönderebilir.

#### Address Dependent Filtering

Sadece eşlemenin oluşturulduğu host eşlemeyi kullanabilir. `A` host'una bir paket gönderirseniz sadece aynı host'tan yanıt alabilirsiniz. `B` host'u o eşlemeye paket göndermeye çalışırsa, görmezden gelinecektir.

#### Address and Port Dependent Filtering

Sadece eşlemenin oluşturulduğu host ve port o eşlemeyi kullanabilir. `A:5000`'e bir paket gönderirseniz sadece aynı host ve port'tan yanıt alabilirsiniz. `A:5001` o eşlemeye paket göndermeye çalışırsa, görmezden gelinecektir.

### Eşleme Yenileme

Bir eşleme 5 dakika kullanılmazsa yok edilmesi önerilir. Bu tamamen ISP veya donanım üreticisine bağlıdır.

## STUN

STUN (NAT için Oturum Geçiş Yardımcı Programları) sadece NAT'larla çalışmak için oluşturulmuş bir protokoldür. Bu, WebRTC'den (ve ICE'den!) önce var olan başka bir teknolojidir. [RFC 8489](https://tools.ietf.org/html/rfc8489) tarafından tanımlanır, bu aynı zamanda STUN paket yapısını da tanımlar. STUN protokolü ayrıca ICE/TURN tarafından da kullanılır.

STUN, NAT Eşlemelerinin programatik olarak oluşturulmasına izin verdiği için yararlıdır. STUN'dan önce, bir NAT eşlemesi oluşturabiliyorduk, ancak bunun IP ve port'unun ne olduğu hakkında hiçbir fikrimiz yoktu! STUN size sadece eşleme oluşturma yeteneği vermekle kalmaz, aynı zamanda başkalarıyla paylaşabilmeniz için ayrıntıları da verir, böylece az önce oluşturduğunuz eşleme aracılığıyla size trafik geri gönderebilirler.

STUN'un temel bir açıklamasıyla başlayalım. Daha sonra, TURN ve ICE kullanımını genişleteceğiz. Şimdilik, sadece eşleme oluşturmak için İstek/Yanıt akışını açıklayacağız. Sonra başkalarıyla paylaşmak için ayrıntılarını nasıl alacağımızı konuşacağız. Bu, WebRTC PeerConnection için ICE URL'lerinizde bir `stun:` sunucunuz olduğunda gerçekleşen işlemdir. Özetle, STUN bir NAT arkasındaki endpoint'in NAT dışındaki bir STUN sunucusundan gözlemlediğini rapor etmesini isteyerek hangi eşlemenin oluşturulduğunu anlamasına yardımcı olur.

### Protokol Yapısı

Her STUN paketi aşağıdaki yapıya sahiptir:

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

Her STUN paketinin bir türü vardır. Şimdilik, sadece aşağıdakilerle ilgileniyoruz:

- Binding Request - `0x0001`
- Binding Response - `0x0101`

NAT eşlemesi oluşturmak için bir `Binding Request` yaparız. Sonra sunucu `Binding Response` ile yanıt verir.

#### Message Length

Bu, `Data` bölümünün ne kadar uzun olduğudur. Bu bölüm `Message Type` tarafından tanımlanan rastgele veriler içerir.

#### Magic Cookie

Ağ byte sırasında sabit değer `0x2112A442`, STUN trafiğini diğer protokollerden ayırt etmeye yardımcı olur.

#### Transaction ID

Bir istek/yanıtı benzersiz şekilde tanımlayan 96-bit tanımlayıcı. Bu, isteklerinizi ve yanıtlarınızı eşleştirmenize yardımcı olur.

#### Data

Data bir STUN öznitelikleri listesi içerecektir. Bir STUN Özniteliği aşağıdaki yapıya sahiptir:

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Type                  |            Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Value (variable)                ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

`STUN Binding Request` hiçbir öznitelik kullanmaz. Bu, `STUN Binding Request`'in sadece başlığı içerdiği anlamına gelir.

`STUN Binding Response` bir `XOR-MAPPED-ADDRESS (0x0020)` kullanır. Bu öznitelik bir IP ve port içerir. Bu, oluşturulan NAT eşlemesinin IP ve port'udur!

### NAT Eşlemesi Oluşturma

STUN kullanarak NAT eşlemesi oluşturmak sadece bir istek göndermeyi gerektirir! STUN Sunucusuna bir `STUN Binding Request` gönderirsiniz. STUN Sunucusu daha sonra `STUN Binding Response` ile yanıt verir.
Bu `STUN Binding Response` `Mapped Address` içerecektir. `Mapped Address`, STUN Sunucusunun sizi nasıl gördüğüdür ve sizin `NAT eşlemenizdir`.
`Mapped Address`, birinin size paketler göndermesini istiyorsanız paylaşacağınız şeydir.

İnsanlar `Mapped Address`'i aynı zamanda sizin `Public IP`'niz veya `Server Reflexive Candidate`'ınız olarak da adlandırırlar.

### NAT Türünü Belirleme

Ne yazık ki, `Mapped Address` tüm durumlarda yararlı olmayabilir. `Address Dependent` ise, sadece STUN sunucusu size geri trafik gönderebilir. Bunu paylaştıysanız ve başka bir eş mesaj göndermeye çalıştıysa, düşürüleceklerdir. Bu, başkalarıyla iletişim kurmak için işe yaramaz hale getirir. `Address Dependent` durumunun aslında çözülebilir olduğunu görebilirsiniz, eğer STUN sunucusunu çalıştıran host aynı zamanda sizin için paketleri eşe yönlendirebiliyorsa! Bu bizi aşağıda TURN kullanarak çözüme götürür.

[RFC 5780](https://tools.ietf.org/html/rfc5780) NAT Türünüzü belirlemek için bir test çalıştırma yöntemi tanımlar. Bu yararlıdır çünkü doğrudan bağlantının mümkün olup olmadığını önceden bilirsiniz.

## TURN

TURN (NAT etrafında Relay'ler Kullanarak Geçiş) [RFC 8656](https://tools.ietf.org/html/rfc8656)'da tanımlanır ve doğrudan bağlantının mümkün olmadığı durumlarda çözümdür. Bu, uyumsuz iki NAT Türünüz olması veya belki aynı protokolü konuşamıyor olmanız nedeniyle olabilir! TURN ayrıca gizlilik amaçları için de kullanılabilir. Tüm iletişiminizi TURN üzerinden çalıştırarak istemcinin gerçek adresini gizlersiniz.

TURN özel bir sunucu kullanır. Bu sunucu bir istemci için proxy görevi görür. İstemci bir TURN Sunucusuna bağlanır ve bir `Allocation` oluşturur. Allocation oluşturarak, istemci istemciye geri trafik göndermek için kullanılabilecek geçici bir IP/Port/Protokol alır. Bu yeni dinleyici `Relayed Transport Address` olarak bilinir. Bunu yönlendirme adresi olarak düşünün, başkalarının TURN üzerinden size trafik gönderebilmesi için bunu dağıtırsınız! `Relay Transport Address`'i verdiğiniz her eş için, sizinle iletişime izin vermek için yeni bir `Permission` oluşturmalısınız.

TURN üzerinden giden trafiği gönderdiğinizde, `Relayed Transport Address` üzerinden gönderilir. Uzak bir eş trafik aldığında, TURN Sunucusundan geldiğini görür.

### TURN Yaşam Döngüsü

Aşağıda TURN allocation oluşturmak isteyen bir istemcinin yapması gereken her şey bulunmaktadır. TURN kullanan biriyle iletişim kurmak hiçbir değişiklik gerektirmez. Diğer eş bir IP ve port alır ve herhangi bir diğer host gibi onunla iletişim kurar.

#### Allocations

Allocation'lar TURN'ün kalbindedir. Bir `allocation` temel olarak bir "TURN Oturumu"dur. TURN allocation oluşturmak için TURN `Server Transport Address` (genellikle port `3478`) ile iletişim kurarsınız.

Allocation oluştururken, aşağıdakileri sağlamanız gerekir:

- Kullanıcı Adı/Şifre - TURN allocation'ları oluşturmak kimlik doğrulaması gerektirir.
- Allocation Transport - Sunucu (`Relayed Transport Address`) ve eşler arasındaki aktarım protokolü, UDP veya TCP olabilir.
- Even-Port - Birden fazla allocation için ardışık portlar isteyebilirsiniz, WebRTC için ilgili değil.

İstek başarılı olursa, Data bölümünde aşağıdaki STUN Öznitelikleri ile TURN Sunucusundan bir yanıt alırsınız:

- `XOR-MAPPED-ADDRESS` - `TURN Client`'ın `Mapped Address`'i. Birisi `Relayed Transport Address`'e veri gönderdiğinde, buraya yönlendirilir.
- `RELAYED-ADDRESS` - Bu, diğer istemcilere verdiğiniz adrestir. Birisi bu adrese bir paket gönderirse, TURN istemcisine aktarılır.
- `LIFETIME` - Bu TURN Allocation'ın ne kadar süre sonra yok edildiği. `Refresh` isteği göndererek yaşam süresini uzatabilirsiniz.

#### Permissions

Uzak bir host, onlar için bir permission oluşturana kadar `Relayed Transport Address`'inize gönderemez. Permission oluşturduğunuzda, TURN sunucusuna bu IP ve port'un gelen trafiği göndermeye izinli olduğunu söylüyorsunuz.

Uzak host'un size TURN sunucusuna göründüğü şekliyle IP ve port'u vermesi gerekir. Bu, TURN Sunucusuna bir `STUN Binding Request` göndermesi gerektiği anlamına gelir. Yaygın bir hata durumu, uzak host'un farklı bir sunucuya `STUN Binding Request` göndermesidir. Daha sonra sizden bu IP için permission oluşturmanızı isteyeceklerdir.

Diyelim ki `Address Dependent Mapping` arkasındaki bir host için permission oluşturmak istiyorsunuz. Farklı bir TURN sunucusundan `Mapped Address` üretirseniz, tüm gelen trafik düşürülecektir. Farklı bir host ile her iletişim kurduklarında yeni bir eşleme oluşturur. Permission'lar yenilenmezlerse 5 dakika sonra sona erer.

#### SendIndication/ChannelData

Bu iki mesaj TURN Client'ın uzak bir eşe mesaj göndermesi içindir.

SendIndication bağımsız bir mesajdır. İçinde göndermek istediğiniz veri ve kime göndermek istediğiniz vardır. Uzak bir eşe çok sayıda mesaj gönderiyorsanız bu savurgan olur. 1.000 mesaj gönderirseniz IP Adreslerini 1.000 kez tekrar edeceksiniz!

ChannelData veri göndermenize izin verir, ancak IP Adresini tekrar etmez. Bir IP ve port ile Channel oluşturursunuz. Daha sonra ChannelId ile gönderirsiniz ve IP ve port sunucu tarafında doldurulacaktır. Çok sayıda mesaj gönderiyorsanız bu daha iyi seçimdir.

#### Refreshing

Allocation'lar kendilerini otomatik olarak yok ederler. TURN Client bunları allocation oluştururken verilen `LIFETIME`'dan daha önce yenilemelidir.

### TURN Kullanımı

TURN Kullanımı iki formda var olur. Genellikle, bir eşiniz "TURN Client" görevi görür ve diğer taraf doğrudan iletişim kurar. Bazı durumlarda her iki tarafta da TURN kullanımınız olabilir, örneğin her iki istemci de UDP'yi bloke eden ağlarda olduğu ve bu nedenle ilgili TURN sunucularına bağlantı TCP üzerinden gerçekleştiği için.

Bu diyagramlar bunun nasıl görüneceğini açıklamaya yardımcı olur.

#### İletişim için Bir TURN Allocation

![One TURN allocation](../images/03-one-turn-allocation.png "One TURN allocation")

#### İletişim için İki TURN Allocation

![Two TURN allocations](../images/03-two-turn-allocations.png "Two TURN allocations")

## ICE

ICE (Etkileşimli Bağlantı Kurma) WebRTC'nin iki Ajanı nasıl bağladığıdır. [RFC 8445](https://tools.ietf.org/html/rfc8445)'te tanımlanır, bu WebRTC'den önce var olan başka bir teknolojidir! ICE bağlantı kurmak için bir protokoldür. İki eş arasındaki tüm olası yolları belirler ve sonra bağlı kaldığınızı garanti eder.

Bu yollar `Candidate Pairs` olarak bilinir, bu yerel ve uzak aktarım adresinin eşleştirilmesidir. STUN ve TURN'ün ICE ile devreye girdiği yer burasıdır. Bu adresler yerel IP Adresiniz artı port, `NAT mapping` veya `Relayed Transport Address` olabilir. Her taraf kullanmak istedikleri tüm adresleri toplar, bunları değiş tokuş eder ve sonra bağlanmaya çalışır!

İki ICE Ajanı bağlantı kurmak için ICE ping paketleri (veya resmi olarak connectivity checks adı verilen) kullanarak iletişim kurar. Bağlantı kurulduktan sonra, istedikleri herhangi bir veriyi gönderebilirler. Normal socket kullanmak gibi olacaktır. Bu kontroller STUN protokolünü kullanır.

### ICE Ajanı Oluşturma

Bir ICE Ajanı ya `Controlling` ya da `Controlled`'dır. `Controlling` Ajanı seçilen `Candidate Pair`'i belirleyen ajandır. Genellikle, teklifi gönderen eş controlling taraftır.

Her tarafın bir `user fragment` ve `password`'ü olmalıdır. Bu iki değer connectivity check'ler başlamadan önce değiş tokuş edilmelidir. `user fragment` düz metin olarak gönderilir ve birden fazla ICE Oturumunu demux etmek için yararlıdır.
`password` bir `MESSAGE-INTEGRITY` özniteliği oluşturmak için kullanılır. Her STUN paketinin sonunda, `password`'ü anahtar olarak kullanan tüm paketin hash'i olan bir öznitelik vardır. Bu paketi doğrulamak ve kurcalanmadığından emin olmak için kullanılır.

WebRTC için, tüm bu değerler önceki bölümde açıklandığı gibi `Session Description` aracılığıyla dağıtılır.

### Candidate Gathering

Şimdi ulaşılabilir olduğumuz tüm olası adresleri toplamamız gerekiyor. Bu adresler candidate olarak bilinir.

#### Host

Host candidate doğrudan yerel arayüzde dinler. Bu UDP veya TCP olabilir.

#### mDNS

mDNS candidate host candidate'e benzer, ancak IP adresi gizlenir. Diğer tarafa IP adresinizi bildirmek yerine, hostname olarak onlara bir UUID verirsiniz. Daha sonra multicast dinleyici kurarsınız ve yayınladığınız UUID'yi isteyen olursa yanıt verirsiniz.

Ajan ile aynı ağdaysanız, Multicast aracılığıyla birbirinizi bulabilirsiniz. Aynı ağda değilseniz, bağlanamayacaksınız (ağ yöneticisi ağı Multicast paketlerinin geçişine izin verecek şekilde açıkça yapılandırmadıkça).

Bu gizlilik amacıyla yararlıdır. Bir kullanıcı Host candidate ile WebRTC aracılığıyla yerel IP adresinizi öğrenebilir (size bağlanmaya çalışmadan bile), ancak mDNS candidate ile şimdi sadece rastgele bir UUID alırlar.

#### Server Reflexive

Server Reflexive candidate, STUN Sunucusuna `STUN Binding Request` yaparak oluşturulur.

`STUN Binding Response` aldığınızda, `XOR-MAPPED-ADDRESS` sizin Server Reflexive Candidate'ınızdır.

#### Peer Reflexive

Peer Reflexive candidate, uzak eş isteğinizi daha önce eşe bilinmeyen bir adresten aldığında oluşturulur. Alındığında, eş söz konusu adresi size geri bildirir (yansıtır). Eş isteğin sizin tarafınızdan gönderildiğini ve başka biri tarafından gönderilmediğini bilir çünkü ICE kimlik doğrulamalı bir protokoldür.

Bu yaygın olarak bir `Host Candidate`'in farklı alt ağda olan `Server Reflexive Candidate` ile iletişim kurması durumunda gerçekleşir ve bu yeni bir `NAT mapping` oluşturulmasına neden olur. Connectivity check'lerin aslında STUN paketleri olduğunu söylediğimizi hatırlayın? STUN yanıtının formatı doğal olarak eşin peer-reflexive adresi geri bildirmesine izin verir.

#### Relay

Relay Candidate, TURN Sunucusu kullanarak oluşturulur.

TURN Sunucusu ile ilk handshake'den sonra size bir `RELAYED-ADDRESS` verilir, bu sizin Relay Candidate'ınızdır.

### Connectivity Checks

Şimdi uzak ajanın `user fragment`, `password` ve candidate'larını biliyoruz. Artık bağlanmaya çalışabiliriz! Her candidate birbiriyle eşleştirilir. Her tarafta 3 candidate'ınız varsa, şimdi 9 candidate çiftiniz vardır.

Görsel olarak şöyle görünür:

![Connectivity checks](../images/03-connectivity-checks.png "Connectivity checks")

### Candidate Selection

Controlling ve Controlled Agent'lar her çift üzerinde trafik göndermeye başlar. Bu, bir Ajanın `Address Dependent Mapping` arkasında olması durumunda gereklidir, bu `Peer Reflexive Candidate` oluşturulmasına neden olacaktır.

Ağ trafiği gören her `Candidate Pair` daha sonra `Valid Candidate` çiftine terfi edilir. Controlling Agent daha sonra bir `Valid Candidate` çiftini alır ve onu aday gösterir. Bu `Nominated Pair` olur. Controlling ve Controlled Agent daha sonra bir tur daha çift yönlü iletişim denemeye çalışır. Bu başarılı olursa, `Nominated Pair` `Selected Candidate Pair` olur! Bu çift daha sonra oturumun geri kalanı için kullanılır.

### Restarts

`Selected Candidate Pair` herhangi bir nedenle çalışmayı durdurursa (NAT mapping süresi dolar, TURN Sunucusu çöker) ICE Ajanı `Failed` durumuna geçer. Her iki ajan da yeniden başlatılabilir ve tüm süreci baştan yapacaktır.
