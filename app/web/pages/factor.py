import logging
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from app import core
from app.web import components
from app.api import Universe, MultiFactors


logger = logging.getLogger(__name__)


class Factor:
    href = "/factor"

    @classmethod
    def layout(cls):
        return html.Div(
            children=[
                dcc.Store(id="cache", data={}),
                html.H1("Factor Analysis"),
                html.Div(
                    children=[
                        dmc.Group(
                            [
                                dmc.Select(
                                    label="Investment Universe",
                                    data=list(Universe.UNIVERSE.keys()),
                                    id="user-universe",
                                    value=list(Universe.UNIVERSE.keys())[0],
                                    persistence=True,
                                ),
                                dmc.NumberInput(
                                    label="Investment Horizon in Days",
                                    id="user-periods",
                                    value=5,
                                    min=0,
                                    max=250,
                                    step=5,
                                    persistence=True,
                                ),
                                dmc.NumberInput(
                                    label="Trade Commission in bps",
                                    id="user-commission",
                                    value=10,
                                    min=0,
                                    max=100,
                                    step=2,
                                    persistence=True,
                                ),
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
                            # visible=False,
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
    Output("factor-performance-table", "children"),
    Output("factor-chart-title", "children"),
    Input("user-factor-test", "n_clicks"),
    State("user-universe", "value"),
    State("user-periods", "value"),
    State("user-commission", "value"),
)
def compute_factor_data(
    n_clicks: int,
    universe: str,
    periods: int,
    commission: int,
):
    performances = factor_test(
        universe=universe, periods=periods, commission=commission
    )
    mete = pd.concat(
        [
            core.cum_return(performances),
            core.ann_return(performances),
            core.ann_volatility(performances),
            core.ann_sharpe(performances),
        ],
        axis=1,
    ).round(3)
    d = mete.reset_index().sort_values(by="AnnSharpe", ascending=False)

    gg = dag.AgGrid(
        id="cell-double-clicked-grid",
        rowData=d.to_dict("records"),
        columnDefs=[{"field": i} for i in d.columns],
        defaultColDef={
            "resizable": False,
            "sortable": True,
            "filter": True,
            "minWidth": 125,
        },
        columnSize="sizeToFit",
        getRowId="params.data.State",
    )

    fig = go.Figure()
    indices = np.linspace(0, len(performances.index) - 1, 50, dtype=int)
    i_performances = performances.iloc[indices].round(2)

    for f in i_performances:
        i_factor = i_performances[f]
        fig.add_trace(trace=go.Scatter(x=i_factor.index, y=i_factor.values, name=f))
    fig.update_layout(
        # plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color as transparent
        # paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color as transparent
        # showlegend=False,  # Hide the legend for a cleaner border look
        # autosize=False,  # Disable autosizing to maintain border consistency
        # width=600,  # Set the width of the chart
        # height=height,  # Set the height of the chart
        # margin=dict(l=20, r=20),  # Adjust the margins as needed
        # paper_bordercolor='black',  # Set the border color
        # paper_borderwidth=1  # Set the border width
        # hovermode="x unified",
        legend={
            "orientation": "h",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.05,
            "yanchor": "top",
            "itemsizing": "constant",
            # "font": {"size": 12},
        },
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
    )
    return fig, gg, f"Factor Performances Universe: {universe} Forward {periods} Days (comm:{commission:.0f}bps)"


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


@lru_cache()
def factor_test(universe: str, periods: int = 21, commission=10):
    multi_factors = MultiFactors(Universe.from_code(code=universe))
    performances = multi_factors.to_performance(
        periods=periods, commission=commission
    ).ffill()
    return performances
