from dash import html, dcc, callback, Output, Input, State
from app import db
import plotly.express as px
from app.db.models import TbMarketReport
import dash_bootstrap_components as dbc
from .. import components


class Page:
    ...


class Dashboard(Page):
    menu = {
        "component": "Item",
        "props": {
            "key": "/Dashboard",
            "name": "/Dashboard",
            "title": "Dashboard",
            "href": "/Dashboard",
            "icon": "antd-dot-chart",
        },
    }

    def layout(self):
        rep = TbMarketReport.latest()[-1]["content"]
        return html.Div(
            children=[
                html.H1("Market Briefing", style={"text-align": "center"}),
                html.Hr(),
                dbc.Placeholder(
                    children=dbc.Card(
                        dbc.CardBody(
                            children=dcc.Markdown(
                                children=rep,
                                style={
                                    "font-size": "18px",
                                    "font-family": "Calibri",
                                },
                            )
                        )
                    )
                ),
                html.P(""),  # Add an empty paragraph for line break
            ]
        )


class CapitalMarkets(Page):
    menu = {
        "component": "Item",
        "props": {
            "key": "/CapitalMarkets",
            "name": "/CapitalMarkets",
            "title": "CapitalMarkets",
            "href": "/CapitalMarkets",
            "icon": "antd-dot-chart",
        },
    }

    def layout(self):
        return html.Div(
            children=[
                components.DateRangePicker(
                    id="capital-markets-date-range-picker",
                    persistence=True,
                ),
                html.Div(
                    [
<<<<<<< HEAD
                        dcc.Loading(
                            dcc.Graph(
                                id="us-yields",
                                config={"displayModeBar": False},
                            )
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id="s&p500-chart",
=======
                        dcc.Loading(id="yield-curve-loader"),
                        dcc.Loading(
                            dcc.Graph(
                                figure=px.line(
                                    db.get_sp500()
                                    .pct_change(252)
                                    .rolling(252 * 10)
                                    .mean()
                                ),
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
                                config={"displayModeBar": False},
                            )
                        ),
                    ]
                ),
            ]
        )


@callback(
<<<<<<< HEAD
    Output("us-yields", "figure"),
    Output("s&p500-chart", "figure"),
=======
    Output("yield-curve-loader", "children"),
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
    Input("capital-markets-date-range-picker", "value"),
)
def update_output(value):
    yields = db.get_yields()
<<<<<<< HEAD
    start, end = value
=======

    start, end = value

>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
    if start is not None:
        yields = yields.loc[start:]
    if end is not None:
        yields = yields.loc[:end]
    n_data = len(yields)
    yields = yields.ffill().iloc[:: n_data // 100, :]
<<<<<<< HEAD
    fig1 = px.line(yields)
    fig2 = px.line(db.get_sp500().pct_change(252).rolling(252 * 10).mean())

    return fig1, fig2
=======
    return dcc.Graph(
        id="yield-curve-chart",
        config={"displayModeBar": False},
        figure=px.line(yields),
        style={"min-height": "300px"},
    )
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
