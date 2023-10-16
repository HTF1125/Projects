import logging
from dash import html, dcc, callback, Output, Input, State
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
                                id="factor-backtest-performance",
                                config={"displayModeBar": False},
                            )
                        )
                    ]
                ),
                # components.Container(
                #     dcc.Loading(
                #         # components.Table(
                #         #     id="factor-table",
                #         #     page_size=10,
                #         #     sort_action="native",
                #         #     sort_mode="multi",
                #         #     page_action="native",
                #         # ),
                #     ),
                # ),
                html.Div(id="table-factor-result")

            ]
        )


    @staticmethod
    def get_input():
        return html.Div(
            children=[
                html.Div(
                    dcc.Dropdown(
                        options=universes.__all__,
                        placeholder="Select an Investment Universe",
                        id="universe-dropdown",
                        persistence=True,
                    ),
                    style={"flex": 1, "padding": "0px 5px"},
                ),
                html.Div(
                    dcc.Dropdown(
                        options=factors.__all__,
                        placeholder="Select an Investment Factor",
                        id="factor-dropdown",
                        persistence=True,
                    ),
                    style={"flex": 1, "padding": "0px 5px"},
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "space-between",
                "align-items": "center",
                "padding": "10px 20px",
            },
        )

import dash_ag_grid as dag


@callback(
    # Output("factor-table", "data"),
    # Output("factor-table", "columns"),
    Output("table-factor-result", "children"),
    Output("factor-backtest-performance", "figure"),
    Input("universe-dropdown", "value"),
)
def get_factor_table(universe: str):

    uni_instance = getattr(universes, universe)()
    uni_instance.add_factor(*factors.__all__)
    perfs = [
        factor.to_performance()
        for name, factor in uni_instance.cache["factors"].items()
    ]
    perfs = pd.concat(perfs, axis=1)
    perf_fig = px.line(perfs)
    perfs = pd.concat(
        [
            stats.cum_return(perfs),
            stats.ann_return(perfs),
            stats.ann_volatility(perfs),
            stats.ann_sharpe(perfs),
        ],
        axis=1,
    ).round(3)
    data = perfs.reset_index()

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


    return (gg, perf_fig)


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig
