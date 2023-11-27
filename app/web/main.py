# from dash import Dash, dcc, html

# from app.web import pages, components


from dash import Dash, html, dcc
from dash import Output, Input, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from . import components
from .theme import Theme
from . import views



app = Dash(
    name=__name__,
    title="RobertDashboard",
    suppress_callback_exceptions=True,
)

server = app.server


app.layout = fuc.FefferyTopProgress(
    fuc.FefferyDiv(
        [
            dcc.Location(id="url"),
            fuc.FefferyReload(id="global-reload", delay=300),
            dcc.Store(id="side-props-width", storage_type="local"),
            # Insert sidemenu scroll to current key
            html.Div(id="side-div-scroll-to-current-key"),
            # Insert scroll while page initalize.
            html.Div(id="page-anchor-scroll-to-while-page-initial"),
            components.Reloader(),
            # top_section(),
            fac.AntdRow(
                [
                    components.SideMenu(),
                    fac.AntdCol(
                        [
                            components.Topmenu(),
                            fuc.FefferyDiv(
                                # html.Div(style={"minHeight": "100vh"}),
                                id="docs-content",
                                # style={"backgroundColor": "rgb(255, 255, 255)", "padding": "30px"},
                            ),
                        ],
                        flex="auto",
                    ),
                ],
                wrap=False,
            ),
        ],
    )
)


@app.callback(
    [
        Output("docs-content", "children"),
        Output("docs-content-spin-center", "key"),
        Output("page-header", "title"),
        Output("page-header", "subTitle"),
    ],
    Input("url", "pathname"),
)
def render_docs_content(pathname):
    """路由回调"""
    import uuid
    import time

    pathname = pathname.replace("/", "")
    if pathname == "":
        pathname = "dashboard"
    time.sleep(0.3)
    try:
        return (
            getattr(views, pathname)().layout(),
            str(uuid.uuid4()),
            pathname,
            f"Welcom to {pathname}",
        )
    except:
        return (
            fac.AntdText("Error"),
            str(uuid.uuid4()),
            pathname,
            f"Welcom to {pathname}",
        )


@app.callback(
    Output("page-anchor-scroll-to-while-page-initial", "children"),
    Input("docs-content-spin-center", "key"),
    State("url", "hash"),
)
def page_anchor_scroll_to_while_page_initial(_, hash_):
    if _ and hash_:
        from urllib.parse import unquote

        targetId = unquote(hash_)[1:]
        return fuc.FefferyScroll(
            scrollTargetId=targetId,
            scrollMode="target",
            executeScroll=True,
            offset=0,
        )


# @app.callback(
#     [
#         Output("side-div", "style"),
#         Output("side-div-collapse-icon", "icon"),
#     ],
#     Input("side-div-collapse-button", "nClicks"),
#     State("side-div", "style"),
#     prevent_initial_call=True,
# )
# def handle_side_menu_collapse(n_clicks, style):
#     if n_clicks:
#         if style["width"] == "325px":
#             return [
#                 {
#                     "width": "80px",
#                     "height": "100vh",
#                     "transition": "width 0.2s",
#                     "borderRight": "1px solid rgb(240, 240, 240)",
#                 },
#                 "antd-arrow-right",
#             ]
#         return [
#             {
#                 "width": "325px",
#                 "height": "100vh",
#                 "transition": "width 0.2s",
#                 "borderRight": "1px solid rgb(240, 240, 240)",
#             },
#             "antd-arrow-left",
#         ]
