---
title: FAQ
type: docs
weight: 12
---

# FAQ

{{<details "Mengapa WebRTC menggunakan UDP?">}}
NAT Traversal memerlukan UDP. Tanpa NAT Traversal membangun koneksi P2P
tidak akan mungkin. UDP tidak menyediakan "pengiriman terjamin" seperti TCP, jadi WebRTC menyediakannya di
level pengguna.

Lihat [Connecting]({{< ref "03-connecting" >}}) untuk info lebih lanjut.
{{</details>}}

{{<details "Berapa banyak DataChannel yang bisa saya miliki?">}}
65534 channel karena _stream identifier_ memiliki 16 bit. Anda dapat menutup dan membuka yang baru kapan saja.
{{</details>}}

{{<details "Apakah WebRTC memberlakukan batas bandwidth?">}}
Baik DataChannel maupun RTP menggunakan _congestion control_. Ini berarti bahwa WebRTC secara aktif mengukur
_bandwidth_ Anda dan mencoba menggunakan jumlah yang optimal. Ini adalah keseimbangan antara mengirim sebanyak
mungkin, tanpa membebani koneksi.
{{</details>}}

{{<details "Bisakah saya mengirim data biner?">}}
Ya, Anda dapat mengirim data teks dan biner melalui DataChannel.
{{</details>}}

{{<details "Latensi apa yang bisa saya harapkan dengan WebRTC?">}}
Untuk media yang tidak disetel, Anda dapat mengharapkan di bawah 500 milidetik. Jika Anda bersedia menyetel atau mengorbankan kualitas
untuk latensi, _developer_ telah mendapatkan latensi di bawah 100 ms.

DataChannel mendukung opsi "Partial-reliability" yang dapat mengurangi latensi yang disebabkan oleh
retransmisi data melalui koneksi yang hilang. Jika dikonfigurasi dengan benar, telah ditunjukkan untuk mengalahkan koneksi TCP TLS.
{{</details>}}

{{<details "Mengapa saya menginginkan pengiriman tidak terurut untuk DataChannel?">}}
Ketika informasi yang lebih baru membuat yang lama menjadi usang seperti informasi posisi sebuah
objek, atau setiap pesan independen dari yang lain dan perlu menghindari
penundaan _head-of-line blocking_.
{{</details>}}

{{<details "Bisakah saya mengirim audio atau video melalui DataChannel?">}}
Ya, Anda dapat mengirim data apa pun melalui DataChannel. Dalam kasus peramban, itu akan menjadi
tanggung jawab Anda untuk mendekode data dan meneruskannya ke pemutar media untuk rendering,
sementara semua itu dilakukan secara otomatis jika Anda menggunakan _media channel_.
{{</details>}}
