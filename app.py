import streamlit as st

st.set_page_config(
    page_title="EarthMax • Environmental Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Futurista
st.markdown("""
<style>
    .title {
        font-size: 4.2rem;
        background: linear-gradient(90deg, #2ecc71, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 6px;
    }
    .subtitle { color: #2ecc71; text-align: center; font-size: 1.6rem; margin-top: -20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">EARTHMAX</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#a0e0c0;">Monitoramento Global em Tempo Real • IA + Geoespacial</p>', unsafe_allow_html=True)

st.markdown("---")

st.info("👈 Use o menu lateral para navegar entre os dashboards")
