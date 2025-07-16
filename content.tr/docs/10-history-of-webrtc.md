---
title: Tarihçe
type: docs
weight: 11
---

# Tarihçe

WebRTC öğrenirken geliştiriciler genellikle karmaşıklık nedeniyle hayal kırıklığı yaşarlar.
Mevcut projelerine alakasız WebRTC özelliklerini görür ve WebRTC'nin
daha basit olmasını dilerler. Sorun
herkesin farklı bir kullanım durumu setine sahip olmasıdır. Gerçek zamanlı iletişimin zengin
bir geçmişi vardır ve birçok farklı insan birçok farklı şey inşa eder.

Bu bölüm WebRTC'yi oluşturan protokollerin yazarlarıyla yapılan röportajları içerir.
Her protokolü inşa ederken yapılan tasarımlara dair içgörü verir ve
WebRTC'nin kendisi hakkında bir röportajla biter. Yazılımın
niyetlerini ve tasarımlarını anlarsanız onunla daha etkili sistemler inşa edebilirsiniz.

## RTP

RTP ve RTCP WebRTC için tüm medya aktarımını yöneten protokoldür.
Ocak 1996'da [RFC 1889](https://tools.ietf.org/html/rfc1889)'da tanımlandı.
Yazarlarından biri olan [Ron Frederick](https://github.com/ronf)'in bunu kendisinin anlatma
şansımız olduğu için çok şanslıyız. Ron yakın zamanda
RTP'yi bilgilendiren bir proje olan [Network Video tool](https://github.com/ronf/nv)'u GitHub'a yükledi.

### Kendi Sözleriyle

Ekim 1992'de, IP multicast tabanlı bir ağ video konferans aracı yazma
fikriyle Sun VideoPix çerçeve yakalayıcı kartıyla deneyler yapmaya başladım.
LBL'de geliştirilen bir ses konferans aracı olan "vat"ı model aldı,
çünkü kullanıcıların konferanslara katılması için benzer hafif oturum protokolü kullanıyordu,
burada sadece belirli bir multicast grubuna veri gönderiyordunuz ve diğer grup
üyelerinden gelen herhangi bir trafik için o grubu izliyordunuz.

Programın gerçekten başarılı olması için video verilerini ağa koymadan önce
sıkıştırması gerekiyordu. Hedefim yaklaşık 128 kbps'ye sığacak kabul edilebilir
görünümlü bir veri akışı yapmaktı, veya standart ev ISDN hattında mevcut
bant genişliği. Ayrıca bu bant genişliğinin yarısına sığan hala izlenebilir
bir şey üretmeyi umuyordum. Bu, çalıştığım belirli görüntü boyutu ve kare hızı
için yaklaşık 20 kat sıkıştırma faktörüne ihtiyacım olduğu anlamına geliyordu.
Bu sıkıştırmayı başardım ve kullandığım teknikler için patent başvurusunda bulundum,
daha sonra verildi, ancak bu tamamen farklı bir hikaye.

1993 yazının başında, San Francisco'daki Multimedia Computing and Networking
konferansında kendim yazıp "Network Video (nv)" diye adlandırdığım bu programı gösterdim.
Bu gösterim "vat"ın yaratıcısı Van Jacobson'dan iyi gözüktü
ve ondan bu proje üzerinde birlikte çalışmak isteyip istemediğimi sordu.
Elinden geldiğince bana yardım etmeyi kabul etti.

Van ile çalışırken öğrendiğim ilk şeylerden biri bu tür gerçek zamanlı uygulamalar
için yayın kontrolü ve kalite kontrolünün önemiydi. vat'ta yaptıkları şey
herkesin trafiğini dinlemekti ve eğer network tıkanıklığına dair işaretler görürlerse
transmisyon kalitelerini azaltırlardı.

nv için, bu birkaç şeyle gerçekleştirildi. İlk olarak, biz diğer gönderenlerden
gelen farklı veri hızlarını ölçtük. Network'e çok fazla trafik gönderdiğimizi
fark edersek, kare hızını ve kaliteyi azaltırdık. İkinci olarak, herhangi
bir alıcıya gönderenin kalitesini azaltmasını isteyebileceğini söylememize
izin veren "komutu gönder" mesajları gönderdik. Bunu, özellikle bant genişliği
gereksinimlerimizi kendi ağ kapasitesine uydurmak isteyen alıcılar için
yaptık.

nv, Mart 1993'te Sun'dan halka yayınlandı ve hızla çok popüler oldu.
Bu konuyla ilgili çok sayıda email aldığım hatırlıyorum. İnsanlar bunu
dünya çapında Mbone üzerinden üniversiteler arası video konferanslar için
kullanıyorlardı, ve birçok insan kendi video konferans araçlarını bu kod
üzerine inşa etti.

nv'de kullandığımız formatın artık RTP diye bilinen şeyin ilk versiyonu
olduğunu söyleyebilirim. Video verilerinin başında, kare hızı ve kalite
hakkında alıcılara bilgi veren küçük bir başlık vardı. Bu başlık ayrıca
gönderenin bir parçası olduğu farklı oturumları, hangi kullanıcıdan
geldiğini ve benzer şeyleri tanımlamaya yardımcı olacak alanlar içeriyordu.

Aslında başlık formatını tasarlarken, vat'ta kullanılan basit yaklaşımdan
sonra modellendirdi. Ancak, nv o zamanlar daha karmaşık bir medya türü
olduğundan daha fazla bilgiye ihtiyacı vardı. Daha sonra, RTP komitesinde
çalıştığımızda, nv'de kullandığımız format, daha sonra RTP'nin standardı
haline gelecek şeyin temelini oluşturdu.

Nitekim, nv'de kullandığımız format ile RTP v1 RFC'si arasında doğrudan
bir çizgi vardır. Bu o zamandan beri evrildi, ancak temel konseptler
aynı kalıyor.

Vat'ta Van'ın yaptığı işin gerçekten akıllıcaydı. Ağ tıkanıklığıyla
nasıl başa çıkılacağı konusunda öncü bir iş yaptı ve bu RTP ve daha sonra
RTCP'nin gelişiminde gerçekten önemliydi.

### Neden paket başına zaman damgası?

Bu günlerde, paket başına zaman damgası oldukça açık görünüyor,
ancak o zamanlar bunun böyle açık olup olmadığından emin değildim.
Ben bu işe başladığımda, çerçeveleri düşünce alışkanlığındaydım,
paketleri değil.

Her pakette zaman damgası bulunmasının nedenlerinden biri ses ve
video arasında yeterince senkronizasyon sağlayabilmekti. Bu,
özellikle genellikle çerçeveler arasında dağıtılan ve genellikle
düşük bir kare hızından dolayı çerçeveler arasında önemli miktarda
zaman olan video için önemliydi.

Diğer nedeni ise bant genişliği yönetimi içindi. Bir çerçeve içinde
farklı bölümlere farklı öncelikler atayabilsek, alıcıların network
koşulları kötüleştiğinde hangi paketleri düşüreceğini bilmelerine
izin verseydik yardımcı olacaktı. Bu, çerçeve düzeyinde değil paket
düzeyinde öncelik bilgilerine sahip olmayı gerektirdi.

### RTP/RTCP'nin geleceği

RTP, ilk oluşturulduğundan bu yana oldukça başarılı olduğunu düşünüyorum.
Bu, İnternet'teki gerçek zamanlı uygulamaların çoğunun temelini oluşturuyor
ve çok geniş bir alanda kullanılıyor.

RTP'nin en başarılı kısımlarından biri esnekliği olmuştur. Genelleştirilmiş
bir çerçeve olacak şekilde tasarlandı, bu da belirli medya türleri için
özelleştirilebileceği anlamına geliyordu. Bu, RTP'nin başlangıçta tasarlandığından
çok daha fazla uygulama alanında kullanılmasına izin verdi.

WebRTC ile ilgili özellikle heyecanlandıran şey, RTP'yi sadece nokta-nokta
konferans çağrıları için değil, çok daha karmaşık uygulamalar için de
kullanıyor olmasıdır. Bu benim başlangıçta hayal ettiğim türden kullanımın
ötesinde.

## ICE

ICE, internet bağlantısı kurma (Internet Connection Establishment) anlamına gelir.
ICE, WebRTC'nin NAT geçişi nasıl yaptığıdır. Birden fazla ağda NAT'ların arkasındaki
iki WebRTC ajanının birbirlerini nasıl bulduğudur.

ICE [RFC 8445](https://tools.ietf.org/html/rfc8445)'te tanımlanmıştır ve
[Jonathan Rosenberg](https://www.linkedin.com/in/jdrosen/) tarafından yazılmıştır.
İCANN'ın eski CTO'su ve şu anda [Five9](http://five9.com/)'un CTO'sudur.

### Kendi Sözleriyle

Ben şirketimde video konferans teknolojileri üzerinde çalışıyordum.
1999 gibi erken bir tarihte enterprise video konferans sistemleri
inşa ediyorduk. Bu sistemler, ağ içinde iki nokta arasında çağrılar
yapmak için tasarlanmıştı.

Sorun, kullanıcılar bu sistemleri iş yerlerinin dışında kullanmaya
başladığında ortaya çıktı. Evdeki kullanıcıların çoğu NAT'ın arkasındaydı
ve bizim sistemimiz çalışmıyordu. O zamanlar NAT geçişi bu kadar yaygın
değildi - aslında hiç yoktu.

Insanların internet üzerinden ses ve video konferansı yapabilmesi için
NAT geçişi problemini çözmemiz gerekiyordu. Bu problemin birçok farklı
parçası vardı: NAT tespiti, NAT tipi belirleme, NAT geçişi, ve bağlantı
kurma.

Bunu çözmek için birkaç farklı yöntem denedik. Bunlardan biri UPnP'yi
kullanmaktı, ancak bu yeterince yaygın değildi. Diğeri de STUN ve TURN
kullanmaktı, ancak bunlar her durumda çalışmıyordu.

ICE, tüm bu farklı yöntemleri birleştirmeye çalışan bir yaklaşımdı.
Temel fikir şuydu: bağlantı kurmaya çalışırken mümkün olan tüm yöntemleri
deneyin ve hangisi çalışırsa onu kullanın.

ICE'ın ilk versiyonu oldukça karmaşıktı. Birçok farklı bağlantı yöntemini
koordine etmeye çalışıyordu ve implementasyon oldukça zordu. Zamanla
protokol basitleşti ve daha pratik hale geldi.

ICE'ın en büyük katkısı, farklı NAT geçiş yöntemlerini standart bir
şekilde birleştirmesi oldu. Bu, geliştiricilerin her durum için özel
çözümler yazmak zorunda kalmaması anlamına geldi.

ICE bugün WebRTC'nin temel bir parçası. NAT'ların arkasındaki aygıtların
birbirleriyle güvenilir bir şekilde bağlantı kurmasını sağlıyor. Bu olmadan,
WebRTC bugünkü kadar yaygın bir şekilde kullanılamazdı.

### ICE'ın geleceği

ICE teknolojisi olarak oldukça olgun. Temel protokol iyi çalışıyor ve
büyük değişikliklere ihtiyaç duymuyoru. Gelecekteki gelişmelerin çoğu
performans optimizasyonları ve belirli kullanım durumları için iyileştirmeler
olacak.

Özellikle mobile cihazlar için pil ömrünü iyileştirme üzerine çok çalışma
yapılıyor. ICE süreçlerinin daha verimli olması ve daha az enerji tüketmesi
için yöntemler araştırılıyor.

## mDNS

mDNS (multicast DNS), WebRTC'nin yerel ağda eş keşfi için kullandığı
teknolojilerden biridir. Bu, WebRTC ajanlarının aynı yerel ağdaki
diğer ajanları bulmasına olanak tanır.

mDNS, [RFC 6763](https://tools.ietf.org/html/rfc6763)'te tanımlanmıştır
ve Apple tarafından geliştirilmiştir. Bonjour teknolojisinin bir parçasıdır.

### Neden mDNS?

WebRTC'de gizlilik giderek daha önemli hale geldi. Kullanıcıların IP
adreslerinin gereksiz yere ifşa edilmemesi önemli. mDNS, yerel ağdaki
eş keşfi için IP adreslerini ifşa etmeyen bir yöntem sağlar.

Geleneksel ICE sürecinde, WebRTC ajanları kendi IP adreslerini ICE
adayları olarak paylaşır. Bu, kullanıcının ağ topolojisi hakkında
bilgi verebilir ve gizlilik endişeleri yaratabilir.

mDNS kullanarak, WebRTC ajanları gerçek IP adresleri yerine
.local etki alanı adları kullanabilir. Bu adlar sadece yerel ağ
içinde çözülebilir ve dış ağlara bilgi sızdırmaz.

### mDNS'in WebRTC'deki kullanımı

WebRTC'de mDNS öncelikle aynı yerel ağdaki eşler arasında bağlantı
kurmak için kullanılır. Bu özellikle aynı WiFi ağındaki cihazlar
arasında doğrudan bağlantı kurmak için yararlıdır.

mDNS kullanımı, WebRTC'nin gizlilik özelliklerini artırırken aynı
zamanda yerel ağ performansını da iyileştirir. Yerel bağlantılar
genellikle internet üzerinden gelen bağlantılardan daha hızlı ve
daha düşük gecikmeye sahiptir.

## WebRTC kendisi

WebRTC'nin hikayesini anlatmak için [Justin Uberti](https://www.linkedin.com/in/juberti/)'yi
davet ettik. Justin Google'da WebRTC'nin temel kurucularından biriydi ve
standardizasyon sürecinin büyük bir parçasıydı. Şu anda
[Clubhouse](https://www.clubhouse.com/)'da çalışıyor.

### Kendi Sözleriyle

WebRTC'ye giden yol uzundu. 2003'te Google'a katıldığımda, şirket
gerçek zamanlı iletişim alanında henüz aktif değildi. Ancak zaman
geçtikçe, bu alanın gelecekte önemli olacağını gördük.

2005 civarında Google Talk'ı piyasaya sürdük. Bu bizim ilk gerçek
zamanlı iletişim ürünümüzdü ve Jabber/XMPP tabanlıydı. Bu ürünü
geliştirirken, mevcut teknolojilerin sınırlarını gördük.

O zamanlar, web tarayıcılarında gerçek zamanlı iletişim yapmak çok zordu.
Flash veya Java gibi eklentiler kullanmanız gerekiyordu. Bu hem güvenlik
hem de kullanılabilirlik açısından sorunluydu.

2009'da HTML5 ortaya çıktığında, web'in yerel olarak gerçek zamanlı
iletişimi destekleyebileceği fikri daha gerçekçi hale geldi. Ancak
bu için browserlara önemli yeni API'ler eklenmesi gerekiyordu.

### Neden browser-tabanlı?

Browser-tabanlı gerçek zamanlı iletişim yapmanın birçok avantajı vardı:

Öncelikle, platform bağımsızlığı. Aynı kod Windows, Mac, Linux ve
mobile platformlarda çalışabilirdi. Bu, geliştiriciler için büyük
bir kolaylıktı.

İkincisi, güvenlik. Browser'lar zaten güvenlik odaklı tasarlanmıştı
ve sandbox modeli vardı. Bu, gerçek zamanlı iletişimin de güvenli
olmasını sağlardı.

Üçüncüsü, kolay dağıtım. Kullanıcılar herhangi bir yazılım indirmek
zorunda kalmadan uygulamaları kullanabilirdi. Bu, adapsiyon için
kritikti.

### Teknik zorluklar

WebRTC'yi geliştirirken karşılaştığımız birçok teknik zorluk vardı:

NAT geçişi büyük bir sorundu. Internet'teki cihazların çoğu NAT'ların
arkasındaydı ve birbirleriyle doğrudan iletişim kuramazlardı. ICE
protokolü bu sorunu çözmek için geliştirildi.

Codec seçimi başka bir zorlukhti. Farklı platformlar farklı audio/video
codec'lerini destekliyordu. WebRTC için ortak bir set belirlemek
zordu.

Echo cancellation ve noise reduction gibi ses işleme algoritmaları
da zordu. Bunların web browserlarında gerçek zamanlı çalışması
gerekiyordu.

### Açık kaynak yaklaşımı

WebRTC'yi açık kaynak yapmak stratejik bir karardı. Bunun birkaç
nedeni vardı:

İlk olarak, standardizasyon. Açık kaynak olmayan bir teknoloji
internet standardı olmaya uygun değildi.

İkincisi, güven. Güvenlik açısından kritik bir teknoloji için
kod şeffaflığı önemliydi.

Üçüncüsü, ekosistem. Geniş bir geliştirici ekosistemi yaratmak
için açık kaynak gerekliyde.

### NPAPI'den uzaklaşma

NPAPI'den uzaklaşma büyük bir odak noktası haline geldi. Bu güçlü
bir API'ydi, ancak büyük güvenlik sonuçları vardı. Chrome kullanıcıları
güvende tutmak için sandbox tasarımı kullanır. Potansiyel olarak
güvenli olmayan işlemler farklı süreçlerde çalışır. Bir şeyler
ters gitse bile, saldırgan hala kullanıcı verilerine erişime sahip olmaz.

### WebRTC'nin doğuşu

Benim için WebRTC birkaç motivasyonla doğdu. Bunlar birleşerek
bu çabayı doğurdu.

RTC deneyimleri inşa etmek bu kadar zor olmamalıydı. Çok fazla çaba
farklı geliştiricilerin aynı şeyi yeniden uygulamasıyla harcandı.
Bu sinir bozucu entegrasyon problemlerini bir kez çözmeli ve diğer
şeylere odaklanmalıydık.

İnsan iletişimi engellenmemeli ve açık olmalıydı. Metin ve HTML'nin
açık olması tamam da, sesim ve gerçek zamanlı görüntümün açık olmaması
nasıl kabul edilebilir?

Güvenlik bir önceliktir. NPAPI kullanmak kullanıcılar için en iyisi
değildi. Bu aynı zamanda varsayılan olarak güvenli bir protokol
yapma şansıydı.

WebRTC'yi gerçekleştirmek için Google daha önce kullandığımız bileşenleri
satın aldı ve Açık Kaynak yaptı. Video teknolojisi için
[On2](https://en.wikipedia.org/wiki/On2_Technologies) satın alındı ve
RTC teknolojisi için
[Global IP Solutions](https://en.wikipedia.org/wiki/Global_IP_Solutions).
GIPS'i satın alma çabasının sorumlusu bendim. Bunları birleştirme
ve browser içinde ve dışında kullanımı kolay hale getirme işine
koyulduk.

### Standardizasyon

WebRTC'yi standardize etmek gerçekten yapmak istediğimiz bir şeydi,
ancak daha önce yaptığım bir şey değildi, yakın ekibimizden hiç
kimse de yapmamıştı. Bunun için Google'da Harald Alvestrand'a
sahip olmak gerçekten şanslıydık. IETF'te zaten kapsamlı çalışmalar
yapmıştı ve WebRTC standardizasyon sürecini başlattı.

2010 yazında Maastricht'te gayri resmi bir öğle yemeği planlandı.
Birçok şirketten geliştiriciler WebRTC'nin ne olması gerektiğini
tartışmak için bir araya geldi. Öğle yemeğinde Google, Cisco,
Ericsson, Skype, Mozilla, Linden Labs ve daha fazlasından mühendisler
vardı. Tam katılım ve sunucu slaytlarını
[rtc-web.alvestrand.com](http://rtc-web.alvestrand.com)'da bulabilirsiniz.

Skype ayrıca IETF'te Opus ile yaptıkları çalışma nedeniyle harika
rehberlik sağladı.

### Devlerin omuzlarında durmak

IETF'te çalışırken sizden önce gelen çalışmaları genişletiyorsunuz.
WebRTC ile çok fazla şeyin mevcut olması şansımıza oldu. Her problemi
üstlenmek zorunda değildik çünkü zaten çözülmüşlerdi. Önceden var olan
teknolojiyi sevmiyorsanız bu sinir bozucu olabilir. Mevcut çalışmayı
yok saymak için oldukça büyük bir nedene sahip olmanız gerekir, bu
yüzden kendi başınıza yapmak bir seçenek değil.

Ayrıca sinyalleşme gibi şeyleri yeniden standardize etmeye bilinçli
olarak girişmedik. Bu zaten SIP ve diğer IETF dışı çabalarla çözülmüştü
ve çok politik olabileceği hissiyatı vardı. Sonunda bu alana
eklecek çok fazla değer olmadığı hissiyatı vardı.

Standardizasyon konusunda Justin ve Harald kadar dahil olmadım, ancak
yaptığım süreyi sevdim. Kullanıcılar için bir şeyler inşa etmeye
geri dönme konusunda daha heyecanlıydım.

### Gelecek

WebRTC bugün harika bir yerde. Birçok yinelemeli değişiklik oluyor,
ancak özellikle üzerinde çalıştığım bir şey yok.

İletişim için bulut bilişimin yapabilecekleri konusunda en çok
heyecanlıyım. Gelişmiş algoritmalar kullanarak bir çağrıdan arka
plan gürültüsünü kaldırabilir ve daha önce mümkün olmayan yerlerde
iletişimi mümkün kılabiliyoruz. Ayrıca WebRTC'nin iletişimin çok
ötesine geçtiğini görüyoruz... 9 yıl sonra bulut tabanlı oyunları
destekleyeceğini kim bilebilirdi? Bunların hiçbiri WebRTC'nin
temeli olmadan mümkün olmazdı.
