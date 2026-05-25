import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ?? Monitoramento Sísmico - EarthMax")

col1, col2 = st.columns(2)
with col1: futuristic_kpi("Terremotos Hoje", "23", 0)
with col2: futuristic_kpi("Magnitude Máxima", "7.8", -2)

st.success("Sistema de alerta em tempo real ativo.")
st.info("?? Integre API de dados sísmicos aqui.")
