"""ROBERT"""
import streamlit as st
from streamlit_option_menu import option_menu
from app.website import pages, state


def loadNavbar() -> None:
    with st.sidebar:
        st.markdown(
            "<h1 style='width: 100%; text-align: center;'>  ROBERT-DASHBOARD  </h1>",
            unsafe_allow_html=True,
        )
        page = option_menu(
            menu_title=None,
            options=pages.__all__,
            default_index=int(pages.__all__.index(state.Webpage.get())),
            orientation="vertical",
            styles={
                "container": {"padding": "10!important", "max-width": "100%"},
                "icon": {"font-size": "16px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "5px",
                },
            },
        )
        state.Webpage.set(item=page, rerun=True)
        st.markdown(body="Version: 0.0.1")
