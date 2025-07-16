---
title: Veri İletişimi
type: docs
weight: 8
---

# Veri İletişimi

## WebRTC'nin veri iletişiminden ne elde ederim?

WebRTC, veri iletişimi için veri kanalları sağlar. İki eş arasında 65.534 veri kanalı açabilirsiniz.
Veri kanalı datagram tabanlıdır ve her birinin kendi dayanıklılık ayarları vardır. Varsayılan olarak, her veri kanalının garantili sıralı teslimatı vardır.

WebRTC'ye medya geçmişinden yaklaşıyorsanız veri kanalları savurgan görünebilir. HTTP veya WebSocket'leri kullanabileceğim zaman neden bu alt sisteme ihtiyacım var?

Veri kanallarının gerçek gücü, onları sırasız/kayıplı teslimatla UDP gibi davranacak şekilde yapılandırabilmenizdir.
Bu, düşük gecikme ve yüksek performans durumları için gereklidir. Backpressure'ı ölçebilir ve sadece ağınızın desteklediği kadar gönderdüğinizden emin olabilirsiniz.

## Nasıl çalışır?

WebRTC, [RFC 4960](https://tools.ietf.org/html/rfc4960)'ta tanımlanan Stream Control Transmission Protocol (SCTP) kullanır. SCTP, TCP veya UDP'ye alternatif olarak amaçlanan bir aktarım katmanı protokolüdür. WebRTC için bunu DTLS bağlantımız üzerinde çalışan bir uygulama katmanı protokolü olarak kullanırız.

SCTP size akışlar verir ve her akış bağımsız olarak yapılandırılabilir. WebRTC veri kanalları bunların etrafındaki ince soyutlamalardır. Dayanıklılık ve sıralama etrafındaki ayarlar doğrudan SCTP Ajanına aktarılır.

Veri kanallarının SCTP'nin ifade edemeyeceği bazı özellikleri vardır, örneğin kanal etiketleri. Bunu çözmek için WebRTC, [RFC 8832](https://tools.ietf.org/html/rfc8832)'de tanımlanan Data Channel Establishment Protocol (DCEP) kullanır. DCEP, kanal etiketi ve protokolünü iletmek için bir mesaj tanımlar.

## DCEP

DCEP'in sadece iki mesajı vardır: `DATA_CHANNEL_OPEN` ve `DATA_CHANNEL_ACK`. Açılan her veri kanalı için uzak tarafın bir ack ile yanıt vermesi gerekir.

### DATA_CHANNEL_OPEN

Bu mesaj, kanal açmak isteyen WebRTC Ajanı tarafından gönderilir.

#### Paket Formatı

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |  Channel Type |            Priority           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Reliability Parameter                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Label Length          |       Protocol Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                             Label                             /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            Protocol                           /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Message Type

Message Type, `0x03`'ün statik değeridir.

#### Channel Type

Channel Type, kanalın dayanıklılık/sıralama özelliklerini kontrol eder. Aşağıdaki değerlere sahip olabilir:

- `DATA_CHANNEL_RELIABLE` (`0x00`) - Hiçbir mesaj kaybolmaz ve sırayla gelir
- `DATA_CHANNEL_RELIABLE_UNORDERED` (`0x80`) - Hiçbir mesaj kaybolmaz, ancak sıra dışı gelebilirler.
- `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT` (`0x01`) - İstenen sayıda denedikten sonra mesajlar kaybolabilir, ancak sırayla gelirler.
- `DATA_CHANNEL_PARTIAL_RELIABLE_REXMIT_UNORDERED` (`0x81`) - İstenen sayıda denedikten sonra mesajlar kaybolabilir ve sıra dışı gelebilirler.
- `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED` (`0x02`) - İstenen sürede gelmezlerse mesajlar kaybolabilir, ancak sırayla gelirler.
- `DATA_CHANNEL_PARTIAL_RELIABLE_TIMED_UNORDERED` (`0x82`) - İstenen sürede gelmezlerse mesajlar kaybolabilir ve sıra dışı gelebilirler.

#### Priority

Veri kanalının önceliği. Daha yüksek önceliğe sahip veri kanalları önce planlanacaktır. Büyük düşük öncelikli kullanıcı mesajları, yüksek öncelikli kullanıcı mesajlarının gönderimini geciktirmeyecektir.

#### Reliability Parameter

Veri kanalı türü `DATA_CHANNEL_PARTIAL_RELIABLE` ise, sonekler davranışı yapılandırır:

- `REXMIT` - Gönderenin vazgeçmeden önce mesajı kaç kez yeniden göndereceğini tanımlar.
- `TIMED` - Gönderenin vazgeçmeden önce mesajı ne kadar süre (ms cinsinden) yeniden göndereceğini tanımlar.

#### Label

Veri kanalının adını içeren UTF-8 kodlu string. Bu string boş olabilir.

#### Protocol

Bu boş bir string ise, protokol belirtilmemiştir. Boş olmayan bir string ise, [RFC 6455](https://tools.ietf.org/html/rfc6455#page-61)'te tanımlanan "WebSocket Subprotocol Name Registry"'de kayıtlı bir protokol belirtmelidir.

### DATA_CHANNEL_ACK

Bu mesaj, bu veri kanalının açıldığını kabul etmek için WebRTC Ajanı tarafından gönderilir.

#### Paket Formatı

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Message Type |
+-+-+-+-+-+-+-+-+
```

## Stream Control Transmission Protocol

SCTP, WebRTC veri kanallarının arkasındaki gerçek güçtür. Veri kanalının tüm bu özelliklerini sağlar:

- Multiplexing
- TCP benzeri yeniden iletim mekanizması kullanarak güvenilir teslimat
- Kısmi güvenilirlik seçenekleri
- Tıkanıklık Önleme
- Akış Kontrolü

SCTP'yi anlamak için onu üç bölümde inceleyeceğiz. Amaç, bu bölümden sonra SCTP'yi hata ayıklamak ve derin detaylarını kendi başınıza öğrenmek için yeterince bilmenizdir.

## Kavramlar

SCTP özellik bakımından zengin bir protokoldür. Bu bölüm sadece WebRTC tarafından kullanılan SCTP bölümlerini kapsayacaktır.
WebRTC tarafından kullanılmayan SCTP'deki özellikler multi-homing ve yol seçimini içerir.

Yirmi yılı aşkın geliştirme ile SCTP'yi tam olarak kavramak zor olabilir.

### Association

Association, SCTP Oturumu için kullanılan terimdir. İki SCTP Ajanının iletişim halindeyken paylaştığı durumdur.

### Streams

Stream, tek yönlü kullanıcı verisi dizisidir. Veri kanalı oluşturduğunuzda aslında sadece SCTP stream oluşturuyorsunuz. Her SCTP Association, stream'lerin bir listesini içerir. Her stream farklı güvenilirlik türleri ile yapılandırılabilir.

WebRTC sadece stream oluşturma sırasında yapılandırmanıza izin verir, ancak SCTP aslında yapılandırmayı istediğiniz zaman değiştirmeye izin verir.

### Datagram Based

SCTP verileri datagram olarak çerçeveler ve byte stream olarak değil. Veri gönderme ve alma TCP yerine UDP kullanmak gibi hissedilir.
Tek stream üzerinden birden fazla dosya aktarmak için herhangi bir ekstra kod eklemeniz gerekmez.

SCTP mesajlarının UDP gibi boyut sınırları yoktur. Tek bir SCTP mesajı boyut olarak birden fazla gigabayt olabilir.

### Chunks

SCTP protokolü chunk'lardan oluşur. Birçok farklı chunk türü vardır. Bu chunk'lar tüm iletişim için kullanılır.
Kullanıcı verisi, bağlantı başlatma, tıkanıklık kontrolü ve daha fazlası chunk'lar aracılığıyla yapılır.

Her SCTP paketi chunk'ların bir listesini içerir. Böylece bir UDP paketinde farklı stream'lerden mesajlar taşıyan birden fazla chunk'ınız olabilir.

### Transmission Sequence Number

Transmission Sequence Number (TSN), DATA chunk'ları için global benzersiz tanımlayıcıdır. DATA chunk, kullanıcının göndermek istediği tüm mesajları taşıyan şeydir. TSN önemlidir çünkü alıcının paketlerin kayıp olup olmadığını veya sıra dışı olup olmadığını belirlemesine yardımcı olur.

Alıcı eksik bir TSN fark ederse, yerine gelinene kadar veriyi kullanıcıya vermez.

### Stream Identifier

Her stream'in benzersiz bir tanımlayıcısı vardır. Açık ID ile veri kanalı oluşturduğunuzda, aslında doğrudan SCTP'ye stream identifier olarak aktarılır. ID geçmezseniz stream identifier sizin için seçilir.

### Payload Protocol Identifier

Her DATA chunk'ının ayrıca bir Payload Protocol Identifier (PPID) vardır. Bu, ne tür verinin değiş tokuş edildiğini benzersiz şekilde tanımlamak için kullanılır.
SCTP'nin birçok PPID'si vardır, ancak WebRTC sadece aşağıdaki beşini kullanır:

- `WebRTC DCEP` (`50`) - DCEP mesajları.
- `WebRTC String` (`51`) - DataChannel string mesajları.
- `WebRTC Binary` (`53`) - DataChannel binary mesajları.
- `WebRTC String Empty` (`56`) - 0 uzunluklu DataChannel string mesajları.
- `WebRTC Binary Empty` (`57`) - 0 uzunluklu DataChannel binary mesajları.

## Protokol

Aşağıdakiler SCTP protokolü tarafından kullanılan chunk'lardan bazılarıdır. Bu kapsamlı bir gösteri değildir. State machine'in anlamlı olması için yeterli yapıları sağlar.

Her Chunk bir `type` alanı ile başlar. Chunk'ların listesinden önce, ayrıca bir header'ınız olacaktır.

### DATA Chunk

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 0    | Reserved|U|B|E|    Length                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              TSN                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Stream Identifier        |   Stream Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Payload Protocol Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/                            User Data                          /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

DATA chunk, tüm kullanıcı verisinin nasıl değiş tokuş edildiğidir. Veri kanalı üzerinden herhangi bir şey gönderdiğinizde, bu şekilde değiş tokuş edilir.

### INIT Chunk

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 1    |  Chunk Flags  |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Initiate Tag                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Advertised Receiver Window Credit (a_rwnd)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Number of Outbound Streams   |  Number of Inbound Streams    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Initial TSN                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
\                                                               \
/              Optional/Variable-Length Parameters              /
\                                                               \
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

INIT chunk, association oluşturma sürecini başlatır.

### SACK Chunk

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Type = 3    |Chunk  Flags   |      Chunk Length             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Cumulative TSN Ack                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Advertised Receiver Window Credit (a_rwnd)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Number of Gap Ack Blocks = N  |  Number of Duplicate TSNs = X |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

SACK (Selective Acknowledgment) Chunk, alıcının gönderene paket aldığını nasıl bildirdiğidir.

## State Machine

Bunlar SCTP state machine'inin bazı ilginç bölümleridir. WebRTC, SCTP state machine'inin tüm özelliklerini kullanmaz.

### Connection Establishment Flow

`INIT` ve `INIT ACK` chunk'ları, her eşin yetenek ve yapılandırmalarını değiş tokuş etmek için kullanılır.

![Connection establishment](../images/07-connection-establishment.png "Connection establishment")

### Keep-Alive Mechanism

SCTP, bağlantıyı canlı tutmak için `HEARTBEAT REQUEST` ve `HEARTBEAT ACK` parçacıklarını kullanır. Bu parçacıklar, yapılandırılabilir bir aralıkla gönderilir. Ayrıca, SCTP bir paket ulaşmadığında **üssel geri çekilme** (exponential backoff) uygular.

`HEARTBEAT` parçacığı ayrıca bir **zaman değeri** içerir. Bu, iki bağlantının (association) iki uç nokta arasındaki **seyahat süresini (trip time)** hesaplamasını sağlar.
