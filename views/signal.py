"""Aba Environmental Signal Router (dados reais, sem chaves de API) — painel escuro com globo 3D."""
import html, json, math, os, tempfile
from datetime import datetime, timezone

import requests
import streamlit as st

from compat import embed_html
from router import signals as S
from router.i18n import T

NEWS_URL = os.getenv("NEWS_JSON_URL", "https://amaurialmeida.github.io/environmental-portfolio/news.json")
HEADLINE_SECONDS = 12          # ~12 s por manchete → 25 manchetes ≈ 5 minutos
DEFAULT_SHOWN = 12

CSS = """
<style>
#MainMenu,footer{visibility:hidden}
.block-container{max-width:1440px;padding:20px 20px 40px}
[class*="st-key-card"]{background:rgba(8,20,38,.78);border:1px solid rgba(80,150,255,.22);border-radius:18px;padding:20px;box-shadow:0 0 30px rgba(34,193,238,.08)}
.sec{font-size:18px;font-weight:700;margin-bottom:12px;color:#e5e7eb}
.meta{color:#94a3b8;font-size:14px;margin-bottom:8px}
</style>
"""

# Textos extras do painel (9 idiomas)
X = {
    "pt": {"sub": "Inteligência ambiental em tempo real", "tag": "Observar · Analisar · Proteger", "online": "Sistema online", "log": "Log de inteligência ambiental"},
    "en": {"sub": "Real-time environmental intelligence", "tag": "Observe · Analyze · Protect", "online": "System online", "log": "Environmental intelligence log"},
    "es": {"sub": "Inteligencia ambiental en tiempo real", "tag": "Observar · Analizar · Proteger", "online": "Sistema en línea", "log": "Registro de inteligencia ambiental"},
    "it": {"sub": "Intelligence ambientale in tempo reale", "tag": "Osserva · Analizza · Proteggi", "online": "Sistema online", "log": "Log di intelligence ambientale"},
    "fr": {"sub": "Renseignement environnemental en temps réel", "tag": "Observer · Analyser · Protéger", "online": "Système en ligne", "log": "Journal de renseignement environnemental"},
    "de": {"sub": "Umwelt-Intelligence in Echtzeit", "tag": "Beobachten · Analysieren · Schützen", "online": "System online", "log": "Umwelt-Intelligence-Log"},
    "zh": {"sub": "实时环境情报", "tag": "观察 · 分析 · 守护", "online": "系统在线", "log": "环境情报日志"},
    "ar": {"sub": "الاستخبارات البيئية في الوقت الفعلي", "tag": "راقب · حلّل · احمِ", "online": "النظام متصل", "log": "سجل الاستخبارات البيئية"},
    "el": {"sub": "Περιβαλλοντική πληροφόρηση σε πραγματικό χρόνο", "tag": "Παρατήρηση · Ανάλυση · Προστασία", "online": "Σύστημα online", "log": "Αρχείο περιβαλλοντικής πληροφόρησης"},
}

