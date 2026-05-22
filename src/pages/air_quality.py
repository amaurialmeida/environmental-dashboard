import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_air(t):
    st.header(f"🌫 {t['air']}")

    df = pd.DataFrame({
        "city": ["São Paulo", "Rio", "Santiago", "New York"],
        "aqi": np.random.randint(20, 180, 4)
    })

    fig = px.bar(
        df,
        x="city",
        y="aqi",
        title=t["air"]
    )

    st.plotly_chart(fig, use_container_width=True)
