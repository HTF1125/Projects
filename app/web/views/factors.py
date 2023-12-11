import logging
from dash import html, dcc, callback, Output, Input, State, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from .. import components

from app.api import factors

import feffery_antd_components as fac
import feffery_utils_components as fuc

from app.api.universes.base import Universe
from app import db
from .base import Page


def get_universe():
    data = list(db.get_universe().index.unique())
    return dmc.Select(
        label="Investment Universe",
        data=data,
        id="user-universe",
        value=data[0],
        persistence=True,
    )


def get_factor():
    data = list(factors.__all__)
    return dmc.Select(
        label="Investment Factor",
        data=data,
        id="user-factor",
        value=data[0],
        persistence=True,
    )


def get_periods():
    return dmc.NumberInput(
        label="Investment Horizon (Day)",
        id="user-periods",
        value=1,
        min=0,
        max=250,
        step=5,
        persistence=True,
    )


def get_commission():
    return dmc.NumberInput(
        label="Trade Commission (bps)",
        id="user-commission",
        value=10,
        min=0,
        max=100,
        step=2,
        persistence=True,
    )


def get_factor_args():
    style = {
        "margin-top": 0,
        "margin-bottom": 10,
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
    }

    return dmc.Group(
        style=style,
        children=[
            get_universe(),
            get_factor(),
        ],
    )


class Factors(Page):
    menu = {
        "component": "Item",
        "props": {
            "key": "/Factors",
            "name": "/Factors",
            "title": "Factors",
            "href": "/Factors",
            "icon": "antd-dot-chart",
        },
    }

    def layout(self):
        return html.Div(
            children=[
                dcc.Store(id="cache", data={}),
                html.H1("Factor Analysis"),
                html.Div(
                    children=[
                        fac.AntdRow(
                            children=[
                                self.get_universe(),
                                self.get_factor(),
                            ],
                            style={
                                "margin-top": 0,
                                "margin-bottom": 10,
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                        html.Div(
                            fac.AntdButton("Test Factors", id="user-factor-test"),
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        components.Info(
                            dcc.Markdown(
                                children="""
**Universe:**
The Universe module is specifically curated with major ETFs, simplifying your focus on essential assets.

- **GlobalAllo:**
  - SPY, AGG, TLT, TIP, GSG, GLD, TIP, IVV

- **UsSectors:**
  - XLC, XLY, XLK, and YOU KNOW WHATS NEXT.

**Factors:**
Given the constraints of data availability, our Factors predominantly encompass momentum, ensuring an intuitive and actionable analysis.

**Running the Module:**
Upon hitting 'run', the generated graph provides insights into the average expected forward performance on a daily basis. This projection extends over three distinct investment horizons: 1, 5, and 10 trading days.

**Additional Information:**
The notation `(q=5, za=0)` signifies the use of quantiles (in this case, 5) and a non-zero-aware approach when processing factor data.

                                """
                            )
                        ),
                        dcc.Loading(
                            children=html.Div(
                                id="factor-chart",
                                style={
                                    "min-height": 500,
                                    "min-width": 1000,
                                },
                            ),
                            type="circle",
                        ),
                    ],
                    style={
                        "margin-bottom": 20,
                    },
                ),
                html.Div(id="factor-performance-table"),
                html.Div(id="factor-performance-stats"),
            ]
        )


# @callback(
#     Output("cache", "chart"),
#     Input("factor-performance-chart", "figure"),
#     State("user-universe", "value"),
#     State("user-periods", "value"),
#     State("cache", "chart"),
# )
# def cache_plt(chart, universe, periods, cache):
#     if not cache:
#         return {universe: {periods: chart}}
#     if universe not in cache:
#         cache[universe] = {}
#     if periods not in cache[universe]:
#         cache[universe] = {periods: chart}
#     return cache


# @lru_cache()
# def factor_test(universe: str, periods: int = 21, commission=10):
#     multi_factors = MultiFactors(Universe.from_code(code=universe))
#     performances = multi_factors.to_performance(
#         periods=periods, commission=commission
#     ).ffill()
#     return performances


# @callback(
#     Output("factor-performance-chart", "figure"),
#     Input("user-universe", "value"),
#     State("global-cache", "data"),
#     prevent_initial_call=True,
# )
# def handle_chart(universe, cache):
#     import json
#     from app.api import Universe

#     if cache is not None:
#         print("cache found start update")
#         print(cache[:500])
#         cache = json.loads(cache)
#         Universe.from_store(cache.get("factor-test"))
#         uni = Universe.from_code(code=universe)
#         fig = uni.multi_factors.plot_performances()
#         return fig
#     print("no cache found, return no update.")
#     return no_update


@callback(
    Output("factor-chart", "children"),
    Input("user-factor-test", "nClicks"),
    State("user-universe", "value"),
    State("user-factor", "value"),
    prevent_initial_call=True,
)
def handle_chart(nClicks, universe, factor):
    if nClicks:
        factor_ins = getattr(factors, factor)
        if issubclass(factor_ins, factors.Factor):
            return [
                fac.AntdCenter(html.H3(f"{factor} Performance")),
                fac.AntdCenter(
                    dcc.Graph(
                        figure=factor_ins.create(universe).plot(),
                        config={"displayModeBar": False},
                    ),
                ),
            ]
    return no_update
