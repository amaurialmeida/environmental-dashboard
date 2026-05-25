import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ?? Qualidade da Água - EarthMax")

col1, col2, col3 = st.columns(3)
with col1: futuristic_kpi("Rios Monitorados", "12.450", -5)
with col2: futuristic_kpi("Áreas Críticas", "387", 12)
with col3: futuristic_kpi("Índice Médio", "62/100", -8)

st.markdown("### Evolução da Qualidade da Água")
st.plotly_chart(st.empty(), use_container_width=True)  # Placeholder
st.caption("Use Polars + Plotly para gráficos interativos.")
