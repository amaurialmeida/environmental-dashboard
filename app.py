"""Greenlog — Environmental Intelligence Hub (Streamlit).

Abas laterais: Início (carrossel original) · Environmental Signal Router · 12 projetos do portfólio.
"""
import json
from pathlib import Path

import streamlit as st

from ui_text import LANGS, UI
from views import home, project, signal

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Greenlog • Environmental Intelligence", page_icon="🌱", layout="wide",
                   initial_sidebar_state="expanded")


def pick_lang():
    q = st.query_params.get("lang")
    if q in UI:
        return q
    try:
        loc = (st.context.locale or "")[:2].lower()
        if loc in UI:
            return loc
    except Exception:
        pass
    return "pt"


if "lang" not in st.session_state:
    st.session_state["lang"] = pick_lang()

st.markdown("""
<style>
[data-testid="stSidebar"]{border-right:1px solid rgba(46,204,113,.25)}
[data-testid="stSidebarNavLink"]{border-radius:10px}
[data-testid="stSidebarNavLink"]:hover{background:rgba(46,204,113,.12)}
[data-testid="stSidebarNavLink"][aria-current="page"]{background:rgba(46,204,113,.2);border:1px solid rgba(46,204,113,.5)}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.selectbox(UI[st.session_state["lang"]]["lang"], list(LANGS), key="lang", format_func=lambda k: LANGS[k])
lang = st.session_state["lang"]
U = UI[lang]

projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))


def make_project_page(p):
    return st.Page(lambda s=p["slug"]: project.render(s, st.session_state["lang"]),
                   title=project.name_of(p["slug"], lang), icon=p["icon"], url_path=p["slug"])


pages = {
    U["sec_main"]: [
        st.Page(lambda: home.render(st.session_state["lang"]), title=U["home"], icon="🌱", url_path="inicio", default=True),
        st.Page(lambda: signal.render(st.session_state["lang"]), title=U["router"], icon="🛰️", url_path="signal-router"),
    ],
    U["sec_projects"]: [make_project_page(p) for p in projects],
}
st.navigation(pages, expanded=True).run()
