"""Build the three quick start pages (ja / easy ja / en) from quickstart_src.html.

Edit quickstart_src.html (the Japanese page) and the EN / EASY text lists below, then run:

    python3 guide_src/build_quickstart.py

It writes hello_chat_quickstart.html, _easy.html and _en.html to the repository root
and stops with an error if a Japanese sentence it should translate is no longer in the source.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
BASE = "https://msysng.github.io/hello-translate-chat/"
src = open(os.path.join(HERE, "quickstart_src.html"), encoding="utf-8").read()
qr = subprocess.run([sys.executable, os.path.join(HERE, "qr.py")], capture_output=True, text=True).stdout.strip()
src = src.replace("{{QR}}", qr)

PAGES = [("ja", "hello_chat_quickstart.html", "日本語"),
         ("easy", "hello_chat_quickstart_easy.html", "やさしい にほんご"),
         ("en", "hello_chat_quickstart_en.html", "English")]

def r(k, rd):  # ruby
    return f"<ruby>{k}<rt>{rd}</rt></ruby>"

EN = [
    ('<html lang="ja">', '<html lang="en">'),
    ('<title>HELLO chat クイックスタート</title>', '<title>HELLO chat Quick Start</title>'),
    ('<p class="sub">chat · クイックスタート</p>', '<p class="sub">chat · quick start</p>'),
    ('aria-label="言語"', 'aria-label="Language"'),
    ('<p class="lead">ラップトップ1台とスマホで、言葉の違う人とすぐ話せます。<br>4ステップ、5分で試せます。</p>',
     '<p class="lead">Talk with people who speak other languages, using one laptop and their phones.<br>Four steps, about five minutes.</p>'),
    ('<h2>こんなしくみです</h2>', '<h2>How it works</h2>'),
    ('aria-label="ラップトップがWi-Fi経由で2台のスマホとつながり、「こんにちは！」が英語とスペイン語に翻訳されて届く図"',
     'aria-label="A laptop connects to two phones over Wi-Fi; a Japanese message arrives in English on one phone and in Spanish on the other"'),
    ('font-weight="700">ラップトップ = 翻訳役</text>', 'font-weight="700">Laptop = translator</text>'),
    ('text-anchor="middle">同じ Wi-Fi</text>', 'text-anchor="middle">Same Wi-Fi</text>'),
    ('Aiko · 翻訳</text>', 'Aiko · translated</text>'),
    ('font-weight="700">スマホ = 見て書くだけ</text>', 'font-weight="700">Phones = read &amp; write</text>'),
    ('<div><b>ラップトップ</b>の Chrome が、全員のメッセージを各自の言語に翻訳します。</div>',
     "<div>Chrome on the <b>laptop</b> translates every message into each person's language.</div>"),
    ('<div><b>参加者のスマホ</b>はQRコードを読むだけ。アプリもログインも要りません。</div>',
     '<div><b>Phones</b> just scan a QR code. No app, no sign-in.</div>'),
    ('<h2>用意するもの</h2>', '<h2>What you need</h2>'),
    ('<li><b>PC</b>ラップトップ（Mac / Windows）と Chrome</li>', '<li><b>PC</b>A laptop (Mac or Windows) with Chrome</li>'),
    ('<li><b>SP</b>参加者のスマホ</li>', "<li><b>SP</b>Everyone's phones</li>"),
    ('<li><b>Wi</b>みんなで同じ Wi-Fi</li>', '<li><b>Wi</b>One Wi-Fi network for everyone</li>'),
    ('<summary>初めてのときだけ：ダウンロードと Python の準備</summary>', '<summary>First time only: download the tool and install Python</summary>'),
    ('<li><a href="https://github.com/MsYsng/hello-translate-chat">GitHub のページ</a>の <b>Code</b> → <b>Download ZIP</b> でダウンロードし、ZIP を開いてフォルダにします。</li>',
     '<li>On the <a href="https://github.com/MsYsng/hello-translate-chat">GitHub page</a>, click <b>Code</b> → <b>Download ZIP</b>, then unzip it.</li>'),
    ('<li>Python がなければ <a href="https://www.python.org/downloads/">python.org</a> から入れます。Windows ではインストール画面の「Add python.exe to PATH」にチェックを入れてください。</li>',
     '<li>If you don\'t have Python, install it from <a href="https://www.python.org/downloads/">python.org</a>. On Windows, tick "Add python.exe to PATH" in the installer.</li>'),
    ('<h2>4ステップで始める</h2>', '<h2>Start in four steps</h2>'),
    ('<h3>起動する</h3>', '<h3>Start it</h3>'),
    ('<p>フォルダの中の起動用ファイルをダブルクリック。ブラウザに<b>管理画面</b>が開きます。</p>',
     '<p>Double-click the launcher in the folder. The <b>admin screen</b> opens in your browser.</p>'),
    ('<p class="small">Mac は <code>HELLO-chat.command</code>、Windows は <code>HELLO-chat.bat</code>。Mac で開けないときは右クリック →「開く」。</p>',
     '<p class="small"><code>HELLO-chat.command</code> on Mac, <code>HELLO-chat.bat</code> on Windows. If a Mac won\'t open it, right-click it and choose Open.</p>'),
    ('aria-label="起動用ファイルをダブルクリックする絵"', 'aria-label="Double-clicking the launcher file"'),
    ('<h3>自分も参加する</h3>', '<h3>Join on the laptop</h3>'),
    ('<p>管理画面の <span class="ui">チャット画面を開く</span> を押し、名前と言語を選んで <span class="ui">話し始める</span>。</p>',
     '<p>On the admin screen, click <span class="ui">Open the chat</span>. Enter your name, pick your language and click <span class="ui">Start chatting</span>.</p>'),
    ('<p class="small">このラップトップの画面が翻訳役になります。会話中は閉じないでください。</p>',
     '<p class="small">This laptop window does the translating. Keep it open while you talk.</p>'),
    ('aria-label="名前と言語を入れて話し始めるボタンを押す画面の絵"', 'aria-label="Entering a name and language, then clicking Start chatting"'),
    ('font-size="10">名前</text>', 'font-size="10">Name</text>'),
    ('font-size="10">言語</text>', 'font-size="10">Language</text>'),
    ('<text x="40" y="75" font-size="12">Aiko</text>', '<text x="40" y="75" font-size="12">Sam</text>'),
    ('font-size="12">日本語 ▾</text>', 'font-size="12">English ▾</text>'),
    ('font-weight="700">話し始める</text>', 'font-weight="700">Start chatting</text>'),
    ('<rect class="s-red" x="130" y="100" width="90" height="22" rx="11"/>', '<rect class="s-red" x="128" y="100" width="100" height="22" rx="11"/>'),
    ('<text class="t-white" x="175" y="115" font-size="11"', '<text class="t-white" x="178" y="115" font-size="10.5"'),
    ('<h3>相手を招く</h3>', '<h3>Invite others</h3>'),
    ('<p>画面に出る<b>QRコード</b>を、相手のスマホのカメラで読んでもらいます。相手も名前と言語を選べば参加完了です。</p>',
     '<p>Have others scan the <b>QR code</b> on the screen with their phone camera. They enter a name and language, and they\'re in.</p>'),
    ('<p class="small">開けないときは、スマホの Wi-Fi 名がラップトップと<b>同じか</b>を確認。</p>',
     '<p class="small">Page won\'t open? Check the phone is on the <b>same</b> Wi-Fi network as the laptop.</p>'),
    ('aria-label="ラップトップのQRコードをスマホのカメラで読む絵"', "aria-label=\"A phone camera scanning the QR code on the laptop\""),
    ('<h3>話す</h3>', '<h3>Talk</h3>'),
    ('<p>自分の言語で書けば、相手には相手の言語で届きます。</p>', '<p>Write in your language. Everyone else reads it in theirs.</p>'),
    ('<p>ラップトップに <span class="ui">翻訳モデルをダウンロード</span> ボタンが出たら押してください。初回だけ、言語の組み合わせごとに1回必要です。</p>',
     '<p>If a <span class="ui">Download translation model</span> button appears on the laptop, click it. It\'s needed once for each language pair, the first time only.</p>'),
    ('aria-label="英語のメッセージに日本語訳が付いて表示されるチャットの絵"', 'aria-label="A Japanese message shown in English in the chat"'),
    ('font-weight="700">はじめまして！</text>', 'font-weight="700">Nice to meet you!</text>'),
    ('font-size="11">Nice to meet you!</text>', 'font-size="11">はじめまして！</text>'),
    ('font-size="10">Sam · English</text>', 'font-size="10">Aiko · 日本語</text>'),
    ('font-weight="700">よろしく！</text>', 'font-weight="700">Hi, I\'m Sam!</text>'),
    ('text-anchor="end">あなた · 日本語</text>', 'text-anchor="end">you · English</text>'),
    ('<p class="prep">終わったら、管理画面の <span class="ui">サーバーを終了</span> を押します。会話はすべて消えます。</p>',
     '<p class="prep">When you\'re done, click <span class="ui">Stop server</span> on the admin screen. The whole conversation is deleted.</p>'),
    ('<h2>つまずきやすい3つ</h2>', '<h2>Three common snags</h2>'),
    ('<div><b>スマホで開けない</b><span>Wi-Fi の名前がラップトップと完全に同じか確認。ゲスト用 Wi-Fi なら、スマホのテザリングに全員でつなぎます。</span></div>',
     '<div><b>A phone can\'t open the page</b><span>Check its Wi-Fi network name matches the laptop\'s exactly. On guest Wi-Fi, have everyone join a phone hotspot instead.</span></div>'),
    ('<div><b>翻訳が止まった</b><span>ラップトップのチャット画面を閉じたり、ふたを閉じたりすると全員の翻訳が止まります。</span></div>',
     '<div><b>Translation stopped</b><span>Closing the chat window on the laptop, or closing its lid, stops translation for everyone.</span></div>'),
    ('<div><b>ボタンが何度も出る</b><span>翻訳モデルは1回押すと1組ずつダウンロードされます。ボタンが消えるまで押してください。</span></div>',
     '<div><b>The button keeps coming back</b><span>Each click downloads one language pair. Keep clicking until it goes away.</span></div>'),
    ('<p>事前の準備、Claude で翻訳する方法、困ったときの対処は詳細版に、参加者に見せる印刷用カードは<a href="https://msysng.github.io/hello-translate-chat/hello_chat_card.html">参加者カード</a>にまとめています。</p>',
     '<p>Preparing before an event, translating with Claude and troubleshooting are in the full guide (in Japanese) and the README. For a card to show participants, print the <a href="https://msysng.github.io/hello-translate-chat/hello_chat_card.html">participant card</a> (multilingual).</p>'),
    ('>詳しい使い方ガイド →</a>', '>Full guide (Japanese) →</a>'),
    ('<footer class="wrap">HELLO chat（hello_chat.py）のクイックスタート。</footer>',
     '<footer class="wrap">Quick start for HELLO chat (hello_chat.py). <a href="https://github.com/MsYsng/hello-translate-chat#english">README in English</a></footer>'),
]

PC, TR, GA, SM = "パソコン", r("翻訳", "ほんやく"), r("画面", "がめん"), "スマホ"
EASY = [
    ('<title>HELLO chat クイックスタート</title>', '<title>HELLO chat やさしい にほんご</title>'),
    ('<p class="sub">chat · クイックスタート</p>', '<p class="sub">chat · はじめかた（やさしい にほんご）</p>'),
    ('<p class="lead">ラップトップ1台とスマホで、言葉の違う人とすぐ話せます。<br>4ステップ、5分で試せます。</p>',
     f'<p class="lead">{PC} 1{r("台","だい")}と {SM}で、ちがう {r("言葉","ことば")}の {r("人","ひと")}と {r("話","はな")}せます。<br>4つの ステップで できます。</p>'),
    ('<h2>こんなしくみです</h2>', '<h2>どう うごくの？</h2>'),
    ('aria-label="ラップトップがWi-Fi経由で2台のスマホとつながり、「こんにちは！」が英語とスペイン語に翻訳されて届く図"',
     'aria-label="パソコンと スマホ2だいが Wi-Fiで つながっている え。こんにちは が えいごと スペインごに なって とどく"'),
    ('font-weight="700">ラップトップ = 翻訳役</text>', 'font-weight="700">パソコン = ほんやく する</text>'),
    ('text-anchor="middle">同じ Wi-Fi</text>', 'text-anchor="middle">おなじ Wi-Fi</text>'),
    ('Aiko · 翻訳</text>', 'Aiko · ほんやく</text>'),
    ('font-weight="700">スマホ = 見て書くだけ</text>', 'font-weight="700">スマホ = よむ・かく</text>'),
    ('<div><b>ラップトップ</b>の Chrome が、全員のメッセージを各自の言語に翻訳します。</div>',
     f'<div><b>{PC}</b>の Chrome が、みんなの メッセージを {TR}します。</div>'),
    ('<div><b>参加者のスマホ</b>はQRコードを読むだけ。アプリもログインも要りません。</div>',
     f'<div><b>{SM}</b>は QRコードを {r("読","よ")}むだけです。アプリは いりません。</div>'),
    ('<h2>用意するもの</h2>', f'<h2>{r("用意","ようい")}する もの</h2>'),
    ('<li><b>PC</b>ラップトップ（Mac / Windows）と Chrome</li>', f'<li><b>PC</b>{PC}（Mac / Windows）と Chrome</li>'),
    ('<li><b>SP</b>参加者のスマホ</li>', f'<li><b>SP</b>みんなの {SM}</li>'),
    ('<li><b>Wi</b>みんなで同じ Wi-Fi</li>', f'<li><b>Wi</b>みんな {r("同","おな")}じ Wi-Fi</li>'),
    ('<summary>初めてのときだけ：ダウンロードと Python の準備</summary>', f'<summary>{r("初","はじ")}めての ときだけ：ダウンロードと Python</summary>'),
    ('<li><a href="https://github.com/MsYsng/hello-translate-chat">GitHub のページ</a>の <b>Code</b> → <b>Download ZIP</b> でダウンロードし、ZIP を開いてフォルダにします。</li>',
     f'<li><a href="https://github.com/MsYsng/hello-translate-chat">GitHub の ページ</a>で <b>Code</b> → <b>Download ZIP</b> を {r("押","お")}します。ZIP を {r("開","ひら")}きます。</li>'),
    ('<li>Python がなければ <a href="https://www.python.org/downloads/">python.org</a> から入れます。Windows ではインストール画面の「Add python.exe to PATH」にチェックを入れてください。</li>',
     f'<li>Python が ないときは、<a href="https://www.python.org/downloads/">python.org</a> から {r("入","い")}れます。Windows では「Add python.exe to PATH」に チェックを {r("入","い")}れます。</li>'),
    ('<h2>4ステップで始める</h2>', f'<h2>4つの ステップ</h2>'),
    ('<h3>起動する</h3>', f'<h3>{r("始","はじ")}める</h3>'),
    ('<p>フォルダの中の起動用ファイルをダブルクリック。ブラウザに<b>管理画面</b>が開きます。</p>',
     f'<p>フォルダの {r("中","なか")}の ファイルを ダブルクリックします。<b>{r("管理","かんり")}{GA}</b>が {r("開","ひら")}きます。</p>'),
    ('<p class="small">Mac は <code>HELLO-chat.command</code>、Windows は <code>HELLO-chat.bat</code>。Mac で開けないときは右クリック →「開く」。</p>',
     f'<p class="small">Mac は <code>HELLO-chat.command</code>、Windows は <code>HELLO-chat.bat</code> です。{r("開","ひら")}かないときは、{r("右","みぎ")}クリック →「{r("開","ひら")}く」を {r("押","お")}します。</p>'),
    ('aria-label="起動用ファイルをダブルクリックする絵"', 'aria-label="ファイルを ダブルクリックする え"'),
    ('<h3>自分も参加する</h3>', f'<h3>{r("自分","じぶん")}も {r("入","はい")}る</h3>'),
    ('<p>管理画面の <span class="ui">チャット画面を開く</span> を押し、名前と言語を選んで <span class="ui">話し始める</span>。</p>',
     f'<p>{r("管理","かんり")}{GA}の <span class="ui">チャット画面を開く</span> を {r("押","お")}します。{r("名前","なまえ")}と {r("言葉","ことば")}を {r("選","えら")}んで、<span class="ui">話し始める</span> を {r("押","お")}します。</p>'),
    ('<p class="small">このラップトップの画面が翻訳役になります。会話中は閉じないでください。</p>',
     f'<p class="small">この {GA}が {TR}を します。{r("話","はな")}している あいだは {r("閉","と")}じないで ください。</p>'),
    ('aria-label="名前と言語を入れて話し始めるボタンを押す画面の絵"', 'aria-label="なまえと ことばを いれて ボタンを おす え"'),
    ('<h3>相手を招く</h3>', f'<h3>{r("相手","あいて")}を よぶ</h3>'),
    ('<p>画面に出る<b>QRコード</b>を、相手のスマホのカメラで読んでもらいます。相手も名前と言語を選べば参加完了です。</p>',
     f'<p>{GA}の <b>QRコード</b>を、{r("相手","あいて")}の {SM}の カメラで {r("読","よ")}んで もらいます。{r("相手","あいて")}も {r("名前","なまえ")}と {r("言葉","ことば")}を {r("選","えら")}びます。</p>'),
    ('<p class="small">開けないときは、スマホの Wi-Fi 名がラップトップと<b>同じか</b>を確認。</p>',
     f'<p class="small">{r("開","ひら")}かないときは、{SM}と {PC}の Wi-Fi の {r("名前","なまえ")}が <b>{r("同","おな")}じか</b> 見て ください。</p>'),
    ('aria-label="ラップトップのQRコードをスマホのカメラで読む絵"', 'aria-label="パソコンの QRコードを スマホで よむ え"'),
    ('<h3>話す</h3>', f'<h3>{r("話","はな")}す</h3>'),
    ('<p>自分の言語で書けば、相手には相手の言語で届きます。</p>',
     f'<p>{r("自分","じぶん")}の {r("言葉","ことば")}で {r("書","か")}きます。{r("相手","あいて")}には {r("相手","あいて")}の {r("言葉","ことば")}で とどきます。</p>'),
    ('<p>ラップトップに <span class="ui">翻訳モデルをダウンロード</span> ボタンが出たら押してください。初回だけ、言語の組み合わせごとに1回必要です。</p>',
     f'<p>{PC}に <span class="ui">翻訳モデルをダウンロード</span> の ボタンが {r("出","で")}たら、{r("押","お")}して ください。{r("初","はじ")}めての ときだけ です。</p>'),
    ('aria-label="英語のメッセージに日本語訳が付いて表示されるチャットの絵"', 'aria-label="えいごの メッセージが にほんごに なって とどく え"'),
    ('<h2>つまずきやすい3つ</h2>', f'<h2>こまったときは</h2>'),
    ('<p class="prep">終わったら、管理画面の <span class="ui">サーバーを終了</span> を押します。会話はすべて消えます。</p>',
     f'<p class="prep">{r("終","お")}わったら、{r("管理","かんり")}{GA}の <span class="ui">サーバーを終了</span> を {r("押","お")}します。{r("話","はな")}した ことは ぜんぶ {r("消","き")}えます。</p>'),
    ('<div><b>スマホで開けない</b><span>Wi-Fi の名前がラップトップと完全に同じか確認。ゲスト用 Wi-Fi なら、スマホのテザリングに全員でつなぎます。</span></div>',
     f'<div><b>{SM}で {r("開","ひら")}かない</b><span>Wi-Fi の {r("名前","なまえ")}が {PC}と {r("同","おな")}じか {r("見","み")}て ください。だめなときは、{SM}の テザリングに みんなで つなぎます。</span></div>'),
    ('<div><b>翻訳が止まった</b><span>ラップトップのチャット画面を閉じたり、ふたを閉じたりすると全員の翻訳が止まります。</span></div>',
     f'<div><b>{TR}が {r("止","と")}まった</b><span>{PC}の チャット{GA}や ふたを {r("閉","と")}じると、{TR}が {r("止","と")}まります。</span></div>'),
    ('<div><b>ボタンが何度も出る</b><span>翻訳モデルは1回押すと1組ずつダウンロードされます。ボタンが消えるまで押してください。</span></div>',
     f'<div><b>ボタンが {r("何度","なんど")}も {r("出","で")}る</b><span>1{r("回","かい")} {r("押","お")}すと、1つ ダウンロードします。ボタンが {r("消","き")}えるまで {r("押","お")}して ください。</span></div>'),
    ('<p>事前の準備、Claude で翻訳する方法、困ったときの対処は詳細版に、参加者に見せる印刷用カードは<a href="https://msysng.github.io/hello-translate-chat/hello_chat_card.html">参加者カード</a>にまとめています。</p>',
     f'<p>もっと くわしい {r("説明","せつめい")}は、こちらです（ふつうの にほんご）。{r("参加者","さんかしゃ")}に わたす カードは <a href="https://msysng.github.io/hello-translate-chat/hello_chat_card.html">こちら</a>。</p>'),
    ('>詳しい使い方ガイド →</a>', '>くわしい せつめい →</a>'),
    ('<footer class="wrap">HELLO chat（hello_chat.py）のクイックスタート。</footer>',
     '<footer class="wrap">HELLO chat（hello_chat.py）の はじめかた。</footer>'),
]
# easy ja shows the same mock screens as ja; only "Aiko · 翻訳" labels change (above)

def langs(cur):
    out = []
    for key, fn, label in PAGES:
        cur_attr = ' aria-current="page"' if key == cur else ""
        lang = {"ja": "ja", "easy": "ja", "en": "en"}[key]
        out.append(f'<a href="{BASE}{fn}" hreflang="{lang}"{cur_attr}>{label}</a>')
    return "".join(out)

def apply(s, reps, name):
    for a, b in reps:
        n = s.count(a)
        if n == 0:
            sys.exit(f"{name}: not found: {a[:70]}")
        s = s.replace(a, b)
    return s

for key, fn, _ in PAGES:
    s = src
    if key == "en":
        s = apply(s, EN, key)
    elif key == "easy":
        s = apply(s, EASY, key)
        s = s.replace(".hero .lead{", "rt{font-size:.55em;font-weight:400;letter-spacing:0}\nbody{line-height:2.05}.st .tx p,.st .small,.trip span,.how-cap,.prep,.need li{line-height:2.1}.st h3{line-height:1.9}\n.hero .lead{", 1)
    s = s.replace("{{LANGS}}", langs(key))
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(s)
    print("wrote", fn)

en = open(os.path.join(OUT, "hello_chat_quickstart_en.html"), encoding="utf-8").read()
body = en.split("</style>", 1)[1]
left = re.findall(r"[぀-ヿ一-鿿][^<\n]{0,30}", body)
print("Japanese left in en:", left)