DASH_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:radial-gradient(ellipse at 50% 0%,#0b2347 0%,#050b16 60%);color:#e5eefc;font-family:'Segoe UI',Inter,system-ui,sans-serif;overflow-x:hidden}
body{padding:14px}
.top{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:6px 6px 14px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}
.logo{width:44px;height:44px;border-radius:10px;background:linear-gradient(135deg,#22c1ee,#2ecc71);display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 0 18px rgba(34,193,238,.5)}
.brand h1{font-size:1.25rem;letter-spacing:.06em;text-transform:uppercase;color:#e8f3ff;font-weight:700}
.brand small{display:block;font-size:.68rem;letter-spacing:.16em;color:#7fb4e8;text-transform:uppercase}
.tag{font-size:.72rem;letter-spacing:.3em;color:#7fa6cf;text-transform:uppercase;text-align:center}
.right{display:flex;align-items:center;gap:14px;font-size:.85rem;color:#b9d2ee}
.pill{display:flex;align-items:center;gap:7px;border:1px solid rgba(46,204,113,.5);background:rgba(46,204,113,.1);color:#4ade80;border-radius:999px;padding:4px 12px;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase}
.pill i{width:8px;height:8px;border-radius:50%;background:#4ade80;box-shadow:0 0 8px #4ade80;animation:bl 1.6s infinite}
@keyframes bl{50%{opacity:.3}}
.grid{display:grid;grid-template-columns:300px minmax(0,1fr) 340px;gap:14px;margin-bottom:14px}
.panel{background:rgba(8,20,38,.78);border:1px solid rgba(80,150,255,.22);border-radius:16px;padding:14px;box-shadow:0 0 30px rgba(34,193,238,.06);min-width:0;position:relative}
.ph{display:flex;align-items:center;gap:8px;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:#cfe3fa;margin-bottom:10px;font-weight:600}
.ph b{color:#22c1ee;font-weight:700}
.ev{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.07)}
.ev:last-child{border-bottom:none}
.tile{width:50px;height:50px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;font-size:24px;border:1px solid rgba(255,255,255,.15)}
.ev .t{flex:1;min-width:0}
.ev .t strong{display:block;font-size:.82rem;line-height:1.25;font-weight:600;color:#eaf3ff;overflow-wrap:anywhere}
.ev .t small{color:#7f9bbb;font-size:.7rem}
.ev .v{font-weight:700;font-size:.85rem;white-space:nowrap}
.empty{color:#7f9bbb;font-size:.85rem;padding:10px 0}
.globe-panel{padding:0;overflow:hidden;display:flex;flex-direction:column}
#globe{flex:none;height:500px;position:relative;cursor:grab;overflow:hidden}
.chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;padding:10px 12px 12px;background:linear-gradient(0deg,rgba(5,11,22,.9),rgba(5,11,22,0))}
.chip{border:1px solid rgba(130,170,220,.4);background:rgba(10,24,44,.8);color:#cfe3fa;border-radius:999px;padding:5px 12px;font-size:.76rem;cursor:pointer;display:flex;gap:6px;align-items:center;transition:all .2s;font-family:inherit}
.chip:hover{border-color:var(--c)}
.chip.on{background:var(--c);border-color:var(--c);color:#04101f;font-weight:700;box-shadow:0 0 14px var(--c)}
.chip em{font-style:normal;opacity:.75;font-size:.7rem}
#msg{position:absolute;inset:0;display:none;align-items:center;justify-content:center;color:#7f9bbb;text-align:center;padding:20px}
.chartbox{height:230px;position:relative}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.kpi{border:1px solid rgba(80,150,255,.25);border-radius:12px;padding:10px 4px;text-align:center;background:rgba(10,24,44,.7)}
.kpi .i{font-size:1.1rem}.kpi .n{font-size:1.5rem;font-weight:700;color:#fff;line-height:1.1}.kpi .l{font-size:.58rem;letter-spacing:.06em;color:#7f9bbb;text-transform:uppercase}
.hl{margin-top:12px;border:1px solid rgba(80,150,255,.25);border-radius:12px;padding:12px;background:linear-gradient(135deg,rgba(34,193,238,.12),rgba(46,204,113,.08))}
.hl .hh{font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#7fb4e8;margin-bottom:4px}.hl strong{font-size:.9rem;color:#fff}.hl p{font-size:.76rem;color:#9db6d3;line-height:1.45;margin-top:4px}
.grid2{display:grid;grid-template-columns:300px minmax(0,1fr) 340px;gap:14px}
.src{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.07);font-size:.85rem}
.src:last-child{border-bottom:none}
.src .nm{flex:1}
.on-t{color:#4ade80;font-weight:600;font-size:.72rem;display:flex;gap:6px;align-items:center}.off-t{color:#f87171;font-weight:600;font-size:.72rem}
.on-t i{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80}
.log{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:.8rem;align-items:baseline}
.log:last-child{border-bottom:none}
.log .tm{font-family:ui-monospace,Consolas,monospace;color:#7fb4e8;font-size:.72rem;flex:none;width:42px}
.log .tx{flex:1;min-width:0;overflow-wrap:anywhere}
.nw{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.07);align-items:center}
.nw:last-child{border-bottom:none}
.nw .tile{width:42px;height:42px;font-size:18px;background:rgba(34,193,238,.12)}
.nw a{color:#eaf3ff;text-decoration:none;font-size:.8rem;font-weight:600;line-height:1.25;display:block;overflow-wrap:anywhere}
.nw a:hover{color:#22c1ee}.nw small{color:#7f9bbb;font-size:.68rem}
@media(max-width:1100px){.grid,.grid2{grid-template-columns:1fr}.tag{display:none}#globe{height:380px}}
</style></head><body>
<div class="top">
  <div class="brand"><div class="logo">🛰️</div><div><h1 id="h-title"></h1><small id="h-sub"></small></div></div>
  <div class="tag" id="h-tag"></div>
  <div class="right"><span id="clock"></span><span class="pill"><i></i><span id="h-online"></span></span></div>
</div>
<div class="grid">
  <div class="panel"><div class="ph"><b>01</b><span id="t-recent"></span></div><div id="events"></div></div>
  <div class="panel globe-panel"><div id="globe"><div id="msg"></div></div><div class="chips" id="chips"></div></div>
  <div class="panel"><div class="ph"><b>04</b><span id="t-act"></span><span style="margin-left:auto;font-size:.65rem;color:#7f9bbb;text-transform:none;letter-spacing:0" id="t-last7"></span></div>
    <div class="chartbox"><canvas id="chart"></canvas></div><div class="kpis" id="kpis"></div>
    <div class="hl"><div class="hh" id="t-hl"></div><strong id="t-hlt"></strong><p id="t-hlp"></p></div></div>
</div>
<div class="grid2">
  <div class="panel"><div class="ph"><b>02</b><span id="t-src"></span></div><div id="srcs"></div></div>
  <div class="panel"><div class="ph"><b>03</b><span id="t-log"></span></div><div id="log"></div></div>
  <div class="panel"><div class="ph"><b>05</b><span id="t-news"></span></div><div id="news"></div></div>
</div>
<script>
const P = /*__DATA__*/;
const L = P.L, COL = P.colors, IC = P.icons;
let focus = 'all', globe = null, chart = null;
const $ = id => document.getElementById(id);
const esc = t => String(t == null ? '' : t).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function hex(c, a){ c = c.replace('#',''); return 'rgba('+parseInt(c.substr(0,2),16)+','+parseInt(c.substr(2,2),16)+','+parseInt(c.substr(4,2),16)+','+a+')'; }
function fit(){ try{ if(window.frameElement){ window.frameElement.style.height = (document.documentElement.scrollHeight + 4) + 'px'; } }catch(e){} }

if (P.rtl) document.documentElement.dir = 'rtl';
$('h-title').textContent = L.title; $('h-sub').textContent = L.sub; $('h-tag').textContent = L.tag; $('h-online').textContent = L.online;
$('t-recent').textContent = L.recent; $('t-act').textContent = L.act; $('t-last7').textContent = L.last7;
$('t-hl').textContent = L.hl; $('t-hlt').textContent = L.hlt; $('t-hlp').textContent = L.hlp;
$('t-src').textContent = L.src; $('t-log').textContent = L.log; $('t-news').textContent = L.news;
function clock(){ const d = new Date(); $('clock').textContent = d.toLocaleDateString(P.loc, {day:'2-digit',month:'short',year:'numeric'}) + '  ' + d.toISOString().substr(11,5) + ' UTC'; }
clock(); setInterval(clock, 20000);

function chips(){
  const items = ['all'].concat(P.cats);
  $('chips').innerHTML = items.map(k => {
    const c = k === 'all' ? '#22c1ee' : COL[k];
    const n = k === 'all' ? '' : '<em>'+(P.counts[k]||0)+'</em>';
    return '<button class="chip '+(k===focus?'on':'')+'" style="--c:'+c+'" data-k="'+k+'">'+(k==='all'?'':IC[k]+' ')+esc(k==='all'?L.all:L[k])+' '+n+'</button>';
  }).join('');
  document.querySelectorAll('.chip').forEach(b => b.onclick = () => setFocus(b.dataset.k));
}
function setFocus(k){ focus = k; chips(); events(); logs(); drawChart(); paint(true); fit(); }

function events(){
  let rows = P.ev.filter(r => focus === 'all' || r.cat === focus);
  if (focus === 'all'){ const seen = {}, mix = []; rows.forEach(r => { seen[r.cat] = (seen[r.cat]||0)+1; if (seen[r.cat] <= (r.cat==='eq'?2:1)) mix.push(r); }); rows = mix; }
  rows = rows.slice(0, 5);
  $('events').innerHTML = rows.length ? rows.map(r => '<div class="ev"><div class="tile" style="background:linear-gradient(135deg,'+hex(COL[r.cat],.45)+','+hex(COL[r.cat],.12)+')">'+IC[r.cat]+'</div><div class="t"><strong dir="auto">'+esc(r.title)+'</strong><small>'+esc(r.meta)+'</small></div><div class="v" style="color:'+COL[r.cat]+'">'+esc(r.val)+'</div></div>').join('') : '<div class="empty">'+esc(L.nodata)+'</div>';
}
function logs(){
  const rows = P.log.filter(r => focus === 'all' || r.cat === focus).slice(0, 8);
  $('log').innerHTML = rows.length ? rows.map(r => '<div class="log"><span class="tm">'+esc(r.tm)+'</span><span>'+IC[r.cat]+'</span><span class="tx" dir="auto" style="color:'+(r.cat==='eq'?'#eaf3ff':hex(COL[r.cat],1))+'">'+esc(r.text)+'</span></div>').join('') : '<div class="empty">'+esc(L.nodata)+'</div>';
}
function srcs(){
  $('srcs').innerHTML = P.sources.map(s => '<div class="src"><span class="nm">'+esc(s.n)+'</span>'+(s.ok?'<span class="on-t"><i></i>'+esc(L.on)+'</span>':'<span class="off-t">'+esc(L.off)+'</span>')+'</div>').join('');
}
function newsList(){
  $('news').innerHTML = P.news.length ? P.news.map(n => '<div class="nw"><div class="tile">📰</div><div><a href="'+esc(n.u)+'" target="_blank" rel="noopener" dir="auto">'+esc(n.t)+'</a><small>'+esc(n.s)+' · '+esc(n.a)+'</small></div></div>').join('') : '<div class="empty">'+esc(L.nonews)+'</div>';
}
function kpis(){
  const k = [['🌍', P.total_active, L.active], ['🔥', P.counts.fire, L.fire], ['🌀', P.counts.cyc, L.cyc], ['📡', P.signals, L.sig]];
  $('kpis').innerHTML = k.map(x => '<div class="kpi"><div class="i">'+x[0]+'</div><div class="n">'+x[1]+'</div><div class="l">'+esc(x[2])+'</div></div>').join('');
}
function drawChart(){
  if (typeof Chart === 'undefined') return;
  const cats = focus === 'all' ? P.cats : [focus];
  const ds = [];
  cats.forEach(c => {
    const raw = P.series[c]; if (!raw || raw.every(v => v == null)) return;
    const peak = Math.max.apply(null, raw.filter(v => v != null).concat([0]));
    const y = focus === 'all' ? raw.map(v => v == null ? null : (peak ? Math.round(1000*v/peak)/10 : 0)) : raw;
    ds.push({label: L[c], data: y, raw: raw, borderColor: COL[c], backgroundColor: hex(COL[c], focus==='all'?0.08:0.25), fill: true, tension: .4, borderWidth: 2.2, pointRadius: 2.5, pointBackgroundColor: COL[c]});
  });
  const data = {labels: P.days, datasets: ds};
  if (chart){ chart.data = data; chart.update(); return; }
  chart = new Chart($('chart'), {type: 'line', data: data, options: {responsive: true, maintainAspectRatio: false,
    plugins: {legend: {position: 'bottom', labels: {color: '#b9d2ee', boxWidth: 8, boxHeight: 8, usePointStyle: true, font: {size: 10}}},
      tooltip: {callbacks: {label: c => c.dataset.label + ': ' + c.dataset.raw[c.dataIndex]}}},
    scales: {x: {ticks: {color: '#7f9bbb', font: {size: 9}}, grid: {color: 'rgba(255,255,255,.05)'}},
             y: {beginAtZero: true, ticks: {color: '#7f9bbb', font: {size: 9}}, grid: {color: 'rgba(255,255,255,.08)'}}}}});
}
function paint(move){
  if (!globe) return;
  const cats = focus === 'all' ? P.cats : [focus];
  let pts = [];
  cats.forEach(c => (P.points[c] || []).forEach(p => pts.push({lat:p.lat, lng:p.lng, size:p.size, color:COL[c], title: IC[c]+' '+L[c]+' · '+p.title})));
  globe.pointsData(pts);
  globe.ringsData(pts.slice().sort((a,b) => b.size - a.size).slice(0, 60));
  if (move && focus !== 'all' && pts.length) globe.pointOfView({lat: pts[0].lat, lng: pts[0].lng, altitude: 1.9}, 900);
}
function initGlobe(){
  try{
    const box = $('globe');
    globe = Globe()(box)
      .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
      .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
      .backgroundColor('rgba(0,0,0,0)')
      .atmosphereColor('#3b9cff').atmosphereAltitude(0.28)
      .width(box.clientWidth).height(box.clientHeight)
      .pointLat('lat').pointLng('lng')
      .pointColor(d => d.color)
      .pointAltitude(d => 0.012 + Math.min(d.size, 20)/20*0.1)
      .pointRadius(d => 0.2 + Math.min(d.size, 20)/20*0.5)
      .pointLabel(d => '<div style="background:rgba(5,11,22,.92);padding:5px 9px;border:1px solid '+d.color+';border-radius:8px;font-size:12px;max-width:260px">'+esc(d.title)+'</div>')
      .ringLat('lat').ringLng('lng')
      .ringColor(d => t => hex(d.color, 1 - t))
      .ringMaxRadius(d => 2 + Math.min(d.size, 20)/20*5)
      .ringPropagationSpeed(2).ringRepeatPeriod(1500);
    globe.pointOfView({lat: 15, lng: -40, altitude: 2.0});
    const c = globe.controls(); c.autoRotate = true; c.autoRotateSpeed = 0.5; c.enableZoom = false;
    new ResizeObserver(() => globe.width(box.clientWidth).height(box.clientHeight)).observe(box);
    paint(false);
  }catch(e){ const m = $('msg'); m.style.display = 'flex'; m.textContent = '3D globe unavailable (WebGL / network).'; }
}
function loadScript(src){ return new Promise((ok,no) => { const e = document.createElement('script'); e.src = src; e.async = true; e.onload = ok; e.onerror = no; document.head.appendChild(e); }); }
chips(); events(); logs(); srcs(); newsList(); kpis(); fit();
loadScript('https://unpkg.com/globe.gl@2.27.2/dist/globe.gl.min.js').then(initGlobe)
  .catch(() => loadScript('https://cdn.jsdelivr.net/npm/globe.gl@2.27.2/dist/globe.gl.min.js').then(initGlobe).catch(() => { const m = $('msg'); m.style.display = 'flex'; m.textContent = '3D globe unavailable (network).'; }));
loadScript('https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js').then(() => { drawChart(); fit(); }).catch(() => {});
window.addEventListener('resize', fit);
</script></body></html>"""

COLORS = {"eq": "#ff4d4d", "fire": "#ff9f1c", "cyc": "#22d3ee", "torn": "#a78bfa",
          "tsu": "#2dd4bf", "vol": "#e879f9", "flood": "#3b82f6"}


def dash_html(payload):
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return DASH_HTML.replace("/*__DATA__*/", data)


# ── carregamento (cache) ─────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner="…")
def signals():
    return S.load_signals()


@st.cache_data(ttl=900, show_spinner=False)
def load_news(lang):
    """1) news.json do portfólio (robô Update News)  2) coleta ao vivo com o mesmo script (fetch_news.py)."""
    try:
        d = requests.get(NEWS_URL, headers=S.UA, timeout=10).json()
        items, upd = d.get("items") or [], d.get("updated")
        if items and upd and (datetime.now(timezone.utc) - datetime.fromisoformat(upd)).total_seconds() < 48 * 3600:
            return items, upd, "news.json"
    except Exception:
        pass
    try:
        from router import fetch_news
        fetch_news.TRANSLATE_TO = {lang: fetch_news.TRANSLATE_TO[lang]} if lang in fetch_news.TRANSLATE_TO else {}
        out = os.path.join(tempfile.mkdtemp(), "news.json")
        fetch_news.main(out)
        d = json.load(open(out, encoding="utf-8"))
        return d["items"], d["updated"], "live"
    except Exception:
        return [], None, "off"


def esc(x):
    return html.escape(str(x if x is not None else ""))


def age(iso, units):
    try:
        m = max(0, int((datetime.now(timezone.utc) - datetime.fromisoformat(iso)).total_seconds() // 60))
    except Exception:
        return ""
    u = units.split("|")
    return f"{m} {u[0]}" if m < 60 else f"{m // 60} {u[1]}" if m < 1440 else f"{m // 1440} {u[2]}"


def title_in(item, lang):
    return item["title"] if lang == "en" else (item.get("t") or {}).get(lang) or item["title"]





def render(lang):
    st.markdown(CSS, unsafe_allow_html=True)
    L = dict(T[lang]); L.update(X.get(lang, X["pt"]))
    D = signals()
    news, news_updated, news_mode = load_news(lang)
    news_topics = [S.topics(i["title"]) for i in news]

    # ── pontos do globo (todas as camadas; o filtro é feito dentro do painel) ──
    pts = {c: [] for c in S.CATS}
    pts["eq"] = [{"lat": q["lat"], "lng": q["lng"], "title": f'{q["title"]} · {L["mag"]} {q["mag"]}',
                  "size": max(4, (q["mag"] or 1) * 2.4)} for q in D["quakes"]]
    pts["tsu"] = [{"lat": q["lat"], "lng": q["lng"], "title": q["title"], "size": 15} for q in D["quakes"] if q["tsu"]]
    pts["torn"] = [{"lat": p["lat"], "lng": p["lng"], "title": p["title"], "size": 9} for p in D["torn_points"]]
    for e in D["events"]:
        if e["cat"] in pts and e["lat"] is not None:
            pts[e["cat"]].append({"lat": e["lat"], "lng": e["lng"], "title": e["title"], "size": 10})

    # ── lista de eventos recentes ──
    ev = []
    for q in sorted(D["quakes"], key=lambda q: q["mag"] or 0, reverse=True)[:6]:
        ev.append({"cat": "eq", "title": q["title"], "meta": "USGS", "val": f'M {q["mag"]}'})
    for t in D["nws_tsu"][:2]:
        ev.append({"cat": "tsu", "title": t["title"], "meta": "NOAA", "val": "⚠"})
    for p in D["torn_points"][:3]:
        f = p["f"] if p["f"] not in ("", "UNK") else ""
        ev.append({"cat": "torn", "title": p["title"], "meta": "NOAA SPC", "val": f"F {f}" if f else ""})
    for e in sorted(D["events"], key=lambda e: e["date"] or "", reverse=True):
        if e["cat"] != "oth":
            ev.append({"cat": e["cat"], "title": e["title"], "meta": "NASA EONET · " + age(e.get("date") or "", L["units"]), "val": ""})

    # ── log de inteligência (mais recentes primeiro) ──
    lg = []
    for q in D["quakes"]:
        if q.get("time"):
            lg.append((q["time"] / 1000, "eq", f'M{q["mag"]} · {q["title"]}'))
    for e in D["events"]:
        if e["cat"] != "oth" and e.get("date"):
            try:
                lg.append((datetime.fromisoformat(e["date"].replace("Z", "+00:00")).timestamp(), e["cat"], e["title"]))
            except Exception:
                pass
    lg.sort(reverse=True)
    log = [{"tm": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"), "cat": c, "text": x} for t, c, x in lg[:60]]

    payload = {
        "L": {k: v for k, v in L.items() if isinstance(v, str)},
        "rtl": lang == "ar", "loc": {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "it": "it-IT", "fr": "fr-FR", "de": "de-DE",
                                      "zh": "zh-CN", "ar": "ar-EG-u-nu-latn", "el": "el-GR"}.get(lang, "en-US"),
        "cats": S.CATS, "colors": COLORS, "icons": S.ICONS, "counts": D["counts"], "points": pts, "ev": ev, "log": log,
        "days": [d.strftime("%d/%m") for d in D["days"]], "series": D["series"],
        "total_active": D["total_active"], "signals": D["signals"],
        "sources": [{"n": "USGS", "ok": D["status"]["usgs"]}, {"n": "NASA EONET", "ok": D["status"]["eonet"]},
                    {"n": "NOAA", "ok": D["status"]["noaa"]}, {"n": "Fetch News", "ok": news_mode != "off"}],
        "news": [{"t": title_in(i, lang), "s": i["source"], "u": i["url"] if str(i["url"]).startswith("http") else "#",
                  "a": age(i.get("date"), L["units"])} for i in news[:5]],
    }
    embed_html(dash_html(payload), 1080)

    # ── Boletim Ambiental: notícias atuais de portais confiáveis, interativo ─────
    with st.container(key="card_news"):
        st.markdown(f'<div class="sec">{esc(L["news"])}</div>', unsafe_allow_html=True)
        if not news:
            st.markdown(f'<div class="meta">{esc(L["nonews"])}</div>', unsafe_allow_html=True)
        else:
            sources = sorted({i["source"] for i in news})
            picked = st.pills("src", sources, selection_mode="multi", key="srcsel", label_visibility="collapsed") or []
            idx = [n for n, i in enumerate(news) if (not picked or i["source"] in picked)]
            note = ""
            expand = st.toggle(f'{L["more"]} ({len(idx)})', key="expand") if len(idx) > DEFAULT_SHOWN else False
            shown = idx if expand else idx[:DEFAULT_SHOWN]
            read = 0
            boxes = []
            for n in shown:
                i = news[n]
                key = "read_" + str(abs(hash(i["url"])))
                tags = " ".join(S.ICONS[t] for t in news_topics[n])
                label = f'[{title_in(i, lang)}]({i["url"]}) · :gray[{i["source"]} · {age(i.get("date"), L["units"])}] {tags}'
                boxes.append((key, label))
            for key, label in boxes:
                read += 1 if st.session_state.get(key) else 0
            remaining = max(0, math.ceil((len(shown) - read) * HEADLINE_SECONDS / 60))
            stamp = news_updated[11:16] + "Z" if news_updated else ""
            st.markdown(f'<div class="meta">⏱ ≈ {remaining} {esc(L["readtime"])} · {len(shown)} {esc(L["headlines"])} · '
                        f'{esc(L["updated"])} {stamp} · {read}/{len(shown)} ✓</div>', unsafe_allow_html=True)
            st.progress(read / len(shown) if shown else 0)
            if note:
                st.caption(note)
            for key, label in boxes:
                st.checkbox(label, key=key)
