import streamlit as st
import plotly.express as px
import polars as pl
import pydeck as pdk
import duckdb

st.set_page_config(page_title="Environmental Dashboard V2", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Idiomas
langs = {"Português":"Dashboard Ambiental","English":"Environmental Dashboard","Español":"Panel Ambiental"}
lang_choice = st.sidebar.radio("🌐 Language", list(langs.keys()))
st.title(langs[lang_choice])

# Sidebar modular
menu = st.sidebar.selectbox("📊 Projetos", [
    "Temperaturas globais",
    "Energia solar",
    "Colapso das abelhas",
    "Potencial eólico",
    "Qualidade da água",
    "Monitoramento sísmico",
    "Espécies invasoras",
    "Abelhas sem ferrão",
    "Previsão El Niño",
    "Mudanças climáticas globais"
])

# ---- Função genérica para criar tabs ----
def create_tabs(df, x, y, titulo, mapa=False):
    tab1, tab2, tab3 = st.tabs(["📊 Gráfico", "🗺️ Mapa", "📑 Tabela"])
    with tab1:
        fig = px.line(df.to_pandas(), x=x, y=y, title=titulo)
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        if mapa:
            map_data = df.to_pandas()
            map_data["lat"] = [-23.55, -22.90, -21.17, -19.92, -15.78]
            map_data["lon"] = [-46.63, -43.20, -47.82, -43.94, -47.93]
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
        else:
            st.info("Mapa não disponível para este módulo.")
    with tab3:
        st.dataframe(df.to_pandas())

# ---- Módulos ----
def temperaturas():
    df = pl.DataFrame({"year":[2018,2019,2020,2021,2022],"temp":[20,22,25,27,30]})
    st.metric("🌡️ Temp Média", f"{df['temp'].mean():.2f} °C")
    create_tabs(df, "year", "temp", "Temperatura Global", mapa=True)

def energia_solar():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"solar":[15,18,22,28,35]})
    st.metric("⚡ Energia Solar", f"{df['solar'].max():.0f} GW")
    create_tabs(df, "ano", "solar", "Energia Solar", mapa=True)

def abelhas():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"colmeias_perdidas":[10,12,15,20,25]})
    st.metric("🐝 Colmeias Perdidas", f"{df['colmeias_perdidas'].sum()} mil")
    create_tabs(df, "ano", "colmeias_perdidas", "Colapso das Abelhas", mapa=True)

def eolico():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"potencia":[30,35,40,50,65]})
    st.metric("💨 Potência Eólica", f"{df['potencia'].max():.0f} GW")
    create_tabs(df, "ano", "potencia", "Potencial Eólico", mapa=True)

def agua():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"iqa":[80,78,75,70,68]})
    st.metric("💧 IQA Médio", f"{df['iqa'].mean():.0f}")
    create_tabs(df, "ano", "iqa", "Qualidade da Água", mapa=True)

def sismos():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"eventos":[50,60,55,70,80]})
    st.metric("🌍 Eventos Sísmicos", f"{df['eventos'].sum()}")
    create_tabs(df, "ano", "eventos", "Monitoramento Sísmico", mapa=True)

def invasoras():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"area_afetada":[100,120,150,180,200]})
    st.metric("🌱 Área Afetada", f"{df['area_afetada'].max()} km²")
    create_tabs(df, "ano", "area_afetada", "Espécies Invasoras", mapa=True)

def abelhas_sem_ferrao():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"populacao":[200,220,250,270,300]})
    st.metric("🐝 Abelhas sem Ferrão", f"{df['populacao'].mean():.0f}")
    create_tabs(df, "ano", "populacao", "Abelhas sem Ferrão", mapa=True)

def el_nino():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"impacto":[0.2,0.3,0.5,0.4,0.6]})
    st.metric("🔥 Impacto Médio", f"{df['impacto'].mean():.2f}")
    create_tabs(df, "ano", "impacto", "Previsão El Niño", mapa=True)

def mudancas_climaticas():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"co2":[2.1,2.3,2.5,2.7,2.9]})
    st.metric("🌍 CO₂ Médio", f"{df['co2'].mean():.2f} t")
    create_tabs(df, "ano", "co2", "Mudanças Climáticas Globais", mapa=True)

# ---- Roteamento ----
if menu == "Temperaturas globais": temperaturas()
elif menu == "Energia solar": energia_solar()
elif menu == "Colapso das abelhas": abelhas()
elif menu == "Potencial eólico": eolico()
elif menu == "Qualidade da água": agua()
elif menu == "Monitoramento sísmico": sismos()
elif menu == "Espécies invasoras": invasoras()
elif menu == "Abelhas sem ferrão": abelhas_sem_ferrao()
elif menu == "Previsão El Niño": el_nino()
elif menu == "Mudanças climáticas globais": mudancas_climaticas()
