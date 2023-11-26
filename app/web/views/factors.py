import logging
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import pandas as pd
import plotly.graph_objects as go


from app.api import factor


from app import api
def get_universe():
    data = list(api.universe.Universe.UNIVERSE.keys())
    return dmc.Select(
        label="Investment Universe",
        data=data,
        id="user-universe",
        value=data[0],
        persistence=True,
    )
def get_factor():
    data = list(factor.__all__)
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
            get_periods(),
            get_factor(),
        ],
    )


class Factors:
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
                        get_factor_args(),
                        html.Div(
                            dmc.Button(
                                "Run",
                                id="user-factor-test",
                                leftIcon=DashIconify(
                                    icon="fluent:database-plug-connected-20-filled"
                                ),
                                style={
                                    "marginTop": 0,
                                    "marginBottom": 10,
                                    "text-align": "right",
                                },
                            ),
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
                        ),
                        dmc.LoadingOverlay(
                            children=[
                                html.H3(
                                    id="factor-chart-title",
                                    style={"text-align": "center"},
                                ),
                                dcc.Graph(
                                    figure=blank_fig(),
                                    id="factor-performance-chart",
                                    config={"displayModeBar": False},
                                ),
                            ],
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




@callback(
    Output("factor-performance-chart", "figure"),
    Output("factor-chart-title", "children"),
    Input("user-factor-test", "n_clicks"),
    State("user-universe", "value"),
    State("user-periods", "value"),
    State("user-factor", "value"),
    prevent_initial_call=True,
)
def compute_factor_data(
    n_clicks: int,
    universe: str,
    periods: int,
    factor: str,
):
    uni = api.get_universe(code=universe)
    uni.f.append(factor, periods=periods)
    fig = uni.f.plot()
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",  # Set plot background color as transparent
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color as transparent
        legend={
            "orientation": "h",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.05,
            "yanchor": "top",
            "itemsizing": "constant",
        },
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
    )
    return (
        fig,
        f"Factor Performances",
    )


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


@callback(
    Output("cache", "chart"),
    Input("factor-performance-chart", "figure"),
    State("user-universe", "value"),
    State("cache", "chart"),
)
def cache_plt(chart, universe, cache):
    cache = {universe: chart}
    return cache


from functools import lru_cache

# @lru_cache()
# def factor_test(universe: str, periods: int = 21, commission=10):
#     multi_factors = MultiFactors(Universe.from_code(code=universe))
#     performances = multi_factors.to_performance(
#         periods=periods, commission=commission
#     ).ffill()
#     return performances
