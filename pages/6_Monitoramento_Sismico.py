import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🌋 Monitoramento Sísmico - GREENLOG")

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
with col1: futuristic_kpi("Eventos Hoje", "47")
with col2: futuristic_kpi("Maior Magnitude", "7.4")
with col3: futuristic_kpi("Risco Alto", "12 Regiões")

st.subheader("🗺️ Atividade Sísmica Global")
quake_data = pd.DataFrame({"lat": [-15, 35, -8, 40], "lon": [-70, 140, 120, -120], "mag": [6.8, 5.9, 7.1, 6.2]})
layer = pdk.Layer("ScatterplotLayer", quake_data, get_position=["lon", "lat"], get_radius=150000, get_color=[255, 80, 80, 200])
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=10, longitude=0, zoom=1.5, pitch=50), layers=[layer]))
