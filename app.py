import streamlit as st

st.set_page_config(
    page_title="Environmental Intelligence Platform",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 Environmental Intelligence Platform")
st.markdown("Modern Big Data + AI Dashboard")

pages = [
    "Climate Analytics",
    "Air Quality",
    "Deforestation",
    "Renewable Energy",
    "Urban Heat"
]

selected = st.sidebar.radio("Select Dashboard", pages)

if selected == "Climate Analytics":
    exec(open("src/pages/climate.py").read())

elif selected == "Air Quality":
    exec(open("src/pages/air_quality.py").read())

elif selected == "Deforestation":
    exec(open("src/pages/deforestation.py").read())

elif selected == "Renewable Energy":
    exec(open("src/pages/renewable_energy.py").read())

elif selected == "Urban Heat":
    exec(open("src/pages/urban_heat.py").read())
