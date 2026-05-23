import streamlit as st
import plotly.express as px
import polars as pl

# Configuração futurista
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
    "Previsão El Niño"
])

# ---- Funções de cada módulo ----
def temperaturas():
    df = pl.DataFrame({"year":[2018,2019,2020,2021,2022],"temp":[20,22,25,27,30]})
    st.metric("🌡️ Temp Média", f"{df['temp'].mean():.2f} °C")
    fig = px.line(df.to_pandas(), x="year", y="temp", title="Temperatura Global")
    st.plotly_chart(fig, use_container_width=True)

def energia_solar():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"solar":[15,18,22,28,35]})
    st.metric("⚡ Energia Solar", f"{df['solar'].max():.0f} GW")
    fig = px.bar(df.to_pandas(), x="ano", y="solar", title="Crescimento Solar")
    st.plotly_chart(fig, use_container_width=True)

def abelhas():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"colmeias_perdidas":[10,12,15,20,25]})
    st.metric("🐝 Colmeias Perdidas", f"{df['colmeias_perdidas'].sum()} mil")
    fig = px.area(df.to_pandas(), x="ano", y="colmeias_perdidas", title="Colapso das Abelhas")
    st.plotly_chart(fig, use_container_width=True)

def eolico():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"potencia":[30,35,40,50,65]})
    st.metric("💨 Potência Eólica", f"{df['potencia'].max():.0f} GW")
    fig = px.line(df.to_pandas(), x="ano", y="potencia", title="Potencial Eólico")
    st.plotly_chart(fig, use_container_width=True)

def agua():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"iqa":[80,78,75,70,68]})
    st.metric("💧 IQA Médio", f"{df['iqa'].mean():.0f}")
    fig = px.bar(df.to_pandas(), x="ano", y="iqa", title="Qualidade da Água")
    st.plotly_chart(fig, use_container_width=True)

def sismos():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"eventos":[50,60,55,70,80]})
    st.metric("🌍 Eventos Sísmicos", f"{df['eventos'].sum()}")
    fig = px.line(df.to_pandas(), x="ano", y="eventos", title="Monitoramento Sísmico")
    st.plotly_chart(fig, use_container_width=True)

def invasoras():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"area_afetada":[100,120,150,180,200]})
    st.metric("🌱 Área Afetada", f"{df['area_afetada'].max()} km²")
    fig = px.area(df.to_pandas(), x="ano", y="area_afetada", title="Espécies Invasoras")
    st.plotly_chart(fig, use_container_width=True)

def el_nino():
    df = pl.DataFrame({"ano":[2018,2019,2020,2021,2022],"impacto":[0.2,0.3,0.5,0.4,0.6]})
    st.metric("🔥 Impacto Médio", f"{df['impacto'].mean():.2f}")
    fig = px.line(df.to_pandas(), x="ano", y="impacto", title="Previsão El Niño")
    st.plotly_chart(fig, use_container_width=True)

# ---- Roteamento ----
if menu == "Temperaturas globais": temperaturas()
elif menu == "Energia solar": energia_solar()
elif menu == "Colapso das abelhas": abelhas()
elif menu == "Potencial eólico": eolico()
elif menu == "Qualidade da água": agua()
elif menu == "Monitoramento sísmico": sismos()
elif menu == "Espécies invasoras": invasoras()
elif menu == "Previsão El Niño": el_nino()
