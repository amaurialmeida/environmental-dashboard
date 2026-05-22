import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.header("🌫 Air Quality Dashboard")

cities = ["São Paulo", "Rio", "Santiago", "Buenos Aires"]
aqi = np.random.randint(20, 180, len(cities))

df = pd.DataFrame({
    "city": cities,
    "aqi": aqi
})

fig = px.bar(df, x="city", y="aqi", title="Air Quality Index")

st.plotly_chart(fig, use_container_width=True)
