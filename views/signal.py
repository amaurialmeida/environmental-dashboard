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
    "pt": {"langs": "Idioma", "sub": "Inteligência ambiental em tempo real", "tag": "Observar · Analisar · Proteger", "online": "Sistema online", "log": "Log de inteligência ambiental"},
    "en": {"langs": "Language", "sub": "Real-time environmental intelligence", "tag": "Observe · Analyze · Protect", "online": "System online", "log": "Environmental intelligence log"},
    "es": {"langs": "Idioma", "sub": "Inteligencia ambiental en tiempo real", "tag": "Observar · Analizar · Proteger", "online": "Sistema en línea", "log": "Registro de inteligencia ambiental"},
    "it": {"langs": "Lingua", "sub": "Intelligence ambientale in tempo reale", "tag": "Osserva · Analizza · Proteggi", "online": "Sistema online", "log": "Log di intelligence ambientale"},
    "fr": {"langs": "Langue", "sub": "Renseignement environnemental en temps réel", "tag": "Observer · Analyser · Protéger", "online": "Système en ligne", "log": "Journal de renseignement environnemental"},
    "de": {"langs": "Sprache", "sub": "Umwelt-Intelligence in Echtzeit", "tag": "Beobachten · Analysieren · Schützen", "online": "System online", "log": "Umwelt-Intelligence-Log"},
    "zh": {"langs": "语言", "sub": "实时环境情报", "tag": "观察 · 分析 · 守护", "online": "系统在线", "log": "环境情报日志"},
    "ar": {"langs": "اللغة", "sub": "الاستخبارات البيئية في الوقت الفعلي", "tag": "راقب · حلّل · احمِ", "online": "النظام متصل", "log": "سجل الاستخبارات البيئية"},
    "el": {"langs": "Γλώσσα", "sub": "Περιβαλλοντική πληροφόρηση σε πραγματικό χρόνο", "tag": "Παρατήρηση · Ανάλυση · Προστασία", "online": "Σύστημα online", "log": "Αρχείο περιβαλλοντικής πληροφόρησης"},
}

# Índice de intensidade ambiental por região (9 idiomas)
X_IDX = {
    "pt": {"idx": "Intensidade ambiental por região", "idxn": "Indicador próprio (0–100) com os sinais das últimas 24 h; não é um índice oficial. Seta = variação frente à média dos 6 dias anteriores.",
           "r": ["América do Norte", "América do Sul", "Europa", "África", "Ásia", "Oceania"], "lv": ["Baixa", "Moderada", "Elevada", "Alta"]},
    "en": {"idx": "Environmental intensity by region", "idxn": "Own indicator (0–100) from the last 24 h of signals; not an official index. Arrow = change vs. the previous 6-day average.",
           "r": ["North America", "South America", "Europe", "Africa", "Asia", "Oceania"], "lv": ["Low", "Moderate", "Elevated", "High"]},
    "es": {"idx": "Intensidad ambiental por región", "idxn": "Indicador propio (0–100) con las señales de las últimas 24 h; no es un índice oficial. Flecha = variación frente al promedio de los 6 días anteriores.",
           "r": ["América del Norte", "América del Sur", "Europa", "África", "Asia", "Oceanía"], "lv": ["Baja", "Moderada", "Elevada", "Alta"]},
    "it": {"idx": "Intensità ambientale per regione", "idxn": "Indicatore proprio (0–100) basato sui segnali delle ultime 24 h; non è un indice ufficiale. Freccia = variazione rispetto alla media dei 6 giorni precedenti.",
           "r": ["Nord America", "Sud America", "Europa", "Africa", "Asia", "Oceania"], "lv": ["Bassa", "Moderata", "Elevata", "Alta"]},
    "fr": {"idx": "Intensité environnementale par région", "idxn": "Indicateur propre (0–100) basé sur les signaux des dernières 24 h ; ce n'est pas un indice officiel. Flèche = variation par rapport à la moyenne des 6 jours précédents.",
           "r": ["Amérique du Nord", "Amérique du Sud", "Europe", "Afrique", "Asie", "Océanie"], "lv": ["Faible", "Modérée", "Élevée", "Haute"]},
    "de": {"idx": "Umweltintensität nach Region", "idxn": "Eigener Indikator (0–100) aus den Signalen der letzten 24 h; kein offizieller Index. Pfeil = Veränderung gegenüber dem Durchschnitt der 6 Vortage.",
           "r": ["Nordamerika", "Südamerika", "Europa", "Afrika", "Asien", "Ozeanien"], "lv": ["Niedrig", "Mäßig", "Erhöht", "Hoch"]},
    "zh": {"idx": "各地区环境强度", "idxn": "自有指标（0–100），基于过去 24 小时的信号；并非官方指数。箭头＝与前 6 天平均值相比的变化。",
           "r": ["北美洲", "南美洲", "欧洲", "非洲", "亚洲", "大洋洲"], "lv": ["低", "中", "较高", "高"]},
    "ar": {"idx": "الشدة البيئية حسب المنطقة", "idxn": "مؤشر خاص (0–100) مبني على إشارات آخر 24 ساعة؛ وليس مؤشرًا رسميًا. السهم = التغير مقارنة بمتوسط الأيام الستة السابقة.",
           "r": ["أمريكا الشمالية", "أمريكا الجنوبية", "أوروبا", "أفريقيا", "آسيا", "أوقيانوسيا"], "lv": ["منخفضة", "معتدلة", "مرتفعة", "عالية"]},
    "el": {"idx": "Περιβαλλοντική ένταση ανά περιοχή", "idxn": "Ιδιόκτητος δείκτης (0–100) με βάση τα σήματα των τελευταίων 24 ωρών· δεν είναι επίσημος δείκτης. Βέλος = μεταβολή σε σχέση με τον μέσο όρο των 6 προηγούμενων ημερών.",
           "r": ["Βόρεια Αμερική", "Νότια Αμερική", "Ευρώπη", "Αφρική", "Ασία", "Ωκεανία"], "lv": ["Χαμηλή", "Μέτρια", "Αυξημένη", "Υψηλή"]},
}
for _lg, _v in X_IDX.items():
    X[_lg].update(_v)


