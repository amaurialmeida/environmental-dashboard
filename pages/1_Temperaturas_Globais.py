import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd

st.markdown("# 🌍 Temperaturas Globais - GREENLOG")

def futuristic_kpi(label, value, delta=None, color="#2ecc71"):
    delta_str = ""
    if delta is not None:
        arrow = "↑" if delta > 0 else "↓"
        delta_color = "#2ecc71" if delta > 0 else "#e74c3c"
        delta_str = f'<span style="color:{delta_color};">{arrow} {abs(delta)}%</span>'
    st.markdown(f"""
    <div style="background:rgba(10,20,33,0.9); border:2px solid {color}; border-radius:12px; padding:18px; text-align:center; margin:5px;">
        <p style="color:#aaa; margin:0; font-size:0.95rem;">{label}</p>
        <h2 style="color:{color}; margin:8px 0;">{value}</h2>
        {delta_str}
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: futuristic_kpi("Temp. Média Global", "14.92°C", 1.45)
with col2: futuristic_kpi("Ano Mais Quente", "2025", 0.9)
with col3: futuristic_kpi("Anomalia Atual", "+1.54°C", 15)
with col4: futuristic_kpi("Países em Risco", "157", -4)

tab1, tab2, tab3 = st.tabs(["📈 Evolução Histórica", "🗺️ Mapa de Calor Global", "🔮 Previsão"])

with tab1:
    df = pd.DataFrame({"Ano": list(range(1850, 2027)), "Temperatura (°C)": [13.6 + (x-1850)*0.007 + (x>1980)*0.4 for x in range(1850,2027)]})
    fig = px.line(df, x="Ano", y="Temperatura (°C)", template="plotly_dark", color_discrete_sequence=["#2ecc71"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Mapa Interativo de Temperaturas")
    map_data = pd.DataFrame({"lat": [40, -23, 35], "lon": [-74, -46, 139], "temp": [15.2, 22.8, 18.5]})
    layer = pdk.Layer("ColumnLayer", map_data, get_position=["lon", "lat"], get_elevation="temp", elevation_scale=1000, radius=80000, get_fill_color=[255, 140, 0, 140])
    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=1.5, pitch=50), layers=[layer]))

with tab3:
    st.success("**Projeção 2030:** +2.1°C acima da média")
