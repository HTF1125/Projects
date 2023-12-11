import plotly.graph_objects as go
import feffery_antd_components as fac
from app import db
from app.api import signals, factors


class Page:
    @staticmethod
    def get_universe():
        options = list(db.get_universe().index.unique())

        return fac.AntdSelect(
            id="user-universe",
            defaultValue=options[0],
            options=[{"label": value, "value": value} for value in options],
            style={
                "width": 200,
                "margin": 10,
            },
        )

    @staticmethod
    def get_signal():
        options = signals.__all__

        return fac.AntdSelect(
            id="user-signal",
            defaultValue=options[0],
            options=[{"label": value, "value": value} for value in options],
            style={
                "width": 200,
            },
        )

    @staticmethod
    def get_factor():
        options = list(factors.__all__)
        return fac.AntdSelect(
            id="user-factor",
            defaultValue=options[0],
            options=[{"label": value, "value": value} for value in options],
            style={
                "width": 200,
            },
        )

    @staticmethod
    def blank_fig() -> go.Figure:
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig
