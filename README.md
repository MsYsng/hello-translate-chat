# HELLO chat

初対面の外国語話者と、ログインなしで翻訳チャットするためのツールです。
各自が自分の言語で書くと、相手には相手の言語で届きます。

🚀 **[クイックスタート（図解・4ステップ）](https://msysng.github.io/hello-translate-chat/hello_chat_quickstart.html)** ・ 📖 **[詳しい使い方ガイド（主催者の準備・参加者向けカード・困ったとき）](https://msysng.github.io/hello-translate-chat/hello_chat_guide.html)**

*English follows below.*

- **翻訳はラップトップ1台が担当**: 標準では Chrome / Edge に内蔵の [Translator API](https://developer.chrome.com/docs/ai/translator-api) で、端末内で翻訳します。API キーやアカウントは不要で、翻訳する文章は外部のサービスに送られません。
- **Claude で翻訳することもできる（オプション）**: API キーを設定すると、Anthropic の Claude で翻訳します。会話の流れを踏まえた自然な訳になり、モデルのダウンロードも不要です。
- **参加者はスマホで開くだけ**: 同じ Wi-Fi で URL か QR コードを開きます。アプリのインストールは不要です。
- **3人以上・多言語でも使える**: 各メッセージを、参加者全員の言語に訳して届けます。選べる言語は20です。
- **ファイル1つで動く**: Python の標準ライブラリだけを使っています。`pip install` は不要です。

## 必要なもの

| | |
|---|---|
| ラップトップ | Python 3.8 以上（Mac / Windows） |
| ブラウザ | デスクトップ版の Chrome または Edge（最新版） |
| ネットワーク | ラップトップと参加者のスマホが同じ Wi-Fi にいて、端末どうしで通信できること |

ゲスト用 Wi-Fi や会場の公衆 Wi-Fi は、端末どうしの通信を禁止していることが多く、その場合はスマホから開けません。スマホのテザリングに全員でつなぐと確実です。

## 使い方

1. サーバーを起動します。いちばん簡単なのは、起動用ファイルをダブルクリックする方法です。ブラウザで管理画面が自動で開きます。
   - Mac: `HELLO-chat.command`（初回は「開発元を確認できない」と出ることがあります。右クリック →「開く」で起動できます）
   - Windows: `HELLO-chat.bat`

   ターミナルから起動することもできます。

   ```bash
   python3 hello_chat.py
   ```

   Windows では `py hello_chat.py` で起動します。ポートを変えたいときは `python3 hello_chat.py 9000` のように番号を付けます。`--open` を付けると管理画面が開きます。

2. ラップトップの Chrome で `http://localhost:8765` を開き（管理画面の「チャット画面を開く」からも開けます）、名前と言語を入れて参加します。このタブが全員分の翻訳を担当します。
3. 画面に出る URL（`http://192.168.…:8765` の形）か QR コードを、参加者のスマホで開いてもらいます。
4. 初めての言語の組み合わせでは **「翻訳モデルをダウンロード」** ボタンが出るので、押してください。**1回押すごとに1組**（例: 日本語→英語）ダウンロードされます。
5. 終わったら、管理画面の **「サーバーを終了」** を押します（ターミナルで `Ctrl+C` でも止まります）。

### 管理画面（`http://localhost:8765/admin`）

サーバーを動かしているラップトップからだけ開けます。参加者のスマホや、ほかのウェブサイトからは使えません。

- **チャット**: 参加人数とメッセージ数、参加者用の URL と QR コード。「チャットを終了」で送信を止めて会話を消去し、「チャットを開始」で新しい会話を始めます。サーバーを止めずに、回ごとに会話をリセットできます。
- **翻訳**: Chrome と Claude の切り替え、Claude のモデル選択、API キーの入力（下の「Claude で翻訳する」）。
- **サーバー**: 「サーバーを終了」で全員の接続を切って停止します。もう一度使うときは、起動用ファイルをダブルクリックします。

### 翻訳モデルは事前に準備しておくのがおすすめ

モデルは言語の組み合わせと向きごとに1回ずつダウンロードが必要です（3言語なら6回、4言語なら12回）。1度ダウンロードしたモデルは、そのラップトップの Chrome に残ります。

イベント前に準備するには、ラップトップの Chrome の別タブで参加者用の URL（`http://192.168.…:8765`）を開き、準備したい言語で参加します。このタブはスマホと同じ「表示だけ」の参加者になるので、`localhost` のタブに出るボタンを押してダウンロードします。

### 会話中の注意

- 翻訳役の `localhost` のタブを閉じたり、ラップトップをスリープさせたりしないでください。止まると全員の翻訳が止まります。
- `localhost` のタブは1つだけにしてください。
- ラップトップでは必ず `localhost` の URL を開いてください。`192.168…` の URL では翻訳機能が使えません。

## Claude で翻訳する（オプション）

Anthropic の API キーがあれば、Chrome の代わりに Claude で翻訳できます。

| | Chrome（標準） | Claude（オプション） |
|---|---|---|
| 訳の自然さ | 1文ずつ訳す | 直前の会話を踏まえて訳す。口調や敬語も自然 |
| 事前準備 | 言語ペアごとにモデルをダウンロード | 不要 |
| インターネット | 準備が済めば不要 | 必要 |
| 料金 | 無料 | API の利用料（下の目安） |
| 会話の送信先 | ラップトップの中だけ | Anthropic の API |

### API キーの取り方

API キーは Anthropic の開発者向けサイト **Claude Console**（[platform.claude.com](https://platform.claude.com/)）で作ります。Claude.ai の有料プラン（Pro など）とは別のサービスで、API の利用料は別に支払います。

1. [platform.claude.com](https://platform.claude.com/) を開き、Google アカウントかメールアドレスでアカウントを作るかサインインします。
2. **クレジットを購入します。** API は前払い制で、残高がないと使えません。[Billing](https://platform.claude.com/settings/billing) の「Buy credits」から金額を入れて購入します。イベント1回なら少額で足ります（下の「トークン消費量と料金の目安」を参照）。購入したクレジットは返金されず、1年で失効します。
3. [API keys](https://platform.claude.com/settings/keys) で **Create key** を押し、名前（例: `hello-chat`）を付けて作成します。
4. 表示されたキー（`sk-ant-` で始まる文字列）をコピーし、そのまま管理画面に貼り付けます。**キーが表示されるのは作成時の1回だけです。** なくしたら新しく作り直します。

- 念のため [Spend limits](https://platform.claude.com/settings/spend-limits) で月の上限額を決めておくと、使いすぎを防げます。
- キーはパスワードと同じです。チャットやメール、GitHub に貼らないでください。漏れたときは API keys のページで削除（無効化）します。
- 画面の文言や手順は変わることがあります。詳しくは公式の [API キーの取得方法](https://platform.claude.com/docs/en/get-api-key) を見てください。

### 設定する

1. SDK を入れます（Python 3.8 以上）。

   ```bash
   pip install anthropic
   ```

2. 管理画面の「翻訳」で **Claude** を選び、API キーを入力して **「保存して確認」** を押します。キーが使えるかその場で確認し、結果を表示します（トークンは使いません）。
   - 「このPCに保存する」にチェックすると、次回から入力は不要です。キーはこのフォルダではなく `~/.config/hello-chat/config.json` に、あなただけが読める権限で保存されます。「保存したキーを削除」で消せます。
   - チェックを外すと、サーバーを止めた時点でキーは消えます。
   - 環境変数 `ANTHROPIC_API_KEY` を設定して起動した場合は、そちらが優先されます。

   キーをこのフォルダ内のファイルや GitHub に書かないでください。

- 参加者の名前入力画面とチャットの上部に、Claude で翻訳していること（メッセージが Anthropic に送られること）が表示されます。
- Claude に接続できないとき（ネットが切れたなど）は、自動でラップトップの Chrome 翻訳に切り替わり、60秒ごとに Claude を再試行します。念のため、ラップトップでは Chrome で `localhost` のタブを開いておいてください。
- モデルは標準で `claude-opus-5-5` です。管理画面で `claude-haiku-5-5` に変えられます（環境変数 `HELLO_CLAUDE_MODEL` でも指定できます）。
- Claude を使わずに起動するには `python3 hello_chat.py --no-claude` とします。管理画面で Chrome を選んでも切り替えられます。

### トークン消費量と料金の目安

1メッセージにつき API を1回呼び出し、参加者全員の言語にまとめて訳します。1回あたりのトークンはおおよそ次のとおりです（短いチャット文、参加者2〜3言語の場合の見積もり）。

| | トークン数の目安 | 中身 |
|---|---|---|
| 入力 | 約 700〜900 | 翻訳の指示（約250）、出力形式の指定、直前8件の会話（文脈）、訳すメッセージ |
| 出力 | 約 150〜300 | 各言語の訳文と、短い思考。言語が1つ増えるごとに 30〜60 ほど増えます |

| モデル | 1メッセージ | 1,000メッセージ | 例: 5人で2時間・約300メッセージ |
|---|---|---|---|
| Claude Opus 5.5（標準） | 約 0.7〜1セント | 約 7〜9ドル | 約 2〜3ドル |
| Claude Haiku 5.5 | 約 0.02〜0.03セント | 約 0.2〜0.3ドル | 約 0.1ドル未満 |

（Opus 5.5 は入力 100万トークンあたり 4ドル・出力 20ドル、Haiku 5.5 は 0.10ドル・0.50ドルで計算。Haiku 5.5 は同じ文でもトークン数が 3割ほど多く数えられます。）

注意すること:

- **新しい言語の人が参加すると、直前の最大50件を訳し直します。** あとから来た人も会話を読めるようにするためです。その分の料金がかかります（Opus 5.5 で50件あたり約 0.4ドル）。
- 長いメッセージや言語の多い会話では、上の目安より多くなります。
- これは見積もりです。実際の使用量と料金は [Claude Console](https://platform.claude.com/usage) の「Usage」 で確認できます。心配な場合は、Console の [Spend limits](https://platform.claude.com/settings/spend-limits) で月の利用上限を設定しておくと安心です。

## プライバシー

- ログインがないため、同じ Wi-Fi で URL を知っている人は誰でも参加でき、会話を読めます。
- 会話はサーバーのメモリにだけ置かれ、ファイルには保存されません。サーバーを止めると消えます。
- 標準の Chrome 翻訳では、翻訳はラップトップの中で行われます。インターネットにアクセスするのは、翻訳モデルのダウンロードと、QR コード表示用のライブラリの読み込みだけです。
- Claude で翻訳するときは、メッセージ本文、送った人の名前と言語、直前の数件の会話が Anthropic の API に送られます。

## 困ったとき

| 症状 | 対処 |
|---|---|
| スマホで URL が開けない（「このサイトにアクセスできません」） | まずスマホの Wi-Fi 設定で、つながっているネットワーク名がラップトップと**完全に同じ**か確認します。名前が似た別のネットワーク（`-guest`、`-5G` / `-2.4G`、`_EXT` など）や、Wi-Fi が切れてモバイル通信になっていることがよくあります。名前が同じでも開けない場合は、ルーターが端末どうしの通信を止めています（プライバシーセパレーター / AP アイソレーション）。ルーターの設定でオフにするか、テザリングに全員でつなぎます。ファイアウォールで Python の受信を許可しているかも確認します。 |
| ずっと「翻訳中…」のまま | ラップトップの `localhost` のタブに、ダウンロードボタンが出ていないか確認します。 |
| 「翻訳役のPCがまだ参加していません」 | ラップトップで `http://localhost:8765` を Chrome / Edge で開き、参加します。 |
| 「翻訳できない言語の組み合わせです」 | その組み合わせにブラウザが対応していません。原文がそのまま表示されます。 |
| QR コードが出ない | インターネットにつながっていないと表示されません。画面の URL を伝えてください。 |
| 起動用ファイルが開けない（Mac） | 右クリック →「開く」を選びます。それでも開けないときは、ターミナルで `python3 hello_chat.py --open` を実行します。 |
| 「Port 8765 is already in use」 | すでに起動しています。`http://localhost:8765/admin` を開いてください。 |

主催者向けの詳しい手順と、参加者に見せるカード（日本語・英語）は [hello_chat_guide.html](hello_chat_guide.html) にあります。ブラウザで開いてください。

## 動作確認済みの環境

- macOS + Chrome 158（日本語・英語・スペイン語・韓国語）
- Windows と Edge ではまだ確認していません。

---

## English

HELLO chat is a login-free, translated group chat for meeting people who speak other languages. Everyone writes in their own language and reads everyone else's messages in theirs.

🚀 **[Quick start, illustrated (Japanese)](https://msysng.github.io/hello-translate-chat/hello_chat_quickstart.html)** · 📖 **[Full guide (Japanese, with an English participant card)](https://msysng.github.io/hello-translate-chat/hello_chat_guide.html)**

- **One laptop does the translating.** By default it uses the [Translator API](https://developer.chrome.com/docs/ai/translator-api) built into desktop Chrome and Edge, which runs on the device. No API key or account, and messages are not sent to an outside translation service.
- **Optional: translate with Claude.** With an Anthropic API key, the server translates with Claude instead: more natural, context-aware translations and no model downloads.
- **Others just open a page on their phone.** Same Wi-Fi, a URL or QR code, no app install.
- **Works for groups and many languages.** Each message is translated into every participant's language. 20 languages are available.
- **One file.** Python standard library only, no `pip install` (Claude translation needs the `anthropic` package).
- **Admin screen on the laptop.** Start or end the chat, switch translators, enter an API key, and stop the server from `http://localhost:8765/admin`.

### Requirements

- A laptop with Python 3.8+ (macOS or Windows)
- Desktop Chrome or Edge, latest version
- A Wi-Fi network where the laptop and phones can reach each other. Guest and public Wi-Fi networks often block this; a phone hotspot is a reliable fallback.

If a phone shows "This site can't be reached", first check that it is on exactly the same Wi-Fi network name as the laptop (not a `-guest`, `-5G` / `-2.4G` or extender network, and not on mobile data). If the names match and it still fails, the router is isolating devices (AP / client isolation): turn that off or use a phone hotspot.

### Quick start

1. Start the server: double-click `HELLO-chat.command` (Mac; the first time, right-click → Open) or `HELLO-chat.bat` (Windows), which also opens the admin screen. Or run `python3 hello_chat.py` (on Windows: `py hello_chat.py`); add a port number to change it, e.g. `python3 hello_chat.py 9000`, and `--open` to open the admin screen.
2. On the laptop, open `http://localhost:8765` in Chrome or Edge and join. This tab translates for everyone.
3. Have the others open the `http://192.168.…:8765` URL or scan the QR code shown on the page.
4. When a **"Download translation model"** button appears, click it. **Each click downloads one language pair in one direction** (e.g. Japanese → English).
5. To stop, click **Stop server** on the admin screen (or press `Ctrl+C` in the terminal). The conversation is deleted.

The admin screen (`http://localhost:8765/admin`) opens only on the laptop running the server, not from phones or other websites. "End chat" stops sending and deletes the conversation without stopping the server; "Start chat" begins a new one.

**Tip:** download models before the event. Open the `http://192.168.…:8765` URL in a second laptop tab and join with the language you want to prepare (that tab acts like a phone), then click the buttons in the `localhost` tab. Models stay in Chrome once downloaded.

Keep the `localhost` tab open and the laptop awake while chatting, and open only one `localhost` tab.

### Optional: translate with Claude

Get an API key from the Claude Console at [platform.claude.com](https://platform.claude.com/) (separate from Claude.ai subscriptions): sign in, buy prepaid credits on the [Billing](https://platform.claude.com/settings/billing) page, then click **Create key** on the [API keys](https://platform.claude.com/settings/keys) page and copy the key (it starts with `sk-ant-` and is shown only once). Consider setting a monthly cap under [Spend limits](https://platform.claude.com/settings/spend-limits). See the official [get an API key](https://platform.claude.com/docs/en/get-api-key) page for details.

Install the SDK with `pip install anthropic`, start the server, then on the admin screen choose **Claude**, enter your API key and click **Save and check**. The key is checked right away (no tokens used). With "Save on this laptop" ticked, it is stored in `~/.config/hello-chat/config.json`, readable only by you, never in this folder; otherwise it is forgotten when the server stops. An `ANTHROPIC_API_KEY` environment variable takes precedence. Claude translates each message into every participant's language in one request, using the last few messages as context. It needs internet, costs API usage: each message is one request of about 700–900 input and 150–300 output tokens, so roughly $7–9 per 1,000 messages with Claude Opus 5.5 or $0.20–0.30 with Claude Haiku 5.5 (when someone joins with a new language, up to the last 50 messages are translated again for them; check actual usage and set a spend limit in the Anthropic Console), and sends messages to Anthropic; participants see a notice saying so. If Claude can't be reached, the laptop's Chrome takes over automatically and Claude is retried every 60 seconds, so keep the `localhost` tab open. Change the model on the admin screen (or with `HELLO_CLAUDE_MODEL`), or start with `--no-claude` to turn it off. Never commit your API key.

### Privacy

Anyone on the same Wi-Fi who knows the URL can join and read the chat. Messages are held in memory only and disappear when the server stops. With the default Chrome translator, translation happens on the laptop; the only internet access is downloading translation models and the QR code library. With Claude, each message, its sender's name and language, and the last few messages are sent to Anthropic's API.

### Tested on

macOS with Chrome 158 (Japanese, English, Spanish, Korean). Not yet tested on Windows or Edge.

## License

MIT License. See [LICENSE](LICENSE).
