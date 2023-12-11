from dash import html
from dash import callback, Output, Input, State
import feffery_antd_components as fac
from .. import views


def CollapseButton():
    return fac.AntdButton(
        fac.AntdIcon(
            id="side-menu-collapse-icon",
            icon="antd-arrow-left",
        ),
        id="side-menu-collapse-button",
        type="text",
        shape="circle",
        style={
            "position": "absolute",
            "zIndex": 999,
            "top": "10px",
            "right": "-15px",
            "boxShadow": "0 4px 10px 0 rgba(0,0,0,.1)",
            "background": "white",
        },
    )


def Header():
    return fac.AntdCenter(
        fac.AntdText(
            "ROBERTDASHBOARD",
            id="side-menu-header",
            style={
                "fontWeight": "bold",
                "fontSize": "36px",
            },
        ),
        style={
            "marginTop": "10px",
            "padding": "5px",
            "width": "100%",
            "minHeight": "50px",
        },
    )


def SideMenu():
    menuItems = [
        view.menu
        for view in [
            views.Dashboard,
            views.CapitalMarkets,
            views.Signals,
            views.Factors,
        ]
    ]

    return fac.AntdCol(
        [
            html.Div(
                [
                    Header(),
                    CollapseButton(),
                    fac.AntdMenu(
                        menuItems=menuItems,
                        id="router-menu",
                        mode="vertical",
                        currentKey="/Dashboard",
                        style={
                            "fontSize": "16px",
                            "fontColor": "white",
                            "height": "100%",
                            "width": "100%",
                            "border": "0",
                            "paddingBottom": "50px",
                        },
                    ),
                ],
                id="side-menu",
                style={
                    "width": "250px",
                    "height": "100vh",
                    "transition": "width 0.2s",
                    "paddingRight": "0",
                },
            ),
        ],
        style={
            "marginRight": "20px",
        },
    )


@callback(
    [
        Output("side-menu", "style"),
        Output("side-menu-collapse-icon", "icon"),
        Output("side-menu-header", "children"),
    ],
    Input("side-menu-collapse-button", "nClicks"),
    State("side-menu", "style"),
    prevent_initial_call=True,
)
def handle_side_menu_collapse(nClicks, style):
    if nClicks:
        if style.get("width") == "250px":
            style.update({"width": "35px"})
            return (style, "antd-arrow-right", None)
        style.update({"width": "250px"})
        return (style, "antd-arrow-left", "ROBERTDASHBOARD")


@callback(
    Output("router-menu", "currentKey"),
    Input("url", "pathname"),
)
def handle_router_menu_key(pathname):
    print(pathname)
    if pathname == "/":
        pathname = "/Dashboard"
    return pathname
