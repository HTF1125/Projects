"""ROBERT"""
import streamlit as st
import plotly.graph_objects as go
from app.website.pages.base import BasePage
from app.core import factors, universes


class AlphaFactors(BasePage):
    @staticmethod
    def getPeriods() -> int:
        return int(
            st.slider(
                label="Periods",
                min_value=1,
                max_value=252,
                value=21,
                step=1,
            )
        )

    @staticmethod
    def getCommission() -> int:
        return int(
            st.slider(
                label="Commission",
                min_value=0,
                max_value=100,
                value=10,
                step=5,
            )
        )

    @staticmethod
    def getFactor() -> str:
        return str(st.selectbox(label="Factor", options=factors.__all__))

    @staticmethod
    def getUniverse() -> str:
        return str(st.selectbox(label="Universe", options=universes.__all__))

    def load_page(self):
        with st.form("alphafactors.form"):
            cols = st.columns(2)
            with cols[0]:
                universe = getattr(universes, self.getUniverse())()
                periods = self.getPeriods()
            with cols[1]:
                factor = getattr(factors, self.getFactor())()
                commission = self.getCommission()

            submit = st.form_submit_button("Backtest")
            if submit:

                factor_data = factor.fit(universe=universe).data


                perf = universe.backtest(
                    factor = factor.fit(universe=universe).data,
                    periods=periods,
                    commission=commission
                )
                fig = go.Figure()
                fig.add_trace(
                    trace=go.Scatter(
                        x=perf.index,
                        y=perf.values,
                        name=perf.name,
                        mode="lines",
                    )
                )
                fig.update_yaxes(tickformat=".2%")

                self.plotly(fig, height=400)
