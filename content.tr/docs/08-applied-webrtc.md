---
title: Uygulamalı WebRTC
type: docs
weight: 9
---

# Uygulamalı WebRTC

Artık WebRTC'nin nasıl çalıştığını bildiğinize göre, onunla geliştirme zamanı! Bu bölüm insanların
WebRTC ile ne geliştirdiğini ve nasıl geliştirdiğini araştırıyor. WebRTC ile olan tüm ilginç gelişmeleri öğreneceksiniz. WebRTC'nin gücü bir bedelle gelir. Üretim kalitesi WebRTC hizmetleri geliştirmek
zorludur. Bu bölüm size bu zorlukları karşılaşmadan önce açıklamaya çalışacaktır.

## Kullanım Durumuna Göre

Birçoğu WebRTC'nin sadece web tarayıcısında konferans için bir teknoloji olduğunu düşünür. Ama çok daha fazlasıdır!
WebRTC geniş bir uygulama yelpazesinde kullanılır. Yeni kullanım durumları sürekli ortaya çıkıyor. Bu bölümde bazı yaygın olanları ve WebRTC'nin bunları nasıl devrimleştirdiğini listeleyeceğiz.

### Konferans

Konferans WebRTC'nin orijinal kullanım durumudur. Protokol, tarayıcıda başka hiçbir protokolün sunmadığı birkaç gerekli özellik içerir. WebSocket'lerle bir konferans sistemi geliştirebilirsiniz ve optimal koşullarda çalışabilir. Gerçek dünya ağ koşullarında dağıtılabilecek bir şey istiyorsanız, WebRTC en iyi seçenektir.

WebRTC medya için tıkanıklık kontrolü ve uyarlanabilir bit hızı sağlar. Ağın koşulları değiştikçe, kullanıcılar yine de mümkün olan en iyi deneyimi alacaktır. Geliştiricilerin bu koşulları ölçmek için herhangi bir ek kod yazması da gerekmez.

Katılımcılar birden fazla akış gönderip alabilir. Ayrıca çağrı sırasında istediği zaman bu akışları ekleyip çıkarabilirler. Codec'ler de müzakere edilir. Tüm bu işlevsellik tarayıcı tarafından sağlanır, geliştirici tarafından özel kod yazılması gerekmez.

Konferans ayrıca veri kanallarından da yararlanır. Kullanıcılar metadata gönderebilir veya belge paylaşabilir. Güvenilirlikten çok performansa ihtiyacınız varsa birden fazla akış oluşturabilir ve bunları yapılandırabilirsiniz.

### Yayıncılık

WebRTC kullanan yayın alanında birçok yeni proje ortaya çıkmaya başladı. Protokol hem medya yayıncısı hem de tüketicisi için çok şey sunuyor.

WebRTC'nin tarayıcıda olması kullanıcıların video yayınlamasını kolaylaştırır. Kullanıcıların yeni bir istemci indirme gereksinimini ortadan kaldırır.
Web tarayıcısına sahip herhangi bir platform video yayınlayabilir. Yayıncılar daha sonra birden fazla parça gönderebilir ve bunları istediği zaman değiştirebilir veya kaldırabilir. Bu, bağlantı başına sadece bir ses veya bir video parçasına izin veren eski protokollere göre büyük bir gelişmedir.

WebRTC geliştiricilere gecikme ve kalite ödünleşimleri üzerinde daha fazla kontrol verir. Gecikmenin asla belirli bir eşiği aşmaması daha önemliyse ve bazı dekodlama hatalarını tolere etmeye istekliyseniz. Görüntüleyiciyi medyayı gelir gelmez oynatacak şekilde yapılandırabilirsiniz. TCP üzerinden çalışan diğer protokollerle bu o kadar kolay değildir. Tarayıcıda veri isteyebilirsiniz ve o kadar.

### Uzaktan Erişim

Uzaktan Erişim, WebRTC aracılığıyla başka bir bilgisayara uzaktan erişmektir. Uzak ana makinenin tam kontrolüne sahip olabilir veya belki sadece tek bir uygulamaya. Bu, yerel donanım yapamadığında hesaplama açısından pahalı görevleri çalıştırmak için harikadır. Yeni bir video oyunu veya CAD yazılımı çalıştırmak gibi. WebRTC alanı üç şekilde devrimleştirebildi.

