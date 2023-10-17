import logging
from dash import html, dcc, callback, Output, Input, State
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.core import factors, universes, stats
from app.web import components


logger = logging.getLogger(__name__)


class Factor:
    href = "/factor"

    @classmethod
    def layout(cls):
        return html.Div(
            children=[
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
    Output("factor-performance-stats", "children"),
    Input("universe-dropdown", "value"),
)
def compute_factor_data(universe: str):
    cls = getattr(universes, universe)
    if issubclass(cls, universes.Universe):
        ins = cls.instance().add_factor(*factors.__all__)
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
        data = mete.reset_index().sort_values(by="AnnSharpe", ascending=False)

        gg = dag.AgGrid(
            id="cell-double-clicked-grid",
            rowData=data.to_dict("records"),
            columnDefs=[{"field": i} for i in data.columns],
            defaultColDef={
                "resizable": False,
                "sortable": True,
                "filter": True,
                "minWidth": 125,
            },
            columnSize="sizeToFit",
            getRowId="params.data.State",
        )

        indices = np.linspace(0, perfs.shape[0] - 1, 50, dtype=int)
        perf_fig = px.line(perfs.iloc[indices])
        return perf_fig, gg


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig
