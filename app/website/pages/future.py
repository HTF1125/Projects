"""ROBERT"""
import streamlit as st
import pandas as pd
import plotly.express as px
from website.pages.base import BasePage
from database.client import get_yields

class Future(BasePage):
    def load_page(self):
        # ccy = "USD"
        # pxs = get_prices(f"{ccy}KRW, SPY, AGG").dropna()
        # perfs = []
        # for hedge_ratio in range(11):
        #     weights = pd.Series(
        #         {"SPY": 0.0, "AGG": 1., f"{ccy}KRW": 1-hedge_ratio / 10}
        #     )
        #     pri_return = pxs.pct_change().fillna(0)
        #     perf = pri_return.dot(weights)
        #     perfs.append(perf.add(1).cumprod())
        # perfs = pd.concat(perfs, axis=1)

        # self.plotly(px.line(perfs))

        # self.plotly(px.line(perfs.pct_change().rolling(252).std()))


        # st.line_chart(get_prices("DGS3MO, DGS1, DSG2, DGS3, DGS5, DGS10, DGS20, DGS30").loc["2020":])


        st.line_chart(get_yields().loc["2020":])