WebRTC, dünya routable olmayan bir ana makineye uzaktan erişmek için kullanılabilir. NAT Geçişi ile sadece STUN aracılığıyla erişilebilen bir bilgisayara erişebilirsiniz. Bu güvenlik ve gizlilik için harikadır. Kullanıcılarınızın videoyu bir girdi veya "jump box" üzerinden yönlendirmesi gerekmez. NAT Geçişi ayrıca dağıtımları kolaylaştırır. Önceden port yönlendirme veya statik IP kurma konusunda endişelenmenize gerek yok.

Veri kanalları da bu senaryoda gerçekten güçlüdür. Sadece en son verinin kabul edilecek şekilde yapılandırılabilirler. TCP ile Head-of-line blocking ile karşılaşma riski yaşarsınız. Eski bir fare tıklaması veya tuş basımı geç gelebilir ve sonraki olanların kabul edilmesini engelleyebilir.
WebRTC'nin veri kanalları bunu ele almak için tasarlanmıştır ve kayıp paketleri yeniden göndermeyecek şekilde yapılandırılabilir. Ayrıca geri basıncı ölçebilir ve ağınızın desteklediğinden fazla veri göndermediğinizden emin olabilirsiniz.

WebRTC'nin tarayıcıda mevcut olması büyük bir yaşam kalitesi gelişimi olmuştur. Oturumu başlatmak için özel bir istemci indirmeniz gerekmez. Giderek daha fazla istemci WebRTC ile birlikte geliyor, akıllı TV'ler artık tam web tarayıcıları alıyor.

### Dosya Paylaşımı ve Sansür Aşma

Dosya Paylaşımı ve Sansür Aşma dramatik olarak farklı problemlerdir. Ancak WebRTC her ikisi için de aynı problemleri çözer. Her ikisini de kolayca erişilebilir hale getirir ve engellenmesi daha zor hale getirir.

WebRTC'nin çözdüğü ilk problem istemciyi almaktır. Bir dosya paylaşım ağına katılmak istiyorsanız, istemciyi indirmeniz gerekir. Ağ dağıtılmış olsa bile yine de önce istemciyi almanız gerekir. Kısıtlı bir ağda indirme genellikle engellenecektir. İndirebilseniz bile kullanıcı istemciyi kurup çalıştıramayabilir. WebRTC her web tarayıcısında zaten mevcut olduğu için kolayca erişilebilir.

WebRTC'nin çözdüğü ikinci problem trafiğinizin engellenmesidir. Sadece dosya paylaşımı veya sansür aşma için bir protokol kullanırsanız engellenmesi çok daha kolaydır. WebRTC genel amaçlı bir protokol olduğundan, onu engellemek herkesi etkiler. WebRTC'yi engellemek ağın diğer kullanıcılarının konferans görüşmelerine katılmasını engelleyebilir.

### Nesnelerin İnterneti

Nesnelerin İnterneti (IoT) birkaç farklı kullanım durumunu kapsar. Birçoğu için bu ağa bağlı güvenlik kameraları anlamına gelir. WebRTC kullanarak videoyu telefonunuz veya tarayıcı gibi başka bir WebRTC eşine aktarabilirsiniz. Başka bir kullanım durumu cihazların bağlanıp sensör verilerini değiş tokuş etmesidir. LAN'ınızdaki iki cihazın iklim, gürültü veya ışık okumalarını değiş tokuş etmesini sağlayabilirsiniz.

WebRTC'nin burada eski video akış protokollerine göre büyük bir gizlilik avantajı vardır. WebRTC P2P bağlantısını desteklediğinden kamera videoyu doğrudan tarayıcınıza gönderebilir. Videonuzun 3. taraf sunucuya gönderilmesi için hiçbir neden yoktur. Video şifreli olsa bile, saldırgan çağrının metadata'sından varsayımlarda bulunabilir.

Birlikte çalışabilirlik IoT alanı için başka bir avantajdır. WebRTC birçok farklı dilde mevcuttur; C#, C++, C, Go, Java, Python, Rust ve TypeScript. Bu sizin için en iyi işleyen dili kullanabileceğiniz anlamına gelir. Ayrıca istemcilerinizi bağlayabilmek için özel protokollere veya formatlara yönelmenize gerek yoktur.

### Medya Protokol Köprüleme

Mevcut donanımınız ve yazılımınız video üretiyor, ancak henüz yükseltemiyor. Kullanıcıların video izlemek için özel bir istemci indirmesini beklemek sinir bozucudur. Cevap bir WebRTC köprüsü çalıştırmaktır. Köprü iki protokol arasında çeviri yapar böylece kullanıcılar eski kurulumunuzla tarayıcıyı kullanabilir.

