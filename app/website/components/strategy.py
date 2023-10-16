"""ROBERT"""
from typing import Dict
from datetime import date
import streamlit as st


def frequency() -> str:
    return str(
        st.selectbox(
            label="Frequency",
            options=["D", "W", "M", "Q", "Y"],
            index=2,
        )
    )


def inception() -> str:
    return str(
        st.date_input(
            label="Inception",
            value=date.fromisoformat("2015-01-01"),
            max_value=date.today(),
        )
    )


def principal() -> float:
    return float(
        st.number_input(
            label="Principal",
            min_value=1_000,
            max_value=1_000_000_000,
            value=100_000,
            step=1_000,
        )
    )


def commission() -> int:
    return int(
        st.number_input(
            label="Commission",
            min_value=0,
            max_value=100,
            value=10,
            step=5,
        )
    )


def allow_franctional_shares() -> bool:
    return st.checkbox(
        label="Allow fractional shares",
        value=False,
    )


def min_periods() -> int:
    return int(
        st.number_input(
            label="Min Periods",
            min_value=2,
            max_value=252 * 3,
            value=252,
        )
    )


def kwargs() -> Dict:
    kws = [frequency, inception, principal, commission, min_periods]
    out = {}

    cols = st.columns(len(kws))
    for col, kw in zip(cols, kws):
        with col:
            out[kw.__name__] = kw()
    return out
