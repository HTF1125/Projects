"""ROBERT"""
from typing import Optional
from typing import Tuple
import pandas as pd
import streamlit as st


def get_date_range(
    start: str = "2015-01-01", end: Optional[str] = None
) -> Tuple[str, str]:
    start_col, end_col = st.columns(2)
    with start_col:
        start = str(
            st.date_input(
                label="Start",
                value=pd.Timestamp(start),
                # max_value=pd.Timestamp("now"),
            )
        )
    with end_col:
        if end is not None:
            end = str(
                st.date_input(
                    label="End",
                    value=pd.Timestamp(end),
                )
            )
        else:
            end = str(
                st.date_input(
                    label="End",
                    value=max(pd.Timestamp("now"), pd.Timestamp(start)),
                )
            )

        return start, end
