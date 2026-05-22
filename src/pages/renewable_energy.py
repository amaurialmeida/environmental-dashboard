import streamlit as st
import pandas as pd
import plotly.express as px

def show_energy(t):
    st.header(f"⚡ {t['energy']}")

    df = pd.DataFrame({
        "source": ["Solar", "Wind", "Hydro", "Biomass"],
        "value": [40, 30, 20, 10]
    })

    fig = px.pie(
        df,
        values="value",
        names="source",
        title=t["energy"]
    )

    st.plotly_chart(fig, use_container_width=True)
