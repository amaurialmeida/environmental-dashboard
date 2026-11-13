"""Gera as 4 ferramentas do portfólio como páginas independentes (widgets/*.html) para o Greenlog.

Uso:  python tools/build_widgets.py  caminho/para/environmental-portfolio/index.html

Cada widget é o próprio index.html do portfólio, só que mostrando apenas a ferramenta escolhida
(o resto da página fica oculto), sem contador de visitas e sem os quadros (iframes) de outros sites.
Assim as ferramentas rodam DENTRO do Greenlog, como o Signal Router, sem abrir o site do portfólio.
Sempre que o index.html do portfólio mudar, rode este script de novo e faça commit dos widgets.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "environmental-portfolio" / "index.html"

# slug -> (atributo, valor) que identifica o bloco da ferramenta no index.html
TOOLS = {
    "monitor": ("id", "env-dashboard"),
    "amauri-virtual": ("id", "terminal-section"),
    "urban-observatory": ("id", "ueo-section"),
    "knowledge-network": ("class", "graph-section"),
}

CSS = """<style id="gl-widget">
html,body{background:transparent!important;margin:0!important;padding:0!important;min-height:0!important}
body>*:not(.gl-chain):not(script):not(style):not(link):not(meta){display:none!important}
.gl-chain{margin:0!important;padding:0!important;max-width:none!important}
.gl-chain>*:not(.gl-keep):not(script):not(style){display:none!important}
.gl-keep{margin-top:0!important}
</style>"""

LANG_JS = """<script>
document.addEventListener('DOMContentLoaded', function(){
  try { setLang('__GL_LANG__'); } catch(e) {}
});
</script>"""


def mark(html, how, value, cls):
    if how == "id":
        m = re.search(r'<(\w+)([^>]*\bid="%s"[^>]*)>' % re.escape(value), html)
    else:
        m = re.search(r'<(\w+)([^>]*\bclass="%s"[^>]*)>' % re.escape(value), html)
    assert m, f"bloco não encontrado: {how}={value}"
    tag = m.group(0)
    if 'class="' in tag:
        new = tag.replace('class="', f'class="{cls} ', 1)
    else:
        new = tag[:-1] + f' class="{cls}">'
    return html.replace(tag, new, 1)


def build(slug):
    how, value = TOOLS[slug]
    h = SRC.read_text(encoding="utf-8")
    # sem contador de visitas nem analytics (não queremos inflar os números do portfólio)
    h = re.sub(r'<script[^>]*goatcounter[^>]*></script>', '', h)
    h = h.replace("https://countapi.mileshilliard.com/api/v1/hit/amauri-almeida-environmental-portfolio-views",
                  "data:application/json,{}")
    # sem quadros de outros sites (exceto o Our World in Data do Observatório)
    def off(m):
        tag = m.group(0)
        if 'id="ow-frame"' in tag:
            return tag
        tag = re.sub(r'\sonload="[^"]*"', '', tag)
        return re.sub(r'\bsrc=', 'data-off-src=', tag)
    h = re.sub(r'<iframe\b[^>]*>', off, h)
    h = mark(h, "id", "main-content", "gl-chain")
    h = mark(h, how, value, "gl-keep")
    h = h.replace("</head>", CSS + "\n</head>", 1)
    h = h.replace("</body>", LANG_JS + "\n</body>", 1)
    return h


if __name__ == "__main__":
    out = HERE / "widgets"
    out.mkdir(exist_ok=True)
    for slug in TOOLS:
        (out / f"{slug}.html").write_text(build(slug), encoding="utf-8")
        print("ok", slug)
