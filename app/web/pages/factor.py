import logging
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import core
from app.web import components
from app.api import Universe, MultiFactors


style = {
    "height": 100,
    # "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "marginTop": 20,
    "marginBottom": 20,
    "display": "flex",
}


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
                                    style={"width": 200},
                                    persistence=True,
                                ),
                                dmc.NumberInput(
                                    label="Investment Horizon in Days",
                                    id="user-periods",
                                    value=5,
                                    min=0,
                                    max=250,
                                    step=5,
                                    style={"width": 200},
                                    persistence=True,
                                ),
                                dmc.NumberInput(
                                    label="Trade Commission in bps",
                                    id="user-commission",
                                    value=10,
                                    min=0,
                                    max=100,
                                    step=2,
                                    style={"width": 200},
                                    persistence=True,
                                ),
                            ],
                            style=style,
                        ),
                        html.Div(
                            dmc.Button(
                                "Load from database",
                                id="user-start-test",
                                leftIcon=DashIconify(
                                    icon="fluent:database-plug-connected-20-filled"
                                ),
                                style={
                                    "marginTop": 20,
                                    "marginBottom": 20,
                                    "text-align": "right",
                                },
                            ),
                            style={"display": "flex", "justify-content": "flex-end"},
                        ),
                    ],
                ),
                components.Container(
                    [
                        dcc.Loading(
                            dcc.Graph(
                                figure=blank_fig(),
                                id="factor-performance-chart",
                                config={"displayModeBar": False},
                            ),
                        ),
                        html.Div(id="factor-performance-table"),
                    ]
                ),
                html.Div(id="factor-performance-stats"),
            ]
        )


import dash_ag_grid as dag


@callback(
    Output("factor-performance-chart", "figure"),
    Output("factor-performance-table", "children"),
    Input("user-universe", "value"),
    State("user-periods", "value"),
    State("user-commission", "value"),
    State("cache", "chart"),
    State("cache", "table"),
)
def compute_factor_data(
    universe: str,
    periods: int,
    commission: int,
    cache_chart: dict,
    cache_table: dict,
):
    if cache_chart is not None and cache_table is not None:
        if (
            cache_chart.get(universe) is not None
            and cache_table.get(universe) is not None
        ):
            return cache_chart.get(universe), cache_table.get(universe)

    multi_factors = MultiFactors(Universe.from_code(code=universe))
    performances = multi_factors.to_performance(
        periods=periods, commission=commission
    ).ffill()

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
            "y": -0.3,
            "yanchor": "top",
            "itemsizing": "constant",
            # "font": {"size": 12},
        },
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
    )
    return fig, gg


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


@callback(
    Output("cache", "table"),
    Input("factor-performance-table", "children"),
    State("user-universe", "value"),
    State("cache", "table"),
)
def cache_table(table, universe, cache):
    cache = {universe: table}
    return cache
