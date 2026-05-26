import streamlit as st
import time

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# ===================== CSS MODERNO E ELEGANTE =====================
st.markdown("""
<style>
    .title { 
        font-size: 5rem; 
        background: linear-gradient(90deg, #2ecc71, #3498db); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        font-weight: bold; 
        letter-spacing: 6px;
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
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(46, 204, 113, 0.35);
        height: 100%;
        transition: all 0.3s;
    }
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.6);
    }
    .kpi-number {
        font-size: 3.6rem;
        font-weight: bold;
        color: #2ecc71;
        margin: 10px 0;
    }
    .kpi-label {
        font-size: 1.2rem;
        color: #ddd;
        min-height: 55px;
    }
    .delta {
        font-size: 1.35rem;
        font-weight: bold;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">GREENLOG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</p>', unsafe_allow_html=True)

# Idioma
col1, col2 = st.columns([8, 2])
with col2:
    st.selectbox("🌐 Idioma", ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"], key="lang")

st.markdown("---")

# ===================== DADOS REAIS DOS SEUS PROJETOS =====================
themes = [
    ("🌍 Temperaturas Globais", [  # Você pode adicionar os números exatos depois
        ("Temperatura Média Global", "14.92°C", "↑ 1.45%"),
        ("Ano Mais Quente", "2025", "↑ 0.9%"),
        ("Anomalia Atual", "+1.54°C", "↑ 15%")
    ]),
    
    ("☀️ Energia Solar", [
        ("Energia Gerada", "390 MWh", "↑ 1.07 GWh"),
        ("CO₂ Evitado", "953 t", ""),
        ("Árvores Equivalentes", "7.250", "")
    ]),
    
    ("🐝 Colapso das Abelhas", [
        ("Colmeias Perdidas", "338", ""),
        ("Abelhas Perdidas", "~20M", ""),
        ("Produtores Monitorados", "4", ""),
        ("Colmeias RS (2024)", "6.300+", "")
    ]),
    
    ("🐝 Abelhas sem Ferrão", [
        ("Espécies Meliponini", "12+6", ""),
        ("Registros GBIF", "24.500", ""),
        ("Estados Cobertos", "15", ""),
        ("Espécies Ameaçadas", "4 VU", "")
    ]),
    
    ("🌬️ Potencial Eólico", [
        ("Velocidade Média", "30.2 km/h", ""),
        ("Fator de Capacidade", ">60%", ""),
        ("Rajada Máxima", "130 km/h", ""),
        ("Potencial Total", "9.500 MW", "")
    ]),
    
    ("💧 Qualidade da Água", [
        ("IQA Médio Geral", "81.9", ""),
        ("Estações Excelente", "3/18", ""),
        ("Rios Monitorados", "10", ""),
        ("Parâmetros Analisados", "4", "")
    ]),
    
    ("🌋 Monitoramento Sísmico", [
        ("Magnitude Registrada", "M7.4", ""),
        ("Profundidade", "10 km", ""),
        ("Evacuados", "1.800", ""),
        ("Réplicas Registradas", "50+", "")
    ]),
    
    ("🌿 Espécies Invasoras", [
        ("Castores Estimados", "110.000+", ""),
        ("Represas Construídas", "70.600", ""),
        ("Hectares Devastados", "31.000 ha", ""),
        ("Ano de Introdução", "1946", "")
    ]),
    
    ("🌊 Previsão El Niño 2026", [
        ("Probabilidade El Niño", "98%", ""),
        ("Niño 3.4 Atual", "+0.9°C", ""),
        ("Previsão Pico", "+2.4°C", ""),
        ("Chance Super El Niño", "33%", "")
    ])
]

# ===================== CARROSSEL AUTOMÁTICO =====================
placeholder = st.empty()
current = 0

while True:
    with placeholder.container():
        theme_name, kpis = themes[current % len(themes)]
        
        st.markdown(f"<h2 style='text-align:center; color:#2ecc71; margin:25px 0;'>{theme_name}</h2>", unsafe_allow_html=True)
        
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
        
        st.caption(f"● Slide {current % len(themes) + 1} de {len(themes)} • Troca automática a cada 15 segundos")
    
    time.sleep(15)
    current += 1
    st.rerun()
