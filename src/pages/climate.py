import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import polars as pl

def show_climate(t):
    st.header(f"🌡 {t['climate']}")

    years = np.arange(2000, 2025)

    df = pd.DataFrame({
        "year": years,
        "temperature": np.random.normal(24, 2, len(years))
    })

    fig = px.line(
        df,
        x="year",
        y="temperature",
        title=t["climate"]
    )

    st.plotly_chart(fig, use_container_width=True)

    uploaded = st.file_uploader(
        t["upload"],
        type=["csv"]
    )

    if uploaded:
        data = pl.read_csv(uploaded)
        st.dataframe(data.head().to_pandas())
