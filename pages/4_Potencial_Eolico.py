import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🌬️ Potencial Eólico - GREENLOG")

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
with col1: futuristic_kpi("Potencial Global", "120 TW", 18)
with col2: futuristic_kpi("Capacidade Instalada", "1.05 TW", 25)
with col3: futuristic_kpi("Brasil", "143 GW")

st.subheader("🗺️ Mapa de Potencial Eólico")
wind_data = pd.DataFrame({"lat": [-23.5, 40, 55], "lon": [-46.6, -100, 10], "vel": [8.5, 9.2, 11.8]})
layer = pdk.Layer("ColumnLayer", wind_data, get_position=["lon", "lat"], get_elevation="vel", elevation_scale=80000, radius=60000, get_fill_color=[100, 200, 255, 180])
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=-5, longitude=0, zoom=1.8, pitch=55), layers=[layer]))
