---
title: Güvenlik
type: docs
weight: 5
---

# Güvenlik

## WebRTC hangi güvenlik özelliklerine sahip?

Her WebRTC bağlantısı kimlik doğrulamalı ve şifrelidir. Üçüncü bir tarafın gönderdiğiniz şeyleri göremeyeceğinden veya sahte mesajlar ekleyemeyeceğinden emin olabilirsiniz. Ayrıca Oturum Tanımını oluşturan WebRTC Ajanının iletişim kurduğunuz kişi olduğundan da emin olabilirsiniz.

Bu mesajlarla kimsenin oynamaması çok önemlidir. Üçüncü bir tarafın geçiş sırasında Oturum Tanımını okuması sorun değil. Ancak, WebRTC'nin değiştirilmesine karşı koruması yoktur. Bir saldırgan, ICE Adaylarını değiştirip Sertifika Parmak İzini güncelleyerek size ortadaki adam saldırısı gerçekleştirebilir.

## Nasıl çalışır?

WebRTC, önceden var olan iki protokol kullanır: Datagram Aktarım Katmanı Güvenliği ([DTLS](https://tools.ietf.org/html/rfc6347)) ve Güvenli Gerçek zamanlı Aktarım Protokolü ([SRTP](https://tools.ietf.org/html/rfc3711)).

DTLS, bir oturum müzakere etmenizi ve ardından iki eş arasında güvenli bir şekilde veri alışverişi yapmanızı sağlar. HTTPS'yi destekleyen aynı teknoloji olan TLS'nin bir kardeşidir, ancak DTLS aktarım katmanı olarak TCP yerine UDP kullanır. Bu, protokolün güvenilmez teslimatı ele alması gerektiği anlamına gelir. SRTP özellikle medyayı güvenli bir şekilde değiş tokuş etmek için tasarlanmıştır. DTLS yerine bunu kullanarak yapabileceğimiz bazı optimizasyonlar vardır.

DTLS önce kullanılır. ICE tarafından sağlanan bağlantı üzerinden el sıkışma yapar. DTLS bir istemci/sunucu protokolüdür, bu yüzden bir tarafın el sıkışmayı başlatması gerekir. İstemci/Sunucu rolleri sinyalleşme sırasında seçilir. DTLS el sıkışması sırasında her iki taraf da bir sertifika sunar.
El sıkışma tamamlandıktan sonra, bu sertifika Oturum Tanımındaki sertifika hash'i ile karşılaştırılır. Bu, el sıkışmanın beklediğiniz WebRTC Ajanı ile gerçekleştiğinden emin olmak içindir. DTLS bağlantısı daha sonra DataChannel iletişimi için kullanılabilir hale gelir.

SRTP oturumu oluşturmak için onu DTLS tarafından oluşturulan anahtarları kullanarak başlatırız. SRTP'nin el sıkışma mekanizması yoktur, bu yüzden dış anahtarlarla önyüklenmesi gerekir. Bu yapıldıktan sonra, SRTP kullanılarak şifrelenmiş medya değiş tokuş edilebilir!

## Güvenlik 101

Bu bölümde sunulan teknolojiyi anlamak için önce bu terimleri anlamanız gerekecek. Kriptografi zor bir konudur, bu yüzden diğer kaynaklara da danışmaya değer!

### Düz Metin ve Şifreli Metin

Düz metin bir şifrenin girdisidir. Şifreli metin bir şifrenin çıktısıdır.

### Şifre

Şifre, düz metni şifreli metne götüren bir dizi adımdır. Şifre daha sonra tersine çevrilebilir, böylece şifreli metninizi tekrar düz metne dönüştürebilirsiniz. Bir şifre genellikle davranışını değiştirmek için bir anahtara sahiptir. Bunun için başka bir terim şifreleme ve şifre çözmedir.

Basit bir şifre ROT13'tür. Her harf 13 karakter ileri taşınır. Şifreyi geri almak için 13 karakter geri taşırsınız. `HELLO` düz metni `URYYB` şifreli metnine dönüşür. Bu durumda, Şifre ROT'dur ve anahtar 13'tür.

### Hash Fonksiyonları

Kriptografik hash fonksiyonu, bir özet üreten tek yönlü bir işlemdir. Bir girdi verildiğinde, her seferinde aynı çıktıyı üretir. Çıktının tersine _çevrilemez_ olması önemlidir. Bir çıktınız varsa, girdisini belirleyememelisiniz. Hash, bir mesajın kurcalanmadığını doğrulamak istediğinizde yararlıdır.

Basit (kesinlikle gerçek kriptografi için uygun olmasa da) bir hash fonksiyonu sadece her iki harften birini almak olacaktır. `HELLO` `HLO` olacaktır. `HELLO`'nun girdi olduğunu varsayamazsınız, ancak `HELLO`'nun hash özetine eşleşme olacağını doğrulayabilirsiniz.

### Açık/Özel Anahtar Kriptografisi

Açık/Özel Anahtar Kriptografisi, DTLS ve SRTP'nin kullandığı şifre türünü açıklar. Bu sistemde, açık ve özel anahtar olmak üzere iki anahtarınız vardır. Açık anahtar mesajları şifrelemek içindir ve paylaşılması güvenlidir.
Özel anahtar şifre çözmek içindir ve asla paylaşılmamalıdır. Açık anahtarla şifrelenmiş mesajları çözebilen tek anahtardır.

### Diffie–Hellman Değişimi

Diffie–Hellman değişimi, daha önce hiç tanışmamış iki kullanıcının internet üzerinden güvenli bir şekilde paylaşılan bir sır oluşturmasına izin verir. Kullanıcı `A`, gizlice dinleme konusunda endişelenmeden Kullanıcı `B`'ye bir sır gönderebilir. Bu, ayrık logaritma problemini çözmenin zorluğuna bağlıdır.
Bunun nasıl çalıştığını tam olarak anlamanıza gerek yok, ancak DTLS el sıkışmasını mümkün kılan şeyin bu olduğunu bilmek yararlıdır.

Wikipedia'da bunun eylemde örneği [burada](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation) mevcut.

### Pseudorandom Fonksiyon

Pseudorandom Fonksiyon (PRF), rastgele görünen bir değer üretmek için önceden tanımlanmış bir fonksiyondur. Birden fazla girdi alabilir ve tek bir çıktı üretebilir.

### Anahtar Türetme Fonksiyonu

Anahtar Türetme, Pseudorandom Fonksiyonun bir türüdür. Anahtar Türetme, bir anahtarı daha güçlü hale getirmek için kullanılan bir fonksiyondur. Yaygın bir desen anahtar uzatmadır.

Diyelim ki size 8 byte'lık bir anahtar verildi. Onu daha güçlü hale getirmek için KDF kullanabilirsiniz.

### Nonce

Nonce, bir şifreye ek girdidiri. Bu, aynı mesajı birden fazla kez şifreliyor olsanız bile şifreden farklı çıktı alabilmeniz için kullanılır.

Aynı mesajı 10 kez şifrelerseniz, şifre size 10 kez aynı şifreli metni verecektir. Nonce kullanarak, aynı anahtarı kullanırken farklı çıktı alabilirsiniz. Her mesaj için farklı bir nonce kullanmanız önemlidir! Aksi takdirde, değerin çoğunu yok eder.

### Mesaj Kimlik Doğrulama Kodu

Mesaj Kimlik Doğrulama Kodu, mesajın sonuna yerleştirilen bir hash'tir. MAC, mesajın beklediğiniz kullanıcıdan geldiğini kanıtlar.

MAC kullanmazsanız, bir saldırgan geçersiz mesajlar ekleyebilir. Şifreyi çözdükten sonra, anahtarı bilmedikleri için sadece saçmalıklarınız olacaktır.

### Anahtar Rotasyonu

Anahtar Rotasyonu, anahtarınızı belirli aralıklarla değiştirme uygulamasıdır. Bu, çalınan bir anahtarın etkisini daha az hale getirir. Bir anahtar çalınır veya sızarsa, daha az veri şifresi çözülebilir.

## DTLS

DTLS (Datagram Aktarım Katmanı Güvenliği), iki eşin önceden var olan hiçbir yapılandırma olmadan güvenli iletişim kurmasına izin verir. Birisi konuşmayı gizlice dinliyor olsa bile, mesajları şifreyi çözemeyecektir.

DTLS İstemcisi ve Sunucusunun iletişim kurması için bir şifre ve anahtar üzerinde anlaşmaları gerekir. Bu değerleri DTLS el sıkışması yaparak belirlerler. El sıkışması sırasında mesajlar düz metindedir.
DTLS İstemcisi/Sunucusu şifrelemeye başlamak için yeterli detayı değiş tokuş ettiğinde bir `Change Cipher Spec` gönderir. Bu mesajdan sonra, sonraki her mesaj şifrelenecektir!

### Paket Formatı

Her DTLS paketi bir başlık ile başlar.

#### İçerik Türü

Aşağıdaki türleri bekleyebilirsiniz:

- `20` - Change Cipher Spec
- `22` - Handshake
- `23` - Application Data

`Handshake` oturumu başlatmak için detayları değiş tokuş etmek için kullanılır. `Change Cipher Spec` diğer tarafa her şeyin şifreleneceğini bildirmek için kullanılır. `Application Data` şifrelenmiş mesajlardır.

#### Sürüm

Sürüm `0x0000feff` (DTLS v1.0) veya `0x0000fefd` (DTLS v1.2) olabilir, v1.1 yoktur.

#### Epoch

Epoch `0`'da başlar, ancak `Change Cipher Spec`'ten sonra `1` olur. Sıfır olmayan epoch'a sahip herhangi bir mesaj şifrelidir.

#### Sıra Numarası

Sıra Numarası mesajları sırayla tutmak için kullanılır. Her mesaj Sıra Numarasını artırır. Epoch artırıldığında, Sıra Numarası baştan başlar.

#### Uzunluk ve Yük

Yük `İçerik Türü`'ne özgüdür. `Application Data` için `Yük` şifrelenmiş veridir. `Handshake` için mesaja bağlı olarak farklı olacaktır. Uzunluk, `Yük`'ün ne kadar büyük olduğudur.

### El Sıkışma Durum Makinesi

El sıkışması sırasında, İstemci/Sunucu bir dizi mesaj değiş tokuş eder. Bu mesajlar uçuşlara gruplandırılır. Her uçuşta birden fazla mesaj olabilir (veya sadece bir).
Uçuştaki tüm mesajlar alınana kadar Uçuş tamamlanmaz. Her mesajın amacını aşağıda daha ayrıntılı olarak açıklayacağız.

![Handshake](../images/04-handshake.png "Handshake")

#### ClientHello

ClientHello, istemci tarafından gönderilen ilk mesajdır. Nitelik listesi içerir. Bu nitelikler sunucuya istemcinin desteklediği şifreleri ve özellikleri söyler. WebRTC için SRTP Şifresini de bu şekilde seçeriz. Ayrıca oturum için anahtarları oluşturmak için kullanılacak rastgele veri içerir.

#### HelloVerifyRequest

HelloVerifyRequest sunucu tarafından istemciye gönderilir. İstemcinin isteği göndermeyi amaçladığından emin olmak içindir. İstemci daha sonra ClientHello'yu yeniden gönderir, ancak HelloVerifyRequest'te sağlanan token ile.

#### ServerHello

ServerHello, bu oturumun yapılandırması için sunucunun yanıtıdır. Bu oturum bittiğinde hangi şifrenin kullanılacağını içerir. Ayrıca sunucu rastgele verisini de içerir.

#### Certificate

Certificate, İstemci veya Sunucu için sertifika içerir. Bu, kiminle iletişim kurduğumuzu benzersiz şekilde tanımlamak için kullanılır. El sıkışma bittikten sonra bu sertifikanın hash'lendiğinde `SessionDescription`'daki parmak izine uyduğundan emin olacağız.

#### ServerKeyExchange/ClientKeyExchange

Bu mesajlar açık anahtarı iletmek için kullanılır. Başlangıçta, istemci ve sunucu ikisi de bir anahtar çifti oluşturur. El sıkışmadan sonra bu değerler `Pre-Master Secret` oluşturmak için kullanılacaktır.

#### CertificateRequest

CertificateRequest, sunucu tarafından istemciye sertifika istediğini bildirmek için gönderilir. Sunucu sertifika İsteyebilir veya Gerektirebilir.

#### ServerHelloDone

ServerHelloDone, istemciye sunucunun el sıkışmayla işinin bittiğini bildirir.

#### CertificateVerify

CertificateVerify, gönderenin Certificate mesajında gönderilen özel anahtara sahip olduğunu kanıtlama yöntemidir.

#### ChangeCipherSpec

ChangeCipherSpec, alıcıya bu mesajdan sonra gönderilen her şeyin şifreleneceğini bildirir.

#### Finished

Finished şifrelidir ve tüm mesajların hash'ini içerir. Bu, el sıkışmanın kurcalanmadığını iddia etmek içindir.

### Anahtar Üretimi

El Sıkışma tamamlandıktan sonra, şifrelenmiş veri göndermeye başlayabilirsiniz. Şifre sunucu tarafından seçildi ve ServerHello'da. Peki anahtar nasıl seçildi?

Önce `Pre-Master Secret`'i oluşturuyoruz. Bu değeri elde etmek için `ServerKeyExchange` ve `ClientKeyExchange` tarafından değiş tokuş edilen anahtarlarda Diffie–Hellman kullanılır. Detaylar seçilen Şifreye bağlı olarak farklıdır.

Sonra `Master Secret` oluşturulur. DTLS'nin her sürümünün tanımlanmış `Pseudorandom fonksiyonu` vardır. DTLS 1.2 için fonksiyon `Pre-Master Secret`'i ve `ClientHello` ve `ServerHello`'daki rastgele değerleri alır.
`Pseudorandom Fonksiyonu` çalıştırmanın çıktısı `Master Secret`'tir. `Master Secret`, Şifre için kullanılan değerdir.

### ApplicationData Değiş Tokuşu

DTLS'nin iş atı `ApplicationData`'dır. Artık başlatılmış bir şifremiz olduğuna göre, değerleri şifrelemeye ve göndermeye başlayabiliriz.

`ApplicationData` mesajları daha önce açıklandığı gibi DTLS başlığı kullanır. `Yük` şifreli metin ile doldurulur. Artık çalışan bir DTLS Oturumunuz var ve güvenli bir şekilde iletişim kurabilirsiniz.

DTLS'nin yeniden müzakere gibi daha birçok ilginç özelliği vardır. WebRTC tarafından kullanılmadıkları için burada ele alınmayacaktır.

## SRTP

SRTP, özellikle RTP paketlerini şifrelemek için tasarlanmış bir protokoldür. SRTP oturumu başlatmak için anahtarlarınızı ve şifrenizi belirtirsiniz. DTLS'nin aksine el sıkışma mekanizması yoktur. Tüm yapılandırma ve anahtarlar DTLS el sıkışması sırasında oluşturuldu.

DTLS, anahtarları başka bir işlem tarafından kullanılmak üzere dışa aktarmak için özel bir API sağlar. Bu [RFC 5705](https://tools.ietf.org/html/rfc5705)'te tanımlanmıştır.

### Oturum Oluşturma

SRTP, girdiler üzerinde kullanılan bir Anahtar Türetme Fonksiyonu tanımlar. SRTP Oturumu oluştururken girdiler SRTP Şifremiz için anahtarlarımızı oluşturmak için bundan geçirilir. Bundan sonra medya işlemeye geçebilirsiniz.

### Medya Değiş Tokuşu

Her RTP paketinin 16 bit SıraNumarası vardır. Bu Sıra Numaraları paketleri sırayla tutmak için kullanılır, Birincil Anahtar gibi. Bir çağrı sırasında bunlar döner. SRTP bunu takip eder ve buna rollover sayacı denir.

Bir paketi şifrelerken SRTP rollover sayacını ve sıra numarasını nonce olarak kullanır. Bu, aynı veriyi iki kez gönderseniz bile şifreli metnin farklı olacağından emin olmak içindir. Bu, bir saldırganın kalıpları tanımlamasını veya tekrar saldırısı denemesini önlemek için önemlidir.
