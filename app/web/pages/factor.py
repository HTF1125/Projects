import logging
from dash import html, dcc, callback, Output, Input, State
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.core import stats
from app.api import universes, factors
from app.web import components


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
                    dcc.Dropdown(
                        options=universes.__all__,
                        placeholder="Select an Investment Universe",
                        id="universe-dropdown",
                        persistence=True,
                    ),
                    style={"flex": 1, "padding": "0px 5px"},
                ),
                components.Container(
                    [
                        dcc.Loading(
                            dcc.Graph(
                                figure=blank_fig(),
                                id="factor-performance-chart",
                                config={"displayModeBar": False},
                            )
                        )
                    ]
                ),
                html.Div(id="factor-performance-stats"),
            ]
        )


import dash_ag_grid as dag


@callback(
    Output("factor-performance-chart", "figure"),
    Input("universe-dropdown", "value"),
    State("cache", "data"),
)
def compute_factor_data(universe: str, cache: dict):
    if universe in cache:
        if "chart" in cache[universe]:
            return cache[universe]["chart"]
    cls = getattr(universes, universe)
    if issubclass(cls, universes.Universe):
        ins = cls().add_factors(*factors.__all__)
        perfs = pd.concat(
            [factor.to_performance() for _, factor in ins.factors.items()], axis=1
        )
        mete = pd.concat(
            [
                stats.cum_return(perfs),
                stats.ann_return(perfs),
                stats.ann_volatility(perfs),
                stats.ann_sharpe(perfs),
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

        for f_name, f_instance in ins.factors.items():
            _perf = f_instance.to_performance()
            indices = np.linspace(0, _perf.shape[0] - 1, 50, dtype=int)
            _perf = _perf.iloc[indices]
            fig.add_trace(
                trace=go.Scatter(
                    x=_perf.index,
                    y=_perf.values,
                    name=f_name,
                )
            )
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
        return fig


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


@callback(
    Output("cache", "data"),
    Input("factor-performance-chart", "figure"),
    State("universe-dropdown", "value"),
    State("cache", "data"),
)
def cache_plt(chart, universe, cache):
    if universe not in cache:
        cache[universe] = {}
    cache[universe].update({"chart": chart})
    return cache
