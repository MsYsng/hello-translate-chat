# HELLO chat

初対面の外国語話者と、ログインなしで翻訳チャットするためのツールです。
各自が自分の言語で書くと、相手には相手の言語で届きます。

*English follows below.*

- **翻訳はラップトップ1台が担当**: Chrome / Edge に内蔵の [Translator API](https://developer.chrome.com/docs/ai/translator-api) で、端末内で翻訳します。API キーやアカウントは不要で、翻訳する文章は外部のサービスに送られません。
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

1. サーバーを起動します。

   ```bash
   python3 hello_chat.py
   ```

   Windows では `py hello_chat.py` で起動します。ポートを変えたいときは `python3 hello_chat.py 9000` のように番号を付けます。
   起動すると、ラップトップ用と参加者用の2つの URL が表示されます。

2. ラップトップの Chrome で `http://localhost:8765` を開き、名前と言語を入れて参加します。このタブが全員分の翻訳を担当します。
3. 画面に出る URL（`http://192.168.…:8765` の形）か QR コードを、参加者のスマホで開いてもらいます。
4. 初めての言語の組み合わせでは **「翻訳モデルをダウンロード」** ボタンが出るので、押してください。**1回押すごとに1組**（例: 日本語→英語）ダウンロードされます。
5. 終わったら、ターミナルで `Ctrl+C` を押してサーバーを止めます。

### 翻訳モデルは事前に準備しておくのがおすすめ

モデルは言語の組み合わせと向きごとに1回ずつダウンロードが必要です（3言語なら6回、4言語なら12回）。1度ダウンロードしたモデルは、そのラップトップの Chrome に残ります。

イベント前に準備するには、ラップトップの Chrome の別タブで参加者用の URL（`http://192.168.…:8765`）を開き、準備したい言語で参加します。このタブはスマホと同じ「表示だけ」の参加者になるので、`localhost` のタブに出るボタンを押してダウンロードします。

### 会話中の注意

- 翻訳役の `localhost` のタブを閉じたり、ラップトップをスリープさせたりしないでください。止まると全員の翻訳が止まります。
- `localhost` のタブは1つだけにしてください。
- ラップトップでは必ず `localhost` の URL を開いてください。`192.168…` の URL では翻訳機能が使えません。

## プライバシー

- ログインがないため、同じ Wi-Fi で URL を知っている人は誰でも参加でき、会話を読めます。
- 会話はサーバーのメモリにだけ置かれ、ファイルには保存されません。サーバーを止めると消えます。
- 翻訳はラップトップの中で行われます。インターネットにアクセスするのは、翻訳モデルのダウンロードと、QR コード表示用のライブラリの読み込みだけです。

## 困ったとき

| 症状 | 対処 |
|---|---|
| スマホで URL が開けない | 同じ Wi-Fi か確認します。ゲスト Wi-Fi ならテザリングに切り替えます。ファイアウォールで Python の受信を許可しているかも確認します。 |
| ずっと「翻訳中…」のまま | ラップトップの `localhost` のタブに、ダウンロードボタンが出ていないか確認します。 |
| 「翻訳役のPCがまだ参加していません」 | ラップトップで `http://localhost:8765` を Chrome / Edge で開き、参加します。 |
| 「翻訳できない言語の組み合わせです」 | その組み合わせにブラウザが対応していません。原文がそのまま表示されます。 |
| QR コードが出ない | インターネットにつながっていないと表示されません。画面の URL を伝えてください。 |

主催者向けの詳しい手順と、参加者に見せるカード（日本語・英語）は [hello_chat_guide.html](hello_chat_guide.html) にあります。ブラウザで開いてください。

## 動作確認済みの環境

- macOS + Chrome 158（日本語・英語・スペイン語・韓国語）
- Windows と Edge ではまだ確認していません。

---

## English

HELLO chat is a login-free, translated group chat for meeting people who speak other languages. Everyone writes in their own language and reads everyone else's messages in theirs.

- **One laptop does the translating.** It uses the [Translator API](https://developer.chrome.com/docs/ai/translator-api) built into desktop Chrome and Edge, which runs on the device. No API key or account, and messages are not sent to an outside translation service.
- **Others just open a page on their phone.** Same Wi-Fi, a URL or QR code, no app install.
- **Works for groups and many languages.** Each message is translated into every participant's language. 20 languages are available.
- **One file.** Python standard library only, no `pip install`.

### Requirements

- A laptop with Python 3.8+ (macOS or Windows)
- Desktop Chrome or Edge, latest version
- A Wi-Fi network where the laptop and phones can reach each other. Guest and public Wi-Fi networks often block this; a phone hotspot is a reliable fallback.

### Quick start

1. Start the server: `python3 hello_chat.py` (on Windows: `py hello_chat.py`). Add a port number to change it, e.g. `python3 hello_chat.py 9000`.
2. On the laptop, open `http://localhost:8765` in Chrome or Edge and join. This tab translates for everyone.
3. Have the others open the `http://192.168.…:8765` URL or scan the QR code shown on the page.
4. When a **"Download translation model"** button appears, click it. **Each click downloads one language pair in one direction** (e.g. Japanese → English).
5. Press `Ctrl+C` in the terminal to stop. The conversation is deleted.

**Tip:** download models before the event. Open the `http://192.168.…:8765` URL in a second laptop tab and join with the language you want to prepare (that tab acts like a phone), then click the buttons in the `localhost` tab. Models stay in Chrome once downloaded.

Keep the `localhost` tab open and the laptop awake while chatting, and open only one `localhost` tab.

### Privacy

Anyone on the same Wi-Fi who knows the URL can join and read the chat. Messages are held in memory only and disappear when the server stops. Translation happens on the laptop; the only internet access is downloading translation models and the QR code library.

### Tested on

macOS with Chrome 158 (Japanese, English, Spanish, Korean). Not yet tested on Windows or Edge.

## License

MIT License. See [LICENSE](LICENSE).
