"""Tira um print de cada projeto (apps Streamlit) e salva em assets/screens/<slug>.png.

Roda numa GitHub Action (ver .github/workflows/screens.yml) — sem chaves e sem contas.
Apps "dormindo" são acordados automaticamente. Se um app falhar, o print antigo é mantido.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"
OUT.mkdir(parents=True, exist_ok=True)
projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
only = set(sys.argv[1:])
done = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    for pr in projects:
        if only and pr["slug"] not in only:
            continue
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        try:
            page.goto(pr["url"] + "?embed=true", wait_until="domcontentloaded", timeout=60000)
            # app dormindo: botão "Yes, get this app back up!"
            wake = page.get_by_role("button", name="get this app back up")
            if wake.count():
                wake.first.click()
            page.wait_for_selector('[data-testid="stApp"]', timeout=120000)
            page.wait_for_timeout(15000)      # tempo para mapas e gráficos desenharem
            page.screenshot(path=str(OUT / f"{pr['slug']}.png"))
            print("ok", pr["slug"])
            done.append(pr["slug"])
        except Exception as e:                  # mantém o print anterior
            print("falhou", pr["slug"], e)
        finally:
            page.close()
    browser.close()

print(f"{len(done)} prints gerados:", ", ".join(done) or "nenhum")
if not done:
    sys.exit(1)          # a Action fica vermelha se nada foi gerado
