from typing import Optional
from dash import html
import feffery_antd_components as fac
from ..theme import Theme


def Title():
    return html.Div(
        fac.AntdSpace(
            [
                fac.AntdText(
                    id="title",
                    style={
                        "color": Theme.Color.secondary[300],
                        "fontWeight": "bold",
                        "fontSize": Theme.size[500],
                    },
                ),
                fac.AntdText(
                    id="subtitle",
                    style={
                        "color": Theme.Color.secondary[100],
                        "fontSize": Theme.size[300],
                    },
                ),
            ],
            size=0,
            direction="vertical",
            style={
                "marginleft": Theme.size[100],
            },
        )
    )


def RightMenu():
    return html.Div(
        fac.AntdSpace(
            [
                fac.AntdAvatar(icon=icon, style={"background": "#4551f5"})
                for icon in [
                    "antd-user",
                    "antd-team",
                    "antd-github",
                ]
            ],
            size="small",
            direction="horizontal",
            align="center",
        )
    )


def Topmenu():
    return fac.AntdRow(
        [
            Title(),
            fac.AntdCol(RightMenu()),
        ],
        justify="space-between",
        align="middle",
        style={
            "paddingLeft": "20px",
            "paddingRight": "100px",
        },
    )