# Palavras de atribuição (fontes dos dados)
X_ATTR = {"pt": ("Fonte", "Imagem"), "en": ("Source", "Image"), "es": ("Fuente", "Imagen"), "it": ("Fonte", "Immagine"),
          "fr": ("Source", "Image"), "de": ("Quelle", "Bild"), "zh": ("数据来源", "图像"), "ar": ("المصدر", "الصورة"), "el": ("Πηγή", "Εικόνα")}
for _lg, (_a, _b) in X_ATTR.items():
    X[_lg].update({"srcw": _a, "imgw": _b})


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
.globe-panel{padding:0;overflow:hidden;display:flex;flex-direction:column;background:radial-gradient(circle at 50% 40%,#0f3d6b,#061a30)}
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
.src{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.07);font-size:.85rem}
.src:last-child{border-bottom:none}
.src .nm{flex:1}.src .nm small{display:block;color:#7f9bbb;font-size:.64rem;margin-top:1px}
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
.lang-box{margin-top:14px;padding:12px;border:1px solid rgba(46,204,113,.25);border-radius:14px;background:linear-gradient(135deg,rgba(46,204,113,.08),rgba(10,24,44,.55));box-shadow:0 0 22px rgba(46,204,113,.08)}
.lang-box .lt{font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;color:#7fd9a6;margin-bottom:9px;text-align:center}
.lang-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.lang-btn{display:flex;align-items:center;justify-content:center;gap:6px;padding:6px 4px;background:rgba(46,204,113,.12);color:#2ecc71;border:1px solid #2ecc71;border-radius:16px;cursor:pointer;font-size:.74rem;font-family:inherit;transition:all .25s}
.lang-btn img{width:20px;height:15px;object-fit:cover;border-radius:2px;display:block}
.lang-btn:hover,.lang-btn.active{background:#2ecc71;color:#04140b;box-shadow:0 0 10px rgba(46,204,113,.8);font-weight:700}
.attr{margin-top:10px;font-size:.62rem;line-height:1.4;color:#6f8cab;letter-spacing:.02em;overflow-wrap:anywhere}
.globe-panel .attr{margin:0;padding:0 12px 10px;text-align:center;background:rgba(5,11,22,.9)}
.col{display:flex;flex-direction:column;gap:14px;min-width:0}
.rg{display:grid;grid-template-columns:104px minmax(0,1fr) 26px 50px;gap:8px;align-items:center;padding:4px 0;font-size:.76rem;color:#dbe9fb}
.rg .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rg .bar{height:7px;border-radius:4px;background:rgba(255,255,255,.08);overflow:hidden}.rg .bar i{display:block;height:100%;border-radius:4px}
.rg .n{font-weight:700;text-align:right}.rg .d{font-size:.66rem;white-space:nowrap}
.d.up{color:#f87171}.d.dn{color:#4ade80}.d.fl{color:#7f9bbb}
.idxn{font-size:.62rem;line-height:1.4;color:#7f9bbb;margin-top:8px}
@media(max-width:1100px){.grid,.grid2{grid-template-columns:1fr}.tag{display:none}#globe{height:380px}}
</style></head><body>
<div class="top">
  <div class="brand"><div class="logo">🛰️</div><div><h1 id="h-title"></h1><small id="h-sub"></small></div></div>
  <div class="tag" id="h-tag"></div>
  <div class="right"><span id="clock"></span><span class="pill"><i></i><span id="h-online"></span></span></div>
</div>
<div class="grid">
  <div class="panel"><div class="ph"><b>01</b><span id="t-recent"></span></div><div id="events"></div><div class="attr" id="a-ev"></div>
    <div class="lang-box"><div class="lt" id="t-lang"></div><div class="lang-grid" id="langs"></div></div></div>
  <div class="panel globe-panel"><div id="globe"><div id="msg"></div></div><div class="chips" id="chips"></div><div class="attr" id="a-gl"></div></div>
  <div class="panel"><div class="ph"><b>04</b><span id="t-act"></span><span style="margin-left:auto;font-size:.65rem;color:#7f9bbb;text-transform:none;letter-spacing:0" id="t-last7"></span></div>
    <div class="chartbox"><canvas id="chart"></canvas></div><div class="kpis" id="kpis"></div>
    <div class="hl"><div class="hh" id="t-hl"></div><strong id="t-hlt"></strong><p id="t-hlp"></p></div><div class="attr" id="a-act"></div></div>
</div>
<div class="grid2">
  <div class="col"><div class="panel"><div class="ph"><b>02</b><span id="t-src"></span></div><div id="srcs"></div></div>
    <div class="panel"><div class="ph"><b>06</b><span id="t-idx"></span></div><div id="idx"></div><p class="idxn" id="t-idxn"></p><div class="attr" id="a-idx" style="margin-top:4px"></div></div></div>
  <div class="panel"><div class="ph"><b>03</b><span id="t-log"></span></div><div id="log"></div><div class="attr" id="a-log"></div></div>
  <div class="panel"><div class="ph"><b>05</b><span id="t-news"></span></div><div id="news"></div><div class="attr" id="a-news"></div></div>
</div>
<script>
const P = /*__DATA__*/;
let L = P.LS[P.lang] || P.LS.pt, lang = P.lang;
const COL = P.colors, IC = P.icons;
const FLAGS = {pt:['br','🇧🇷','PT'],en:['gb','🇬🇧','EN'],es:['es','🇪🇸','ES'],it:['it','🇮🇹','IT'],fr:['fr','🇫🇷','FR'],de:['de','🇩🇪','DE'],zh:['cn','🇨🇳','ZH'],ar:['sa','🇸🇦','AR'],el:['gr','🇬🇷','EL']};
let focus = 'all', globe = null, chart = null;
const $ = id => document.getElementById(id);
const esc = t => String(t == null ? '' : t).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function hex(c, a){ c = c.replace('#',''); return 'rgba('+parseInt(c.substr(0,2),16)+','+parseInt(c.substr(2,2),16)+','+parseInt(c.substr(4,2),16)+','+a+')'; }
function fit(){ try{ if(window.frameElement){ window.frameElement.style.height = (document.documentElement.scrollHeight + 4) + 'px'; } }catch(e){} }

// ── tradução da parte fixa dos nomes de eventos (nomes próprios de lugares ficam como estão) ──
const DIRW = {
  pt:{N:'N',S:'S',E:'L',W:'O'}, es:{N:'N',S:'S',E:'E',W:'O'}, it:{N:'N',S:'S',E:'E',W:'O'}, fr:{N:'N',S:'S',E:'E',W:'O'},
  de:{N:'N',S:'S',E:'O',W:'W'}, el:{N:'Β',S:'Ν',E:'Α',W:'Δ'}};
const DIRZ = {N:'北',S:'南',E:'东',W:'西',NE:'东北',NW:'西北',SE:'东南',SW:'西南',NNE:'东北偏北',ENE:'东北偏东',ESE:'东南偏东',SSE:'东南偏南',SSW:'西南偏南',WSW:'西南偏西',WNW:'西北偏西',NNW:'西北偏北'};
const DIRA = {N:'شمال',S:'جنوب',E:'شرق',W:'غرب',NE:'شمال شرق',NW:'شمال غرب',SE:'جنوب شرق',SW:'جنوب غرب',NNE:'شمال-شمال شرق',ENE:'شرق-شمال شرق',ESE:'شرق-جنوب شرق',SSE:'جنوب-جنوب شرق',SSW:'جنوب-جنوب غرب',WSW:'غرب-جنوب غرب',WNW:'غرب-شمال غرب',NNW:'شمال-شمال غرب'};
function dirTxt(d, lg){
  if (lg === 'zh') return DIRZ[d] || d;
  if (lg === 'ar') return DIRA[d] || d;
  const m = DIRW[lg]; return m ? d.split('').map(c => m[c] || c).join('') : d;
}
const PHR = {
  pt:(n,d,p)=>n+' km a '+d+' de '+p, es:(n,d,p)=>'a '+n+' km al '+d+' de '+p, it:(n,d,p)=>n+' km a '+d+' di '+p,
  fr:(n,d,p)=>'à '+n+' km au '+d+' de '+p, de:(n,d,p)=>n+' km '+d+' von '+p, zh:(n,d,p)=>p+' '+d+'方 '+n+' 公里',
  ar:(n,d,p)=>n+' كم '+d+' '+p, el:(n,d,p)=>n+' χλμ '+d+' από '+p};
const KIND = [
  ['super typhoon',{pt:'Super Tufão',es:'Supertifón',it:'Super Tifone',fr:'Super Typhon',de:'Supertaifun',zh:'超强台风',ar:'تيفون فائق',el:'Σούπερ Τυφώνας'}],
  ['tropical cyclone',{pt:'Ciclone Tropical',es:'Ciclón Tropical',it:'Ciclone Tropicale',fr:'Cyclone Tropical',de:'Tropischer Zyklon',zh:'热带气旋',ar:'إعصار مداري',el:'Τροπικός Κυκλώνας'}],
  ['tropical storm',{pt:'Tempestade Tropical',es:'Tormenta Tropical',it:'Tempesta Tropicale',fr:'Tempête Tropicale',de:'Tropischer Sturm',zh:'热带风暴',ar:'عاصفة مدارية',el:'Τροπική Καταιγίδα'}],
  ['prescribed fire',{pt:'Queima Controlada',es:'Quema Prescrita',it:'Fuoco Prescritto',fr:'Brûlage Dirigé',de:'Kontrollierter Brand',zh:'计划烧除',ar:'حرق مُخطَّط',el:'Ελεγχόμενη Καύση'}],
  ['typhoon',{pt:'Tufão',es:'Tifón',it:'Tifone',fr:'Typhon',de:'Taifun',zh:'台风',ar:'تيفون',el:'Τυφώνας'}],
  ['hurricane',{pt:'Furacão',es:'Huracán',it:'Uragano',fr:'Ouragan',de:'Hurrikan',zh:'飓风',ar:'إعصار',el:'Τυφώνας'}],
  ['cyclone',{pt:'Ciclone',es:'Ciclón',it:'Ciclone',fr:'Cyclone',de:'Zyklon',zh:'气旋',ar:'إعصار',el:'Κυκλώνας'}],
  ['wildfire',{pt:'Incêndio Florestal',es:'Incendio Forestal',it:'Incendio Boschivo',fr:'Feu de Forêt',de:'Waldbrand',zh:'野火',ar:'حريق غابات',el:'Δασική Πυρκαγιά'}],
  ['flood',{pt:'Inundação',es:'Inundación',it:'Alluvione',fr:'Inondation',de:'Überschwemmung',zh:'洪水',ar:'فيضان',el:'Πλημμύρα'}],
  ['volcano',{pt:'Vulcão',es:'Volcán',it:'Vulcano',fr:'Volcan',de:'Vulkan',zh:'火山',ar:'بركان',el:'Ηφαίστειο'}]];
const ALIAS = {'Turkey':'TR','Myanmar':'MM','Burma':'MM','Czech Republic':'CZ','Ivory Coast':'CI','Macedonia':'MK','Swaziland':'SZ','East Timor':'TL','Cape Verde':'CV','Democratic Republic of the Congo':'CD','Republic of the Congo':'CG','Falkland Islands':'FK','Russia':'RU'};
let CMAP = null;
function cmap(){
  if (CMAP) return CMAP; CMAP = Object.assign({}, ALIAS);
  try{ const dn = new Intl.DisplayNames(['en'], {type:'region'}), A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let i = 0; i < 26; i++) for (let j = 0; j < 26; j++){ const c = A[i]+A[j]; try{ const n = dn.of(c); if (n && n !== c && !(n in CMAP)) CMAP[n] = c; }catch(e){} } }catch(e){}
  return CMAP;
}
const RLOC = {zh:'zh-CN', ar:'ar'};
function countryIn(name, lg){
  const code = cmap()[name]; if (!code) return name;
  try{ return new Intl.DisplayNames([RLOC[lg] || lg], {type:'region'}).of(code) || name; }catch(e){ return name; }
}
function tt(s){
  s = String(s == null ? '' : s);
  if (lang === 'en') return s;
  try{
    let m = s.match(/^(.*?)([0-9]+(?:[.][0-9]+)?) km ([NSEW]{1,3}) of (.+)$/);
    if (m){
      const parts = m[4].split(', '), last = parts.pop();
      const place = lang === 'zh' ? [countryIn(last, lang)].concat(parts.slice().reverse()).join(' ') : parts.concat([countryIn(last, lang)]).join(', ');
      return m[1] + PHR[lang](m[2], dirTxt(m[3], lang), place);
    }
    const k = KIND.find(x => s.toLowerCase().indexOf(x[0] + ' ') === 0 || s.toLowerCase() === x[0]);
    if (k && k[1][lang]) s = k[1][lang] + s.slice(k[0].length);
    const c = s.lastIndexOf(', ');
    if (c > 0){ const nm = s.slice(c + 2); if (cmap()[nm]) s = s.slice(0, c + 2) + countryIn(nm, lang); }
  }catch(e){}
  return s;
}

function ageTxt(iso){
  if(!iso) return '';
  const m = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime())/60000)); if (isNaN(m)) return '';
  const u = (L.units || 'min|h|d').split('|');
  return m < 60 ? m+' '+u[0] : m < 1440 ? Math.floor(m/60)+' '+u[1] : Math.floor(m/1440)+' '+u[2];
}
function clock(){ const d = new Date(); let t; try{ t = d.toLocaleDateString(P.locs[lang], {day:'2-digit',month:'short',year:'numeric'}); }catch(e){ t = d.toDateString(); } $('clock').textContent = t + '  ' + d.toISOString().substr(11,5) + ' UTC'; }
function langButtons(){
  $('langs').innerHTML = Object.keys(FLAGS).map(k => '<button class="lang-btn '+(k===lang?'active':'')+'" data-l="'+k+'" aria-label="'+k.toUpperCase()+'"><img src="https://flagcdn.com/24x18/'+FLAGS[k][0]+'.png" srcset="https://flagcdn.com/48x36/'+FLAGS[k][0]+'.png 2x" alt="" data-f="'+FLAGS[k][1]+'"><span>'+FLAGS[k][2]+'</span></button>').join('');
  document.querySelectorAll('.lang-btn').forEach(b => b.onclick = () => setLang(b.dataset.l));
}
// se a imagem da bandeira não carregar, mostra o emoji da bandeira
document.addEventListener('error', e => { const t = e.target; if (t && t.tagName === 'IMG' && t.dataset.f) { const sp = document.createElement('span'); sp.textContent = t.dataset.f; t.replaceWith(sp); } }, true);
function texts(){
  document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'; document.documentElement.lang = lang;
  $('h-title').textContent = L.title; $('h-sub').textContent = L.sub; $('h-tag').textContent = L.tag; $('h-online').textContent = L.online;
  $('t-recent').textContent = L.recent; $('t-act').textContent = L.act; $('t-last7').textContent = L.last7;
  $('t-hl').textContent = L.hl; $('t-hlt').textContent = L.hlt; $('t-hlp').textContent = L.hlp;
  $('t-idx').textContent = L.idx; $('t-idxn').textContent = L.idxn; $('t-src').textContent = L.src; $('t-log').textContent = L.log; $('t-news').textContent = L.news; $('t-lang').textContent = L.langs;
  clock();
}
function setLang(l){
  if (!P.LS[l]) return; lang = l; L = P.LS[l];
  texts(); langButtons(); chips(); events(); logs(); srcs(); idx(); newsList(); kpis(); attrs();
  if (chart){ chart.destroy(); chart = null; } drawChart(); paint(false); fit();
}
setInterval(clock, 20000);


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
  $('events').innerHTML = rows.length ? rows.map(r => '<div class="ev"><div class="tile" style="background:linear-gradient(135deg,'+hex(COL[r.cat],.45)+','+hex(COL[r.cat],.12)+')">'+IC[r.cat]+'</div><div class="t"><strong dir="auto">'+esc(tt(r.title))+'</strong><small>'+esc(r.meta)+'</small></div><div class="v" style="color:'+COL[r.cat]+'">'+esc(r.val)+'</div></div>').join('') : '<div class="empty">'+esc(L.nodata)+'</div>';
}
function logs(){
  const rows = P.log.filter(r => focus === 'all' || r.cat === focus).slice(0, 8);
  $('log').innerHTML = rows.length ? rows.map(r => '<div class="log"><span class="tm">'+esc(r.tm)+'</span><span>'+IC[r.cat]+'</span><span class="tx" dir="auto" style="color:'+(r.cat==='eq'?'#eaf3ff':hex(COL[r.cat],1))+'">'+esc(tt(r.text))+'</span></div>').join('') : '<div class="empty">'+esc(L.nodata)+'</div>';
}
function srcs(){
  $('srcs').innerHTML = P.sources.map(s => {
    const a = s.ok && s.t ? ageTxt(s.t) : '';
    return '<div class="src"><span class="nm">'+esc(s.n)+(a ? '<small>'+esc(L.updated)+' · '+esc(a)+'</small>' : '')+'</span>'+(s.ok?'<span class="on-t"><i></i>'+esc(L.on)+'</span>':'<span class="off-t">'+esc(L.off)+'</span>')+'</div>';
  }).join('');
}
function attrs(){
  const w = L.srcw + ': ', U = 'USGS · NASA EONET · NOAA SPC';
  $('a-ev').textContent = w + U;
  $('a-gl').textContent = w + U + ' · ' + L.imgw + ': NASA Blue Marble';
  $('a-act').textContent = w + U;
  $('a-log').textContent = w + 'USGS · NASA EONET';
  $('a-idx').textContent = w + U;
  const ns = Array.from(new Set(P.news.map(n => n.s))).filter(Boolean);
  $('a-news').textContent = ns.length ? w + ns.join(' · ') : '';
}
const REGS = ['na','sa','eu','af','as','oc'];
function idx(){
  const R = P.RI;
  if (!R || !R.length){ $('idx').innerHTML = '<div class="empty">'+esc(L.nodata)+'</div>'; return; }
  const cl = ['#4ade80','#facc15','#fb923c','#f87171'];
  $('idx').innerHTML = R.slice().sort((a,b) => b.score - a.score).map(r => {
    const lv = r.score < 25 ? 0 : r.score < 50 ? 1 : r.score < 75 ? 2 : 3, d = r.delta;
    const dt = d == null ? '' : '<span class="d '+(d >= 5 ? 'up' : d <= -5 ? 'dn' : 'fl')+'">'+(d >= 5 ? '▲' : d <= -5 ? '▼' : '■')+' '+(d > 0 ? '+' : '')+d+'</span>';
    const nm = (L.r || [])[REGS.indexOf(r.k)] || r.k;
    return '<div class="rg" title="'+esc(nm+' · '+(L.lv||[])[lv]+' · '+r.score+'/100')+'"><span class="nm">'+esc(nm)+'</span><span class="bar"><i style="width:'+r.score+'%;background:'+cl[lv]+'"></i></span><span class="n" style="color:'+cl[lv]+'">'+r.score+'</span>'+(dt || '<span></span>')+'</div>';
  }).join('');
}
function newsList(){
  $('news').innerHTML = P.news.length ? P.news.map(n => '<div class="nw"><div class="tile">📰</div><div><a href="'+esc(n.u)+'" target="_blank" rel="noopener" dir="auto">'+esc(n.t[lang] || n.t.en || '')+'</a><small>'+esc(n.s)+' · '+esc(ageTxt(n.d))+'</small></div></div>').join('') : '<div class="empty">'+esc(L.nonews)+'</div>';
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
  cats.forEach(c => (P.points[c] || []).forEach(p => pts.push({lat:p.lat, lng:p.lng, size:p.size, cat:c, color:COL[c], title: IC[c]+' '+L[c]+' · '+tt(p.title)+(p.mag != null ? ' · '+L.mag+' '+p.mag : '')})));
  globe.pointsData(pts);
  if (move && focus !== 'all' && pts.length) globe.pointOfView({lat: pts[0].lat, lng: pts[0].lng, altitude: 1.9}, 900);
}
function initGlobe(){
  try{
    const box = $('globe');
    globe = Globe()(box)
      .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
      .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
      .backgroundColor('rgba(0,0,0,0)')
      .atmosphereColor('#22c1ee').atmosphereAltitude(0.25)
      .width(box.clientWidth).height(box.clientHeight)
      .pointLat('lat').pointLng('lng')
      .pointColor(d => d.color)
      .pointAltitude(0.02)
      .pointRadius(d => d.cat === 'eq' ? Math.max(0.25, d.size/14.4) : 0.45)
      .pointLabel(d => '<div style="background:rgba(5,11,22,.92);padding:5px 9px;border:1px solid '+d.color+';border-radius:8px;font-size:12px;max-width:260px">'+esc(d.title)+'</div>')
;
    globe.pointOfView({lat: 15, lng: -40, altitude: 2.2});
    const c = globe.controls(); c.autoRotate = true; c.autoRotateSpeed = 0.4; c.enableZoom = false;
    new ResizeObserver(() => globe.width(box.clientWidth).height(box.clientHeight)).observe(box);
    paint(false);
  }catch(e){ const m = $('msg'); m.style.display = 'flex'; m.textContent = '3D globe unavailable (WebGL / network).'; }
}
function loadScript(src){ return new Promise((ok,no) => { const e = document.createElement('script'); e.src = src; e.async = true; e.onload = ok; e.onerror = no; document.head.appendChild(e); }); }
texts(); langButtons(); chips(); events(); logs(); srcs(); idx(); newsList(); kpis(); attrs(); fit();
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
    pts["eq"] = [{"lat": q["lat"], "lng": q["lng"], "title": q["title"],
                  "size": max(4, (q["mag"] or 1) * 2.4), "mag": q["mag"]} for q in D["quakes"]]
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
            ev.append({"cat": e["cat"], "title": e["title"], "meta": "NASA EONET", "d": e.get("date"), "val": ""})

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

    LOCS = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "it": "it-IT", "fr": "fr-FR", "de": "de-DE",
            "zh": "zh-CN", "ar": "ar-EG-u-nu-latn", "el": "el-GR"}
    LS = {lg: {**{k: v for k, v in T[lg].items() if isinstance(v, str)}, **X.get(lg, X["pt"])} for lg in T}
    payload = {
        "LS": LS, "lang": lang, "locs": LOCS,
        "cats": S.CATS, "colors": COLORS, "icons": S.ICONS, "counts": D["counts"], "points": pts, "ev": ev, "log": log,
        "days": [d.strftime("%d/%m") for d in D["days"]], "series": D["series"],
        "total_active": D["total_active"], "signals": D["signals"], "RI": D.get("region_idx"),
        "sources": [{"n": "USGS", "ok": D["status"]["usgs"], "t": D["stamps"]["usgs"]},
                    {"n": "NASA EONET", "ok": D["status"]["eonet"], "t": D["stamps"]["eonet"]},
                    {"n": "NOAA", "ok": D["status"]["noaa"], "t": D["stamps"]["noaa"]},
                    {"n": "Fetch News", "ok": news_mode != "off", "t": news_updated}],
        "news": [{"t": {lg: title_in(i, lg) for lg in T}, "s": i["source"],
                  "u": i["url"] if str(i["url"]).startswith("http") else "#", "d": i.get("date")} for i in news[:5]],
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
