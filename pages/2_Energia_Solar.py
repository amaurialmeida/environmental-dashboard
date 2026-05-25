import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# ☀️ Energia Solar - GREENLOG")

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
with col1: futuristic_kpi("Capacidade Global", "1.87 TW", 31)
with col2: futuristic_kpi("Irradiação Média", "4.8 kWh/m²", 12)
with col3: futuristic_kpi("Potencial Brasil", "2.500 GW")

st.subheader("🗺️ Potencial Solar Global")
solar_data = pd.DataFrame({"lat": [-15, 30, 40], "lon": [-55, 35, 100], "pot": [2200, 1800, 1600]})
layer = pdk.Layer("HexagonLayer", solar_data, get_position=["lon", "lat"], radius=800000, elevation_scale=500, extruded=True)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=2), layers=[layer]))
