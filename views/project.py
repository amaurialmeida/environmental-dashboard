"""Aba de projeto: print, números-chave, botão para abrir o app e carregamento embutido sob demanda."""
import html as _html
import json
from pathlib import Path

import streamlit as st

from compat import embed_url
from ui_text import EXTRA_NAMES, UI

ROOT = Path(__file__).resolve().parent.parent
THEMES = {t["slug"]: t for t in json.loads((ROOT / "data" / "greenlog.json").read_text(encoding="utf-8"))["themes"]}
PROJECTS = {p["slug"]: p for p in json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))}
SCREENS = ROOT / "assets" / "screens"

CSS = """
<style>
.pj-kpis{display:flex;gap:16px;flex-wrap:wrap;margin:6px 0 18px}
.pj-kpi{flex:1;min-width:200px;max-width:300px;background:rgba(10,20,35,.88);border:2px solid #2ecc71;border-radius:16px;padding:18px 14px;text-align:center;box-shadow:0 0 25px rgba(46,204,113,.2)}
.pj-kpi small{display:block;color:#cbd5e1;font-size:.95rem}
.pj-kpi strong{display:block;color:#2ecc71;font-size:2.2rem;margin-top:4px;text-shadow:0 0 10px rgba(46,204,113,.4)}
.pj-ph{height:340px;border-radius:18px;border:1px dashed rgba(46,204,113,.5);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#94a3b8;background:radial-gradient(circle at 50% 40%,rgba(46,204,113,.12),rgba(5,5,5,.9))}
.pj-ph span{font-size:64px}
</style>
"""


def name_of(slug, lang):
    p = PROJECTS[slug]
    if p["theme"] in THEMES:
        n = THEMES[p["theme"]]["name"]
        n = n.get(lang) or n["pt"]
        return n[len(n.split(" ")[0]) + 1:]          # remove o emoji inicial
    return EXTRA_NAMES[slug].get(lang) or EXTRA_NAMES[slug]["pt"]


def _fmt(kpi, lang):
    loc_dec = len(str(kpi["value"]).split(".")[1]) if "." in str(kpi["value"]) else 0
    v = kpi["value"]
    txt = f"{v:.{loc_dec}f}" if kpi.get("fmt") == "year" else f"{v:,.{loc_dec}f}"
    if kpi.get("fmt") != "year" and lang in ("pt", "es", "it", "de", "el"):
        txt = txt.replace(",", "§").replace(".", ",").replace("§", ".")
    elif kpi.get("fmt") != "year" and lang == "fr":
        txt = txt.replace(",", " ").replace(".", ",")
    return txt + (f" {kpi['unit']}" if kpi["unit"] else "")


def render(slug, lang):
    U, p = UI[lang], PROJECTS[slug]
    st.markdown(CSS, unsafe_allow_html=True)
    if lang == "ar":
        st.markdown("<style>.pj-kpi,h1{direction:rtl}</style>", unsafe_allow_html=True)
    st.markdown(f"# {p['icon']} {_html.escape(name_of(slug, lang))}")

    t = THEMES.get(p["theme"])
    if t:
        st.markdown(f"##### {U['numbers']}")
        cards = "".join(f'<div class="pj-kpi"><small>{_html.escape(k["label"].get(lang) or k["label"]["pt"])}</small>'
                        f'<strong>{_fmt(k, lang)}</strong></div>' for k in t["kpis"])
        st.markdown(f'<div class="pj-kpis">{cards}</div>', unsafe_allow_html=True)

    shot = SCREENS / f"{slug}.png"
    st.markdown(f"##### {U['preview']}")
    if shot.exists():
        st.image(str(shot), width="stretch")
    else:
        st.markdown(f'<div class="pj-ph"><span>{p["icon"]}</span><div>{_html.escape(U["no_preview"])}</div></div>',
                    unsafe_allow_html=True)

    c1, c2, _ = st.columns([1, 1, 2])
    c1.link_button(U["open_app"], p["url"], type="primary", width="stretch")
    key = f"embed_{slug}"
    if c2.button(U["hide"] if st.session_state.get(key) else U["load_here"], key=f"btn_{slug}", width="stretch"):
        st.session_state[key] = not st.session_state.get(key, False)
        st.rerun()
    st.caption(U["heavy"])
    if st.session_state.get(key):
        st.markdown(f"##### {U['embed_title']}")
        embed_url(p["url"] + "?embed=true", 820)
