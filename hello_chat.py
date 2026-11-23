#!/usr/bin/env python3
"""HELLO chat - login-free translated chat over the same Wi-Fi.

Run on the laptop:   python3 hello_chat.py
Then open http://localhost:8765 in desktop Chrome (or Edge) on the laptop,
and open the "Phone URL" it prints on the other person's phone.

Translation runs inside the laptop's Chrome with its built-in, on-device
Translator API, so no account, API key or extra install is needed.
Python 3.8+ standard library only.
"""
import json, queue, socket, sys, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
LANGS = {"ja","en","zh","zh-Hant","ko","es","fr","de","pt","it","vi","th","id","ru","ar","hi","tr","nl","pl","uk"}

lock = threading.Lock()
people = {}     # client id -> {"name","lang","canTr","conns"}
messages = []   # list of {"id","from","name","lang","text","tr":{},"t"}
listeners = set()

def broadcast(ev):
    data = json.dumps(ev, ensure_ascii=False)
    for q in list(listeners):
        q.put(data)

def people_list():
    return [{"id": k, "name": v["name"], "lang": v["lang"], "canTr": v["canTr"], "wait": v.get("wait", False)}
            for k, v in people.items() if v["conns"] > 0 and v["name"]]

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is sent
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def clean(s, n):
    return str(s or "").replace("\x00", "")[:n]

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            b = PAGE.replace("__LAN_URL__", f"http://{lan_ip()}:{PORT}").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(b); return
        if u.path == "/events":
            cid = clean(parse_qs(u.query).get("id", [""])[0], 40)
            q = queue.Queue()
            with lock:
                p = people.setdefault(cid, {"name": "", "lang": "en", "canTr": False, "conns": 0})
                p["conns"] += 1
                listeners.add(q)
                hello = {"type": "hello", "msgs": messages[-300:], "people": people_list()}
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            try:
                self.wfile.write(f"data: {json.dumps(hello, ensure_ascii=False)}\n\n".encode()); self.wfile.flush()
                with lock: broadcast({"type": "people", "people": people_list()})
                while True:
                    try:
                        d = q.get(timeout=15)
                        self.wfile.write(f"data: {d}\n\n".encode())
                    except queue.Empty:
                        self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass
            finally:
                with lock:
                    listeners.discard(q)
                    p["conns"] -= 1
                    broadcast({"type": "people", "people": people_list()})
            self.close_connection = True
            return
        self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 20000: return self.send_json({"error": "too big"}, 413)
        try: body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError: return self.send_json({"error": "bad json"}, 400)
        path = urlparse(self.path).path
        with lock:
            if path == "/join":
                cid = clean(body.get("id"), 40)
                lang = body.get("lang") if body.get("lang") in LANGS else "en"
                p = people.setdefault(cid, {"name": "", "lang": "en", "canTr": False, "conns": 0})
                p.update(name=clean(body.get("name"), 24).strip() or "?", lang=lang, canTr=bool(body.get("canTr")), wait=bool(body.get("wait")))
                broadcast({"type": "people", "people": people_list()})
                return self.send_json({"ok": True})
            if path == "/send":
                cid = clean(body.get("from"), 40); p = people.get(cid)
                text = clean(body.get("text"), 1500).strip()
                if not p or not text: return self.send_json({"error": "join first"}, 400)
                m = {"id": uuid.uuid4().hex[:12], "from": cid, "name": p["name"], "lang": p["lang"],
                     "text": text, "tr": {}, "t": int(time.time() * 1000)}
                messages.append(m); del messages[:-500]
                broadcast({"type": "msg", "m": m})
                return self.send_json({"ok": True, "id": m["id"]})
            if path == "/tr":
                mid = clean(body.get("id"), 40)
                m = next((x for x in reversed(messages) if x["id"] == mid), None)
                tr = body.get("tr") if isinstance(body.get("tr"), dict) else {}
                add = {k: clean(v, 3000) for k, v in tr.items() if k in LANGS and isinstance(v, str) and k not in (m or {}).get("tr", {})}
                if m and add:
                    m["tr"].update(add)
                    broadcast({"type": "tr", "id": mid, "tr": add})
                return self.send_json({"ok": True})
        self.send_json({"error": "not found"}, 404)

