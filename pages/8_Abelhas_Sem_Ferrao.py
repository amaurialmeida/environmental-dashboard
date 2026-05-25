import streamlit as st
import pydeck as pdk
import pandas as pd

st.markdown("# 🐝 Abelhas sem Ferrão - GREENLOG")

def futuristic_kpi(label, value, delta=None, color="#2ecc71"):
    delta_str = f'<span style="color:#2ecc71;">↑ {abs(delta)}%</span>' if delta else ""
    st.markdown(f"""
    <div style="background:rgba(10,20,33,0.9); border:2px solid {color}; border-radius:12px; padding:18px; text-align:center; margin:5px;">
        <p style="color:#aaa;">{label}</p>
        <h2 style="color:{color};">{value}</h2>
        {delta_str}
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: futuristic_kpi("Colônias Ativas", "2.847")
with col2: futuristic_kpi("Espécies Preservadas", "98", 4)

st.subheader("🗺️ Distribuição de Abelhas sem Ferrão")
bee_data = pd.DataFrame({"lat": [-23.5, -15, -5, -25], "lon": [-46.6, -55, -40, -50], "densidade": [85, 65, 92, 45]})
layer = pdk.Layer("ScatterplotLayer", bee_data, get_position=["lon", "lat"], get_color=[255, 215, 0, 180], get_radius=90000)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v11", initial_view_state=pdk.ViewState(latitude=-15, longitude=-50, zoom=3.5), layers=[layer]))
