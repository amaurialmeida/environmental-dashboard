import streamlit as st

st.set_page_config(
    page_title="Greenlog • Environmental Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS FUTURISTA =====================
st.markdown("""
<style>
    .title {
        font-size: 4.5rem;
        background: linear-gradient(90deg, #2ecc71, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 6px;
        font-weight: bold;
    }
    .subtitle { 
        color: #2ecc71; 
        text-align: center; 
        font-size: 1.6rem; 
        margin-top: -20px;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ===================== IDIOMA (Topo) =====================
col1, col2 = st.columns([8, 2])
with col2:
    idioma = st.selectbox(
        "🌐 Idioma", 
        ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"],
        key="idioma_selector"
    )

st.session_state.lang = idioma.split()[-1].lower()[:2]

# ===================== HEADER =====================
st.markdown('<h1 class="title">GREENLOG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#a0e0c0;">Monitoramento Global em Tempo Real • IA + Geoespacial</p>', unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Use o menu lateral para navegar entre os dashboards")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555;'>🌱 Greenlog Portfolio • Amauri Almeida</p>",
    unsafe_allow_html=True
)
