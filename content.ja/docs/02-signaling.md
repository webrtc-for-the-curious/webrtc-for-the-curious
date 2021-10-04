---
title: シグナリング
type: docs
weight: 3
---

# WebRTCシグナリングとは？

WebRTC エージェントを作成したとき、エージェントは他のピアについて何も知りません。誰と接続しようとしているのか、何を送ろうとしているのか、全くわかりません。
シグナリングは、通話を可能にする最初のブートストラップです。これらの値が交換されると、WebRTC エージェントはお互いに直接通信できるようになります。

シグナリングメッセージは単なるテキストです。WebRTC エージェントは、メッセージの転送方法を気にしません。一般的には WebSocket で共有されますが、これは必須ではありません。

## WebRTC のシグナリングはどのように動作しますか？

WebRTC は、Session Description Protocol と呼ばれる既存のプロトコルを使用しています。このプロトコルにより、2 つの WebRTC エージェントは、接続を確立するために必要なすべての状態を共有します。このプロトコル自体は、読んで理解するのは簡単です。
複雑なのは、WebRTC がこのプロトコルに入力するすべての値を理解することです。

このプロトコルは WebRTC 固有のものではありません。WebRTC の話をしなくても、まず Session Description Protocol を学びます。WebRTC はこのプロトコルのサブセットを実際に利用するだけなので、ここでは必要なものだけを取り上げます。
プロトコルを理解した後は、WebRTC での応用的な使い方に進みます。

## *Session Description Protocol* (SDP)とは？

