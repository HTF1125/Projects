from dash import html
import feffery_antd_components as fac


class MainLayout(fac.AntdLayout):
    style = {
        "height": "100%",
    }


class HeaderLayout(fac.AntdHeader):
    style = {
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
    }


class SidebarLayout(fac.AntdSider):
    style = {
        "position": "relative",
    }
    id = "sidebar-menu"
    collapsible = True
    collapseWidth = 60


class SidebarMenuButton(fac.AntdButton):
    style = {
        "position": "aboslute",
        "zIndex": 1,
        "top": 25,
        "right": -13,
        "box-shadow": "rgb(0 0 0 / 10%) 0px 4px 10px 0px",
        "background": "white",
    }


class FooterLayout(fac.AntdFooter):
    style = {
        "backgroundColor": "rgb(193, 193, 193)",
        "height": "40px",
    }


from .sidebar import sidebar


def PageLayout():
    return html.Div(
        [
            # fac.AntdHeader(
            #     fac.AntdTitle(
            #         "Header", level=2, style={"color": "white", "margin": "0"}
            #     ),
            #     style={
            #         "display": "flex",
            #         "justifyContent": "center",
            #         "alignItems": "center",
            #     },
            # ),
            fac.AntdLayout(
                [
                    sidebar(),
                    fac.AntdLayout(
                        [
                            fac.AntdContent(
                                html.Div(id="content-section", style={"margin":"20px"})
                            ),
                            # fac.AntdFooter(
                            #     html.Div(
                            #         fac.AntdTitle(
                            #             "Footer", level=2, style={"margin": "0"}
                            #         ),
                            #         style={
                            #             "display": "flex",
                            #             "height": "100%",
                            #             "justifyContent": "center",
                            #             "alignItems": "center",
                            #         },
                            #     ),
                            #     style={
                            #         "backgroundColor": "rgb(193, 193, 193)",
                            #         "height": "40px",
                            #         "justifyContent": "center",
                            #         "alignItems": "center",
                            #         "position": "relative",
                            #         "bottom": 0,
                            #     },
                            # ),
                        ],
                        style={
                            "height": "100%",
                        },
                    ),
                ],
                style={"height": "100%"},
            ),
        ],
        className="sider-demo",
        style={"height": "100%", "border": "1px solid rgb(241, 241, 241)"},
    )
