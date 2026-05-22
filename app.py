import streamlit as st
from streamlit_option_menu import option_menu

from src.translations import TRANSLATIONS

from src.pages.climate import show_climate
from src.pages.air_quality import show_air
from src.pages.deforestation import show_forest
from src.pages.renewable_energy import show_energy
from src.pages.urban_heat import show_urban

st.set_page_config(
    page_title="Environmental Intelligence Platform",
    page_icon="🌎",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state.lang = "en"

col1, col2, col3, col4 = st.columns([8,1,1,1])

with col2:
    if st.button("🇧🇷"):
        st.session_state.lang = "pt"

with col3:
    if st.button("🇺🇸"):
        st.session_state.lang = "en"

with col4:
    if st.button("🇪🇸"):
        st.session_state.lang = "es"

t = TRANSLATIONS[st.session_state.lang]

st.title(f"🌎 {t['title']}")
st.caption(t["subtitle"])

with st.sidebar:
    selected = option_menu(
        menu_title=t["select_dashboard"],
        options=[
            t["climate"],
            t["air"],
            t["forest"],
            t["energy"],
            t["urban"]
        ],
        icons=[
            "globe",
            "wind",
            "tree",
            "lightning",
            "geo-alt"
        ],
        default_index=0
    )

if selected == t["climate"]:
    show_climate(t)

elif selected == t["air"]:
    show_air(t)

elif selected == t["forest"]:
    show_forest(t)

elif selected == t["energy"]:
    show_energy(t)

elif selected == t["urban"]:
    show_urban(t)
