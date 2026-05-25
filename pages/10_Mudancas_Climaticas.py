import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🌡️ Mudanças Climáticas Globais - GREENLOG")

def futuristic_kpi(label, value, delta=None, color="#2ecc71"):
    delta_str = f'<span style="color:#2ecc71;">↑ {abs(delta)}%</span>' if delta else ""
    st.markdown(f"""
    <div style="background:rgba(10,20,33,0.9); border:2px solid {color}; border-radius:12px; padding:18px; text-align:center; margin:5px;">
        <p style="color:#aaa;">{label}</p>
        <h2 style="color:{color};">{value}</h2>
        {delta_str}
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: futuristic_kpi("CO₂ Atual", "428 ppm", 2.3)
with col2: futuristic_kpi("Nível do Mar", "+4.7 mm/ano", 8)
with col3: futuristic_kpi("Gelo Ártico", "-14%", -14)
with col4: futuristic_kpi("Meta 1.5°C", "Em Risco")

st.subheader("🗺️ Vulnerabilidade Climática Global")
vuln_data = pd.DataFrame({"lat": [-23, 35, 55, -10], "lon": [-46, 140, 10, 120], "risco": [78, 65, 82, 91]})
layer = pdk.Layer("ColumnLayer", vuln_data, get_position=["lon", "lat"], get_elevation="risco", elevation_scale=3000, radius=70000, get_fill_color=[255, 100, 100, 160])
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=10, longitude=0, zoom=1.6, pitch=50), layers=[layer]))