Geliştiricilerin köprülediği formatların çoğu WebRTC ile aynı protokolleri kullanır. SIP yaygın olarak WebRTC aracılığıyla açığa çıkarılır ve kullanıcıların tarayıcılarından telefon aramaları yapmalarına izin verir. RTSP birçok eski güvenlik kamerasında kullanılır. Her ikisi de aynı temel protokolleri (RTP ve SDP) kullanır bu yüzden çalıştırması hesaplama açısından ucuzdur. Köprü sadece WebRTC'ye özgü şeyleri eklemek veya çıkarmak için gereklidir.

### Veri Protokol Köprüleme

Bir web tarayıcısı sadece kısıtlı bir protokol setini konuşabilir. HTTP, WebSocket'ler, WebRTC ve QUIC kullanabilirsiniz. Başka bir şeye bağlanmak istiyorsanız, bir protokol köprüsü kullanmanız gerekir. Protokol köprüsü yabancı trafiği tarayıcının erişebileceği bir şeye dönüştüren bir sunucudur. Popüler bir örnek tarayıcınızdan SSH kullanarak bir sunucuya erişmektir. WebRTC'nin veri kanalları rakiplerine göre iki avantaja sahiptir.

WebRTC'nin veri kanalları güvenilmez ve sırasız teslimat sağlar. Düşük gecikmenin kritik olduğu durumlarda bu gereklidir. Yeni verilerin eski veriler tarafından engellenmesini istemezsiniz, bu head-of-line blocking olarak bilinir. Çok oyunculu bir First-person shooter oynadığınızı hayal edin. Oyuncunun iki saniye önce nerede olduğunu gerçekten umursayor musunuz? Bu veri zamanında gelmediysе, göndermeye devam etmenin anlamı yoktur. Güvenilmez ve sırasız teslimat verileri gelir gelmez kullanmanıza izin verir.

Veri kanalları ayrıca geri bildirim basıncı sağlar. Bu size bağlantınızın destekleyebileceğinden daha hızlı veri gönderip göndermediğinizi söyler. Bu durumda iki seçeneğiniz vardır. Veri kanalı verileri tamponlayacak ve geç teslim edecek şekilde yapılandırılabilir veya gerçek zamanda gelmemiş verileri düşürebilirsiniz.

### Teleoperasyon

Teleoperasyon WebRTC veri kanalları aracılığıyla bir cihazı uzaktan kontrol etme ve videoyu RTP aracılığıyla geri gönderme eylemidir. Geliştiriciler bugün WebRTC aracılığıyla arabaları uzaktan kullanıyor! Bu inşaat sahalarında robotları kontrol etmek ve paket teslim etmek için kullanılıyor. Bu problemler için WebRTC kullanmak iki nedenden dolayı mantıklıdır.

WebRTC'nin yaygınlığı kullanıcılara kontrol vermeyi kolaylaştırır. Kullanıcının ihtiyacı olan tek şey bir web tarayıcısı ve bir girdi cihazıdır. Tarayıcılar joystick ve gamepad'lerden girdi almayı bile destekler. WebRTC kullanıcının cihazına ek istemci kurma ihtiyacını tamamen ortadan kaldırır.

### Dağıtılmış CDN

Dağıtılmış CDN'ler dosya paylaşımının bir alt kümesidir. Dağıtılan dosyalar bunun yerine CDN operatörü tarafından yapılandırılır. Kullanıcılar CDN ağına katıldıklarında izin verilen dosyaları indirebilir ve paylaşabilirler. Kullanıcılar dosya paylaşımı ile aynı tüm faydaları alır.

Bu CDN'ler kötü dış bağlantıya sahip ancak harika LAN bağlantısına sahip bir ofisteyken harika çalışır. Bir kullanıcının video indirmesini ve sonra herkesle paylaşmasını sağlayabilirsiniz. Herkes aynı dosyayı dış ağ üzerinden almaya çalışmadığından, aktarım daha hızlı tamamlanacaktır.

## WebRTC Topolojileri

WebRTC iki aracıyı bağlamaya yönelik bir protokoldür, peki geliştiriciler aynı anda yüzlerce insanı nasıl bağlıyor? Bunu yapmanın birkaç farklı yolu vardır ve hepsinin artıları ve eksileri vardır. Bu çözümler geniş olarak iki kategoriye ayrılır; Eşten-Eşe veya İstemci/Sunucu. WebRTC'nin esnekliği her ikisini de yaratmamıza olanak tanır.

### Bire-Bir

Bire-Bir WebRTC ile kullanacağınız ilk bağlantı türüdür. İki WebRTC Aracısını doğrudan bağlarsınız ve çift yönlü medya ve veri gönderebilirler.

