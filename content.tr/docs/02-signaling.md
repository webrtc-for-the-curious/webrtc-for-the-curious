---
title: Sinyalleşme
type: docs
weight: 3
---

# Sinyalleşme

## WebRTC Sinyalleşme Nedir?

Bir WebRTC ajanı oluşturduğunuzda, diğer eş hakkında hiçbir şey bilmez. Kiminle bağlantı kuracağını veya ne göndereceklerini bilmez!
Sinyalleşme, bir çağrıyı mümkün kılan ilk önyüklemedir. Bu değerler değiş tokuş edildikten sonra, WebRTC ajanları doğrudan birbirleriyle iletişim kurabilir.

Sinyalleşme mesajları sadece metindir. WebRTC ajanları bunların nasıl taşındığını umursamaz. Genellikle Websocket'ler aracılığıyla paylaşılırlar, ancak bu bir gereklilik değildir.

## WebRTC sinyalleşme nasıl çalışır?

WebRTC, Oturum Tanımlama Protokolü adlı mevcut bir protokol kullanır. Bu protokol aracılığıyla, iki WebRTC Ajanı bir bağlantı kurmak için gerekli tüm durumu paylaşacaktır. Protokolün kendisi okumak ve anlamak için basittir.
Karmaşıklık, WebRTC'nin onunla doldurduğu tüm değerleri anlamaktan gelir.

Bu protokol WebRTC'ye özgü değildir. İlk olarak WebRTC hakkında konuşmadan Oturum Tanımlama Protokolünü öğreneceğiz. WebRTC gerçekten protokolün sadece bir alt kümesinden yararlanır, bu yüzden sadece ihtiyacımız olanı kapsayacağız.
Protokolü anladıktan sonra, WebRTC'deki uygulamalı kullanımına geçeceğiz.

## _Oturum Tanımlama Protokolü_ (SDP) Nedir?

