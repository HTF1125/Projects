"""











"""


from dash import html, dcc, callback, Output, Input, State, no_update
import feffery_antd_components as fac
import dash_mantine_components as dmc
import plotly.graph_objects as go
from .factors import get_universe

from app.api import signals


class Signals:
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

    @staticmethod
    def get_signals():
        options = signals.__all__

        return fac.AntdSelect(
            id="user-signal",
            defaultValue=options[0],
            options=[{"label": value, "value": value} for value in options],
            style={
                "width": 200,
            },
        )

    def layout(self):
        return html.Div(
            children=[
                html.H1("Dynamic Allocation Signals"),
                get_universe(),
                self.get_signals(),
                html.Div(
                    fac.AntdButton("Test Signal", id="user-signal-test"),
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
                dcc.Loading(
                    children=[
                        dcc.Graph(
                            figure=blank_fig(),
                            id="signal-performance-chart",
                            config={"displayModeBar": False},
                            # style={
                            #     "max-width" : "500px",
                            # }
                        ),
                    ],
                ),
            ]
        )


@callback(
    Output("signal-performance-chart", "figure"),
    Input("user-signal-test", "nClicks"),
    State("user-universe", "value"),
    State("user-signal", "value"),
    prevent_initial_call=True,
)
def handle_chart(nClicks, universe, signal):
    signal_ins = getattr(signals, signal)
    if issubclass(signal_ins, signals.Signal):

        return signal_ins.create(universe).plot()
    return no_update


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig
