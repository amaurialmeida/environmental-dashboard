import streamlit as st
import pandas as pd
import plotly.express as px

st.header("🌳 Deforestation Monitoring")

df = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023],
    "area_lost": [8000, 9500, 10200, 12000, 9700]
})

fig = px.area(
    df,
    x="year",
    y="area_lost",
    title="Forest Loss"
)

st.plotly_chart(fig, use_container_width=True)
