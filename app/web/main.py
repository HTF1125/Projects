from dash import Dash, dcc, html
from dash import callback, Output, Input, State
from app.web import pages, components


app = Dash(
    name=__name__,
    title="RobertDashboard",
    suppress_callback_exceptions=True,
)

server = app.server
from .layout import PageLayout


@callback(
    Output("content-section", "children"),
    Input("url", "pathname"),
)
def display(pathname: str):
    for page in pages.all_pages:
        if page.href.startswith(pathname):
            return page.layout()
    raise


app.layout = components.GlobalLayout(
    children=[
        dcc.Store(id="store"),
        dcc.Store(id="status"),
        dcc.Location(id="url", refresh=False),
        PageLayout(),
        components.MainLayout(id="page"),
    ],
)



app.clientside_callback(
    """
    function(trigger) {
        //  can use any prop to trigger this callback - we just want to store the info on startup
        const inner_width  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        const inner_height = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;
        const screenInfo = {height :screen.height, width: screen.width, in_width: inner_width, in_height: inner_height};
        return screenInfo
    }
    """,
    Output("store", "data"),
    Input("store", "data"),
)
