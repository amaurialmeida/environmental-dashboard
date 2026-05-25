import streamlit as st
from utils.components import futuristic_kpi

st.markdown("# ?? Espécies Invasoras - EarthMax")

col1, col2, col3 = st.columns(3)
with col1: futuristic_kpi("Espécies Monitoradas", "184", 9)
with col2: futuristic_kpi("Impacto Econômico", "US$ 1.2T", 0)
with col3: futuristic_kpi("Regiões Afetadas", "63", 14)

futuristic_card("Alerta", "A espécie X está se expandindo rapidamente no Brasil.")
