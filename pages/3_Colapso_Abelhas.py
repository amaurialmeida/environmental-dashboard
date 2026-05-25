import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ?? Colapso das Abelhas - EarthMax")

col1, col2 = st.columns(2)
with col1: futuristic_kpi("População Reduzida", "68%", -68)
with col2: futuristic_kpi("Regiões Críticas", "47", 0)

st.warning("Monitoramento de polinização e impacto na segurança alimentar.")
