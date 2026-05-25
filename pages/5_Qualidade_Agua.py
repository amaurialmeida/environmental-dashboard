import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 💧 Qualidade da Água - GREENLOG")

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
with col1: futuristic_kpi("Rios Monitorados", "18.450")
with col2: futuristic_kpi("Índice Global", "64/100", -7)
with col3: futuristic_kpi("Áreas Críticas", "428", 19)

st.subheader("🗺️ Mapa de Qualidade da Água")
water_data = pd.DataFrame({"lat": [-22, 30, 55], "lon": [-43, 30, 10], "qual": [45, 82, 78]})
layer = pdk.Layer("ScatterplotLayer", water_data, get_position=["lon", "lat"], get_color=[0, 255, 100, 160], get_radius=120000)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=1.6), layers=[layer]))
