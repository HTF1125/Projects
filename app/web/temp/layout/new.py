import feffery_antd_components as fac


class Sidebar(fac.AntdSider):
    trigger = None
    breakposint = ("xl",)
    collapsible = True
    collapseWidth = 60
    id = "sidebar"
    style = dict(
        display="flex",
        justifyContent = "center",
    )


class SidebarMenu(fac.AntdMenu):
    model = "inline"
    style = dict(
        height="100%",
        overflow="hidden auto",
    )


class Button(fac.AntdButton):
    ...


class Icon(fac.AntdIcon):
    ...


class SidebarCollapsedIcon(Icon):
    id = "sidebar-collapse-icon"
    icon = "antd-right"
    style = dict(
        fontSize="14px",
    )


class SidebarCollapseButton(Button):
    style = dict(
        position="absolute",
        zIndex=1,
        top=0,
        right=-25,
        backgroundColor="rgba(0, 0, 0, 0)",
    )
    type = "text"

    id = "sidebar-collapse-button"



class AffixLeft(fac.AntdAffix):

