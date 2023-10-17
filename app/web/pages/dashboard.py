from datetime import date

from dash import html, dcc, callback, Output, Input, State
from app import database
import plotly.express as px


class Dashboard:
    href = "/"

    @classmethod
    def layout(cls):
        return (html.H1(__name__),)


class CapitalMarkets:
    href = "/capitalmarkets"

    @classmethod
    def layout(cls):
        return html.Div(
            children=[
                html.H1(__name__),
                dcc.DatePickerRange(
                    id="my-date-picker-range",
                    start_date=date(2018, 1, 1),
                    max_date_allowed=date.today(),
                    end_date=date.today(),
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
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
)
def update_output(start_date, end_date):
    yields = database.get_yields()
    if start_date is not None:
        yields = yields.loc[start_date:]
    if end_date is not None:
        yields = yields.loc[:end_date]
    n_data = len(yields)
    yields = yields.ffill().iloc[:: n_data//100, :]
    return px.line(yields)