SDP は、[RFC 8866 (旧:RFC 4566)](https://tools.ietf.org/html/rfc8866)で定義されています。SDP はキーと値で構成されるプロトコルで、各値の後には改行が入ります。これは、INI ファイルに似ています。
Session Description は、0 個以上のメディア記述を含みます。頭の中では、Session Description にメディア記述の配列が含まれているようにモデル化できます。

メディア記述は通常、メディアの 1 つのストリームに対応しています。つまり、3 つのビデオストリームと 2 つのオーディオトラックを持つ通話を記述したい場合、5 つのメディア記述が必要になります。

### SDPの読み方

Session Description の各行は、1 つの文字で始まります。その後、等号が続きます。この等号以降が値となります。値が完了すると、改行されます。

SDP では、有効なキーをすべて定義しています。プロトコルで定義されているキーには、文字しか使用できません。これらのキーにはすべて重要な意味がありますが、それについては後ほど説明します。

Session Description の例を見てみましょう。

```
a=my-sdp-value
a=second-value
```

2 つの行がありますね。それぞれがキー `a` を持っています。1 行目には `my-sdp-value` という値があり、2 行目には `second-value` という値があります。

### WebRTCは一部のSDPキーしか使用しない

WebRTC では、SDP で定義されているすべてのキー値を使用しているわけではありません。以下の 7 つのキーだけは、今すぐ理解しておく必要があります。

* `v` - バージョン(Version)、`0` と同じでなければなりません。
* `o` - オリジン(Origin)、再交渉に便利なユニークな ID を含む。
* `s` - セッション名(Session Name)、`-` と同じでなければなりません。
* `t` - タイミング(Timing)、`0 0` と同じでなければなりません。
* `m` - メディア記述(Media Description: `m=<media> <port> <proto> <fmt> ...`)、詳細は以下の通りです。
* `a` - 属性(Attribute)、フリーテキストのフィールドです。これは WebRTC で最も一般的な行です。
* `c` - 接続データ(Connection Data)、 `IN IP4 0.0.0.0` と等しくなければなりません。

### Session Description に含まれるメディアの説明文

Session Description には、メディア記述を無制限に含めることができます。

メディア記述の定義には、フォーマットのリストが含まれます。これらのフォーマットは RTP ペイロードタイプに対応しています。実際のコーデックは、メディア記述の中の `rtpmap` という値を持つ属性によって定義されます。
RTP と RTP Payload Type の重要性については、「メディア」の章で後述します。各メディア記述には、無制限の数の属性を含めることができます。

Session Description を例に挙げてみましょう。

```
v=0
m=audio 4000 RTP/AVP 111
a=rtpmap:111 OPUS/48000/2
m=video 4000 RTP/AVP 96
a=rtpmap:96 VP8/90000
a=my-sdp-value
```

2つのメディア記述があります。1つはfmt`111`のaudioタイプで、もう1つはfmt`96`のvideoタイプです。1つ目のメディア記述には1つの属性しかありません。この属性は、ペイロードタイプ `111` をOpusにマッピングします。
2つ目のメディア記述には2つの属性があります。1つ目の属性は、Payload Type `96` を VP8 にマップし、2つ目の属性は単なる `my-sdp-value` です。

### Full Example

### 完全な例

次の例では、これまで説明してきたすべての概念をまとめています。これらはすべて、WebRTC が使用する SDP の機能です。
これが読めれば、どんな WebRTC の Session Description でも読めます。

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

* `v`, `o`, `s`, `c`, `t` が定義されていますが、WebRTC セッションには影響しません。
* 2つのメディア記述があります。1つは `audio` タイプで、もう1つは `video` タイプです。
* それぞれに1つの属性があります。この属性は RTP パイプラインの詳細を設定するもので、「メディアコミュニケーション」の章で説明します。

## *SDP(Session Description Protocol)* と WebRTC の連携について

次のパズルのピースは、WebRTC が SDP をどのように使用するかを理解することです。

### オファーとアンサーとは？

WebRTCでは、オファー/アンサーモデルを採用しています。つまり、一方の WebRTC エージェントが「オファー」を出して通話を開始し、他方の WebRTC エージェントがオファーされた内容を受け入れるかどうかを「アンサー」します。

これにより、回答者はコーデックやメディア記述を拒否する機会が与えられます。このようにして、2つのピアが何を交換しようとしているのかを理解できます。

### トランシーバーは送受信用

トランシーバーはWebRTC特有の概念で、APIの中にも出てきます。これは、「メディア記述」を JavaScript API に公開するものです。各メディア記述は、トランシーバーになります。
トランシーバーを作成するたびに、新しいメディア記述がローカルの Session Description に追加されます

WebRTCの各メディア記述は、direction属性を持ちます。これにより、WebRTCエージェントは「このコーデックを送信するが、何も受信しない」と宣言できます。有効な値は4つあります。

* `send` (送信)
* `recv` (受信)
* `sendrecv` (送受信)
* `inactive` (非アクティブ)

### WebRTC で使用される SDP の値

ここでは、WebRTC エージェントの Session Description で見られる一般的な属性の一覧を示します。これらの値の多くは、これまで説明してこなかったサブシステムを制御するものです。

##### `group:BUNDLE`

バンドルとは、複数の種類のトラフィックを1つの接続で実行することです。WebRTCの実装によっては、メディアストリームごとに専用の接続を使用するものもあります。バンドルが望ましいです。

##### `fingerprint:sha-256`

これは、ピアがDTLSに使用している証明書のハッシュ値です。DTLSのハンドシェイクが完了した後、これを実際の証明書と比較して、期待通りの相手と通信していることを確認します。

##### `setup:`

これは、DTLSエージェントの動作を制御します。ICEが接続した後に、クライアントとして実行するか、サーバーとして実行するかを決定します。設定可能な値は以下の通りです。

* `setup:active` - DTLSクライアントとして動作します。
* `setup:passive` - DTLSサーバーとして動作します。
* `setup:actpass` - 他の WebRTC エージェントに選択を依頼します。

##### `ice-ufrag`

ICEエージェントのユーザーフラグメント値です。ICEトラフィックの認証に使用されます。

##### `ice-pwd`

ICEエージェントのパスワードです。ICEトラフィックの認証に使用されます。

##### `rtpmap`

この値は、特定のコーデックをRTPペイロードタイプにマッピングするために使用されます。ペイロードタイプは固定されていないので、通話ごとにオファー側が各コーデックのペイロードタイプを決定します。

##### `fmtp`
1つのPayload Typeに対して追加の値を定義します。これは、特定のビデオプロファイルやエンコーダの設定を伝えるのに便利です。

##### `candidate` (候補)
ICE エージェントから送られてくる ICE キャンディデートです。これは、WebRTCエージェントが利用可能なアドレスの1つです。これらについては、次の章で詳しく説明します。

##### `ssrc`
同期ソース（SSRC）は、1つのメディアストリームトラックを定義します。

`label` は、この個々のストリームの ID です。 `mslabel` は、内部に複数のストリームを持つことができるコンテナの ID です。

### WebRTC Session Description の例

WebRTCクライアントが生成する Session Description の例を以下に示します。

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

このメッセージからわかったことは以下の通りです。

* オーディオとビデオの2つのメディアセクションがあります。
* どちらも `sendrecv` トランシーバーです。2つのストリームを受信しているので、2つのストリームを送り返すことができます。
* ICE CandidatesとAuthenticationの詳細があるので、接続を試みることができます。
* 証明書のフィンガープリントがあるので、安全な通話ができます。

### その他のトピック

本書の次のバージョンでは、以下のトピックについても説明します。疑問点があれば、Pull Request を提出してください。

* リネゴシエーション
* サイマルキャスト
