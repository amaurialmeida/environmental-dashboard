"""Ferramentas interativas do portfólio, rodando DENTRO do Greenlog (sem abrir o site do portfólio).

Cada ferramenta é uma página independente em widgets/<slug>.html, gerada por tools/build_widgets.py
a partir do index.html do portfólio (mesmo código, mesmos 9 idiomas, mesmas fontes de dados públicas).
Funciona como o Signal Router: um painel escuro que ocupa a página, sem quadro do site original.
Para atualizar depois de mudar o portfólio:  python tools/build_widgets.py ../environmental-portfolio/index.html
"""
from pathlib import Path

import streamlit as st

from compat import embed_html

WIDGETS = Path(__file__).resolve().parent.parent / "widgets"

# altura do painel (px); o conteúdo rola dentro do painel se a janela for estreita
TOOLS = {
    "monitor":           {"icon": "🛰️", "title": "Monitoramento Ambiental em Tempo Real", "height": 310},
    "amauri-virtual":    {"icon": "🤖", "title": "Amauri Virtual", "height": 800},
    "urban-observatory": {"icon": "🏙️", "title": "Urban Environmental Observatory", "height": 2700},
    "knowledge-network": {"icon": "🕸️", "title": "Rede de Conhecimento · Conexões temáticas", "height": 980},
}

CSS = """
<style>
#MainMenu,footer{visibility:hidden}
.block-container{max-width:1440px;padding:20px 20px 40px}
</style>
"""


@st.cache_data(show_spinner=False)
def _widget(slug: str) -> str:
    return (WIDGETS / f"{slug}.html").read_text(encoding="utf-8")


def render(slug: str, lang: str = "pt") -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    html = _widget(slug).replace("__GL_LANG__", lang)
    embed_html(html, TOOLS[slug]["height"])


TITLES = {
    "monitor": {"pt": "Monitoramento Ambiental em Tempo Real", "en": "Real-Time Environmental Monitoring", "es": "Monitoreo Ambiental en Tiempo Real",
                "it": "Monitoraggio Ambientale in Tempo Reale", "fr": "Surveillance environnementale en temps réel", "de": "Umweltüberwachung in Echtzeit",
                "zh": "实时环境监测", "ar": "المراقبة البيئية في الوقت الفعلي", "el": "Περιβαλλοντική παρακολούθηση σε πραγματικό χρόνο"},
    "amauri-virtual": {"pt": "Amauri Virtual", "en": "Amauri Virtual", "es": "Amauri Virtual", "it": "Amauri Virtual", "fr": "Amauri Virtual",
                       "de": "Amauri Virtual", "zh": "Amauri 虚拟助手", "ar": "أمَوري الافتراضي", "el": "Amauri Virtual"},
    "urban-observatory": {"pt": "Observatório Ambiental Urbano", "en": "Urban Environmental Observatory", "es": "Observatorio Ambiental Urbano",
                          "it": "Osservatorio Ambientale Urbano", "fr": "Observatoire environnemental urbain", "de": "Städtisches Umweltobservatorium",
                          "zh": "城市环境观测站", "ar": "المرصد البيئي الحضري", "el": "Αστικό Περιβαλλοντικό Παρατηρητήριο"},
    "knowledge-network": {"pt": "Rede de Conhecimento", "en": "Knowledge Network", "es": "Red de Conocimiento", "it": "Rete della Conoscenza",
                          "fr": "Réseau de connaissances", "de": "Wissensnetzwerk", "zh": "知识网络", "ar": "شبكة المعرفة", "el": "Δίκτυο γνώσης"},
}


def title_of(slug: str, lang: str = "pt") -> str:
    return TITLES[slug].get(lang) or TITLES[slug]["pt"]
