"""











"""


from dash import html, dcc, callback, Output, Input, State, no_update
import feffery_antd_components as fac
import plotly.graph_objects as go
from app.api import signals
from app.web.views.base import Page


class Signals(Page):
    menu = {
        "component": "Item",
        "props": {
            "key": "/Signals",
            "name": "/Signals",
            "title": "Signals",
            "href": "/Signals",
            "icon": "antd-dot-chart",
        },
    }

    def layout(self):
        return html.Div(
            children=[
                html.H1("Dynamic Allocation Signals"),
                fac.AntdRow(
                    children=[
                        self.get_universe(),
                        self.get_signal(),
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
                    fac.AntdButton("Test Signal", id="user-signal-test"),
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
                html.Div(id="signal-chart"),
            ]
        )


@callback(
    Output("signal-chart", "children"),
    Input("user-signal-test", "nClicks"),
    State("user-universe", "value"),
    State("user-signal", "value"),
    prevent_initial_call=True,
)
def handle_chart(nClicks, universe, signal):
    signal_ins = getattr(signals, signal)
    if issubclass(signal_ins, signals.Signal):
        return html.Div(
            dcc.Loading(
                dcc.Graph(
                    figure=signal_ins.create(universe).plot(),
                    config={"displayModeBar": False},
                )
            )
        )
    return no_update