![Bire-Bir](../images/08-one-to-one.png "Bire-Bir")

### Tam Mesh

Tam Mesh, bire-bir modelin mantıksal uzantısıdır. Her WebRTC Aracısı diğer tüm WebRTC Aracılarıyla doğrudan bağlantı kurar. Büyük bir çok noktaya yayında her üye diğer tüm üyelere doğrudan gönderir.

![Tam Mesh](../images/08-full-mesh.png "Tam Mesh")

Tam Mesh avantajları şunlardır:

- **Minimum Gecikme** - Medya direkt olarak gönderilir, hiçbir aracı sunucu yoktur.
- **Gelişmiş Gizlilik** - Medya sunuculardan geçmez.

Tam Mesh dezavantajları şunlardır:

- **Sınırlı Ölçeklendirme** - Her bir eş, oturumdaki her bir diğer eş için medya kodlaması ve karşıya yükleme yapmalıdır.

Tam Mesh genellikle 4 kişiden az olan küçük konferanslar için kullanılır.

### Hibrit Mesh

Hibrit Mesh, Tam Mesh ile aynı teknolojide çalışır ancak her eş her eşle bağlanmaz. Bu tasarım medya kalitesini artırmak için de kullanılabilir. Yüksek bant genişliğine sahip olmayan eşler düşük kalite akışı sağlayabilir.

![Hibrit Mesh](../images/08-hybrid-mesh.png "Hibrit Mesh")

Hibrit Mesh avantajları şunlardır:

- **Konfigürasyona uygun ölçeklendirme** - Ağın karmaşıklığını kontrol edebilirsiniz.
- **Gelişmiş Gizlilik** - Medya sunuculardan geçmez.

Hibrit Mesh dezavantajları şunlardır:

- **Karmaşık sinyalleşme** - Konfigürasyonunuz ne kadar karmaşık olursa karar vermeniz o kadar zor olur.

### Seçici Yönlendirme Birimi

Seçici Yönlendirme Birimi (SFU), her eşin kendi medyasını merkezi sunucuya gönderdiği ve daha sonra sunucunun her eşe hangi medya akışını alacağını belirlediği bir topolojidir. Bu tipik olarak her eş için birden fazla kodlama sağlanarak (simulcast) ve her bir alıcının tercihine/yeteneğine göre en uygun kodlama seçilerek yapılır.

![SFU](../images/08-sfu.png "SFU")

SFU avantajları şunlardır:

- **Verimli Bant Genişliği Kullanımı** - Her eş medyasını yalnızca bir kez karşıya yükler.
- **Heterojen İstemci Desteği** - SFU her alıcı için optimal medya akışını seçebilir.
- **Gelişmiş Gizlilik** - Medya sunucu tarafından incelenmez yalnızca yönlendirilir.

SFU dezavantajları şunlardır:

- **Daha Fazla Gecikme** - Medya artık peer-to-peer değil, bir sunucu üzerinden geçiyor.

### Çok Nokta Konferans Birimi

Çok Nokta Konferans Birimi (MCU), tüm eşlerin kendi medyasını merkezi sunucuya gönderdiği ve daha sonra sunucunun tüm akışları tek bir medya akışında birleştirdiği topolojidir. Her katılımcı sadece bu karışık medya akışını alır.

![MCU](../images/08-mcu.png "MCU")

MCU avantajları şunlardır:

- **Verimli İndirme Bant Genişliği** - Her eş sadece tek bir video alır.
- **Heterojen İstemci Desteği** - MCU'nun hedeflediği düşük güçlü cihazları destekleyebilir.

MCU dezavantajları şunlardır:

- **Kayıplı İşlem** - Çünkü medya yeniden kodlanıyor, orijinal kalitesi kaybediliyor.
- **Artan Gecikme** - Medya işlem için zaman alır.
- **Gizlilik Yok** - Medya MCU tarafından incelenir ve işlenir.

Bu CDN'ler zayıf dış bağlantıya sahip ancak harika LAN bağlantısına sahip bir ofisteyken harika çalışır. Bir kullanıcının video indirmesini ve daha sonra herkesle paylaşmasını sağlayabilirsiniz. Herkes aynı dosyayı dış ağ üzerinden almaya çalışmadığından, aktarım daha hızlı tamamlanacaktır.

## WebRTC Topolojileri

