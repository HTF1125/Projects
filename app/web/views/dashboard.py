"""



"""


from dash import html, dcc, callback, Output, Input
import plotly.express as px
from app import db
from .. import components
from .base import Page


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
        # rep = TbMarketReport.latest()[-1]["content"]
        return html.Div(
            children=[
                html.H1("Market Briefing", style={"text-align": "center"}),
                html.Hr(),
                # dbc.Placeholder(
                #     children=dbc.Card(
                #         dbc.CardBody(
                #             children=dcc.Markdown(
                #                 children=rep,
                #                 style={
                #                     "font-size": "18px",
                #                     "font-family": "Calibri",
                #                 },
                #             )
                #         )
                #     )
                # ),
                html.P("UnderDevelopment..."),  # Add an empty paragraph for line break
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
                        dcc.Loading(
                            dcc.Graph(
                                id="us-yields",
                                config={"displayModeBar": False},
                            )
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id="s&p500-chart",
                                config={"displayModeBar": False},
                            )
                        ),
                    ]
                ),
            ]
        )


@callback(
    Output("us-yields", "figure"),
    Output("s&p500-chart", "figure"),
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
    fig1 = px.line(yields)
    fig2 = px.line(db.get_sp500().pct_change(252).rolling(252 * 10).mean())
    return fig1, fig2
