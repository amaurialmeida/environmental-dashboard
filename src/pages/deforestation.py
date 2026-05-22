import streamlit as st
import pandas as pd
import plotly.express as px

def show_forest(t):
    st.header(f"🌳 {t['forest']}")

    df = pd.DataFrame({
        "year": [2019, 2020, 2021, 2022, 2023],
        "forest_loss": [8000, 9500, 10200, 12000, 9700]
    })

    fig = px.area(
        df,
        x="year",
        y="forest_loss",
        title=t["forest"]
    )

    st.plotly_chart(fig, use_container_width=True)
