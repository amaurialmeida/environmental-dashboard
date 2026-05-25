import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ??? Mudanças Climáticas Globais - EarthMax")

col1, col2, col3, col4 = st.columns(4)
with col1: futuristic_kpi("CO2 Atual", "428 ppm", 2.1)
with col2: futuristic_kpi("Nível do Mar", "+4.2mm/ano", 0)
with col3: futuristic_kpi("Gelo Ártico", "-13%", -13)
with col4: futuristic_kpi("Meta Paris 1.5°C", "Em Risco", 0)

st.markdown("### Cenários Futuros (SSP2-4.5 vs SSP5-8.5)")
st.plotly_chart(st.empty(), use_container_width=True)
