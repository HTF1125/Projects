# from dash import Dash, dcc, html

# from app.web import pages, components


from dash import Dash, html, dcc
from dash import Output, Input, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from . import components
from . import views


import logging

logger = logging.getLogger(__name__)
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
            # dcc.Store(id="global-cache"),
            # dcc.Interval(
            #     id="factor-test-interval",
            #     interval=24 * 60 * 60 * 1000,
            #     n_intervals=1,
            #     disabled=False,
            # ),
            fuc.FefferyReload(id="global-reload", delay=300),
            dcc.Store(id="side-props-width", storage_type="local"),
            # Insert sidemenu scroll to current key
            html.Div(id="side-div-scroll-to-current-key"),
            # Insert scroll while page initalize.
            html.Div(id="page-anchor-scroll-to-while-page-initial"),
            components.Reloader(),
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

    pathname = pathname.replace("/", "")
    if pathname == "":
        pathname = "Dashboard"
    return (
        getattr(views, pathname)().layout(),
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


# from dash import callback, no_update
# from .callbacks.manager import manager


# @callback(
#     Output("global-cache", "data"),
#     Input("factor-test-interval", "n_intervals"),
#     State("global-cache", "data"),
#     prevent_initial_call=False,
#     background=True,
#     manager=manager,
#     running=[
#         (Output("factor-test-interval", "disabled"), True, False),
#     ],
# )
# def handle_background_factor_test(n_intervals, cache):
#     import app
#     import json
#     import logging

#     logger = logging.getLogger(f"{__name__}.background")

#     if not n_intervals:
#         logger.warning(f"Update Factor Not Run. n_intervals = {n_intervals}")
#         return no_update

#     if cache is not None:
#         cache = json.loads(cache)
#         app.api.Universe.from_store(cache.get("factor-test"))

#     for universe in app.api.Universe.UNIVERSE.keys():
#         uni = app.api.Universe.from_code(code=universe)
#         funcs = {
#             f: getattr(app.api.funcs.factors, f) for f in app.api.funcs.factors.__all__
#         }
#         uni.multi_factors.append(funcs=funcs, periods=1)
#     logger.info(f"Update Factor Complete {n_intervals}")
#     out = app.api.Universe.get_class_store()
#     out_json = json.dumps({"factor-test": out})
#     logger.info(out_json[:200])
#     return out_json
