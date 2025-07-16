---
title: SSS
type: docs
weight: 12
---

# SSS (Sıkça Sorulan Sorular)

{{<details "WebRTC neden UDP kullanıyor?">}}
NAT Geçişi UDP gerektirir. NAT Geçişi olmadan P2P bağlantı kurmak
mümkün olmazdı. UDP, TCP gibi "garantili teslimat" sağlamaz, bu yüzden WebRTC bunu
kullanıcı seviyesinde sağlar.

Daha fazla bilgi için [Bağlanma]({{< ref "03-connecting" >}}) bölümüne bakın.
{{</details>}}

{{<details "Kaç tane DataChannel'ım olabilir?">}}
Akış tanımlayıcısı 16 bit olduğu için 65534 kanal. İstediğiniz zaman kapatıp yeni bir tane açabilirsiniz.
{{</details>}}

{{<details "WebRTC bant genişliği sınırları koyuyor mu?">}}
Hem DataChannel'lar hem de RTP tıkanıklık kontrolü kullanır. Bu, WebRTC'nin aktif olarak
bant genişliğinizi ölçtüğü ve optimal miktarı kullanmaya çalıştığı anlamına gelir. Bu, mümkün olduğu kadar fazla gönderme ile bağlantıyı bunaltmama arasında bir dengedir.
{{</details>}}

{{<details "Binary veri gönderebilir miyim?">}}
Evet, DataChannel'lar aracılığıyla hem metin hem de binary veri gönderebilirsiniz.
{{</details>}}

{{<details "WebRTC ile ne kadar gecikme bekleyebilirim?">}}
Ayarlanmamış medya için 500 milisaniyenin altında gecikme bekleyebilirsiniz. Gecikme için kaliteyi ayarlamaya veya feda etmeye istekliyseniz, geliştiriciler 100ms'nin altında gecikme elde etmişlerdir.

DataChannel'lar, kayıplı bağlantı üzerinden veri yeniden iletimlerinin neden olduğu gecikmeyi azaltabilen "Kısmi-güvenilirlik" seçeneğini destekler. Doğru yapılandırılırsa, TCP TLS bağlantılarını geçtiği gösterilmiştir.
{{</details>}}

{{<details "DataChannel'lar için neden sırasız teslimat isteyeyim?">}}
Bir nesnenin konumsal bilgisi gibi yeni bilginin eskisini geçersiz kıldığı durumlarda, veya her mesajın diğerlerinden bağımsız olduğu ve baş-of-line engelleme gecikmesinden kaçınması gerektiği durumlarda.
{{</details>}}

{{<details "DataChannel üzerinden ses veya video gönderebilir miyim?">}}
Evet, DataChannel üzerinden herhangi bir veri gönderebilirsiniz. Tarayıcı durumunda, verileri decode etmek ve rendering için bir medya oynatıcısına geçmek sizin sorumluluğunuz olacaktır,
medya kanallarını kullanırsanız tüm bunlar otomatik olarak yapılırken.
{{</details>}}
