# 🌱 Greenlog — Environmental Intelligence Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://environmental-dashboard.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Environmental Data Aggregation — Live KPI Dashboard**
**Author:** Amauri Almeida de Souza Junior

---

## ❓ Project Question

> "Can a single, self-playing dashboard summarize the full breadth of a decade of environmental field research — climate, energy, biodiversity, water, and geohazards — in a format a non-specialist can absorb in seconds per topic, without losing what makes it credible to a specialist?"

**Answer:** Yes. Greenlog condenses nine distinct environmental research themes into an auto-rotating carousel of animated KPI cards, layered over a live global wind map, so each topic is delivered as 3–4 headline numbers with count-up animation rather than a dense report — while remaining fully sourced from the author's own field research and public datasets (GBIF, seismological records, water quality monitoring).

---

## 📊 Themes Covered

| # | Theme | Example KPIs |
|---|---|---|
| 1 | 🌍 Global Temperatures | Global average temperature, hottest year on record, current anomaly |
| 2 | ☀️ Solar Energy | Energy generated, CO₂ avoided, equivalent trees offset |
| 3 | 🐝 Bee Colony Collapse | Hives lost, bees lost, regional hive counts (RS, 2024) |
| 4 | 🐝 Stingless Bees (Meliponini) | Monitored species, GBIF occurrence records, states covered, threatened species |
| 5 | 🌬️ Wind Energy Potential | Average wind speed, capacity factor, max gust, total regional potential |
| 6 | 💧 Water Quality | Average Water Quality Index (IQA), stations rated "excellent," rivers monitored |
| 7 | 🌋 Seismic Monitoring | Magnitude, depth, evacuations, aftershocks — Drake Passage region |
| 8 | 🌿 Invasive Species (Patagonian Beavers) | Estimated population, hectares devastated, dams built |
| 9 | 🌊 El Niño 2026 | Event probability, current Niño 3.4 index, peak forecast, Super El Niño odds |

---

## 🔵 Key Features

- **Live global backdrop** — an embedded real-time wind map (Windy.com) runs behind the dashboard, tinted and blended into the visual theme rather than shown as a plain widget.
- **Auto-rotating carousel** — cycles through all 9 themes automatically every 15 seconds, with manual navigation available.
- **Animated KPI cards** — each metric counts up from zero on entry, using locale-aware number formatting (decimal comma for PT/ES contexts).
- **Trilingual by design** — every theme name and KPI label is stored in a structured PT/EN/ES dictionary and switches instantly via the language selector, with no page reload.
- **Zero backend dependency** — the entire interactive experience (map, cards, animation, language switching) runs client-side inside a single embedded HTML/CSS/JS component, with Streamlit acting purely as the delivery shell.
- **Cross-project synthesis** — each theme summarizes findings that map to the author's dedicated deep-dive projects (e.g., seismic data connects to the Puerto Williams earthquake fieldwork, bee data connects to the standalone colony collapse research).

---

## 🔬 Methodology

```
Data sourcing    →  Aggregated from the author's own field research, public
                     biodiversity records (GBIF), water quality monitoring
                     stations, seismological reports, and climate datasets

Presentation     →  9 themed KPI sets, each with 3–4 headline numbers,
                     rendered as glassmorphic cards over a live map backdrop

Animation        →  JavaScript requestAnimationFrame count-up (0 → target
                     value) triggered on each slide transition

Internationalization →  Structured translation object per theme/label,
                     switched via DOM text replacement (no reload)
```

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Streamlit shell / app entry point |
| Streamlit `components.v1.html` | Embeds the full interactive experience |
| HTML5 / CSS3 | Layout, glassmorphism, gradients, responsive KPI cards |
| Vanilla JavaScript | Slide rotation, count-up animation, language switching |
| Windy.com Embed API | Live global wind/weather map backdrop |

---

## 📁 Repository Structure

```
environmental-dashboard/
├── app.py                   # Streamlit entry point (embeds the HTML/JS dashboard)
├── requirements.txt         # Python dependencies
├── README.md                  # This file (English)
├── README.pt-BR.md            # Portuguese version
└── README.es.md               # Spanish version
```

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/environmental-dashboard.git
cd environmental-dashboard

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[environmental-dashboard.streamlit.app](https://environmental-dashboard.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇬🇧 English, and 🇪🇸 Spanish via the in-app language selector.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2025–2026 · Amauri Almeida de Souza Junior · Portfolio Project
