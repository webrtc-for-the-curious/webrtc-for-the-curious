---
title: Ne, Neden ve Nasıl
type: docs
weight: 2
---

# Ne, Neden ve Nasıl

## WebRTC Nedir?

WebRTC, Web Real-Time Communication'ın kısaltması olarak hem bir API hem de bir Protokoldür. WebRTC protokolü, iki WebRTC aracısının çift yönlü güvenli gerçek zamanlı iletişim müzakere etmesi için bir dizi kuraldan oluşur. WebRTC API'si ise geliştiricilerin WebRTC protokolünü kullanmasına olanak tanır. WebRTC API'si yalnızca JavaScript için belirtilmiştir.

Benzer bir ilişki HTTP ve Fetch API arasındaki ilişki olacaktır. WebRTC protokolü HTTP olurken, WebRTC API'si Fetch API olur.

WebRTC protokolü JavaScript dışında diğer API'ler ve dillerde de mevcuttur. WebRTC için sunucular ve domain-spesifik araçlar da bulabilirsiniz. Tüm bu uygulamalar WebRTC protokolünü kullanır böylece birbirleriyle etkileşim kurabilirler.

WebRTC protokolü IETF'de [rtcweb](https://datatracker.ietf.org/wg/rtcweb/documents/) çalışma grubunda sürdürülmektedir. WebRTC API'si ise W3C'de [webrtc](https://www.w3.org/TR/webrtc/) olarak belgelendirilmiştir.

## Neden WebRTC öğrenmeliyim?

WebRTC'nin size vereceği şeyler şunlardır:

- Açık standart
- Çoklu uygulamalar
- Tarayıcılarda mevcut
- Zorunlu şifreleme
- NAT Geçişi
- Mevcut teknolojinin yeniden kullanımı
- Tıkanıklık kontrolü
- Saniyenin altında gecikme

Bu liste kapsamlı değil, yolculuğunuz sırasında takdir edebileceğiniz şeylerin sadece bir örneği. Henüz tüm bu terimleri bilmiyorsanız endişelenmeyin, bu kitap bunları yol boyunca size öğretecek.

## WebRTC Protokolü diğer teknolojilerin bir koleksiyonudur

WebRTC Protokolü, açıklamak için tam bir kitap gerektirecek muazzam bir konudur. Ancak başlangıç olarak onu dört adıma ayırıyoruz.

1. Sinyalleme
2. Bağlanma
3. Güvenlik
4. İletişim

Bu adımlar sıralıdır, yani önceki adımın sonraki adımın başlaması için %100 başarılı olması gerekir.

WebRTC hakkındaki garip bir gerçek, her adımın aslında birçok başka protokolden oluşmasıdır! WebRTC yapmak için birçok mevcut teknolojiyi bir araya getiriyoruz. Bu anlamda WebRTC'yi, kendi başına yepyeni bir süreç olmaktan ziyade 2000'li yılların başlarına dayanan iyi anlaşılmış teknolojilerin bir kombinasyonu ve konfigürasyonu olarak düşünebilirsiniz.

Bu adımların her birinin özel bölümleri vardır, ancak önce bunları yüksek düzeyde anlamak yararlıdır. Birbirlerine bağımlı oldukları için, bu adımların her birinin amacını daha fazla açıklarken yardımcı olacaktır.

### Sinyalleme: WebRTC'de eşler birbirlerini nasıl bulur

Bir WebRTC Aracısı başladığında, kimle iletişim kuracağı veya ne hakkında iletişim kuracağı hakkında hiçbir fikri yoktur. _Sinyalleme_ adımı bu sorunu çözer! Sinyalleme, çağrıyı başlatmak için kullanılır ve iki bağımsız WebRTC aracısının iletişim kurmaya başlamasına olanak tanır.

Sinyalleme, SDP (Session Description Protocol) adı verilen mevcut, düz metin bir protokol kullanır. Her SDP mesajı anahtar/değer çiftlerinden oluşur ve "medya bölümleri" listesi içerir. İki WebRTC aracısının değiş tokuş ettiği SDP şu gibi detayları içerir:

- Aracının ulaşılabilir olduğu IP'ler ve Portlar (adaylar).
- Aracının göndermek istediği ses ve video parça sayısı.
- Her aracının desteklediği ses ve video codec'leri.
- Bağlanırken kullanılan değerler (`uFrag`/`uPwd`).
- Güvenlik sağlanırken kullanılan değerler (sertifika parmak izi).

