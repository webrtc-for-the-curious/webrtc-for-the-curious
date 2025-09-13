---
title: Глоссарий
type: docs
weight: 13
---

# Глоссарий

* ACK: Подтверждение
* AVP: Профиль аудио и видео
* B-кадр: [Двунаправленный предсказанный кадр](../06-media-communication/#intra-and-inter-frame-compression). Частичное изображение, являющееся модификацией предыдущих и будущих изображений.
* DCEP: [Протокол установления канала данных](../07-data-communication/#dcep), определен в [RFC 8832](https://datatracker.ietf.org/doc/html/rfc8832)
* DeMux: Демультиплексор
* DLSR: Задержка с момента последнего отчета отправителя
* DTLS: [Безопасность транспортного уровня для датаграмм](../04-securing/#dtls), определен в [RFC 6347](https://datatracker.ietf.org/doc/html/rfc6347)
* E2E: От конца до конца
* FEC: [Упреждающая коррекция ошибок](../06-media-communication/#forward-error-correction)
* FIR: [Запрос полного внутрикадрового обновления](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)
* G.711: Узкополосный аудиокодек
* GCC: [Контроль перегрузки Google](../06-media-communication/#google-congestion-control-gcc), определен в [draft-ietf-rmcat-gcc-02](https://datatracker.ietf.org/doc/html/draft-ietf-rmcat-gcc-02)
* H.264: Расширенное видеокодирование для универсальных аудиовизуальных служб
* H.265: Спецификация соответствия для высокоэффективного видеокодирования ITU-T H.265
* HEVC: Высокоэффективное видеокодирование
* HTTP: Протокол передачи гипертекста
* HTTPS: HTTP поверх TLS, определен в [RFC 2818](https://datatracker.ietf.org/doc/html/rfc2818)
* I-кадр: [Внутрикадрово закодированный кадр](../06-media-communication/#intra-and-inter-frame-compression). Полное изображение, которое может быть декодировано без чего-либо другого.
* ICE: [Установление связности](../03-connecting/#ice), определен в [RFC 8445](https://datatracker.ietf.org/doc/html/rfc8445)
* INIT: Инициализация
* IoT: Интернет вещей
* IPv4: Интернет-протокол, версия 4
* IPv6: Интернет-протокол, версия 6
* ITU-T: Сектор стандартизации телекоммуникаций Международного союза электросвязи
* JSEP: [Протокол установления сеанса JavaScript](../02-signaling/#what-is-the-session-description-protocol-sdp), определен в [RFC 8829](https://datatracker.ietf.org/doc/html/rfc8829)
* MCU: [Многоточечный конференц-блок](../08-applied-webrtc/#mcu)
* mDNS: [Многоадресный DNS](../03-connecting/#mdns), определен в [RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762)
* MITM: Атака "человек посередине"
* MTU: Максимальный размер передаваемого блока данных
* MUX: Мультиплексирование
* NACK: Отрицательное подтверждение
* NADA: [Динамическая адаптация, поддерживаемая сетью](../06-media-communication/#bandwidth-estimation-alternatives), определен в [draft-zhu-rmcat-nada-04](https://tools.ietf.org/html/draft-zhu-rmcat-nada-04)
* NAT: [Преобразование сетевых адресов](../03-connecting/#nat-mapping), определен в [RFC 4787](https://datatracker.ietf.org/doc/html/rfc4787)
* Opus: Полностью открытый, свободный от роялти, высокоуниверсальный аудиокодек
* P-кадр: [Предсказанный кадр](../06-media-communication/#intra-and-inter-frame-compression). Частичное изображение, содержащее только изменения по сравнению с предыдущим изображением.
* P2P: Одноранговый
* PLI: [Индикация потери изображения](../06-media-communication/#full-intra-frame-request-fir-and-picture-loss-indication-pli)
* PPID: [Идентификатор протокола полезной нагрузки](../07-data-communication/#payload-protocol-identifier)
* REMB: [Оценка максимальной скорости передачи получателем](../06-media-communication/#tmmbr-tmmbn-and-remb)
* RFC: Запрос комментариев
* RMCAT: [Методы избегания перегрузки медиа RTP](../06-media-communication/#generating-a-bandwidth-estimate)
* RR: Отчет получателя
* RTCP: [Протокол управления RTP](../10-history-of-webrtc/#rtp), определен в [RFC 3550](https://datatracker.ietf.org/doc/html/rfc3550)
* RTP: [Протокол передачи в реальном времени](../10-history-of-webrtc/#rtp), определен в [RFC 3550](https://datatracker.ietf.org/doc/html/rfc3550)
* RTT: Время кругового обхода
* SACK: Избирательное подтверждение
* SCReAM: [Самосинхронизирующаяся адаптация скорости для мультимедиа](../06-media-communication/#bandwidth-estimation-alternatives), определен в [draft-johansson-rmcat-scream-cc-05](https://tools.ietf.org/html/draft-johansson-rmcat-scream-cc-05)
* SCTP: [Протокол управления потоком передачи](../07-data-communication/#stream-control-transmission-protocol), определен в [RFC 4960](https://datatracker.ietf.org/doc/html/rfc4960)
* SDP: [Протокол описания сеанса](../02-signaling/#what-is-the-session-description-protocol-sdp), определен в [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866)
* SFU: [Блок селективной пересылки](../08-applied-webrtc/#selective-forwarding-unit)
* SR: Отчет отправителя
* SRTP: [Защищенный протокол передачи в реальном времени](../04-securing/#srtp), определен в [RFC 3711](https://datatracker.ietf.org/doc/html/rfc3711)
* SSRC: Источник синхронизации
* STUN: [Утилиты обхода сеансов для NAT](../03-connecting/#stun), определен в [RFC 8489](https://datatracker.ietf.org/doc/html/rfc8489)
* TCP: Протокол управления передачей
* TLS: Безопасность транспортного уровня, определена в [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446)
* TMMBN: [Уведомление о временном максимальном битрейте медиапотока](../06-media-communication/#tmmbr-tmmbn-and-remb)
* TMMBR: [Запрос временного максимального битрейта медиапотока](../06-media-communication/#tmmbr-tmmbn-and-remb)
* TSN: [Номер последовательности передачи](../07-data-communication/#transmission-sequence-number)
* TURN: [Обход с использованием ретрансляторов вокруг NAT](../03-connecting/#turn), определен в [RFC 8656](https://datatracker.ietf.org/doc/html/rfc8656)
* TWCC: [Контроль перегрузки по всей транспортной сети](../06-media-communication/#transport-wide-congestion-control)
* UDP: Протокол пользовательских датаграмм
* VP8, VP9: Высокоэффективные технологии сжатия видео (видеокодеки), разработанные проектом WebM. Любой может использовать эти кодеки без роялти.
* WebM: Открытый формат медиафайлов, разработанный для веба.
* WebRTC: Веб-коммуникации в реальном времени. [Стандарт W3C WebRTC 1.0: Коммуникации в реальном времени между браузерами](https://www.w3.org/TR/webrtc/)
