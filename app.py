import streamlit as st
import os

st.set_page_config(page_title="EarthMax • Environmental Intelligence", 
                   page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

# ===================== CUSTOM CSS - NEON FUTURISTA =====================
st.markdown("""
<style>
    .main { background-color: #050505; }
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #0a1421 100%);
    }
    .title {
        font-size: 4rem;
        background: linear-gradient(90deg, #2ecc71, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(46, 204, 113, 0.5);
        letter-spacing: 6px;
    }
    .neon-card {
        background: rgba(10, 20, 33, 0.85);
        border: 2px solid #2ecc71;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 25px rgba(46, 204, 113, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Language Selector
col1, col2 = st.columns([8, 2])
with col2:
    lang = st.selectbox("🌐 Idioma", ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"])

st.session_state.lang = lang.split()[-1].lower()[:2]

# Header
st.markdown('<h1 class="title" style="text-align:center;">EARTHMAX</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; color:#2ecc71; margin-top:-15px;">ENVIRONMENTAL INTELLIGENCE 2030</h3>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#a0e0c0;">Monitoramento Global em Tempo Real • IA + Geoespacial</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2ecc71/050505?text=EARTHMAX+2030", use_column_width=True)
    st.markdown("### **NAVEGAÇÃO PRINCIPAL**")
    
    menu = st.radio("**Selecione o Tema**", [
        "🌍 Temperaturas Globais",
        "☀️ Energia Solar",
        "🐝 Colapso das Abelhas",
        "🌬️ Potencial Eólico",
        "💧 Qualidade da Água",
        "🌋 Monitoramento Sísmico",
        "🌿 Espécies Invasoras",
        "🐝 Abelhas sem Ferrão",
        "🌊 Previsão El Niño",
        "🌡️ Mudanças Climáticas"
    ])

# Navigation Logic
page_files = {
    "🌍 Temperaturas Globais": "pages/1_Temperaturas_Globais.py",
    "☀️ Energia Solar": "pages/2_Energia_Solar.py",
    # ... (adicione os demais)
}

if os.path.exists(page_files.get(menu, "")):
    with open(page_files.get(menu, ""), encoding="utf-8") as f:
        exec(f.read())
else:
    st.warning("🚧 Dashboard em construção...")