Sinyallemenin tipik olarak "bant dışı" gerçekleştiğini not etmek çok önemlidir, bu da uygulamaların genellikle sinyalleme mesajlarını değiş tokuş etmek için WebRTC'nin kendisini kullanmadığı anlamına gelir. İki taraf arasında bir WebRTC bağlantısı başlatmadan önce başka bir iletişim kanalına ihtiyaç vardır. Kullanılan kanal türü WebRTC'nin endişesi değildir. Mesaj göndermek için uygun herhangi bir mimari, bağlanan eşler arasında SDP'leri aktarabilir ve birçok uygulama, uygun istemciler arasında SDP'lerin değiş tokuşunu kolaylaştırmak için mevcut altyapılarını (örneğin REST uç noktaları, WebSocket bağlantıları veya kimlik doğrulama proxy'leri) basitçe kullanacaktır.

### STUN/TURN ile Bağlanma ve NAT Geçişi

İki WebRTC aracısı SDP'leri değiş tokuş ettikten sonra, birbirlerine bağlanmaya çalışmak için yeterli bilgiye sahip olurlar. Bu bağlantıyı gerçekleştirmek için WebRTC, ICE (Interactive Connectivity Establishment) adı verilen başka bir yerleşik teknolojiyi kullanır.

ICE, WebRTC'den önce var olan ve merkezi bir sunucu olmadan iki aracı arasında doğrudan bağlantı kurulmasına olanak tanıyan bir protokoldür. Bu iki aracı aynı ağda veya dünyanın diğer ucunda olabilir.

ICE doğrudan bağlantı sağlar, ancak bağlanma sürecinin gerçek büyüsü 'NAT Geçişi' kavramını ve STUN/TURN Sunucularının kullanımını içerir. Daha sonra derinlemesine keşfedeceğimiz bu iki kavram, başka bir alt ağdaki ICE Aracısı ile iletişim kurmak için ihtiyacınız olan her şeydir.

İki aracı başarıyla bir ICE bağlantısı kurduğunda, WebRTC bir sonraki adıma geçer; aralarında ses, video ve veri paylaşımı için şifrelenmiş bir aktarım katmanı kurmak.

### DTLS ve SRTP ile aktarım katmanını güvenlik altına alma

Artık çift yönlü iletişimimiz (ICE aracılığıyla) olduğuna göre, iletişimimizi güvenli hale getirmemiz gerekiyor! Bu, yine WebRTC'den önce var olan iki protokol daha aracılığıyla yapılır; DTLS (Datagram Transport Layer Security) ve SRTP (Secure Real-Time Transport Protocol). İlk protokol olan DTLS, basitçe UDP üzerinden TLS'dir (TLS, HTTPS üzerinden iletişimi güvenli hale getirmek için kullanılan kriptografik protokoldür). İkinci protokol olan SRTP, RTP (Real-time Transport Protocol) veri paketlerinin şifrelenmesini sağlamak için kullanılır.

İlk olarak, WebRTC, ICE tarafından kurulan bağlantı üzerinden bir DTLS el sıkışması yaparak bağlanır. HTTPS'den farklı olarak, WebRTC sertifikalar için merkezi bir otorite kullanmaz. Sadece DTLS aracılığıyla değiş tokuş edilen sertifikanın, sinyalleme yoluyla paylaşılan parmak iziyle eşleştiğini doğrular. Bu DTLS bağlantısı daha sonra DataChannel mesajları için kullanılır.

Ardından, WebRTC ses/video iletimi için SRTP kullanarak güvenli hale getirilmiş RTP protokolünü kullanır. SRTP oturumumuzu, müzakere edilen DTLS oturumundan anahtarları çıkararak başlatırız.

Medya ve veri iletiminin neden kendi protokollerine sahip olduğunu daha sonraki bir bölümde tartışacağız, ancak şimdilik bunların ayrı ayrı ele alındığını bilmek yeterlidir.

Şimdi bittik! Başarılı bir şekilde çift yönlü ve güvenli iletişim kurduk. WebRTC aracılarınız arasında kararlı bir bağlantınız varsa, ihtiyacınız olan tüm karmaşıklık budur. Bir sonraki bölümde, WebRTC'nin talihsiz gerçek dünya problemleri olan paket kaybı ve bant genişliği sınırları ile nasıl başa çıktığını tartışacağız.

### RTP ve SCTP aracılığıyla eşlerle iletişim

Artık iki WebRTC aracımız bağlandı ve güvenli, çift yönlü iletişim kuruldu, hadi iletişim kurmaya başlayalım! Yine, WebRTC iki önceden var olan protokol kullanacak: RTP (Real-time Transport Protocol) ve SCTP (Stream Control Transmission Protocol). SRTP ile şifrelenmiş medyayı değiş tokuş etmek için RTP kullanır ve DTLS ile şifrelenmiş DataChannel mesajlarını göndermek ve almak için SCTP kullanırız.

RTP oldukça minimal bir protokoldür, ancak gerçek zamanlı akış uygulamak için gerekli araçları sağlar. RTP hakkında en önemli şey, geliştiriciye esneklik sağlamasıdır ve gecikme, paket kaybı ve tıkanıklığı istedikleri gibi ele almalarına olanak tanır. Bunu medya bölümünde daha ayrıntılı tartışacağız.

Yığındaki son protokol SCTP'dir. SCTP hakkında önemli olan şey, güvenilir ve sıralı mesaj teslimini (birçok farklı seçenek arasında) kapatabilmenizdir. Bu, geliştiricilerin gerçek zamanlı sistemler için gerekli gecikmeyi sağlamalarına olanak tanır.

## WebRTC, protokollerin bir koleksiyonu

WebRTC bir sürü problemi çözer. İlk bakışta teknoloji aşırı mühendislik edilmiş görünebilir, ancak WebRTC'nin dehası onun alçakgönüllülüğündedir. Her şeyi daha iyi çözebileceği varsayımı altında yaratılmamıştır. Bunun yerine, birçok mevcut tek amaçlı teknolojiyi kucaklamış ve bunları akıcı, yaygın olarak uygulanabilir bir pakete getirmiştir.

Bu, her parçayı bunalmadan ayrı ayrı incelememize ve öğrenmemize olanak tanır. Bunu görselleştirmenin iyi bir yolu, bir 'WebRTC Aracısı'nın gerçekten birçok farklı protokolün sadece bir orkestratörü olduğudur.

![WebRTC Agent](../images/01-webrtc-agent.png "WebRTC Agent Diyagramı")

## WebRTC API'si nasıl çalışır?

Bu bölüm, WebRTC JavaScript API'sinin yukarıda açıklanan WebRTC protokolüne nasıl eşlendiğini özetler. WebRTC API'sinin kapsamlı bir demosu olması amaçlanmamıştır, daha çok her şeyin nasıl bir araya geldiğini gösteren zihinsel bir model oluşturmak içindir.
Protokol veya API'ye aşina değilseniz endişelenmeyin. Bu, daha fazla öğrendikçe geri dönmek için eğlenceli bir bölüm olabilir!

### `new RTCPeerConnection`

`RTCPeerConnection`, üst düzey "WebRTC Oturumu"dur. Yukarıda bahsedilen tüm protokolleri içerir. Alt sistemlerin hepsi tahsis edilir ancak henüz hiçbir şey olmaz.

### `addTrack`

`addTrack` yeni bir RTP akışı oluşturur. Bu akış için rastgele bir Synchronization Source (SSRC) oluşturulacaktır. Bu akış daha sonra `createOffer` tarafından oluşturulan Session Description içinde bir medya bölümü içinde yer alacaktır. Her `addTrack` çağrısı yeni bir SSRC ve medya bölümü oluşturacaktır.

Bir SRTP Oturumu kurulur kurulmaz, bu medya paketleri SRTP kullanılarak şifrelenmeye başlar ve ICE aracılığıyla gönderilir.

### `createDataChannel`

`createDataChannel`, SCTP ilişkisi yoksa yeni bir SCTP akışı oluşturur. SCTP varsayılan olarak etkin değildir. Yalnızca bir taraf veri kanalı talep ettiğinde başlatılır.

Bir DTLS Oturumu kurulur kurulmaz, SCTP ilişkisi DTLS ile şifrelenmiş paketleri ICE aracılığıyla göndermeye başlayacaktır.

### `createOffer`

`createOffer`, uzak eşle paylaşılacak yerel durumun bir Session Description'ını oluşturur.

`createOffer` çağrısı yerel eş için hiçbir şeyi değiştirmez.

### `setLocalDescription`

`setLocalDescription`, talep edilen değişiklikleri onaylar. `addTrack`, `createDataChannel` ve benzer çağrılar bu çağrıya kadar geçicidir. `setLocalDescription`, `createOffer` tarafından oluşturulan değerle çağrılır.

Genellikle bu çağrıdan sonra, teklifi uzak eşe göndereceksiniz, o da bunu `setRemoteDescription` çağırmak için kullanacaktır.

### `setRemoteDescription`

`setRemoteDescription`, yerel aracıyı uzak adayların durumu hakkında nasıl bilgilendirdiğimizdir. 'Sinyalleme' eylemi JavaScript API'si ile bu şekilde yapılır.

Her iki tarafta da `setRemoteDescription` çağrıldığında, WebRTC aracıları artık Eşten-Eşe (P2P) iletişim kurmaya başlamak için yeterli bilgiye sahiptir!

### `addIceCandidate`

`addIceCandidate`, bir WebRTC aracısının herhangi bir zamanda daha fazla uzak ICE Adayı eklemesine olanak tanır. Bu API, ICE Adayını doğrudan ICE alt sistemine gönderir ve daha büyük WebRTC bağlantısı üzerinde başka bir etkisi yoktur.

### `ontrack`

`ontrack`, uzak eşten bir RTP paketi alındığında tetiklenen bir callback'tir. Gelen paketler, `setRemoteDescription`'a geçirilen Session Description'da beyan edilmiş olacaktır.

WebRTC, SSRC'yi kullanır ve ilişkili `MediaStream` ve `MediaStreamTrack`'i arar ve bu detaylarla doldurulmuş bu callback'i tetikler.

### `oniceconnectionstatechange`

`oniceconnectionstatechange`, ICE aracısının durumundaki değişikliği yansıtan bir callback'tir. Ağ bağlantısında bir değişiklik olduğunda bu şekilde bilgilendirilirsiniz.

### `onconnectionstatechange`

`onconnectionstatechange`, ICE aracısı ve DTLS aracısı durumunun bir kombinasyonudur. ICE ve DTLS'nin her ikisi de başarıyla tamamlandığında bilgilendirilmek için bunu izleyebilirsiniz.
