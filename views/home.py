"""Aba Início: o carrossel original do Greenlog (mesmo visual), alimentado por data/greenlog.json."""
import json
from pathlib import Path

from compat import embed_html

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "greenlog_home.html").read_text(encoding="utf-8")


def _js(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def render(lang):
    data = json.loads((ROOT / "data" / "greenlog.json").read_text(encoding="utf-8"))
    html = (HTML.replace("/*__TRANSLATIONS__*/", _js(data["translations"]))
                .replace("/*__THEMES__*/", _js(data["themes"]))
                .replace("__LANG__", lang))
    embed_html(html, 520)
