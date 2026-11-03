"""Coleta de sinais ambientais reais (sem chaves de API): USGS, NASA EONET, NOAA/NWS e NOAA/SPC."""
import csv, io, math, re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import requests

UA = {"User-Agent": "environmental-portfolio-signal-router (github.com/amaurialmeida)"}
USGS_DAY = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
USGS_WEEK = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"
EONET = "https://eonet.gsfc.nasa.gov/api/v3/events?status=all&days=7&limit=500"
NWS = ("https://api.weather.gov/alerts/active?event="
       "Tsunami%20Warning,Tsunami%20Watch,Tsunami%20Advisory,Tornado%20Warning")
SPC_TODAY = "https://www.spc.noaa.gov/climo/reports/today_torn.csv"
SPC_DAY = "https://www.spc.noaa.gov/climo/reports/{:%y%m%d}_rpts_torn.csv"

CATS = ["eq", "fire", "cyc", "torn", "tsu", "vol", "flood"]
COLORS = {"eq": "#2196f3", "fire": "#ff9800", "cyc": "#22c1ee", "torn": "#8b5cf6",
          "tsu": "#14b8a6", "vol": "#ef4444", "flood": "#1e40af", "oth": "#94a3b8"}
ICONS = {"eq": "🌎", "fire": "🔥", "cyc": "🌀", "torn": "🌪️", "tsu": "🌊", "vol": "🌋", "flood": "💧", "oth": "🌍"}
EONET_CAT = {"wildfires": "fire", "severeStorms": "cyc", "volcanoes": "vol", "floods": "flood"}


def _get(url, timeout=15):
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r


def _try(fn):
    try:
        return fn(), True
    except Exception:
        return None, False


