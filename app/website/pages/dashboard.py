"""ROBERT"""
import streamlit as st
import plotly.graph_objects as go
from app.website.pages.base import BasePage
from app.website.components.common import get_date_range
from app.database.client import get_sp500, get_dollar_index, get_yields

class Dashboard(BasePage):
    def load_page(self):


        start, end = get_date_range()
        spy = get_sp500()
        spy_yoy_10yr_ma = (
            spy.pct_change(252)
            .rolling(252 * 10)
            .mean()
            .dropna(how="all")
            .loc[start:end]
        )

        col1, col2 = st.columns(2)
        with col1:
            self.plotly(
                fig=(
                    go.Figure()
                    .add_trace(
                        go.Scatter(x=spy_yoy_10yr_ma.index, y=spy_yoy_10yr_ma.values)
                    )
                    .update_layout(
                        hovermode="x unified",
                        title="S&P500 YoY 10Yr Moving Average",
                        xaxis_tickformat="%Y-%m-%d",
                        yaxis_tickformat=".2%",
                    )
                ),
            )
        with col2:
            dollar = get_dollar_index()
            dollar_yoy = dollar.pct_change(252).dropna().loc[start:end]

            self.plotly(
                go.Figure()
                .add_trace(go.Scatter(x=dollar_yoy.index, y=dollar_yoy.values))
                .update_layout(
                    hovermode="x unified",
                    title="US Dollar Index YoY%",
                    xaxis_tickformat="%Y-%m-%d",
                    yaxis_tickformat=".2%",
                )
            )

        data = (
            get_yields()
            .dropna()[["3M", "1Y", "2Y", "3Y", "5Y", "10Y", "20Y", "30Y"]]
            .loc[start:end]
            .T
        )
        self.plotly(
            fig=go.Figure(
                data=go.Heatmap(
                    z=data.values,
                    x=data.columns,
                    y=data.index,
                    colorscale='Viridis',
                )
            )
        )

