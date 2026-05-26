import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# ===================== CSS =====================
st.markdown("""
<style>
    .title { 
        font-size: 5rem; 
        background: linear-gradient(90deg, #2ecc71, #3498db); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        font-weight: bold; 
        letter-spacing: 5px;
    }
    .subtitle { 
        color: #2ecc71; 
        text-align: center; 
        font-size: 1.9rem; 
        margin-top: -25px;
        margin-bottom: 40px;
    }
    .kpi-card {
        background: rgba(15, 25, 40, 0.95);
        border: 2px solid #2ecc71;
        border-radius: 20px;
        padding: 35px 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(46, 204, 113, 0.5);
        height: 100%;
    }
    .kpi-number {
        font-size: 3.8rem;
        font-weight: bold;
        color: #2ecc71;
        margin: 12px 0;
    }
    .kpi-label {
        font-size: 1.25rem;
        color: #ddd;
    }
    .delta {
        font-size: 1.45rem;
        font-weight: bold;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">GREENLOG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</p>', unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])
with col2:
    st.selectbox("🌐 Idioma", ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"])

st.markdown("---")

# ===================== DADOS COMPLETOS =====================
themes = [
    ("🌍 Temperaturas Globais", [
        ("Temperatura Média Global", "14.92°C", "↑ 1.45%"),
        ("Ano Mais Quente", "2025", "↑ 0.9%"),
        ("Anomalia Atual", "+1.54°C", "↑ 15%")
    ]),
    ("☀️ Energia Solar", [
        ("Energia Gerada", "390 MWh", ""),
        ("CO₂ Evitado", "953 t", ""),
        ("Árvores Equivalentes", "7.250", "")
    ]),
    ("🐝 Colapso das Abelhas", [
        ("Colmeias Perdidas", "338", ""),
        ("Abelhas Perdidas", "~20M", ""),
        ("Colmeias RS (2024)", "6.300+", "")
    ]),
    ("🐝 Abelhas sem Ferrão", [
        ("Espécies Monitoradas", "18", ""),
        ("Registros GBIF", "24.500", ""),
        ("Estados Cobertos", "15", ""),
        ("Espécies Ameaçadas", "4 VU", "")
    ]),
    ("🌬️ Potencial Eólico", [
        ("Vel. Média", "30.2 km/h", ""),
        ("Fator de Capacidade", ">60%", ""),
        ("Rajada Máxima", "130 km/h", ""),
        ("Potencial Total", "9.500 MW", "")
    ]),
    ("💧 Qualidade da Água", [
        ("IQA Médio", "81.9", ""),
        ("Estações Excelente", "3/18", ""),
        ("Rios Monitorados", "10", "")
    ]),
    ("🌋 Monitoramento Sísmico", [
        ("Magnitude", "M7.4", ""),
        ("Profundidade", "10 km", ""),
        ("Evacuados", "1.800", ""),
        ("Réplicas", "50+", "")
    ]),
    ("🌿 Espécies Invasoras", [
        ("Castores Estimados", "110.000+", ""),
        ("Hectares Devastados", "31.000 ha", ""),
        ("Represas Construídas", "70.600", "")
    ]),
    ("🌊 El Niño 2026", [
        ("Probabilidade", "98%", ""),
        ("Niño 3.4 Atual", "+0.9°C", ""),
        ("Previsão Pico", "+2.4°C", ""),
        ("Super El Niño", "33%", "")
    ])
]

# Controle de Slide
if 'current_slide' not in st.session_state:
    st.session_state.current_slide = 0

theme_name, kpis = themes[st.session_state.current_slide]

st.markdown(f"<h2 style='text-align:center; color:#2ecc71; margin:30px 0;'>{theme_name}</h2>", unsafe_allow_html=True)

cols = st.columns(len(kpis))
for i, (label, value, delta) in enumerate(kpis):
    color = "#2ecc71" if "↑" in delta else "#e74c3c"
    with cols[i]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="delta" style="color:{color};">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

# Navegação
st.markdown("---")
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("← Tema Anterior", use_container_width=True):
        st.session_state.current_slide = (st.session_state.current_slide - 1) % len(themes)
        st.rerun()

with col_next:
    if st.button("Próximo Tema →", use_container_width=True):
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(themes)
        st.rerun()

st.caption(f"Slide {st.session_state.current_slide + 1} de {len(themes)}")
