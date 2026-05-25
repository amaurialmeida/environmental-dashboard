import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🌿 Espécies Invasoras - GREENLOG")

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
with col1: futuristic_kpi("Espécies Monitoradas", "217", 12)
with col2: futuristic_kpi("Áreas Invadidas", "1.840", 8)
with col3: futuristic_kpi("Impacto Econômico", "US$ 1.2T")

st.subheader("🗺️ Distribuição de Espécies Invasoras")
invasive_data = pd.DataFrame({"lat": [-23, 40, 20, -35], "lon": [-46, 120, 80, 150], "risco": [85, 65, 92, 78]})
layer = pdk.Layer("HeatmapLayer", invasive_data, get_position=["lon", "lat"], opacity=0.8)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=1.7), layers=[layer]))