def _utc_day(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()


def _parse_torn(text):
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            rows.append({"lat": float(row["Lat"]), "lng": float(row["Lon"]),
                         "title": f'{row.get("Location","")}, {row.get("State","")}'.strip(", "),
                         "f": row.get("F_Scale", "")})
        except Exception:
            pass
    return rows


# ── Intensidade ambiental por região (indicador próprio, 0–100) ──────────────
REGIONS = ["na", "sa", "eu", "af", "as", "oc"]
_CENT = {
    "na": [(50, -105), (62, -150), (18, -90), (20, -72), (46, -70), (72, -40)],
    "sa": [(-10, -60), (-35, -65), (0, -75), (-50, -72)],
    "eu": [(50, 10), (62, 15), (40, -4), (65, -18), (55, 35)],
    "af": [(8, 20), (-20, 25), (30, 10), (0, 38), (-25, 47)],
    "as": [(35, 95), (50, 90), (23, 78), (35, 50), (39, 45), (10, 105), (-2, 115), (36, 138), (60, 100), (55, 135), (14, 122)],
    "oc": [(-25, 135), (-42, 172), (-8, 148), (-17, 168), (-18, 178), (-20, -175), (20, -157), (-15, -150), (13, 145)],
}
W_EVENT = {"fire": 1.0, "cyc": 6.0, "vol": 3.0, "flood": 3.0, "torn": 1.5, "tsu": 8.0}
IDX_K = 50.0


def region_of(lat, lng):
    """Região mais próxima (pontos de referência de cada continente). Antártida e polos ficam de fora."""
    if lat is None or lng is None or lat < -62:
        return None
    best, bd = None, 1e9
    la = math.radians(lat)
    for r, pts in _CENT.items():
        for clat, clng in pts:
            lb = math.radians(clat)
            h = math.sin((lb - la) / 2) ** 2 + math.cos(la) * math.cos(lb) * math.sin(math.radians(clng - lng) / 2) ** 2
            if h < bd:
                bd, best = h, r
    return best


def quake_weight(mag):
    return min(64.0, max(0.15, 2 ** ((mag or 0) - 4)))


def region_index(buckets):
    """buckets[0] = últimas 24 h, buckets[1..6] = dias anteriores (cada um: {região: peso}). → lista por região."""
    if not buckets or buckets[0] is None:
        return None
    score = lambda raw: int(round(100 * (1 - math.exp(-raw / IDX_K))))
    out = []
    for r in REGIONS:
        now = score(buckets[0].get(r, 0.0))
        prev = [score(b.get(r, 0.0)) for b in buckets[1:] if b is not None]
        delta = round(now - sum(prev) / len(prev)) if prev else None
        out.append({"k": r, "score": now, "delta": delta})
    return out


def load_signals():
    today = datetime.now(timezone.utc).date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    status = {}

    with ThreadPoolExecutor(max_workers=8) as ex:
        f_day = ex.submit(lambda: _try(lambda: _get(USGS_DAY).json()))
        f_week = ex.submit(lambda: _try(lambda: _get(USGS_WEEK).json()))
        f_eo = ex.submit(lambda: _try(lambda: _get(EONET).json()))
        f_nws = ex.submit(lambda: _try(lambda: _get(NWS).json()))
        f_spc = {d: ex.submit(lambda d=d: _try(lambda: _get(SPC_TODAY if d == today else SPC_DAY.format(d)).text))
                 for d in days}
        day_json, ok_day = f_day.result()
        week_json, ok_week = f_week.result()
        eo_json, ok_eo = f_eo.result()
        nws_json, ok_nws = f_nws.result()
        spc = {d: f.result() for d, f in f_spc.items()}

    status["usgs"] = ok_day or ok_week
    status["eonet"] = ok_eo
    status["noaa"] = ok_nws or any(ok for _, ok in spc.values())

    # ── Selo de atualização por fonte (quando a informação foi gerada/consultada) ──
    now_iso = datetime.now(timezone.utc).isoformat()
    usgs_iso = now_iso
    for js in (day_json, week_json):
        try:
            usgs_iso = datetime.fromtimestamp(js["metadata"]["generated"] / 1000, tz=timezone.utc).isoformat()
            break
        except Exception:
            pass
    stamps = {"usgs": usgs_iso if status["usgs"] else None,
              "eonet": now_iso if status["eonet"] else None,
              "noaa": now_iso if status["noaa"] else None}

    # ── Terremotos / tsunamis (USGS) ──────────────────────────────────────────
    quakes = []
    for f in (day_json or {}).get("features", []):
        try:
            p, c = f["properties"], f["geometry"]["coordinates"]
            quakes.append({"title": p.get("place") or "—", "mag": p.get("mag") or 0, "lat": c[1], "lng": c[0],
                           "tsu": bool(p.get("tsunami")), "time": p.get("time")})
        except Exception:
            pass
    eq_week = {d: 0 for d in days}
    tsu_week = {d: 0 for d in days}
    for f in (week_json or {}).get("features", []):
        try:
            d = _utc_day(f["properties"]["time"])
            if d in eq_week:
                eq_week[d] += 1
                if f["properties"].get("tsunami"):
                    tsu_week[d] += 1
        except Exception:
            pass

    # ── NOAA / NWS: alertas ativos ────────────────────────────────────────────
    nws_tsu, nws_torn = [], 0
    for f in (nws_json or {}).get("features", []):
        p = f.get("properties", {})
        if "Tsunami" in (p.get("event") or ""):
            nws_tsu.append({"title": p.get("headline") or p.get("event"), "lat": None, "lng": None})
        elif "Tornado" in (p.get("event") or ""):
            nws_torn += 1
    tsu_week[today] += len(nws_tsu)

    # ── Tornados (NOAA / SPC) ─────────────────────────────────────────────────
    torn_week, torn_points, torn_by_day = {}, [], {}
    for d, (txt, ok) in spc.items():
        if ok and txt is not None:
            rows = _parse_torn(txt)
            torn_week[d] = len(rows)
            torn_by_day[d] = rows
            if d == today:
                torn_points = rows
        else:
            torn_week[d] = None

    # ── NASA EONET ───────────────────────────────────────────────────────────
    events = []
    ev_week = {c: {d: 0 for d in days} for c in ("fire", "cyc", "vol", "flood")}
    for e in (eo_json or {}).get("events", []):
        eid = ((e.get("categories") or [{}])[0] or {}).get("id", "")
        cat = EONET_CAT.get(eid, "oth")
        geoms = e.get("geometry") or []
        last = geoms[-1] if geoms else {}
        pt = last.get("coordinates") if last.get("type") == "Point" else None
        for dd in {g.get("date", "")[:10] for g in geoms}:
            try:
                d = datetime.strptime(dd, "%Y-%m-%d").date()
            except Exception:
                continue
            if cat in ev_week and d in ev_week[cat]:
                ev_week[cat][d] += 1
        events.append({"title": e.get("title", ""), "cat": cat, "active": not e.get("closed"),
                       "date": last.get("date"), "lat": pt[1] if pt else None, "lng": pt[0] if pt else None})

    # ── Índice por região: últimas 24 h vs. 6 janelas de 24 h anteriores ──────
    now_dt = datetime.now(timezone.utc)

    def _bk(dt):
        b = int((now_dt - dt).total_seconds() // 86400)
        return b if 0 <= b <= 6 and (now_dt - dt).total_seconds() >= -3600 else None

    have_hist = bool(week_json and ok_week)
    bks = [{} for _ in range(7)]

    def _add(b, lat, lng, w):
        r = region_of(lat, lng)
        if b is not None and r:
            bks[b][r] = bks[b].get(r, 0.0) + w

    q_src = (week_json or {}).get("features", []) if have_hist else (day_json or {}).get("features", [])
    for f in q_src:
        try:
            pr, c = f["properties"], f["geometry"]["coordinates"]
            mag = pr.get("mag") or 0
            if mag < 2.5:
                continue
            dt = datetime.fromtimestamp(pr["time"] / 1000, tz=timezone.utc)
            w = quake_weight(mag) + (W_EVENT["tsu"] if pr.get("tsunami") else 0)
            _add(_bk(dt), c[1], c[0], w)
        except Exception:
            pass
    for e in (eo_json or {}).get("events", []):
        cat = EONET_CAT.get(((e.get("categories") or [{}])[0] or {}).get("id", ""))
        if not cat:
            continue
        seen = set()
        for g in e.get("geometry") or []:
            try:
                co = g.get("coordinates")
                if g.get("type") != "Point":
                    continue
                dt = datetime.fromisoformat(g["date"].replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                b = _bk(dt)
                if b is not None and b not in seen:
                    seen.add(b)
                    _add(b, co[1], co[0], W_EVENT[cat])
            except Exception:
                pass
    for d, rows in torn_by_day.items():
        b = (today - d).days
        if 0 <= b <= 6:
            for r_ in rows:
                _add(b, r_["lat"], r_["lng"], W_EVENT["torn"])
    if not ok_day and not ok_week and not ok_eo:
        region_idx = None
    else:
        region_idx = region_index(bks if have_hist else [bks[0]])

    series = {"eq": [eq_week[d] for d in days],
              "fire": [ev_week["fire"][d] for d in days],
              "cyc": [ev_week["cyc"][d] for d in days],
              "torn": [torn_week.get(d) for d in days],
              "tsu": [tsu_week[d] for d in days],
              "vol": [ev_week["vol"][d] for d in days],
              "flood": [ev_week["flood"][d] for d in days]}
    active = [e for e in events if e["active"]]
    counts = {"eq": len(quakes),
              "fire": sum(e["cat"] == "fire" for e in active),
              "cyc": sum(e["cat"] == "cyc" for e in active),
              "torn": len(torn_points) if torn_week.get(today) is not None else nws_torn,
              "tsu": sum(q["tsu"] for q in quakes) + len(nws_tsu),
              "vol": sum(e["cat"] == "vol" for e in active),
              "flood": sum(e["cat"] == "flood" for e in active)}
    return {"days": days, "series": series, "counts": counts, "quakes": quakes, "events": active,
            "torn_points": torn_points, "nws_tsu": nws_tsu, "status": status,
            "region_idx": region_idx, "stamps": stamps, "total_active": len(active), "signals": len(quakes) + len(active) + counts["torn"] + len(nws_tsu)}


# ── Classificação de manchetes (mesmas categorias do gráfico) ────────────────
TOPIC_RE = {
    "eq": re.compile(r"earthquake|quake|seismic|tremor", re.I),
    "fire": re.compile(r"wildfire|bushfire|forest fire|blaze|\bfires?\b", re.I),
    "cyc": re.compile(r"cyclone|hurricane|typhoon|tropical storm|\bstorm", re.I),
    "torn": re.compile(r"tornado", re.I),
    "tsu": re.compile(r"tsunami", re.I),
    "vol": re.compile(r"volcan|eruption", re.I),
    "flood": re.compile(r"flood|deluge|monsoon|heavy rain", re.I),
}


def topics(title):
    return [k for k, rx in TOPIC_RE.items() if rx.search(title or "")]
