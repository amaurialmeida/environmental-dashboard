import streamlit as st

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# ===================== CSS + JAVASCRIPT (Count-up + Auto Carousel) =====================
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
        padding: 35px 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(46, 204, 113, 0.4);
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
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 12px;
    }
</style>

<script>
let currentSlide = 0;
const totalSlides = 9;

function animateCount(id, start, end, duration) {
    let startTime = null;
    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = Math.min((timestamp - startTime) / duration, 1);
        let value = Math.floor(progress * (end - start) + start);
        document.getElementById(id).innerHTML = value.toLocaleString('pt-BR');
        if (progress < 1) requestAnimationFrame(step);
        else document.getElementById(id).innerHTML = end.toLocaleString('pt-BR');
    }
    requestAnimationFrame(step);
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    document.getElementById('carousel').style.opacity = '0';
    setTimeout(() => {
        window.location.reload();
    }, 600);
}

// Inicia o timer automático
setTimeout(() => {
    nextSlide();
}, 15000);
</script>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">GREENLOG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</p>', unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])
with col2:
    st.selectbox("🌐 Idioma", ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"])

st.markdown("---")

# Dados
themes = [
    ("🌍 Temperaturas Globais", [
        ("Temperatura Média Global", 14.92, "°C", "↑ 1.45%"),
        ("Ano Mais Quente", 2025, "", "↑ 0.9%"),
        ("Anomalia Atual", 1.54, "°C", "↑ 15%")
    ]),
    ("☀️ Energia Solar", [
        ("Energia Gerada", 390, "MWh", ""),
        ("CO₂ Evitado", 953, "t", ""),
        ("Árvores Equivalentes", 7250, "", "")
    ]),
    ("🐝 Colapso das Abelhas", [
        ("Colmeias Perdidas", 338, "", ""),
        ("Abelhas Perdidas", 20000000, "", ""),
        ("Colmeias RS", 6300, "", "")
    ]),
    ("🐝 Abelhas sem Ferrão", [
        ("Espécies Monitoradas", 18, "", ""),
        ("Registros GBIF", 24500, "", ""),
        ("Estados Cobertos", 15, "", ""),
        ("Espécies Ameaçadas", 4, "VU", "")
    ]),
    ("🌬️ Potencial Eólico", [
        ("Vel. Média", 30.2, "km/h", ""),
        ("Fator Capacidade", 60, "%", ""),
        ("Rajada Máx.", 130, "km/h", ""),
        ("Potencial", 9500, "MW", "")
    ]),
    ("💧 Qualidade da Água", [
        ("IQA Médio", 81.9, "", ""),
        ("Estações Excelente", 3, "/18", ""),
        ("Rios Monitorados", 10, "", "")
    ]),
    ("🌋 Monitoramento Sísmico", [
        ("Magnitude", 7.4, "", ""),
        ("Profundidade", 10, "km", ""),
        ("Evacuados", 1800, "", ""),
        ("Réplicas", 50, "+", "")
    ]),
    ("🌿 Espécies Invasoras", [
        ("Castores", 110000, "+", ""),
        ("Hectares Devastados", 31000, "ha", ""),
        ("Represas", 70600, "", "")
    ]),
    ("🌊 El Niño 2026", [
        ("Probabilidade", 98, "%", ""),
        ("Niño 3.4", 0.9, "°C", ""),
        ("Previsão Pico", 2.4, "°C", ""),
        ("Super El Niño", 33, "%", "")
    ])
]

# Exibir Slide Atual
current = 0  # Por enquanto fixo - o JS fará o reload

theme_name, kpis = themes[current]

st.markdown(f"<h2 style='text-align:center; color:#2ecc71; margin:30px 0;'>{theme_name}</h2>", unsafe_allow_html=True)

cols = st.columns(len(kpis))
for i, (label, value, unit, delta) in enumerate(kpis):
    num_id = f"num_{i}"
    color = "#2ecc71" if "↑" in delta else "#e74c3c"
    
    with cols[i]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number" id="{num_id}">{value}</div>
            <div class="kpi-label">{label} {unit}</div>
            <div class="delta" style="color:{color};">{delta}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Animação de contagem
        if isinstance(value, (int, float)):
            st.markdown(f"""
            <script>
                setTimeout(() => animateCount("{num_id}", 0, {value}, 2000), 400);
            </script>
            """, unsafe_allow_html=True)

st.caption("● Troca automática a cada 15 segundos")
