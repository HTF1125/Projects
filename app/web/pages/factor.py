import logging
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from app import core
from app.api import Universe
from .. import components
from app.api import factor


logger = logging.getLogger(__name__)

from .dashboard import Page


class Factor(Page):
    href = "/factor"
    icon = "antd-dot-chart"

    @classmethod
    def layout(cls):
        return html.Div(
            children=[
                dcc.Store(id="cache", data={}),
                html.H1("Factor Analysis"),
                html.Div(
                    children=[
                        components.get_factor_args(),
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


import dash_ag_grid as dag


@callback(
    Output("factor-performance-chart", "figure"),
    Output("factor-chart-title", "children"),
    Input("user-factor-test", "n_clicks"),
    State("user-universe", "value"),
    State("user-periods", "value"),
    State("user-factor", "value"),
)
def compute_factor_data(
    n_clicks: int,
    universe: str,
    periods: int,
    factor: str,
):
    uni = Universe.from_code(universe)
    uni.f.append(factor, periods=periods)
    # performances = factor_test(
    #     universe=universe, periods=periods, commission=commission
    # )
    # mete = pd.concat(
    #     [
    #         core.cum_return(performances),
    #         core.ann_return(performances),
    #         core.ann_volatility(performances),
    #         core.ann_sharpe(performances),
    #     ],
    #     axis=1,
    # ).round(3)
    # d = mete.reset_index().sort_values(by="AnnSharpe", ascending=False)

    # gg = dag.AgGrid(
    #     id="cell-double-clicked-grid",
    #     rowData=d.to_dict("records"),
    #     columnDefs=[{"field": i} for i in d.columns],
    #     defaultColDef={
    #         "resizable": False,
    #         "sortable": True,
    #         "filter": True,
    #         "minWidth": 125,
    #     },
    #     columnSize="sizeToFit",
    #     getRowId="params.data.State",
    # )

    # fig = go.Figure()
    # indices = np.linspace(0, len(performances.index) - 1, 50, dtype=int)
    # i_performances = performances.iloc[indices].round(2)

    # for f in i_performances:
    #     i_factor = i_performances[f]
    #     fig.add_trace(trace=go.Scatter(x=i_factor.index, y=i_factor.values, name=f))
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