WebRTC iki ajanı bağlamak için bir protokoldür, peki geliştiriciler aynı anda yüzlerce kişiyi nasıl bağlıyor? Bunu yapmanın birkaç farklı yolu vardır ve hepsinin artıları ve eksileri vardır. Bu çözümler genel olarak iki kategoriye ayrılır; Eşten-Eşe veya İstemci/Sunucu. WebRTC'nin esnekliği her ikisini de oluşturmamıza izin verir.

### Birden-Bire

Birden-Bire WebRTC ile kullanacağınız ilk bağlantı türüdür. İki WebRTC Ajanını doğrudan bağlarsınız ve çift yönlü medya ve veri gönderebilirler.
Bağlantı şöyle görünür.

![Birden-Bire](../images/08-one-to-one.png "Birden-Bire")

### Tam Mesh

Tam mesh bir konferans görüşmesi veya çok oyunculu oyun geliştirmek istiyorsanız cevaptır. Bu topolojide her kullanıcı doğrudan diğer her kullanıcıyla bağlantı kurar. Bu uygulamanızı geliştirmenize izin verir, ancak bazı dezavantajları da vardır.

Tam Mesh topolojisinde her kullanıcı doğrudan bağlıdır. Bu, çağrının her üyesi için bağımsız olarak video kodlamanız ve yüklemeniz gerektiği anlamına gelir.
Her bağlantı arasındaki ağ koşulları farklı olacaktır, bu yüzden aynı videoyu yeniden kullanamazsınız. Bu dağıtımlarda hata işleme de zordur. Tam bağlantıyı mı kaybettiğinizi yoksa sadece bir uzak eşle bağlantıyı mı kaybettiğinizi dikkatli bir şekilde değerlendirmeniz gerekir.

Bu endişeler nedeniyle, Tam Mesh en iyi küçük gruplar için kullanılır. Daha büyük herhangi bir şey için istemci/sunucu topolojisi en iyisidir.

![Tam mesh](../images/08-full-mesh.png "Tam mesh")

### Hibrit Mesh

Hibrit Mesh, Tam Mesh'in bazı sorunlarını hafifletebilen Tam Mesh'e bir alternatiftir. Hibrit Mesh'te her kullanıcı arasında bağlantı kurulmaz. Bunun yerine medya ağdaki eşler aracılığıyla aktarılır. Bu medya yaratıcısının medyayı dağıtmak için o kadar fazla bant genişliği kullanması gerekmediği anlamına gelir.

Bunun bazı dezavantajları vardır. Bu kurulumda medyanın orijinal yaratıcısının videosunun kime gönderildiği veya başarıyla ulaşıp ulaşmadığı hakkında hiçbir fikri yoktur. Ayrıca Hibrit Mesh ağınızdaki her atlama ile gecikme artışı yaşayacaksınız.

![Hibrit mesh](../images/08-hybrid-mesh.png "Hibrit mesh")

### Seçici Yönlendirme Birimi

Bir SFU (Seçici Yönlendirme Birimi) de Tam Mesh'in sorunlarını çözer, ancak tamamen farklı bir şekilde. SFU, P2P yerine istemci/sunucu topolojisi uygular.
Her WebRTC eşi SFU'ya bağlanır ve medyasını yükler. SFU daha sonra bu medyayı her bağlı istemciye iletir.

SFU ile her WebRTC Ajanının videosunu sadece bir kez kodlaması ve yüklemesi gerekir. Tüm görüntüleyicilere dağıtma yükü SFU'dadır.
SFU ile bağlantı da P2P'den çok daha kolaydır. Dünya routable adresinde bir SFU çalıştırabilirsiniz, bu da istemcilerin bağlanmasını çok daha kolay hale getirir.
NAT Eşlemeleri konusunda endişelenmenize gerek yoktur. Yine de SFU'nuzun TCP aracılığıyla erişilebilir olduğundan emin olmanız gerekir (ICE-TCP veya TURN aracılığıyla).

Basit bir SFU bir hafta sonunda yapılabilir. Her türlü istemciyi kaldırabilen iyi bir SFU geliştirmek hiç bitmez. Tıkanıklık Kontrolü, Hata Düzeltme ve Performansı ayarlamak hiç bitmeyen bir görevdir.

![Seçici Yönlendirme Birimi](../images/08-sfu.png "Seçici Yönlendirme Birimi")

### MCU

MCU (Çok Nokta Konferans Birimi) SFU gibi istemci/sunucu topolojisidir, ancak çıktı akışlarını birleştirir. Giden medyayı değiştirilmeden dağıtmak yerine bunları tek bir beslem olarak yeniden kodlar.

![Çok Nokta Konferans Birimi](../images/08-mcu.png "Çok Nokta Konferans Birimi")
