#!/usr/bin/env python3
"""Coleta manchetes ambientais de redações jornalísticas confiáveis (RSS público, sem chave)
e grava news.json na raiz do site. Roda no GitHub Actions a cada hora.
ONGs (WWF, Greenpeace etc.) ficam de fora por regra: só domínios da lista ALLOWED_HOSTS."""
import json, os, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

FEEDS = [
    # (rótulo, url, filtrar_por_tema)
    ("BBC",        "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml", False),
    ("GUARDIAN",   "https://www.theguardian.com/environment/rss",                  False),
    ("NYTIMES",    "https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",     False),
    ("NPR",        "https://feeds.npr.org/1025/rss.xml",                           False),
    ("NATURE",     "https://www.nature.com/nature.rss",                            True),
    ("AL JAZEERA", "https://www.aljazeera.com/xml/rss/all.xml",                    True),
    ("DW",         "https://rss.dw.com/rdf/rss-en-all",                            True),
]
ALLOWED_HOSTS = ("bbc.co.uk", "bbc.com", "theguardian.com", "nytimes.com", "npr.org",
                 "nature.com", "aljazeera.com", "dw.com", "reuters.com", "apnews.com",
                 "nationalgeographic.com", "science.org")
ENV_RE = re.compile(r"climate|environment|emission|carbon|warming|heatwave|wildfire|flood|drought|"
                    r"biodiversity|species|forest|deforest|ocean|coral|glacier|ice sheet|renewable|"
                    r"solar|wind (farm|power)|energy transition|pollution|plastic|extinction|wildlife|"
                    r"conservation|\bcop\d+|amazon|arctic|antarctic|sea level|hurricane|cyclone|"
                    r"earthquake|storm|fossil fuel|net zero|ecosystem", re.I)
PER_SOURCE, TOTAL = 4, 24
# idiomas do site (código do site -> código do tradutor). EN é o original.
TRANSLATE_TO = {"pt": "pt", "es": "es", "it": "it", "zh": "zh-CN", "fr": "fr", "ar": "ar", "de": "de", "el": "el"}

def host_ok(url):
    h = (urlparse(url).hostname or "").lower()
    return any(h == d or h.endswith("." + d) for d in ALLOWED_HOSTS)

def _t(el, *names):
    for n in names:
        x = el.find(n)
        if x is not None and (x.text or "").strip():
            return x.text.strip()
    return ""

def parse_date(s):
    if not s: return None
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try: d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception: return None
    if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def parse_feed(data):
    """Aceita RSS 2.0, RDF/RSS 1.0 e Atom. Retorna [(titulo, link, datetime|None)]."""
    root = ET.fromstring(data)
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag not in ("item", "entry"): continue
        title = ""; link = ""; date = None
        for c in el:
            ct = c.tag.split("}")[-1]
            if ct == "title": title = (c.text or "").strip()
            elif ct == "link":
                link = (c.attrib.get("href") or c.text or "").strip() or link
            elif ct in ("pubDate", "date", "published", "updated") and date is None:
                date = parse_date((c.text or "").strip())
        if title and link: out.append((re.sub(r"\s+", " ", title), link, date))
    return out

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio news bot)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

def _gtx(text, tl):
    """Tradução automática sem chave (endpoint público do Google Tradutor). Retorna texto ou None."""
    url = ("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=%s&dt=t&q=%s"
           % (tl, urllib.parse.quote(text)))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio news bot)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode("utf-8"))
    return "".join(seg[0] for seg in data[0] if seg and seg[0])

def translate_titles(titles, tl, call=_gtx):
    """Traduz uma lista de títulos em lotes de 10 (separados por quebra de linha).
    Se o lote voltar desalinhado, traduz um a um. Itens que falharem ficam None."""
    out = [None] * len(titles)
    for i in range(0, len(titles), 10):
        chunk = titles[i:i + 10]
        try:
            parts = call("\n".join(chunk), tl).split("\n")
            if len(parts) == len(chunk):
                out[i:i + len(chunk)] = [p.strip() or None for p in parts]; time.sleep(0.4); continue
        except Exception as e:
            print("lote falhou", tl, e, file=sys.stderr)
        for j, t in enumerate(chunk):
            try: out[i + j] = (call(t, tl) or "").strip() or None
            except Exception as e: print("item falhou", tl, e, file=sys.stderr)
            time.sleep(0.4)
    return out

def add_translations(items, previous, call=_gtx):
    """Preenche item["t"] = {pt:..., es:...}. Reaproveita traduções já feitas (mesmo link e título)."""
    prev = {(i["url"], i["title"]): i.get("t", {}) for i in previous}
    for it in items:
        it["t"] = dict(prev.get((it["url"], it["title"]), {}))
    for code, tl in TRANSLATE_TO.items():
        todo = [it for it in items if not it["t"].get(code)]
        if not todo: continue
        res = translate_titles([it["title"] for it in todo], tl, call)
        for it, t in zip(todo, res):
            if t: it["t"][code] = t
    return items

def main(out_path="news.json"):
    items, seen = [], set()
    for label, url, filt in FEEDS:
        try:
            entries = parse_feed(fetch(url))
        except Exception as e:
            print("skip", label, e, file=sys.stderr); continue
        n = 0
        for title, link, date in sorted(entries, key=lambda e: e[2] or datetime(1970,1,1,tzinfo=timezone.utc), reverse=True):
            if n >= PER_SOURCE: break
            if not host_ok(link) or link in seen: continue
            if filt and not ENV_RE.search(title): continue
            seen.add(link); n += 1
            items.append({"source": label, "title": title, "url": link,
                          "date": date.isoformat() if date else None})
    items.sort(key=lambda i: i["date"] or "", reverse=True)
    items = items[:TOTAL]
    previous = []
    if os.path.exists(out_path):
        try: previous = json.load(open(out_path, encoding="utf-8")).get("items", [])
        except Exception: previous = []
    items = add_translations(items, previous)
    if not items:
        print("nenhuma manchete coletada — mantendo o arquivo anterior", file=sys.stderr); return 0
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": items},
              open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(items), "manchetes gravadas")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
