"""Compatibilidade: st.iframe (Streamlit recente) com fallback para st.components.v1 (versões antigas)."""
import streamlit as st


def embed_html(html, height):
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=height, scrolling=False)


def embed_url(url, height):
    if hasattr(st, "iframe"):
        st.iframe(url, height=height)
    else:
        import streamlit.components.v1 as components
        components.iframe(url, height=height, scrolling=True)