PAGE = r"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>HELLO chat</title>
<style>
:root{color-scheme:light dark;--bg:light-dark(#f6f4f1,#121314);--card:light-dark(#fff,#1d1f21);--ink:light-dark(#17181a,#eceae6);--mute:light-dark(#6b6a67,#9c9a95);--red:#d7332b;--line:light-dark(#e3e0da,#2c2e31);--me:light-dark(#fbe4e2,#3a1d1b)}
*{box-sizing:border-box;min-width:0}html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Hiragino Sans","Noto Sans JP","Segoe UI",system-ui,sans-serif}
button,input,select,textarea{font:inherit;color:inherit}button{cursor:pointer}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.wrap{max-width:720px;margin:0 auto;padding:0 max(4vw,14px)}
#join{min-height:100%;display:grid;place-items:center;padding:28px 14px}
.badge{width:min(440px,100%);background:var(--card);border-radius:22px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(0,0,0,.35)}
.top{background:var(--red);color:#fff;text-align:center;padding:22px 16px 16px}
.top h1{font:900 46px/1.05 "Arial Black",Arial,sans-serif;margin:0}.top p{margin:4px 0 0;font-size:15px}
form{padding:22px;display:grid;gap:14px}
label{font-size:14px;color:var(--mute);display:grid;gap:6px}
input,select,textarea{font-size:16px;border:1.5px solid var(--line);background:var(--bg);border-radius:12px;padding:11px 12px;min-height:46px;width:100%}
#name{font-weight:700;font-size:26px;text-align:center;border-style:dashed}
.go{background:var(--red);color:#fff;border:0;border-radius:12px;min-height:50px;font-weight:700;font-size:17px}
.note{font-size:13px;color:var(--mute);margin:0;text-align:center}
#share{margin:0 22px 22px;padding:14px;border:1.5px dashed var(--line);border-radius:14px;text-align:center;display:none}
#share b{display:block;font-size:18px;word-break:break-all;margin:4px 0}
#qr{display:inline-block;background:#fff;padding:8px;border-radius:8px;margin-top:6px}
#chat{display:none;height:100%;flex-direction:column}
header{background:var(--red);color:#fff}
header .wrap{display:flex;align-items:center;gap:8px;padding-block:10px;flex-wrap:wrap}
header b{font:900 20px/1 "Arial Black",Arial,sans-serif;margin-right:auto}
.chip{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.2);border-radius:99px;padding:4px 10px;font-size:13px;white-space:nowrap}
.chip i{width:8px;height:8px;border-radius:50%;background:#7be08f}
#bar{font-size:14px;color:var(--mute);text-align:center;padding:8px 0 0}
#bar button{background:var(--red);color:#fff;border:0;border-radius:10px;padding:10px 14px;margin:4px;font-weight:700}
#log{flex:1;overflow-y:auto;padding:10px 0 16px}
.msg{display:flex;flex-direction:column;align-items:flex-start;margin:10px 0}.msg.mine{align-items:flex-end}
.who{font-size:13px;color:var(--mute);margin:0 6px 3px}
.bub{max-width:min(86%,560px);background:var(--card);border:1px solid var(--line);border-radius:18px 18px 18px 6px;padding:10px 14px}
.mine .bub{background:var(--me);border-color:transparent;border-radius:18px 18px 6px 18px}
.main{font-size:18px;white-space:pre-wrap;overflow-wrap:anywhere}
.orig{font-size:13px;color:var(--mute);margin-top:6px;padding-top:6px;border-top:1px dashed var(--line);white-space:pre-wrap;overflow-wrap:anywhere}
.wait{color:var(--mute);font-style:italic}
.empty{text-align:center;color:var(--mute);margin:40px 10px}.empty strong{display:block;font-size:28px;color:var(--ink)}
footer{border-top:1px solid var(--line);background:var(--card);padding-bottom:env(safe-area-inset-bottom)}
footer .wrap{display:flex;gap:8px;padding-block:10px;align-items:flex-end}
textarea{resize:none;max-height:140px;flex:1}
.send{flex:none;width:52px;height:48px;border-radius:12px;border:0;background:var(--red);color:#fff;font-size:20px}
</style></head><body>
<section id="join"><div class="badge">
  <div class="top"><h1>HELLO</h1><p>my name is / はじめまして</p></div>
  <form id="jf">
    <input id="name" maxlength="24" placeholder="Your name / 名前" autocomplete="nickname" required>
    <label>I speak / 私の言語<select id="lang"></select></label>
    <button class="go">Start chatting / 話し始める</button>
    <p class="note">Write in your own language. The other person reads it in theirs.<br>自分の言語で書けば、相手には相手の言語で届きます。</p>
  </form>
  <div id="share">相手のスマホで開くURL / Open on the other phone<b>__LAN_URL__</b><div id="qr"></div></div>
</div></section>
<section id="chat">
  <header><div class="wrap"><b>HELLO</b><span id="peers"></span></div></header>
  <div class="wrap" id="bar"></div>
  <div id="log"><div class="wrap" id="logi"></div></div>
  <footer><div class="wrap"><textarea id="box" rows="1"></textarea><button class="send" id="send" aria-label="Send">➤</button></div></footer>
</section>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>
{
const LAN="__LAN_URL__";
const LANGS=[["ja","日本語"],["en","English"],["zh","中文（简体）"],["zh-Hant","中文（繁體）"],["ko","한국어"],["es","Español"],["fr","Français"],["de","Deutsch"],["pt","Português"],["it","Italiano"],["vi","Tiếng Việt"],["th","ไทย"],["id","Bahasa Indonesia"],["ru","Русский"],["ar","العربية"],["hi","हिन्दी"],["tr","Türkçe"],["nl","Nederlands"],["pl","Polski"],["uk","Українська"]];
const LN=Object.fromEntries(LANGS);
const UI={ja:{ph:"メッセージを入力…",empty:"話しかけてみよう",emptyS:"相手が参加すると上に名前が出ます。",alone:"相手を待っています… 相手のスマホで次を開いてください: ",tr:"翻訳中…",notr:"翻訳役のPC（ChromeかEdge）がまだ参加していません。",prep:"翻訳モデルをダウンロード",prepS:"初回だけ翻訳データの準備が必要です（1組ずつダウンロード）:",dl:"ダウンロード中:",setup:"翻訳役のPCで翻訳データを準備しています…",fail:"翻訳できない言語の組み合わせです（原文を表示）",you:"あなた",off:"接続が切れました。再接続中…"},
 en:{ph:"Type a message…",empty:"Say hello",emptyS:"When the other person joins, their name appears at the top.",alone:"Waiting for the other person… open this on their phone: ",tr:"Translating…",notr:"No translator laptop (Chrome/Edge) has joined yet.",prep:"Download translation model",prepS:"First-time setup for translation (one pair per click):",dl:"Downloading:",setup:"The translator laptop is preparing translation data…",fail:"This language pair can't be translated (showing original)",you:"you",off:"Disconnected. Reconnecting…"}};
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const store={get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const sel=$('lang');sel.innerHTML=LANGS.map(l=>`<option value="${l[0]}">${l[1]}</option>`).join('');
const nav=(navigator.language||'en');
const guess=LANGS.find(l=>l[0].toLowerCase()===nav.toLowerCase())||LANGS.find(l=>nav.toLowerCase().startsWith(l[0].slice(0,2)));
const saved=store.get('hello-me')||{};
sel.value=saved.lang||(guess?guess[0]:'en');if(saved.name)$('name').value=saved.name;
const myId=saved.id||(Date.now().toString(36)+Math.random().toString(36).slice(2,8));

const hasAPI='Translator' in self;
const isHostPage=location.hostname==='localhost'||location.hostname==='127.0.0.1';
if(isHostPage){$('share').style.display='block';try{new QRCode($('qr'),{text:LAN,width:160,height:160})}catch(e){$('qr').style.display='none'}}

let me=null,t=UI.en,msgs=[],people=[],online=false,barHTML=null,sentWait=null,busy=false,again=false;
// translators: ready models. broken: pair the browser can't translate. needGesture: pair that needs a click to download.
// loading: pair being downloaded -> progress 0..1. Chrome allows only ONE downloading create() per click.
const translators=new Map(),broken=new Set(),needGesture=new Set(),loading=new Map();

function render(){
  const box=$('logi');
  if(!msgs.length){box.innerHTML=`<div class="empty"><strong>${esc(t.empty)}</strong>${esc(t.emptyS)}</div>`}
  else box.innerHTML=msgs.map(m=>{
    const mine=m.from===myId;let main,orig='';
    if(m.lang===me.lang)main=esc(m.text);
    else if(m.tr[me.lang]){main=esc(m.tr[me.lang]);orig=esc(m.text)}
    else if(broken.has(m.lang+'>'+me.lang)){main=esc(m.text);orig=esc(t.fail)}
    else{main=`<span class="wait">${esc(!anyTranslator()?t.notr:helperWaiting()?t.setup:t.tr)}</span>`;orig=esc(m.text)}
    return `<div class="msg${mine?' mine':''}"><div class="who">${esc(mine?t.you:m.name)}</div><div class="bub"><div class="main">${main}</div>${orig?`<div class="orig">${orig}</div>`:''}</div></div>`}).join('');
  const lg=$('log');lg.scrollTop=lg.scrollHeight;
  $('peers').innerHTML=people.map(p=>`<span class="chip"><i></i>${esc(p.name)}${p.id===myId?' ('+esc(t.you)+')':''} · ${esc(LN[p.lang]||'?')}</span>`).join(' ');
  const pair=k=>k.split('>').map(l=>esc(LN[l]||l)).join(' → ');
  let bar='';
  if(!online)bar=esc(t.off);
  else if(amHelper()&&(needGesture.size||loading.size)){
    const next=[...needGesture];
    // one button = one pair: Chrome lets each click start only one model download.
    // Button first and progress below it, so the button doesn't jump when a download finishes.
    if(next.length)bar=`${esc(t.prepS)} ${next.map(pair).join(', ')}<br><button id="prep">${esc(t.prep)}: ${pair(next[0])}${next.length>1?` (1/${next.length})`:''}</button>`;
    if(loading.size)bar+=`${bar?'<br>':''}${esc(t.dl)} ${[...loading].map(([k,p])=>`${pair(k)} ${Math.round(p*100)}%`).join(', ')}`;
  }
  else if(people.filter(p=>p.id!==myId).length===0)bar=esc(t.alone)+esc(LAN);
  else if(!anyTranslator())bar=esc(t.notr);
  else if(helperWaiting())bar=esc(t.setup);
  // only touch the DOM when the bar changed, so incoming messages don't swap the button out from under a click
  if(bar!==barHTML){barHTML=bar;$('bar').innerHTML=bar;const pb=$('prep');if(pb)pb.onclick=prepare}
  syncWait();
}
const anyTranslator=()=>people.some(p=>p.canTr);
function helperId(){return people.filter(p=>p.canTr).map(p=>p.id).sort()[0]}
function amHelper(){return hasAPI&&helperId()===myId}
const helperWaiting=()=>!!(people.find(p=>p.id===helperId())||{}).wait;
const joinBody=()=>({id:myId,name:me.name,lang:me.lang,canTr:hasAPI,wait:amHelper()&&(needGesture.size+loading.size)>0});
function syncWait(){ // tell phones when the helper laptop is waiting for a model download
  if(!online||!amHelper())return;
  const w=joinBody().wait;if(w===sentWait)return;sentWait=w;post('/join',joinBody());
}

async function avail(f,to){try{return await Translator.availability({sourceLanguage:f,targetLanguage:to})}catch(e){return 'unavailable'}}
async function getTr(from,to){
  const k=from+'>'+to;
  if(translators.has(k))return translators.get(k);
  if(broken.has(k)||loading.has(k))return null;
  const a=await avail(from,to);
  if(translators.has(k))return translators.get(k);
  if(a==='unavailable'){broken.add(k);needGesture.delete(k);return null}
  if(a!=='available'){needGesture.add(k);return null}  // downloadable/downloading: wait for a click
  needGesture.delete(k);
  try{const tr=await Translator.create({sourceLanguage:from,targetLanguage:to});translators.set(k,tr);return tr}
  catch(e){console.warn('[HELLO] create',k,e);needGesture.add(k);return null}
}
function prepare(){ // runs inside the click: start exactly one download (a 2nd create() in the same click gets NotAllowedError)
  const k=[...needGesture][0];if(!k)return;
  const[f,to]=k.split('>');
  needGesture.delete(k);loading.set(k,0);
  Translator.create({sourceLanguage:f,targetLanguage:to,monitor(m){m.addEventListener('downloadprogress',e=>{loading.set(k,e.loaded);render()})}})
    .then(tr=>translators.set(k,tr))
    .catch(async e=>{console.warn('[HELLO] download',k,e);if(await avail(f,to)==='unavailable')broken.add(k);else needGesture.add(k)})
    .finally(()=>{loading.delete(k);render();work()});
  render();
}
async function work(){ // one pass at a time; calls that arrive meanwhile trigger one more pass
  if(!amHelper())return;
  if(busy){again=true;return}
  busy=true;
  try{do{again=false;await workOnce();render()}while(again)}
  finally{busy=false}
}
async function workOnce(){
  const langs=[...new Set(people.map(p=>p.lang))];
  for(const a of langs)for(const b of langs)if(a!==b)await getTr(a,b); // get models ready before the first message
  render();
  for(const m of msgs){
    const out={};
    for(const l of langs){
      if(l===m.lang||m.tr[l])continue;
      const tr=await getTr(m.lang,l);if(!tr)continue;
      try{out[l]=await tr.translate(m.text)}catch(e){console.warn('[HELLO] translate',m.lang+'>'+l,e)}
    }
    if(Object.keys(out).length){Object.assign(m.tr,out);post('/tr',{id:m.id,tr:out})}
  }
}
function post(u,b){return fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).catch(()=>{})}
function connect(){
  const es=new EventSource('/events?id='+encodeURIComponent(myId));
  es.onopen=()=>{online=true;const b=joinBody();sentWait=b.wait;post('/join',b);render()};
  es.onerror=()=>{online=false;render()};
  es.onmessage=e=>{
    let d;try{d=JSON.parse(e.data)}catch(x){return}
    if(d.type==='hello'){msgs=d.msgs;people=d.people}
    else if(d.type==='people')people=d.people;
    else if(d.type==='msg'&&!msgs.some(m=>m.id===d.m.id))msgs.push(d.m);
    else if(d.type==='tr'){const m=msgs.find(x=>x.id===d.id);if(m)Object.assign(m.tr,d.tr)}
    render();work();
  };
}
function grow(){const b=$('box');b.style.height='auto';b.style.height=Math.min(b.scrollHeight,140)+'px'}
function send(){const b=$('box');const text=b.value.trim();if(!text)return;b.value='';grow();post('/send',{from:myId,text})}
$('jf').addEventListener('submit',e=>{
  e.preventDefault();
  me={name:$('name').value.trim().slice(0,24)||'?',lang:sel.value};
  store.set('hello-me',{...me,id:myId});
  t=UI[me.lang]||UI.en;document.documentElement.lang=me.lang;$('box').placeholder=t.ph;
  $('join').style.display='none';$('chat').style.display='flex';
  render();connect();
});
$('send').addEventListener('click',send);
$('box').addEventListener('input',grow);
$('box').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();send()}});
}
</script></body></html>"""

if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), H)
    srv.daemon_threads = True
    ip = lan_ip()
    print("HELLO chat is running.")
    print(f"  Laptop (open in Chrome/Edge): http://localhost:{PORT}")
    print(f"  Phone URL (same Wi-Fi):       http://{ip}:{PORT}")
    print("Press Ctrl+C to stop.", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
