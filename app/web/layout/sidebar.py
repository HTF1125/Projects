from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
import dash
from ..pages import all_pages


from dash import callback, Output, Input, State


@callback(
    Output("menu-collapse-sider-custom-demo", "collapsed"),
    Output("sidebar-menu-collapse-trigger-icon", "icon"),
    Input("sidebar-menu-collapse-trigger", "nClicks"),
    State("menu-collapse-sider-custom-demo", "collapsed"),
    prevent_initial_call=True,
)
def toggle_sidebar_collapsed(nClicks, collapsed):
    if collapsed:
        return False, "antd-left"
    return True, "antd-right"


def sidebar():
    return fac.AntdSider(
        [
            fac.AntdButton(
                id="sidebar-menu-collapse-trigger",
                icon=fac.AntdIcon(
                    id="sidebar-menu-collapse-trigger-icon",
                    icon="antd-right",
                    style={
                        "fontSize": "14px",
                    },
                ),
                type="text",
                style={
                    "position": "absolute",
                    "zIndex": 1,
                    "top": 0,
                    "right": -26,
                    "backgroundColor": "rgba(0,0,0,0)",
                },
            ),
            fac.AntdMenu(
                menuItems=[
                    {
                        "component": "Item",
                        "props": {
                            "title": page.__name__,
                            "icon": page.icon,
                            "href": page.href,
                        },
                    }
                    for page in all_pages
                ],
                mode="inline",
                style={
                    "height": "100%",
                    "overflow": "hidden auto",
                },
            ),
        ],
        id="menu-collapse-sider-custom-demo",
        collapsible=True,
        collapsedWidth=60,
        trigger=None,
        breakpoint="xl",
        style={"position": "relative", "margin-right": "20px"},
    )
