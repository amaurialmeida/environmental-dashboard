import streamlit as st
import polars as pl
import plotly.express as px
import pandas as pd
import numpy as np

st.header("🌡 Climate Analytics")

years = np.arange(2000, 2025)
temperatures = np.random.normal(24, 2, len(years))

df = pd.DataFrame({
    "year": years,
    "temperature": temperatures
})

fig = px.line(
    df,
    x="year",
    y="temperature",
    title="Average Global Temperature"
)

st.plotly_chart(fig, use_container_width=True)

uploaded = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

if uploaded:
    data = pl.read_csv(uploaded)
    st.dataframe(data.head().to_pandas())
