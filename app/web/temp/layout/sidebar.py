from typing import Optional
import dash
import feffery_antd_components as fac
from ..pages import all_pages


def SidebarCollapseIcon():
    return fac.AntdIcon(
        id="sidebar-collapse-icon", icon="antd-right", style={"fontSize": 14}
    )


def SidebarCollapseButton():
    style = {
        "position": "absolute",
        "zIndex": 1,
        "top": 0,
        "right": -26,
        "backgroundColor": "rgba(0, 0, 0, 0)",
    }

    return fac.AntdButton(
        id="sidebar-collapse-trigger",
        type="text",
        icon=SidebarCollapseIcon(),
        style=style,
    )


def SidebarMenu(menuItems):
    style = {
        "height": "100%",
        "overflow": "hidden auto",
    }

    return fac.AntdMenu(menuItems=menuItems, model="inline", style=style)


def SideBar(
    id="sidebar",
    collapsible: bool = True,
    collapseWidth: int = 60,
    trigger=None,
    breakpoint: str = "xl",
):
    menuItems = [
        {
            "component": "Item",
            "props": {
                "title": page.__name__,
                "icon": page.icon,
                "href": page.href,
            },
        }
        for page in all_pages
    ]

    style = {
        "position": "relative",
        "margin-right": "20px",
    }
    return fac.AntdSider(
        children=[SidebarCollapseButton(), SidebarMenu(menuItems)],
        id=id,
        trigger=trigger,
        collapsible=collapsible,
        collapsedWidth=collapseWidth,
        breakpoint=breakpoint,
        style=style,
    )


@dash.callback(
    dash.Output("sidebar", "collapsed"),
    dash.Output("sidebar-collapse-icon", "icon"),
    dash.Input("sidebar-collapsee-trigger", "nClicks"),
    dash.State("sidebar", "collapsed"),
    prevent_initial_call=True,
)
def toggle_sidebar_collapsed(nClicks: int, collased: bool):
    if collased:
        return (False, "antd-left")
    return (True, "antd-right")
