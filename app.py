import streamlit as st
import polars as pl
import duckdb
import plotly.express as px
import pydeck as pdk
from sklearn.linear_model import LinearRegression
import pandas as pd

# ---- Configuração de página ----
st.set_page_config(
    page_title="Environmental Dashboard V2",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Carregar CSS futurista ----
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- Idiomas ----
langs = {
    "Português": {"title": "Dashboard Ambiental", "kpi": "Indicadores"},
    "English": {"title": "Environmental Dashboard", "kpi": "KPIs"},
    "Español": {"title": "Panel Ambiental", "kpi": "Indicadores"}
}
lang_choice = st.sidebar.radio("🌐 Language", list(langs.keys()))
texts = langs[lang_choice]

st.title(texts["title"])

# ---- Upload CSV ----
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV", type=["csv"])
if uploaded_file:
    df = pl.read_csv(uploaded_file)
else:
    df = pl.DataFrame({"temp":[20,22,25,27,30], "year":[2018,2019,2020,2021,2022]})

# ---- KPIs ----
col1, col2, col3 = st.columns(3)
col1.metric(texts["kpi"], f"{df['temp'].mean():.2f} °C")
col2.metric("Max Temp", f"{df['temp'].max():.2f} °C")
col3.metric("Min Temp", f"{df['temp'].min():.2f} °C")

# ---- Gráfico interativo ----
fig = px.line(df.to_pandas(), x="year", y="temp", title="Temperature Trend")
st.plotly_chart(fig, use_container_width=True)

# ---- Mapa futurista ----
map_data = pd.DataFrame({
    'lat': [-23.55, -22.90, -21.17],
    'lon': [-46.63, -43.20, -47.82],
    'temp': [25, 28, 22]
})
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=pdk.ViewState(latitude=-23.55, longitude=-46.63, zoom=4),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=50000,
        ),
    ],
))
