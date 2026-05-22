import streamlit as st
import pandas as pd
import pydeck as pdk

def show_urban(t):
    st.header(f"🏙 {t['urban']}")

    df = pd.DataFrame({
        "lat": [-23.55, -22.90, -15.78],
        "lon": [-46.63, -43.20, -47.92],
        "temperature": [35, 33, 36]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_radius=50000
    )

    view_state = pdk.ViewState(
        latitude=-15,
        longitude=-47,
        zoom=3
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state
        )
    )
