"""ROBERT"""
from typing import Optional
import streamlit as st
from core import universes

# from website.pages.dashboard import Dashboard
# from website.pages.factors import AlphaFactors


class BaseHook:
    item = None

    @classmethod
    def get(cls) -> ...:
        if cls.__name__ not in st.session_state:
            st.session_state[cls.__name__] = cls.item
        return st.session_state[cls.__name__]

    @classmethod
    def set(cls, item: ..., rerun: bool = True):
        if cls.get() != item:
            st.session_state[cls.__name__] = item
            if rerun:
                st.rerun()


class Universe(BaseHook):
    item = universes.UsSectors

    @classmethod
    def update(cls) -> None:

        options = [cls.item, ]
        st.write(cls.get())
        st.write(cls.item)
        option = st.selectbox(
            label=cls.__name__,
            options=options,
            index=options.index(cls.get()),
        )
        if option is not None:
            cls.set(item=option)
            st.rerun()


class Page(BaseHook):
    item = "Dashboard"
