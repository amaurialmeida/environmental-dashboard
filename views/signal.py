"""Aba Environmental Signal Router (dados reais, sem chaves de API) — tema escuro do Greenlog."""
import html, json, math, os, tempfile
from datetime import datetime, timezone

import plotly.graph_objects as go
import requests
import streamlit as st

from router import signals as S
from router.i18n import T

NEWS_URL = os.getenv("NEWS_JSON_URL", "https://amaurialmeida.github.io/environmental-portfolio/news.json")
HEADLINE_SECONDS = 12          # ~12 s por manchete → 25 manchetes ≈ 5 minutos
DEFAULT_SHOWN = 12


CSS = """
<style>
#MainMenu,footer{visibility:hidden}
.block-container{max-width:1440px;padding:20px 20px 40px}
[class*="st-key-card"]{background:rgba(10,20,35,.88);border:1px solid rgba(46,204,113,.35);border-radius:24px;padding:20px;box-shadow:0 0 25px rgba(46,204,113,.15)}
.metric{display:flex;align-items:center;gap:14px}
.metric .mi{font-size:28px}
.metric small{color:#94a3b8;display:block}
.metric strong{display:block;font-size:34px;line-height:1.1;color:#2ecc71;text-shadow:0 0 10px rgba(46,204,113,.4)}
.sec{font-size:18px;font-weight:700;margin-bottom:12px;color:#e5e7eb}
.ev{display:flex;gap:10px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.08);font-size:14px;color:#e5e7eb}
.ev .ic{font-size:22px}.ev small{color:#94a3b8}.ev strong{overflow-wrap:anywhere}
.srow{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.08);color:#e5e7eb}
.on{color:#2ecc71;font-weight:600}.off{color:#f87171;font-weight:600}
.stat{display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.08);color:#e5e7eb}
.ctitle{text-align:center;font-size:28px;font-weight:700;margin:0 0 6px;color:#2ecc71;text-shadow:0 0 15px rgba(46,204,113,.5)}
.meta{color:#94a3b8;font-size:14px;margin-bottom:8px}
.hl img{width:100%;height:180px;object-fit:cover;border-radius:18px;margin-bottom:12px}
.hl h3{color:#e5e7eb}.hl p{color:#94a3b8;margin-top:6px}
@media(max-width:700px){.ctitle{font-size:20px}}
</style>
"""

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
    L = T[lang]
    if lang == "ar":
        st.markdown("<style>.ev,.srow,.stat,.meta{direction:rtl}</style>", unsafe_allow_html=True)
    D = signals()
    news, news_updated, news_mode = load_news(lang)
    news_topics = [S.topics(i["title"]) for i in news]
    mentions = {c: sum(c in t for t in news_topics) for c in S.CATS}

    # ── métricas ─────────────────────────────────────────────────────────────────
    cols = st.columns(5)
    for col, cat in zip(cols, ["eq", "fire", "cyc", "torn", "tsu"]):
        with col.container(key=f"card_m_{cat}"):
            st.markdown(f'<div class="metric"><div class="mi">{S.ICONS[cat]}</div><div><small>{esc(L[cat])}</small>'
                        f'<strong>{D["counts"][cat]}</strong></div></div>', unsafe_allow_html=True)

    left, center, right = st.columns([1.0, 2.2, 1.05])

    # ── foco (liga globo, gráfico, eventos e boletim) ────────────────────────────
    focus_opts = ["all"] + S.CATS
    def fmt(k):
        if k == "all":
            return L["all"]
        return f'{S.ICONS[k]} {L[k]}' + (f' · 📰{mentions[k]}' if mentions[k] else "")

    # ── centro: globo ────────────────────────────────────────────────────────────
    with center:
        with st.container(key="card_globe"):
            st.markdown(f'<div class="ctitle">{esc(L["title"])}</div>', unsafe_allow_html=True)
            focus = st.pills(L["focus"], focus_opts, selection_mode="single", default="all", key="focus",
                             format_func=fmt, label_visibility="collapsed") or "all"
            pts = {c: [] for c in S.CATS}
            pts["eq"] = [{"lat": q["lat"], "lng": q["lng"], "title": f'{q["title"]} · {L["mag"]} {q["mag"]}',
                          "size": max(4, (q["mag"] or 1) * 2.4)} for q in D["quakes"]]
            pts["tsu"] = [{"lat": q["lat"], "lng": q["lng"], "title": q["title"], "size": 15} for q in D["quakes"] if q["tsu"]]
            pts["torn"] = [{"lat": p["lat"], "lng": p["lng"], "title": p["title"], "size": 9} for p in D["torn_points"]]
            for e in D["events"]:
                if e["cat"] in pts and e["lat"] is not None:
                    pts[e["cat"]].append({"lat": e["lat"], "lng": e["lng"], "title": e["title"], "size": 10})
            fig = go.Figure()
            shown = S.CATS if focus == "all" else [focus]
            for c in shown:
                if not pts[c]:
                    continue
                sym = "circle-open" if c == "tsu" else "circle"
                fig.add_trace(go.Scattergeo(
                    lat=[p["lat"] for p in pts[c]], lon=[p["lng"] for p in pts[c]], mode="markers", name=L[c],
                    text=[p["title"] for p in pts[c]], hovertemplate="%{text}<extra>" + L[c] + "</extra>",
                    marker=dict(size=[p["size"] for p in pts[c]], color=S.COLORS[c], symbol=sym, opacity=.85,
                                line=dict(width=2 if c == "tsu" else 0.5, color=S.COLORS[c] if c == "tsu" else "#fff"))))
            lat0, lon0 = 15, -40
            if focus != "all" and pts[focus]:
                lat0 = sum(p["lat"] for p in pts[focus][:1]); lon0 = sum(p["lng"] for p in pts[focus][:1])
            fig.update_geos(projection_type="orthographic", projection_rotation=dict(lon=lon0, lat=lat0),
                            showland=True, landcolor="#2f6b45", showocean=True, oceancolor="#0b2a4a",
                            showcountries=True, countrycolor="rgba(255,255,255,.35)", coastlinecolor="#cfe8ff",
                            showlakes=True, lakecolor="#0d4b86", bgcolor="rgba(0,0,0,0)")
            fig.update_layout(height=640, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, dragmode="pan")
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False, "scrollZoom": False}, key="sr_globe")

    # ── esquerda: eventos + fontes ───────────────────────────────────────────────
    def build_events():
        rows = []
        for q in sorted(D["quakes"], key=lambda q: q["mag"] or 0, reverse=True)[:4]:
            rows.append(("eq", q["title"], f'{L["mag"]} {q["mag"]}'))
        for t in D["nws_tsu"][:2]:
            rows.append(("tsu", t["title"], "NOAA"))
        for p in D["torn_points"][:2]:
            rows.append(("torn", p["title"], f'NOAA SPC · F {p["f"]}' if p["f"] not in ("", "UNK") else "NOAA SPC"))
        for e in sorted(D["events"], key=lambda e: e["date"] or "", reverse=True):
            if e["cat"] != "oth":
                rows.append((e["cat"], e["title"], "NASA EONET"))
        if focus != "all":
            rows = [r for r in rows if r[0] == focus]
        else:  # no máximo 2 do mesmo tipo (exceto terremotos) para mostrar variedade
            seen, mix = {}, []
            for r in rows:
                seen[r[0]] = seen.get(r[0], 0) + 1
                if seen[r[0]] <= (3 if r[0] == "eq" else 2):
                    mix.append(r)
            rows = mix
        return rows[:8]

    with left:
        with st.container(key="card_events"):
            st.markdown(f'<div class="sec">{esc(L["recent"])}</div>', unsafe_allow_html=True)
            ev = build_events()
            st.markdown("".join(f'<div class="ev"><div class="ic">{S.ICONS[c]}</div><div><strong dir="auto">{esc(t)}</strong>'
                                f'<br><small>{esc(m)}</small></div></div>' for c, t, m in ev) or
                        f'<div class="meta">{esc(L["nodata"])}</div>', unsafe_allow_html=True)
        with st.container(key="card_sources"):
            st.markdown(f'<div class="sec">{esc(L["src"])}</div>', unsafe_allow_html=True)
            rows = [("USGS", D["status"]["usgs"]), ("NASA EONET", D["status"]["eonet"]),
                    ("NOAA", D["status"]["noaa"]), ("Fetch News", news_mode != "off")]
            st.markdown("".join(f'<div class="srow"><span>{n}</span><span class="{"on" if ok else "off"}">'
                                f'{L["on"] if ok else L["off"]}</span></div>' for n, ok in rows), unsafe_allow_html=True)

    # ── direita: gráfico + estatísticas + destaque ───────────────────────────────
    with right:
        with st.container(key="card_chart"):
            st.markdown(f'<div class="sec">{esc(L["act"])} <span class="meta">· {esc(L["last7"])}</span></div>',
                        unsafe_allow_html=True)
            norm = st.toggle(L["norm"], value=True, key="norm") if focus == "all" else False
            labels = [d.strftime("%d/%m") for d in D["days"]]
            cf = go.Figure()
            for c in (S.CATS if focus == "all" else [focus]):
                raw = D["series"][c]
                vals = [None if v is None else v for v in raw]
                if norm:
                    peak = max([v for v in vals if v is not None] or [0])
                    y = [None if v is None else (round(100 * v / peak, 1) if peak else 0) for v in vals]
                else:
                    y = vals
                cf.add_trace(go.Scatter(x=labels, y=y, mode="lines+markers", name=L[c], customdata=raw,
                                        line=dict(color=S.COLORS[c], shape="spline", width=2.5), marker=dict(size=6),
                                        fill="tozeroy" if focus != "all" else None,
                                        hovertemplate=f"{L[c]}: %{{customdata}}<extra></extra>", connectgaps=False))
            cf.update_layout(height=300, margin=dict(l=0, r=0, t=6, b=0), paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"), legend=dict(orientation="h", y=-0.28, font=dict(size=11, color="#cbd5e1")),
                             yaxis=dict(rangemode="tozero", gridcolor="rgba(255,255,255,.1)", title=dict(text=L["axis_norm"] if norm else L["axis_abs"], font=dict(size=11))),
                             xaxis=dict(gridcolor="rgba(255,255,255,.05)", tickangle=0, tickfont=dict(size=9)))
            st.plotly_chart(cf, width="stretch", config={"displayModeBar": False}, key="sr_chart")
        with st.container(key="card_stats"):
            for k, v in ((L["active"], D["total_active"]), (L["fire"], D["counts"]["fire"]), (L["sig"], D["signals"])):
                st.markdown(f'<div class="stat"><span>{esc(k)}</span><strong>{v}</strong></div>', unsafe_allow_html=True)
        with st.container(key="card_hl"):
            st.markdown(f'<div class="sec">{esc(L["hl"])}</div><div class="hl">'
                        f'<img src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200" alt="">'
                        f'<h3>{esc(L["hlt"])}</h3><p>{esc(L["hlp"])}</p></div>', unsafe_allow_html=True)

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
            if focus != "all":
                f_idx = [n for n in idx if focus in news_topics[n]]
                if f_idx:
                    idx = f_idx
                else:
                    note = L["nofocus"]
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
