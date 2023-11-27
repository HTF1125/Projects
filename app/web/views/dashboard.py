from datetime import date
from dash import html, dcc, callback, Output, Input, State
from app import db
import plotly.express as px
from app.db.models import TbMarketReport
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
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
                    dcc.Loading(
                        dcc.Graph(
                            id="yield-curve-chart",
                            config={"displayModeBar": False},
                        )
                    )
                ),
            ]
        )


@callback(
    Output("yield-curve-chart", "figure"),
    Input("capital-markets-date-range-picker", "value"),
)
def update_output(value):
    yields = db.get_yields()

    start, end = value

    if start is not None:
        yields = yields.loc[start:]
    if end is not None:
        yields = yields.loc[:end]
    n_data = len(yields)
    yields = yields.ffill().iloc[:: n_data // 100, :]
    return px.line(yields)
