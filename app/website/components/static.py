"""ROBERT"""
import streamlit as st
from app.website import static


def loadStatic() -> None:
    st.set_page_config(
        page_title="HKLIFE",
        page_icon=":snowflake:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None,
    )
    filenames = static.all_filenames()
    for filename in filenames:
        if filename.endswith(".html"):
            with open(file=filename, encoding="utf-8") as f:
                content = f.read()
                st.markdown(body=content, unsafe_allow_html=True)
        elif filename.endswith(".css"):
            with open(file=filename, encoding="utf-8") as f:
                content = f.read()
            st.markdown(body=f"<style>{content}</style>", unsafe_allow_html=True)
