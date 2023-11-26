from dash import html
import feffery_antd_components as fac
from ..theme import Theme
from .. import views


def Header():
    return fac.AntdCenter(
        fac.AntdText(
            "ROBERTDASHBOARD",
            style={
                "color": Theme.Color.primary[200],
                "fontWeight": "bold",
                "fontSize": Theme.size[500],
            },
        ),
        style={
            "marginTop": "10px",
            "padding": "5px",
            "width": "100%",
        },
    )


def Sidemenu():
    menuItems = [
        view.menu
        for view in [
            views.Dashboard,
            views.CapitalMarkets,
            views.Factors,
        ]
    ]

    return fac.AntdCol(
        [
            Header(),
            html.Div(
                fac.AntdMenu(
                    menuItems=menuItems,
                    id="router-menu",
                    mode="vertical",
                    style={
                        "fontSize": "16px",
                        "fontColor": "white",
                        "height": "100%",
                        "width": "100%",
                        "border": "0",
                        "paddingBottom": "50px",
                        "backgroundColor": Theme.Color.primary[600],
                    },
                ),
                id="sidemenu",
                style={
                    "width": "250px",
                    "height": "100vh",
                    "transition": "width 0.2s",
                    "paddingRight": "0",
                    "backgroundColor": Theme.Color.primary[600],
                },
            ),
        ],
        style={
            "backgroundColor": Theme.Color.primary[600],
            "marginRight" : "20px",
        },
    )
