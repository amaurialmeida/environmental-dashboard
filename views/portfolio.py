"""Ferramentas interativas do portfólio, preservando o index.html publicado.

As páginas usam o próprio index.html ativo do portfólio em um iframe com âncora.
Isso evita duplicar os datasets e o JavaScript em duas bases de código diferentes.
"""
import streamlit as st

from compat import embed_url

PORTFOLIO = "https://amaurialmeida.github.io/environmental-portfolio/"

TOOLS = {
    "monitor": {
        "icon": "🛰️",
        "title": "Monitoramento Ambiental em Tempo Real",
        "anchor": "#esr-section",
        "description": "Feeds públicos ao vivo de USGS, NASA EONET e NOAA, com eventos ambientais, log de eco-inteligência e boletim de notícias.",
    },
    "amauri-virtual": {
        "icon": "🤖",
        "title": "Amauri Virtual",
        "anchor": "#terminal-section",
        "description": "Terminal conversacional do portfólio para perguntas sobre projetos, formação, habilidades e disponibilidade.",
    },
    "urban-observatory": {
        "icon": "🏙️",
        "title": "Urban Environmental Observatory",
        "anchor": "#ueo-section",
        "description": "Comparação entre cidades usando os quatro eixos do dataset curado: água, conforto, áreas verdes e resíduos.",
    },
    "knowledge-network": {
        "icon": "🕸️",
        "title": "Rede de Conhecimento · Conexões temáticas",
        "anchor": "#network-graph",
        "description": "Grafo D3 que conecta temas ambientais, tecnologias, métodos e fontes de dados dos projetos.",
    },
}

CSS = """
<style>
.portfolio-intro{padding:16px 20px;margin-bottom:14px;border:1px solid rgba(46,204,113,.28);border-radius:16px;background:linear-gradient(135deg,rgba(13,35,43,.95),rgba(10,24,38,.78));}
.portfolio-intro h1{margin:0 0 6px;color:#e8f3ff;font-size:1.55rem;}
.portfolio-intro p{margin:0;color:#a8c5c0;line-height:1.55;}
.portfolio-note{font-size:.8rem;color:#7f9bbb;margin-top:8px;}
</style>
"""


def render(slug: str, lang: str = "pt") -> None:
    tool = TOOLS[slug]
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="portfolio-intro"><h1>{tool["icon"]} {tool["title"]}</h1>'
        f'<p>{tool["description"]}</p>'
        '<div class="portfolio-note">Conteúdo sincronizado com a versão ativa do portfólio · amaurialmeida.github.io/environmental-portfolio</div></div>',
        unsafe_allow_html=True,
    )
    st.link_button("Abrir esta ferramenta no portfólio ↗", PORTFOLIO + tool["anchor"])
    # O fragmento posiciona o iframe diretamente na seção correspondente, mantendo
    # a implementação visual e os fallbacks do index.html original.
    embed_url(PORTFOLIO + tool["anchor"], 1100)
