import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🌊 Previsão El Niño - GREENLOG")

def futuristic_kpi(label, value, delta=None, color="#2ecc71"):
    delta_str = f'<span style="color:#2ecc71;">↑ {abs(delta)}%</span>' if delta else ""
    st.markdown(f"""
    <div style="background:rgba(10,20,33,0.9); border:2px solid {color}; border-radius:12px; padding:18px; text-align:center; margin:5px;">
        <p style="color:#aaa;">{label}</p>
        <h2 style="color:{color};">{value}</h2>
        {delta_str}
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1: futuristic_kpi("Intensidade Prevista", "Forte")
with col2: futuristic_kpi("Probabilidade 2026", "72%", 5)
with col3: futuristic_kpi("Impacto no Brasil", "Alto")

st.subheader("🗺️ Impacto Esperado do El Niño")
impact_data = pd.DataFrame({"lat": [-10, -25, 5, -30], "lon": [-55, -45, -75, -60], "impacto": [85, 65, 90, 75]})
layer = pdk.Layer("HeatmapLayer", impact_data, get_position=["lon", "lat"], opacity=0.7)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=-15, longitude=-55, zoom=3.8), layers=[layer]))
