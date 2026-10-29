"""Coleta de sinais ambientais reais (sem chaves de API): USGS, NASA EONET, NOAA/NWS e NOAA/SPC."""
import csv, io, re
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
    torn_week, torn_points = {}, []
    for d, (txt, ok) in spc.items():
        if ok and txt is not None:
            rows = _parse_torn(txt)
            torn_week[d] = len(rows)
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
            "total_active": len(active), "signals": len(quakes) + len(active) + counts["torn"] + len(nws_tsu)}


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
