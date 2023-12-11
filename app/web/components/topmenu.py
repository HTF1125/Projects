from dash import html
import feffery_antd_components as fac


def Title():
    return fac.AntdCol(
        fac.AntdPageHeader(
            id="page-header",
            style={
                "padding": 0,
                "margin": 0,
                "font": "Calibri",
            },
        )
    )


def RightMenu():
    return fac.AntdCol(
        html.Div(
            fac.AntdSpace(
                [
                    fac.AntdAvatar(
                        icon=icon,
                        # style={"background": "#4551f5"},
                    )
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
    )


def Topmenu():
    return fac.AntdRow(
        [Title(), RightMenu()],
        justify="space-between",
        align="middle",
        style={
            "padding": "5px",
        },
        wrap=False,
    )
