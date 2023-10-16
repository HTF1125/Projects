"""ROBERT"""
import streamlit as st
import plotly.graph_objects as go
from app.core import universes, factors


class BaseState:
    item = None

    @classmethod
    def get(cls) -> ...:
        if cls.__name__ not in st.session_state:
            cls.reset()
        return st.session_state[cls.__name__]

    @classmethod
    def reset(cls) -> None:
        st.session_state[cls.__name__] = cls.item

    @classmethod
    def set(cls, item: ..., rerun: bool = True):
        if cls.get() != item:
            st.session_state[cls.__name__] = item
            if rerun:
                st.rerun()


class Universe(BaseState):
    item = "UsSectors"

    @classmethod
    def select(cls) -> str:
        return str(
            st.selectbox(
                label=cls.__name__,
                options=universes.__all__,
                index=universes.__all__.index(cls.get()),
            )
        )


class Factor(BaseState):
    item = "PxMom1M"

    @classmethod
    def select(cls) -> str:
        return str(
            st.selectbox(
                label=cls.__name__,
                options=factors.__all__,
                index=factors.__all__.index(cls.get()),
            )
        )


class Webpage(BaseState):
    item = "Dashboard"


class FactorPlot(BaseState):
    item = go.Figure()
