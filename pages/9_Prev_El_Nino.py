import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ?? Previsão El Niño - EarthMax")

col1, col2, col3 = st.columns(3)
with col1: futuristic_kpi("Probabilidade 2026", "68%", 0)
with col2: futuristic_kpi("Intensidade", "Forte", 0)
with col3: futuristic_kpi("Impacto no Brasil", "Alto", 0)

st.warning("?? Secas no Norte e chuvas intensas no Sul previstas.")
