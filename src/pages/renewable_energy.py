import streamlit as st
import pandas as pd
import plotly.express as px

st.header("⚡ Renewable Energy")

df = pd.DataFrame({
    "source": ["Solar", "Wind", "Hydro", "Biomass"],
    "value": [40, 30, 20, 10]
})

fig = px.pie(
    df,
    values="value",
    names="source",
    title="Renewable Matrix"
)

st.plotly_chart(fig, use_container_width=True)