Oturum Tanımlama Protokolü [RFC 8866](https://tools.ietf.org/html/rfc8866)'da tanımlanmıştır. Her değerden sonra yeni satır olan bir anahtar/değer protokolüdür. Bir INI dosyasına benzer hissettirecektir.
Bir Oturum Tanımı sıfır veya daha fazla Medya Tanımı içerir. Zihinsel olarak bunu, bir Medya Tanımları dizisi içeren bir Oturum Tanımı olarak modelleyebilirsiniz.

Bir Medya Tanımı genellikle tek bir medya akışıyla eşlenir. Yani üç video akışı ve iki ses parçası olan bir çağrıyı tanımlamak istiyorsanız, beş Medya Tanımınız olurdu.

### SDP nasıl okunur

Bir Oturum Tanımındaki her satır tek bir karakterle başlayacaktır, bu sizin anahtarınızdır. Ardından eşittir işareti gelecektir. Bu eşittir işaretinden sonra gelen her şey değerdir. Değer tamamlandıktan sonra, yeni bir satırınız olacaktır.

Oturum Tanımlama Protokolü geçerli olan tüm anahtarları tanımlar. Protokolde tanımlandığı gibi anahtarlar için sadece harfleri kullanabilirsiniz. Bu anahtarların hepsi önemli anlamlara sahiptir ve daha sonra açıklanacaktır.

Bu Oturum Tanımı alıntısını ele alalım:

```
a=my-sdp-value
a=second-value
```

İki satırınız var. Her biri `a` anahtarıyla. İlk satırın değeri `my-sdp-value`, ikinci satırın değeri `second-value`.

### WebRTC sadece bazı SDP anahtarlarını kullanır

Oturum Tanımlama Protokolü tarafından tanımlanan tüm anahtar değerleri WebRTC tarafından kullanılmaz. Sadece [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829)'da tanımlanan JavaScript Oturum Kurma Protokolü (JSEP)'nde kullanılan anahtarlar önemlidir. Aşağıdaki yedi anahtar şu anda anlamanız gereken tek anahtarlardır:

- `v` - Sürüm, `0`'a eşit olmalıdır.
- `o` - Kaynak, yeniden müzakereler için yararlı benzersiz bir ID içerir.
- `s` - Oturum Adı, `-`'ye eşit olmalıdır.
- `t` - Zamanlama, `0 0`'a eşit olmalıdır.
- `m` - Medya Tanımı (`m=<media> <port> <proto> <fmt> ...`), aşağıda ayrıntılı olarak açıklanmıştır.
- `a` - Öznitelik, serbest metin alanı. Bu WebRTC'de en yaygın satırdır.
- `c` - Bağlantı Verisi, `IN IP4 0.0.0.0`'a eşit olmalıdır.

### Oturum Tanımında Medya Tanımları

Bir Oturum Tanımı sınırsız sayıda Medya Tanımı içerebilir.

Bir Medya Tanımı tanımı, format listesi içerir. Bu formatlar RTP Yük Türleriyle eşlenir. Gerçek codec daha sonra Medya Tanımında `rtpmap` değerine sahip bir Öznitelik tarafından tanımlanır.
RTP ve RTP Yük Türlerinin önemi daha sonra Medya bölümünde tartışılır. Her Medya Tanımı sınırsız sayıda öznitelik içerebilir.

Bu Oturum Tanımı alıntısını örnek olarak ele alalım:

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

İki Medya Tanımınız var, biri fmt `111` olan ses türünde ve biri format `96` olan video türünde. İlk Medya Tanımının sadece bir özniteliği var. Bu öznitelik Yük Türü `111`'i Opus'a eşler.
İkinci Medya Tanımının iki özniteliği var. İlk öznitelik Yük Türü `96`'yı VP8 olarak eşler ve ikinci öznitelik sadece `my-sdp-value`.

### Tam Örnek

Aşağıdaki, bahsettiğimiz tüm kavramları bir araya getirir. Bunlar WebRTC'nin kullandığı Oturum Tanımlama Protokolünün tüm özellikleridir.
Bunu okuyabiliyorsanız, herhangi bir WebRTC Oturum Tanımını okuyabilirsiniz!

```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=-
c=IN IP4 127.0.0.1
t=0 0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4002 RTP/AVP 96
a=rtpmap:96 VP8/90000
```

- `v`, `o`, `s`, `c`, `t` tanımlandı, ancak WebRTC oturumunu etkilemezler.
- İki Medya Tanımınız var. Biri `audio` türünde ve biri `video` türünde.
- Her birinin bir özniteliği var. Bu öznitelik, "Medya İletişimi" bölümünde tartışılan RTP pipeline'ının detaylarını yapılandırır.

## _Oturum Tanımlama Protokolü_ ve WebRTC nasıl birlikte çalışır

Bulmacının bir sonraki parçası WebRTC'nin Oturum Tanımlama Protokolünü _nasıl_ kullandığını anlamaktır.

### Teklifler ve Cevaplar Nedir?

WebRTC bir teklif/cevap modeli kullanır. Bunun anlamı, bir WebRTC Ajanının bir çağrı başlatmak için "Teklif" yapması ve diğer WebRTC Ajanlarının sunulanı kabul etmeye istekliyse "Cevap" vermesidir.

Bu, cevaplayıcıya Medya Tanımlarında desteklenmeyen codec'leri reddetme şansı verir. İki eşin hangi formatları değiş tokuş etmeye istekli olduklarını anlayabilmesinin yolu budur.

### Transceiverlar gönderme ve alma içindir

Transceiverlar API'de göreceğiniz WebRTC'ye özgü bir kavramdır. Yaptığı şey "Medya Tanımını" JavaScript API'sine açmaktır. Her Medya Tanımı bir Transceiver olur.
Her Transceiver oluşturduğunuzda yerel Oturum Tanımına yeni bir Medya Tanımı eklenir.

WebRTC'deki her Medya Tanımının bir yön özniteliği olacaktır. Bu, bir WebRTC Ajanının "Size bu codec'i göndereceğim, ama geri hiçbir şey kabul etmeye istekli değilim" demesine izin verir. Dört geçerli değer vardır:

- `send`
- `recv`
- `sendrecv`
- `inactive`

### WebRTC tarafından kullanılan SDP Değerleri

Bu, bir WebRTC Ajanından gelen Oturum Tanımında göreceğiniz bazı yaygın özniteliklerin listesidir. Bu değerlerin çoğu henüz tartışmadığımız alt sistemleri kontrol eder.

#### `group:BUNDLE`

Bundling, birden fazla trafik türünü tek bir bağlantı üzerinden çalıştırma eylemidir. Bazı WebRTC uygulamaları medya akışı başına özel bağlantı kullanır. Bundling tercih edilmelidir.

#### `fingerprint:sha-256`

Bu, bir eşin DTLS için kullandığı sertifikanın hash'idir. DTLS el sıkışması tamamlandıktan sonra, beklediğiniz kişiyle iletişim kurduğunuzu onaylamak için bunu gerçek sertifikayla karşılaştırırsınız.

#### `setup:`

Bu, DTLS Ajanı davranışını kontrol eder. ICE bağlandıktan sonra istemci veya sunucu olarak çalışıp çalışmayacağını belirler. Olası değerler:

- `setup:active` - DTLS İstemcisi olarak çalış.
- `setup:passive` - DTLS Sunucusu olarak çalış.
- `setup:actpass` - Diğer WebRTC Ajanından seçmesini iste.

#### `mid`

"mid" özniteliği, oturum tanımı içindeki medya akışlarını tanımlamak için kullanılır.

#### `ice-ufrag`

Bu, ICE Ajanı için kullanıcı parçası değeridir. ICE Trafiğinin kimlik doğrulaması için kullanılır.

#### `ice-pwd`

Bu, ICE Ajanı için paroladır. ICE Trafiğinin kimlik doğrulaması için kullanılır.

#### `rtpmap`

Bu değer, belirli bir codec'i RTP Yük Türüne eşlemek için kullanılır. Yük türleri statik değildir, bu yüzden her çağrı için teklif veren her codec için yük türlerini belirler.

#### `fmtp`

Bir Yük Türü için ek değerleri tanımlar. Bu, belirli bir video profili veya kodlayıcı ayarını iletmek için yararlıdır.

#### `candidate`

Bu, ICE Ajanından gelen bir ICE Adayıdır. Bu, WebRTC Ajanının mevcut olduğu olası bir adrestir. Bunlar bir sonraki bölümde tam olarak açıklanmıştır.

#### `ssrc`

Bir Senkronizasyon Kaynağı (SSRC) tek bir medya akışı parçasını tanımlar.

`label` bu bireysel akış için ID'dir. `mslabel` içinde birden fazla akış olabilen bir konteyner için ID'dir.

### WebRTC Oturum Tanımı Örneği

Aşağıdaki, bir WebRTC İstemcisi tarafından oluşturulan tam bir Oturum Tanımıdır:

```
v=0
o=- 3546004397921447048 1596742744 IN IP4 0.0.0.0
s=-
t=0 0
a=fingerprint:sha-256 0F:74:31:25:CB:A2:13:EC:28:6F:6D:2C:61:FF:5D:C2:BC:B9:DB:3D:98:14:8D:1A:BB:EA:33:0C:A4:60:A8:8E
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=setup:active
a=mid:0
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=ssrc:350842737 cname:yvKPspsHcYcwGFTw
a=ssrc:350842737 msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=ssrc:350842737 mslabel:yvKPspsHcYcwGFTw
a=ssrc:350842737 label:DfQnKjQQuwceLFdV
a=msid:yvKPspsHcYcwGFTw DfQnKjQQuwceLFdV
a=sendrecv
a=candidate:foundation 1 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 2 udp 2130706431 192.168.1.1 53165 typ host generation 0
a=candidate:foundation 1 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=candidate:foundation 2 udp 1694498815 1.2.3.4 57336 typ srflx raddr 0.0.0.0 rport 57336 generation 0
a=end-of-candidates
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=setup:active
a=mid:1
a=ice-ufrag:CsxzEWmoKpJyscFj
a=ice-pwd:mktpbhgREmjEwUFSIJyPINPUhgDqJlSd
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=ssrc:2180035812 cname:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=ssrc:2180035812 mslabel:XHbOTNRFnLtesHwJ
a=ssrc:2180035812 label:JgtwEhBWNEiOnhuW
a=msid:XHbOTNRFnLtesHwJ JgtwEhBWNEiOnhuW
a=sendrecv
```

Bu mesajdan bildiklerimiz:

- İki medya bölümümüz var, biri ses ve biri video.
- Her ikisi de `sendrecv` transceiverları. İki akış alıyoruz ve ikisini geri gönderebiliriz.
- ICE Adayları ve Kimlik Doğrulama detaylarımız var, böylece bağlanmaya çalışabiliriz.
- Sertifika parmak izimiz var, böylece güvenli bir çağrı yapabiliriz.

### İleri Konular

Bu kitabın sonraki sürümlerinde, aşağıdaki konular da ele alınacaktır:

- Yeniden müzakere
- Simulcast
